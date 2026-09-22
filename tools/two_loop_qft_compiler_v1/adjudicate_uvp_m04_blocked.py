"""Record UVP_M04 as the first fail-fast blocker after M03 passes."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload)
    work.pop(field, None)
    return sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text())
    assert payload[field] == digest(payload, field)
    return payload


def main():
    primary = load("uvp_m04_primary_blocker.json")
    replay = load("uvp_m04_independent_blocker_replay.json")
    assert primary["blocker_code"] == replay["blocker_code"]
    assert primary["classification"] == replay["classification"]
    assert not primary["all_four_real_cubic_directions_derived"]
    assert not replay["all_four_real_cubic_directions_derived"]
    uv_ir = {
        "schema_version": 1, "test_id": "UVP_M04", "attempt": 1,
        "classification": {"primary": primary["uv_ir"],
                           "replay": replay["uv_ir"]},
        "reason": "UV_IR classification deferred because 1PI three-point integrands do not exist",
    }
    uv_ir["artifact_sha256"] = digest(uv_ir)
    (HERE / "uvp_m04_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n"
    )
    evidence = {
        "schema_version": 1, "test_id": "UVP_M04", "attempt": 1,
        "contract_sha256": primary["contract_sha256"],
        "execution_plan_sha256": primary["execution_plan_sha256"],
        "primary": primary, "independent_replay": replay,
        "comparison": {"blocker_agreement": True,
                       "blocker_code": primary["blocker_code"],
                       "physics_failure": False, "residues_derived": False},
        "uv_ir_classification": uv_ir["classification"],
        "verdict": "BLOCKED",
    }
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_m04_blocked_evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n"
    )

    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text())
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    assert all(row["status"] == "PASS" for row in ledger["tests"][:29])
    row = ledger["tests"][29]
    assert row["test_id"] == "UVP_M04" and row["authorization"] == "READY"
    row.update({
        "status": "BLOCKED", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE", "method": primary["method"],
                    "inventory_sha256": primary["inventory_sha256"],
                    "residue_sha256": primary["artifact_sha256"],
                    "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": replay["method"],
                   "inventory_sha256": replay["inventory_sha256"],
                   "residue_sha256": replay["artifact_sha256"],
                   "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "derived_result": {"residues_derived": False,
                           "blocker_code": primary["blocker_code"],
                           "classification": primary["classification"],
                           "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": (
            "required_exhaustive_parent_scalar_3pt_contraction_and_projection_kernel_is_not_implemented"
        ),
        "evidence_files": ["uvp_m04_primary_blocker.json",
                           "uvp_m04_independent_blocker_replay.json",
                           "uvp_m04_uv_ir_provenance.json",
                           "uvp_m04_blocked_evidence.json"],
    })
    ledger["overall_status"] = "CANONICAL_BLOCKED"
    ledger["authority"] = "ENGINE_GATE_AUTHORITY"
    ledger["counters"].update({
        "executed": 30, "passed": 29, "blocked": 1, "failed": 0,
        "not_run_or_locked": 9, "canonical_executed": 3,
        "canonical_passed": 2,
    })
    ledger["promotion"] = {"engine_gate": "PASS",
                           "counterterm_compiler": "BLOCKED",
                           "layer6_authorized": False}
    assert all(item["status"] == "NOT_RUN" and
               item["authorization"] == "WAITING_PREDECESSOR"
               for item in ledger["tests"][30:])
    ledger.pop("result_sha256")
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text())
    Draft202012Validator(schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    print("UVP_M04_BLOCKED")
    print("BLOCKER_CODE", primary["blocker_code"])
    print("FAIL_FAST_STOP 30/39")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
