"""Exact eta1 Hessian slice at the canonical 126 singlet VEV.

Zero-based vector indices 0..5 span SO(6)~SU(4), 6..9 span
SO(4)~SU(2)L x SU(2)R. All arithmetic in the tensor contractions is Z[i].
"""

from itertools import product

from test_eta1_invariant import (
    TEN, ZERO, add, component, conjugate, contraction_vector_on_a, parity,
)


def vacuum_form():
    """V = wedge_(k=0..4)(e_(2k+1) + i e_(2k)); *V=+i V."""
    out = {}
    for picks in product((0, 1), repeat=5):
        indices = tuple(2 * k + (0 if pick else 1) for k, pick in enumerate(picks))
        power = sum(picks) % 4
        out[indices] = ((1, 0), (0, 1), (-1, 0), (0, -1))[power]
    return out


def doublet_form(weak):
    """P_(+i)(*6 J_U1 wedge e_weak), before canonical 1/sqrt(3)."""
    assert weak in range(6, 10)
    out = {}
    # *6(e01+e23+e45) is invariant under the color SU(3) subgroup.
    for color4 in ((2, 3, 4, 5), (0, 1, 4, 5), (0, 1, 2, 3)):
        indices = color4 + (weak,)
        out[indices] = (1, 0)
        complement = tuple(i for i in TEN if i not in indices)
        sign = parity(indices + complement)
        out[complement] = add(out.get(complement, ZERO), (0, -sign))
    return out


def norm2(form):
    return sum(a * a + b * b for a, b in form.values())


def hodge_eigencheck(form):
    from itertools import combinations

    for idx in combinations(TEN, 5):
        complement = tuple(i for i in TEN if i not in idx)
        value = component(form, idx)
        dual = component(form, complement)
        sign = parity(complement + idx)
        assert (sign * dual[0], sign * dual[1]) == (-value[1], value[0])


def bilinear_matrices():
    v = vacuum_form()
    bar_v = conjugate(v)
    assert len(v) == 32 and norm2(v) == 32
    hodge_eigencheck(v)
    basis = {a: doublet_form(a) for a in range(6, 10)}
    for e in basis.values():
        assert norm2(e) == 6
        hodge_eigencheck(e)
        # 4 SO(6) indices + 1 SO(4) index, and its self-dual partner.
        assert sum(len(set(idx) & set(range(6))) == 4 for idx in e) == 3
        assert sum(len(set(idx) & set(range(6))) == 2 for idx in e) == 3
    # In canonical kinetic normalization V_phys = sigma V/(4 sqrt(2)),
    # E_phys = E/sqrt(3), phi_n = unit vector. Scale raw coefficients by
    # sigma^2/(32 sqrt(3)) to obtain the Hessian block.
    sigma_phi = []
    barsigma_phi = []
    for a in range(6, 10):
        row_s = []
        row_bar = []
        e = basis[a]
        bar_e = conjugate(e)
        for n in range(6, 10):
            left = contraction_vector_on_a(e, v, bar_v, n)
            right = contraction_vector_on_a(v, e, bar_v, n)
            row_s.append(add(left, right))
            row_bar.append(contraction_vector_on_a(v, v, bar_e, n))
        sigma_phi.append(row_s)
        barsigma_phi.append(row_bar)
    return sigma_phi, barsigma_phi


def main():
    direct, conjugate_block = bilinear_matrices()
    from sympy import I, Matrix, eye

    matrix = Matrix(4, 4, lambda a, n: direct[a][n][0] + I * direct[a][n][1])
    j = Matrix([[0, -1, 0, 0], [1, 0, 0, 0],
                [0, 0, 0, -1], [0, 0, 1, 0]])
    assert matrix == 192 * (eye(4) + I * j)
    assert matrix.rank() == 2
    assert all(x == ZERO for row in conjugate_block for x in row)
    print("basis: SU(3)-singlet adjoint color 4-form *6(e01+e23+e45) x SO(4) vector e6..e9")
    print("raw coefficient matrices; multiply by sigma^2/(32 sqrt(3)) for canonical fields")
    print("deltaSigma x delta_phi:")
    for row in direct:
        print(row)
    print("deltaSigma* x delta_phi:")
    for row in conjugate_block:
        print(row)
    print("SO(4) projector: B=192 (I+iJ), rank=2; one T3R charge sector couples to its opposite in the vector.")
    print("Canonical doublet coefficient: 4 sqrt(3) sigma^2 per paired SU(2)L component, before eta1 coupling.")
    print("NONZERO_COMPONENT_MIXING")


if __name__ == "__main__":
    main()
