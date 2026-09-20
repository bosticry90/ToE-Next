"""Derive the exact one-doublet determinant condition from the parent action."""

from pathlib import Path
import sys

from sympy import Poly, Rational, factor, simplify, sqrt, symbols, N

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from evaluate_sm_hessian_blocks import block
from replay_candidate_exact import exact_coefficients


def tuned_effective(u):
    stage1, b, s = exact_coefficients()
    c = dict(stage1)
    c["mphi2"] = 60*u
    c["z6"] = Rational(3, 10)*60**Rational(1, 2)*s
    c["zK"] = Rational(3, 10)*s
    c["zEta"] = Rational(3, 10)*b**3
    return c


def main():
    u = symbols("u", real=True)
    h = block((0, 0, 1, 3), tuned_effective(u))
    polynomial = Poly(factor(h.det()), u)
    print("DOUBLET_DETERMINANT_DEGREE", polynomial.degree(), flush=True)
    print("FACTOR", factor(polynomial.as_expr()), flush=True)
    assert polynomial.degree() == 2
    a, bb, cc = polynomial.all_coeffs()
    discriminant = simplify(bb*bb-4*a*cc)
    roots = [simplify((-bb+sign*sqrt(discriminant))/(2*a)) for sign in (-1, 1)]
    for root in roots:
        print("EXACT_ROOT", root, "NUMERIC", N(root, 40), flush=True)


if __name__ == "__main__":
    main()
