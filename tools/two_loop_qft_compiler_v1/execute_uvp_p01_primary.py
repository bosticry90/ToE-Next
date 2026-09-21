"""Primary UVP_P01 calculation: asymptotic UV projection with auxiliary mass."""

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
    m2, aux2, u = sp.symbols("m2 aux2 u", positive=True)

    # After radializing in d=4-2 epsilon, J1 has a t^-epsilon base and
    # J2 a t^(-1-epsilon) base.  The indicated coefficients are therefore
    # precisely the logarithmic large-t terms.  No Gamma-function integral is
    # used in this primary route.
    j1_series_factor = sp.series(1 / (1 + aux2 * u), u, 0, 3).removeO()
    j2_series_factor = sp.series(1 / (1 + aux2 * u) ** 2, u, 0, 2).removeO()
    j1_log_coefficient = sp.expand(j1_series_factor).coeff(u, 1)
    j2_log_coefficient = sp.expand(j2_series_factor).coeff(u, 0)
    radial_prefactor_d4 = sp.Rational(1, 16) / sp.pi ** 2

    # Exact auxiliary-mass rearrangement:
    # 1/(t+m2) = 1/(t+aux2) + (aux2-m2)/(t+aux2)^2 + R,
    # with R ~ t^-3 and hence UV finite after the four-dimensional radial
    # measure.  The normalized pole coefficient is the bracket below.
    normalized_residue = sp.simplify(
        j1_log_coefficient + (aux2 - m2) * j2_log_coefficient)
    assert j1_log_coefficient == -aux2
    assert j2_log_coefficient == 1
    assert not normalized_residue.has(aux2)
    assert radial_prefactor_d4 == 1 / (16 * sp.pi ** 2)

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P01",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "large_loop_momentum_radial_UV_projection_with_auxiliary_mass",
        "integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d/"
            "(k_E^2+m2)]"
        ),
        "dimension": "d=4-2*epsilon",
        "radial_prefactor_at_d4": "1/(16*pi^2)",
        "auxiliary_mass_symbol": "aux2",
        "exact_rearrangement": (
            "1/(t+m2)=1/(t+aux2)+(aux2-m2)/(t+aux2)^2+"
            "(aux2-m2)^2/((t+m2)*(t+aux2)^2)"
        ),
        "master_log_coefficients": {
            "J1_aux2": str(j1_log_coefficient),
            "J2_aux2": str(j2_log_coefficient),
        },
        "remainder_UV_behavior": "radial_integrand_O(t^-2-epsilon)_UV_finite",
        "auxiliary_mass_cancelled": True,
        "normalized_residue": str(normalized_residue),
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "pole_expression": pole_expression(normalized_residue),
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p01_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P01_PRIMARY_COMPLETE")
    print("NORMALIZED_RESIDUE", payload["normalized_residue"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
