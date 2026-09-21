"""Audit the layer-5A preregistration without executing an evaluator."""

import json
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    spec = json.loads((HERE / "one_loop_uv_pole_evaluator_contract.json").read_text(
        encoding="utf-8"))
    status = json.loads((HERE / "compiler_status.json").read_text(
        encoding="utf-8"))
    assert spec["outcome"] == "ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT_PREREGISTERED"
    assert spec["authority"] == "TEST_SPECIFICATION_ONLY_NO_UV_POLE_RESULT"
    embedded_hash = spec.pop("uv_pole_evaluator_contract_sha256")
    canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    recomputed_hash = sha256(canonical.encode()).hexdigest()
    spec["uv_pole_evaluator_contract_sha256"] = embedded_hash
    assert embedded_hash == recomputed_hash
    assert spec["schema_version"] == 2
    assert spec["revision"]["supersedes_contract_sha256"] == (
        "f4cf741afed95657b8c8c80ff178147189f35c7db42a8fdcea95e8ed3ae3f588")
    assert spec["counts"] == {
        "primitive_tests": 13,
        "control_theory_tests": 13,
        "canonical_model_tests": 13,
        "total_required_tests": 39,
    }
    ids = [row["test_id"] for group in (
        spec["primitive_tests"], spec["minimum_control_theories"],
        spec["canonical_model_tests"])
        for row in group]
    assert len(ids) == len(set(ids)) == 39
    assert any(row["test_id"] == "UVP_P13"
               and row["target"] == "rank8_tensor_vacuum_integral"
               and "105_pairing" in row["requirement"]
               for row in spec["primitive_tests"])
    assert any(row["test_id"] == "UVP_M13"
               and "independent_diagram_inventory" in row["requirement"]
               for row in spec["canonical_model_tests"])
    assert spec["UV_IR_separation_contract"]["scaleless_integrals"] == (
        "must_store_UV_and_IR_labels_separately_not_accept_bare_zero")
    assert spec["independent_replay"]["required"] is True
    assert spec["independent_replay"][
        "primary_diagram_inventory_may_not_be_imported"] is True
    assert spec["independent_replay"][
        "same_incomplete_graph_list_evaluated_twice"] == (
            "NOT_AN_INDEPENDENT_REPLAY")
    assert spec["fail_fast_partition"]["phase_5A_engine"]["count"] == 27
    assert spec["fail_fast_partition"][
        "phase_5B_canonical_counterterms"]["count"] == 12
    assert spec["promotion_policy"]["layer6_authorized_only_after"] == (
        "ONE_LOOP_COUNTERTERM_COMPILER_PASS")
    assert status["outcome"] == "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED"
    assert status["layer6_tensor_IBP_reduction_authorized"] is False

    status.update({
        "layer5a_uv_pole_evaluator_contract": (
            "PREREGISTERED_V2_13_PRIMITIVE_13_CONTROL_13_CANONICAL_TESTS"),
        "layer5a_uv_pole_evaluator_contract_sha256": spec[
            "uv_pole_evaluator_contract_sha256"],
        "layer5a_uv_ir_separation": (
            "AUXILIARY_MASS_PLUS_LOCAL_IR_COUNTERTERMS_WITH_OFFSHELL_REPLAY"),
        "layer5a_independent_replay_required": True,
        "layer5a_independent_diagram_completeness_required": True,
        "layer5a_rank8_primitive_required": True,
        "layer5a_fail_fast_partition": (
            "27_EVALUATOR_ENGINE_PLUS_12_CANONICAL_COUNTERTERM_TESTS"),
        "layer5a_uv_pole_evaluator_contract_supersedes_sha256": spec[
            "revision"]["supersedes_contract_sha256"],
        "layer5a_evaluator_implemented": False,
        "layer5a_tests_required": 39,
        "layer5a_tests_executed": 0,
        "next_gate": "EXECUTE_ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT",
    })
    (HERE / "compiler_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8")
    result = {
        "outcome": "ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT_PREREGISTERED",
        "contract_sha256": spec["uv_pole_evaluator_contract_sha256"],
        "required_tests": 39,
        "tests_executed": 0,
        "compiler_outcome_preserved": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
        "layer6_authorized": False,
        "authority": "SPECIFICATION_ONLY",
    }
    (HERE / "uv_pole_evaluator_contract_status.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["outcome"])
    print("REQUIRED_TESTS", 39)
    print("TESTS_EXECUTED", 0)
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
