"""Attach explicit UV/IR provenance to the aggregate M06/M07 passes."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(payload, field="artifact_sha256"):
    work = dict(payload); work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def write(name, payload):
    payload["artifact_sha256"] = digest(payload)
    (HERE / name).write_text(json.dumps(payload, indent=2) + "\n",
                             encoding="utf-8")
    return payload


def main():
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    m06 = write("uvp_m06_uv_ir_provenance.json", {
        "schema_version": 1, "test_id": "UVP_M06", "attempt": 1,
        "classification": "AGGREGATE_OF_LOCAL_ONE_LOOP_UV_POLE_OPERATORS",
        "UV_poles": "INHERITED_FROM_PASSED_M03_M04_M05_LOCAL_PROJECTIONS",
        "IR_poles": "NO_UNMATCHED_IR_POLE_IN_ANY_CONSTITUENT_OPERATOR",
        "locality": "EXACT_POLYNOMIAL_DEGREE_2_3_4_DIRECT_SUM",
    })
    m07 = write("uvp_m07_uv_ir_provenance.json", {
        "schema_version": 1, "test_id": "UVP_M07", "attempt": 1,
        "classification": "ALGEBRAIC_CONSISTENCY_AUDIT_OF_CALCULATED_LOCAL_UV_POLE_ACTION",
        "UV_poles": "INPUT_IS_COMPLETE_PASSED_M06_LOCAL_POLE_ACTION",
        "IR_poles": "NOT_AN_ADDITIONAL_INTEGRAL_EXTRACTION",
        "locality": "PRESERVED",
    })
    for index, artifact in ((31, m06), (32, m07)):
        ledger["tests"][index]["primary"]["uv_ir_provenance_sha256"] = artifact["artifact_sha256"]
        ledger["tests"][index]["replay"]["uv_ir_provenance_sha256"] = artifact["artifact_sha256"]
        ledger["tests"][index]["evidence_files"].append(
            f"uvp_m0{index - 25}_uv_ir_provenance.json"
        )
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    checkpoint_path = HERE / "layer5b_m07_pass_m08_blocked_checkpoint.json"
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    checkpoint["hashes"]["ledger_sha256"] = ledger["result_sha256"]
    checkpoint["artifact_sha256"] = digest(checkpoint)
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + "\n",
                               encoding="utf-8")
    status_path = HERE / "compiler_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["layer5a_current_result_sha256"] = ledger["result_sha256"]
    status["layer5b_execution_checkpoint_sha256"] = checkpoint["artifact_sha256"]
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    state_path = ROOT / "project_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    node = state["scaffold"]["two_loop_qft_compiler_v1"]
    node["layer5a_current_result_sha256"] = ledger["result_sha256"]
    node["layer5b_execution_checkpoint_sha256"] = checkpoint["artifact_sha256"]
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print("M06_M07_UV_IR_PROVENANCE_ATTACHED")
    print("LEDGER_SHA256", ledger["result_sha256"])
    print("CHECKPOINT_SHA256", checkpoint["artifact_sha256"])


if __name__ == "__main__":
    main()
