"""Next-order direct physical-vacuum Spin(10)->SM gauge test.

The passed one-loop heavy threshold is kept fixed.  The low-energy evolution
is upgraded to two-loop SM gauge running with the one-loop third-family
Yukawa/Higgs system required at this order.  This is deliberately *not*
promoted to a full two-loop GUT match: the script exposes the residual
matching-scale dependence and the missing model-dependent two-loop heavy
decoupling data separately.
"""

from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root


HERE = Path(__file__).resolve().parent
CALC = HERE.parent

PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"

PI = math.pi
LOOP = 16 * PI**2


def verify(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == expected, path


# GUT-normalized g1.  The two-loop gauge matrix and Yukawa coefficients are
# the standard MSbar SM coefficients in this normalization.
B1 = np.asarray([41 / 10, -19 / 6, -7.0])
B2 = np.asarray(
    [[199 / 50, 27 / 10, 44 / 5],
     [9 / 10, 35 / 6, 12],
     [11 / 10, 9 / 2, -26]],
    dtype=float,
)
CYT = np.asarray([17 / 10, 3 / 2, 2.0])
CYB = np.asarray([1 / 2, 3 / 2, 2.0])
CYTAU = np.asarray([3 / 2, 1 / 2, 0.0])


def beta_coupled(_, state, include_yukawa_in_gauge=True):
    """Two-loop gauge plus one-loop yt,yb,ytau,lambda running.

    One-loop Yukawa running is the perturbatively consistent accuracy needed
    inside the two-loop gauge term.  Lambda is evolved as a consistency
    monitor; it first enters the gauge beta function beyond two loops.
    The potential convention is V=-m^2 H^dag H+lambda(H^dag H)^2.
    """
    g = state[:3]
    yt, yb, ytau, lam = state[3:]
    g2 = g * g
    yuk = CYT * yt * yt + CYB * yb * yb + CYTAU * ytau * ytau
    if not include_yukawa_in_gauge:
        yuk = np.zeros(3)
    dg = B1 * g**3 / LOOP + g**3 * (B2 @ g2 - yuk) / LOOP**2

    dyt = yt * (
        4.5 * yt**2 + 1.5 * yb**2 + ytau**2
        - 17 / 20 * g2[0] - 9 / 4 * g2[1] - 8 * g2[2]
    ) / LOOP
    dyb = yb * (
        1.5 * yt**2 + 4.5 * yb**2 + ytau**2
        - 1 / 4 * g2[0] - 9 / 4 * g2[1] - 8 * g2[2]
    ) / LOOP
    dytau = ytau * (
        3 * yt**2 + 3 * yb**2 + 2.5 * ytau**2
        - 9 / 4 * g2[0] - 9 / 4 * g2[1]
    ) / LOOP

    trace_y2 = 3 * yt**2 + 3 * yb**2 + ytau**2
    trace_y4 = 3 * yt**4 + 3 * yb**4 + ytau**4
    dlam = (
        24 * lam**2
        - (9 / 5 * g2[0] + 9 * g2[1]) * lam
        + 27 / 200 * g2[0]**2
        + 9 / 20 * g2[0] * g2[1]
        + 9 / 8 * g2[1]**2
        + 4 * lam * trace_y2
        - 2 * trace_y4
    ) / LOOP
    return np.concatenate((dg, [dyt, dyb, dytau, dlam]))


def build_flow(A0, MZ, mt, weak_boundary, include_yukawa_in_gauge=True):
    """Construct a dense coupled flow while imposing Yukawa data at mt."""
    g_mz = np.sqrt(4 * PI / A0)
    t_mt = math.log(mt / MZ)

    def mismatch(low_y):
        state0 = np.concatenate((g_mz, low_y))
        sol = solve_ivp(
            lambda t, y: beta_coupled(t, y, include_yukawa_in_gauge),
            (0, t_mt), state0, rtol=3e-11, atol=2e-13,
        )
        assert sol.success
        return sol.y[3:, -1] - weak_boundary

    solved = root(mismatch, weak_boundary)
    assert solved.success, solved.message
    state0 = np.concatenate((g_mz, solved.x))
    t_max = math.log(1e19 / MZ)
    flow = solve_ivp(
        lambda t, y: beta_coupled(t, y, include_yukawa_in_gauge),
        (0, t_max), state0, rtol=3e-11, atol=2e-13, dense_output=True,
    )
    assert flow.success
    at_mt = flow.sol(t_mt)
    assert np.max(abs(at_mt[3:] - weak_boundary)) < 2e-9
    return flow, state0, at_mt


def alpha_inverse(flow, log_mu_over_mz):
    g = flow.sol(log_mu_over_mz)[:3]
    return 4 * PI / (g * g)


def main():
    verify(CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md", PARENT_HASH)
    verify(CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH)

    prior = json.loads((CALC / "canonical_so10_direct_gauge_matching" /
                        "direct_matching.json").read_text())
    assert prior["kernel"]["outcome"] == "DIRECT_ONE_LOOP_KERNEL_PASS"
    assert prior["outcome"] == "DIRECT_GAUGE_MATCHING_UNRESOLVED"

    scalar_log = json.loads((CALC / "canonical_so10_matrix_threshold" /
                             "scalar_matrix_log.json").read_text())
    scalar_lambda_at_omega = np.asarray(
        scalar_log["lambda_scalar_SM_order_1_2_3"], dtype=float)
    b_scalar = np.asarray([377 / 30, 77 / 6, 79 / 6], dtype=float)
    vector_sets = [
        (0.005, np.asarray([14 / 5, 0, 1.0])),
        (0.025, np.zeros(3)),
        (50 / 120, np.asarray([5.0, 3.0, 2.0])),
        (50.6 / 120, np.asarray([1 / 5, 3.0, 2.0])),
    ]
    assert np.allclose(sum((z[1] for z in vector_sets), np.zeros(3)), [8, 6, 5])

    inputs = prior["frozen_inputs_MZ"]
    A0 = np.asarray(inputs["alpha_inverse_GUT_order_1_2_3"], dtype=float)
    MZ = float(inputs["MZ_GeV"])

    # Weak-scale Yukawa/Higgs matching is a frozen boundary comparator, not a
    # fermion fit.  yt and lambda use the reference MSbar formulas at mt;
    # yb and ytau are nuisance inputs whose deliberately broad variations are
    # propagated below.
    mt = 173.34
    mh = 125.15
    alpha_s_mz = float(inputs["alpha_s_MSbar_MZ"])
    yt_mt = 0.93690 - 0.00042 * ((alpha_s_mz - 0.1184) / 0.0007)
    weak_boundary = np.asarray([yt_mt, 0.0164, 0.0102, 0.12604], dtype=float)

    coupled, state_mz, state_mt = build_flow(A0, MZ, mt, weak_boundary, True)
    no_yuk_gauge, _, _ = build_flow(A0, MZ, mt, weak_boundary, False)

    def scalar_lambda(kappa):
        return scalar_lambda_at_omega - 6 * b_scalar * math.log(kappa)

    def vector_lambda(g10, kappa):
        return sum((index * (1 - 21 * math.log(g10 * math.sqrt(m2) / kappa))
                    for m2, index in vector_sets), np.zeros(3))

    def residual(x, kappa, flow=coupled):
        g10, omega = math.exp(x[0]), math.exp(x[1])
        mu = kappa * omega
        t = math.log(mu / MZ)
        matched = (4 * PI / g10**2
                   - (scalar_lambda(kappa) + vector_lambda(g10, kappa)) /
                   (12 * PI))
        return matched - alpha_inverse(flow, t)

    prior_fit = prior["one_loop_solve"]
    start = np.asarray([math.log(prior_fit["least_squares_g10"]),
                        math.log(prior_fit["least_squares_omega_GeV"])])

    fits = []
    for kappa in (0.5, 0.75, 1.0, 1.5, 2.0):
        fit = least_squares(lambda x: residual(x, kappa), start,
                            xtol=2e-13, ftol=2e-13, gtol=2e-13)
        r = residual(fit.x, kappa)
        fits.append({
            "kappa_mu_over_omega": kappa,
            "g10": math.exp(fit.x[0]),
            "omega_GeV": math.exp(fit.x[1]),
            "matching_scale_GeV": kappa * math.exp(fit.x[1]),
            "residual_inverse_couplings": r.tolist(),
            "max_absolute_residual": float(np.max(abs(r))),
            "euclidean_residual": float(np.linalg.norm(r)),
        })
        start = fit.x

    central = next(z for z in fits if z["kappa_mu_over_omega"] == 1.0)
    central_x = np.log([central["g10"], central["omega_GeV"]])
    central_t = math.log(central["omega_GeV"] / MZ)
    central_running_state = coupled.sol(central_t)
    yukawa_gauge_shift = (alpha_inverse(coupled, central_t)
                          - alpha_inverse(no_yuk_gauge, central_t))

    pair_solutions = []
    for pair in ((0, 1), (0, 2), (1, 2)):
        solved = root(lambda x: residual(x, 1.0)[list(pair)], central_x)
        assert solved.success
        rr = residual(solved.x, 1.0)
        pair_solutions.append({
            "matched_channels": list(pair),
            "g10": math.exp(solved.x[0]),
            "omega_GeV": math.exp(solved.x[1]),
            "all_channel_residual": rr.tolist(),
            "unmatched_channel_residual": float(rr[({0, 1, 2} - set(pair)).pop()]),
        })
    assert min(abs(z["unmatched_channel_residual"]) for z in pair_solutions) > 1e-3

    # Broad weak-boundary variations test the relevance of the unfitted
    # bottom/tau inputs and the reference top/quartic boundary.  These do not
    # substitute for the missing GUT two-loop threshold.
    variations = {
        "yt_plus_0p006": weak_boundary + np.asarray([0.006, 0, 0, 0]),
        "yt_minus_0p006": weak_boundary + np.asarray([-0.006, 0, 0, 0]),
        "yb_plus_20pct": weak_boundary * np.asarray([1, 1.2, 1, 1]),
        "yb_minus_20pct": weak_boundary * np.asarray([1, 0.8, 1, 1]),
        "ytau_plus_20pct": weak_boundary * np.asarray([1, 1, 1.2, 1]),
        "ytau_minus_20pct": weak_boundary * np.asarray([1, 1, 0.8, 1]),
        "lambda_plus_0p002": weak_boundary + np.asarray([0, 0, 0, 0.002]),
        "lambda_minus_0p002": weak_boundary + np.asarray([0, 0, 0, -0.002]),
    }
    sensitivity = {}
    for name, boundary in variations.items():
        flow, _, _ = build_flow(A0, MZ, mt, boundary, True)
        fit = least_squares(lambda x: residual(x, 1.0, flow), central_x,
                            xtol=2e-12, ftol=2e-12, gtol=2e-12)
        rr = residual(fit.x, 1.0, flow)
        sensitivity[name] = {
            "max_absolute_residual": float(np.max(abs(rr))),
            "change_from_central": float(np.max(abs(rr))
                                           - central["max_absolute_residual"]),
            "residual_inverse_couplings": rr.tolist(),
        }

    scale_residuals = np.asarray([z["max_absolute_residual"] for z in fits])
    scale_envelope = float(np.ptp(scale_residuals))
    residual_floor = float(np.min(scale_residuals))
    residual_ceiling = float(np.max(scale_residuals))
    max_weak_input_effect = max(abs(z["change_from_central"])
                                for z in sensitivity.values())

    # Perturbative-order audit.  A complete two-loop heavy decoupling
    # coefficient is model-dependent.  It receives pure gauge/scalar terms
    # and Yukawa-dependent heavy-light terms.  The canonical Yukawa matrices
    # and their phases are not frozen, and no calculation-local two-loop
    # massive-vacuum integral basis has been derived.  Therefore no rigorous
    # numerical bound smaller than the residual is available.  Scale
    # variation is retained as a diagnostic, not used as such a bound.
    matching_order = {
        "one_loop_heavy_kernel": "PASS_PRESERVED",
        "two_loop_SM_gauge_running": "PASS",
        "one_loop_yukawa_higgs_coupled_running": "PASS_REQUIRED_ACCURACY",
        "higgs_quartic_enters_two_loop_gauge_beta": False,
        "two_loop_heavy_gauge_scalar_decoupling": "NOT_DERIVED",
        "two_loop_heavy_yukawa_decoupling": "UNDERDEFINED_CANONICAL_YUKAWA_MATRICES_NOT_FROZEN",
        "rigorous_next_heavy_threshold_bound": None,
        "matching_scale_variation_role": "DIAGNOSTIC_NOT_A_RIGOROUS_BOUND",
    }

    outcome = "DIRECT_GAUGE_MATCHING_UNRESOLVED"
    assert central["max_absolute_residual"] > 0
    assert matching_order["rigorous_next_heavy_threshold_bound"] is None

    result = {
        "outcome": outcome,
        "preserved_kernel": "DIRECT_ONE_LOOP_KERNEL_PASS",
        "authority": "TWO_LOOP_SM_RUNNING_PLUS_ONE_LOOP_PHYSICAL_HEAVY_MATCH_AND_UNCERTAINTY_AUDIT",
        "scheme": "MSbar_GUT_NORMALIZED_G1",
        "sources": {
            "two_loop_SM_RGE": "https://arxiv.org/abs/hep-ph/0207271",
            "weak_scale_MSbar_boundary": "https://arxiv.org/abs/1307.3536",
        },
        "rge": {
            "gauge_order": "TWO_LOOP",
            "yukawa_order": "ONE_LOOP_CONSISTENT_FOR_TWO_LOOP_GAUGE",
            "higgs_quartic_order": "ONE_LOOP_MONITOR",
            "included_yukawas": ["top", "bottom", "tau"],
            "lighter_yukawas": "NEGLECTED_WITH_TRACE_SUPPRESSION",
            "weak_scale_boundary_mu_GeV": mt,
            "weak_scale_boundary_yt_yb_ytau_lambda": weak_boundary.tolist(),
            "solved_MZ_boundary_yt_yb_ytau_lambda": state_mz[3:].tolist(),
            "replayed_mt_state_g1_g2_g3_yt_yb_ytau_lambda": state_mt.tolist(),
            "central_scale_state_g1_g2_g3_yt_yb_ytau_lambda":
                central_running_state.tolist(),
            "yukawa_term_shift_in_alpha_inverse_at_central_scale": yukawa_gauge_shift.tolist(),
        },
        "central_refit": central,
        "known_next_order_common_exact_solution": False,
        "known_next_order_pair_solutions": pair_solutions,
        "matching_scale_scan": fits,
        "matching_scale_max_residual_range": [residual_floor, residual_ceiling],
        "matching_scale_max_residual_envelope": scale_envelope,
        "weak_boundary_sensitivity": sensitivity,
        "max_weak_boundary_effect_on_max_residual": max_weak_input_effect,
        "matching_order_audit": matching_order,
        "verdict_logic": {
            "pass_requires_common_solution_with_residual_below_controlled_uncertainty": True,
            "fail_requires_minimum_residual_decisively_above_complete_uncertainty": True,
            "complete_higher_order_uncertainty_available": False,
            "reason": "model-dependent two-loop heavy decoupling is neither computed nor rigorously bounded; canonical Yukawa data needed by part of it are unfrozen",
        },
        "bfb_status": "BFB_UNRESOLVED",
        "downstream": {
            "gauge_unification_passed": False,
            "gauge_unification_failed": False,
            "physical_g10_or_omega_promoted": False,
            "flavor_started": False,
            "proton_decay_started": False,
            "PS_resummation_started": False,
            "replacement_benchmark_search_started": False,
        },
    }
    (HERE / "next_order.json").write_text(json.dumps(result, indent=2) + "\n")

    print("COUPLED_TWO_LOOP_CENTRAL", central)
    print("YUKAWA_GAUGE_SHIFT", yukawa_gauge_shift.tolist())
    print("SCALE_ENVELOPE", scale_envelope, "range", residual_floor, residual_ceiling)
    print("MAX_WEAK_BOUNDARY_EFFECT", max_weak_input_effect)
    print(outcome)


if __name__ == "__main__":
    main()
