"""Audit the terminal M05 implementation blocker after M04 passes."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload); work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text())
    assert payload[field] == digest(payload, field)
    return payload


def main():
    evidence = load("uvp_m05_blocked_evidence.json")
    m04 = load("uvp_m04_evidence_attempt2.json")
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    assert m04["verdict"] == "PASS"
    assert evidence["verdict"] == "BLOCKED"
    assert evidence["comparison"]["physics_failure"] is False
    assert all(row["status"] == "PASS" for row in ledger["tests"][:30])
    assert ledger["tests"][29]["attempt"] == 2
    assert ledger["tests"][30]["status"] == "BLOCKED"
    assert ledger["counters"]["executed"] == 31
    assert ledger["counters"]["passed"] == 30
    assert ledger["counters"]["blocked"] == 1
    assert ledger["promotion"]["layer6_authorized"] is False
    print("UVP_M05_BLOCKED_EVIDENCE_AUDIT_PASS")
    print("PROGRESS 31/39 PASSED 30 BLOCKED 1 FAIL 0")
    print("M04 PASS ATTEMPT2; COUNTERTERM_COMPILER BLOCKED_AT_M05")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
