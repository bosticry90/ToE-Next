"""Bounded scalar-only Stage 1 search using affine Hessian blocks.

At fixed VEV ratios the three tadpole masses are affine in the remaining
action coefficients. Thus physical Hessian positivity is a small SDP, not a
blind 33-dimensional optimization. This is exploratory numerical evidence;
any survivor still needs exact-parent, higher-precision independent replay.
"""

from pathlib import Path
import sys

import cvxpy as cp
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from parent_bilinear_oracle import REAL_NAMES, COMPLEX_NAMES
from compile_numeric_blocks import SLOTS

OMEGA = np.sqrt(60.0)
FREE = ("mphi2", "muPhi", "muPhiPhi") + REAL_NAMES[6:] + tuple(
    name + ":re" for name in COMPLEX_NAMES) + tuple(
    name + ":im" for name in COMPLEX_NAMES)
assert len(FREE) == 31 and len(SLOTS) == 34

DEGREES = {
    "mSigma2": (2, 0), "mS2": (0, 2),
    "lambdaPhiSigma1": (2, 0), "lambdaPhiSigma2": (2, 0),
    "lambdaPhiS": (0, 2),
    **{name: (4, 0) for name in
       ("lambdaSigma1", "lambdaSigma2", "lambdaSigma3", "lambdaSigma4")},
    "lambdaSigmaphi1": (2, 0), "lambdaSigmaphi2": (2, 0),
    "lambdaSigmaS": (2, 2), "lambdaVectorS": (0, 2),
    "lambdaS": (0, 4), "z6": (0, 1), "z4": (2, 1),
    "zK": (0, 1), "zEta": (3, 0), "zD": (2, 0),
}


def parent_coefficients(values, x, y):
    """Numeric parent coefficients at omega and chosen VEV ratios."""
    z = dict(zip(FREE, values))
    c = {name: z[name] for name in REAL_NAMES if name in z}
    for name in COMPLEX_NAMES:
        c[name] = z[name + ":re"] + 1j * z[name + ":im"]
    c["mphi2"] *= OMEGA**2
    c["muPhi"] *= OMEGA
    c["muPhiPhi"] *= OMEGA
    c["z6"] *= OMEGA
    sigma, vs = x * OMEGA, y * OMEGA
    lphi = c["lambdaPhi1"] + 7*c["lambdaPhi2"]/60
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    c["mPhi2"] = (-1.5*c["muPhi"]*OMEGA/OMEGA
                   -2*lphi*OMEGA**2-lmix*sigma**2
                   -0.5*c["lambdaPhiS"]*vs**2)
    c["mSigma2"] = (-lmix*OMEGA**2-2*c["lambdaSigma1"]*sigma**2
                    -0.5*c["lambdaSigmaS"]*vs**2)
    c["mS2"] = (-c["lambdaPhiS"]*OMEGA**2
                -c["lambdaSigmaS"]*sigma**2-c["lambdaS"]*vs**2)
    assert set(c) == set(REAL_NAMES) | set(COMPLEX_NAMES)
    return c


def effective_slot_vector(values, x, y):
    """Field-rescale each homogeneous monomial to the frozen raw VEV.

    Phi stays at diag(-2x6,+3x4); Sigma -> b Sigma and S -> c S.
    The resulting Hessian is a congruent-coordinate Hessian, preserving
    inertia and nullity (but not physical eigenvalue magnitudes).
    """
    c = parent_coefficients(values, x, y)
    b, s = x*np.sqrt(15/8), y*np.sqrt(30)
    out = []
    for slot in SLOTS:
        name, _, part = slot.partition(":")
        n_sigma, n_s = DEGREES.get(name, (0, 0))
        v = c[name] * b**n_sigma * s**n_s
        out.append(float(v.real if part != "im" else v.imag))
    return np.asarray(out)


def load_blocks():
    archive = np.load(HERE / "generated_linear_blocks.npz")
    return {tuple(int(v) for v in key.split("_")): archive[key]
            for key in archive.files}


def affine_matrices(blocks, x, y):
    basis = np.eye(len(FREE))
    slots = np.stack([effective_slot_vector(row, x, y) for row in basis])
    return {label: np.einsum("js,sab->jab", slots, block)
            for label, block in blocks.items()}


def physical_complement(mats, required_nullity):
    m = mats.shape[1]
    if not required_nullity:
        return np.eye(m, dtype=np.complex128)
    trial = np.linspace(0.05, 0.95, len(FREE))
    h = np.einsum("j,jab->ab", trial, mats)
    eigenvalues, eigenvectors = np.linalg.eigh(h)
    order = np.argsort(np.abs(eigenvalues))
    zero = eigenvalues[order[:required_nullity]]
    assert max(abs(zero)) < 1e-6*max(1.0, np.max(abs(eigenvalues))), zero
    return eigenvectors[:, order[required_nullity:]]


def solve_fixed_ratios(blocks, x, y, solver="CLARABEL"):
    expected = expected_block_ranks()
    affine = affine_matrices(blocks, x, y)
    v = cp.Variable(len(FREE))
    t = cp.Variable()
    constraints = [v >= -1, v <= 1]
    for name in COMPLEX_NAMES:
        i, j = FREE.index(name + ":re"), FREE.index(name + ":im")
        constraints.append(cp.norm(v[[i, j]], 2) <= 1)
    for label, mats in affine.items():
        _, nullity, rank = expected[label]
        if rank == 0:
            continue
        p = physical_complement(mats, nullity)
        reduced = np.einsum("ab,jbc,cd->jad", p.conj().T, mats, p)
        reduced = 0.5*(reduced + reduced.conj().transpose(0, 2, 1))
        # Fixed positive scaling improves the conic conditioning without
        # changing the positive-definite feasibility question.
        scale = max(1.0, np.linalg.norm(reduced))
        table = (reduced/scale).transpose(1, 2, 0).reshape(rank*rank, len(FREE))
        h = cp.reshape(table @ v, (rank, rank), order="C")
        constraints.append(h - t*np.eye(rank) >> 0)
    problem = cp.Problem(cp.Maximize(t), constraints)
    problem.solve(solver=solver, verbose=False,
                  **({"max_iter": 5000} if solver == "CLARABEL" else {}))
    print("SDP", x, y, problem.status, "t", t.value, flush=True)
    if v.value is None:
        return None
    vector = np.asarray(v.value).reshape(-1)
    worst = (float("inf"), None)
    real_rank = 0
    max_zero = 0.0
    for label, mats in affine.items():
        h = np.einsum("j,jab->ab", vector, mats)
        eigenvalues = np.linalg.eigvalsh(h)
        _, k, _ = expected[label]
        order = np.argsort(abs(eigenvalues))
        if k:
            max_zero = max(max_zero, float(np.max(abs(eigenvalues[order[:k]]))))
        physical = eigenvalues[order[k:]]
        real_rank += dimension(label)*int(np.sum(abs(physical) > 1e-8))
        if len(physical) and float(min(physical)) < worst[0]:
            worst = (float(min(physical)), label)
    print("REPLAY", x, y, "min_raw_physical", worst,
          "max_zero_residue", max_zero, "rank", real_rank, flush=True)
    return vector, worst, max_zero, real_rank


def main():
    blocks = load_blocks()
    assert len(blocks) == 35
    for x, y in ((0.1, 0.1), (0.01, 0.01), (0.3, 0.1), (0.1, 0.3)):
        result = solve_fixed_ratios(blocks, x, y)
        if result is not None and result[1][0] > 1e-7 and result[3] == 294:
            vector = result[0]
            np.savez_compressed(HERE / "generated_stage1_candidate.npz",
                                free=vector, x=x, y=y)
            print("PRELIMINARY_STAGE1_SURVIVOR", x, y, flush=True)
            break


if __name__ == "__main__":
    main()
