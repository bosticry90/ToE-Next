"""Audit the terminal UVP_M03 attempt-2 pass and preserved attempt 1."""

from hashlib import sha256
import json
from pathlib import Path


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
    evidence = load("uvp_m03_evidence_attempt2.json")
    attempt1 = load("uvp_m03_blocked_evidence.json")
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    assert attempt1["verdict"] == "BLOCKED"
    assert evidence["verdict"] == "PASS" and evidence["attempt"] == 2
    assert evidence["comparison"] == {
        "quadratic_residue_residual": "0",
        "quartic_trace_table_residual": "0",
        "cubic_trace_table_residual": "0",
        "full_operator_projection_residual": "0",
        "rank": 4,
    }
    row = ledger["tests"][28]
    assert row["status"] == "PASS" and row["attempt"] == 2
    assert row["derived_result"]["attempt1_blocked_evidence_sha256"] == (
        attempt1["artifact_sha256"]
    )
    successor = ledger["tests"][29]
    assert successor["test_id"] == "UVP_M04"
    if successor["status"] == "NOT_RUN":
        assert successor["authorization"] == "READY"
        assert ledger["counters"]["executed"] == 29
        assert ledger["counters"]["passed"] == 29
        assert ledger["counters"]["blocked"] == 0
    else:
        # A later fail-fast successor may be terminal without weakening or
        # reopening the already-earned M03 authority.
        assert successor["status"] in {"BLOCKED", "FAIL"}
        assert successor["authorization"] == "TERMINAL"
        assert ledger["counters"]["executed"] == 30
        assert ledger["counters"]["passed"] == 29
    assert ledger["promotion"] == {"engine_gate": "PASS",
                                    "counterterm_compiler": "BLOCKED",
                                    "layer6_authorized": False}
    print("UVP_M03_ATTEMPT2_EVIDENCE_AUDIT_PASS")
    print("PROGRESS", f"{ledger['counters']['executed']}/39",
          "PASS", ledger["counters"]["passed"],
          "BLOCKED", ledger["counters"]["blocked"],
          "FAIL", ledger["counters"]["failed"])
    print("M03_AUTHORITY PRESERVED; SUCCESSOR", successor["status"])
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
