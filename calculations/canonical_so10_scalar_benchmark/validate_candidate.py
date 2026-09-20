"""Deterministic Stage 1 replay in the canonical scalar kinetic metric."""

from pathlib import Path
import json
import sys

import numpy as np
from sympy import N

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from compile_sm_multiplicity_representatives import kinetic_inner
from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import rational_representatives
from search import FREE, OMEGA, affine_matrices, load_blocks, parent_coefficients
from compile_numeric_blocks import SLOTS


def kinetic_diag(label, x, y):
    b, s = x*np.sqrt(15/8), y*np.sqrt(30)
    values = []
    for sector, _, obj in rational_representatives()[label]:
        if sector == "Phi":
            g = 2*kinetic_inner(obj, obj, "matrix")
        elif sector in ("Sigma", "SigmaBar"):
            g = b*b*kinetic_inner(obj, obj, "form")
        elif sector in ("phi", "phiBar"):
            g = kinetic_inner(obj, obj, "vector")
        else:
            g = s*s
        values.append(float(N(g)))
    assert all(g > 0 for g in values)
    return np.asarray(values)


def replay(free, x, y, blocks):
    expected = expected_block_ranks()
    affine = affine_matrices(blocks, x, y)
    worst = (float("inf"), None)
    worst_color = (float("inf"), None)
    max_zero = 0.0
    real_rank = 0
    for label, mats in affine.items():
        raw = np.einsum("j,jab->ab", free, mats)
        assert np.max(abs(raw-raw.conj().T)) < 1e-8
        d = kinetic_diag(label, x, y)
        h = raw / np.sqrt(d[:, None]*d[None, :])
        eig = np.linalg.eigvalsh(h)
        _, k, _ = expected[label]
        order = np.argsort(abs(eig))
        if k:
            max_zero = max(max_zero, float(max(abs(eig[order[:k]]))))
        physical = eig[order[k:]]
        real_rank += dimension(label)*int(np.sum(abs(physical) > 1e-7))
        if len(physical) and float(min(physical)) < worst[0]:
            worst = (float(min(physical)), label)
        if (label[0] or label[1]) and len(physical) and float(min(physical)) < worst_color[0]:
            worst_color = (float(min(physical)), label)
    return worst, worst_color, max_zero, real_rank


def main():
    point = json.loads((HERE / "STAGE1_POINT.json").read_text())
    x, y = float(point["x_sigma_over_omega"]), float(point["y_v_over_omega"])
    rounded = np.asarray([float(point["free_coefficients"][name]) for name in FREE])
    blocks = load_blocks()
    for name in ("lambdaPhiVector1", "lambdaPhiVector2"):
        assert all(np.max(abs(coeff[SLOTS.index(name)])) == 0
                   for coeff in blocks.values()), name
    for label, free in (("frozen_exact_decimal", rounded),):
        bounds = float(max(abs(free)))
        complex_norms = {name: float(np.hypot(
            free[FREE.index(name+":re")], free[FREE.index(name+":im")]))
            for name in ("z6", "z4", "zK", "zEta", "zD")}
        print(label, "max_abs_free", bounds, "complex_norms", complex_norms,
              flush=True)
        c = parent_coefficients(free, x, y)
        print(label, "tadpole_masses", {n: c[n] for n in
              ("mPhi2", "mSigma2", "mS2")}, flush=True)
        worst, color, zero, rank = replay(free, x, y, blocks)
        print(label, "minimum_physical_m2", worst,
              "minimum_colored_m2", color,
              "minimum_colored_over_omega2", color[0]/OMEGA**2,
              "max_goldstone_residue", zero, "real_rank", rank, flush=True)
    assert max(abs(rounded)) <= 1+1e-10
    assert replay(rounded, x, y, blocks)[0][0] > 0
    assert replay(rounded, x, y, blocks)[1][0]/OMEGA**2 >= 1e-4


if __name__ == "__main__":
    main()
