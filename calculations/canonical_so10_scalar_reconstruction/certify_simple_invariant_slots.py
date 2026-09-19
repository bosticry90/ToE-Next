"""Exact lower-bound witnesses for simple canonical scalar invariant slots.

The character count in count_d5_singlets.py supplies the matching upper bounds.
Only the listed 2-/3-dimensional and elementary quartic slices are certified;
this is not an enumeration of all 34 slots or a normalized parent action.
"""

from itertools import combinations

from sympy import I, Matrix, conjugate

from test_eta1_invariant import component, contraction_vector_on_a, conjugate as form_conjugate, selfdual_form


def norm_sigma(form):
    return sum(a * a + b * b for a, b in form.values())


def k_diagonal(form):
    # K_ii = (1/4!) Sigma_{i abcd} Sigma*_{i abcd}; independent 5-index
    # components containing i already include the 4! contraction factor.
    return [
        sum(a * a + b * b for idx, (a, b) in form.items() if i in idx)
        for i in range(10)
    ]


def k_entry(form, i, j):
    result = 0
    for four in combinations(range(10), 4):
        ai, bi = component(form, (i,) + four)
        aj, bj = component(form, (j,) + four)
        result += (ai + I*bi) * (aj - I*bj)
    return result


def t_entry(form, i, j):
    result = 0
    for four in combinations(range(10), 4):
        ai, bi = component(form, (i,) + four)
        aj, bj = component(form, (j,) + four)
        result += (ai + I*bi) * (aj + I*bj)
    return result


def pair_counts(form):
    return {(i, j): sum(a*a+b*b for idx, (a, b) in form.items() if i in idx and j in idx)
            for i in range(10) for j in range(i+1, 10)}


def vector_norm(v):
    return sum(conjugate(z) * z for z in v)


def vector_square(v):
    return sum(z * z for z in v)


def rank_witness(name, rows, expected):
    matrix = Matrix(rows)
    assert matrix.rank() == expected, (name, matrix)
    print(f"{name}: exact rank {expected} on {matrix.rows} witness configurations")


def main():
    s = selfdual_form()
    n = norm_sigma(s)
    k = k_diagonal(s)
    pair = pair_counts(s)
    assert n > 0 and sum(k) == 5 * n
    p1 = (1, -1, 0, 0, 0, 0, 0, 0, 0, 0)
    p2 = (1, 1, 1, -3, 0, 0, 0, 0, 0, 0)
    p3 = (2, 2, 2, 2, 2, 2, -3, -3, -3, -3)
    e0 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    e9 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
    c0 = (1, I, 0, 0, 0, 0, 0, 0, 0, 0)

    # Four quadratic and four cubic singlet-bearing multisets; their
    # representation multiplicities are exactly one each.
    one_dimensional = {
        "Phi^2 = Tr(Phi^2)": sum(x * x for x in p1),
        "Sigma Sigma* = |Sigma|^2": n,
        "phi phi* = phi^dagger phi": vector_norm(e0),
        "S S* = |S|^2": 1,
        "Phi^3 = Tr(Phi^3)": sum(x**3 for x in p2),
        "Phi phi phi* = phi^dagger Phi phi": p2[0],
        "phi^2 S* = (phi dot phi) S*": vector_square(e0),
        "phi*^2 S = conjugate(phi dot phi) S": conjugate(vector_square(e0)),
        "Phi phi^2 S* = Phi_ij phi_i phi_j S*": p2[0],
        "Phi phi*^2 S = conjugate(Phi_ij phi_i phi_j) S": p2[0],
        "Phi^2 S S* = Tr(Phi^2)|S|^2": sum(x*x for x in p1),
        "Sigma Sigma* S S* = |Sigma|^2|S|^2": n,
        "phi phi* S S* = |phi|^2|S|^2": vector_norm(e0),
        "S^2 S*^2 = |S|^4": 1,
    }
    nonzero_t = next(((i, j, t_entry(s, i, j))
                      for i in range(10) for j in range(10)
                      if t_entry(s, i, j) != 0), None)
    assert nonzero_t is not None
    ti, tj, tv = nonzero_t
    # Phi_ij can select the symmetric T_ij; if i=j, explicitly choose a
    # traceless diagonal Phi=e_ii-e_jj. The irrep count is one per slot.
    if ti == tj:
        other = next(j for j in range(10) if t_entry(s, ti, ti) != t_entry(s, j, j))
        phi_t = tv - t_entry(s, other, other)
    else:
        phi_t = 2*tv  # real symmetric Phi with Phi_ij=Phi_ji=1
    one_dimensional["Phi Sigma^2 S = Phi_ij T_ij S"] = phi_t
    one_dimensional["Phi Sigma*^2 S* = conjugate(Phi_ij T_ij S)"] = conjugate(phi_t)
    one_dimensional["Sigma^2 phi^2 = T_ij phi_i phi_j"] = tv
    one_dimensional["Sigma*^2 phi*^2 = conjugate(T_ij phi_i phi_j)"] = conjugate(tv)
    eta = contraction_vector_on_a(s, s, form_conjugate(s), 0)
    assert eta != (0, 0)
    one_dimensional["Sigma^2 Sigma* phi = I_eta"] = eta[0] + I*eta[1]
    one_dimensional["Sigma Sigma*^2 phi* = conjugate(I_eta)"] = eta[0] - I*eta[1]
    assert all(value != 0 for value in one_dimensional.values())
    print(f"single-multiplicity slots with exact nonzero contraction: {len(one_dimensional)}")

    # Two independent contractions for each listed multiplicity-two family.
    rank_witness(
        "Phi^4: (Tr Phi^2)^2, Tr Phi^4",
        [(sum(x*x for x in p)**2, sum(x**4 for x in p)) for p in (p1, p2)], 2,
    )
    rank_witness(
        "phi^2 phi*^2: (phi^dagger phi)^2, |phi dot phi|^2",
        [(vector_norm(v)**2, vector_square(v)*conjugate(vector_square(v))) for v in (e0, c0)], 2,
    )
    rank_witness(
        "Phi^2 phi phi*: Tr(Phi^2)|phi|^2, phi^dagger Phi^2 phi",
        [(sum(x*x for x in p)*vector_norm(e0), sum(p[i]**2*e0[i] for i in range(10))) for p in (p1, p2)], 2,
    )
    rank_witness(
        "Sigma Sigma* phi phi*: |Sigma|^2|phi|^2, phi^dagger K phi",
        [(n*vector_norm(v), sum(conjugate(v[i])*k_entry(s, i, j)*v[j]
                               for i in range(10) for j in range(10))) for v in (e0, c0)], 2,
    )
    rank_witness(
        "Phi^2 Sigma Sigma*: Tr(Phi^2)|Sigma|^2, Phi_ij Phi_kl Sigma_ikabc Sigma*_jlabc",
        [(sum(x*x for x in p)*n, sum(p[i]*p[j]*pair[i, j] for i in range(10) for j in range(i+1, 10)))
         for p in (p1, p3)], 2,
    )
    print(f"K diagonal = {k}; Sigma norm = {n}; nonzero T entry = {nonzero_t}; eta = {eta}")
    print("PARTIAL_EXPLICIT_BASIS_CERTIFIED: 20 + 5*2 = 30 of 34 slots")


if __name__ == "__main__":
    main()
