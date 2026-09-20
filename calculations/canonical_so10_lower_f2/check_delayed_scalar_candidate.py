"""Checksum for a *candidate*, not admitted, all-scalars-retained PS EFT.

This algebra shows that delaying all physical-scalar decoupling to MI would
give a complete lower logarithmic beta jump. It does not construct the
PS-covariant EFT or justify its higher-dimensional operator truncation.
"""

import json
from pathlib import Path

from sympy import Rational as Q, simplify

CALC = Path(__file__).resolve().parent.parent


def main():
    data = json.loads((CALC / "canonical_so10_matrix_threshold" /
                       "scalar_matrix_log.json").read_text())
    assert data["heavy_real_directions"] == 290
    assert data["zero_real_directions_excluded"] == 38
    # Rationalize the prior independently evaluated representation weights.
    heavy_scalar_b = (Q(377, 30), Q(77, 6), Q(79, 6))
    assert all(abs(float(b) - z) < 1e-12 for b, z in zip(
        heavy_scalar_b, data["heavy_scalar_beta_SM_order_1_2_3"]))

    lower_vector_t = (Q(14, 5), Q(0), Q(1))
    upper_vector_t = (Q(26, 5), Q(6), Q(4))
    all_vector_t = tuple(a + b for a, b in zip(
        lower_vector_t, upper_vector_t))
    assert all_vector_t == (Q(8), Q(6), Q(5))

    # 84 is the real scalar index of 54_R+126_C+10_C, so b=14.
    # A putative PS EFT retaining all scalars but excluding the 24 eaten
    # upper Goldstones has projected b=14-T_upper/6. Below MI only the
    # tuned complex Higgs doublet contributes, with b=(1/10,1/6,0).
    ps_scalar_b = tuple(Q(14) - t / 6 for t in upper_vector_t)
    sm_higgs_b = (Q(1, 10), Q(1, 6), Q(0))
    raw_scalar_jump = tuple(a - b for a, b in zip(
        ps_scalar_b, sm_higgs_b))
    lower_goldstone_b = tuple(t / 6 for t in lower_vector_t)
    assert raw_scalar_jump == tuple(a + b for a, b in zip(
        heavy_scalar_b, lower_goldstone_b))

    pure_gauge_jump = tuple(-Q(11, 3) * t for t in lower_vector_t)
    raw_total_jump = tuple(a + b for a, b in zip(
        pure_gauge_jump, raw_scalar_jump))
    vector_plus_physical_jump = tuple(-Q(7, 2) * t + bs
                                      for t, bs in zip(lower_vector_t,
                                                       heavy_scalar_b))
    assert raw_total_jump == vector_plus_physical_jump
    # The candidate lower lambda contains the already-derived vector
    # lambda and the 290-physical-scalar log. Its scale derivative must
    # cancel the candidate projected beta jump. Fermion jump is zero.
    lambda_derivative = tuple(21 * t - 6 * bs for t, bs in
                              zip(lower_vector_t, heavy_scalar_b))
    assert all(simplify(dl + 6 * db) == 0 for dl, db in
               zip(lambda_derivative, raw_total_jump))
    assert raw_total_jump == (Q(83, 30), Q(77, 6), Q(29, 3))
    print("DELAYED_SCALAR_PS_EFT_LOG_CHECKSUM_PASS",
          "candidate_high_minus_low_beta", raw_total_jump,
          "candidate_lambda_scale_derivative", lambda_derivative,
          "PS_EFT_CONSTRUCTION_NOT_CERTIFIED")


if __name__ == "__main__":
    main()
