"""Derived SM-side scalar threshold inventory for the frozen positive-Higgs point.

The generated affine blocks are a cache, not scalar authority. Run the cache
regression and the direct-parent point replay before interpreting this output.
Masses are dimensionless m/omega; no physical GeV scale is presumed here.
"""

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Rational, sqrt

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
sys.path.insert(0, str(CALC / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(CALC / "canonical_so10_full_hessian"))

from search import FREE, effective_slot_vector, load_blocks
from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from replay_candidate_exact import kinetic_diag


def scalar_beta_weight(label):
    """One real scalar in this complexified-real irrep: (b1,b2,b3)."""
    p, q, n, y6 = label
    d3 = (p+1)*(q+1)*(p+q+2)//2
    d2 = n+1
    y = y6/6
    c2_3 = (p*p+q*q+p*q+3*p+3*q)/3
    t3 = d3*c2_3/8
    t2 = n*(n+1)*(n+2)/12
    return [((3/5)*y*y*d3*d2)/6,
            (t2*d3)/6,
            (t3*d2)/6]


def frozen_free_values():
    inherited = CALC / "canonical_so10_scalar_benchmark" / "STAGE1_POINT.json"
    point = CALC / "canonical_so10_positive_higgs" / "POINT.json"
    assert hashlib.sha256(point.read_bytes()).hexdigest() == (
        "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"
    )
    base = json.loads(inherited.read_text())["free_coefficients"]
    tuned = json.loads(point.read_text())
    base.update(tuned["changed_free_coefficients"])
    base["mphi2"] = tuned["approximate_mphi2_over_omega2"]
    assert set(base) == set(FREE)
    return np.asarray([float(base[name]) for name in FREE])


def main():
    blocks = load_blocks()
    assert len(blocks) == 35
    slots = effective_slot_vector(frozen_free_values(), 0.1, 0.1)
    b, s = Rational(1, 10)*sqrt(Rational(15, 8)), Rational(1, 10)*sqrt(30)
    expected = expected_block_ranks()
    rows = []
    total_real = physical_real = zero_real = 0
    smallest_heavy = float("inf")
    for label in sorted(blocks):
        coeff = blocks[label]
        h = np.einsum("s,sab->ab", slots, coeff)
        metric = np.asarray([float(g) for g in kinetic_diag(label, b, s)])
        assert np.all(metric > 0), label
        hc = h / np.sqrt(np.outer(metric, metric))
        assert np.max(abs(hc-hc.conj().T)) < 1e-8, label
        ev = np.linalg.eigvalsh(hc).real / 60.0
        ev = sorted(ev, key=abs)
        k = expected[label][1]
        if label in ((0, 0, 1, -3), (0, 0, 1, 3)):
            k += 1
        assert max((abs(q) for q in ev[:k]), default=0) < 1e-9, (label, ev[:k])
        assert min((q for q in ev[k:]), default=1) > 0, (label, ev[k:])
        d = dimension(label)
        total_real += len(ev)*d
        zero_real += k*d
        physical_real += (len(ev)-k)*d
        if k < len(ev):
            smallest_heavy = min(smallest_heavy, min(ev[k:]))
        rows.append({
            "sm_irrep": {"su3_dynkin": list(label[:2]), "su2_dim": label[2]+1,
                         "hypercharge": f"{label[3]}/6"},
            "real_dimension_per_eigenvalue": d,
            "multiplicity": len(ev),
            "zero_multiplicity": k,
            "one_loop_b_per_physical_eigenvalue": scalar_beta_weight(label),
            "mass_squared_over_omega_squared": ev,
        })
    assert (total_real, zero_real, physical_real) == (328, 38, 290)
    higgs = [r for r in rows if r["sm_irrep"]["su3_dynkin"] == [0, 0]
             and r["sm_irrep"]["su2_dim"] == 2
             and r["sm_irrep"]["hypercharge"] in ("-3/6", "3/6")]
    assert len(higgs) == 2
    assert np.allclose(np.sum([r["one_loop_b_per_physical_eigenvalue"]
                               for r in higgs], axis=0), [1/10, 1/6, 0])
    result = {
        "status": "SM_SCALAR_LEDGER_ONLY",
        "units": "m^2/omega^2 (physical kinetic normalization)",
        "point_sha256": "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816",
        "blocks": rows,
        "real_dimension": total_real,
        "zero_real_dimension": zero_real,
        "heavy_real_dimension": physical_real,
        "min_heavy_m2_over_omega2": smallest_heavy,
    }
    output = HERE / "scalar_sm_ledger.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("SM_SCALAR_LEDGER_PASS", total_real, zero_real, physical_real,
          "min_heavy_m2_over_omega2", smallest_heavy)


if __name__ == "__main__":
    main()
