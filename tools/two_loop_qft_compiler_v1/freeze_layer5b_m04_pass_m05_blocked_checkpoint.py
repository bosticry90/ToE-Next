"""Freeze the authoritative Layer-5B 31/39 fail-fast checkpoint."""

from hashlib import sha256
import json
from pathlib import Path


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
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    engine = load("uv_pole_engine_gate_result.json")
    m02 = load("uvp_m02_evidence.json")
    m03a1 = load("uvp_m03_blocked_evidence.json")
    m03 = load("uvp_m03_evidence_attempt2.json")
    m04a1 = load("uvp_m04_blocked_evidence.json")
    m04 = load("uvp_m04_evidence_attempt2.json")
    m05 = load("uvp_m05_blocked_evidence.json")
    assert ledger["counters"] == {
        "total_required": 39, "executed": 31, "passed": 30,
        "blocked": 1, "failed": 0, "not_run_or_locked": 8,
        "engine_required": 27, "engine_executed": 27,
        "engine_passed": 27, "canonical_required": 12,
        "canonical_executed": 4, "canonical_passed": 3,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M04_PARENT_CUBIC_RESIDUES_PASS_ATTEMPT2_M05_IMPLEMENTATION_BLOCK",
        "progress": {"total": "31/39", "passed": 30, "blocked": 1,
                     "failed": 0, "engine": "27/27", "canonical": "3/12"},
        "hashes": {
            "contract_sha256": ledger["contract_sha256"],
            "execution_plan_sha256": ledger["execution_plan_sha256"],
            "ledger_sha256": ledger["result_sha256"],
            "engine_gate_artifact_sha256": engine["artifact_sha256"],
            "M02_evidence_sha256": m02["artifact_sha256"],
            "M03_attempt1_evidence_sha256": m03a1["artifact_sha256"],
            "M03_attempt2_evidence_sha256": m03["artifact_sha256"],
            "M04_attempt1_evidence_sha256": m04a1["artifact_sha256"],
            "M04_attempt2_evidence_sha256": m04["artifact_sha256"],
            "M05_evidence_sha256": m05["artifact_sha256"],
        },
        "earned": {
            "engine_gate": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
            "M02": "FOUR_PARENT_SCALAR_WAVEFUNCTION_RESIDUES_PASS",
            "M03": "FOUR_PARENT_QUADRATIC_RESIDUES_PASS_ATTEMPT2",
            "M04": "FOUR_REAL_PARENT_CUBIC_RESIDUES_PASS_ATTEMPT2",
            "M04_projection_rank": 4,
            "M04_projection_residual": "0",
            "M04_cubic_residues": m04["primary"]["cubic_residues"],
        },
        "first_non_pass": {
            "test_id": "UVP_M05", "verdict": "BLOCKED",
            "blocker_code": m05["comparison"]["blocker_code"],
            "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
            "physics_failure": False,
        },
        "preserved": {
            "counterterm_compiler": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
            "layer6_authorized": False,
            "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
            "bfb": "BFB_UNRESOLVED", "finite_C1_GS": None,
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "layer5b_m04_pass_m05_blocked_checkpoint.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("LAYER5B_M04_PASS_M05_BLOCKED_CHECKPOINT_FROZEN")
    print("PROGRESS 31/39 PASS 30 BLOCKED 1 FAIL 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
