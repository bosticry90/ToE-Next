"""Audit M08 BRST-three-point progress and the unchanged authority ceiling."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def verified(name):
    payload = load(name)
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    calculated = sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert embedded == calculated, name
    return payload


def main():
    action = load("partial_bfm_action.json")
    surface = verified("uvp_m08_brst_vertex_surface.json")
    primary_inventory = verified(
        "uvp_m08_brst_three_point_primary_inventory.json")
    replay_inventory = verified(
        "uvp_m08_brst_inventory_independent_replay.json")
    comparison = verified("uvp_m08_brst_inventory_comparison.json")
    lorentz = verified("uvp_m08_brst_three_point_lorentz_preflight.json")
    primary = verified("uvp_m08_brst_three_point_primary_preflight.json")
    results = load("uv_pole_evaluator_results.json")
    status = load("compiler_status.json")
    project = json.loads((ROOT / "project_state.json").read_text())

    action_hash = action["partial_bfm_action_sha256"]
    for artifact in (surface, primary_inventory, replay_inventory, primary):
        assert artifact["immutable_partial_BFM_action_sha256"] == action_hash
        assert artifact["authority"] == (
            "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY")

    expected = {
        "Gamma_ubarH_uH_VH": (17, 13, 4),
        "Gamma_ubarH_uH_qL": (16, 12, 4),
        "Gamma_cbarL_cL_qL": (2, 2, 0),
    }
    for process, values in expected.items():
        p = primary_inventory["summary"][process]
        r = replay_inventory["summary"][process]
        assert (p["canonical_records"], p["requires_UV_evaluation"],
                p["power_counted_zero"]) == values
        assert p == r
        assert comparison["comparisons"][process][
            "primary_minus_replay"] == []
        assert comparison["comparisons"][process][
            "replay_minus_primary"] == []
    assert comparison["maximum_set_difference"] == 0

    calibration = lorentz["calibration"]
    assert calibration["derived_Lorentz_sum"] == "rho"
    assert calibration["ghost_triangle_color_projection"] == "-C_A/2"
    assert calibration["Yang_Mills_triangle_color_projection"] == "+C_A/2"
    assert calibration["Yang_Mills_cubic_relative_Feynman_rule_sign"] == "-1"
    assert calibration["derived_full_tree_coefficient"] == "-C_A*rho/2"
    assert not calibration["expected_C10_value_imported_as_input"]
    assert primary["formal_M08_retry_authorized"] is False
    assert "independent graph inventory and residue replay" in primary[
        "remaining_before_retry"]

    row = results["tests"][33]
    assert row["test_id"] == "UVP_M08"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    assert results["counters"]["total_required"] == 39
    assert results["counters"]["executed"] == 34
    assert results["counters"]["passed"] == 33
    assert results["counters"]["blocked"] == 1
    assert results["counters"]["failed"] == 0
    assert results["counters"]["not_run_or_locked"] == 5
    assert status["layer5a_M08"] == "BLOCKED"
    assert status["layer5a_M08_BRST_remaining_blocker"] == (
        "HEAVY_CHANNEL_PARTIAL_GF_BRST_RESIDUE_REASSEMBLY_AND_COMPLETE_"
        "INDEPENDENT_REPLAY_MISSING")
    node = project["scaffold"]["two_loop_qft_compiler_v1"]
    assert node["layer5a_M08"] == "BLOCKED"
    assert node["layer5a_M08_BRST_remaining_blocker"] == status[
        "layer5a_M08_BRST_remaining_blocker"]
    assert node["layer6_tensor_IBP_reduction_authorized"] is False
    assert node["finite_C1_GS"] is None
    assert node["bfb_status"] == "BFB_UNRESOLVED"

    print("M08_BRST_THREE_POINT_PREFLIGHT_AUDIT_PASS")
    print("PRIMARY_REPLAY_INVENTORY_MAXIMUM_SET_DIFFERENCE 0")
    print("FORMAL_M08_ATTEMPT2_NOT_AUTHORIZED")
    print("AUTHORITY_REMAINS_34_OF_39_M08_BLOCKED_ATTEMPT1")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
