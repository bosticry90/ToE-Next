"""Exact parent-tensor checks and generic doublet positivity identities.

This is intentionally not a derivation of the full 126-Hessian: the normalized
(15,2,2) fluctuation tensor has not yet been frozen. No benchmark is promoted.
"""

from itertools import combinations, product

import sympy as sp


def parity(indices):
    indices = tuple(map(int, indices))
    return (-1) ** sum(indices[i] > indices[j]
                       for i in range(len(indices))
                       for j in range(i + 1, len(indices)))


def component(form, indices):
    if len(set(indices)) != len(indices):
        return sp.Integer(0)
    return parity(indices) * form.get(tuple(sorted(indices)), sp.Integer(0))


def hodge(form):
    result = {}
    universe = set(range(1, 11))
    for idx, value in form.items():
        complement = tuple(sorted(universe.difference(idx)))
        result[complement] = sp.expand(result.get(complement, 0)
                                        + parity(idx + complement) * value)
    return result


def vacuum_form(sigma):
    # Exterior product of five mutually orthogonal complex null one-forms.
    # Its 246810 component is sigma/(4 sqrt(2)), the paper's Eq. (26).
    amplitude = sigma / (4 * sp.sqrt(2))
    result = {}
    for picks in product((0, 1), repeat=5):
        indices = tuple(2 * k + (1 if odd else 2)
                        for k, odd in enumerate(picks))
        result[tuple(sorted(indices))] = sp.expand(
            amplitude * sp.I ** sum(picks) * parity(indices))
    return result


def contraction(form, conjugate):
    # (1/4!) F_{ijklm} (F* or F)_{ijkln}; summing ordered i,j,k,l
    # is identical to summing unordered four-index subsets here.
    return sp.Matrix(10, 10, lambda m, n: sp.simplify(sum(
        component(form, idx + (m + 1,))
        * (sp.conjugate(component(form, idx + (n + 1,)))
           if conjugate else component(form, idx + (n + 1,)))
        for idx in combinations(range(1, 11), 4))))


def check_parent_tensor():
    omega, sigma = sp.symbols('omega sigma', real=True, nonzero=True)
    phi54 = sp.diag(*([-sp.Rational(2, 5) * omega] * 6
                      + [sp.Rational(3, 5) * omega] * 4))
    assert sp.trace(phi54) == 0
    assert sp.simplify(sp.trace(phi54 ** 2) / omega**2) == sp.Rational(12, 5)
    assert sp.simplify(sp.trace(phi54 ** 3) / omega**3) == sp.Rational(12, 25)
    assert sp.simplify(sp.trace(phi54 ** 4) / omega**4) == sp.Rational(84, 125)

    # These are Hessian coefficients of xi3 Phi phi phi*, eta0/2
    # tr(Phi²) phi phi*, eta2 Phi² phi phi*, and chi5 |S|² phi phi*.
    for idx, xi, eta2 in ((0, -sp.Rational(2, 5), sp.Rational(4, 25)),
                          (6, sp.Rational(3, 5), sp.Rational(9, 25))):
        assert sp.simplify(phi54[idx, idx] / omega) == xi
        assert sp.simplify(phi54[idx, idx] ** 2 / omega**2) == eta2
    assert sp.simplify(sp.trace(phi54 ** 2) / (2 * omega**2)) == sp.Rational(6, 5)

    form = vacuum_form(sigma)
    assert len(form) == 32
    assert form[(2, 4, 6, 8, 10)] == sigma / (4 * sp.sqrt(2))
    norm = sp.simplify(sum(value * sp.conjugate(value) for value in form.values()))
    assert norm == sigma**2  # (1/5!) Sigma Sigma* in full-index notation.
    dual = hodge(form)
    phases = {sp.simplify(dual[idx] / value) for idx, value in form.items()}
    assert len(phases) == 1 and next(iter(phases)) in (sp.I, -sp.I)
    assert set(dual) == set(form)

    k = contraction(form, conjugate=True)
    assert sp.simplify(sp.trace(k) / sigma**2) == 5
    assert sp.simplify(k * k - sigma**2 * k) == sp.zeros(10)
    assert all(sp.simplify(k[i, i] / sigma**2) == sp.Rational(1, 2)
               for i in range(10))
    # On the SO(4) vector block, each gamma contraction has eigenvalues
    # {0, sigma²}, with the two terms swapping the charge-sector projector.
    assert sp.simplify(k[6:10, 6:10].charpoly().as_expr()
                       - sp.Symbol('lambda')**2
                       * (sp.Symbol('lambda') - sigma**2)**2) == 0
    assert contraction(form, conjugate=False) == sp.zeros(10)

    # Literal all-index Einstein summation of Eq. (24) at the Eq. (26)
    # singlet vacuum. The source's Eq. (27) instead prints lambda0*sigma^4
    # and alpha*(3/5)*omega^2*sigma^2 using the SAME coefficient names.
    # No single rescaling N=(Sigma Sigma*)/5!=q*sigma^2 can satisfy both
    # the printed nu^2 and lambda0 terms: the former requires q=1 and
    # the latter q=2. This is a convention/source-normalization gate, not
    # by itself a proof that a physical scalar mass is wrong.
    q = sp.symbols('q', positive=True)
    assert sp.solve(sp.Eq(q / 2, sp.Rational(1, 2)), q) == [1]
    assert sp.solve(sp.Eq(q*q / 4, 1), q) == [2]
    assert sp.simplify(norm / sigma**2) == 1
    nu, lambda0 = sp.symbols('nu lambda0', real=True)
    literal_126 = -nu**2*norm/2 + lambda0*norm**2/4
    printed_126 = -nu**2*sigma**2/2 + lambda0*sigma**4
    assert sp.simplify(literal_126-printed_126) == -3*lambda0*sigma**4/4
    assert sp.simplify(sp.trace(phi54**2) / (2*omega**2)) == sp.Rational(6, 5)

    # beta/3! Phi_ij Phi_kl Sigma_mnoik Sigma*_mnojl, for diagonal Phi.
    # For each 5-form component, the ordered (i,k) sum is twice the sum
    # over unordered index pairs. Each component has three SO(6) indices
    # and two SO(4) indices, hence the same exact weight.
    betas = set()
    diagonal = [phi54[i, i] / omega for i in range(10)]
    for indices in form:
        weight = 2 * sum(diagonal[i-1] * diagonal[j-1]
                         for i, j in combinations(indices, 2))
        betas.add(sp.simplify(weight))
    assert betas == {-sp.Rational(6, 5)}

    # Canonical SO(4) vector -> pair of SU(2)L doublets. The SO(10)
    # invariant phi_i phi_i gives 2 h_u epsilon h_d. Thus, with
    # <S>=v_s/sqrt(2), the off-diagonal mass magnitude is sqrt(2) chi6 v_s.
    u1, u2, d1, d2 = sp.symbols('u1 u2 d1 d2')
    bidoublet = [(u1 + d2) / sp.sqrt(2),
                 sp.I * (u1 - d2) / sp.sqrt(2),
                 (u2 - d1) / sp.sqrt(2),
                 sp.I * (u2 + d1) / sp.sqrt(2)]
    assert sp.simplify(sum(z*z for z in bidoublet)) == 2*(u1*d2-u2*d1)
    return next(iter(phases))


def check_schur_positivity():
    a, b, c, d, e, f, g = sp.symbols('a b c d e f g', real=True)
    mat = sp.Matrix([[a, b, 0, c], [b, d, 0, 0],
                     [0, 0, e, f], [c, 0, f, g]])
    pivot = a - b*b/d
    residual = g - f*f/e - c*c/pivot
    assert sp.simplify(mat.det() - d*e*pivot*residual) == 0
    null = sp.Matrix([-c/pivot, b*c/(d*pivot), -f/e, 1])
    assert sp.simplify(mat*null).subs(g, f*f/e+c*c/pivot) == sp.zeros(4, 1)
    assert sp.simplify((null[0]/null[1]) + d/b) == 0
    assert sp.simplify(null[2] + f/e) == 0

    # Exact nondegenerate witness: one null mode and positive heavy modes.
    vals = {a: sp.Rational(21, 5), b: -1, c: 3, d: 5,
            e: 7, f: -2, g: sp.Rational(79, 28)}
    witness = mat.subs(vals)
    assert witness.det() == 0
    assert witness[:3, :3].det() > 0
    assert witness[:2, :2].det() > 0
    assert witness[0, 0] > 0
    assert witness.rank() == 3
    assert (witness * null.subs(vals)) == sp.zeros(4, 1)


if __name__ == '__main__':
    phase = check_parent_tensor()
    check_schur_positivity()
    print(f'PASS: 54/10/singlet tensor coefficients; 126 singlet norm, duality ({phase}), gamma projector')
    print('PASS: exact generic one-zero/three-positive Schur criterion and projector identities')
    print('SOURCE GATE: literal Eq. (24) and printed Eq. (27) have incompatible 126 normalizations')
    print('NOT TESTED: 126 doublet-fluctuation Clebsches; full doublet/triplet Hessians; new scalar benchmark')
