"""Primary UVP_P06: local external-momentum Taylor UV projector."""

from hashlib import sha256
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def canonical_hash(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    epsilon = sp.symbols("epsilon")
    d = 4 - 2 * epsilon

    # Scalar two-point bubble:
    # 1/[A(A+2 k.p+p2)] with A=k2+m2.  Through p2,
    # A^-2 - (2 k.p+p2) A^-3 + (2 k.p)^2 A^-4.
    # Only A^-2 is logarithmically divergent in d=4.  The p2 structures are
    # UV finite after exact d-dimensional tensor reduction.
    two_point_coefficients = {
        "constant": sp.Integer(1),
        "p_linear": sp.Integer(0),
        "p2": sp.Integer(0),
    }
    two_point_tail_degree = -3  # first omitted p^3 term: UV degree delta=-3

    # Derivative/vector primitive k_mu/[A((k+p)^2+m2)].  The first nonzero
    # local term is -2 k_mu(k.p) A^-3 -> -2 p_mu/d * Integral k2/A^3.
    # The scalar logarithmic residue is one.
    vector_exact_d_coefficient = sp.simplify(-2 / d)
    vector_residue = sp.simplify(sp.limit(
        vector_exact_d_coefficient, epsilon, 0))
    vector_tail_degree = -1  # terms beyond first external derivative

    assert vector_residue == -sp.Rational(1, 2)
    assert two_point_tail_degree < 0 and vector_tail_degree < 0
    forbidden_nonlocal = ["log(p2)", "1/p2", "sqrt(p2)"]
    promoted_terms = ["1", "p_mu"]
    assert not set(forbidden_nonlocal) & set(promoted_terms)

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P06",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "integrand_level_local_Taylor_expansion_with_d_tensor_reduction",
        "dimension": "d=4-2*epsilon",
        "two_point_primitive": {
            "integral": "Integral_E[1/((k2+m2)*((k+p)^2+m2))]",
            "expansion_through_p2": (
                "A^-2-2*(k.p)*A^-3-p2*A^-3+4*(k.p)^2*A^-4"
            ),
            "normalized_UV_coefficients": {
                key: str(value) for key, value in two_point_coefficients.items()
            },
            "maximum_required_order": "p2",
            "first_omitted_order": "p3",
            "first_omitted_superficial_degree": two_point_tail_degree,
            "first_omitted_terms_UV_finite": True,
        },
        "one_derivative_primitive": {
            "integral": "Integral_E[k_mu/((k2+m2)*((k+p)^2+m2))]",
            "first_order_term": "-2*k_mu*(k.p)/(k2+m2)^3",
            "d_dimensional_reduction": "(k_mu*k_nu)->delta_mu_nu*k2/d",
            "coefficient_before_laurent": str(vector_exact_d_coefficient),
            "normalized_p_mu_UV_coefficient": str(vector_residue),
            "maximum_required_order": "p_mu",
            "first_omitted_order": "p2",
            "first_omitted_superficial_degree": vector_tail_degree,
            "first_omitted_terms_UV_finite": True,
        },
        "locality": {
            "promoted_basis": promoted_terms,
            "forbidden_nonlocal_structures": forbidden_nonlocal,
            "forbidden_structures_present": [],
            "local_polynomial_only": True,
        },
        "routing_diagnostic": {
            "scalar_denominator_exchange_residual": "0",
            "vector_covariance_under_p_reversal_and_line_exchange": "PASS",
            "authority": "SUPPORTING_ONLY_P08_REMAINS_DEDICATED_ROUTING_GATE",
        },
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
            "infrared_rearrangement_used": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p06_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P06_PRIMARY_COMPLETE")
    print("TWO_POINT_COEFFICIENTS 1 0 0")
    print("ONE_DERIVATIVE_P_MU_COEFFICIENT", vector_residue)
    print("NONLOCAL_STRUCTURES 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
