"""Audit the non-authoritative M05 implementation checkpoint fail closed."""

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
    payload = json.loads((HERE / name).read_text())
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work)
    return payload


def main():
    primary = verified("uvp_m05_active_scalar_subspace.json")
    replay = verified("uvp_m05_active_scalar_subspace_audit.json")
    projector = verified("uvp_m05_rank26_projector.json")
    gauge = verified("uvp_m05_gauge_orbit_quartic.json")
    progress = verified("m05_unblock_progress.json")
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text())
    state = json.loads((ROOT / "project_state.json").read_text())

    assert primary["authority"] == "M05_SCALAR_SUBSPACE_IMPLEMENTATION_NOT_GATE_PASS"
    assert primary["projection_rank"] == 11
    assert primary["projection_residual"] == "0"
    assert primary["inventory"]["active_internal_real_directions"] == 76
    assert primary["inventory"]["Sigma_directions_deliberately_not_claimed"] == 252
    assert replay["outcome"] == "M05_ACTIVE_SCALAR_SUBSPACE_AUDIT_PASS"
    assert replay["primary_artifact_sha256"] == primary["artifact_sha256"]
    assert replay["projector_rank"] == 11
    assert projector["outcome"] == "M05_RANK26_QUARTIC_PROJECTOR_PASS"
    assert projector["projection_rank"] == 26
    assert projector["inventory"]["active_witnesses"] == 11
    assert projector["inventory"]["Sigma_bearing_witnesses"] == 15
    assert gauge["outcome"] == "M05_GAUGE_ORBIT_QUARTIC_PROJECTION_PASS"
    assert gauge["rank"] == 26 and gauge["verification_residual"] == "0"
    assert gauge["projected_coefficients"]["lambdaPhi2"] == "10"
    assert gauge["projected_coefficients"]["lambdaSigma4"] == "-1/2"
    assert not any(name.startswith("z") for name in gauge["projected_coefficients"])
    assert progress["outcome"] == "M05_UNBLOCK_IMPLEMENTATION_PROGRESS"
    assert progress["current_blocker_code"] == (
        "M05_SIGMA_V4V4_AND_PARTIAL_BFM_4PT_ASSEMBLY_MISSING"
    )
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
    print("RESTRICTED_SCALAR_SUBTHEORY rank=11 internal=76 residual=0")
    print("FULL_QUARTIC_PROJECTOR rank=26 exact_nonzero_determinant")
    print("GAUGE_ORBIT_QUARTIC rank=26 verification_residual=0")
    print("AUTHORITATIVE_LEDGER_UNCHANGED 31/39 M05_BLOCKED_ATTEMPT1")
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
