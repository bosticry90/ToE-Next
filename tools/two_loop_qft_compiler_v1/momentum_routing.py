"""Deterministic two-loop momentum routing for a fixed topology."""

from sympy import Matrix


def route(topology):
    vertices = topology["vertex_count"]
    edges = [tuple(edge) for edge in topology["internal_edges"]]
    parent = list(range(vertices))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree, chords = [], []
    for ordinal, (a, b) in enumerate(edges):
        if a == b:
            chords.append(ordinal)
            continue
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            tree.append(ordinal)
        else:
            chords.append(ordinal)
    assert len(tree) == vertices - 1
    assert len(chords) == topology["loop_order"]

    incidence = Matrix.zeros(vertices, len(tree))
    for column, edge_index in enumerate(tree):
        a, b = edges[edge_index]
        incidence[a, column] = 1
        incidence[b, column] = -1
    reduced = incidence[:-1, :]
    assert reduced.det() in (-1, 1)

    coefficients = [[0, 0, 0] for _ in edges]
    for loop, edge_index in enumerate(chords):
        coefficients[edge_index][loop] = 1

    external = [0] * vertices
    first, second = topology["external_vertices_labelled"]
    external[first] += 1
    external[second] -= 1

    for basis in range(3):
        demand = Matrix.zeros(vertices, 1)
        if basis < len(chords):
            edge_index = chords[basis]
            a, b = edges[edge_index]
            if a != b:
                demand[a] += 1
                demand[b] -= 1
        elif basis < 2:
            continue
        else:
            for vertex, value in enumerate(external):
                demand[vertex] = value
        solution = reduced.inv() * (-demand[:-1, :])
        for column, edge_index in enumerate(tree):
            coefficients[edge_index][basis] = int(solution[column])

    # Exact conservation replay in the k,q,p coefficient basis.
    for basis in range(3):
        residual = [0] * vertices
        for edge_index, (a, b) in enumerate(edges):
            if a != b:
                residual[a] += coefficients[edge_index][basis]
                residual[b] -= coefficients[edge_index][basis]
        if basis == 2:
            residual = [x + y for x, y in zip(residual, external)]
        assert residual == [0] * vertices, (topology["topology_id"], basis, residual)
    return {
        "loop_basis": ["k", "q"][:topology["loop_order"]],
        "external_momentum": "p_in_at_leg0_minus_p_at_leg1",
        "tree_edge_ordinals": tree,
        "chord_edge_ordinals": chords,
        "edge_momentum_coefficients_k_q_p": coefficients,
    }
