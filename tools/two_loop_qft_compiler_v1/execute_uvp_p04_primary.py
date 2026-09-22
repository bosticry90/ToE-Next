"""Primary UVP_P04: d-dimensional rank-two tensor UV reduction."""

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
    m2, u = sp.symbols("m2 u", positive=True)
    d = 4 - 2 * epsilon

    # For the scalar contraction of
    # Integral_E[k_mu k_nu/(k^2+m2)^2], radialization gives
    # t^(-epsilon)*(1+m2/t)^-2.  The u^1 term is the local logarithmic
    # UV coefficient at d=4; the u^0 term is power-like, not logarithmic.
    large_t_factor = sp.series(1 / (1 + m2 * u) ** 2, u, 0, 4).removeO()
    scalar_contraction_residue = sp.expand(large_t_factor).coeff(u, 1)
    assert scalar_contraction_residue == -2 * m2

    # Preserve the exact d-dimensional tensor average until after the
    # pole-times-epsilon algebra is resolved.
    tensor_reduction_coefficient = 1 / d
    exact_pole_kernel = scalar_contraction_residue / (d * epsilon)
    premature_d4_kernel = scalar_contraction_residue / (4 * epsilon)
    normalized_tensor_residue = sp.simplify(
        sp.limit(epsilon * exact_pole_kernel, epsilon, 0))
    contraction_residual = sp.simplify(
        d * tensor_reduction_coefficient * scalar_contraction_residue
        - scalar_contraction_residue)
    adversarial_finite_shift = sp.simplify(sp.limit(
        exact_pole_kernel - premature_d4_kernel, epsilon, 0))

    assert normalized_tensor_residue == -m2 / 2
    assert contraction_residual == 0
    assert adversarial_finite_shift == -m2 / 4

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P04",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "d_dimensional_rotational_tensor_reducer_with_radial_UV_projector",
        "euclidean_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k/(2*pi)^d*"
            "k_mu*k_nu/(k^2+m2)^2]"
        ),
        "dimension": "d=4-2*epsilon",
        "tensor_identity": "T_mu_nu=delta_mu_nu*S/d",
        "scalar_contraction": (
            "S=mu^(2*epsilon)*Integral_E[d^d k/(2*pi)^d*"
            "k^2/(k^2+m2)^2]"
        ),
        "large_t_factor": str(large_t_factor),
        "logarithmic_u_power": 1,
        "scalar_contraction_normalized_residue": str(scalar_contraction_residue),
        "tensor_reduction_coefficient_before_laurent": "1/(4-2*epsilon)",
        "normalized_tensor_residue_coefficient": str(normalized_tensor_residue),
        "tensor_pole_expression": (
            "delta_mu_nu*(-m2/2)/(16*pi^2*epsilon_bar)"
        ),
        "contraction_residual": str(contraction_residual),
        "operation_order": [
            "form_scalar_contraction_in_d_dimensions",
            "apply_exact_delta_mu_nu_over_d",
            "retain_d_equals_4_minus_2epsilon",
            "resolve_pole_times_epsilon_terms",
            "extract_UV_pole",
        ],
        "adversarial_premature_d4": {
            "used_by_promoted_route": False,
            "shortcut_coefficient": "1/4",
            "pole_residue_coefficient": str(normalized_tensor_residue),
            "missed_finite_shift_exact_minus_shortcut_in_1_over_16pi2_units": str(
                adversarial_finite_shift),
        },
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p04_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P04_PRIMARY_COMPLETE")
    print("TENSOR_RESIDUE_COEFFICIENT", normalized_tensor_residue)
    print("CONTRACTION_RESIDUAL", contraction_residual)
    print("PREMATURE_D4_MISSED_FINITE_SHIFT", adversarial_finite_shift)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
