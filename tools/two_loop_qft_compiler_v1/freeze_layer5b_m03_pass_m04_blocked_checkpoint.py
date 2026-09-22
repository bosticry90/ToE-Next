"""Freeze the authoritative Layer-5B 30/39 fail-fast checkpoint."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload)
    work.pop(field, None)
    packed = json.dumps(work, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def load_verified(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field)
    return payload


def main():
    ledger = load_verified("uv_pole_evaluator_results.json", "result_sha256")
    engine = load_verified("uv_pole_engine_gate_result.json")
    m02 = load_verified("uvp_m02_evidence.json")
    m03_attempt1 = load_verified("uvp_m03_blocked_evidence.json")
    m03 = load_verified("uvp_m03_evidence_attempt2.json")
    m04 = load_verified("uvp_m04_blocked_evidence.json")

    assert ledger["overall_status"] == "CANONICAL_BLOCKED"
    assert ledger["counters"] == {
        "total_required": 39,
        "executed": 30,
        "passed": 29,
        "blocked": 1,
        "failed": 0,
        "not_run_or_locked": 9,
        "engine_required": 27,
        "engine_executed": 27,
        "engine_passed": 27,
        "canonical_required": 12,
        "canonical_executed": 3,
        "canonical_passed": 2,
    }
    assert ledger["promotion"] == {
        "engine_gate": "PASS",
        "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }
    assert engine["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert m02["verdict"] == "PASS"
    assert m03_attempt1["verdict"] == "BLOCKED"
    assert m03["verdict"] == "PASS"
    assert m03["attempt_history"] == [{
        "attempt": 1,
        "verdict": "BLOCKED",
        "evidence_sha256": m03_attempt1["artifact_sha256"],
    }]
    assert m04["verdict"] == "BLOCKED"
    assert m04["comparison"]["physics_failure"] is False
    assert all(row["status"] == "PASS" for row in ledger["tests"][:29])
    assert ledger["tests"][29]["test_id"] == "UVP_M04"
    assert ledger["tests"][29]["status"] == "BLOCKED"
    assert all(row["status"] == "NOT_RUN" for row in ledger["tests"][30:])

    checkpoint = {
        "schema_version": 1,
        "outcome": "CANONICAL_BLOCKED",
        "first_test_executed_in_resume": "UVP_M03_ATTEMPT_2",
        "last_test_reached": "UVP_M04",
        "progress": {
            "total": "30/39",
            "passed": 29,
            "blocked": 1,
            "failed": 0,
            "engine": "27/27",
            "canonical": "3/12 executed; 2 PASS; 1 BLOCKED",
        },
        "earned": {
            "uv_pole_evaluator": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
            "counterterm_compiler": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
            "M02_parent_scalar_wavefunction_residues": "PASS",
            "M03_parent_scalar_quadratic_residues": "PASS_ATTEMPT_2",
        },
        "M03_attempt_history": [
            {
                "attempt": 1,
                "verdict": "BLOCKED",
                "evidence_sha256": m03_attempt1["artifact_sha256"],
            },
            {
                "attempt": 2,
                "verdict": "PASS",
                "evidence_sha256": m03["artifact_sha256"],
            },
        ],
        "first_non_pass": {
            "test_id": "UVP_M04",
            "verdict": "BLOCKED",
            "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
            "blocker_code": (
                "M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING"
            ),
            "missing_capabilities": m04["primary"]["inventory"]["missing"],
            "evidence_sha256": m04["artifact_sha256"],
        },
        "hashes": {
            "contract_sha256": ledger["contract_sha256"],
            "execution_plan_sha256": ledger["execution_plan_sha256"],
            "ledger_sha256": ledger["result_sha256"],
            "engine_gate_artifact_sha256": engine["artifact_sha256"],
            "M02_evidence_sha256": m02["artifact_sha256"],
            "M03_attempt1_evidence_sha256": m03_attempt1["artifact_sha256"],
            "M03_attempt2_evidence_sha256": m03["artifact_sha256"],
            "M04_evidence_sha256": m04["artifact_sha256"],
        },
        "preserved_dispositions": ledger["preserved_dispositions"],
        "layer6_authorized": False,
    }
    checkpoint["artifact_sha256"] = digest(checkpoint)
    (HERE / "layer5b_m03_pass_m04_blocked_checkpoint.json").write_text(
        json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8"
    )

    status_path = HERE / "compiler_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status.pop("layer5a_M03_blocker_code", None)
    status.update({
        "next_gate": "IMPLEMENT_M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR",
        "layer5_parent_operator_radiative_pole_closure": (
            "BLOCKED_AT_M04_PARENT_CUBIC_POLE_EXTRACTION"
        ),
        "layer5_missing_required_residues": [
            item for item in status["layer5_missing_required_residues"]
            if item != "delta_parent_quadratic_4"
        ],
        "layer5_blocker": (
            "M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING"
        ),
        "layer5a_tests_executed": 30,
        "layer5a_execution_progress": "30_OF_39_ENGINE_27_OF_27",
        "layer5a_current_result_sha256": ledger["result_sha256"],
        "layer5a_evaluator_implementation": (
            "P01_P13_C01_C13_M01_PRIMARY_AND_INDEPENDENT_REPLAY_PASS"
        ),
        "layer5a_M03": "PASS_ATTEMPT2_FOUR_PARENT_QUADRATIC_RESIDUES",
        "layer5a_M03_attempt1_blocker_code": (
            "M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING"
        ),
        "layer5a_M03_attempt1_blocked_evidence_sha256": m03_attempt1[
            "artifact_sha256"
        ],
        "layer5a_M03_evidence_sha256": m03["artifact_sha256"],
        "layer5a_M04": "BLOCKED",
        "layer5a_M04_blocker_code": (
            "M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING"
        ),
        "layer5a_M04_evidence_sha256": m04["artifact_sha256"],
        "layer5b_execution_checkpoint_sha256": checkpoint["artifact_sha256"],
    })
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    layer5_path = HERE / "layer5_status.json"
    layer5 = json.loads(layer5_path.read_text(encoding="utf-8"))
    earned = list(layer5["earned_subgates"])
    subgate = "M03_PARENT_SCALAR_QUADRATIC_RESIDUES_PASS_ATTEMPT2"
    if subgate not in earned:
        earned.append(subgate)
    layer5.update({
        "earned_subgates": earned,
        "missing_required_residue_groups": 13,
        "blocker": "M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING",
        "layer5a_progress": "30/39",
        "canonical_progress": "M02_M03_PASS_M04_BLOCKED",
        "execution_checkpoint_sha256": checkpoint["artifact_sha256"],
    })
    layer5_path.write_text(json.dumps(layer5, indent=2) + "\n", encoding="utf-8")

    print("LAYER5B_M03_PASS_M04_BLOCKED_CHECKPOINT_FROZEN")
    print("PROGRESS 30/39")
    print("M03 PASS ATTEMPT2")
    print("FIRST_NON_PASS UVP_M04 BLOCKED")
    print("ARTIFACT_SHA256", checkpoint["artifact_sha256"])


if __name__ == "__main__":
    main()
