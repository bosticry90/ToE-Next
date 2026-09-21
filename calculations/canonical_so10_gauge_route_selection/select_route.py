"""Bounded route selection for canonical gauge matching.

The threshold values below are feasibility comparators. They are not a
complete Spin(10)->SM match and do not solve the physical scales.
"""

from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"


def verify(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == expected, path


def spread(x):
    return float(np.max(x)-np.min(x))


def main():
    verify(CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md",
           PARENT_HASH)
    verify(CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH)
    scalar = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "scalar_sm_ledger.json").read_text())
    vector = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "vector_ledger.json").read_text())
    coarse = json.loads((CALC / "canonical_so10_gauge_matching" /
                         "coarse_one_loop.json").read_text())

    scalar_states = []
    for row in scalar["blocks"]:
        masses2 = row["mass_squared_over_omega_squared"][
            row["zero_multiplicity"]:]
        b = np.asarray(row["one_loop_b_per_physical_eigenvalue"], dtype=float)
        for m2 in masses2:
            assert m2 > 0
            scalar_states.append((math.sqrt(m2), b, row["sm_irrep"]))
    assert scalar["heavy_real_dimension"] == 290
    assert scalar["zero_real_dimension"] == 38

    gu = coarse["g_U"]  # diagnostic only; not a fitted result
    vector_index = {
        0.6: np.asarray([14/5, 0, 1.0]),
        3.0: np.zeros(3),
        50.0: np.asarray([5.0, 3.0, 2.0]),
        50.6: np.asarray([1/5, 3.0, 2.0]),
    }
    vector_sets = []
    for row in vector["mass_sets"]:
        raw = float(row["raw_gram_eigenvalue"])
        mass = gu*math.sqrt(row["mass_squared_over_g10_squared_omega_squared"])
        vector_sets.append((mass, vector_index[raw], row["real_vectors"], raw))
    assert sum(z[2] for z in vector_sets) == 33
    assert np.allclose(sum((z[1] for z in vector_sets), np.zeros(3)), [8, 6, 5])

    scalar_masses = [z[0] for z in scalar_states]
    vector_masses = [z[0] for z in vector_sets for _ in range(z[2])]
    all_masses = scalar_masses+vector_masses
    mu = min(all_masses)  # below every integrated mode in the comparator
    max_mass = max(all_masses)
    log_span = math.log(max_mass/mu)
    log_m2_span = 2*log_span

    # For a real scalar, Delta alpha^-1=-b log(m/mu)/(2 pi) in the
    # convention already used by the matrix-log calculation.
    scalar_delta = sum((-b*math.log(m/mu)/(2*math.pi)
                        for m, b, _ in scalar_states), np.zeros(3))
    scalar_contributions = []
    for m, b, irrep in scalar_states:
        delta = -b*math.log(m/mu)/(2*math.pi)
        scalar_contributions.append({
            "mass_over_omega": m,
            "sm_irrep": irrep,
            "delta_alpha_inverse": delta.tolist(),
            "nonuniversal_spread": spread(delta),
        })
    scalar_contributions.sort(key=lambda x: x["nonuniversal_spread"],
                              reverse=True)

    # Universal massive-vector BFM formula from the passed lower-vector
    # comparator. It must be rederived for all 33 vectors in the admitted
    # direct scheme before it becomes matching authority.
    vector_delta = np.zeros(3)
    vector_rows = []
    for m, index, multiplicity, raw in vector_sets:
        lam = index*(1-21*math.log(m/mu))
        delta = -lam/(12*math.pi)
        vector_delta += delta
        vector_rows.append({
            "raw_gram": raw,
            "real_vectors": multiplicity,
            "mass_over_omega_using_coarse_g": m,
            "log_m_over_mu": math.log(m/mu),
            "sm_index": index.tolist(),
            "delta_alpha_inverse_comparator": delta.tolist(),
        })

    combined = scalar_delta+vector_delta
    alpha_u = 1/coarse["alpha_U_inverse"]
    raw_loop_log = alpha_u*log_span/(4*math.pi)
    scalar_beta = np.asarray([377/30, 77/6, 79/6], dtype=float)
    assert np.allclose(sum((z[1] for z in scalar_states), np.zeros(3)),
                       scalar_beta)
    scalar_weighted = raw_loop_log*max(scalar_beta)
    vector_weighted = raw_loop_log*8

    result = {
        "outcome": "ADMIT_DIRECT_MATCHING_FEASIBILITY",
        "authority": "ROUTE_SELECTION_AND_DIRECT_FIXED_ORDER_FEASIBILITY_ONLY",
        "bfb_status": "BFB_UNRESOLVED",
        "physical_spectrum": {
            "positive_scalar_real_directions": 290,
            "scalar_mass_eigenvalues": len(scalar_states),
            "massive_vectors": 33,
            "reference_mu_over_omega": mu,
            "min_heavy_mass_over_omega": mu,
            "max_heavy_mass_over_omega": max_mass,
            "max_to_min_mass_ratio": max_mass/mu,
            "largest_log_mass_ratio": log_span,
            "largest_log_mass_squared_ratio": log_m2_span,
        },
        "direct_one_loop_comparator": {
            "coarse_g_used_only_for_vector_mass_diagnostic": gu,
            "scalar_delta_alpha_inverse": scalar_delta.tolist(),
            "scalar_nonuniversal_spread": spread(scalar_delta),
            "vector_delta_alpha_inverse": vector_delta.tolist(),
            "vector_nonuniversal_spread": spread(vector_delta),
            "combined_delta_alpha_inverse": combined.tolist(),
            "combined_nonuniversal_spread": spread(combined),
            "required_coarse_shift_range": coarse[
                "inverse_coupling_difference_shift_needed_for_vector_ratio_range"],
            "largest_scalar_state_nonuniversal_terms": scalar_contributions[:8],
            "vector_sets": vector_rows,
            "not_a_matching_result": True,
        },
        "fixed_order_diagnostics": {
            "alpha_u_coarse": alpha_u,
            "raw_alpha_log_over_4pi": raw_loop_log,
            "max_scalar_total_index_times_loop_log": scalar_weighted,
            "max_vector_total_index_times_loop_log": vector_weighted,
            "interpretation": (
                "logs are material but not parametrically fatal; a complete "
                "one-loop direct match and explicit two-loop uncertainty are required"
            ),
        },
        "route_A_exact_PS": {
            "finite_local_expansion_available": False,
            "remaining": [
                "complete 132-real heavy-scalar source functional",
                "nonlocal scalar determinant with mixed mass operators",
                "nondegenerate vector-Goldstone-ghost functional determinant",
                "PS interval UV/EFT hard-region subtraction",
                "two-boundary matching-scale cancellation",
            ],
            "authority_if_completed": "RESUMMED_TWO_BOUNDARY_MATCHING",
            "relative_implementation_cost": "HIGH",
        },
        "route_B_direct": {
            "mass_operators_commute_with_unbroken_SM": True,
            "already_earned": [
                "complete physical scalar matrix log",
                "complete scalar and vector mass/index ledgers",
                "basis-invariant SM projector machinery",
                "massive-vector finite/log coefficient in the lower comparator",
            ],
            "minimal_remaining": [
                "single-scheme BFM UV/EFT fluctuation subtraction",
                "all-33 vector Goldstone ghost finite/log replay",
                "direct beta-jump and matching-scale cancellation",
                "coupled omega g10 and measured-coupling solve",
                "explicit two-loop/log truncation uncertainty",
            ],
            "authority_if_completed": "ONE_STEP_FIXED_ORDER_PHYSICAL_VACUUM_MATCH",
            "relative_implementation_cost": "MEDIUM",
        },
        "route_C_benchmark_replacement": {
            "admitted": False,
            "reason": "both matching languages have not yet failed for this benchmark",
        },
        "downstream": {
            "full_direct_match_started": False,
            "exact_PS_match_resumed": False,
            "benchmark_search_started": False,
            "flavor_or_proton_decay_started": False,
        },
    }
    assert log_span < 4
    assert raw_loop_log < .01
    assert scalar_weighted < .1
    assert spread(combined) > min(result["direct_one_loop_comparator"][
        "required_coarse_shift_range"])
    (HERE / "route_selection.json").write_text(json.dumps(result, indent=2)+"\n")
    print("DIRECT_MASS_LOG_SPAN", log_span, "MASS_RATIO", max_mass/mu)
    print("DIRECT_FIXED_ORDER_DIAGNOSTICS", raw_loop_log,
          scalar_weighted, vector_weighted)
    print("DIRECT_COMPARATOR_SPREADS", spread(scalar_delta),
          spread(vector_delta), spread(combined))
    print("ADMIT_DIRECT_MATCHING_FEASIBILITY")


if __name__ == "__main__":
    main()
