"""Primary complete one-loop topology inventory for the three M08 vertices.

The enumerator starts from the action-derived cubic/quartic signatures.  It
does not assume the familiar named diagrams: all solutions of
``n3 + 2*n4 = 3`` are generated, external legs are attached, the remaining
half edges are paired, and connected one-particle-irreducible graphs are
canonicalized.  Dimensionful scalar/Goldstone candidates are retained with
an explicit power-counted-zero disposition.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations_with_replacement
import json
from pathlib import Path

import networkx as nx

from m08_brst_vertex_action import build_vertex_surface
HERE = Path(__file__).resolve().parent

TARGETS = {
    "Gamma_ubarH_uH_VH": ("ubar_H", "u_H", "V_H"),
    "Gamma_ubarH_uH_qL": ("ubar_H", "u_H", "q_L"),
    "Gamma_cbarL_cL_qL": ("cbar_L", "c_L", "q_L"),
}

PAIR = {
    "ubar_H": "u_H", "u_H": "ubar_H",
    "cbar_L": "c_L", "c_L": "cbar_L",
    "V_H": "V_H", "q_L": "q_L", "G_H": "G_H",
    "S_phys": "S_phys",
}


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def pairings(slots):
    """Yield perfect pairings of compatible indexed half edges."""
    if not slots:
        yield ()
        return
    first = slots[0]
    for index in range(1, len(slots)):
        second = slots[index]
        if PAIR[first[2]] != second[2]:
            continue
        rest = slots[1:index] + slots[index + 1:]
        for tail in pairings(rest):
            yield ((first, second),) + tail


def external_attachments(vertices, target):
    slots = [(v, s, field) for v, row in enumerate(vertices)
             for s, field in enumerate(row["fields"])]

    def rec(position, available, chosen):
        if position == len(target):
            yield tuple(chosen), available
            return
        field = target[position]
        for index, slot in enumerate(available):
            if slot[2] != field:
                continue
            yield from rec(position + 1,
                           available[:index] + available[index + 1:],
                           chosen + [(position, slot)])

    yield from rec(0, slots, [])


def graph_is_1pi(vertex_count, edges):
    graph = nx.MultiGraph()
    graph.add_nodes_from(range(vertex_count))
    graph.add_edges_from((left[0], right[0]) for left, right in edges)
    if not nx.is_connected(graph):
        return False
    # Removing any internal line must leave a connected graph.  MultiGraph
    # bridges implements the correct parallel-edge behavior.
    return not list(nx.bridges(graph))


def canonical_key(vertices, external, edges, quartic_channel=None):
    """Slot- and vertex-label independent colored incidence-graph hash."""
    graph = nx.Graph()
    for v, row in enumerate(vertices):
        graph.add_node(("v", v), label="vertex:" + row["vertex_id"])
        for s, field in enumerate(row["fields"]):
            half = ("h", v, s)
            graph.add_node(half, label="halfedge:" + field)
            graph.add_edge(("v", v), half)
    for ext_index, slot in external:
        marker = ("x", ext_index)
        graph.add_node(marker, label=f"external:{ext_index}:{slot[2]}")
        graph.add_edge(marker, ("h", slot[0], slot[1]))
    for edge_index, (left, right) in enumerate(edges):
        fields = tuple(sorted((left[2], right[2])))
        propagator = ("p", edge_index)
        graph.add_node(propagator, label="propagator:" + ":".join(fields))
        graph.add_edge(propagator, ("h", left[0], left[1]))
        graph.add_edge(propagator, ("h", right[0], right[1]))
    graph.add_node(("channel", 0), label="channel:" + str(quartic_channel))
    return nx.weisfeiler_lehman_graph_hash(graph, node_attr="label",
                                           iterations=8)


def ghost_loop_count(topology):
    # Every ordinary triangle/swordfish has one open ghost chain between the
    # two external ghost legs.  When both external ghosts sit on the ordered
    # quartic vertex, its two remaining slots and the cubic vertex make one
    # closed oriented ghost loop.
    return 1 if topology == "equivariant_quartic_ghost_bubble" else 0


def classify(vertices, edges):
    ids = [row["vertex_id"] for row in vertices]
    if len(vertices) == 3:
        if sum(value.startswith(("HGH_", "LGH_")) for value in ids) == 3:
            return "ghost_vector_triangle"
        if any(value.startswith("YM_") for value in ids):
            return "one_ghost_two_vector_triangle"
        if any("_G" in value or "_S" in value for value in ids):
            return "scalar_or_Goldstone_triangle"
        return "three_cubic_triangle"
    if "HGH4_ubar_u_ubar_u" in ids:
        return "equivariant_quartic_ghost_bubble"
    return "seagull_cubic_swordfish"


def build_inventory():
    cubic, quartic = build_vertex_surface()
    candidates = []
    for combo in combinations_with_replacement(range(len(cubic)), 3):
        candidates.append([cubic[index] for index in combo])
    for left in range(len(cubic)):
        for right in range(len(quartic)):
            candidates.append([cubic[left], quartic[right]])

    results = {}
    for process, target in TARGETS.items():
        records = {}
        for vertices in candidates:
            if sum(len(row["fields"]) - 2 for row in vertices) != 3:
                continue
            for external, internal in external_attachments(vertices, target):
                if len(internal) % 2:
                    continue
                for edges in pairings(list(internal)):
                    if not graph_is_1pi(len(vertices), edges):
                        continue
                    channels = [None]
                    if any(row["vertex_id"] == "HGH4_ubar_u_ubar_u"
                           for row in vertices):
                        channels = ["direct", "exchange"]
                    for channel in channels:
                        key = canonical_key(vertices, external, edges, channel)
                        if key in records:
                            continue
                        dimensionful = sum(row.get(
                            "dimensionful_coupling_power", 0)
                            for row in vertices)
                        disposition = (
                            "POWER_COUNTED_UV_ZERO_NO_LOCAL_DIMENSION_ONE_"
                            "GHOST_VECTOR_OPERATOR"
                            if dimensionful >= 2 else "REQUIRES_UV_EVALUATION"
                        )
                        topology = classify(vertices, edges)
                        loops = ghost_loop_count(topology)
                        records[key] = {
                            "process": process,
                            "topology": topology,
                            "vertex_ids": [row["vertex_id"]
                                           for row in vertices],
                            "external_attachments": [
                                {"external_ordinal": ext,
                                 "vertex": slot[0], "slot": slot[1],
                                 "field": slot[2]}
                                for ext, slot in external
                            ],
                            "internal_edges": [
                                {"left": list(left), "right": list(right),
                                 "propagator": (
                                     "heavy_ghost" if left[2] in
                                     ("u_H", "ubar_H") else
                                     "light_ghost" if left[2] in
                                     ("c_L", "cbar_L") else left[2])}
                                for left, right in edges
                            ],
                            "quartic_ghost_channel": channel,
                            "dimensionful_coupling_power": dimensionful,
                            "UV_disposition": disposition,
                            "closed_ghost_loops": loops,
                            "statistics_sign": str(-1 if loops % 2 else 1),
                            "canonical_graph_sha256": key,
                        }
        ordered = sorted(records.values(), key=lambda row: (
            row["topology"], row["vertex_ids"],
            row["canonical_graph_sha256"]))
        results[process] = ordered
    return results


def main():
    action_manifest = json.loads(
        (HERE / "partial_bfm_action.json").read_text(encoding="utf-8"))
    inventory = build_inventory()
    summary = {}
    for process, records in inventory.items():
        summary[process] = {
            "canonical_records": len(records),
            "requires_UV_evaluation": sum(
                row["UV_disposition"] == "REQUIRES_UV_EVALUATION"
                for row in records),
            "power_counted_zero": sum(
                row["UV_disposition"].startswith("POWER_COUNTED")
                for row in records),
            "topology_counts": dict(sorted(Counter(
                row["topology"] for row in records).items())),
        }
    payload = {
        "schema_version": 1,
        "outcome": "M08_PRIMARY_BRST_THREE_POINT_INVENTORY_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action_manifest[
            "partial_bfm_action_sha256"],
        "topology_equation": "n3+2*n4=3_for_E3_L1",
        "enumeration_method": (
            "action_signature_half_edge_pairing_then_graph_isomorphism_"
            "canonicalization"
        ),
        "summary": summary,
        "records": inventory,
        "completeness": {
            "all_cubic_triangle_candidates_considered": True,
            "all_cubic_quartic_bubble_candidates_considered": True,
            "connected_and_1PI_required": True,
            "ordered_quartic_ghost_channels": ["direct", "exchange"],
            "scalar_and_Goldstone_candidates_retained": True,
        },
    }
    payload["inventory_sha256"] = digest({"records": inventory})
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_three_point_primary_inventory.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    for process, row in summary.items():
        print(process, row)
    print("INVENTORY_SHA256", payload["inventory_sha256"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
