"""Freeze the non-authoritative M05--M13 implementation preflight."""

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
    scalar = verified("uvp_m05_complete_scalar_v4v4.json")
    primary = verified("uvp_m05_primary_complete_candidate.json")
    gauge_replay = verified("uvp_m05_independent_gauge_replay.json")
    payload = {
        "schema_version": 1,
        "outcome": "LAYER5B_M05_M13_IMPLEMENTATION_PREFLIGHT_COMPLETE",
        "authority": "NO_NEW_TEST_AUTHORITY_SERIAL_GATE_REMAINS_AT_M05",
        "inputs": {
            "complete_primary_scalar": scalar["artifact_sha256"],
            "complete_primary_scalar_plus_gauge": primary["artifact_sha256"],
            "independent_gauge_replay": gauge_replay["artifact_sha256"],
        },
        "capabilities": {
            "M05": {
                "primary_scalar_26_direction": "COMPLETE",
                "primary_partial_BFM_gauge": "COMPLETE",
                "independent_gauge_replay": "COMPLETE",
                "independent_complete_scalar_operator_replay": "MISSING",
                "scientific_status": "BLOCKED_ATTEMPT1",
            },
            "M06": "LOCKED_AGGREGATE_RANK34_NOT_EXECUTED",
            "M07": "LOCKED_AGGREGATE_HERMITICITY_PQ_NOT_EXECUTED",
            "M08": "LOCKED_QUANTUM_VECTOR_GHOST_XI_RESIDUES_INCOMPLETE",
            "M09": "LOCKED_VEV_TADPOLE_RESIDUES_INCOMPLETE",
            "M10": "LOCKED_33_GOLDSTONE_IDENTITIES_NOT_EXECUTABLE",
            "M11": "LOCKED_RENORMALIZED_AMPLITUDE_CANCELLATION_NOT_EXECUTABLE",
            "M12": "LOCKED_21_SLOT_STRUCTURES_EXIST_COEFFICIENTS_INCOMPLETE",
            "M13": "LOCKED_COMPLETE_INVENTORY_INDEPENDENT_REPLAY_MISSING",
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
    (HERE / "layer5b_m05_m13_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
