"""Audit the non-authoritative complete-primary M05 checkpoint."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work), name
    return payload


def main():
    radial = verified("uvp_m05_sigma_radial_subtheory.json")
    bilinear = verified("uvp_m05_sigma_bilinear_subtheory.json")
    mixed = verified("uvp_m05_phi_sigma_mixed_subtheory.json")
    pure = verified("uvp_m05_pure_sigma_subtheory.json")
    zeta = verified("uvp_m05_zeta_subtheory.json")
    scalar = verified("uvp_m05_complete_scalar_v4v4.json")
    primary = verified("uvp_m05_primary_complete_candidate.json")
    replay_raw = verified("uvp_m05_independent_gauge_replay_uncompared.json")
    replay = verified("uvp_m05_independent_gauge_replay.json")
    preflight = verified("layer5b_m05_m13_preflight.json")
    progress = verified("m05_unblock_progress.json")
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text())
    state = json.loads((ROOT / "project_state.json").read_text())

    assert radial["outcome"] == "M05_SIGMA_RADIAL_SCALAR_SUBTHEORY_PASS"
    assert radial["projection_rank"] == 15 and radial["projection_residual"] == "0"
    assert bilinear["outcome"] == "M05_SIGMA_BILINEAR_SCALAR_SUBTHEORY_PASS"
    assert bilinear["projection_rank"] == 20 and bilinear["projection_residual"] == "0"
    assert mixed["outcome"] == "M05_PHI_SIGMA_MIXED_SCALAR_SUBTHEORY_PASS"
    assert mixed["projection_rank"] == 21 and mixed["projection_residual"] == "0"
    assert pure["outcome"] == "M05_PURE_SIGMA_SCALAR_SUBTHEORY_PASS"
    assert pure["projection_rank"] == 4
    assert pure["projection_residual"] == pure["independent_background_residual"] == "0"
    assert zeta["outcome"] == "M05_ZETA_SCALAR_SUBTHEORY_PASS"
    assert zeta["projection_rank"] == 26
    assert zeta["projection_residual"] == zeta["independent_background_residual"] == "0"

    assert scalar["outcome"] == "M05_COMPLETE_SCALAR_V4V4_PASS"
    assert scalar["authority"] == "IMPLEMENTATION_COMPONENT_ONLY_NOT_UVP_M05_PASS"
    assert scalar["inventory"]["parent_internal_real_directions"] == 328
    assert len(scalar["inventory"]["input_quartic_directions"]) == 26
    assert len(scalar["inventory"]["output_quartic_directions"]) == 26
    assert scalar["projection_rank"] == 26
    assert scalar["projection_residual"] == "0"
    assert scalar["independent_background_residual"] == "0"

    assert primary["outcome"] == "M05_PRIMARY_SCALAR_PLUS_PARTIAL_BFM_GAUGE_COMPLETE"
    assert primary["authority"] == (
        "PRIMARY_IMPLEMENTATION_COMPLETE_REPLAY_PENDING_NOT_UVP_M05_PASS"
    )
    assert primary["projection"]["rank"] == 26
    assert primary["projection"]["scalar_out_of_basis_residual"] == "0"
    assert primary["projection"]["gauge_orbit_out_of_basis_residual"] == "0"
    assert primary["projection"]["PQ_forbidden_residual"] == "0"
    assert primary["projection"]["xi_residual"] == "0"
    assert primary["inventory"]["M02_field_conversion"] == "INCLUDED_EXACTLY_ONCE"

    assert replay_raw["outcome"] == "M05_INDEPENDENT_GAUGE_REPLAY_UNCOMPARED"
    assert replay_raw["inventory"]["projector_rank"] == 26
    assert replay_raw["inventory"]["primary_orbit_projection_imported"] is False
    assert replay_raw["inventory"]["primary_gauge_residues_imported"] is False
    assert replay_raw["extra_background_residual"] == "0"
    assert replay_raw["xi_residual"] == "0"
    assert replay["outcome"] == "M05_INDEPENDENT_GAUGE_REPLAY_PASS"
    assert replay["uncompared_replay_sha256"] == replay_raw["artifact_sha256"]
    assert replay["primary_candidate_sha256"] == primary["artifact_sha256"]
    assert replay["orbit_coefficient_residual"] == "0"
    assert set(replay["gauge_residue_residuals"].values()) == {"0"}
    assert replay["maximum_residual"] == replay["xi_residual"] == "0"
    assert replay["remaining_M05_blocker"] == (
        "INVENTORY_INDEPENDENT_COMPLETE_SCALAR_OPERATOR_REPLAY_MISSING"
    )

    assert preflight["authority"] == (
        "NO_NEW_TEST_AUTHORITY_SERIAL_GATE_REMAINS_AT_M05"
    )
    assert progress["outcome"] == "M05_UNBLOCK_IMPLEMENTATION_PROGRESS"
    assert progress["schema_version"] == 2
    assert progress["current_blocker_code"] == (
        "M05_INVENTORY_INDEPENDENT_COMPLETE_SCALAR_OPERATOR_REPLAY_MISSING"
    )
    assert progress["scientific_boundary"] == {
        "primary_complete": True,
        "independent_gauge_replay_complete": True,
        "independent_complete_scalar_replay_complete": False,
        "UVP_M05_pass_claimed": False,
    }
    assert progress["authoritative_ledger"]["UVP_M05"] == "BLOCKED_ATTEMPT1"

    row = ledger["tests"][30]
    assert row["test_id"] == "UVP_M05"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    counters = ledger["counters"]
    assert {key: counters[key] for key in (
        "total_required", "executed", "passed", "blocked", "failed",
        "not_run_or_locked"
    )} == {
        "total_required": 39, "executed": 31, "passed": 30,
        "blocked": 1, "failed": 0, "not_run_or_locked": 8,
    }
    compiler = state["scaffold"]["two_loop_qft_compiler_v1"]
    assert compiler["layer5a_M05"] == "BLOCKED"
    assert compiler["layer6_tensor_IBP_reduction_authorized"] is False
    assert ledger["preserved_dispositions"]["gauge_matching"] == (
        "DIRECT_GAUGE_MATCHING_UNRESOLVED"
    )
    assert ledger["preserved_dispositions"]["bfb"] == "BFB_UNRESOLVED"

    print("M05_UNBLOCK_PROGRESS_AUDIT_PASS")
    print("PRIMARY_SCALAR_V4V4 rank=26 internal=328 residual=0")
    print("PRIMARY_PARTIAL_BFM_GAUGE xi_residual=0")
    print("INDEPENDENT_GAUGE_REPLAY rank=26 residual=0")
    print("REMAINING complete_inventory_independent_scalar_replay")
    print("AUTHORITATIVE_LEDGER_UNCHANGED 31/39 M05_BLOCKED_ATTEMPT1")
    print("M06_M13_LOCKED LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
