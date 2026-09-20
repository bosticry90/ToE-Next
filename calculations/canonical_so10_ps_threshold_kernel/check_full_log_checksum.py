"""Whole-spectrum one-loop logarithmic checksum without solving gauge scales.

The identity is for a direct Spin(10)->SM decoupling of the frozen spectrum.
It checks the total scalar/Goldstone/vector index bookkeeping and the
matching-scale derivative, not the required two-boundary PS interval map.
"""

import json
from pathlib import Path

import numpy as np
from sympy import Rational as Q

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "canonical_so10_gauge_matching" / "scalar_sm_ledger.json"


def main():
    rows = json.loads(LEDGER.read_text())["blocks"]
    all_s = np.sum([np.asarray(r["one_loop_b_per_physical_eigenvalue"])
                    *r["multiplicity"] for r in rows], axis=0)
    zero_s = np.sum([np.asarray(r["one_loop_b_per_physical_eigenvalue"])
                     *r["zero_multiplicity"] for r in rows], axis=0)
    assert np.allclose(all_s, [14, 14, 14], atol=1e-12)
    # 54_R index 12; 126_C index 35 (realified 70); 10_C index 1
    # (realified 2): total real scalar index 12+70+2=84, b=84/6=14.
    vector_index = np.asarray([8, 6, 5], dtype=float)  # (1,2,3)
    higgs_b = np.asarray([.1, 1/6, 0])
    assert np.allclose(zero_s, vector_index/6+higgs_b, atol=1e-12)
    heavy_scalar_b = all_s-zero_s
    b_high = -Q(11, 3)*8 + Q(2, 3)*6 + Q(14)
    assert b_high == -Q(34, 3)
    b_low = [Q(41, 10), -Q(19, 6), -Q(7)]
    lhs = np.asarray([float(b_high-z) for z in b_low])
    rhs = -3.5*vector_index+heavy_scalar_b
    assert np.allclose(lhs, rhs, atol=1e-12), (lhs, rhs)
    # In alpha_low^-1=alpha_high^-1-lambda/(12pi),
    # d lambda/d ln mu = 21*T_vector - 6*b_heavy_scalar.
    d_lambda = 21*vector_index-6*heavy_scalar_b
    assert np.allclose(lhs, -d_lambda/6, atol=1e-12)
    print("FULL_LOG_MATCHING_SCALE_CHECK_PASS",
          "all_scalar_b", all_s,
          "zero_b", zero_s,
          "heavy_scalar_b", heavy_scalar_b,
          "high_minus_low_beta", lhs)


if __name__ == "__main__":
    main()
