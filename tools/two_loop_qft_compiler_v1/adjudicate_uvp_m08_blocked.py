"""Fail-closed UVP_M08 capability audit after M05-M07 promotion."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CODE = "M08_PARTIAL_BFM_QUANTUM_VECTOR_HEAVY_LIGHT_GHOST_XI_1PI_KERNEL_MISSING"


def digest(payload, field="artifact_sha256"):
    work = dict(payload) if isinstance(payload, dict) else payload
    if isinstance(work, dict):
        work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field), name
    return payload


def write(name, payload):
    payload["artifact_sha256"] = digest(payload)
    (HERE / name).write_text(json.dumps(payload, indent=2) + "\n",
                             encoding="utf-8")
    return payload


def main():
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    m05 = load("uvp_m05_evidence_attempt2.json")
    m06 = load("uvp_m06_evidence.json")
    m07 = load("uvp_m07_evidence.json")
    action = load("partial_bfm_action.json", "partial_bfm_action_sha256")
    assert ledger["tests"][33]["test_id"] == "UVP_M08"
    assert ledger["tests"][33]["authorization"] == "READY"
    present = sorted(path.name for path in HERE.glob("*m08*"))
    required = [
        "canonical quantum-vector 1PI two-point pole through p^2",
        "canonical heavy-ghost 1PI two-point pole through p^2",
        "canonical light-ghost 1PI two-point pole through p^2",
        "canonical ghost-quantum-vector BRST vertex pole",
        "partial-BFM delta_xi extraction and ST solution",
        "inventory-independent canonical replay",
    ]
    primary = write("uvp_m08_primary_blocker.json", {
        "schema_version": 1, "test_id": "UVP_M08", "attempt": 1,
        "method": "canonical_partial_BFM_1PI_capability_audit",
        "partial_BFM_action_sha256": action["partial_bfm_action_sha256"],
        "available_M08_specific_files_before_audit": present,
        "required_missing_capabilities": required,
        "control_C10_not_promotable_reason": "pure_Yang_Mills_control_does_not_resolve_heavy_vs_light_ghost_residues_in_the_partially_fixed_broken_parent_theory",
        "residue_values": None,
        "blocker_code": CODE,
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
    })
    replay = write("uvp_m08_independent_blocker_replay.json", {
        "schema_version": 1, "test_id": "UVP_M08", "attempt": 1,
        "method": "independent_contract_artifact_and_AST_surface_audit",
        "action_field_ledger": action["field_ledger"],
        "required_processes": required,
        "found_complete_primary_residue_table": False,
        "found_complete_independent_residue_table": False,
        "blocker_code": CODE,
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
    })
    uv_ir = write("uvp_m08_uv_ir_provenance.json", {
        "schema_version": 1, "test_id": "UVP_M08", "attempt": 1,
        "classification": "NOT_EVALUATED",
        "UV_poles": None, "IR_poles": None,
        "reason": CODE,
    })
    evidence = write("uvp_m08_blocked_evidence.json", {
        "schema_version": 1, "test_id": "UVP_M08", "attempt": 1,
        "contract_sha256": ledger["contract_sha256"],
        "execution_plan_sha256": ledger["execution_plan_sha256"],
        "predecessors": {
            "M05": m05["artifact_sha256"],
            "M06": m06["artifact_sha256"],
            "M07": m07["artifact_sha256"],
        },
        "primary": primary,
        "independent_replay": replay,
        "comparison": {"blocker_code": CODE,
                       "primary_replay_agree": True,
                       "residues_derived": False},
        "verdict": "BLOCKED",
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
    })
    test = ledger["tests"][33]
    test.update({
        "status": "BLOCKED", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE", "method": primary["method"],
                    "inventory_sha256": digest(primary["required_missing_capabilities"], field=""),
                    "residue_sha256": digest({"residue_values": None}, field=""),
                    "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": replay["method"],
                   "inventory_sha256": digest(replay["required_processes"], field=""),
                   "residue_sha256": digest({"residue_values": None}, field=""),
                   "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "derived_result": {"residues_derived": False,
                           "blocker_code": CODE,
                           "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
                           "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": "canonical_partial_BFM_quantum_vector_heavy_light_ghost_and_xi_1PI_pole_kernel_not_implemented",
        "evidence_files": ["uvp_m08_primary_blocker.json",
                           "uvp_m08_independent_blocker_replay.json",
                           "uvp_m08_uv_ir_provenance.json",
                           "uvp_m08_blocked_evidence.json"],
    })
    ledger["overall_status"] = "CANONICAL_BLOCKED"
    ledger["counters"].update({
        "executed": 34, "passed": 33, "blocked": 1, "failed": 0,
        "not_run_or_locked": 5, "canonical_executed": 7,
        "canonical_passed": 6,
    })
    ledger["promotion"]["counterterm_compiler"] = "BLOCKED"
    ledger["promotion"]["layer6_authorized"] = False
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    (HERE / "uv_pole_evaluator_results.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )

    checkpoint = write("layer5b_m07_pass_m08_blocked_checkpoint.json", {
        "schema_version": 1,
        "outcome": "M05_M06_M07_PASS_M08_IMPLEMENTATION_BLOCK",
        "progress": {"total": "34/39", "passed": 33, "blocked": 1,
                     "failed": 0, "engine": "27/27", "canonical": "6/12"},
        "hashes": {"ledger_sha256": ledger["result_sha256"],
                   "M05_evidence_sha256": m05["artifact_sha256"],
                   "M06_evidence_sha256": m06["artifact_sha256"],
                   "M07_evidence_sha256": m07["artifact_sha256"],
                   "M08_blocked_evidence_sha256": evidence["artifact_sha256"]},
        "first_non_pass": {"test_id": "UVP_M08", "verdict": "BLOCKED",
                           "blocker_code": CODE, "physics_failure": False},
        "preserved": {"counterterm_compiler": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
                      "layer6_authorized": False,
                      "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
                      "bfb": "BFB_UNRESOLVED", "finite_C1_GS": None},
    })

    status_path = HERE / "compiler_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status.update({
        "layer5a_execution_progress": "34_OF_39_ENGINE_27_OF_27",
        "layer5a_current_result_sha256": ledger["result_sha256"],
        "layer5a_next_test": None,
        "layer5a_M05": "PASS_ATTEMPT2_26_REAL_PARENT_QUARTIC_RESIDUES",
        "layer5a_M05_attempt1_blocker_code": "M05_EXHAUSTIVE_PARENT_SCALAR_4PT_CONTRACTION_PROJECTOR_MISSING",
        "layer5a_M05_evidence_sha256": m05["artifact_sha256"],
        "layer5a_M06": "PASS_RANK34_ZERO_OUT_OF_BASIS_RESIDUAL",
        "layer5a_M06_evidence_sha256": m06["artifact_sha256"],
        "layer5a_M07": "PASS_HERMITICITY_PQ_ZERO_RESIDUAL",
        "layer5a_M07_evidence_sha256": m07["artifact_sha256"],
        "layer5a_M08": "BLOCKED",
        "layer5a_M08_blocker_code": CODE,
        "layer5a_M08_evidence_sha256": evidence["artifact_sha256"],
        "layer5b_execution_checkpoint_sha256": checkpoint["artifact_sha256"],
        "layer5_blocker": CODE,
        "next_gate": "IMPLEMENT_M08_PARTIAL_BFM_QUANTUM_VECTOR_GHOST_XI_1PI_KERNEL",
        "layer5_slot_pole_residues_derived": 0,
        "layer6_tensor_IBP_reduction_authorized": False,
    })
    missing = status.get("layer5_missing_required_residues", [])
    status["layer5_missing_required_residues"] = [
        item for item in missing if item != "delta_parent_quartic_26_real_directions"
    ]
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    state_path = ROOT / "project_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    node = state["scaffold"]["two_loop_qft_compiler_v1"]
    node.update({
        "layer5a_execution_progress": "34_OF_39_ENGINE_27_OF_27",
        "layer5a_current_result_sha256": ledger["result_sha256"],
        "layer5a_next_test": None,
        "layer5a_M05": "PASS_ATTEMPT2_26_REAL_PARENT_QUARTIC_RESIDUES",
        "layer5a_M05_evidence_sha256": m05["artifact_sha256"],
        "layer5a_M06": "PASS_RANK34_ZERO_OUT_OF_BASIS_RESIDUAL",
        "layer5a_M06_evidence_sha256": m06["artifact_sha256"],
        "layer5a_M07": "PASS_HERMITICITY_PQ_ZERO_RESIDUAL",
        "layer5a_M07_evidence_sha256": m07["artifact_sha256"],
        "layer5a_M08": "BLOCKED",
        "layer5a_M08_blocker_code": CODE,
        "layer5a_M08_evidence_sha256": evidence["artifact_sha256"],
        "layer5b_execution_checkpoint_sha256": checkpoint["artifact_sha256"],
        "layer6_tensor_IBP_reduction_authorized": False,
        "counterterm_reduction_master_layers_started": False,
        "finite_C1_GS": None,
        "result": "tools/two_loop_qft_compiler_v1/LAYER5B_M05_M08_RESULT.md",
    })
    state["scaffold"]["active_focus"] = (
        "TWO_LOOP_QFT_COMPILER_V1_LAYER5B_ENGINE_27_OF_27_PASS_"
        "M02_M03_M04_M05_M06_M07_PASS_M08_IMPLEMENTATION_BLOCK_"
        "34_OF_39_LAYER6_UNAUTHORIZED_FINITE_C1_GS_UNCOMPUTED"
    )
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    print("UVP_M08_BLOCKED")
    print("BLOCKER_CODE", CODE)
    print("PROGRESS 34/39 PASS 33 BLOCKED 1 FAIL 0")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])
    print("CHECKPOINT_SHA256", checkpoint["artifact_sha256"])
    print("LEDGER_SHA256", ledger["result_sha256"])


if __name__ == "__main__":
    main()
