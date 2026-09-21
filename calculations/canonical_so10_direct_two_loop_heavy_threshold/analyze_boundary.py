"""RG and Yukawa-structure gate for the direct two-loop heavy threshold.

This program deliberately does not manufacture the finite two-loop matching
constant.  It derives everything fixed without evaluating the benchmark's
two-loop massive vacuum integrals: the parent gauge/scalar beta coefficients,
the channel-by-channel logarithmic consistency data, the size of the finite
constant required by the existing residual, and the exact family-invariant
Yukawa dependency at quadratic order.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
CALC = HERE.parent
PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"
NEXT_HASH = "62a8c3150e26c957641883ba3ac6fc6d977890c8543e859a4af22cbf7bbfb54a"


def verify(path: Path, expected: str) -> None:
    assert sha256(path.read_bytes()).hexdigest() == expected, path


def qstr(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main() -> None:
    verify(CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md", PARENT_HASH)
    verify(CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH)
    verify(CALC / "canonical_so10_direct_gauge_next_order" / "next_order.json", NEXT_HASH)

    previous = json.loads((CALC / "canonical_so10_direct_gauge_next_order" /
                           "next_order.json").read_text())
    direct = json.loads((CALC / "canonical_so10_direct_gauge_matching" /
                         "direct_matching.json").read_text())
    scalar_log = json.loads((CALC / "canonical_so10_matrix_threshold" /
                             "scalar_matrix_log.json").read_text())

    # General two-loop coefficient for Weyl fermions and real scalars:
    # b = -11/3 C_A + 2/3 S2(F) + 1/6 S2(S)
    # B = -34/3 C_A^2
    #     + 2 sum_F C2(F)T(F) + 10/3 C_A S2(F)
    #     + 2 sum_S C2(S)T(S) + 1/3 C_A S2(S).
    # Complex scalars count as two real scalar representations.
    ca = F(8)
    s2_f = F(3 * 2)  # three Weyl 16_F families, T(16)=2
    c2t_f = F(3) * F(2) * F(45, 8)
    scalar_reps = {
        "54_real": {"S2_real": F(12), "C2": F(10)},
        "126_complex": {"S2_real": F(70), "C2": F(25, 2)},
        "10_complex": {"S2_real": F(2), "C2": F(9, 2)},
        "singlet_complex": {"S2_real": F(0), "C2": F(0)},
    }
    s2_s = sum((v["S2_real"] for v in scalar_reps.values()), F(0))
    c2t_s = sum((v["S2_real"] * v["C2"] for v in scalar_reps.values()), F(0))
    b_parent = -F(11, 3) * ca + F(2, 3) * s2_f + F(1, 6) * s2_s
    B_parent = (-F(34, 3) * ca * ca
                + 2 * c2t_f + F(10, 3) * ca * s2_f
                + 2 * c2t_s + F(1, 3) * ca * s2_s)
    assert b_parent == -F(34, 3)
    assert B_parent == F(10405, 6)

    b_sm = [F(41, 10), -F(19, 6), -F(7)]
    B_sm = [
        [F(199, 50), F(27, 10), F(44, 5)],
        [F(9, 10), F(35, 6), F(12)],
        [F(11, 10), F(9, 2), -F(26)],
    ]
    B_rows = [sum(row, F(0)) for row in B_sm]
    delta_b = [z - b_parent for z in b_sm]
    delta_B_gs = [z - B_parent for z in B_rows]
    assert delta_b == [F(463, 30), F(49, 6), F(13, 3)]
    assert delta_B_gs == [-F(257803, 150), -F(51463, 30), -F(52637, 30)]

    # Martens' RG solution fixes the L^2 and L terms of the two-loop
    # decoupling function.  In its notation:
    # zeta_i = 1 + (alpha/pi)[db_i L/2-C0_i]
    # + (alpha/pi)^2[db_i^2 L^2/4
    # + (dB_i/8-C0_i db_i)L+C1_i].
    # The three C1_i are finite massive two-loop constants and are not fixed
    # by beta functions or matching-scale variation.
    rg_template = []
    for db, dB in zip(delta_b, delta_B_gs):
        rg_template.append({
            "delta_b": qstr(db),
            "delta_B_yukawa_independent": qstr(dB),
            "L2_coefficient": qstr(db * db / 4),
            "L_coefficient_without_C0_term": qstr(dB / 8),
            "complete_L_coefficient": f"{qstr(dB/8)} - ({qstr(db)})*C0_i",
            "finite_constant": "C1_i_UNCALCULATED",
        })

    g10 = previous["central_refit"]["g10"]
    alpha_u = g10 * g10 / (4 * math.pi)
    loop_a = g10 * g10 / (16 * math.pi**2)
    parent_two_over_one = abs(float(B_parent) * loop_a / float(b_parent))

    # Recover the one-loop finite/log coefficient at mu=omega in the passed
    # direct convention.  This is used only to expose the known C0 data; it
    # does not determine C1.
    scalar_lambda = np.asarray(scalar_log["lambda_scalar_SM_order_1_2_3"], dtype=float)
    vector_sets = [
        (0.005, np.asarray([14/5, 0, 1.0])),
        (0.025, np.zeros(3)),
        (50/120, np.asarray([5.0, 3.0, 2.0])),
        (50.6/120, np.asarray([1/5, 3.0, 2.0])),
    ]
    vector_lambda = sum((idx * (1 - 21 * math.log(g10 * math.sqrt(m2)))
                         for m2, idx in vector_sets), np.zeros(3))
    lambda_total = scalar_lambda + vector_lambda
    # At the chosen reference L=ln(mu/omega)=0, alpha_i=alpha_U*zeta_i
    # has -C0_i=lambda_i/12 at one loop.
    C0_reference = -lambda_total / 12

    residual = np.asarray(previous["central_refit"]["residual_inverse_couplings"], dtype=float)
    # In an inverse-coupling convention a two-loop finite constant has the
    # natural conversion alpha_U/pi^2.  These are the C1-equivalent channel
    # values required to cancel the residual after all convention-fixed
    # lower-order pieces; a common shift is physically absorbed in alpha_U.
    c1_equivalent = residual * math.pi**2 / alpha_u
    c1_centered = c1_equivalent - np.mean(c1_equivalent)
    assert abs(np.mean(c1_centered)) < 1e-12

    # Yukawa dependence with massless fermion propagators has exactly two
    # Yukawa vertices at this loop order.  With r,s in {10,126}, all family
    # dependence is the positive-semidefinite Hermitian Gram matrix
    # K_rs=Tr(Y_r^dagger Y_s).  Its four real coordinates are complete at
    # quadratic order.  At the physical vacuum M_N is proportional to
    # sigma*Y126, so exact massive integrals depend additionally on spectral
    # matrix functions and cannot be evaluated from K alone.
    yukawa_basis = {
        "matrices": ["Y10=Y10^T", "Y126=Y126^T"],
        "quadratic_family_kernel": "K_rs=Tr(Y_r^dagger Y_s), r,s in {10,126}",
        "real_coordinates": [
            "Tr(Y10^dagger Y10)",
            "Tr(Y126^dagger Y126)",
            "Re Tr(Y10^dagger Y126)",
            "Im Tr(Y10^dagger Y126)",
        ],
        "positivity": "K is Hermitian PSD; |K_10,126|^2 <= K_10,10*K_126,126",
        "cross_term_condition": "off-diagonal K contributes only with a 10/bar126 scalar mixing kernel",
        "physical_mass_dependency": "M_N=c_N*sigma*Y126; exact massive threshold needs its singular values and mixing projectors",
        "numerical_status": "UNDEFINED_NO_CANONICAL_FLAVOR_POINT",
    }

    # The published two-loop formula is an RG/log comparator only.  Every
    # simplifying hypothesis below is violated by the frozen benchmark.
    applicability = {
        "one_GUT_scale_vev": False,
        "no_scalar_trilinears": False,
        "no_heavy_fermions": False,
        "common_mass_heavy_vectors": False,
        "gut_breaking_higgs_at_most_three_SM_irreps": False,
        "other_heavy_scalars_common_mass": False,
        "consequence": "published_finite_C1_formula_not_applicable",
    }

    result = {
        "outcome": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
        "heavy_threshold_gate": "DIRECT_TWO_LOOP_HEAVY_THRESHOLD_BLOCKED",
        "preserved_results": [
            "DIRECT_ONE_LOOP_KERNEL_PASS",
            "DIRECT_SM_TWO_LOOP_RUNNING_PASS",
        ],
        "scheme": "MSbar_background_field_Feynman_gauge",
        "frozen_hashes": {
            "parent_action": PARENT_HASH,
            "positive_higgs_point": POINT_HASH,
            "next_order_json": NEXT_HASH,
        },
        "part_A_gauge_scalar": {
            "parent_group_data": {
                "C2_G": qstr(ca),
                "S2_Weyl_F": qstr(s2_f),
                "sum_C2T_Weyl_F": qstr(c2t_f),
                "S2_real_scalars": qstr(s2_s),
                "sum_C2T_real_scalars": qstr(c2t_s),
            },
            "parent_b_one_loop": qstr(b_parent),
            "parent_B_two_loop_yukawa_independent": qstr(B_parent),
            "SM_B_row_sums_at_unified_coupling": [qstr(x) for x in B_rows],
            "rg_log_kernel": rg_template,
            "parent_two_loop_over_one_loop_at_diagnostic_g10": parent_two_over_one,
            "one_loop_C0_at_mu_eq_omega": C0_reference.tolist(),
            "finite_C1": "NOT_CALCULATED",
            "finite_C1_reason": "requires benchmark-specific two-loop massive hard-region diagrams and one-loop counterterms",
            "published_formula_applicability": applicability,
        },
        "finite_threshold_demand": {
            "existing_residual_inverse_couplings": residual.tolist(),
            "minimum_canceling_inverse_coupling_shift": (-residual).tolist(),
            "alpha_U_diagnostic": alpha_u,
            "C1_equivalent_centered_required": c1_centered.tolist(),
            "max_abs_C1_equivalent": float(np.max(abs(c1_centered))),
            "interpretation": "normalization diagnostic only; no plausibility bound or threshold result",
        },
        "part_B_yukawa": yukawa_basis,
        "checks": {
            "parent_one_loop_beta_replay": "PASS",
            "parent_two_loop_yukawa_independent_beta": "DERIVED_EXACTLY",
            "two_loop_log_structure": "PASS_RG_CONSISTENCY_TEMPLATE",
            "basis_invariance": "PASS_FOR_K_RS_SYMBOLIC_FORM",
            "gauge_parameter_cancellation": "NOT_TESTED_FINITE_TWO_LOOP_DIAGRAMS_ABSENT",
            "degenerate_mass_limit": "NOT_TESTED_FINITE_TWO_LOOP_DIAGRAMS_ABSENT",
            "combined_order_matching_scale_cancellation": "LOG_STRUCTURE_FIXED_FULL_NUMERICAL_CHECK_BLOCKED_BY_C1_AND_YUKAWA",
            "refit_with_two_loop_heavy_threshold": "NOT_AUTHORIZED_NO_FINITE_THRESHOLD",
        },
        "bfb_status": "BFB_UNRESOLVED",
        "downstream": {
            "gauge_unification_passed": False,
            "gauge_unification_failed": False,
            "physical_g10_or_omega_promoted": False,
            "flavor_fit_started": False,
            "proton_decay_started": False,
            "benchmark_replacement_started": False,
        },
    }
    (HERE / "two_loop_boundary.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PARENT_BETA", qstr(b_parent), qstr(B_parent))
    print("DELTA_B", [qstr(x) for x in delta_b])
    print("DELTA_B_TWO_LOOP_YUKAWA_INDEPENDENT", [qstr(x) for x in delta_B_gs])
    print("PARENT_TWO_OVER_ONE", parent_two_over_one)
    print("REQUIRED_CENTERED_C1_EQUIVALENT", c1_centered.tolist())
    print("DIRECT_TWO_LOOP_HEAVY_THRESHOLD_BLOCKED")
    print("DIRECT_GAUGE_MATCHING_UNRESOLVED")


if __name__ == "__main__":
    main()
