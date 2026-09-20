"""Exact highest-weight representatives for every SM scalar multiplicity.

Construct the 10 Cartan-weight vectors, the traceless symmetric 54, and
both Hodge eigenspaces of five-forms directly in the frozen SO(10) tensor
convention. Kernel intersections of the three simple SM raising operators
give one exact representative per irrep copy. The Hermitian kinetic norm is
then fixed separately for each parent-field sector.

This is an irrep-basis compiler only: it does not evaluate Hessian blocks.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations

from sympy import I, Matrix, conjugate, simplify, sqrt, zeros

from decompose_sm_tangent import (
    BAR_SIGMA, PHI, SIGMA, VEC, Z, adjoint_char, decompose, sm_label,
)
from test_eta1_invariant import parity


INDEX5 = tuple(combinations(range(10), 5))


def complement(idx):
    return tuple(i for i in range(10) if i not in idx)


HALF5 = tuple(idx for idx in INDEX5 if idx < complement(idx))
assert len(HALF5) == 126


def weight_vector(j, sign):
    assert j in range(5) and sign in (-1, 1)
    v = zeros(10, 1)
    v[2*j] = 1
    v[2*j+1] = -sign*I
    w = [0]*5
    w[j] = sign
    return tuple(w), v


VECTORS = tuple(weight_vector(j, sign) for j in range(5) for sign in (1, -1))


def raising(i, j):
    """Orthogonal E_{ij}: u_j^+ -> u_i^+, u_i^- -> -u_j^-."""
    assert i < j
    vi = weight_vector(i, 1)[1]
    vjbar = weight_vector(j, -1)[1]
    g = (vi*vjbar.T-vjbar*vi.T)/2
    assert g+g.T == zeros(10)
    assert g*weight_vector(j, 1)[1] == vi
    assert g*weight_vector(i, -1)[1] == -vjbar
    return g


RAISING = tuple(raising(i, j) for i, j in ((0, 1), (1, 2), (3, 4)))


def wedge(vectors):
    form = {(): 1}
    for vec in vectors:
        out = defaultdict(lambda: 0)
        for key, coefficient in form.items():
            for i in range(10):
                z = vec[i]
                if z == 0 or i in key:
                    continue
                new = tuple(sorted(key+(i,)))
                sign = (-1)**sum(old > i for old in key)
                out[new] += sign*coefficient*z
        form = {key: simplify(z) for key, z in out.items() if z != 0}
    return form


def hodge(form):
    return {idx: parity(complement(idx)+idx)*form.get(complement(idx), 0)
            for idx in INDEX5
            if form.get(complement(idx), 0) != 0}


def projected(form, eigen):
    assert eigen in (I, -I)
    star = hodge(form)
    # For *^2=-1, the projector onto eigenvalue eigen is (1+*/eigen)/2.
    out = {idx: simplify((form.get(idx, 0)+star.get(idx, 0)/eigen)/2)
           for idx in set(form) | set(star)}
    return {idx: value for idx, value in out.items() if value != 0}


def form_action(g, form):
    out = defaultdict(lambda: 0)
    for old, z in form.items():
        for slot, j in enumerate(old):
            for i in range(10):
                coefficient = g[i, j]
                if coefficient == 0 or i in old:
                    continue
                moved = old[:slot]+(i,)+old[slot+1:]
                out[tuple(sorted(moved))] += coefficient*parity(moved)*z
    return {idx: simplify(z) for idx, z in out.items() if z != 0}


def add_form(a, b, factor=1):
    out = {idx: simplify(a.get(idx, 0)+factor*b.get(idx, 0))
           for idx in set(a) | set(b)}
    return {idx: z for idx, z in out.items() if z != 0}


def add_obj(a, b, factor=1):
    if isinstance(a, dict):
        return add_form(a, b, factor)
    return a+factor*b


def scale_obj(a, factor):
    if isinstance(a, dict):
        return {idx: simplify(factor*z) for idx, z in a.items() if factor*z != 0}
    return a*factor


def coordinates(obj, sector):
    if sector == "form":
        return Matrix([obj.get(idx, 0) for idx in HALF5])
    if sector == "matrix":
        return Matrix(list(obj))
    return Matrix(obj)


def action(g, obj, sector):
    if sector == "form":
        return form_action(g, obj)
    if sector == "matrix":
        return g*obj+obj*g.T
    return g*obj


def kinetic_inner(a, b, sector):
    if sector == "form":
        return simplify(sum(conjugate(a.get(idx, 0))*b.get(idx, 0)
                            for idx in INDEX5)/2)
    if sector == "matrix":
        return simplify(sum(conjugate(x)*y for x, y in zip(a, b))/2)
    return simplify(sum(conjugate(x)*y for x, y in zip(a, b)))


def choose_independent(candidates, sector):
    if not candidates:
        return []
    mat = Matrix.hstack(*(coordinates(v, sector) for v in candidates))
    _, pivots = mat.rref()
    return [candidates[j] for j in pivots]


def form_weight_spaces(eigen):
    spaces = defaultdict(list)
    for selected in combinations(range(10), 5):
        weight = tuple(sum(VECTORS[k][0][j] for k in selected)
                       for j in range(5))
        raw = wedge([VECTORS[k][1] for k in selected])
        form = projected(raw, eigen)
        if form:
            spaces[weight].append(form)
    return {w: choose_independent(forms, "form") for w, forms in spaces.items()}


def matrix_weight_spaces():
    spaces = defaultdict(list)
    for a in range(10):
        for b in range(a, 10):
            wa, va = VECTORS[a]
            wb, vb = VECTORS[b]
            weight = tuple(x+y for x, y in zip(wa, wb))
            m = (va*vb.T+vb*va.T)/2
            spaces[weight].append(m)
    # The weight-zero symmetric space contains the invariant metric;
    # subtract one copy before taking the traceless 54.
    zero_weight = (0,)*5
    traceful = spaces[zero_weight]
    assert len(traceful) == 5
    spaces[zero_weight] = [traceful[j]-traceful[-1] for j in range(4)]
    assert all(v.trace() == 0 for vals in spaces.values() for v in vals)
    return dict(spaces)


def adjoint_weight_spaces():
    spaces = defaultdict(list)
    for a, b in combinations(range(10), 2):
        wa, va = VECTORS[a]
        wb, vb = VECTORS[b]
        weight = tuple(x+y for x, y in zip(wa, wb))
        g = va*vb.T-vb*va.T
        spaces[weight].append(g)
    return {w: choose_independent(matrices, "matrix")
            for w, matrices in spaces.items()}


def adjoint_highest_weights():
    spaces = adjoint_weight_spaces()
    assert Counter({w: len(v) for w, v in spaces.items()}) == adjoint_char()
    found = highest_weights(spaces, "matrix")
    assert Counter({label: len(v) for label, v in found.items()}) == decompose(adjoint_char())
    return found


def vector_weight_spaces():
    return {weight: [vec] for weight, vec in VECTORS}


def highest_weights(spaces, sector):
    results = defaultdict(list)
    for weight, basis in spaces.items():
        if not (weight[0] >= weight[1] >= weight[2]
                and weight[3] >= weight[4]):
            continue
        cols = []
        for obj in basis:
            pieces = [coordinates(action(g, obj, sector), sector)
                      for g in RAISING]
            cols.append(Matrix.vstack(*pieces))
        kernel = Matrix.hstack(*cols).nullspace()
        for coefficients in kernel:
            obj = scale_obj(basis[0], 0)
            for coefficient, candidate in zip(coefficients, basis):
                obj = add_obj(obj, candidate, coefficient)
            assert all(all(x == 0 for x in coordinates(action(g, obj, sector), sector))
                       for g in RAISING)
            results[sm_label(weight)].append((weight, obj))
    return dict(results)


def normalize_copies(entries, sector):
    out = []
    for weight, obj in entries:
        for _, old in out:
            obj = add_obj(obj, old, -kinetic_inner(old, obj, sector))
        norm2 = simplify(kinetic_inner(obj, obj, sector))
        assert norm2.is_positive, (weight, norm2)
        obj = scale_obj(obj, 1/sqrt(norm2))
        out.append((weight, obj))
    for j, (_, a) in enumerate(out):
        for k, (_, b) in enumerate(out):
            assert simplify(kinetic_inner(a, b, sector)-int(j == k)) == 0
    return out


@dataclass(frozen=True)
class Sector:
    name: str
    kind: str
    character: object
    spaces: object


def compile_representatives():
    sectors = (
        Sector("Phi", "matrix", PHI, matrix_weight_spaces()),
        Sector("Sigma", "form", SIGMA, form_weight_spaces(I)),
        Sector("SigmaBar", "form", BAR_SIGMA, form_weight_spaces(-I)),
        Sector("phi", "vector", VEC, vector_weight_spaces()),
        Sector("phiBar", "vector", VEC, vector_weight_spaces()),
    )
    result = defaultdict(list)
    for sector in sectors:
        assert sum(len(v) for v in sector.spaces.values()) == sum(sector.character.values())
        assert Counter({w: len(v) for w, v in sector.spaces.items()}) == sector.character
        found = highest_weights(sector.spaces, sector.kind)
        expected = decompose(sector.character)
        assert Counter({label: len(v) for label, v in found.items()}) == expected, (
            sector.name, found, expected)
        for label, entries in found.items():
            for weight, obj in normalize_copies(entries, sector.kind):
                result[label].append((sector.name, weight, obj))
    result[(0, 0, 0, 0)].extend((name, Z, Matrix([1]))
                                 for name in ("S", "SBar"))
    expected_total = Counter()
    for char in (PHI, SIGMA, BAR_SIGMA, VEC, VEC, Counter({Z: 2})):
        expected_total.update(decompose(char))
    assert Counter({label: len(v) for label, v in result.items()}) == expected_total
    return dict(result)


def main():
    reps = compile_representatives()
    print("EXACT_SM_HIGHEST_WEIGHT_REPRESENTATIVES_PASS")
    print("irrep classes:", len(reps), "multiplicity directions:", sum(map(len, reps.values())))
    for label in sorted(reps):
        print(label, [(sector, weight) for sector, weight, _ in reps[label]])


if __name__ == "__main__":
    main()
