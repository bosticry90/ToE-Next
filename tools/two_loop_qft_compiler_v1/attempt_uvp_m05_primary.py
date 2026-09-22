"""Fail-closed UVP_M05 capability audit after the M04 attempt-2 pass."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload); embedded = work.pop("artifact_sha256")
    assert embedded == digest(work)
    return payload


def main():
    predecessor = load("uvp_m04_evidence_attempt2.json")
    required = [
        "complete parent-origin one-loop scalar four-point graph inventory",
        "complete symmetrized V4_ABEF*V4_CDEF contractions over 328 real fields",
        "complete partial-BFM vector/Goldstone/ghost scalar four-point pole assembly",
        "projection onto 18 real plus four complex equals 26 real quartic directions",
        "inventory-independent fourth-derivative functional replay",
    ]
    available = [
        "M04 exhaustive sparse V3*V4 cubic contraction backend",
        "exact parent quartic invariant evaluator and on-demand fourth derivatives",
        "passed scalar field residues from M02",
        "validated partial-BFM action and physical vertex API",
    ]
    missing = [
        "exhaustive symmetrized V4*V4 parent four-point contraction backend",
        "complete gauge/Goldstone/ghost scalar four-point pole kernel including gauge-generated quartics",
        "rank-26-real quartic invariant projector",
        "inventory-independent full fourth-derivative replay",
    ]
    inventory = {
        "targets": {
            "real_quartics": 18, "complex_quartics": 4,
            "real_directions": 26,
        },
        "required": required, "available": available, "missing": missing,
    }
    payload = {
        "schema_version": 1, "test_id": "UVP_M05", "attempt": 1,
        "contract_sha256": CONTRACT, "execution_plan_sha256": PLAN,
        "predecessor_M04_evidence_sha256": predecessor["artifact_sha256"],
        "method": "primary_capability_audit_after_M04_cubic_kernel_promotion",
        "inventory": inventory, "inventory_sha256": digest(inventory),
        "all_26_real_quartic_directions_derived": False,
        "residue_values": None,
        "blocker_code": "M05_EXHAUSTIVE_PARENT_SCALAR_4PT_CONTRACTION_PROJECTOR_MISSING",
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
        "uv_ir": {"status": "NOT_EVALUATED",
                  "reason": "required complete 1PI four-point integrands not materialized"},
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m05_primary_blocker.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M05_PRIMARY_BLOCKED")
    print("BLOCKER", payload["blocker_code"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
