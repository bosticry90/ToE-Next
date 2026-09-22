"""Record UVP_M05 as the first fail-fast blocker after M04 passes."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload); work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field)
    return payload


def main():
    primary = load("uvp_m05_primary_blocker.json")
    replay = load("uvp_m05_independent_blocker_replay.json")
    assert primary["blocker_code"] == replay["blocker_code"]
    assert primary["classification"] == replay["classification"]
    assert not primary["all_26_real_quartic_directions_derived"]
    assert not replay["all_26_real_quartic_directions_derived"]
    uv_ir = {
        "schema_version": 1, "test_id": "UVP_M05", "attempt": 1,
        "classification": {"primary": primary["uv_ir"],
                           "replay": replay["uv_ir"]},
        "reason": "UV_IR classification deferred because complete 1PI four-point integrands do not exist",
    }
    uv_ir["artifact_sha256"] = digest(uv_ir)
    (HERE / "uvp_m05_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8"
    )
    evidence = {
        "schema_version": 1, "test_id": "UVP_M05", "attempt": 1,
        "contract_sha256": primary["contract_sha256"],
        "execution_plan_sha256": primary["execution_plan_sha256"],
        "primary": primary, "independent_replay": replay,
        "comparison": {"blocker_agreement": True,
                       "blocker_code": primary["blocker_code"],
                       "physics_failure": False, "residues_derived": False},
        "uv_ir_classification": uv_ir["classification"], "verdict": "BLOCKED",
    }
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_m05_blocked_evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )

    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    assert all(row["status"] == "PASS" for row in ledger["tests"][:30])
    row = ledger["tests"][30]
    assert row["test_id"] == "UVP_M05" and row["authorization"] == "READY"
    assert row["status"] == "NOT_RUN"
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
            "required_exhaustive_parent_scalar_4pt_contraction_gauge_completion_and_projection_are_not_implemented"
        ),
        "evidence_files": ["uvp_m05_primary_blocker.json",
                           "uvp_m05_independent_blocker_replay.json",
                           "uvp_m05_uv_ir_provenance.json",
                           "uvp_m05_blocked_evidence.json"],
    })
    ledger["overall_status"] = "CANONICAL_BLOCKED"
    ledger["authority"] = "ENGINE_GATE_AUTHORITY"
    ledger["counters"].update({
        "executed": 31, "passed": 30, "blocked": 1, "failed": 0,
        "not_run_or_locked": 8, "canonical_executed": 4,
        "canonical_passed": 3,
    })
    ledger["promotion"] = {"engine_gate": "PASS",
                           "counterterm_compiler": "BLOCKED",
                           "layer6_authorized": False}
    assert all(item["status"] == "NOT_RUN" and
               item["authorization"] == "WAITING_PREDECESSOR"
               for item in ledger["tests"][31:])
    ledger.pop("result_sha256")
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text())
    Draft202012Validator(schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print("UVP_M05_BLOCKED")
    print("BLOCKER_CODE", primary["blocker_code"])
    print("FAIL_FAST_STOP 31/39")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
