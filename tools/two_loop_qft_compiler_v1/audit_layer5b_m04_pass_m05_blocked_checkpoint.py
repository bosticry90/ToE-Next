"""Final-state audit for the frozen 31/39 Layer-5B checkpoint."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(payload, field):
    work = dict(payload); embedded = work.pop(field)
    calculated = sha256(json.dumps(work, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()
    return embedded, calculated


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(name, field="artifact_sha256"):
    payload = load(HERE / name)
    assert digest(payload, field)[0] == digest(payload, field)[1]
    return payload


def main():
    ledger = verify("uv_pole_evaluator_results.json", "result_sha256")
    schema = load(HERE / "uv_pole_evaluator_result_schema.json")
    Draft202012Validator(schema).validate(ledger)
    assert ledger["counters"] == {
        "total_required": 39, "executed": 31, "passed": 30,
        "blocked": 1, "failed": 0, "not_run_or_locked": 8,
        "engine_required": 27, "engine_executed": 27,
        "engine_passed": 27, "canonical_required": 12,
        "canonical_executed": 4, "canonical_passed": 3,
    }
    assert all(row["status"] == "PASS" for row in ledger["tests"][:30])
    assert ledger["tests"][29]["test_id"] == "UVP_M04"
    assert ledger["tests"][29]["attempt"] == 2
    assert ledger["tests"][30]["test_id"] == "UVP_M05"
    assert ledger["tests"][30]["status"] == "BLOCKED"
    assert all(row["status"] == "NOT_RUN" for row in ledger["tests"][31:])
    for row in ledger["tests"][:31]:
        for evidence_file in row["evidence_files"]:
            if evidence_file.endswith(".json"):
                verify(evidence_file)

    engine = verify("uv_pole_engine_gate_result.json")
    m04a1 = verify("uvp_m04_blocked_evidence.json")
    m04 = verify("uvp_m04_evidence_attempt2.json")
    m05 = verify("uvp_m05_blocked_evidence.json")
    checkpoint = verify("layer5b_m04_pass_m05_blocked_checkpoint.json")
    assert engine["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    assert m04a1["verdict"] == "BLOCKED"
    assert m04["verdict"] == "PASS" and m04["comparison"]["rank"] == 4
    assert m04["comparison"]["full_operator_projection_residual"] == "0"
    assert m05["verdict"] == "BLOCKED"
    assert m05["comparison"]["physics_failure"] is False
    assert checkpoint["hashes"]["ledger_sha256"] == ledger["result_sha256"]
    assert checkpoint["hashes"]["M04_attempt2_evidence_sha256"] == m04[
        "artifact_sha256"
    ]
    assert checkpoint["hashes"]["M05_evidence_sha256"] == m05[
        "artifact_sha256"
    ]

    compiler = load(HERE / "compiler_status.json")
    layer5 = load(HERE / "layer5_status.json")
    contract_status = load(HERE / "uv_pole_evaluator_contract_status.json")
    execution_status = load(HERE / "uv_pole_evaluator_execution_status.json")
    assert compiler["layer5a_tests_executed"] == 31
    assert compiler["layer5a_evaluator_implementation"] == (
        "P01_P13_C01_C13_M01_PRIMARY_AND_INDEPENDENT_REPLAY_PASS"
    )
    assert compiler["next_gate"] == (
        "IMPLEMENT_M05_EXHAUSTIVE_PARENT_SCALAR_4PT_CONTRACTION_PROJECTOR"
    )
    assert compiler["layer5a_M04"] == "PASS_ATTEMPT2_FOUR_REAL_PARENT_CUBIC_RESIDUES"
    assert compiler["layer5a_M05"] == "BLOCKED"
    assert compiler["layer5b_execution_checkpoint_sha256"] == checkpoint[
        "artifact_sha256"
    ]
    assert compiler["layer6_tensor_IBP_reduction_authorized"] is False
    assert layer5["layer5a_progress"] == "31/39"
    assert layer5["canonical_progress"] == "M02_M03_M04_PASS_M05_BLOCKED"
    assert layer5["missing_required_residue_groups"] == 12
    assert layer5["layer6_authorized"] is False
    assert contract_status["tests_executed"] == 31
    assert execution_status["current_result_sha256"] == ledger["result_sha256"]
    assert execution_status["total_progress"] == "31/39"

    project = load(ROOT / "project_state.json")
    scaffold = project["scaffold"]["two_loop_qft_compiler_v1"]
    assert scaffold["layer5a_tests_executed"] == 31
    assert scaffold["layer5a_M04"] == (
        "PASS_ATTEMPT2_FOUR_REAL_PARENT_CUBIC_RESIDUES"
    )
    assert scaffold["layer5a_M05"] == "BLOCKED"
    assert scaffold["layer5b_execution_checkpoint_sha256"] == checkpoint[
        "artifact_sha256"
    ]
    assert scaffold["layer6_tensor_IBP_reduction_authorized"] is False
    assert scaffold["finite_C1_GS"] is None
    assert ledger["preserved_dispositions"] == {
        "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
        "bfb": "BFB_UNRESOLVED", "finite_C1_GS": None,
    }

    print("LAYER5B_M04_PASS_M05_BLOCKED_CHECKPOINT_AUDIT_PASS")
    print("PROGRESS 31/39 PASS 30 BLOCKED 1 FAIL 0")
    print("ENGINE_GATE ONE_LOOP_UV_POLE_EVALUATOR_PASS 27/27")
    print("M04 PASS ATTEMPT2; COUNTERTERM_COMPILER BLOCKED_AT_M05")
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
