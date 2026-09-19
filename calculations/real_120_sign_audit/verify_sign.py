"""Exact parent-Spin(10) check of real-120 Pati-Salam conjugation signs.

This is a sign audit, not a fit or an RGE calculation. The construction uses
Pauli-tensor Clifford matrices, rather than the Sigma intertwiners of
arXiv:2604.04021. All matrix equalities are exact SymPy equalities.
"""

from itertools import combinations

import sympy as sp


def clifford_pairs(n: int) -> list[sp.Matrix]:
    """Hermitian generators of Euclidean Cl(2n) from Jordan-Wigner strings."""
    identity = sp.eye(2)
    pauli_x = sp.Matrix([[0, 1], [1, 0]])
    pauli_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    pauli_z = sp.diag(1, -1)
    result = []
    for k in range(n):
        for end in (pauli_x, pauli_y):
            factors = [pauli_z] * k + [end] + [identity] * (n - k - 1)
            result.append(sp.kronecker_product(*factors))
    return result


def chirality(gamma: list[sp.Matrix]) -> sp.Matrix:
    n = len(gamma) // 2
    result = sp.eye(gamma[0].rows)
    for generator in gamma:
        result *= generator
    return sp.I**n * result


def equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in left - right)


def main() -> None:
    g6 = clifford_pairs(3)
    g4 = clifford_pairs(2)
    for gamma in (g6, g4):
        unit = sp.eye(gamma[0].rows)
        for a, ga in enumerate(gamma):
            assert equal(ga.H, ga)
            for b, gb in enumerate(gamma):
                assert equal(ga * gb + gb * ga, 2 * int(a == b) * unit)

    chi6 = chirality(g6)
    chi4 = chirality(g4)
    assert equal(chi6 * chi6, sp.eye(8))
    assert equal(chi4 * chi4, sp.eye(4))
    assert equal(chi6.H, chi6)
    assert equal(chi4.H, chi4)

    # The real SO(10) 120 is Lambda^3(R^6 + R^4). Its relevant pieces are
    # Lambda^3 R^4 (SU4 singlet) and Lambda^2 R^6 x R^4 (SU4 adjoint).
    # An SO(4) Hodge dual is real, and its Clifford realization carries no i.
    triple_signs = []
    for mu in range(4):
        other = [nu for nu in range(4) if nu != mu]
        triple = g4[other[0]] * g4[other[1]] * g4[other[2]]
        target = chi4 * g4[mu]
        sign = next((s for s in (-1, 1) if equal(triple, s * target)), None)
        assert sign is not None
        triple_signs.append(sign)

    # Spin(6) = SU(4): a real bivector of R^6 acts on a chiral spinor by
    # J_ab = [gamma_a,gamma_b]/4. Restrict to the four-dimensional 4 of SU4.
    positive = [i for i in range(8) if chi6[i, i] == 1]
    assert len(positive) == 4
    generators = []
    for a, b in combinations(range(6), 2):
        jab = (g6[a] * g6[b] - g6[b] * g6[a]) / 4
        xab = jab.extract(positive, positive)
        assert equal(xab.H, -xab)
        assert sp.trace(xab) == 0
        assert xab != sp.zeros(4)
        generators.append(xab)
    assert len(generators) == 15
    flattened = [sp.Matrix(16, 1, list(x)) for x in generators]
    assert sp.Matrix.hstack(*flattened).rank() == 15

    # The three commuting parent SO6 rotation planes give the B-L direction
    # on this chiral 4: three equal quark weights and one minus-three lepton
    # weight. This also fixes the relative i in the common SO10 Yukawa map.
    x_bl = generators[0] + generators[9] + generators[14]  # (01), (23), (45)
    assert equal(x_bl, sp.I * sp.diag(1, 1, 1, -3) / 2)

    # Choose a nontrivial real 2-form F and an independent real SO(4) vector.
    # X is exactly the representation of F in the compact SU4 Lie algebra.
    weights = [2, -3, 1, 4, -2, 5, 1, -1, 3, 2, -4, 1, 2, -1, 3]
    x = sum((weight * gen for weight, gen in zip(weights, generators)), sp.zeros(4))
    assert equal(x.H, -x)
    assert equal(x.conjugate(), -x.T)

    # The Spin(4) vector is a pseudoreal (2,2). The quaternionic basis below
    # is an SU2_L x SU2_R intertwiner; its epsilon reality has plus sign.
    pauli_x = sp.Matrix([[0, 1], [1, 0]])
    pauli_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    pauli_z = sp.diag(1, -1)
    bidoublet_basis = [sp.eye(2), sp.I * pauli_x, sp.I * pauli_y, sp.I * pauli_z]
    epsilon = sp.Matrix([[0, 1], [-1, 0]])
    assert all(equal(epsilon * q.conjugate() * epsilon.inv(), q) for q in bidoublet_basis)
    h = [2, -3, 5, 7]
    q = sum((weight * basis for weight, basis in zip(h, bidoublet_basis)), sp.zeros(2))

    # Induced real structures. Under complex conjugation the SU4 adjoint
    # reverses its fundamental indices (transpose). A real Spin6 bivector is
    # anti-Hermitian, so it has one extra minus sign relative to the singlet.
    e4 = sp.kronecker_product(sp.eye(4), epsilon)
    singlet = sp.kronecker_product(sp.eye(4), q)
    adjoint = sp.kronecker_product(x, q)
    assert equal(e4 * singlet.conjugate() * e4.inv(), singlet)
    assert equal(e4 * adjoint.conjugate() * e4.inv(), -sp.kronecker_product(x.T, q))
    assert not equal(e4 * adjoint.conjugate() * e4.inv(), sp.kronecker_product(x.T, q))

    # A neutral (2,2) background has up/down entries z and z*. The singlet
    # quark coefficient is z/z*, while the adjoint quark coefficient is
    # i*z/2, i*z*/2. Hence down = -conj(up) only for the latter. The fourth
    # SU4 weight is -3 times each quark weight, the usual lepton Clebsch.
    a, b = sp.symbols("a b", real=True)
    z = a + b * sp.I
    neutral_q = sp.diag(z, sp.conjugate(z))
    assert equal(neutral_q, a * bidoublet_basis[0] + b * bidoublet_basis[3])
    singlet_up, singlet_down = neutral_q[0, 0], neutral_q[1, 1]
    adjoint_up = x_bl[0, 0] * neutral_q[0, 0]
    adjoint_down = x_bl[0, 0] * neutral_q[1, 1]
    assert singlet_down == sp.conjugate(singlet_up)
    assert sp.simplify(adjoint_down + sp.conjugate(adjoint_up)) == 0
    assert x_bl[3, 3] == -3 * x_bl[0, 0]

    # The same parent Clifford matrices give the 120 Yukawa tensor coupling:
    # Gamma_{abc}=Gamma_[a Gamma_b Gamma_c]. Both relevant branches below use
    # the very same real three-form and common coupling. The 4D triple/dual
    # relation above adds only a REAL orientation sign, not an arbitrary i.
    ten = [sp.kronecker_product(ga, sp.eye(4)) for ga in g6]
    ten += [sp.kronecker_product(chi6, gm) for gm in g4]
    assert equal(ten[0] * ten[1] * ten[6], sp.kronecker_product(g6[0] * g6[1] * chi6, g4[0]))
    assert equal(ten[7] * ten[8] * ten[9], sp.kronecker_product(chi6, g4[1] * g4[2] * g4[3]))

    # Independently construct a charge-conjugation intertwiner and check the
    # parent Yukawa bilinear C*Gamma_[ijk]. Both pieces must be nonzero in the
    # same 16 x 16 chiral sector; an arbitrary component-wise phase insertion
    # would no longer be this single real SO10 tensor contraction.
    c10 = sp.eye(32)
    for index in (1, 3, 5, 7, 9):
        c10 *= ten[index]
    assert equal(c10.T, -c10)
    for generator in ten:
        assert equal(c10 * generator * c10.inv(), -generator.T)
    chi10 = chirality(ten)
    positive10 = [i for i in range(32) if chi10[i, i] == 1]
    assert len(positive10) == 16
    negative10 = [i for i in range(32) if chi10[i, i] == -1]
    pair_sum = ten[0] * ten[1] + ten[2] * ten[3] + ten[4] * ten[5]
    for mu in range(4):
        others = [nu for nu in range(4) if nu != mu]
        # h_mu = epsilon_(mu,others) T_others is the real Hodge convention.
        ordering = [mu] + others
        inversions = sum(ordering[i] > ordering[j] for i in range(4) for j in range(i + 1, 4))
        hodge_sign = (-1) ** inversions
        singlet_parent = hodge_sign * c10
        for nu in others:
            singlet_parent *= ten[6 + nu]
        adjoint_parent = c10 * pair_sum * ten[6 + mu]
        for chirality_basis, expected in (
            (positive10, {-sp.I, 3 * sp.I}),
            (negative10, {sp.I, -3 * sp.I}),
        ):
            singlet_yukawa = singlet_parent.extract(chirality_basis, chirality_basis)
            adjoint_yukawa = adjoint_parent.extract(chirality_basis, chirality_basis)
            assert singlet_yukawa != sp.zeros(16)
            assert adjoint_yukawa != sp.zeros(16)
            assert all(
                adjoint_yukawa[i, j] == 0
                for i in range(16)
                for j in range(16)
                if singlet_yukawa[i, j] == 0
            )
            yukawa_ratios = {
                sp.simplify(adjoint_yukawa[i, j] / singlet_yukawa[i, j])
                for i in range(16)
                for j in range(16)
                if singlet_yukawa[i, j] != 0
            }
            assert yukawa_ratios == expected, (mu, yukawa_ratios, expected)

    # Basis-independent consequence for the unchanged 2024 point. This uses
    # its PRINTED q=e^{i phi}, r=r2, not a new fit or any fitted uncertainty.
    phi = -1.35108
    r2 = complex(-0.355963, 1.25289)
    q2024 = complex(sp.N(sp.cos(phi), 16), sp.N(sp.sin(phi), 16))
    modulus = abs(q2024 + r2)
    assert abs(modulus - 2) > 1

    print("SO10_120_parent_representation = REAL_THREE_FORM")
    print("clifford_generators = EXACT_PASS")
    print("SU4_adjoints_independent = 15")
    print("SU4_BL_weights = i/2 * (1, 1, 1, -3)")
    print(f"SO4_hodge_clifford_signs = {triple_signs} (all real)")
    print("parent_chiral_yukawa_adjoint_over_singlet = -i (quarks), +3i (lepton), all 4 modes")
    print("opposite_chirality_ratios = +i (quarks), -3i (lepton), all 4 modes")
    print("PS_120_singlet_conjugation_sign = +1")
    print("PS_120_adjoint_conjugation_sign = -1")
    print("relative_parent_SO10_sign = OPPOSITE")
    print(f"unchanged_2024_abs_exp_i_phi_plus_r2 = {modulus:.9f}")
    print("necessary_corrected_modulus = 2")
    print("unchanged_2024_point = FAILS_PARENT_REALITY_CONDITION")


if __name__ == "__main__":
    main()
