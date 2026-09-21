"""Fail-fast tree operator gate for the frozen candidate PS split."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import sys

from sympy import Matrix

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
for name in ("canonical_so10_vacuum_kernel", "canonical_so10_scalar_reconstruction",
             "canonical_so10_scalar_benchmark"):
    sys.path.insert(0, str(CALC / name))

from derive_stabilizers import form_action, generators
from verify_eta1_doublet_mixing import vacuum_form
from check_gauge_hierarchy import spectrum

PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"


def verify(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == expected, path


def main():
    verify(CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md",
           PARENT_HASH)
    verify(CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH)
    error = json.loads((CALC / "canonical_so10_ps_eft_error_budget" /
                        "error_budget.json").read_text())
    target = error["accuracy_target_inverse_coupling"]

    phi0 = Matrix.diag(*([-2]*6+[3]*4))
    sigma0 = vacuum_form()
    idx5 = tuple(combinations(range(10), 5))
    phi_cols, sigma_cols = [], []
    sigma_nonzero = 0
    sigma_k = set()
    for (i, j), g in generators():
        if (i < 6) == (j < 6):
            continue
        dp = g*phi0-phi0*g
        ds = form_action(g, sigma0)
        phi_cols.append(Matrix(list(dp)))
        sigma_cols.append(Matrix(
            [ds.get(k, (0, 0))[0] for k in idx5]
            +[ds.get(k, (0, 0))[1] for k in idx5]))
        if ds:
            sigma_nonzero += 1
            sigma_k.update(min(sum(q < 6 for q in key),
                               6-sum(q < 6 for q in key)) for key in ds)
    phi_orbit = Matrix.hstack(*phi_cols)
    sigma_orbit = Matrix.hstack(*sigma_cols)
    combined = Matrix.vstack(phi_orbit, sigma_orbit)
    assert (len(phi_cols), phi_orbit.rank(), sigma_orbit.rank(),
            combined.rank()) == (24, 24, 12, 24)
    assert sigma_nonzero == 24 and sigma_k == {2}

    # The exact physical orbit Gram has 12 states at 50 and 12 at 50.6.
    _, _, all_ev = spectrum(.1)
    assert sum(abs(z-50) < 1e-10 for z in all_ev) == 12
    assert sum(abs(z-50.6) < 1e-10 for z in all_ev) == 12
    # In L = 1/2 A M2 A + g A J, M2=g2 K with
    # K/omega2=raw_gram/120. Eliminating A gives
    # -1/2 J K^-1 J, hence the coefficients below in omega^-2.
    c50 = -Fraction(60, 50)
    c506 = -Fraction(300, 253)  # 50.6 = 253/5
    assert c50 == -Fraction(6, 5)

    q = error["quadratic_and_derivative_diagnostics"]
    retained_to_heavy = q["retained_to_heavy_ratio"]
    retained_to_vector = q["retained_to_upper_vector_m2_ratio"]
    scalar_dim6_tail = retained_to_heavy/(1-retained_to_heavy)
    scalar_dim8_tail = retained_to_heavy**2/(1-retained_to_heavy)
    assert retained_to_vector > 1
    assert q["log_lipschitz_bound_closes"] is False
    result = {
        "disposition": "PS_EFT_ERROR_UNRESOLVED",
        "accuracy_target_inverse_coupling": target,
        "goldstone_disposition": {
            "upper_vectors": 24,
            "phi_orbit_rank": phi_orbit.rank(),
            "sigma_projection_rank": sigma_orbit.rank(),
            "combined_orbit_rank": combined.rank(),
            "upper_generators_with_nonzero_sigma_projection": sigma_nonzero,
            "sigma_projection_ps_origin": "126_k2_(15,2,2)",
            "valid_local_gauge_slice": "set_54_(6,2,2)_orbit_coordinates_to_zero",
            "ghosts": "24_complex_only_in_loop_gauge_fixing_not_tree_spectrum",
        },
        "upper_vector_tree_operator": {
            "form": "-1/2 J_A (K_V^-1)_AB J_B",
            "mass_form": "M_V^2=g10^2 K_V",
            "coefficients_over_inverse_omega2": [
                {"multiplicity": 12, "raw_gram": 50,
                 "coefficient": str(c50), "decimal": float(c50)},
                {"multiplicity": 12, "raw_gram": "253/5",
                 "coefficient": str(c506), "decimal": float(c506)},
            ],
            "ps_limit_coefficient": str(c50),
        },
        "candidate_heavy_scalar_tree_operator": {
            "real_directions": 132,
            "exact_form": "-1/2 J_H^T (M_HH^2-D^2)^-1 J_H",
            "local_leading_form": "-1/2 J_H^T (M_HH^2)^-1 J_H",
            "retained_to_heavy_m2_ratio": retained_to_heavy,
            "dimension6_inverse_tail_diagnostic": scalar_dim6_tail,
            "dimension8_inverse_tail_diagnostic": scalar_dim8_tail,
            "complete_cubic_source_tensor_compiled": False,
        },
        "one_loop_F2_insertion": {
            "retained_to_coarse_upper_vector_m2_ratio": retained_to_vector,
            "finite_local_vector_series_convergent_on_all_retained_modes": False,
            "scalar_matrix_log_bound_closed": False,
            "background_field_operator_insertion_computed": False,
        },
        "rerun_error_gate": "NOT_ADMISSIBLE_MISSING_INSERTION_COEFFICIENTS",
    }
    (HERE / "tree_operator_gate.json").write_text(json.dumps(result, indent=2)+"\n")
    print("UPPER_GOLDSTONE_ORBIT", 24, "PHI_RANK", phi_orbit.rank(),
          "SIGMA_K2_RANK", sigma_orbit.rank())
    print("VECTOR_CURRENT_CURRENT_COEFFICIENTS", c50, c506, "over_omega2")
    print("SCALAR_LOCAL_INVERSE_TAILS", scalar_dim6_tail, scalar_dim8_tail)
    print("RETAINED_TO_COARSE_VECTOR_M2", retained_to_vector)
    print("PS_EFT_ERROR_UNRESOLVED")


if __name__ == "__main__":
    main()
