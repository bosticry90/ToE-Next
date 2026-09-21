"""Model-independent 1PI two-point topology generation.

Vertices have valence three or four and the two external background legs are
labelled.  Internal self-loops and parallel edges are retained.  The canonical
form fixes the external legs and quotients only by internal-vertex relabelling.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
import json

def _edge_degrees(edges, vertices):
    degrees = [0] * vertices
    for a, b in edges:
        if a == b:
            degrees[a] += 2
        else:
            degrees[a] += 1
            degrees[b] += 1
    return tuple(degrees)


def _connected_and_one_particle_irreducible(edges, vertices):
    def connected(removed=None):
        adjacency = [set() for _ in range(vertices)]
        for index, (a, b) in enumerate(edges):
            if index == removed or a == b:
                continue
            adjacency[a].add(b)
            adjacency[b].add(a)
        seen, pending = {0}, [0]
        while pending:
            current = pending.pop()
            for neighbor in adjacency[current] - seen:
                seen.add(neighbor)
                pending.append(neighbor)
        return len(seen) == vertices

    if not connected():
        return False
    return all(a == b or connected(index)
               for index, (a, b) in enumerate(edges))


def _transform(valences, external_vertices, edges, permutation):
    transformed_edges = tuple(sorted(
        (min(permutation[a], permutation[b]), max(permutation[a], permutation[b]))
        for a, b in edges
    ))
    transformed_valences = [0] * len(valences)
    for old, new in enumerate(permutation):
        transformed_valences[new] = valences[old]
    transformed_external = tuple(permutation[v] for v in external_vertices)
    return (tuple(transformed_valences), transformed_external, transformed_edges)


def canonical_form(valences, external_vertices, edges):
    vertices = len(valences)
    candidates = [_transform(valences, external_vertices, edges, p)
                  for p in permutations(range(vertices))]
    return min(candidates)


def vertex_automorphisms(valences, external_vertices, edges):
    identity = (tuple(valences), tuple(external_vertices), tuple(sorted(edges)))
    return [p for p in permutations(range(len(valences)))
            if _transform(valences, external_vertices, edges, p) == identity]


def symmetry_denominator(valences, external_vertices, edges):
    """Automorphisms including identical parallel edges and loop flips."""
    vertex_factor = len(vertex_automorphisms(valences, external_vertices, edges))
    multiplicities = {}
    for edge in edges:
        multiplicities[edge] = multiplicities.get(edge, 0) + 1
    edge_factor = 1
    for (a, b), count in multiplicities.items():
        for value in range(2, count + 1):
            edge_factor *= value
        if a == b:
            edge_factor *= 2 ** count
    return vertex_factor * edge_factor


def topology_id(loop_order, canonical):
    packed = json.dumps([loop_order, canonical], separators=(",", ":"))
    return "L%d_%s" % (loop_order, sha256(packed.encode()).hexdigest()[:12])


def enumerate_two_point_topologies(loop_order):
    """Enumerate connected 1PI two-point topologies at one or two loops."""
    if loop_order == 1:
        valence_multisets = ((3, 3), (4,))
    elif loop_order == 2:
        valence_multisets = ((3, 3, 3, 3), (4, 3, 3), (4, 4))
    else:
        raise ValueError(loop_order)

    unique = {}
    for valences in valence_multisets:
        vertices = len(valences)
        internal_edges = vertices + loop_order - 1
        pair_types = tuple((a, b) for a in range(vertices)
                           for b in range(a, vertices))
        for external_vertices in product(range(vertices), repeat=2):
            external_counts = [external_vertices.count(v)
                               for v in range(vertices)]
            wanted = tuple(valences[v] - external_counts[v]
                           for v in range(vertices))
            if min(wanted) < 0 or sum(wanted) != 2 * internal_edges:
                continue
            for edges in combinations_with_replacement(pair_types,
                                                       internal_edges):
                if _edge_degrees(edges, vertices) != wanted:
                    continue
                if not _connected_and_one_particle_irreducible(edges, vertices):
                    continue
                canonical = canonical_form(valences, external_vertices, edges)
                if canonical in unique:
                    continue
                cv, ce, ci = canonical
                denominator = symmetry_denominator(cv, ce, ci)
                unique[canonical] = {
                    "topology_id": topology_id(loop_order, canonical),
                    "loop_order": loop_order,
                    "vertex_valences": list(cv),
                    "external_vertices_labelled": list(ce),
                    "internal_edges": [list(edge) for edge in ci],
                    "internal_propagators": len(ci),
                    "vertex_count": len(cv),
                    "vertex_automorphism_count": len(vertex_automorphisms(
                        cv, ce, ci)),
                    "uncolored_symmetry_denominator": denominator,
                    "uncolored_symmetry_factor": str(Fraction(1, denominator)),
                }
    return sorted(unique.values(), key=lambda row: row["topology_id"])


def validate_topology(record):
    valences = tuple(record["vertex_valences"])
    external = tuple(record["external_vertices_labelled"])
    edges = tuple(tuple(edge) for edge in record["internal_edges"])
    loops = len(edges) - len(valences) + 1
    assert loops == record["loop_order"]
    assert _edge_degrees(edges, len(valences)) == tuple(
        valences[v] - external.count(v) for v in range(len(valences)))
    assert _connected_and_one_particle_irreducible(edges, len(valences))
    assert canonical_form(valences, external, edges) == (valences, external, edges)
    assert symmetry_denominator(valences, external, edges) == (
        record["uncolored_symmetry_denominator"])
