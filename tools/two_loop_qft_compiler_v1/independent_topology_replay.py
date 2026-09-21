"""Independent half-edge replay of the model-independent topology inventory."""

from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pairings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1:]
        for tail in pairings(rest):
            yield ((first, second),) + tail


def normalized_edges(matching):
    return tuple(sorted((min(a[0], b[0]), max(a[0], b[0]))
                        for a, b in matching))


def connected_1pi(edges, vertices):
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

    return connected() and all(a == b or connected(index)
                               for index, (a, b) in enumerate(edges))


def transform(valences, external, edges, p):
    transformed_valences = [0] * len(valences)
    for old, new in enumerate(p):
        transformed_valences[new] = valences[old]
    transformed_external = tuple(p[v] for v in external)
    transformed_edges = tuple(sorted(
        (min(p[a], p[b]), max(p[a], p[b])) for a, b in edges))
    return tuple(transformed_valences), transformed_external, transformed_edges


def canonical(valences, external, edges):
    return min(transform(valences, external, edges, p)
               for p in permutations(range(len(valences))))


def independent_inventory(loop_order):
    multisets = (((3, 3), (4,)) if loop_order == 1 else
                 ((3, 3, 3, 3), (4, 3, 3), (4, 4)))
    output = set()
    for valences in multisets:
        vertices = len(valences)
        for external in product(range(vertices), repeat=2):
            ext_counts = [external.count(v) for v in range(vertices)]
            counts = [valences[v] - ext_counts[v] for v in range(vertices)]
            if min(counts) < 0 or sum(counts) != 2 * (vertices + loop_order - 1):
                continue
            half_edges = tuple((v, slot) for v, count in enumerate(counts)
                               for slot in range(count))
            for matching in pairings(half_edges):
                edges = normalized_edges(matching)
                if connected_1pi(edges, vertices):
                    output.add(canonical(valences, external, edges))
    return output


def main():
    primary = json.loads((HERE / "layer4_topologies.json").read_text())
    for loop_order, key in ((1, "one_loop_topologies"),
                            (2, "two_loop_topologies")):
        expected = {
            (tuple(row["vertex_valences"]),
             tuple(row["external_vertices_labelled"]),
             tuple(tuple(edge) for edge in row["internal_edges"]))
            for row in primary[key]
        }
        observed = independent_inventory(loop_order)
        assert observed == expected, (loop_order, observed - expected,
                                      expected - observed)
    result = {
        "outcome": "INDEPENDENT_TOPOLOGY_REPLAY_PASS",
        "one_loop_topologies": len(independent_inventory(1)),
        "two_loop_topologies": len(independent_inventory(2)),
        "imports_primary_topology_generator": False,
        "representation": "recursive_labelled_half_edge_pairings",
    }
    (HERE / "layer4_topology_independent_replay.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["outcome"])
    print("ONE_LOOP_TOPOLOGIES", result["one_loop_topologies"])
    print("TWO_LOOP_TOPOLOGIES", result["two_loop_topologies"])


if __name__ == "__main__":
    main()
