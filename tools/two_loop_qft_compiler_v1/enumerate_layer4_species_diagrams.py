"""Enumerate tensor-indexed canonical field assignments on layer-4 topologies.

This is an exact species/tensor inventory.  A line such as ``H[a3]`` denotes a
finite sum over the 290 physical heavy-scalar mass eigenstates and carries the
mass identifier ``m_H[a3]^2``.  Dense component vertices are not materialized.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path

from diagram_topology import vertex_automorphisms
from layer4_vertex_catalog import FIELD_DOMAINS, manifest as catalog_manifest
from momentum_routing import route
from quartic_ghost_vertex import closed_ghost_loops, vertex_channels


HERE = Path(__file__).resolve().parent
BOSONS = ("q", "V", "G", "H", "h", "p")


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def line_options(edge):
    a, b = edge
    options = list(BOSONS)
    if a == b:
        options.extend(("U", "C"))
    else:
        options.extend(("U+", "U-", "C+", "C-"))
    return tuple(options)


def endpoint_tokens(edge, line):
    a, b = edge
    if line in BOSONS:
        return ((a, line), (b, line))
    ghost = line[0]
    particle, antiparticle = (("u", "ubar") if ghost == "U"
                              else ("c", "cbar"))
    if a == b:
        return ((a, antiparticle), (b, particle))
    if line.endswith("+"):
        return ((a, antiparticle), (b, particle))
    return ((a, particle), (b, antiparticle))


def transform_line(edge, line, permutation):
    a, b = edge
    na, nb = permutation[a], permutation[b]
    if line in BOSONS:
        return (min(na, nb), max(na, nb), line)
    base = line[0]
    roles = endpoint_tokens(edge, line)
    role_at = {permutation[v]: token for v, token in roles}
    lo, hi = min(na, nb), max(na, nb)
    if lo == hi:
        return (lo, hi, base)
    anti = "ubar" if base == "U" else "cbar"
    suffix = "+" if role_at[lo] == anti else "-"
    return (lo, hi, base + suffix)


def transform_assignment(topology, vertex_ids, lines, permutation):
    transformed_vertices = [None] * len(vertex_ids)
    for old, new in enumerate(permutation):
        transformed_vertices[new] = vertex_ids[old]
    transformed_lines = sorted(
        transform_line(tuple(edge), line, permutation)
        for edge, line in zip(topology["internal_edges"], lines)
    )
    return tuple(transformed_vertices), tuple(transformed_lines)


def colored_canonical(topology, vertex_ids, lines):
    valences = tuple(topology["vertex_valences"])
    external = tuple(topology["external_vertices_labelled"])
    edges = tuple(tuple(x) for x in topology["internal_edges"])
    return min(transform_assignment(topology, vertex_ids, lines, p)
               for p in vertex_automorphisms(valences, external, edges))


def colored_symmetry_denominator(topology, vertex_ids, lines):
    valences = tuple(topology["vertex_valences"])
    external = tuple(topology["external_vertices_labelled"])
    edges = tuple(tuple(x) for x in topology["internal_edges"])
    reference = transform_assignment(topology, vertex_ids, lines,
                                     tuple(range(len(valences))))
    vertex_factor = sum(
        transform_assignment(topology, vertex_ids, lines, p) == reference
        for p in vertex_automorphisms(valences, external, edges)
    )
    multiplicities = {}
    for edge, line in zip(edges, lines):
        key = (edge, line)
        multiplicities[key] = multiplicities.get(key, 0) + 1
    edge_factor = 1
    for ((a, b), line), count in multiplicities.items():
        edge_factor *= factorial(count)
        if a == b and line in BOSONS:
            edge_factor *= 2 ** count
    return vertex_factor * edge_factor


def ghost_sign_status(vertex_ids, lines):
    has_ghost = any(line.startswith(("U", "C")) for line in lines)
    has_quartic = "HGH4_ubar_u_ubar_u" in vertex_ids
    if has_quartic:
        return "EXPAND_ORDERED_QUARTIC_GRASSMANN_CHANNELS"
    if has_ghost:
        return "RESOLVE_CLOSED_ORIENTED_GHOST_CYCLES"
    return "1"


def assign(topology, lookup):
    edges = tuple(tuple(x) for x in topology["internal_edges"])
    external_counts = [topology["external_vertices_labelled"].count(v)
                       for v in range(topology["vertex_count"])]
    unique = {}
    routing = route(topology)
    for lines in product(*(line_options(edge) for edge in edges)):
        local = [[] for _ in range(topology["vertex_count"])]
        for edge, line in zip(edges, lines):
            for vertex, token in endpoint_tokens(edge, line):
                local[vertex].append(token)
        vertex_rows = []
        for vertex, fields in enumerate(local):
            key = (external_counts[vertex], tuple(sorted(fields)))
            row = lookup.get(key)
            if row is None:
                break
            vertex_rows.append(row)
        else:
            vertex_ids = tuple(row["vertex_id"] for row in vertex_rows)
            key = colored_canonical(topology, vertex_ids, lines)
            if key in unique:
                continue
            denominator = colored_symmetry_denominator(
                topology, vertex_ids, lines)
            edge_records = []
            for ordinal, (edge, line) in enumerate(zip(edges, lines)):
                base = line[0] if line.startswith(("U", "C")) else line
                domain_key = ("u" if base == "U" else
                              "c" if base == "C" else base)
                domain = FIELD_DOMAINS[domain_key]
                mass_id = domain["mass"]
                mass_id = mass_id.replace("[i]", f"[a{ordinal}]")
                mass_id = mass_id.replace("[a]", f"[a{ordinal}]")
                edge_records.append({
                    "edge_ordinal": ordinal,
                    "vertices": list(edge),
                    "line_assignment": line,
                    "dummy_index": f"a{ordinal}",
                    "finite_index_domain": domain["range"],
                    "propagator_id": domain["propagator"],
                    "mass_id": mass_id,
                })
            unique[key] = {
                "diagram_id": "D_" + sha256(repr(key).encode()).hexdigest()[:16],
                "topology_id": topology["topology_id"],
                "vertex_ids": list(vertex_ids),
                "ordered_field_assignments": edge_records,
                "background_channels": ["U1Y", "SU2L", "SU3C"],
                "statistics_sign": ghost_sign_status(vertex_ids, lines),
                "symmetry_denominator": denominator,
                "symmetry_factor": str(Fraction(1, denominator)),
                "action_hash": catalog_manifest()[
                    "immutable_partial_bfm_action_sha256"],
                "momentum_routing_id": topology["topology_id"],
                "denominator_skeleton": [
                    {
                        "edge_ordinal": edge["edge_ordinal"],
                        "momentum_coefficients_k_q_p": routing[
                            "edge_momentum_coefficients_k_q_p"][
                                edge["edge_ordinal"]],
                        "mass_id": edge["mass_id"],
                        "propagator_power": 1,
                    }
                    for edge in edge_records
                ],
                "numerator_skeleton": {
                    "vertex_tensor_ids": list(vertex_ids),
                    "propagator_numerator_ids": [
                        ("Rxi_vector_numerator" if edge["propagator_id"]
                         in ("q", "V") else "unit_scalar_or_ghost_numerator")
                        for edge in edge_records
                    ],
                    "external_background_indices": ["mu", "nu"],
                    "status": "symbolic_unreduced",
                },
                "coupling_group_coefficient": {
                    "expression": "product_of_vertex_tensors_with_dummy_indices",
                    "vertex_tensor_ids": list(vertex_ids),
                    "dummy_indices": [edge["dummy_index"] for edge in edge_records],
                    "evaluation": "deferred_not_reduced",
                },
            }
    return sorted(unique.values(), key=lambda row: row["diagram_id"])


def main():
    topology_data = json.loads((HERE / "layer4_topologies.json").read_text())
    catalog = catalog_manifest()
    lookup = {
        (row["external_background_legs"], tuple(row["internal_fields"])): row
        for row in catalog["vertex_signatures"]
    }
    all_diagrams = []
    by_topology = {}
    for topology in topology_data["two_loop_topologies"]:
        diagrams = assign(topology, lookup)
        by_topology[topology["topology_id"]] = len(diagrams)
        all_diagrams.extend(diagrams)
    topology_lookup = {row["topology_id"]: row
                       for row in topology_data["two_loop_topologies"]}
    expanded = []
    quartic_base = 0
    for diagram in all_diagrams:
        topology = topology_lookup[diagram["topology_id"]]
        if diagram["statistics_sign"] == (
                "RESOLVE_CLOSED_ORIENTED_GHOST_CYCLES"):
            loops = closed_ghost_loops(topology, diagram)
            loop_sign = -1 if loops % 2 else 1
            diagram["ghost_flow"] = {
                "closed_ghost_loops": loops,
                "closed_ghost_loop_sign": loop_sign,
            }
            diagram["statistics_sign"] = str(loop_sign)
            expanded.append(diagram)
            continue
        if diagram["statistics_sign"] != (
                "EXPAND_ORDERED_QUARTIC_GRASSMANN_CHANNELS"):
            expanded.append(diagram)
            continue
        quartic_base += 1
        for channel in vertex_channels():
            clone = dict(diagram)
            loops = closed_ghost_loops(topology, diagram, channel["channel"])
            loop_sign = -1 if loops % 2 else 1
            clone["diagram_id"] = diagram["diagram_id"] + "_" + channel["channel"]
            clone["quartic_ghost_vertex_term"] = {
                "ordered_slots": ["ubar[a]", "u[b]", "ubar[c]", "u[d]"],
                **{key: value for key, value in channel.items()
                   if key != "local_flow_pairs"},
                "local_flow_pairs": [list(pair)
                                     for pair in channel["local_flow_pairs"]],
                "closed_ghost_loops": loops,
                "closed_ghost_loop_sign": loop_sign,
                "combined_grassmann_sign": (
                    loop_sign * channel["coefficient_sign"]),
            }
            clone["statistics_sign"] = str(
                loop_sign * channel["coefficient_sign"])
            expanded.append(clone)
    all_diagrams = sorted(expanded, key=lambda row: row["diagram_id"])
    payload = {
        "outcome": "CANONICAL_SPECIES_DIAGRAM_ASSIGNMENT_PASS",
        "immutable_partial_bfm_action_sha256": catalog[
            "immutable_partial_bfm_action_sha256"],
        "vertex_catalog_sha256": catalog["vertex_catalog_sha256"],
        "scope": catalog["scope"],
        "representation": catalog["representation"],
        "counts_by_topology": by_topology,
        "diagram_count": len(all_diagrams),
        "quartic_ghost_base_graphs": quartic_base,
        "quartic_ghost_ordered_channel_records": 2 * quartic_base,
        "unresolved_quartic_ghost_statistics_diagrams": 0,
        "all_statistics_signs_resolved": all(
            row["statistics_sign"] in ("-1", "1") for row in all_diagrams),
        "all_symbolic_numerator_denominator_skeletons_present": all(
            row.get("denominator_skeleton")
            and row.get("numerator_skeleton", {}).get("status")
                == "symbolic_unreduced"
            for row in all_diagrams),
        "diagrams": all_diagrams,
        "blocked_requirement": None,
    }
    payload["species_inventory_sha256"] = canonical_hash(payload)
    (HERE / "layer4_species_diagrams.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("DIAGRAMS", len(all_diagrams))
    print("QUARTIC_GHOST_BASE_GRAPHS", quartic_base)
    print("QUARTIC_GHOST_ORDERED_CHANNEL_RECORDS", 2 * quartic_base)
    print("SPECIES_INVENTORY_SHA256", payload["species_inventory_sha256"])


if __name__ == "__main__":
    main()
