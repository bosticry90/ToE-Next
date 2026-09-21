"""Independent UVP_P03 replay from the general Euclidean Gamma integral."""

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
    alpha = sp.Integer(2)
    d = 4 - 2 * epsilon

    # General Euclidean one-denominator formula, specialized only after it is
    # constructed.  This replay imports neither the primary rearrangement nor
    # the frozen P01 residue.
    closed_form = (
        mu2 ** epsilon
        * m2 ** (d / 2 - alpha)
        * sp.gamma(alpha - d / 2)
        / ((4 * sp.pi) ** (d / 2) * sp.gamma(alpha))
    )
    normalized_residue = sp.simplify(
        sp.limit(epsilon * 16 * sp.pi ** 2 * closed_form, epsilon, 0)
    )
    assert normalized_residue == 1
    assert sp.diff(normalized_residue, m2) == 0

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P03",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "independent_general_alpha_Gamma_function_replay",
        "general_formula": (
            "mu2^epsilon*(m2)^(d/2-alpha)*Gamma(alpha-d/2)/"
            "((4*pi)^(d/2)*Gamma(alpha))"
        ),
        "specialized_propagator_power": 2,
        "dimension": "d=4-2*epsilon",
        "normalized_residue_extraction": (
            "limit(epsilon*16*pi^2*closed_form,epsilon->0)"
        ),
        "normalized_residue": str(normalized_residue),
        "physical_mass_derivative_of_residue": "0",
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "pole_expression": "1/(16*pi^2*epsilon_bar)",
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p03_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P03_INDEPENDENT_REPLAY_COMPLETE")
    print("NORMALIZED_RESIDUE", payload["normalized_residue"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
