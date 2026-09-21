"""Observable-specific diagnostics for the candidate PS EFT error budget.

This translates already-earned masses, beta indices, and operator norms into
inverse-coupling units. Unknown induced-operator Wilson coefficients are not
guessed, so a missing bound remains missing rather than being set to one.
"""

from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
for name in ("canonical_so10_ps_multispurion", "canonical_so10_gauge_matching",
             "canonical_so10_full_hessian"):
    sys.path.insert(0, str(CALC / name))

from check_candidate_split import ps_origin
from build_sm_threshold_ledger import scalar_beta_weight
from evaluate_sm_hessian_blocks import rational_representatives
from decompose_sm_tangent import dimension

PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"


def verify_hash(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == expected, path


def pairwise_spread(values):
    return max(values)-min(values)


def main():
    verify_hash(CALC / "canonical_so10_scalar_reconstruction" /
                "PARENT_ACTION_V1.md", PARENT_HASH)
    verify_hash(CALC / "canonical_so10_positive_higgs" / "POINT.json",
                POINT_HASH)
    coarse = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "coarse_one_loop.json").read_text())
    scalar = json.loads((CALC / "canonical_so10_matrix_threshold" /
                         "scalar_matrix_log.json").read_text())
    required = coarse["inverse_coupling_difference_shift_needed_for_vector_ratio_range"]
    target = min(required)/10

    # Candidate upper block: complex (6,1,1)+(15,2,2) inside 126_H.
    beta_h = np.zeros(3)
    real_h = 0
    for label, entries in rational_representatives().items():
        copies = sum(ps_origin(sector, obj) in ("126_k1", "126_k2")
                     for sector, _, obj in entries)
        beta_h += copies*np.asarray(scalar_beta_weight(label))
        real_h += copies*dimension(label)
    # Independent PS branching replay: T_4(6)=1 and
    # T_4(15,2,2)=4*2*2=16; T_L=T_R=15 for (15,2,2).
    b4 = Fraction(1+16, 3)
    bL = bR = Fraction(15, 3)
    b1 = Fraction(2, 5)*b4 + Fraction(3, 5)*bR
    expected_beta = np.asarray([b1, bL, b4], dtype=float)
    assert real_h == 132
    assert np.allclose(beta_h, expected_beta, rtol=0, atol=2e-15), beta_h

    ratios = coarse["vector_hierarchy_mass_ratio_range"]
    placement = []
    for ratio in ratios:
        delta = beta_h*math.log(ratio)/(2*math.pi)
        placement.append({"ratio": ratio, "delta_alpha_inverse": delta.tolist(),
                          "max_pairwise": pairwise_spread(delta),
                          "L_minus_4": abs(delta[1]-delta[2])})

    lambdas = np.asarray(scalar["lambda_scalar_SM_order_1_2_3"])
    assert scalar["heavy_real_directions"] == 290
    assert scalar["zero_real_directions_excluded"] == 38
    expected_all_beta = np.asarray([Fraction(377, 30), Fraction(77, 6),
                                    Fraction(79, 6)], dtype=float)
    assert np.allclose(scalar["heavy_scalar_beta_SM_order_1_2_3"],
                       expected_all_beta, rtol=0, atol=5e-14)
    scalar_alpha = -lambdas/(12*math.pi)
    derivative = np.asarray(scalar["d_lambda_d_log_mu"])
    assert np.allclose(derivative, -6*expected_all_beta, rtol=0, atol=5e-14)
    scalar_scale_drift = []
    for ratio in ratios:
        delta = -derivative*math.log(ratio)/(12*math.pi)
        scalar_scale_drift.append({"ratio": ratio,
                                   "delta_alpha_inverse": delta.tolist(),
                                   "max_pairwise": pairwise_spread(delta),
                                   "L_minus_C": abs(delta[1]-delta[2])})

    # Previously earned numerical operator data, all in units of omega^2.
    min_physical_scalar = 0.0014426926299895904
    physical_heavy_min = 0.28671408106862006
    retained_block_norm = 0.20184463963648908
    direct_schur = 0.00344398405
    conservative_schur = 0.013424018878048763
    mixing = 0.03145010521465646
    retained_to_heavy = retained_block_norm/physical_heavy_min
    schur_to_gap = direct_schur/min_physical_scalar
    conservative_schur_to_gap = conservative_schur/min_physical_scalar
    mixing_to_heavy = mixing/physical_heavy_min

    # Coarse g_U is a comparator only; this tests suppression of the already
    # identified upper-vector current-current expansion for the largest
    # provisionally retained scalar scale.
    gu = coarse["g_U"]
    upper_vector_m2 = gu*gu*Fraction(50, 120)
    retained_to_vector = retained_block_norm/float(upper_vector_m2)

    # A first-order derivative expansion with ratio r has a geometric tail
    # bounded only when r<1; this is diagnostic because Wilson/operator norms
    # have not been derived.
    geometric_tail = (retained_to_heavy**2/(1-retained_to_heavy)
                      if retained_to_heavy < 1 else None)
    result = {
        "disposition": "PS_EFT_ERROR_UNRESOLVED",
        "accuracy_target_inverse_coupling": target,
        "required_coarse_shift_range": required,
        "candidate_upper_scalar": {
            "real_directions": real_h,
            "beta_SM_order_1_2_3": beta_h.tolist(),
            "placement_sensitivity": placement,
        },
        "whole_physical_scalar_log_at_mu_omega": {
            "delta_alpha_inverse_SM_order_1_2_3": scalar_alpha.tolist(),
            "max_nonuniversal_spread": pairwise_spread(scalar_alpha),
            "L_minus_C": abs(scalar_alpha[1]-scalar_alpha[2]),
            "matching_scale_window_drift": scalar_scale_drift,
            "is_direct_broken_phase_contribution_not_PS_error_bound": True,
        },
        "quadratic_and_derivative_diagnostics": {
            "physical_candidate_heavy_min_m2_over_omega2": physical_heavy_min,
            "retained_block_norm_m2_over_omega2": retained_block_norm,
            "retained_to_heavy_ratio": retained_to_heavy,
            "mixing_to_heavy_ratio": mixing_to_heavy,
            "direct_schur_to_smallest_positive_scalar_gap": schur_to_gap,
            "conservative_schur_to_smallest_positive_scalar_gap":
                conservative_schur_to_gap,
            "log_lipschitz_bound_closes": conservative_schur < min_physical_scalar,
            "first_omitted_geometric_tail_diagnostic": geometric_tail,
            "coarse_upper_vector_m2_over_omega2": float(upper_vector_m2),
            "retained_to_upper_vector_m2_ratio": retained_to_vector,
        },
        "unbounded_terms": [
            "upper-vector current-current insertion into retained-field loops",
            "upper-heavy scalar exchange operators in lower F2 matching",
            "covariant removal of 24 upper Goldstone directions",
            "finite hard-region subtraction for borderline retained multiplets",
        ],
    }
    assert result["quadratic_and_derivative_diagnostics"][
        "log_lipschitz_bound_closes"] is False
    assert max(z["L_minus_4"] for z in placement) > target
    assert pairwise_spread(scalar_alpha) < target
    assert retained_to_vector > 1
    (HERE / "error_budget.json").write_text(json.dumps(result, indent=2)+"\n")
    print("ACCURACY_TARGET", target)
    print("CANDIDATE_UPPER_BETA", beta_h, "REAL_DIRECTIONS", real_h)
    print("UPPER_PLACEMENT_L_MINUS_4", [z["L_minus_4"] for z in placement])
    print("WHOLE_SCALAR_DIRECT_MAX_SPREAD", pairwise_spread(scalar_alpha),
          "L_MINUS_C", abs(scalar_alpha[1]-scalar_alpha[2]))
    print("RETAINED_TO_HEAVY", retained_to_heavy,
          "SCHUR_TO_POSITIVE_GAP", schur_to_gap,
          "RETAINED_TO_COARSE_UPPER_VECTOR", retained_to_vector)
    print("PS_EFT_ERROR_UNRESOLVED")


if __name__ == "__main__":
    main()
