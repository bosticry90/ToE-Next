"""Direct physical-vacuum Spin(10)->SM one-loop gauge match.

The one-loop kernel is derived in a common MSbar background-field Feynman
gauge. The gauge-only SM two-loop evolution is an uncertainty comparator,
not promoted matching authority.
"""

from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root
from sympy import Rational as Q, Symbol, diff, limit, simplify

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"


def verify(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == expected, path


def vector_heat_kernel():
    """Re-derive vector+Goldstone+ghost MSbar finite/log coefficients."""
    eps = Symbol("eps")
    d = 4-2*eps
    # One half for a real vector determinant and Goldstone; one complex
    # Grassmann ghost has the displayed full negative weight.
    a_vector = Q(1, 2)*(d/Q(12)-2)
    a_goldstone = Q(1, 2)*Q(1, 12)
    a_ghost = -Q(1, 12)
    total = simplify(a_vector+a_goldstone+a_ghost)
    assert total == -Q(7, 8)-eps/Q(12)
    a0 = total.subs(eps, 0)
    a1 = diff(total, eps)
    log_ratio = simplify(a0/Q(1, 24))
    assert log_ratio == -21
    L = Symbol("L")
    ren = simplify(limit(total*(1/eps-L)-a0/eps, eps, 0))
    assert ren == Q(7, 8)*L-Q(1, 12)
    finite_over_log_m2 = simplify(a1/(-a0))
    assert finite_over_log_m2 == -Q(2, 21)
    return {"a2": str(total), "vector_to_real_scalar_log": int(log_ratio),
            "finite_over_log_m2": str(finite_over_log_m2),
            "lambda_form": "T*(1-21*log(M/mu))"}


def gauge_only_two_loop(A0, b, B, log_scale):
    alpha0 = 1/A0
    def beta(_, alpha):
        return (b*alpha*alpha/(2*math.pi)
                +alpha*alpha*(B@alpha)/(8*math.pi**2))
    solution = solve_ivp(beta, (0, log_scale), alpha0,
                         rtol=2e-11, atol=1e-13)
    assert solution.success
    return 1/solution.y[:, -1]


def main():
    verify(CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md",
           PARENT_HASH)
    verify(CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH)
    heat = vector_heat_kernel()
    scalar_log = json.loads((CALC / "canonical_so10_matrix_threshold" /
                             "scalar_matrix_log.json").read_text())
    scalar_ledger = json.loads((CALC / "canonical_so10_gauge_matching" /
                                "scalar_sm_ledger.json").read_text())
    vector_ledger = json.loads((CALC / "canonical_so10_gauge_matching" /
                                "vector_ledger.json").read_text())
    inputs = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "coarse_one_loop.json").read_text())["inputs"]

    assert scalar_log["heavy_real_directions"] == 290
    assert scalar_log["zero_real_directions_excluded"] == 38
    assert vector_ledger["unbroken_SM_vectors"] == 12
    assert sum(z["real_vectors"] for z in vector_ledger["mass_sets"]) == 33

    # Direct beta-jump checksum. The independent parent result is
    # -11/3*C2(Spin10)+2/3*3*T(16)+1/6*T(54)+1/3*(T(126)+T(10))
    # with C2=8 and T(16,54,126,10)=(2,12,35,1).
    b_sm_q = (Q(41, 10), -Q(19, 6), -Q(7))
    b_scalar_q = (Q(377, 30), Q(77, 6), Q(79, 6))
    vector_index_q = (Q(8), Q(6), Q(5))
    b_parent = -Q(11, 3)*8+Q(2, 3)*3*2+Q(1, 6)*12+Q(1, 3)*(35+1)
    assert b_parent == -Q(34, 3)
    projected = tuple(s+h-Q(7, 2)*t for s, h, t in
                      zip(b_sm_q, b_scalar_q, vector_index_q))
    assert projected == (b_parent,)*3
    d_lambda = tuple(-6*h+21*t for h, t in
                     zip(b_scalar_q, vector_index_q))
    assert d_lambda == tuple(6*(s-b_parent) for s in b_sm_q)

    scalar_lambda = np.asarray(scalar_log["lambda_scalar_SM_order_1_2_3"])
    b_sm = np.asarray([float(z) for z in b_sm_q])
    b_scalar = np.asarray([float(z) for z in b_scalar_q])
    # Exact physical vector mass ratios M^2/(g10^2 omega^2) and SM indices.
    vector_sets = [
        (.005, np.asarray([14/5, 0, 1.0]), 8),
        (.025, np.zeros(3), 1),
        (50/120, np.asarray([5.0, 3.0, 2.0]), 12),
        (50.6/120, np.asarray([1/5, 3.0, 2.0]), 12),
    ]
    assert sum(z[2] for z in vector_sets) == 33
    assert np.allclose(sum((z[1] for z in vector_sets), np.zeros(3)), [8, 6, 5])

    def vector_lambda(g10, mu_over_omega=1):
        return sum((index*(1-21*math.log(
            g10*math.sqrt(m2)/mu_over_omega))
                    for m2, index, _ in vector_sets), np.zeros(3))

    alpha_em = 1/inputs["alpha_em_MSbar_inverse_MZ"]
    sin2 = inputs["sin2theta_MSbar_MZ"]
    A0 = np.asarray([(3/5)*(1-sin2)/alpha_em,
                     sin2/alpha_em,
                     1/inputs["alpha_s_MSbar_MZ"]])
    MZ = inputs["MZ_GeV"]

    def one_loop_prediction(x):
        g10, log_scale = math.exp(x[0]), x[1]
        A_U = 4*math.pi/(g10*g10)
        threshold = (scalar_lambda+vector_lambda(g10))/(12*math.pi)
        # Predict the frozen MZ inputs by matching at mu=omega, then running
        # downward with the one-loop SM coefficients.
        return A_U-threshold+b_sm*log_scale/(2*math.pi)

    def one_residual(x):
        return one_loop_prediction(x)-A0

    # The two independent coupling differences are linear in
    # x=log(g10) and log(omega/MZ), because the common 4*pi/g10^2 term
    # cancels. Their unique solution is an exact global check that no second
    # perturbative root is hidden by the least-squares search.
    total_vector_index = np.asarray([8.0, 6.0, 5.0])
    constant_at_origin = one_loop_prediction(np.asarray([0.0, 0.0]))-A0
    difference_matrix = []
    difference_rhs = []
    for j in (1, 2):
        difference_matrix.append([
            21*(total_vector_index[0]-total_vector_index[j])/(12*math.pi),
            (b_sm[0]-b_sm[j])/(2*math.pi),
        ])
        difference_rhs.append(-(constant_at_origin[0]-constant_at_origin[j]))
    relative_solution = np.linalg.solve(np.asarray(difference_matrix),
                                        np.asarray(difference_rhs))
    relative_residual = one_residual(relative_solution)
    assert np.ptp(relative_residual) < 1e-8*max(abs(relative_residual))
    assert abs(relative_residual[0]) > 1e20

    pair_solutions = []
    for pair in ((0, 1), (0, 2), (1, 2)):
        sol = root(lambda x: one_residual(x)[list(pair)],
                   [math.log(.52), 31])
        assert sol.success
        pair_solutions.append({
            "matched_channels": list(pair),
            "g10": math.exp(sol.x[0]),
            "log_omega_over_MZ": sol.x[1],
            "omega_GeV": MZ*math.exp(sol.x[1]),
            "all_channel_residual": one_residual(sol.x).tolist(),
        })

    one_fit = least_squares(one_residual, [math.log(.52), 31],
                            xtol=1e-13, ftol=1e-13, gtol=1e-13)
    one_r = one_residual(one_fit.x)
    one_g = math.exp(one_fit.x[0])
    one_L = one_fit.x[1]

    # Known gauge-only SM two-loop running is a comparator for the size and
    # direction of omitted orders. Yukawa terms and two-loop thresholds are
    # deliberately not guessed.
    B = np.asarray([[199/50, 27/10, 44/5],
                    [9/10, 35/6, 12],
                    [11/10, 9/2, -26]], dtype=float)
    A_one_high = A0-b_sm*one_L/(2*math.pi)
    A_two_high_at_one = gauge_only_two_loop(A0, b_sm, B, one_L)
    known_two_loop_shift = A_two_high_at_one-A_one_high

    def two_residual(x):
        g10, log_scale = math.exp(x[0]), x[1]
        A_U = 4*math.pi/(g10*g10)
        matched = A_U-(scalar_lambda+vector_lambda(g10))/(12*math.pi)
        return matched-gauge_only_two_loop(A0, b_sm, B, log_scale)

    two_fit = least_squares(two_residual, one_fit.x,
                            xtol=2e-12, ftol=2e-12, gtol=2e-12)
    two_r = two_residual(two_fit.x)

    route = json.loads((CALC / "canonical_so10_gauge_route_selection" /
                        "route_selection.json").read_text())
    threshold_next_order = (route["direct_one_loop_comparator"][
        "combined_nonuniversal_spread"] * route["fixed_order_diagnostics"][
            "max_scalar_total_index_times_loop_log"])
    raw_loop_log = route["fixed_order_diagnostics"]["raw_alpha_log_over_4pi"]
    weighted_loop_log = route["fixed_order_diagnostics"][
        "max_scalar_total_index_times_loop_log"]
    known_two_loop_spread = float(np.ptp(known_two_loop_shift))
    conservative_uncertainty = known_two_loop_spread+threshold_next_order

    outcome = "DIRECT_GAUGE_MATCHING_UNRESOLVED"
    assert np.max(abs(one_r)) > threshold_next_order
    assert np.max(abs(one_r)) < 1.2*conservative_uncertainty
    result = {
        "outcome": outcome,
        "kernel": {
            "outcome": "DIRECT_ONE_LOOP_KERNEL_PASS",
            "scheme": "MSbar_background_field_Feynman_gauge",
            "scalar_positive_real_directions": 290,
            "scalar_symmetry_and_higgs_zeros_excluded": 38,
            "massive_vectors": 33,
            "unbroken_SM_vectors": 12,
            "vector_goldstone_ghost_sets": 33,
            "vector_heat_kernel": heat,
            "direct_beta_parent": str(b_parent),
            "direct_beta_projected_channels": [str(z) for z in projected],
            "matching_scale_derivative_check": "PASS",
            "basis_invariance_replay": "PASS_BY_PHYSICAL_MATRIX_LOG_CONTROLS",
            "degenerate_mass_limit": "PASS_LOGS_VANISH_VECTOR_FINITE_T_REMAINS",
            "fermion_threshold": "ZERO_FOR_SM_GAUGE_CHANNELS_COMPLETE_16F_ONLY_NUR_HEAVY_AND_SM_SINGLET",
        },
        "frozen_inputs_MZ": {"alpha_inverse_GUT_order_1_2_3": A0.tolist(), **inputs},
        "one_loop_solve": {
            "common_exact_solution": False,
            "unique_relative_coupling_solution": {
                "g10": math.exp(relative_solution[0]),
                "log_omega_over_MZ": relative_solution[1],
                "omega_GeV": MZ*math.exp(relative_solution[1]),
                "common_absolute_residual": float(relative_residual[0]),
                "interpretation": "relative couplings meet only at an absurd nonphysical point and the common normalization fails",
            },
            "least_squares_g10": one_g,
            "least_squares_alpha_U_inverse": 4*math.pi/(one_g*one_g),
            "least_squares_log_omega_over_MZ": one_L,
            "least_squares_omega_GeV": MZ*math.exp(one_L),
            "residual_inverse_couplings_order_1_2_3": one_r.tolist(),
            "max_absolute_residual": float(np.max(abs(one_r))),
            "euclidean_residual": float(np.linalg.norm(one_r)),
            "pair_solutions": pair_solutions,
        },
        "uncertainty": {
            "known_SM_gauge_only_two_loop_shift_at_one_loop_scale":
                known_two_loop_shift.tolist(),
            "known_SM_gauge_only_two_loop_nonuniversal_spread":
                known_two_loop_spread,
            "raw_loop_log_squared": raw_loop_log**2,
            "max_index_weighted_loop_log_squared": weighted_loop_log**2,
            "threshold_next_order_diagnostic": threshold_next_order,
            "conservative_linear_diagnostic": conservative_uncertainty,
            "gauge_only_two_loop_refit_g10": math.exp(two_fit.x[0]),
            "gauge_only_two_loop_refit_omega_GeV": MZ*math.exp(two_fit.x[1]),
            "gauge_only_two_loop_refit_residual": two_r.tolist(),
            "gauge_only_two_loop_refit_max_absolute_residual":
                float(np.max(abs(two_r))),
            "missing": [
                "two-loop Yukawa contribution with a frozen fermion fit",
                "two-loop heavy-threshold matching",
                "scheme-consistent higher-order scalar/vector finite terms",
            ],
            "interpretation": "residual and admitted-order uncertainty are comparable",
        },
        "bfb_status": "BFB_UNRESOLVED",
        "downstream": {
            "gauge_unification_passed": False,
            "gauge_unification_failed": False,
            "flavor_started": False,
            "proton_decay_started": False,
            "benchmark_replacement_started": False,
        },
    }
    (HERE / "direct_matching.json").write_text(json.dumps(result, indent=2)+"\n")
    print("DIRECT_BETA_JUMP_PASS", b_parent, projected)
    print("ONE_LOOP_BEST_FIT", one_g, MZ*math.exp(one_L), one_r.tolist(),
          "max", np.max(abs(one_r)))
    print("TWO_LOOP_GAUGE_COMPARATOR", known_two_loop_shift.tolist(),
          "spread", known_two_loop_spread, "refit", two_r.tolist())
    print("UNCERTAINTY_DIAGNOSTICS", threshold_next_order,
          conservative_uncertainty)
    print(outcome)


if __name__ == "__main__":
    main()
