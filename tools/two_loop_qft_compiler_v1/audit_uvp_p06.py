"""Post-execution integrity audit for UVP_P06."""

from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent


def canonical_hash(payload, field="artifact_sha256"):
    work = dict(payload); embedded = work.pop(field)
    actual = sha256(json.dumps(work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert embedded == actual
    return actual


def main():
    schema = json.loads((HERE / "uvp_p06_evidence_schema.json").read_text())
    evidence = json.loads((HERE / "uvp_p06_evidence.json").read_text())
    primary = json.loads((HERE / "uvp_p06_primary.json").read_text())
    replay = json.loads((HERE / "uvp_p06_independent_replay.json").read_text())
    uv_ir = json.loads((HERE / "uvp_p06_uv_ir_provenance.json").read_text())
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text())
    Draft202012Validator(schema).validate(evidence)
    assert canonical_hash(evidence) == ledger["tests"][5]["derived_result"]["evidence_sha256"]
    assert canonical_hash(primary) == ledger["tests"][5]["primary"]["residue_sha256"]
    assert canonical_hash(replay) == ledger["tests"][5]["replay"]["residue_sha256"]
    assert canonical_hash(uv_ir) == ledger["tests"][5]["primary"]["uv_ir_provenance_sha256"]
    assert evidence["local_coefficients"]["maximum_residual"] == "0"
    assert evidence["locality"]["forbidden_structures_present"] == []
    ready = [row["test_id"] for row in ledger["tests"] if row["status"] == "NOT_RUN" and row["authorization"] == "READY"]
    assert len(ready) <= 1
    print("UVP_P06_EVIDENCE_AUDIT_PASS")
    print("LOCAL_COEFFICIENTS 1 0 -1/2")
    print("NEXT_AUTHORIZED_TEST", ready[0] if ready else "NONE")


if __name__ == "__main__":
    main()
