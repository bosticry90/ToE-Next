"""Freeze the first Layer-5A execution order and result-record schema.

This script does not evaluate a loop integral.  It binds contract v2 to an
ordered fail-fast run and emits the initial 0/39 result ledger.
"""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
EXECUTION_ID = "layer5a-v2-first-execution"


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def with_hash(payload, field):
    payload[field] = canonical_hash(payload)
    return payload


def build_result_schema():
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:toe-next:two-loop-qft-compiler-v1:layer5a-result-v1",
        "title": "Layer-5A UV-pole evaluator execution result",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "contract_sha256", "execution_plan_sha256",
            "execution_id", "overall_status", "authority", "counters",
            "promotion", "preserved_dispositions", "tests", "result_sha256",
        ],
        "properties": {
            "schema_version": {"const": 1},
            "contract_sha256": {"const": CONTRACT_HASH},
            "execution_plan_sha256": {
                "type": "string", "pattern": "^[0-9a-f]{64}$"
            },
            "execution_id": {"const": EXECUTION_ID},
            "overall_status": {
                "enum": [
                    "NOT_STARTED", "ENGINE_RUNNING", "ENGINE_BLOCKED",
                    "ENGINE_FAIL", "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
                    "CANONICAL_RUNNING", "CANONICAL_BLOCKED",
                    "CANONICAL_FAIL", "ONE_LOOP_COUNTERTERM_COMPILER_PASS",
                ]
            },
            "authority": {
                "enum": [
                    "EXECUTION_LEDGER_NO_TEST_AUTHORITY",
                    "PARTIAL_TEST_AUTHORITY",
                    "ENGINE_GATE_AUTHORITY",
                    "FULL_LAYER5_AUTHORITY",
                ]
            },
            "counters": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "total_required", "executed", "passed", "blocked",
                    "failed", "not_run_or_locked", "engine_required",
                    "engine_executed", "engine_passed", "canonical_required",
                    "canonical_executed", "canonical_passed",
                ],
                "properties": {
                    key: {"type": "integer", "minimum": 0, "maximum": 39}
                    for key in [
                        "total_required", "executed", "passed", "blocked",
                        "failed", "not_run_or_locked", "engine_required",
                        "engine_executed", "engine_passed",
                        "canonical_required", "canonical_executed",
                        "canonical_passed",
                    ]
                },
            },
            "promotion": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "engine_gate", "counterterm_compiler", "layer6_authorized"
                ],
                "properties": {
                    "engine_gate": {
                        "enum": ["NOT_EARNED", "PASS", "BLOCKED", "FAIL"]
                    },
                    "counterterm_compiler": {
                        "enum": ["BLOCKED", "PASS", "FAIL"]
                    },
                    "layer6_authorized": {"const": False},
                },
            },
            "preserved_dispositions": {
                "type": "object",
                "additionalProperties": False,
                "required": ["gauge_matching", "bfb", "finite_C1_GS"],
                "properties": {
                    "gauge_matching": {
                        "const": "DIRECT_GAUGE_MATCHING_UNRESOLVED"
                    },
                    "bfb": {"const": "BFB_UNRESOLVED"},
                    "finite_C1_GS": {"type": "null"},
                },
            },
            "tests": {
                "type": "array", "minItems": 39, "maxItems": 39,
                "items": {"$ref": "#/$defs/testRecord"},
            },
            "result_sha256": {
                "type": "string", "pattern": "^[0-9a-f]{64}$"
            },
        },
        "$defs": {
            "testRecord": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "test_id", "global_ordinal", "phase", "family", "status",
                    "authorization", "attempt", "primary", "replay",
                    "derived_result", "verdict_reason", "evidence_files",
                ],
                "properties": {
                    "test_id": {
                        "type": "string", "pattern": "^UVP_[PCM][0-9]{2}$"
                    },
                    "global_ordinal": {
                        "type": "integer", "minimum": 1, "maximum": 39
                    },
                    "phase": {"enum": ["ENGINE_5A", "CANONICAL_5B"]},
                    "family": {"enum": ["PRIMITIVE", "CONTROL", "CANONICAL"]},
                    "status": {
                        "enum": ["NOT_RUN", "RUNNING", "PASS", "BLOCKED", "FAIL", "LOCKED"]
                    },
                    "authorization": {
                        "enum": ["READY", "WAITING_PREDECESSOR", "ENGINE_GATE_REQUIRED", "TERMINAL"]
                    },
                    "attempt": {"type": "integer", "minimum": 0},
                    "primary": {"$ref": "#/$defs/evidenceRecord"},
                    "replay": {"$ref": "#/$defs/evidenceRecord"},
                    "derived_result": {"type": ["object", "null"]},
                    "verdict_reason": {"type": ["string", "null"]},
                    "evidence_files": {
                        "type": "array", "items": {"type": "string"},
                    },
                },
            },
            "evidenceRecord": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "state", "method", "inventory_sha256", "residue_sha256",
                    "uv_ir_provenance_sha256",
                ],
                "properties": {
                    "state": {"enum": ["NOT_RUN", "RUNNING", "COMPLETE", "NOT_APPLICABLE"]},
                    "method": {"type": ["string", "null"]},
                    "inventory_sha256": {"type": ["string", "null"]},
                    "residue_sha256": {"type": ["string", "null"]},
                    "uv_ir_provenance_sha256": {"type": ["string", "null"]},
                },
            },
        },
    }
    return with_hash(schema, "x_canonical_sha256")


def build_order(contract):
    primitive = [f"UVP_P{i:02d}" for i in range(1, 14)]
    controls = [f"UVP_C{i:02d}" for i in range(1, 14)]
    canonical = [f"UVP_M{i:02d}" for i in range(1, 14)]
    order = primitive + controls + canonical
    contract_ids = {
        row["test_id"]: row
        for group in (
            contract["primitive_tests"], contract["minimum_control_theories"],
            contract["canonical_model_tests"],
        )
        for row in group
    }
    assert set(order) == set(contract_ids)
    rows = []
    for ordinal, test_id in enumerate(order, start=1):
        if test_id.startswith("UVP_P"):
            family = "PRIMITIVE"
        elif test_id.startswith("UVP_C"):
            family = "CONTROL"
        else:
            family = "CANONICAL"
        phase = "ENGINE_5A" if ordinal <= 27 else "CANONICAL_5B"
        rows.append({
            "test_id": test_id,
            "global_ordinal": ordinal,
            "phase": phase,
            "family": family,
            "predecessor": None if ordinal == 1 else order[ordinal - 2],
            "contract_target": contract_ids[test_id].get(
                "target", contract_ids[test_id].get("amplitude")),
            "advance_only_on": "PASS",
            "on_blocked": "STOP_CURRENT_PHASE_AS_BLOCKED",
            "on_fail": "STOP_CURRENT_PHASE_AS_FAIL",
        })
    return rows


def blank_evidence():
    return {
        "state": "NOT_RUN", "method": None, "inventory_sha256": None,
        "residue_sha256": None, "uv_ir_provenance_sha256": None,
    }


def main():
    contract = json.loads((HERE / "one_loop_uv_pole_evaluator_contract.json").read_text(
        encoding="utf-8"))
    assert contract["uv_pole_evaluator_contract_sha256"] == CONTRACT_HASH
    assert contract["counts"]["total_required_tests"] == 39

    schema = build_result_schema()
    schema_hash = schema["x_canonical_sha256"]
    (HERE / "uv_pole_evaluator_result_schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    order = build_order(contract)
    plan = {
        "schema_version": 1,
        "outcome": "LAYER5A_EXECUTION_PLAN_FROZEN",
        "authority": "EXECUTION_ORDER_AND_RESULT_SCHEMA_ONLY_NO_TEST_EXECUTED",
        "contract_sha256": CONTRACT_HASH,
        "result_schema_sha256": schema_hash,
        "execution_id": EXECUTION_ID,
        "fail_fast": True,
        "engine_gate": {
            "ordinals": [1, 27], "required": 27,
            "pass_outcome": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
            "counterterm_compiler_after_pass": "BLOCKED",
            "layer6_after_pass": "LOCKED",
        },
        "canonical_gate": {
            "ordinals": [28, 39], "required": 12,
            "unlock_condition": "ENGINE_GATE_27_OF_27_PASS",
            "pass_outcome": "ONE_LOOP_COUNTERTERM_COMPILER_PASS",
            "layer6_after_pass": "SEPARATE_AUDIT_REQUIRED",
        },
        "execution_order": order,
    }
    with_hash(plan, "execution_plan_sha256")
    (HERE / "uv_pole_evaluator_execution_plan.json").write_text(
        json.dumps(plan, indent=2) + "\n", encoding="utf-8")

    tests = []
    for row in order:
        if row["global_ordinal"] == 1:
            status, authorization = "NOT_RUN", "READY"
        elif row["phase"] == "ENGINE_5A":
            status, authorization = "NOT_RUN", "WAITING_PREDECESSOR"
        else:
            status, authorization = "LOCKED", "ENGINE_GATE_REQUIRED"
        tests.append({
            "test_id": row["test_id"],
            "global_ordinal": row["global_ordinal"],
            "phase": row["phase"],
            "family": row["family"],
            "status": status,
            "authorization": authorization,
            "attempt": 0,
            "primary": blank_evidence(),
            "replay": blank_evidence(),
            "derived_result": None,
            "verdict_reason": None,
            "evidence_files": [],
        })
    result = {
        "schema_version": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": plan["execution_plan_sha256"],
        "execution_id": EXECUTION_ID,
        "overall_status": "NOT_STARTED",
        "authority": "EXECUTION_LEDGER_NO_TEST_AUTHORITY",
        "counters": {
            "total_required": 39, "executed": 0, "passed": 0,
            "blocked": 0, "failed": 0, "not_run_or_locked": 39,
            "engine_required": 27, "engine_executed": 0,
            "engine_passed": 0, "canonical_required": 12,
            "canonical_executed": 0, "canonical_passed": 0,
        },
        "promotion": {
            "engine_gate": "NOT_EARNED",
            "counterterm_compiler": "BLOCKED",
            "layer6_authorized": False,
        },
        "preserved_dispositions": {
            "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
            "bfb": "BFB_UNRESOLVED",
            "finite_C1_GS": None,
        },
        "tests": tests,
    }
    with_hash(result, "result_sha256")
    result_path = HERE / "uv_pole_evaluator_results.json"
    if result_path.exists():
        existing = json.loads(result_path.read_text(encoding="utf-8"))
        started = (existing["counters"]["executed"] > 0
                   or existing["overall_status"] != "NOT_STARTED")
        if started:
            assert existing["contract_sha256"] == CONTRACT_HASH
            assert existing["execution_plan_sha256"] == plan[
                "execution_plan_sha256"]
            result = existing
        else:
            result_path.write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        result_path.write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(plan["outcome"])
    print("CONTRACT_SHA256", CONTRACT_HASH)
    print("RESULT_SCHEMA_SHA256", schema_hash)
    print("EXECUTION_PLAN_SHA256", plan["execution_plan_sha256"])
    print("PROGRESS", f"{result['counters']['executed']}/39")
    print("ENGINE_CHECKPOINT", f"{result['counters']['engine_executed']}/27")


if __name__ == "__main__":
    main()
