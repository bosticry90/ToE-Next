"""Primary UVP_P02: radial large-loop-momentum logarithmic projector."""

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


def pole_expression(residue):
    if residue.could_extract_minus_sign():
        return f"-{sp.sstr(-residue)}/(16*pi^2*epsilon_bar)"
    return f"{sp.sstr(residue)}/(16*pi^2*epsilon_bar)"


def main():
    m2, u = sp.symbols("m2 u", positive=True)

    # Radialization gives t^(1-epsilon)/(t+m2)^2 =
    # t^(-1-epsilon)*(1+m2/t)^-2.  Only the u^0 coefficient multiplies
    # t^(-1-epsilon) and hence only it contributes to the logarithmic pole.
    large_t_factor = sp.series(1 / (1 + m2 * u) ** 2, u, 0, 4).removeO()
    normalized_residue = sp.expand(large_t_factor).coeff(u, 0)
    mass_derivative = sp.diff(normalized_residue, m2)
    mass_dependent_UV_finite_tail = sp.expand(large_t_factor - normalized_residue)
    radial_prefactor_d4 = sp.Rational(1, 16) / sp.pi ** 2

    assert mass_derivative == 0
    assert not normalized_residue.has(m2)
    assert sp.limit(mass_dependent_UV_finite_tail, u, 0) == 0
    assert radial_prefactor_d4 == 1 / (16 * sp.pi ** 2)

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P02",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "radial_large_loop_momentum_logarithmic_UV_projector",
        "integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d/"
            "(k_E^2+m2)^2]"
        ),
        "dimension": "d=4-2*epsilon",
        "large_t_factor": str(large_t_factor),
        "logarithmic_term": "t^(-1-epsilon)*u^0_coefficient",
        "mass_dependent_tail": str(mass_dependent_UV_finite_tail),
        "mass_dependent_tail_classification": "UV_finite",
        "radial_prefactor_at_d4": "1/(16*pi^2)",
        "normalized_residue": str(normalized_residue),
        "mass_derivative_of_residue": str(mass_derivative),
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "pole_expression": pole_expression(normalized_residue),
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p02_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P02_PRIMARY_COMPLETE")
    print("NORMALIZED_RESIDUE", payload["normalized_residue"])
    print("MASS_DERIVATIVE", payload["mass_derivative_of_residue"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
