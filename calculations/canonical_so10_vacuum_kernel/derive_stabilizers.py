"""Exact Lie-algebra stabilizers of canonical 54 and 126 vacuum tensors."""

import sys
from itertools import combinations
from pathlib import Path

from sympy import Matrix, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from test_eta1_invariant import add, parity
from verify_eta1_doublet_mixing import vacuum_form


def generators():
    result = []
    for a, b in combinations(range(10), 2):
        g = zeros(10)
        g[a, b] = 1
        g[b, a] = -1
        result.append(((a, b), g))
    return result


def form_action(g, form):
    out = {}
    for old, z in form.items():
        for slot, j in enumerate(old):
            for i in range(10):
                coefficient = g[i, j]
                if coefficient == 0 or i in old:
                    continue
                moved = old[:slot] + (i,) + old[slot+1:]
                key = tuple(sorted(moved))
                sign = int(coefficient) * parity(moved)
                val = (sign*z[0], sign*z[1])
                out[key] = add(out.get(key, (0, 0)), val)
    return {key: z for key, z in out.items() if z != (0, 0)}


def phase_complex_structure(pairs):
    j = zeros(10)
    for even, odd in pairs:
        j[even, odd] = -1
        j[odd, even] = 1
    return j


def form_column(form):
    idxs = tuple(combinations(range(10), 5))
    return [form.get(idx, (0, 0))[0] for idx in idxs] + [
        form.get(idx, (0, 0))[1] for idx in idxs]


def main():
    gens = generators()
    phi = Matrix.diag(*([-2]*6 + [3]*4))
    v = vacuum_form()
    # The 54 adjoint orbit has the expected 24 directions.
    phi_columns = [list(g*phi-phi*g) for _, g in gens]
    phi_orbit = Matrix.hstack(*[Matrix(c) for c in phi_columns])
    assert phi_orbit.rank() == 24
    h0 = [(name, g) for name, g in gens
          if all(x == 0 for x in g*phi-phi*g)]
    assert len(h0) == 21

    v_columns = [Matrix(form_column(form_action(g, v))) for _, g in h0]
    v_orbit = Matrix.hstack(*v_columns)
    assert v_orbit.rank() == 9
    sm_vectors = v_orbit.nullspace()
    assert len(sm_vectors) == 12
    sm_generators = [sum((vector[i]*h0[i][1] for i in range(21)), zeros(10))
                     for vector in sm_vectors]

    jc = phase_complex_structure(((0, 1), (2, 3), (4, 5)))
    jw = phase_complex_structure(((6, 7), (8, 9)))
    assert form_action(2*jc-3*jw, v) == {}
    # SO(6) x SO(4) centralizer of Jc,Jw is U(3) x U(2), dimension 13.
    centralizer = Matrix.hstack(*[
        Matrix(list(g*jc-jc*g) + list(g*jw-jw*g)) for _, g in h0])
    assert len(centralizer.nullspace()) == 13
    # Its exact-vacuum kernel has one determinant-phase constraint.
    nullcols = [v_orbit*vector for vector in centralizer.nullspace()]
    assert Matrix.hstack(*nullcols).rank() == 1

    # No additional SM-singlet direction exists in the real 54 or complex
    # 10: compute exact fixed-subspace dimensions of their representations.
    vector_constraint = Matrix.vstack(*sm_generators)
    assert vector_constraint.rank() == 10
    basis54 = []
    for i in range(9):
        p = zeros(10)
        p[i, i], p[9, 9] = 1, -1
        basis54.append(p)
    for i, j in combinations(range(10), 2):
        p = zeros(10)
        p[i, j] = p[j, i] = 1
        basis54.append(p)
    assert len(basis54) == 54
    fixed54 = Matrix.vstack(*[
        Matrix.hstack(*[Matrix(list(g*p-p*g)) for p in basis54])
        for g in sm_generators])
    assert fixed54.rank() == 53

    # Disconnected PS D representative: a reflection in each orthogonal
    # block has determinant +1 overall. It keeps Phi but not Sigma.
    reflected = {idx: ((-1 if ((0 in idx) != (6 in idx)) else 1)*z[0],
                       (-1 if ((0 in idx) != (6 in idx)) else 1)*z[1])
                 for idx, z in v.items()}
    assert reflected != v and reflected != {idx: (-z[0], -z[1]) for idx, z in v.items()}

    print("dim Spin(10)=45; 54 stabilizer Lie dimension=21; first-stage orbit=24")
    print("126 restriction rank within PS=9; combined stabilizer Lie dimension=12; total gauge orbit=33")
    print("centralizer(Jc,Jw)=u(3)+u(2), dimension=13; V phase condition rank=1")
    print("SM fixed subspaces: real 54 dimension=1; complex 10 dimension=0")
    print("unbroken abelian generator 2 Jc - 3 Jw annihilates V")
    print("disconnected PS D representative keeps Phi and moves V")
    print("CONNECTED_STABILIZERS_PASS: su(4)+su(2)L+su(2)R -> su(3)+su(2)+u(1)")


if __name__ == "__main__":
    main()
