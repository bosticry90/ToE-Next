"""Audit the layer-5A preregistration without executing an evaluator."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    spec = json.loads((HERE / "one_loop_uv_pole_evaluator_contract.json").read_text(
        encoding="utf-8"))
    status = json.loads((HERE / "compiler_status.json").read_text(
        encoding="utf-8"))
    assert spec["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT_PREREGISTERED"
    assert spec["authority"] == "TEST_SPECIFICATION_ONLY_NO_UV_POLE_RESULT"
    assert spec["counts"] == {
        "primitive_tests": 12,
        "control_theory_tests": 13,
        "canonical_model_tests": 13,
        "total_required_tests": 38,
    }
    ids = [row["test_id"] for group in (
        spec["primitive_tests"], spec["minimum_control_theories"],
        spec["canonical_model_tests"])
        for row in group]
    assert len(ids) == len(set(ids)) == 38
    assert spec["UV_IR_separation_contract"]["scaleless_integrals"] == (
        "must_store_UV_and_IR_labels_separately_not_accept_bare_zero")
    assert spec["independent_replay"]["required"] is True
    assert spec["promotion_policy"]["layer6_authorized_only_after"] == (
        "ONE_LOOP_COUNTERTERM_COMPILER_PASS")
    assert status["outcome"] == "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED"
    assert status["layer6_tensor_IBP_reduction_authorized"] is False

    status.update({
        "layer5a_uv_pole_evaluator_contract": (
            "PREREGISTERED_12_PRIMITIVE_13_CONTROL_13_CANONICAL_TESTS"),
        "layer5a_uv_pole_evaluator_contract_sha256": spec[
            "uv_pole_evaluator_contract_sha256"],
        "layer5a_uv_ir_separation": (
            "AUXILIARY_MASS_PLUS_LOCAL_IR_COUNTERTERMS_WITH_OFFSHELL_REPLAY"),
        "layer5a_independent_replay_required": True,
        "layer5a_evaluator_implemented": False,
        "layer5a_tests_required": 38,
        "layer5a_tests_executed": 0,
        "next_gate": "EXECUTE_ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT",
    })
    (HERE / "compiler_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8")
    result = {
        "outcome": "ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT_PREREGISTERED",
        "contract_sha256": spec["uv_pole_evaluator_contract_sha256"],
        "required_tests": 38,
        "tests_executed": 0,
        "compiler_outcome_preserved": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
        "layer6_authorized": False,
        "authority": "SPECIFICATION_ONLY",
    }
    (HERE / "uv_pole_evaluator_contract_status.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["outcome"])
    print("REQUIRED_TESTS", 38)
    print("TESTS_EXECUTED", 0)
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
