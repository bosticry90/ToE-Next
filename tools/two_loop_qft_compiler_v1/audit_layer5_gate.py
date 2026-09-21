"""Adjudicate promotion layer 5 without inventing missing pole residues."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main():
    compiler = load("compiler_status.json")
    contract = load("layer5_counterterm_contract.json")
    replay = load("layer5_counterterm_independent_replay.json")

    assert compiler["outcome"] in (
        "TWO_LOOP_DIAGRAM_GENERATOR_PASS",
        "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
    )
    assert contract["slot_count"] == 21
    assert contract["all_slot_structures_populated"] is True
    assert contract["all_slot_pole_residues_derived"] is False
    assert all(row["coefficient"] is not None
               for row in contract["counterterm_slots"])
    assert replay["outcome"] == "LAYER5_BARE_ACTION_ROUNDTRIP_PASS"
    assert replay["parent_monomial_families_replayed"] == 29
    assert replay["counterterm_slots_replayed"] == 21
    assert contract["known_gauge_counterterm"]["b10"] == "-34/3"
    assert contract["known_gauge_counterterm"]["ward_identity_residual"] == "0"
    missing = contract["missing_required_one_loop_residues"]
    assert missing

    compiler.update({
        "outcome": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
        "layer4_outcome_preserved": "TWO_LOOP_DIAGRAM_GENERATOR_PASS",
        "layer5_counterterm_action_structure": (
            "PASS_29_PARENT_MONOMIAL_FAMILIES_AND_21_SLOT_DISPATCHES"),
        "layer5_counterterm_contract_sha256": contract[
            "counterterm_contract_sha256"],
        "layer5_bare_action_independent_roundtrip": replay["outcome"],
        "layer5_parent_gauge_counterterm": (
            "PASS_B10_MINUS_34_OVER_3_AND_BACKGROUND_WARD_IDENTITY"),
        "layer5_tadpole_VEV_prescription": (
            "FROZEN_FJ_LIKE_EXPLICIT_TADPOLE_SHIFT"),
        "layer5_parent_operator_bare_expansion_closure": "PASS",
        "layer5_parent_operator_radiative_pole_closure": (
            "BLOCKED_MISSING_ONE_LOOP_POLE_EVALUATOR"),
        "layer5_slot_structures_populated": 21,
        "layer5_slot_pole_residues_derived": 0,
        "layer5_missing_required_residues": missing,
        "layer5_blocker": contract["blocking_layer"],
        "layer6_tensor_IBP_reduction_authorized": False,
        "next_gate": "ONE_LOOP_UV_POLE_EVALUATOR_FOR_LAYER5",
    })
    (HERE / "compiler_status.json").write_text(
        json.dumps(compiler, indent=2) + "\n", encoding="utf-8")
    payload = {
        "outcome": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
        "earned_subgates": [
            "LAYER5_COUNTERTERM_ACTION_STRUCTURE_PASS_RESIDUES_BLOCKED",
            "LAYER5_BARE_ACTION_ROUNDTRIP_PASS",
            "PARENT_GAUGE_COUNTERTERM_AND_BACKGROUND_WARD_IDENTITY_PASS",
            "FJ_LIKE_TADPOLE_VEV_PRESCRIPTION_FROZEN",
        ],
        "counterterm_contract_sha256": contract[
            "counterterm_contract_sha256"],
        "slot_structures_populated": 21,
        "slot_pole_residues_derived": 0,
        "missing_required_residue_groups": len(missing),
        "blocker": contract["blocking_layer"],
        "layer6_authorized": False,
        "finite_C1_GS": None,
    }
    (HERE / "layer5_status.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("EARNED_COUNTERTERM_STRUCTURE PASS")
    print("SLOT_STRUCTURES_POPULATED", 21)
    print("SLOT_POLE_RESIDUES_DERIVED", 0)
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
