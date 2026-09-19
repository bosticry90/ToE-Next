"""Exact fail-fast checks for the admitted Babu--Khan flavor-kernel attempt.

This does not claim to compute the full Pati--Salam Yukawa beta functions.
"""

from fractions import Fraction as Q
from itertools import combinations

from sympy import Matrix, Rational, symbols, simplify


def gauge_terms():
    c4 = Q(4 * 4 - 1, 2 * 4)
    c2 = Q(2 * 2 - 1, 2 * 2)
    # Luo--Wang--Xiao (2003), one-loop -3 g^2 {C2(F), Y^a}.
    dirac = (3 * (c4 + c4), 3 * c2, 3 * c2)
    left = (3 * (c4 + c4), 3 * (c2 + c2), Q(0))
    right = (3 * (c4 + c4), Q(0), 3 * (c2 + c2))
    assert dirac == (Q(45, 4), Q(9, 4), Q(9, 4))
    assert left == (Q(45, 4), Q(9, 2), Q(0))
    assert right == (Q(45, 4), Q(0), Q(9, 2))
    # Dirac and right-handed terms reproduce Meloni--Ohlsson--Riad (86)--(88).
    assert dirac[0] == Q(9, 4) * 5
    assert right[2] == Q(9, 4) * 2
    return dirac, left, right


def projector_identity():
    a, b, c, d, e, f, g, r, s, t = symbols(
        "a b c d e f g r s t", real=True, nonzero=True
    )
    D = Matrix([[a, b, 0, e], [b, c, 0, 0], [0, 0, d, f], [e, 0, f, g]])
    # beta_h = 1 and beta_H = t; Babu--Khan's r and s then require:
    v = Matrix([r * s * t, t, r, 1])
    enforced = {
        c: -b * r * s,
        f: -d * r,
        g: d * r**2 - e * r * s * t,
        a: -(b * t + e) / (r * s * t),
    }
    assert all(simplify(x.subs(enforced)) == 0 for x in D * v)
    corrected = e**2 / (g - r**2 * d) - b / (r * s)
    published = e**2 / (g - r**2 * d) - b / s
    assert simplify((a - corrected).subs(enforced)) == 0
    assert simplify((a - published).subs(enforced)) != 0

    # Exact counterexample: one light mode, all other modes positive.
    example = Matrix(
        [
            [Rational(1, 3), -1, 0, -1],
            [-1, 6, 0, 0],
            [0, 0, 1, -2],
            [-1, 0, -2, 10],
        ]
    )
    assert example * Matrix([6, 1, 2, 1]) == Matrix.zeros(4, 1)
    assert example.det() == 0 and example.rank() == 3
    for size in (1, 2, 3):
        for subset in combinations(range(4), size):
            assert example.extract(subset, subset).det() > 0
    source_a = Rational(1, 6) - Rational(-1, 3)
    corrected_a = Rational(1, 6) - Rational(-1, 6)
    assert source_a == Rational(1, 2)
    assert corrected_a == example[0, 0] == Rational(1, 3)
    return example, source_a, corrected_a


if __name__ == "__main__":
    print("gauge coefficients (-g^2 times each group):", gauge_terms())
    _, source_value, corrected_value = projector_identity()
    print("published D11 for exact example:", source_value)
    print("zero-mode-consistent D11:", corrected_value)
    print("PASS: exact gauge terms; STOP: published scalar-projector identity fails")
