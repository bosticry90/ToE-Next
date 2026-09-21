"""Independent UVP_P02 replay from the closed Gamma-function bubble."""

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
    epsilon = sp.symbols("epsilon", positive=True)
    m2, mu2 = sp.symbols("m2 mu2", positive=True)
    d = 4 - 2 * epsilon

    closed_form = (
        mu2 ** epsilon
        * m2 ** (d / 2 - 2)
        * sp.gamma(2 - d / 2)
        / (4 * sp.pi) ** (d / 2)
    )
    normalized_residue = sp.simplify(
        sp.limit(epsilon * closed_form * 16 * sp.pi ** 2, epsilon, 0)
    )
    mass_derivative = sp.diff(normalized_residue, m2)
    assert mass_derivative == 0
    assert not normalized_residue.has(m2)

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P02",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "independent_Wick_rotation_and_two_propagator_Gamma_function_residue",
        "minkowski_integral": (
            "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d*"
            "(-i)/(k^2-m2+i0)^2]"
        ),
        "wick_rotated_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d/"
            "(k_E^2+m2)^2]"
        ),
        "closed_form": (
            "mu2^epsilon*(m2)^(d/2-2)*Gamma(2-d/2)/(4*pi)^(d/2)"
        ),
        "dimension": "d=4-2*epsilon",
        "normalized_residue_extraction": (
            "limit(epsilon*16*pi^2*closed_form,epsilon->0)"
        ),
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
    (HERE / "uvp_p02_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P02_INDEPENDENT_REPLAY_COMPLETE")
    print("NORMALIZED_RESIDUE", payload["normalized_residue"])
    print("MASS_DERIVATIVE", payload["mass_derivative_of_residue"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
