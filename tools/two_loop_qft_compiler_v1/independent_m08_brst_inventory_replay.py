"""Inventory-independent template/CSP replay of the M08 one-loop graphs.

Unlike the primary half-edge generator, this replay begins from the two
abstract one-loop three-point templates (triangle and double-edge bubble),
assigns external legs to template vertices, and solves propagator constraints
around each template.  The vertex signatures are reconstructed locally from
the immutable action terms and are not imported from the primary catalog.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path


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


def signatures():
    # Reconstructed independently from the displayed immutable action.
    cubic = {
        "HGH_ubar_u_V": ("ubar_H", "u_H", "V_H"),
        "HGH_ubar_u_q": ("ubar_H", "u_H", "q_L"),
        "LGH_cbar_c_q": ("cbar_L", "c_L", "q_L"),
        "YM_V_V_V": ("V_H", "V_H", "V_H"),
        "YM_q_V_V": ("q_L", "V_H", "V_H"),
        "YM_q_q_q": ("q_L", "q_L", "q_L"),
        "HGH_ubar_u_G": ("ubar_H", "u_H", "G_H"),
        "HGH_ubar_u_S": ("ubar_H", "u_H", "S_phys"),
        "KIN_q_G_G": ("q_L", "G_H", "G_H"),
        "KIN_V_G_G": ("V_H", "G_H", "G_H"),
        "KIN_q_S_S": ("q_L", "S_phys", "S_phys"),
        "KIN_V_S_S": ("V_H", "S_phys", "S_phys"),
    }
    quartic = {
        "HGH4_ubar_u_V_V": ("ubar_H", "u_H", "V_H", "V_H"),
        "HGH4_ubar_u_V_q": ("ubar_H", "u_H", "V_H", "q_L"),
        "HGH4_ubar_u_q_q": ("ubar_H", "u_H", "q_L", "q_L"),
        "HGH4_ubar_u_ubar_u": ("ubar_H", "u_H", "ubar_H", "u_H"),
    }
    return cubic, quartic


def remove_one(fields, value):
    fields = list(fields)
    try:
        fields.remove(value)
    except ValueError:
        return None
    return tuple(fields)


def compatible(left, right):
    return PAIR[left] == right


def triangle_key(nodes, edges):
    # Canonicalize the cyclic template under D3 without using the primary
    # incidence graph or its labels.
    variants = []
    for start in range(3):
        for direction in (1, -1):
            order = [(start + direction * step) % 3 for step in range(3)]
            node_rows = tuple(nodes[index] for index in order)
            edge_rows = []
            for step in range(3):
                a = order[step]
                b = order[(step + 1) % 3]
                edge = edges[tuple(sorted((a, b)))]
                edge_rows.append(tuple(sorted(edge)))
            variants.append(repr(("triangle", node_rows, tuple(edge_rows))))
    return min(variants)


def bubble_key(cubic_node, quartic_node, edge_rows, channel):
    return repr(("bubble", cubic_node, quartic_node,
                 tuple(sorted(tuple(sorted(row)) for row in edge_rows)),
                 channel))


def classify(vertex_ids):
    if "HGH4_ubar_u_ubar_u" in vertex_ids:
        return "equivariant_quartic_ghost_bubble"
    if len(vertex_ids) == 2:
        return "seagull_cubic_swordfish"
    if any(value.startswith("KIN_") for value in vertex_ids):
        return "scalar_or_Goldstone_triangle"
    ghost_count = sum(value.startswith(("HGH_", "LGH_"))
                      for value in vertex_ids)
    return ("ghost_vector_triangle" if ghost_count == 3
            else "one_ghost_two_vector_triangle")


def build():
    cubic, quartic = signatures()
    output = {}
    for process, target in TARGETS.items():
        found = {}
        # Triangle: one external leg at each cubic node.
        for vids in product(cubic, repeat=3):
            for external_order in permutations(target):
                remaining = [remove_one(cubic[vids[n]], external_order[n])
                             for n in range(3)]
                if any(value is None for value in remaining):
                    continue
                for orientations in product((0, 1), repeat=3):
                    ends = [row if orientations[n] == 0 else row[::-1]
                            for n, row in enumerate(remaining)]
                    # Node n endpoint 1 joins node n+1 endpoint 0.
                    if not all(compatible(ends[n][1], ends[(n + 1) % 3][0])
                               for n in range(3)):
                        continue
                    nodes = tuple((vids[n], external_order[n])
                                  for n in range(3))
                    edges = {
                        tuple(sorted((n, (n + 1) % 3))):
                            (ends[n][1], ends[(n + 1) % 3][0])
                        for n in range(3)
                    }
                    key = triangle_key(nodes, edges)
                    found[key] = {
                        "topology": classify(vids),
                        "vertex_ids": sorted(vids),
                        "quartic_ghost_channel": None,
                        "power_counted_zero": sum(
                            value in ("HGH_ubar_u_G", "HGH_ubar_u_S")
                            for value in vids) >= 2,
                    }

        # Double-edge bubble: cubic gets one external, quartic gets two.
        for cvid, cfields in cubic.items():
            for qvid, qfields in quartic.items():
                for cubic_external_index, cubic_external in enumerate(target):
                    crem = remove_one(cfields, cubic_external)
                    if crem is None:
                        continue
                    qexternals = tuple(value for index, value in enumerate(target)
                                       if index != cubic_external_index)
                    qrem = tuple(qfields)
                    valid = True
                    for value in qexternals:
                        qrem = remove_one(qrem, value)
                        if qrem is None:
                            valid = False
                            break
                    if not valid:
                        continue
                    for qorder in (qrem, qrem[::-1]):
                        if not (compatible(crem[0], qorder[0])
                                and compatible(crem[1], qorder[1])):
                            continue
                        channels = ("direct", "exchange") if qvid == (
                            "HGH4_ubar_u_ubar_u") else (None,)
                        for channel in channels:
                            key = bubble_key(
                                (cvid, cubic_external),
                                (qvid, tuple(sorted(qexternals))),
                                ((crem[0], qorder[0]),
                                 (crem[1], qorder[1])), channel)
                            found[key] = {
                                "topology": classify((cvid, qvid)),
                                "vertex_ids": sorted((cvid, qvid)),
                                "quartic_ghost_channel": channel,
                                "power_counted_zero": False,
                            }
        records = sorted(found.values(), key=lambda row: (
            row["topology"], row["vertex_ids"],
            str(row["quartic_ghost_channel"])))
        output[process] = records
    return output


def main():
    action = json.loads((HERE / "partial_bfm_action.json").read_text())
    records = build()
    summary = {}
    for process, rows in records.items():
        counts = Counter(row["topology"] for row in rows)
        summary[process] = {
            "canonical_records": len(rows),
            "requires_UV_evaluation": sum(not row["power_counted_zero"]
                                          for row in rows),
            "power_counted_zero": sum(row["power_counted_zero"]
                                      for row in rows),
            "topology_counts": dict(sorted(counts.items())),
        }
    payload = {
        "schema_version": 1,
        "outcome": "M08_BRST_INVENTORY_INDEPENDENT_REPLAY_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action[
            "partial_bfm_action_sha256"],
        "method": (
            "independent_triangle_and_double_edge_template_constraint_solver"
        ),
        "primary_inventory_imported": False,
        "primary_canonical_labels_imported": False,
        "summary": summary,
        "records": records,
    }
    payload["inventory_sha256"] = digest(records)
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_inventory_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    for process, row in summary.items():
        print(process, row)
    print("INVENTORY_SHA256", payload["inventory_sha256"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
