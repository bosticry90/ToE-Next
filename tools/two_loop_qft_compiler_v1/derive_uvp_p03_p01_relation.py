"""Third UVP_P03 route: differentiate the frozen P01 pole after verification."""

from hashlib import sha256
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def canonical_hash(payload, field="artifact_sha256"):
    work = dict(payload)
    embedded = work.pop(field)
    actual = sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert embedded == actual
    return actual


def main():
    p01 = json.loads((HERE / "uvp_p01_evidence.json").read_text(
        encoding="utf-8"))
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text(
        encoding="utf-8"))
    p01_evidence_hash = canonical_hash(p01)
    assert ledger["tests"][0]["test_id"] == "UVP_P01"
    assert ledger["tests"][0]["status"] == "PASS"
    assert ledger["tests"][0]["derived_result"][
        "evidence_sha256"] == p01_evidence_hash

    m2, k2 = sp.symbols("m2 k2")
    imaginary_unit = sp.I
    p01_integrand = imaginary_unit / (k2 - m2)
    differentiated_integrand = sp.diff(p01_integrand, m2)
    p03_integrand = -imaginary_unit / (k2 - m2) ** 2
    integrand_relation_residual = sp.simplify(
        p03_integrand + differentiated_integrand)
    assert integrand_relation_residual == 0

    frozen_p01_residue = sp.sympify(
        p01["primary"]["normalized_residue"])
    derivative_prediction = sp.simplify(-sp.diff(frozen_p01_residue, m2))
    assert derivative_prediction == 1

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P03",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "mass_derivative_of_verified_frozen_P01_pole",
        "frozen_p01_evidence_sha256": p01_evidence_hash,
        "frozen_p01_normalized_residue": str(frozen_p01_residue),
        "p01_integrand": "+i/(k2-m2+i0)",
        "p01_mass_derivative_integrand": "+i/(k2-m2+i0)^2",
        "p03_integrand": "-i/(k2-m2+i0)^2",
        "integrand_identity": "P03_integrand=-d(P01_integrand)/d(m2)",
        "integrand_relation_residual": str(integrand_relation_residual),
        "pole_identity": "P03_pole=-d(P01_pole)/d(m2)",
        "normalized_derivative_prediction": str(derivative_prediction),
        "pole_expression": "1/(16*pi^2*epsilon_bar)",
    }
    payload["artifact_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (HERE / "uvp_p03_p01_derivative_relation.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P03_P01_DERIVATIVE_RELATION_COMPLETE")
    print("NORMALIZED_DERIVATIVE_PREDICTION", derivative_prediction)
    print("INTEGRAND_RELATION_RESIDUAL", integrand_relation_residual)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
