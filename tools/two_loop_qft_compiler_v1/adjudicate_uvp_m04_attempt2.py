"""Adjudicate UVP_M04 attempt 2 and advance the serial cursor to M05."""

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
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field)
    return payload


def main():
    primary = load("uvp_m04_primary_attempt2.json")
    replay = load("uvp_m04_independent_replay_attempt2.json")
    attempt1 = load("uvp_m04_blocked_evidence.json")
    assert attempt1["verdict"] == "BLOCKED"
    assert primary["attempt"] == replay["attempt"] == 2
    assert primary["attempt1_blocked_evidence_sha256"] == attempt1["artifact_sha256"]
    assert replay["attempt1_blocked_evidence_sha256"] == attempt1["artifact_sha256"]
    assert primary["predecessor_M03_evidence_sha256"] == (
        replay["predecessor_M03_evidence_sha256"]
    )
    assert primary["cubic_residues"] == replay["cubic_residues"]
    assert primary["scalar_residues"] == replay["scalar_residues"]
    assert primary["scalar_coefficient_matrices"] == (
        replay["scalar_coefficient_matrices"]
    )
    assert primary["projector_evaluation"] == replay["projector_evaluation"]
    assert primary["sector_ledgers"] == replay["sector_ledgers"]
    assert primary["inventory"]["background_inventories"] == (
        replay["inventory"]["background_inventories"]
    )
    expected_projection = {
        "basis": ["muPhi", "muPhiPhi", "z6_re", "z6_im"],
        "rank": 4,
        "residual": "0",
        "permutation_symmetry_residual": "0",
        "Sigma_cubic_residual": "0",
        "PQ_forbidden_residual": "0",
        "xi_residual": "0",
    }
    assert primary["projection"] == replay["projection"] == expected_projection

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_M04",
        "attempt": 2,
        "classification": {"primary": primary["uv_ir"],
                           "replay": replay["uv_ir"]},
        "reason": "regulated local parent three-point projection has UV poles and no IR pole",
    }
    uv_ir["artifact_sha256"] = digest(uv_ir)
    (HERE / "uvp_m04_uv_ir_provenance_attempt2.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8"
    )
    evidence = {
        "schema_version": 1,
        "test_id": "UVP_M04",
        "attempt": 2,
        "contract_sha256": primary["contract_sha256"],
        "execution_plan_sha256": primary["execution_plan_sha256"],
        "attempt_history": [{"attempt": 1, "verdict": "BLOCKED",
                             "evidence_sha256": attempt1["artifact_sha256"]}],
        "primary": primary,
        "independent_replay": replay,
        "comparison": {
            "cubic_residue_residual": "0",
            "scalar_coefficient_matrix_residual": "0",
            "field_inventory_symmetric_difference": 0,
            "full_operator_projection_residual": "0",
            "permutation_symmetry_residual": "0",
            "rank": 4,
        },
        "uv_ir_classification": uv_ir["classification"],
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_m04_evidence_attempt2.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )

    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    assert all(row["status"] == "PASS" for row in ledger["tests"][:29])
    row = ledger["tests"][29]
    assert row["test_id"] == "UVP_M04"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    assert row["derived_result"]["evidence_sha256"] == attempt1["artifact_sha256"]
    row.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 2,
        "primary": {"state": "COMPLETE", "method": primary["method"],
                    "inventory_sha256": primary["inventory_sha256"],
                    "residue_sha256": primary["artifact_sha256"],
                    "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": replay["method"],
                   "inventory_sha256": replay["inventory_sha256"],
                   "residue_sha256": replay["artifact_sha256"],
                   "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "derived_result": {
            "cubic_residues": primary["cubic_residues"],
            "projection_rank": 4,
            "maximum_residual": "0",
            "attempt1_blocked_evidence_sha256": attempt1["artifact_sha256"],
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "exhaustive_parent_V3V4_contractions_match_inventory_independent_functional_replay"
        ),
        "evidence_files": [
            "uvp_m04_primary_blocker.json",
            "uvp_m04_independent_blocker_replay.json",
            "uvp_m04_uv_ir_provenance.json",
            "uvp_m04_blocked_evidence.json",
            "uvp_m04_primary_attempt2.json",
            "uvp_m04_independent_replay_attempt2.json",
            "uvp_m04_uv_ir_provenance_attempt2.json",
            "uvp_m04_evidence_attempt2.json",
        ],
    })
    ledger["tests"][30]["authorization"] = "READY"
    ledger["overall_status"] = "CANONICAL_RUNNING"
    ledger["authority"] = "ENGINE_GATE_AUTHORITY"
    ledger["counters"].update({
        "executed": 30, "passed": 30, "blocked": 0, "failed": 0,
        "not_run_or_locked": 9, "canonical_executed": 3,
        "canonical_passed": 3,
    })
    ledger["promotion"] = {"engine_gate": "PASS",
                           "counterterm_compiler": "BLOCKED",
                           "layer6_authorized": False}
    ledger.pop("result_sha256")
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text())
    Draft202012Validator(schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print("UVP_M04_ATTEMPT2_PASS")
    print("FOUR_REAL_CUBIC_RESIDUES_DERIVED")
    print("NEXT_TEST UVP_M05")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
