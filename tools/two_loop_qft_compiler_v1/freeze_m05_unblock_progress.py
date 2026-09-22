"""Freeze implementation progress without adjudicating a new M05 attempt."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


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
    active = verified("uvp_m05_active_scalar_subspace.json")
    replay = verified("uvp_m05_active_scalar_subspace_audit.json")
    projector = verified("uvp_m05_rank26_projector.json")
    gauge = verified("uvp_m05_gauge_orbit_quartic.json")
    payload = {
        "schema_version": 1,
        "outcome": "M05_UNBLOCK_IMPLEMENTATION_PROGRESS",
        "authority": "NO_NEW_TEST_AUTHORITY_M05_ATTEMPT1_REMAINS_BLOCKED",
        "completed_components": {
            "restricted_Phi_phi_S_scalar_V4V4": active["artifact_sha256"],
            "restricted_independent_audit": replay["artifact_sha256"],
            "full_rank26_projector": projector["artifact_sha256"],
            "gauge_orbit_quartic_projection": gauge["artifact_sha256"],
        },
        "completed_counts": {
            "restricted_internal_real_directions": 76,
            "restricted_quartic_directions": 11,
            "full_projector_rank": 26,
            "gauge_orbit_nonzero_invariant_directions": 13,
        },
        "current_blocker_code": (
            "M05_SIGMA_V4V4_AND_PARTIAL_BFM_4PT_ASSEMBLY_MISSING"
        ),
        "missing": [
            "252-real-direction Sigma-containing V4V4 contractions",
            "complete partial-BFM vector/Goldstone/ghost four-point pole prefactor and xi cancellation",
            "complete inventory-independent 26-direction residue replay",
        ],
        "authoritative_ledger": {
            "progress": "31/39",
            "UVP_M05": "BLOCKED_ATTEMPT1",
            "counterterm_compiler": "BLOCKED",
            "layer6_authorized": False,
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "m05_unblock_progress.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("BLOCKER", payload["current_blocker_code"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
