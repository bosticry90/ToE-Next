"""Audit the authoritative 34/39 M07-pass/M08-blocked checkpoint."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(payload, field="artifact_sha256"):
    work = dict(payload); work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field), name
    return payload


def main():
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    m05 = load("uvp_m05_evidence_attempt2.json")
    m06 = load("uvp_m06_evidence.json")
    m07 = load("uvp_m07_evidence.json")
    m08 = load("uvp_m08_blocked_evidence.json")
    checkpoint = load("layer5b_m07_pass_m08_blocked_checkpoint.json")
    assert ledger["counters"] == {
        "total_required": 39, "executed": 34, "passed": 33,
        "blocked": 1, "failed": 0, "not_run_or_locked": 5,
        "engine_required": 27, "engine_executed": 27,
        "engine_passed": 27, "canonical_required": 12,
        "canonical_executed": 7, "canonical_passed": 6,
    }
    assert ledger["overall_status"] == "CANONICAL_BLOCKED"
    assert ledger["promotion"] == {
        "engine_gate": "PASS", "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }
    expected = {30: ("UVP_M05", "PASS", 2),
                31: ("UVP_M06", "PASS", 1),
                32: ("UVP_M07", "PASS", 1),
                33: ("UVP_M08", "BLOCKED", 1)}
    for index, values in expected.items():
        test = ledger["tests"][index]
        assert (test["test_id"], test["status"], test["attempt"]) == values
    for test in ledger["tests"][34:]:
        assert test["status"] == "NOT_RUN"
        assert test["authorization"] == "WAITING_PREDECESSOR"
        assert test["attempt"] == 0
    assert m05["checks"]["projection_rank"] == 26
    assert set(m05["independent_replay"].keys()) >= {
        "uncompared_scalar_sha256", "scalar_comparison_sha256",
        "gauge_comparison_sha256",
    }
    assert m06["projection_rank"] == 34
    assert m06["out_of_basis_residual"] == "0"
    assert m07["Hermiticity_residual"] == "0"
    assert m07["PQ_forbidden_operator_residual"] == "0"
    assert m08["comparison"]["residues_derived"] is False
    assert checkpoint["hashes"]["ledger_sha256"] == ledger["result_sha256"]
    assert checkpoint["first_non_pass"]["test_id"] == "UVP_M08"
    status = json.loads((HERE / "compiler_status.json").read_text())
    assert status["layer5a_execution_progress"] == "34_OF_39_ENGINE_27_OF_27"
    assert status["layer5a_M05"].startswith("PASS_ATTEMPT2")
    assert status["layer5a_M06"].startswith("PASS_RANK34")
    assert status["layer5a_M07"].startswith("PASS_HERMITICITY")
    assert status["layer5a_M08"] == "BLOCKED"
    assert status["layer6_tensor_IBP_reduction_authorized"] is False
    state = json.loads((ROOT / "project_state.json").read_text())
    node = state["scaffold"]["two_loop_qft_compiler_v1"]
    assert node["layer5a_current_result_sha256"] == ledger["result_sha256"]
    assert node["layer5a_M08"] == "BLOCKED"
    assert node["layer6_tensor_IBP_reduction_authorized"] is False
    assert node["finite_C1_GS"] is None
    assert node["bfb_status"] == "BFB_UNRESOLVED"
    print("LAYER5B_M07_PASS_M08_BLOCKED_CHECKPOINT_AUDIT_PASS")
    print("PROGRESS 34/39 PASS 33 BLOCKED 1 FAIL 0")
    print("LEDGER_SHA256", ledger["result_sha256"])
    print("CHECKPOINT_SHA256", checkpoint["artifact_sha256"])


if __name__ == "__main__":
    main()
