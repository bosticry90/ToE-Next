"""Compile model-independent layer-4 topologies and future CT slots only."""

from hashlib import sha256
import json
from pathlib import Path

from diagram_topology import enumerate_two_point_topologies, validate_topology
from momentum_routing import route


HERE = Path(__file__).resolve().parent
ACTION_HASH = "2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491"


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def counterterm_slots(one_loop):
    slots = []
    for topology in one_loop:
        topology_id = topology["topology_id"]
        for edge in range(topology["internal_propagators"]):
            for kind in ("field", "mass", "gauge_parameter"):
                slots.append({
                    "slot_id": f"{topology_id}:edge{edge}:{kind}",
                    "parent_topology_id": topology_id,
                    "location": {"kind": "internal_edge", "ordinal": edge},
                    "counterterm_kind": kind,
                    "coefficient": None,
                })
        for vertex in range(topology["vertex_count"]):
            for kind in ("gauge_coupling", "VEV", "tadpole", "vertex"):
                slots.append({
                    "slot_id": f"{topology_id}:vertex{vertex}:{kind}",
                    "parent_topology_id": topology_id,
                    "location": {"kind": "vertex", "ordinal": vertex},
                    "counterterm_kind": kind,
                    "coefficient": None,
                })
    return slots


def main():
    one_loop = enumerate_two_point_topologies(1)
    two_loop = enumerate_two_point_topologies(2)
    for row in one_loop + two_loop:
        validate_topology(row)
        row["momentum_routing"] = route(row)
    payload = {
        "outcome": "MODEL_INDEPENDENT_TWO_POINT_TOPOLOGY_ENGINE_PASS",
        "immutable_partial_bfm_action_sha256": ACTION_HASH,
        "external_background_legs": "two_labelled_amputated_legs",
        "one_loop_topologies": one_loop,
        "two_loop_topologies": two_loop,
        "one_loop_with_counterterm_slots": counterterm_slots(one_loop),
        "counts": {
            "one_loop_1PI_topologies": len(one_loop),
            "two_loop_1PI_topologies": len(two_loop),
            "future_counterterm_slots": len(counterterm_slots(one_loop)),
        },
        "scope_boundary": {
            "physical_field_assignment": False,
            "counterterm_coefficients": False,
            "numerator_construction": False,
            "tensor_reduction": False,
            "integral_evaluation": False,
        },
    }
    payload["topology_inventory_sha256"] = canonical_hash(payload)
    (HERE / "layer4_topologies.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("ONE_LOOP_TOPOLOGIES", len(one_loop))
    print("TWO_LOOP_TOPOLOGIES", len(two_loop))
    print("COUNTERTERM_SLOTS", len(payload["one_loop_with_counterterm_slots"]))
    print("TOPOLOGY_SHA256", payload["topology_inventory_sha256"])


if __name__ == "__main__":
    main()
