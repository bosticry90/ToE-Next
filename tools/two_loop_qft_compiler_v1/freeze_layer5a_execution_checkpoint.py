"""Freeze the authoritative Layer-5A 29/39 fail-fast checkpoint."""

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
    m03 = load_verified("uvp_m03_blocked_evidence.json")

    assert ledger["overall_status"] == "CANONICAL_BLOCKED"
    assert ledger["counters"] == {
        "total_required": 39,
        "executed": 29,
        "passed": 28,
        "blocked": 1,
        "failed": 0,
        "not_run_or_locked": 10,
        "engine_required": 27,
        "engine_executed": 27,
        "engine_passed": 27,
        "canonical_required": 12,
        "canonical_executed": 2,
        "canonical_passed": 1,
    }
    assert ledger["promotion"] == {
        "engine_gate": "PASS",
        "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }
    assert engine["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert m02["verdict"] == "PASS"
    assert m03["verdict"] == "BLOCKED"
    assert m03["comparison"]["physics_failure"] is False
    assert all(row["status"] == "PASS" for row in ledger["tests"][:28])
    assert ledger["tests"][28]["test_id"] == "UVP_M03"
    assert ledger["tests"][28]["status"] == "BLOCKED"
    assert all(row["status"] == "NOT_RUN" for row in ledger["tests"][29:])

    checkpoint = {
        "schema_version": 1,
        "outcome": "CANONICAL_BLOCKED",
        "first_test_executed_in_pass": "UVP_P06",
        "last_test_reached": "UVP_M03",
        "progress": {
            "total": "29/39",
            "passed": 28,
            "blocked": 1,
            "failed": 0,
            "engine": "27/27",
            "canonical": "2/12 executed; 1 PASS; 1 BLOCKED",
        },
        "earned": {
            "uv_pole_evaluator": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
            "counterterm_compiler": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
            "M02_parent_scalar_wavefunction_residues": "PASS",
        },
        "first_non_pass": {
            "test_id": "UVP_M03",
            "verdict": "BLOCKED",
            "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
            "blocker_code": (
                "M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING"
            ),
            "missing_capabilities": m03["primary"]["inventory"][
                "missing_capabilities"
            ],
            "evidence_sha256": m03["artifact_sha256"],
        },
        "hashes": {
            "contract_sha256": ledger["contract_sha256"],
            "execution_plan_sha256": ledger["execution_plan_sha256"],
            "ledger_sha256": ledger["result_sha256"],
            "engine_gate_artifact_sha256": engine["artifact_sha256"],
            "M02_evidence_sha256": m02["artifact_sha256"],
            "M03_evidence_sha256": m03["artifact_sha256"],
        },
        "preserved_dispositions": ledger["preserved_dispositions"],
        "layer6_authorized": False,
    }
    checkpoint["artifact_sha256"] = digest(checkpoint)
    (HERE / "layer5a_execution_checkpoint.json").write_text(
        json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8"
    )

    status_path = HERE / "compiler_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status.update({
        "next_gate": "IMPLEMENT_M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL",
        "layer5_parent_operator_radiative_pole_closure": (
            "BLOCKED_AT_M03_PARENT_QUADRATIC_POLE_EXTRACTION"
        ),
        "layer5_missing_required_residues": [
            item for item in status["layer5_missing_required_residues"]
            if item not in {"deltaZ_Phi", "deltaZ_Sigma", "deltaZ_phi", "deltaZ_S"}
        ],
        "layer5_blocker": (
            "M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING"
        ),
        "layer5a_evaluator_implemented": True,
        "layer5a_evaluator_implementation": (
            "P01_P13_C01_C13_M01_PRIMARY_AND_INDEPENDENT_REPLAY_PASS"
        ),
        "layer5a_engine_gate": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
        "layer5a_engine_gate_artifact_sha256": engine["artifact_sha256"],
        "layer5a_M02": "PASS_FOUR_PARENT_SCALAR_FIELD_RESIDUES",
        "layer5a_M02_evidence_sha256": m02["artifact_sha256"],
        "layer5a_M03": "BLOCKED",
        "layer5a_M03_blocker_code": (
            "M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING"
        ),
        "layer5a_M03_evidence_sha256": m03["artifact_sha256"],
        "layer5a_execution_checkpoint_sha256": checkpoint["artifact_sha256"],
    })
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    layer5_path = HERE / "layer5_status.json"
    layer5 = json.loads(layer5_path.read_text(encoding="utf-8"))
    earned = list(layer5["earned_subgates"])
    for subgate in (
        "ONE_LOOP_UV_POLE_EVALUATOR_PASS_27_OF_27",
        "M02_PARENT_SCALAR_WAVEFUNCTION_RESIDUES_PASS",
    ):
        if subgate not in earned:
            earned.append(subgate)
    layer5.update({
        "earned_subgates": earned,
        "missing_required_residue_groups": 14,
        "blocker": "M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING",
        "layer5a_progress": "29/39",
        "engine_gate": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
        "canonical_progress": "M02_PASS_M03_BLOCKED",
        "execution_checkpoint_sha256": checkpoint["artifact_sha256"],
    })
    layer5_path.write_text(json.dumps(layer5, indent=2) + "\n", encoding="utf-8")

    print("LAYER5A_EXECUTION_CHECKPOINT_FROZEN")
    print("PROGRESS 29/39")
    print("ENGINE_GATE ONE_LOOP_UV_POLE_EVALUATOR_PASS")
    print("FIRST_NON_PASS UVP_M03 BLOCKED")
    print("ARTIFACT_SHA256", checkpoint["artifact_sha256"])


if __name__ == "__main__":
    main()
