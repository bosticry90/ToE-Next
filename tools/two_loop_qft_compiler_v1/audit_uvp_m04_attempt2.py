"""Audit the terminal UVP_M04 attempt-2 pass and attempt history."""

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
    evidence = load("uvp_m04_evidence_attempt2.json")
    attempt1 = load("uvp_m04_blocked_evidence.json")
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    assert attempt1["verdict"] == "BLOCKED"
    assert evidence["verdict"] == "PASS" and evidence["attempt"] == 2
    assert evidence["comparison"]["rank"] == 4
    assert all(value in ("0", 0) for key, value in evidence["comparison"].items()
               if key != "rank")
    row = ledger["tests"][29]
    assert row["status"] == "PASS" and row["attempt"] == 2
    assert row["derived_result"]["attempt1_blocked_evidence_sha256"] == (
        attempt1["artifact_sha256"]
    )
    successor = ledger["tests"][30]
    assert successor["test_id"] == "UVP_M05"
    assert successor["authorization"] == "READY"
    assert ledger["counters"]["executed"] == 30
    assert ledger["counters"]["passed"] == 30
    assert ledger["counters"]["blocked"] == 0
    assert ledger["promotion"] == {"engine_gate": "PASS",
                                    "counterterm_compiler": "BLOCKED",
                                    "layer6_authorized": False}
    print("UVP_M04_ATTEMPT2_EVIDENCE_AUDIT_PASS")
    print("PROGRESS 30/39 PASS 30 BLOCKED 0 FAIL 0")
    print("NEXT_TEST UVP_M05 READY")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
