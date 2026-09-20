"""Basis-invariant SM-side scalar logarithm at the physical stationary point.

This is a direct broken-phase trace, NOT an MI/MU active-field allocation.
The trace uses the canonical kinetic metric and removes 33 gauge, one PQ,
and four tuned-Higgs zero directions before taking any logarithm.
"""

import json
from pathlib import Path
import sys

import numpy as np
from sympy import Rational, sqrt

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
sys.path.insert(0, str(CALC / "canonical_so10_gauge_matching"))
sys.path.insert(0, str(CALC / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(CALC / "canonical_so10_full_hessian"))

from build_sm_threshold_ledger import frozen_free_values, scalar_beta_weight
from search import effective_slot_vector, load_blocks
from define_generic_nullity_test import expected_block_ranks
from replay_candidate_exact import kinetic_diag
from decompose_sm_tangent import dimension


def trace_log_positive(h, coefficient, zero_count, scale2, rng):
    """Return 1/2 Tr[C P log(M²/scale²)] and test unitary covariance."""
    ev, u = np.linalg.eigh(h)
    order = np.argsort(abs(ev))
    ev, u = ev[order], u[:, order]
    assert max((abs(v) for v in ev[:zero_count]), default=0) < 1e-9
    assert min((v for v in ev[zero_count:]), default=1) > 0
    physical = np.arange(zero_count, len(ev))
    log_operator = (u[:, physical]*np.log(ev[physical]/scale2)) @ (
        u[:, physical].conj().T)
    c = coefficient*np.eye(len(ev))
    original = .5*np.trace(c@log_operator).real
    if len(ev) > 1:
        z = rng.standard_normal((len(ev), len(ev)))+1j*rng.standard_normal(
            (len(ev), len(ev)))
        q, r = np.linalg.qr(z)
        q = q@np.diag(np.exp(-1j*np.angle(np.diag(r))))
        rotated = .5*np.trace((q@c@q.conj().T) @ (
            q@log_operator@q.conj().T)).real
        assert np.isclose(original, rotated, rtol=1e-12, atol=1e-12)
    return original, ev


def main():
    blocks = load_blocks()
    slots = effective_slot_vector(frozen_free_values(), .1, .1)
    b = Rational(1, 10)*sqrt(Rational(15, 8))
    s = Rational(1, 10)*sqrt(30)
    expected = expected_block_ranks()
    ledger = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "scalar_sm_ledger.json").read_text())
    by_label = {}
    for row in ledger["blocks"]:
        ir = row["sm_irrep"]
        by_label[(*ir["su3_dynkin"], ir["su2_dim"]-1,
                  int(ir["hypercharge"].split("/")[0]))] = row
    rng = np.random.default_rng(20260920)
    total = np.zeros(3)
    independent = np.zeros(3)
    heavy_beta = np.zeros(3)
    heavy_real = zero_real = 0
    for label, coeff in sorted(blocks.items()):
        h = np.einsum("s,sab->ab", slots, coeff)
        metric = np.asarray([float(g) for g in kinetic_diag(label, b, s)])
        h = h/np.sqrt(np.outer(metric, metric))/60
        assert np.max(abs(h-h.conj().T)) < 1e-8
        zeros = expected[label][1]
        if label in ((0, 0, 1, -3), (0, 0, 1, 3)):
            zeros += 1
        weight = np.asarray(scalar_beta_weight(label))
        # A real-scalar beta weight is T/6. The literature lambda convention
        # uses T log(M/mu) = (T/2) log(M²/mu²) = 3*b*log(M²/mu²).
        traces = [trace_log_positive(h, 6*w, zeros, 1, rng)
                  for w in weight]
        ev = traces[0][1]
        total += [item[0] for item in traces]
        row = by_label[label]
        ordered = sorted(ev, key=abs)
        assert np.allclose(ordered, row["mass_squared_over_omega_squared"],
                           rtol=1e-9, atol=1e-9)
        independent += 3*weight*sum(np.log(np.asarray(
            row["mass_squared_over_omega_squared"][zeros:])))
        heavy_beta += (len(ev)-zeros)*weight
        heavy_real += (len(ev)-zeros)*dimension(label)
        zero_real += zeros*dimension(label)
    assert (heavy_real, zero_real) == (290, 38)
    assert np.allclose(total, independent, rtol=1e-11, atol=1e-11)
    assert np.allclose(heavy_beta, [12.5666666666667,
                                    12.8333333333333,
                                    13.1666666666667])
    # lambda(mu/omega) = lambda(1) - 6*b_heavy*log(mu/omega).
    derivative = -6*heavy_beta
    shifted = total-6*heavy_beta*np.log(2)
    assert np.allclose(shifted-total, derivative*np.log(2))
    result = {
        "scope": "physical_stationary_broken_phase_SM_scalar_log_trace_only",
        "scale": "mu=omega; m2 in units omega2",
        "lambda_scalar_SM_order_1_2_3": total.tolist(),
        "d_lambda_d_log_mu": derivative.tolist(),
        "heavy_scalar_beta_SM_order_1_2_3": heavy_beta.tolist(),
        "heavy_real_directions": heavy_real,
        "zero_real_directions_excluded": zero_real,
        "two_boundary_allocation_claimed": False,
    }
    (HERE / "scalar_matrix_log.json").write_text(json.dumps(result, indent=2)+"\n")
    print("SCALAR_MATRIX_LOG_PASS", result)


if __name__ == "__main__":
    main()
