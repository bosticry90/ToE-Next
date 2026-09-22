"""Independent M05 implementation-surface audit."""

from ast import parse
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    modules = ["m04_parent_scalar_kernel.py", "physical_vertex_api.py",
               "scalar_vertex_oracle.py"]
    names = set()
    for module in modules:
        path = HERE / module
        if path.exists():
            tree = parse(path.read_text(encoding="utf-8"))
            names.update(node.name for node in tree.body if hasattr(node, "name"))
    required = {
        "contract_all_V4_V4_for_quartic_poles",
        "enumerate_parent_scalar_one_loop_4pt",
        "project_26_real_quartic_poles",
        "functional_fourth_derivative_pole_replay",
        "assemble_partial_BFM_scalar_four_point_poles",
    }
    absent = sorted(required - names)
    assert absent == sorted(required)
    inventory = {
        "AST_scanned_modules": modules,
        "available_top_level_names": len(names),
        "required_entry_points": sorted(required),
        "absent_entry_points": absent,
        "primary_M05_inventory_imported": False,
    }
    payload = {
        "schema_version": 1, "test_id": "UVP_M05", "attempt": 1,
        "contract_sha256": CONTRACT, "execution_plan_sha256": PLAN,
        "method": "independent_AST_and_artifact_manifest_capability_audit",
        "inventory": inventory, "inventory_sha256": digest(inventory),
        "all_26_real_quartic_directions_derived": False,
        "residue_values": None,
        "blocker_code": "M05_EXHAUSTIVE_PARENT_SCALAR_4PT_CONTRACTION_PROJECTOR_MISSING",
        "classification": "IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL",
        "uv_ir": {"status": "NOT_EVALUATED",
                  "reason": "independent complete four-point inventory cannot be constructed"},
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m05_independent_blocker_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M05_INDEPENDENT_BLOCKER_REPLAY_COMPLETE")
    print("BLOCKER", payload["blocker_code"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
