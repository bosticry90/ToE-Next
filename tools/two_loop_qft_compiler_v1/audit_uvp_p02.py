"""Post-execution integrity audit for UVP_P02."""

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
    schema = json.loads((HERE / "uvp_p02_evidence_schema.json").read_text(
        encoding="utf-8"))
    evidence = json.loads((HERE / "uvp_p02_evidence.json").read_text(
        encoding="utf-8"))
    primary = json.loads((HERE / "uvp_p02_primary.json").read_text(
        encoding="utf-8"))
    replay = json.loads((HERE / "uvp_p02_independent_replay.json").read_text(
        encoding="utf-8"))
    uv_ir = json.loads((HERE / "uvp_p02_uv_ir_provenance.json").read_text(
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
    assert evidence["primary"] == primary
    assert evidence["independent_replay"] == replay
    assert sp.simplify(sp.sympify(primary["normalized_residue"])
                       - sp.sympify(replay["normalized_residue"])) == 0
    assert sp.diff(sp.sympify(primary["normalized_residue"]),
                   sp.Symbol("m2")) == 0
    assert primary["pole_expression"] == replay["pole_expression"]
    assert primary["uv_ir"] == replay["uv_ir"]

    row = ledger["tests"][1]
    assert row["test_id"] == "UVP_P02" and row["status"] == "PASS"
    assert row["derived_result"]["evidence_sha256"] == evidence_hash
    assert row["primary"]["residue_sha256"] == primary["artifact_sha256"]
    assert row["replay"]["residue_sha256"] == replay["artifact_sha256"]
    assert row["primary"]["uv_ir_provenance_sha256"] == uv_ir_hash
    assert row["replay"]["uv_ir_provenance_sha256"] == uv_ir_hash
    assert ledger["tests"][2]["authorization"] == "READY"

    print("UVP_P02_EVIDENCE_AUDIT_PASS")
    print("NORMALIZED_RESIDUE", primary["normalized_residue"])
    print("MASS_DERIVATIVE 0")
    print("PRIMARY_MINUS_REPLAY 0")
    print("NEXT_TEST UVP_P03")


if __name__ == "__main__":
    main()
