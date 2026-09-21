"""Independent recursive replay of the complete layer-4 species inventory."""

from itertools import permutations
from math import factorial
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BOSONS = ("q", "V", "G", "H", "h", "p")


def line_options(edge):
    return BOSONS + (("U", "C") if edge[0] == edge[1]
                     else ("U+", "U-", "C+", "C-"))


def endpoints(edge, line):
    a, b = edge
    if line in BOSONS:
        return ((a, line), (b, line))
    particle, anti = (("u", "ubar") if line[0] == "U" else ("c", "cbar"))
    if a == b or line.endswith("+"):
        return ((a, anti), (b, particle))
    return ((a, particle), (b, anti))


def transform_topology(topology, permutation):
    valences = [0] * topology["vertex_count"]
    for old, new in enumerate(permutation):
        valences[new] = topology["vertex_valences"][old]
    external = tuple(permutation[v]
                     for v in topology["external_vertices_labelled"])
    edges = tuple(sorted((min(permutation[a], permutation[b]),
                          max(permutation[a], permutation[b]))
                         for a, b in topology["internal_edges"]))
    return tuple(valences), external, edges


def automorphisms(topology):
    identity = (tuple(topology["vertex_valences"]),
                tuple(topology["external_vertices_labelled"]),
                tuple(tuple(x) for x in topology["internal_edges"]))
    return [p for p in permutations(range(topology["vertex_count"]))
            if transform_topology(topology, p) == identity]


def transformed_assignment(topology, vertices, lines, permutation):
    output_vertices = [None] * len(vertices)
    for old, new in enumerate(permutation):
        output_vertices[new] = vertices[old]
    output_lines = []
    for (a, b), line in zip(topology["internal_edges"], lines):
        na, nb = permutation[a], permutation[b]
        if line in BOSONS:
            normalized = line
        elif na == nb:
            normalized = line[0]
        else:
            roles = {permutation[v]: token for v, token in endpoints((a, b), line)}
            anti = "ubar" if line[0] == "U" else "cbar"
            normalized = line[0] + ("+" if roles[min(na, nb)] == anti else "-")
        output_lines.append((min(na, nb), max(na, nb), normalized))
    return tuple(output_vertices), tuple(sorted(output_lines))


def canonical(topology, vertices, lines):
    return min(transformed_assignment(topology, vertices, lines, p)
               for p in automorphisms(topology))


def enumerate_recursive(topology, lookup):
    edges = [tuple(edge) for edge in topology["internal_edges"]]
    ext = [topology["external_vertices_labelled"].count(v)
           for v in range(topology["vertex_count"])]
    found = set()

    def visit(ordinal, chosen, local):
        if ordinal == len(edges):
            vertices = []
            for vertex, fields in enumerate(local):
                row = lookup.get((ext[vertex], tuple(sorted(fields))))
                if row is None:
                    return
                vertices.append(row["vertex_id"])
            found.add(canonical(topology, tuple(vertices), tuple(chosen)))
            return
        edge = edges[ordinal]
        for line in line_options(edge):
            additions = endpoints(edge, line)
            for vertex, token in additions:
                local[vertex].append(token)
            visit(ordinal + 1, chosen + [line], local)
            for vertex, _token in reversed(additions):
                local[vertex].pop()

    visit(0, [], [[] for _ in range(topology["vertex_count"])])
    return found


def symmetry_denominator(topology, vertices, lines):
    reference = transformed_assignment(
        topology, vertices, lines, tuple(range(topology["vertex_count"])))
    vertex_factor = sum(transformed_assignment(topology, vertices, lines, p)
                        == reference for p in automorphisms(topology))
    counts = {}
    for edge, line in zip(topology["internal_edges"], lines):
        key = (tuple(edge), line)
        counts[key] = counts.get(key, 0) + 1
    edge_factor = 1
    for ((a, b), line), count in counts.items():
        edge_factor *= factorial(count)
        if a == b and line in BOSONS:
            edge_factor *= 2 ** count
    return vertex_factor * edge_factor


def independent_ghost_sign(topology, row):
    lines = [edge["line_assignment"]
             for edge in row["ordered_field_assignments"]]
    ghost_edges = []
    for ordinal, ((a, b), line) in enumerate(zip(topology["internal_edges"], lines)):
        if not line.startswith(("U", "C")):
            continue
        base = line[0]
        particle, anti = (("u", "ubar") if base == "U" else ("c", "cbar"))
        roles = ((anti, particle) if a == b or line.endswith("+")
                 else (particle, anti))
        ghost_edges.append((ordinal, (a, b), roles, base))
    if not ghost_edges:
        return "1"
    nodes = [(edge, side) for edge, _vertices, _roles, _base in ghost_edges
             for side in (0, 1)]
    parent = {node: node for node in nodes}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    local = {v: {"u": [], "ubar": [], "c": [], "cbar": []}
             for v in range(topology["vertex_count"])}
    for edge, vertices, roles, _base in ghost_edges:
        union((edge, 0), (edge, 1))
        for side, (vertex, role) in enumerate(zip(vertices, roles)):
            local[vertex][role].append((edge, side))
    quartic = next((i for i, vertex in enumerate(row["vertex_ids"])
                     if vertex == "HGH4_ubar_u_ubar_u"), None)
    channel = row.get("quartic_ghost_vertex_term", {}).get("channel")
    assert (quartic is None) == (channel is None)
    for vertex, roles in local.items():
        for particle, anti in (("u", "ubar"), ("c", "cbar")):
            us, bars = sorted(roles[particle]), sorted(roles[anti])
            if not us and not bars:
                continue
            if vertex == quartic and particle == "u":
                slots = {"a": bars[0], "c": bars[1],
                         "b": us[0], "d": us[1]}
                pairs = (("a", "b"), ("c", "d")) if channel == "direct" else (
                    ("c", "b"), ("a", "d"))
                for left, right in pairs:
                    union(slots[left], slots[right])
            else:
                assert len(us) == len(bars) == 1
                union(us[0], bars[0])
    loops = len({find(node) for node in nodes})
    coefficient_sign = (-1 if channel == "exchange" else 1)
    return str(((-1) ** loops) * coefficient_sign)


def main():
    topology_data = json.loads((HERE / "layer4_topologies.json").read_text())
    catalog = json.loads((HERE / "layer4_vertex_catalog.json").read_text())
    primary = json.loads((HERE / "layer4_species_diagrams.json").read_text())
    lookup = {(row["external_background_legs"], tuple(row["internal_fields"])): row
              for row in catalog["vertex_signatures"]}
    topologies = {row["topology_id"]: row
                  for row in topology_data["two_loop_topologies"]}

    expected = set()
    base_count = 0
    for topology in topologies.values():
        base = enumerate_recursive(topology, lookup)
        base_count += len(base)
        for key in base:
            channels = (("direct", "exchange")
                        if "HGH4_ubar_u_ubar_u" in key[0] else (None,))
            expected.update((topology["topology_id"], key, channel)
                            for channel in channels)

    observed = set()
    max_symmetry_residual = 0
    statistics_sign_mismatches = 0
    for row in primary["diagrams"]:
        topology = topologies[row["topology_id"]]
        lines = tuple(edge["line_assignment"]
                      for edge in row["ordered_field_assignments"])
        key = canonical(topology, tuple(row["vertex_ids"]), lines)
        channel = row.get("quartic_ghost_vertex_term", {}).get("channel")
        observed.add((row["topology_id"], key, channel))
        denominator = symmetry_denominator(
            topology, tuple(row["vertex_ids"]), lines)
        max_symmetry_residual = max(
            max_symmetry_residual, abs(denominator-row["symmetry_denominator"]))
        statistics_sign_mismatches += (
            independent_ghost_sign(topology, row) != row["statistics_sign"])
    assert observed == expected, (len(observed), len(expected),
                                  len(observed-expected), len(expected-observed))
    assert max_symmetry_residual == 0
    assert statistics_sign_mismatches == 0
    assert base_count == 1896 and len(expected) == 1900

    payload = {
        "outcome": "INDEPENDENT_CANONICAL_SPECIES_ENUMERATION_PASS",
        "representation": "recursive_edge_assignment_with_independent_canonicalization",
        "base_species_graphs": base_count,
        "ordered_quartic_ghost_channel_records": len(expected)-base_count+4,
        "final_records": len(expected),
        "set_difference_primary_minus_replay": 0,
        "set_difference_replay_minus_primary": 0,
        "maximum_symmetry_denominator_residual": max_symmetry_residual,
        "statistics_sign_mismatches": statistics_sign_mismatches,
        "imports_primary_species_enumerator": False,
    }
    (HERE / "layer4_species_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("BASE_SPECIES_GRAPHS", base_count)
    print("FINAL_RECORDS", len(expected))
    print("MAX_SYMMETRY_DENOMINATOR_RESIDUAL", max_symmetry_residual)


if __name__ == "__main__":
    main()
