"""Audit the frozen Layer-5A order and any valid 0/39-to-39/39 ledger."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
EXPECTED_CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"


def recompute(payload, field):
    work = dict(payload)
    embedded = work.pop(field)
    packed = json.dumps(work, sort_keys=True, separators=(",", ":"))
    return embedded, sha256(packed.encode()).hexdigest()


def main():
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    plan = json.loads((HERE / "uv_pole_evaluator_execution_plan.json").read_text(
        encoding="utf-8"))
    result = json.loads((HERE / "uv_pole_evaluator_results.json").read_text(
        encoding="utf-8"))
    contract = json.loads((HERE / "one_loop_uv_pole_evaluator_contract.json").read_text(
        encoding="utf-8"))
    compiler_status = json.loads((HERE / "compiler_status.json").read_text(
        encoding="utf-8"))

    assert contract["uv_pole_evaluator_contract_sha256"] == EXPECTED_CONTRACT
    assert recompute(schema, "x_canonical_sha256")[0] == recompute(
        schema, "x_canonical_sha256")[1]
    assert recompute(plan, "execution_plan_sha256")[0] == recompute(
        plan, "execution_plan_sha256")[1]
    assert recompute(result, "result_sha256")[0] == recompute(
        result, "result_sha256")[1]

    expected_order = (
        [f"UVP_P{i:02d}" for i in range(1, 14)]
        + [f"UVP_C{i:02d}" for i in range(1, 14)]
        + [f"UVP_M{i:02d}" for i in range(1, 14)]
    )
    order_ids = [row["test_id"] for row in plan["execution_order"]]
    result_ids = [row["test_id"] for row in result["tests"]]
    assert order_ids == result_ids == expected_order
    assert [row["global_ordinal"] for row in plan["execution_order"]] == list(
        range(1, 40))
    assert plan["engine_gate"]["required"] == 27
    assert plan["canonical_gate"]["required"] == 12
    assert plan["canonical_gate"]["unlock_condition"] == (
        "ENGINE_GATE_27_OF_27_PASS")

    assert result["preserved_dispositions"] == {
        "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
        "bfb": "BFB_UNRESOLVED",
        "finite_C1_GS": None,
    }

    validator = Draft202012Validator(schema)
    validator.validate(result)

    statuses = [row["status"] for row in result["tests"]]
    terminal = {"PASS", "BLOCKED", "FAIL"}
    executed = sum(status in terminal for status in statuses)
    passed = statuses.count("PASS")
    blocked = statuses.count("BLOCKED")
    failed = statuses.count("FAIL")
    running = [index for index, status in enumerate(statuses)
               if status == "RUNNING"]
    assert all(status in terminal for status in statuses[:executed])
    assert all(status not in terminal for status in statuses[executed:])
    assert len(running) <= 1
    if running:
        assert running[0] == executed
    assert result["counters"] == {
        "total_required": 39, "executed": executed, "passed": passed,
        "blocked": blocked, "failed": failed,
        "not_run_or_locked": 39 - executed,
        "engine_required": 27,
        "engine_executed": sum(status in terminal for status in statuses[:27]),
        "engine_passed": statuses[:27].count("PASS"),
        "canonical_required": 12,
        "canonical_executed": sum(status in terminal for status in statuses[27:]),
        "canonical_passed": statuses[27:].count("PASS"),
    }
    engine_pass = statuses[:27] == ["PASS"] * 27
    canonical_pass = statuses[27:] == ["PASS"] * 12
    if not engine_pass:
        assert all(status == "LOCKED" for status in statuses[27:])
    if blocked or failed:
        assert not running
    for row in result["tests"][:executed]:
        assert row["attempt"] >= 1
        assert row["verdict_reason"]
        assert row["evidence_files"]
        if row["status"] == "PASS":
            for evidence in (row["primary"], row["replay"]):
                assert evidence["state"] == "COMPLETE"
                assert evidence["method"]
                assert evidence["residue_sha256"]
                assert evidence["uv_ir_provenance_sha256"]
                if row["family"] != "PRIMITIVE":
                    assert evidence["inventory_sha256"]
            assert row["derived_result"] is not None
    expected_engine_gate = (
        "PASS" if engine_pass else "FAIL" if failed else
        "BLOCKED" if blocked else "NOT_EARNED"
    )
    expected_counterterm = "PASS" if canonical_pass else "BLOCKED"
    assert result["promotion"] == {
        "engine_gate": expected_engine_gate,
        "counterterm_compiler": expected_counterterm,
        "layer6_authorized": False,
    }

    if executed == 0 and not running:
        assert result["overall_status"] == "NOT_STARTED"
        assert result["authority"] == "EXECUTION_LEDGER_NO_TEST_AUTHORITY"
        assert result["tests"][0]["authorization"] == "READY"
    elif engine_pass and not any(status in terminal | {"RUNNING"}
                                 for status in statuses[27:]):
        assert result["overall_status"] == "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
        assert result["authority"] == "ENGINE_GATE_AUTHORITY"
    elif canonical_pass:
        assert result["overall_status"] == "ONE_LOOP_COUNTERTERM_COMPILER_PASS"
        assert result["authority"] == "FULL_LAYER5_AUTHORITY"

    checkpoint = deepcopy(result)
    checkpoint["overall_status"] = "ONE_LOOP_UV_POLE_EVALUATOR_PASS"
    checkpoint["authority"] = "ENGINE_GATE_AUTHORITY"
    checkpoint["counters"] = {
        "total_required": 39, "executed": 27, "passed": 27,
        "blocked": 0, "failed": 0, "not_run_or_locked": 12,
        "engine_required": 27, "engine_executed": 27,
        "engine_passed": 27, "canonical_required": 12,
        "canonical_executed": 0, "canonical_passed": 0,
    }
    checkpoint["promotion"] = {
        "engine_gate": "PASS", "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }
    for row in checkpoint["tests"][:27]:
        row["status"] = "PASS"
        row["authorization"] = "TERMINAL"
        row["attempt"] = 1
        row["primary"].update({
            "state": "COMPLETE", "method": "SYNTHETIC_SCHEMA_CHECK_ONLY",
            "inventory_sha256": (None if row["family"] == "PRIMITIVE"
                                 else "5" * 64),
            "residue_sha256": "1" * 64,
            "uv_ir_provenance_sha256": "2" * 64,
        })
        row["replay"].update({
            "state": "COMPLETE", "method": "SYNTHETIC_SCHEMA_CHECK_ONLY",
            "inventory_sha256": (None if row["family"] == "PRIMITIVE"
                                 else "6" * 64),
            "residue_sha256": "3" * 64,
            "uv_ir_provenance_sha256": "4" * 64,
        })
        row["derived_result"] = {"synthetic_schema_check_only": True}
        row["verdict_reason"] = "synthetic_27_of_27_schema_transition"
        row["evidence_files"] = ["SYNTHETIC_SCHEMA_CHECK_ONLY"]
    for row in checkpoint["tests"][27:]:
        row["status"] = "LOCKED"
        row["authorization"] = "ENGINE_GATE_REQUIRED"
        row["attempt"] = 0
        row["primary"] = {
            "state": "NOT_RUN", "method": None, "inventory_sha256": None,
            "residue_sha256": None, "uv_ir_provenance_sha256": None,
        }
        row["replay"] = dict(row["primary"])
        row["derived_result"] = None
        row["verdict_reason"] = None
        row["evidence_files"] = []
    checkpoint.pop("result_sha256")
    checkpoint["result_sha256"] = sha256(json.dumps(
        checkpoint, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    validator.validate(checkpoint)
    assert checkpoint["promotion"] == {
        "engine_gate": "PASS",
        "counterterm_compiler": "BLOCKED",
        "layer6_authorized": False,
    }

    assert compiler_status["outcome"] == "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED"
    assert compiler_status["layer6_tensor_IBP_reduction_authorized"] is False
    compiler_status.update({
        "layer5a_execution_plan": "FROZEN_P01_P13_C01_C13_M01_FAIL_FAST",
        "layer5a_execution_plan_sha256": plan["execution_plan_sha256"],
        "layer5a_result_schema_sha256": schema["x_canonical_sha256"],
        "layer5a_current_result_sha256": result["result_sha256"],
        "layer5a_execution_progress": (
            f"{executed}_OF_39_ENGINE_{result['counters']['engine_executed']}_OF_27"),
        "layer5a_synthetic_27_of_27_schema_transition": "PASS",
        "layer5a_tests_executed": executed,
        "layer5a_engine_tests_executed": result["counters"]["engine_executed"],
    })
    if blocked or failed:
        next_test = None
    elif running:
        next_test = result["tests"][running[0]]["test_id"]
    else:
        next_test = next((row["test_id"] for row in result["tests"]
                          if row["status"] in {"NOT_RUN", "LOCKED"}), None)
    compiler_status["next_gate"] = (
        f"EXECUTE_{next_test}" if next_test else result["overall_status"])
    compiler_status["layer5a_next_test"] = next_test
    if result["tests"][0]["status"] == "PASS":
        p01_schema = json.loads((HERE / "uvp_p01_evidence_schema.json").read_text(
            encoding="utf-8"))
        p01_schema_hash = sha256(json.dumps(
            p01_schema, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        compiler_status.update({
            "UVP_P01": "PASS",
            "UVP_P01_evidence_schema_sha256": p01_schema_hash,
            "UVP_P01_normalized_residue": result["tests"][0][
                "derived_result"]["normalized_residue"],
            "UVP_P01_pole_expression": result["tests"][0][
                "derived_result"]["pole_expression"],
            "UVP_P01_evidence_sha256": result["tests"][0][
                "derived_result"]["evidence_sha256"],
        })
    (HERE / "compiler_status.json").write_text(
        json.dumps(compiler_status, indent=2) + "\n", encoding="utf-8")
    execution_status = {
        "outcome": ("LAYER5A_FIRST_EXECUTION_READY" if executed == 0
                    else result["overall_status"]),
        "authority": result["authority"],
        "contract_sha256": EXPECTED_CONTRACT,
        "execution_plan_sha256": plan["execution_plan_sha256"],
        "result_schema_sha256": schema["x_canonical_sha256"],
        "current_result_sha256": result["result_sha256"],
        "total_progress": f"{executed}/39",
        "engine_progress": f"{result['counters']['engine_executed']}/27",
        "next_test": next_test,
        "canonical_gate": "UNLOCKED" if engine_pass else "LOCKED",
        "counterterm_compiler": expected_counterterm,
        "layer6_authorized": False,
    }
    (HERE / "uv_pole_evaluator_execution_status.json").write_text(
        json.dumps(execution_status, indent=2) + "\n", encoding="utf-8")

    print("LAYER5A_EXECUTION_PLAN_AUDIT_PASS")
    print("ORDER P01-P13 C01-C13 M01 THEN_LOCKED_M02-M13")
    print("PROGRESS", f"{executed}/39")
    print("ENGINE_CHECKPOINT", f"{result['counters']['engine_executed']}/27")
    print("SYNTHETIC_27_OF_27_SCHEMA_TRANSITION_PASS")
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
