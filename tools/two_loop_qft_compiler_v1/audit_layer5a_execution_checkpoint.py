"""Final-state audit for the frozen 29/39 Layer-5A checkpoint."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(payload, field):
    work = dict(payload)
    embedded = work.pop(field)
    packed = json.dumps(work, sort_keys=True, separators=(",", ":"))
    return embedded, sha256(packed.encode()).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def verify_artifact(name, field="artifact_sha256"):
    payload = load(name)
    assert digest(payload, field)[0] == digest(payload, field)[1]
    return payload


def main():
    ledger = load("uv_pole_evaluator_results.json")
    schema = load("uv_pole_evaluator_result_schema.json")
    assert digest(ledger, "result_sha256")[0] == digest(
        ledger, "result_sha256"
    )[1]
    Draft202012Validator(schema).validate(ledger)

    assert ledger["counters"] == {
        "total_required": 39,
        "executed": 29,
        "passed": 28,
        "blocked": 1,
        "failed": 0,
        "not_run_or_locked": 10,
        "engine_required": 27,
        "engine_executed": 27,
        "engine_passed": 27,
        "canonical_required": 12,
        "canonical_executed": 2,
        "canonical_passed": 1,
    }
    assert ledger["promotion"] == {
        "engine_gate": "PASS",
        "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }
    assert all(row["status"] == "PASS" for row in ledger["tests"][:28])
    assert ledger["tests"][28]["status"] == "BLOCKED"
    assert all(row["status"] == "NOT_RUN" for row in ledger["tests"][29:])

    for row in ledger["tests"][:29]:
        for evidence_file in row["evidence_files"]:
            if evidence_file.endswith(".json"):
                verify_artifact(evidence_file)

    engine = verify_artifact("uv_pole_engine_gate_result.json")
    checkpoint = verify_artifact("layer5a_execution_checkpoint.json")
    m02 = verify_artifact("uvp_m02_evidence.json")
    m03 = verify_artifact("uvp_m03_blocked_evidence.json")
    assert engine["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert engine["tests_passed"] == "27/27"
    assert checkpoint["hashes"]["ledger_sha256"] == ledger["result_sha256"]
    assert checkpoint["hashes"]["engine_gate_artifact_sha256"] == engine[
        "artifact_sha256"
    ]
    assert checkpoint["hashes"]["M02_evidence_sha256"] == m02[
        "artifact_sha256"
    ]
    assert checkpoint["hashes"]["M03_evidence_sha256"] == m03[
        "artifact_sha256"
    ]
    assert checkpoint["first_non_pass"]["classification"] == (
        "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL"
    )

    compiler = load("compiler_status.json")
    layer5 = load("layer5_status.json")
    assert compiler["layer5a_engine_gate"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert compiler["layer5a_M02"] == "PASS_FOUR_PARENT_SCALAR_FIELD_RESIDUES"
    assert compiler["layer5a_M03"] == "BLOCKED"
    assert compiler["layer5a_execution_checkpoint_sha256"] == checkpoint[
        "artifact_sha256"
    ]
    assert compiler["layer6_tensor_IBP_reduction_authorized"] is False
    assert layer5["outcome"] == "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED"
    assert layer5["engine_gate"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert layer5["layer5a_progress"] == "29/39"
    assert layer5["missing_required_residue_groups"] == 14
    assert layer5["layer6_authorized"] is False

    project = json.loads((ROOT / "project_state.json").read_text(encoding="utf-8"))
    compiler_project = project["scaffold"]["two_loop_qft_compiler_v1"]
    assert compiler_project["layer5a_tests_executed"] == 29
    assert compiler_project["layer5a_engine_tests_executed"] == 27
    assert compiler_project["layer5a_M03"] == "BLOCKED"
    assert compiler_project["layer6_tensor_IBP_reduction_authorized"] is False
    assert compiler_project["finite_C1_GS"] is None
    assert ledger["preserved_dispositions"] == {
        "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
        "bfb": "BFB_UNRESOLVED",
        "finite_C1_GS": None,
    }

    print("LAYER5A_EXECUTION_CHECKPOINT_AUDIT_PASS")
    print("PROGRESS 29/39 PASS 28 BLOCKED 1 FAIL 0")
    print("ENGINE_GATE ONE_LOOP_UV_POLE_EVALUATOR_PASS 27/27")
    print("COUNTERTERM_COMPILER BLOCKED_AT_M03")
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
