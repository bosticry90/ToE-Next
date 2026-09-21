"""Primary UVP_P03: direct doubled-line UV projection.

This route evaluates the doubled propagator directly.  It does not read the
P01 residue or use mass differentiation to obtain its answer.
"""

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
    t, m2, aux2, u = sp.symbols("t m2 aux2 u", positive=True)

    physical = 1 / (t + m2) ** 2
    auxiliary_master = 1 / (t + aux2) ** 2
    remainder = sp.factor(physical - auxiliary_master)
    expected_remainder = sp.factor(
        (aux2 - m2) * (2 * t + aux2 + m2)
        / ((t + m2) ** 2 * (t + aux2) ** 2)
    )
    assert sp.simplify(remainder - expected_remainder) == 0

    # Radialization supplies t^(1-epsilon).  The auxiliary master therefore
    # has t^(-1-epsilon)*(1+aux2/t)^-2.  Its u^0 coefficient is the pole.
    master_large_t_factor = sp.series(
        1 / (1 + aux2 * u) ** 2, u, 0, 4).removeO()
    normalized_residue = sp.expand(master_large_t_factor).coeff(u, 0)

    # The exact remainder starts as t^-3 before the radial t factor and is
    # therefore t^-2 after radialization: UV finite.  Verify its coefficient.
    remainder_large_t = sp.series(
        sp.simplify(remainder.subs(t, 1 / u)), u, 0, 4).removeO()
    remainder_coefficients = [
        sp.expand(remainder_large_t).coeff(u, power) for power in range(4)]
    leading_remainder_power = next(
        power for power, coefficient in enumerate(remainder_coefficients)
        if coefficient != 0)
    assert leading_remainder_power == 3
    assert sp.expand(remainder_large_t).coeff(u, 3) == 2 * (aux2 - m2)
    assert normalized_residue == 1
    assert sp.diff(normalized_residue, m2) == 0
    assert sp.diff(normalized_residue, aux2) == 0

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P03",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "direct_auxiliary_mass_doubled_line_UV_projection",
        "minkowski_integral": (
            "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d*"
            "(-i)/(k^2-m2+i0)^2]"
        ),
        "wick_rotated_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d/"
            "(k_E^2+m2)^2]"
        ),
        "dimension": "d=4-2*epsilon",
        "exact_auxiliary_rearrangement": (
            "1/(t+m2)^2=1/(t+aux2)^2+(aux2-m2)*(2*t+aux2+m2)/"
            "((t+m2)^2*(t+aux2)^2)"
        ),
        "auxiliary_master_large_t_factor": str(master_large_t_factor),
        "remainder_large_t_series": str(remainder_large_t),
        "remainder_leading_inverse_t_power": leading_remainder_power,
        "remainder_after_radialization": "O(t^-2-epsilon)_UV_finite",
        "normalized_residue": str(normalized_residue),
        "physical_mass_derivative_of_residue": "0",
        "auxiliary_mass_derivative_of_residue": "0",
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "pole_expression": "1/(16*pi^2*epsilon_bar)",
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p03_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P03_PRIMARY_COMPLETE")
    print("NORMALIZED_RESIDUE", payload["normalized_residue"])
    print("AUXILIARY_MASS_DERIVATIVE 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
