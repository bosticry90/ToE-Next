"""Post-execution integrity audit for UVP_P04."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import sympy as sp


HERE = Path(__file__).resolve().parent


def canonical_hash(payload, field="artifact_sha256"):
    work = dict(payload)
    embedded = work.pop(field)
    actual = sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert embedded == actual
    return actual


def main():
    schema = json.loads((HERE / "uvp_p04_evidence_schema.json").read_text(
        encoding="utf-8"))
    evidence = json.loads((HERE / "uvp_p04_evidence.json").read_text(
        encoding="utf-8"))
    primary = json.loads((HERE / "uvp_p04_primary.json").read_text(
        encoding="utf-8"))
    replay = json.loads((HERE / "uvp_p04_independent_replay.json").read_text(
        encoding="utf-8"))
    uv_ir = json.loads((HERE / "uvp_p04_uv_ir_provenance.json").read_text(
        encoding="utf-8"))
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text(
        encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(evidence)
    evidence_hash = canonical_hash(evidence)
    assert canonical_hash(primary) == evidence["primary"]["artifact_sha256"]
    assert canonical_hash(replay) == evidence[
        "independent_replay"]["artifact_sha256"]
    uv_ir_hash = canonical_hash(uv_ir)
    assert sp.simplify(
        sp.sympify(primary["normalized_tensor_residue_coefficient"])
        - sp.sympify(replay["normalized_tensor_residue_coefficient"])) == 0
    assert primary["contraction_residual"] == replay["contraction_residual"] == "0"
    assert primary["adversarial_premature_d4"]["used_by_promoted_route"] is False

    row = ledger["tests"][3]
    assert row["test_id"] == "UVP_P04" and row["status"] == "PASS"
    assert row["derived_result"]["evidence_sha256"] == evidence_hash
    assert row["primary"]["residue_sha256"] == primary["artifact_sha256"]
    assert row["replay"]["residue_sha256"] == replay["artifact_sha256"]
    assert row["primary"]["uv_ir_provenance_sha256"] == uv_ir_hash
    assert row["replay"]["uv_ir_provenance_sha256"] == uv_ir_hash
    ready = [candidate["test_id"] for candidate in ledger["tests"]
             if candidate["status"] == "NOT_RUN"
             and candidate["authorization"] == "READY"]
    assert len(ready) <= 1

    print("UVP_P04_EVIDENCE_AUDIT_PASS")
    print("TENSOR_RESIDUE_COEFFICIENT", primary[
        "normalized_tensor_residue_coefficient"])
    print("CONTRACTION_RESIDUAL 0")
    print("NEXT_AUTHORIZED_TEST", ready[0] if ready else "NONE")


if __name__ == "__main__":
    main()
