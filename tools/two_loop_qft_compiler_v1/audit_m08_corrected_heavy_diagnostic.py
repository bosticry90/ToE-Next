"""Audit corrected heavy M08 preflight evidence and authority ceiling."""

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
    partial = verified("uvp_m08_partial_gf_vector_kernel.json")
    replay = verified(
        "uvp_m08_heavy_mixed_partial_gf_independent_replay.json")
    primary = verified("uvp_m08_brst_three_point_primary_preflight.json")
    diagnostic = verified("uvp_m08_corrected_heavy_block_diagnostic.json")
    results = load(HERE / "uv_pole_evaluator_results.json")
    status = load(HERE / "compiler_status.json")
    project = load(ROOT / "project_state.json")

    mixed = partial["external_heavy_mixed_V_q_sector"][
        "yang_mills_plus_partial_gauge_fixing"]
    assert set(mixed) == {"A", "B"}
    assert set(replay["coefficients"]) == {"A", "B"}
    assert diagnostic["mixed_kernel_primary_replay_residual"] == {
        "A": "0", "B": "0"}
    assert diagnostic["equal_unit_gauge_block_count"] == 5
    assert diagnostic["formal_M08_attempt2_authorized"] is False
    assert diagnostic["single_xi_closure_adjudicated"] is False

    for name in ("Gamma_ubarH_uH_VH", "Gamma_ubarH_uH_qL"):
        process = primary["processes"][name]
        fit = process["non_authoritative_topology_weight_diagnostic"]
        assert float(fit["maximum_fit_residual"]) > 0.25
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
    node = project["scaffold"]["two_loop_qft_compiler_v1"]
    for surface in (status, node):
        assert surface["layer5a_M08"] == "BLOCKED"
        assert surface["layer5a_M08_BRST_remaining_blocker"] == BLOCKER
        assert surface[
            "layer5a_M08_heavy_mixed_two_point_primary_replay_residual"] == "0"
        assert surface["layer5a_M08_heavy_three_point_operator_closure"] == (
            "NONZERO_PRIMARY_RESIDUAL_NO_ADJUDICATION")
    assert node["layer6_tensor_IBP_reduction_authorized"] is False
    assert node["finite_C1_GS"] is None
    assert node["bfb_status"] == "BFB_UNRESOLVED"

    print("M08_CORRECTED_HEAVY_DIAGNOSTIC_AUDIT_PASS")
    print("HEAVY_MIXED_TWO_POINT_PRIMARY_REPLAY_RESIDUAL 0")
    print("HEAVY_THREE_POINT_OPERATOR_CLOSURE NONZERO")
    print("FORMAL_M08_ATTEMPT2_NOT_AUTHORIZED")
    print("AUTHORITY_REMAINS_34_OF_39_M08_BLOCKED_ATTEMPT1")
    print("LAYER6_AUTHORIZED false")


if __name__ == "__main__":
    main()
