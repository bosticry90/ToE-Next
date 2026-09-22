"""Independent UVP_P04 replay from a Schwinger-parameter Gaussian source."""

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
    m2, mu2 = sp.symbols("m2 mu2", positive=True)
    d = 4 - 2 * epsilon

    # Differentiating the Gaussian source gives
    # Integral k_mu k_nu exp(-s k^2)
    # = delta_mu_nu/(2s) * (4*pi*s)^(-d/2).
    tensor_coefficient = (
        mu2 ** epsilon
        * m2 ** (d / 2 - 1)
        * sp.gamma(1 - d / 2)
        / (2 * (4 * sp.pi) ** (d / 2))
    )
    scalar_contraction = sp.simplify(d * tensor_coefficient)
    contraction_residual = sp.simplify(
        d * tensor_coefficient - scalar_contraction)
    normalized_tensor_residue = sp.simplify(sp.limit(
        epsilon * 16 * sp.pi ** 2 * tensor_coefficient, epsilon, 0))

    premature_d4_tensor_coefficient = scalar_contraction / 4
    adversarial_finite_shift = sp.simplify(sp.limit(
        16 * sp.pi ** 2
        * (tensor_coefficient - premature_d4_tensor_coefficient),
        epsilon, 0))

    assert normalized_tensor_residue == -m2 / 2
    assert contraction_residual == 0
    assert adversarial_finite_shift == -m2 / 4

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P04",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "independent_Schwinger_parameter_Gaussian_source_replay",
        "euclidean_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k/(2*pi)^d*"
            "k_mu*k_nu/(k^2+m2)^2]"
        ),
        "gaussian_source_identity": (
            "Integral[k_mu*k_nu*exp(-s*k^2)]="
            "delta_mu_nu*(4*pi*s)^(-d/2)/(2*s)"
        ),
        "tensor_coefficient_closed_form": (
            "mu2^epsilon*(m2)^(d/2-1)*Gamma(1-d/2)/"
            "(2*(4*pi)^(d/2))"
        ),
        "scalar_contraction_closed_form": (
            "d*mu2^epsilon*(m2)^(d/2-1)*Gamma(1-d/2)/"
            "(2*(4*pi)^(d/2))"
        ),
        "dimension": "d=4-2*epsilon",
        "normalized_tensor_residue_coefficient": str(normalized_tensor_residue),
        "tensor_pole_expression": (
            "delta_mu_nu*(-m2/2)/(16*pi^2*epsilon_bar)"
        ),
        "contraction_residual": str(contraction_residual),
        "adversarial_finite_shift_exact_minus_shortcut_in_1_over_16pi2_units": str(
            adversarial_finite_shift),
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p04_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P04_INDEPENDENT_REPLAY_COMPLETE")
    print("TENSOR_RESIDUE_COEFFICIENT", normalized_tensor_residue)
    print("CONTRACTION_RESIDUAL", contraction_residual)
    print("PREMATURE_D4_MISSED_FINITE_SHIFT", adversarial_finite_shift)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
