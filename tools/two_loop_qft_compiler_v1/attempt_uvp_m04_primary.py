"""Fail-closed UVP_M04 capability audit after the M03 attempt-2 pass."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
M03 = "ddad67dc0278be554c5a4cd401d66e348ed08cfef6f0bd6a4a0df406ca0b5451"


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def main():
    required = [
        "complete parent-origin one-loop scalar three-point inventory",
        "complete symmetrized V3_ADE*V4_BCDE contractions over 328 real fields",
        "partial-BFM vector/Goldstone/ghost scalar three-point pole assembly",
        "projection onto muPhi,muPhiPhi,Re(z6),Im(z6) after M02 field residues",
        "inventory-independent functional third-derivative replay",
    ]
    available = [
        "M03 diagonal V3_ACD*V3_BCD mass contraction",
        "M03 diagonal M2_CD*V4_ABCD mass contraction",
        "exact on-demand parent scalar derivatives",
        "M02 field residues",
    ]
    missing = [
        "exhaustive mixed V3*V4 three-point contraction backend",
        "complete gauge/Goldstone/ghost scalar three-point pole kernel",
        "rank-four-real cubic invariant projector and independent replay",
    ]
    inventory = {"targets": ["muPhi", "muPhiPhi", "Re(z6)", "Im(z6)"],
                 "required": required, "available": available,
                 "missing": missing}
    payload = {
        "schema_version": 1,
        "test_id": "UVP_M04",
        "attempt": 1,
        "contract_sha256": CONTRACT,
        "execution_plan_sha256": PLAN,
        "predecessor_M03_evidence_sha256": M03,
        "method": "primary_capability_audit_after_M03_quadratic_kernel_promotion",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "all_four_real_cubic_directions_derived": False,
        "residue_values": None,
        "blocker_code": (
            "M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING"
        ),
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
        "uv_ir": {"status": "NOT_EVALUATED",
                  "reason": "required 1PI three-point integrands not materialized"},
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m04_primary_blocker.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M04_PRIMARY_BLOCKED")
    print("BLOCKER", payload["blocker_code"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
