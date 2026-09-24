"""Audit the corrected M08 light-channel ST control and authority ceiling."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BLOCKER = (
    "HEAVY_BRST_THREE_POINT_OPERATOR_CLOSURE_AND_COMPLETE_INDEPENDENT_"
    "RESIDUE_REPLAY_INCOMPLETE"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verified(name):
    payload = load(HERE / name)
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    calculated = sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert embedded == calculated, name
    return payload


def main():
    action = load(HERE / "partial_bfm_action.json")
    kernel = verified("uvp_m08_partial_gf_vector_kernel.json")
    light = verified("uvp_m08_light_st_normalization.json")
    replay = verified("uvp_m08_light_st_independent_replay.json")
    primary = verified("uvp_m08_brst_three_point_primary_preflight.json")
    results = load(HERE / "uv_pole_evaluator_results.json")
    status = load(HERE / "compiler_status.json")
    project = load(ROOT / "project_state.json")

    action_hash = action["partial_bfm_action_sha256"]
    assert light["immutable_partial_BFM_action_sha256"] == action_hash
    assert replay["immutable_partial_BFM_action_sha256"] == action_hash
    assert kernel["complete_heavy_H_matter_gauge_fixing_sector"] == {
        "A": "-11/3", "B": "11/3", "transversality_residual": "0"}
    assert light["maximum_ST_residual"] == "0"
    assert replay["ST_residual"] == "0"
    assert replay["complete_M08_replay"] is False
    assert light["formal_M08_retry_authorized"] is False
    assert light["light_gauge_parameter_diagnostic"]["block_count"] == 3

    # The corrected primary light process closes, while the heavy processes
    # remain deliberately non-promotable until their partial-GF vertices and
    # complete independent replay are assembled.
    samples = primary["processes"]["Gamma_cbarL_cL_qL"][
        "sample_tree_operator_projections"]
    for row in samples:
        assert float(row["ST_actual_minus_counterterm_p_maximum_residual"]) < 3e-11
        assert row["ST_actual_minus_counterterm_q_maximum_residual"] == "0"
    assert primary["formal_M08_retry_authorized"] is False

    row = results["tests"][33]
    assert row["test_id"] == "UVP_M08"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    counters = results["counters"]
    assert counters["total_required"] == 39
    assert counters["executed"] == 34
    assert counters["passed"] == 33
    assert counters["blocked"] == 1
    assert counters["failed"] == 0
    assert counters["not_run_or_locked"] == 5
    assert status["layer5a_M08"] == "BLOCKED"
    assert status["layer5a_M08_BRST_remaining_blocker"] == BLOCKER
    assert status["layer5a_M08_light_ST_residual"] == "0"
    node = project["scaffold"]["two_loop_qft_compiler_v1"]
    assert node["layer5a_M08_BRST_remaining_blocker"] == BLOCKER
    assert node["layer5a_M08_light_ST_residual"] == "0"
    assert node["layer6_tensor_IBP_reduction_authorized"] is False
    assert node["finite_C1_GS"] is None
    assert node["bfb_status"] == "BFB_UNRESOLVED"

    print("M08_LIGHT_ST_NORMALIZATION_AUDIT_PASS")
    print("ORDINARY_LIGHT_ST_RESIDUAL 0")
    print("INDEPENDENT_FUNCTIONAL_REPLAY_RESIDUAL 0")
    print("FORMAL_M08_ATTEMPT2_NOT_AUTHORIZED")
    print("AUTHORITY_REMAINS_34_OF_39_M08_BLOCKED_ATTEMPT1")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
