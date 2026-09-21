"""Ordered equivariant quartic-ghost vertex and closed-loop parity.

For

  (xi/2) f[a,b,A] f[c,d,A] bar_u[a] u[b] bar_u[c] u[d]

left Grassmann differentiation in the canonical external order
``bar_u[a],u[b],bar_u[c],u[d]`` gives

  xi * (f[a,b,A] f[c,d,A] - f[c,b,A] f[a,d,A]).

The two terms define direct and exchange ghost-flow channels.  The usual minus
sign per closed ghost loop is then unambiguous.
"""

from itertools import permutations


def permutation_parity(order):
    inversions = sum(order[i] > order[j] for i in range(len(order))
                     for j in range(i + 1, len(order)))
    return -1 if inversions % 2 else 1


def differentiated_terms():
    """Return the four raw assignments before structure-factor simplification."""
    canonical = ("ba", "ub", "bc", "ud")
    terms = []
    for bars in (("a", "c"), ("c", "a")):
        for ghosts in (("b", "d"), ("d", "b")):
            raw = ("b" + bars[0], "u" + ghosts[0],
                   "b" + bars[1], "u" + ghosts[1])
            order = tuple(canonical.index(item) for item in raw)
            terms.append({
                "raw_slots": list(raw),
                "grassmann_permutation_sign": permutation_parity(order),
                "structure_product": (
                    f"f[{bars[0]},{ghosts[0]},A]*"
                    f"f[{bars[1]},{ghosts[1]},A]"
                ),
                "raw_action_factor": "xi/2",
            })
    assert [row["grassmann_permutation_sign"] for row in terms] == [1, -1, -1, 1]
    return terms


def vertex_channels():
    differentiated_terms()
    return (
        {"channel": "direct", "coefficient_sign": 1,
         "color_tensor": "xi*f[a,b,A]*f[c,d,A]",
         "local_flow_pairs": (("a", "b"), ("c", "d"))},
        {"channel": "exchange", "coefficient_sign": -1,
         "color_tensor": "-xi*f[c,b,A]*f[a,d,A]",
         "local_flow_pairs": (("c", "b"), ("a", "d"))},
    )


def ghost_half_edges(topology, diagram):
    edges = [tuple(edge) for edge in topology["internal_edges"]]
    records = diagram["ordered_field_assignments"]
    output = []
    for edge_index, (edge, record) in enumerate(zip(edges, records)):
        line = record["line_assignment"]
        if not line.startswith(("U", "C")):
            continue
        base = line[0]
        anti = "ubar" if base == "U" else "cbar"
        particle = "u" if base == "U" else "c"
        a, b = edge
        if a == b or line.endswith("+"):
            roles = (anti, particle)
        else:
            roles = (particle, anti)
        output.append({
            "edge": edge_index,
            "nodes": ((edge_index, 0), (edge_index, 1)),
            "vertices": (a, b),
            "roles": roles,
            "base": base,
        })
    return output


def closed_ghost_loops(topology, diagram, quartic_channel=None):
    half_edges = ghost_half_edges(topology, diagram)
    nodes = [node for edge in half_edges for node in edge["nodes"]]
    parent = {node: node for node in nodes}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left

    by_vertex = {v: {"u": [], "ubar": [], "c": [], "cbar": []}
                 for v in range(topology["vertex_count"])}
    for edge in half_edges:
        union(*edge["nodes"])
        for node, vertex, role in zip(edge["nodes"], edge["vertices"], edge["roles"]):
            by_vertex[vertex][role].append(node)

    quartic_vertices = [i for i, vertex in enumerate(diagram["vertex_ids"])
                        if vertex == "HGH4_ubar_u_ubar_u"]
    assert len(quartic_vertices) <= 1
    quartic = quartic_vertices[0] if quartic_vertices else None
    assert (quartic is None) == (quartic_channel is None)
    for vertex, roles in by_vertex.items():
        for prefix in ("", "c"):
            particle = "u" if not prefix else "c"
            anti = "ubar" if not prefix else "cbar"
            us, bars = sorted(roles[particle]), sorted(roles[anti])
            if not us and not bars:
                continue
            if vertex == quartic and particle == "u":
                assert len(bars) == len(us) == 2
                slots = {"a": bars[0], "c": bars[1],
                         "b": us[0], "d": us[1]}
                channel = next(row for row in vertex_channels()
                               if row["channel"] == quartic_channel)
                for left, right in channel["local_flow_pairs"]:
                    union(slots[left], slots[right])
            else:
                assert len(bars) == len(us) == 1, (vertex, roles)
                union(bars[0], us[0])
    components = len({find(node) for node in nodes})
    return components
