"""Fail-closed audit of the non-authoritative M05--M13 preflight."""

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
    assert embedded == digest(work)
    return payload


def main():
    scalar = verified("uvp_m05_complete_scalar_v4v4.json")
    primary = verified("uvp_m05_primary_complete_candidate.json")
    gauge_replay = verified("uvp_m05_independent_gauge_replay.json")
    preflight = verified("layer5b_m05_m13_preflight.json")
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text())
    state = json.loads((ROOT / "project_state.json").read_text())

    assert scalar["outcome"] == "M05_COMPLETE_SCALAR_V4V4_PASS"
    assert scalar["authority"] == "IMPLEMENTATION_COMPONENT_ONLY_NOT_UVP_M05_PASS"
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
    assert primary["projection"]["xi_residual"] == "0"
    assert gauge_replay["outcome"] == "M05_INDEPENDENT_GAUGE_REPLAY_PASS"
    assert gauge_replay["maximum_residual"] == "0"
    assert gauge_replay["xi_residual"] == "0"
    assert preflight["outcome"] == (
        "LAYER5B_M05_M13_IMPLEMENTATION_PREFLIGHT_COMPLETE"
    )
    assert preflight["authority"] == (
        "NO_NEW_TEST_AUTHORITY_SERIAL_GATE_REMAINS_AT_M05"
    )
    assert preflight["capabilities"]["M05"][
        "independent_gauge_replay"
    ] == "COMPLETE"
    assert preflight["capabilities"]["M05"][
        "independent_complete_scalar_operator_replay"
    ] == "MISSING"
    assert all(str(preflight["capabilities"][f"M{index:02d}"]).startswith("LOCKED")
               for index in range(6, 14))

    row = ledger["tests"][30]
    assert row["test_id"] == "UVP_M05"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    assert ledger["counters"] == {
        **ledger["counters"],
        "total_required": 39,
        "executed": 31,
        "passed": 30,
        "blocked": 1,
        "failed": 0,
        "not_run_or_locked": 8,
    }
    compiler = state["scaffold"]["two_loop_qft_compiler_v1"]
    assert compiler["layer5a_M05"] == "BLOCKED"
    assert compiler["layer6_tensor_IBP_reduction_authorized"] is False
    assert ledger["preserved_dispositions"]["gauge_matching"] == (
        "DIRECT_GAUGE_MATCHING_UNRESOLVED"
    )
    assert ledger["preserved_dispositions"]["bfb"] == "BFB_UNRESOLVED"

    print("LAYER5B_M05_M13_PREFLIGHT_AUDIT_PASS")
    print("M05_PRIMARY_COMPLETE_REPLAY_MISSING")
    print("AUTHORITATIVE_LEDGER_UNCHANGED 31/39 M05_BLOCKED_ATTEMPT1")
    print("M06_M13_LOCKED")
    print("LAYER6_AUTHORIZED=false")


if __name__ == "__main__":
    main()
