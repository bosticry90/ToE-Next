"""Freeze M05 implementation progress without adjudicating attempt 2."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


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
    names = {
        "restricted_Phi_phi_S_scalar_V4V4": "uvp_m05_active_scalar_subspace.json",
        "restricted_independent_audit": "uvp_m05_active_scalar_subspace_audit.json",
        "full_rank26_projector": "uvp_m05_rank26_projector.json",
        "gauge_orbit_quartic_projection": "uvp_m05_gauge_orbit_quartic.json",
        "Sigma_radial_regression": "uvp_m05_sigma_radial_subtheory.json",
        "Sigma_bilinear_regression": "uvp_m05_sigma_bilinear_subtheory.json",
        "Phi_Sigma_mixed_regression": "uvp_m05_phi_sigma_mixed_subtheory.json",
        "pure_Sigma_regression": "uvp_m05_pure_sigma_subtheory.json",
        "zEta_regression": "uvp_m05_zeta_subtheory.json",
        "complete_primary_scalar_V4V4": "uvp_m05_complete_scalar_v4v4.json",
        "complete_primary_scalar_plus_gauge": "uvp_m05_primary_complete_candidate.json",
        "independent_gauge_replay_uncompared": "uvp_m05_independent_gauge_replay_uncompared.json",
        "independent_gauge_replay": "uvp_m05_independent_gauge_replay.json",
        "M05_M13_preflight": "layer5b_m05_m13_preflight.json",
    }
    artifacts = {label: verified(name) for label, name in names.items()}
    payload = {
        "schema_version": 2,
        "outcome": "M05_UNBLOCK_IMPLEMENTATION_PROGRESS",
        "authority": "NO_NEW_TEST_AUTHORITY_M05_ATTEMPT1_REMAINS_BLOCKED",
        "completed_components": {
            label: artifact["artifact_sha256"]
            for label, artifact in artifacts.items()
        },
        "completed_counts": {
            "parent_internal_real_directions": 328,
            "quartic_input_directions": 26,
            "quartic_output_directions": 26,
            "primary_projector_rank": 26,
            "primary_verification_backgrounds": 2,
            "independent_gauge_projector_rank": 26,
            "independent_gauge_residue_residual": "0",
            "partial_BFM_xi_residual": "0",
        },
        "current_blocker_code": (
            "M05_INVENTORY_INDEPENDENT_COMPLETE_SCALAR_OPERATOR_REPLAY_MISSING"
        ),
        "missing": [
            "complete inventory-independent scalar V4V4 operator replay across all 328 real internal directions",
            "formal M05 attempt-2 adjudication after primary and complete replay are frozen",
        ],
        "scientific_boundary": {
            "primary_complete": True,
            "independent_gauge_replay_complete": True,
            "independent_complete_scalar_replay_complete": False,
            "UVP_M05_pass_claimed": False,
        },
        "authoritative_ledger": {
            "progress": "31/39",
            "passed": 30,
            "blocked": 1,
            "failed": 0,
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
