"""Physical-vacuum adjoint matrix-log checks for the 33 heavy vectors.

The nine/24 vector windows are separated at this frozen point. The output
certifies logarithms and indices only; it does not derive the finite
background-field vector/Goldstone/ghost matching or scalar interval map.
"""

from itertools import combinations
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
sys.path.insert(0, str(CALC / "canonical_so10_vacuum_kernel"))
sys.path.insert(0, str(CALC / "canonical_so10_scalar_reconstruction"))
from derive_stabilizers import generators, form_action, phase_complex_structure
from verify_eta1_doublet_mixing import vacuum_form


def adjoint_matrix(t, gens):
    return np.column_stack([
        np.asarray(t@np.asarray(g, dtype=float)-np.asarray(g, dtype=float)@t,
                   dtype=float)[tuple(zip(*[p for p, _ in gens]))]
        for _, g in gens]).astype(float)


def physical_vector_gram(gens, sigma=.1*np.sqrt(15/8)):
    phi = np.diag([-2.0]*6+[3.0]*4)
    form = vacuum_form()
    idx = list(combinations(range(10), 5))
    columns = []
    for _, gen in gens:
        g = np.asarray(gen, dtype=float)
        ds = form_action(gen, form)
        arr = np.asarray([complex(*ds.get(k, (0, 0))) for k in idx])
        columns.append(np.r_[((g@phi)-(phi@g)).reshape(-1),
                               sigma*arr.real, sigma*arr.imag])
    raw = np.column_stack(columns)
    return raw.T@raw/120  # M_V²/(g10² omega²), vector-index-one basis


def trace_parts(gram, t, rng):
    adj = adjoint_matrix(t, generators())
    assert np.max(abs(adj+adj.T)) < 1e-12
    assert np.max(abs(gram@adj-adj@gram)) < 1e-9
    insertion = -adj@adj
    ev, u = np.linalg.eigh(gram)
    bins = {"MI": (0.005, 8), "MI_neutral": (0.025, 1),
            "MU_A": (50/120, 12), "MU_B": (50.6/120, 12)}
    out = {}
    for key, (mass2, count) in bins.items():
        q = u[:, abs(ev-mass2) < 1e-9]
        assert q.shape[1] == count
        out[key] = np.trace(q.T@insertion@q).real
    light = u[:, abs(ev) < 1e-9]
    assert light.shape[1] == 12
    assert abs(sum(out.values()) + np.trace(light.T@insertion@light).real
               - np.trace(insertion).real) < 1e-8
    # Conjugate the mass operator and generator together: the inserted
    # logarithm must not depend on the adjoint-coordinate choice.
    z = rng.standard_normal((45, 45))
    rotation, r = np.linalg.qr(z)
    rotation = rotation@np.diag(np.sign(np.diag(r)))
    gram_rot = rotation@gram@rotation.T
    ins_rot = rotation@insertion@rotation.T
    ev2, u2 = np.linalg.eigh(gram_rot)
    for key, (mass2, count) in bins.items():
        q2 = u2[:, abs(ev2-mass2) < 1e-9]
        assert q2.shape[1] == count
        assert abs(out[key]-np.trace(q2.T@ins_rot@q2).real) < 1e-9
    return out


def main():
    gens = generators()
    gram = physical_vector_gram(gens)
    j = [np.asarray(phase_complex_structure(((2*k, 2*k+1),)),
                    dtype=float) for k in range(5)]
    t1 = (2*(j[0]+j[1]+j[2])-3*(j[3]+j[4]))/np.sqrt(60)
    t2 = (j[3]-j[4])/2
    t3 = (j[0]-j[1])/2
    rng = np.random.default_rng(20260921)
    rows = [trace_parts(gram, t, rng) for t in (t1, t2, t3)]
    # A Pati--Salam generator broken by the 126 VEV does not commute with
    # the physical vector mass operator. A PS-side threshold therefore
    # cannot be obtained by blindly recycling these unbroken-SM traces.
    ps_g = np.asarray(dict(gens)[(6, 8)], dtype=float)/np.sqrt(2)
    ps_ad = adjoint_matrix(ps_g, gens)
    ps_commutator_norm = np.linalg.norm(gram@ps_ad-ps_ad@gram)
    assert ps_commutator_norm > 1e-4
    restored_gram = physical_vector_gram(gens, sigma=0)
    assert np.linalg.norm(restored_gram@ps_ad-ps_ad@restored_gram) < 1e-12
    by_mass = {k: np.asarray([row[k] for row in rows]) for k in rows[0]}
    assert np.allclose(by_mass["MI"], [14/5, 0, 1])
    assert np.allclose(by_mass["MI_neutral"], [0, 0, 0])
    assert np.allclose(by_mass["MU_A"], [5, 3, 2])
    assert np.allclose(by_mass["MU_B"], [1/5, 3, 2])
    assert np.allclose(sum(by_mass.values()), [8, 6, 5])
    # In lambda_V=-21 Tr(T² log M/mu), with mu=g10*omega.
    masses = {"MI": .005, "MI_neutral": .025,
              "MU_A": 50/120, "MU_B": 50.6/120}
    lambda_vector = -10.5*sum(by_mass[k]*np.log(masses[k])
                              for k in masses)
    total_index = sum(by_mass.values())
    # Shifting mu -> 2 mu subtracts 2 log(2) from log(M²/mu²).
    shifted = -10.5*sum(by_mass[k]*(np.log(masses[k])-2*np.log(2))
                        for k in masses)
    assert np.allclose(shifted-lambda_vector,
                       21*total_index*np.log(2), atol=1e-10)
    print("VECTOR_MATRIX_LOG_PASS",
          "per_mass_index", {k: v.tolist() for k, v in by_mass.items()},
          "lambda_vector_at_mu_equal_gomega", lambda_vector.tolist(),
          "d_lambda_d_log_mu", (21*total_index).tolist(),
          "broken_PS_generator_mass_commutator_norm", ps_commutator_norm,
          "finite_terms_not_derived")


if __name__ == "__main__":
    main()
