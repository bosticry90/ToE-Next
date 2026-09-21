"""Adjudicate UVP_P01 and advance the frozen ledger only on exact agreement."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import sympy as sp


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def canonical_hash(payload, hash_field="artifact_sha256"):
    work = dict(payload)
    work.pop(hash_field, None)
    return sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload["artifact_sha256"] == canonical_hash(payload)
    assert payload["contract_sha256"] == CONTRACT_HASH
    assert payload["execution_plan_sha256"] == PLAN_HASH
    return payload


def main():
    primary = load_verified("uvp_p01_primary.json")
    replay = load_verified("uvp_p01_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    schema = json.loads((HERE / "uvp_p01_evidence_schema.json").read_text(
        encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)

    row = ledger["tests"][0]
    assert row["test_id"] == "UVP_P01"
    assert row["status"] == "NOT_RUN"
    assert row["authorization"] == "READY"
    assert row["attempt"] == 0
    assert ledger["counters"]["executed"] == 0
    assert all(test["status"] not in {"PASS", "BLOCKED", "FAIL", "RUNNING"}
               for test in ledger["tests"][1:])

    p_residue = sp.sympify(primary["normalized_residue"])
    r_residue = sp.sympify(replay["normalized_residue"])
    difference = sp.simplify(p_residue - r_residue)
    passed = (
        difference == 0
        and primary["pole_expression"] == replay["pole_expression"]
        and primary["uv_ir"] == replay["uv_ir"]
        and primary["auxiliary_mass_cancelled"] is True
    )
    if not passed:
        raise AssertionError("UVP_P01 primary/replay or convention mismatch")

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_P01",
        "mass_domain": "m2>0",
        "classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "auxiliary_mass_cancelled": True, "rstar_required": False,
        },
        "reason": (
            "positive_mass_removes_IR_singularity; superficial_quadratic_"
            "divergence_contains_local_m2_log_pole_under_dimensional_"
            "analytic_continuation"
        ),
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p01_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")

    convention = {
        "dimension": "d=4-2*epsilon",
        "minkowski_integral": (
            "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d * i/(k^2-m2+i0)]"
        ),
        "wick_rotated_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d * 1/(k_E^2+m2)]"
        ),
        "measure": "d^d k/(2*pi)^d",
        "epsilon_bar": "1/epsilon_bar=1/epsilon-gamma_E+log(4*pi)",
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "mass_domain": "m2>0",
    }
    evidence = {
        "schema_version": 1,
        "test_id": "UVP_P01",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "convention": convention,
        "primary": primary,
        "independent_replay": replay,
        "uv_ir_classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "auxiliary_mass_cancelled": True, "rstar_required": False,
        },
        "comparison": {
            "normalized_residue_difference": str(difference),
            "pole_expression_equal": True,
            "convention_equal": True,
        },
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = canonical_hash(evidence)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(evidence)
    (HERE / "uvp_p01_evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    row.update({
        "status": "PASS",
        "authorization": "TERMINAL",
        "attempt": 1,
        "primary": {
            "state": "COMPLETE",
            "method": primary["method"],
            "inventory_sha256": None,
            "residue_sha256": primary["artifact_sha256"],
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "replay": {
            "state": "COMPLETE",
            "method": replay["method"],
            "inventory_sha256": None,
            "residue_sha256": replay["artifact_sha256"],
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "derived_result": {
            "normalized_residue": primary["normalized_residue"],
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "pole_expression": primary["pole_expression"],
            "primary_minus_replay": "0",
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "primary_auxiliary_mass_UV_projection_equals_independent_"
            "Gamma_function_replay_exactly_in_frozen_convention"
        ),
        "evidence_files": [
            "uvp_p01_primary.json", "uvp_p01_independent_replay.json",
            "uvp_p01_uv_ir_provenance.json", "uvp_p01_evidence.json",
        ],
    })
    ledger["tests"][1]["authorization"] = "READY"
    ledger["overall_status"] = "ENGINE_RUNNING"
    ledger["authority"] = "PARTIAL_TEST_AUTHORITY"
    ledger["counters"].update({
        "executed": 1, "passed": 1, "not_run_or_locked": 38,
        "engine_executed": 1, "engine_passed": 1,
    })
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("UVP_P01_PASS")
    print("NORMALIZED_RESIDUE", primary["normalized_residue"])
    print("POLE", primary["pole_expression"])
    print("NEXT_TEST UVP_P02")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
