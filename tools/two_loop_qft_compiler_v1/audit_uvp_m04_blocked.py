"""Audit the terminal M04 blocker after a passed M03 retry."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload)
    work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text())
    assert payload[field] == digest(payload, field)
    return payload


def main():
    evidence = load("uvp_m04_blocked_evidence.json")
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    assert evidence["verdict"] == "BLOCKED"
    assert evidence["comparison"]["physics_failure"] is False
    assert all(row["status"] == "PASS" for row in ledger["tests"][:29])
    assert ledger["tests"][29]["status"] == "BLOCKED"
    assert ledger["tests"][28]["attempt"] == 2
    assert ledger["counters"]["executed"] == 30
    assert ledger["counters"]["passed"] == 29
    assert ledger["counters"]["blocked"] == 1
    assert ledger["promotion"]["layer6_authorized"] is False
    print("UVP_M04_BLOCKED_EVIDENCE_AUDIT_PASS")
    print("PROGRESS 30/39 PASSED 29 BLOCKED 1")
    print("COUNTERTERM_COMPILER BLOCKED")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
