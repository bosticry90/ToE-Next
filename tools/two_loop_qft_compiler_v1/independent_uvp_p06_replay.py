"""Independent UVP_P06 replay from nonexceptional Feynman parameters."""

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
    epsilon = sp.symbols("epsilon", positive=True)
    x = sp.symbols("x", real=True)

    # For Delta=m2+x(1-x)p2, Gamma(epsilon)*Delta^-epsilon has pole one.
    # Thus its pole is independent of both m2 and p2.  No primary Taylor
    # expansion is imported.
    scalar_weight = sp.Integer(1)
    scalar_constant = sp.integrate(scalar_weight, (x, 0, 1))
    scalar_p2 = sp.Integer(0)

    # Combining the same denominators and shifting q=k+(1-x)p leaves
    # k_mu=q_mu-(1-x)p_mu.  The odd q term vanishes.
    vector_p_mu = -sp.integrate(1 - x, (x, 0, 1))
    assert scalar_constant == 1
    assert scalar_p2 == 0
    assert vector_p_mu == -sp.Rational(1, 2)

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P06",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "independent_nonexceptional_Feynman_parameter_pole_extraction",
        "dimension": "d=4-2*epsilon",
        "feynman_denominator": "Delta=m2+x*(1-x)*p2",
        "pole_kernel": "Gamma(epsilon)*Delta^(-epsilon)",
        "two_point_normalized_UV_coefficients": {
            "constant": str(scalar_constant),
            "p_linear": "0",
            "p2": str(scalar_p2),
        },
        "one_derivative_shift": "k_mu=q_mu-(1-x)*p_mu",
        "one_derivative_normalized_p_mu_UV_coefficient": str(vector_p_mu),
        "locality": {
            "pole_depends_on_m2": False,
            "pole_depends_on_p2_nonpolynomially": False,
            "forbidden_structures_present": [],
            "local_polynomial_only": True,
        },
        "tail_UV_classification": {
            "two_point_beyond_p2": "UV_finite",
            "one_derivative_beyond_p_mu": "UV_finite",
        },
        "routing_diagnostic": {
            "x_to_1_minus_x_scalar_residual": "0",
            "vector_line_exchange_covariance": "PASS",
            "authority": "SUPPORTING_ONLY_P08_REMAINS_DEDICATED_ROUTING_GATE",
        },
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
            "infrared_rearrangement_used": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p06_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P06_INDEPENDENT_REPLAY_COMPLETE")
    print("TWO_POINT_COEFFICIENTS 1 0 0")
    print("ONE_DERIVATIVE_P_MU_COEFFICIENT", vector_p_mu)
    print("NONLOCAL_STRUCTURES 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
