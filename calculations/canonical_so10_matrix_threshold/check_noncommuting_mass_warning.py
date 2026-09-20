"""Exact two-mass loop building block; not a full gauge-threshold formula.

At the physical vacuum some PS generators do not commute with mass².
The quadratic functional determinant then contains mixed propagators;
one cannot replace every such contribution by Tr(T² log mass²).
"""

from sympy import Matrix, Rational, integrate, limit, log, simplify, symbols


def main():
    a, b, p2, x = symbols("a b p2 x", positive=True)
    t = Matrix([[0, Rational(1, 2)], [Rational(1, 2), 0]])
    mass2 = Matrix.diag(a, b)
    assert mass2*t-t*mass2 != Matrix.zeros(2)
    propagator = Matrix.diag(1/(p2+a), 1/(p2+b))
    mixed = simplify((propagator*t*propagator*t).trace())
    assert simplify(mixed-1/(2*(p2+a)*(p2+b))) == 0
    feynman_log = simplify(integrate(log(x*a+(1-x)*b), (x, 0, 1)))
    expected = (a*log(a)-b*log(b))/(a-b)-1
    assert simplify(feynman_log-expected) == 0
    assert simplify(limit(expected, a, b)-log(b)) == 0
    mixed_value = simplify(expected.subs({a: 1, b: 4}))
    single_log_proxy = log(4)/2
    assert float(mixed_value-single_log_proxy) > .15
    print("NONCOMMUTING_MASS_WARNING_PASS",
          "mixed_propagator", mixed,
          "two_mass_log_at_1_4", mixed_value,
          "single_log_proxy", single_log_proxy,
          "difference", simplify(mixed_value-single_log_proxy))


if __name__ == "__main__":
    main()
