"""Freeze the exact determinant-zero surface for the selected rational slice."""

from pathlib import Path
import sys

from sympy import N, Poly, Rational, factor, sqrt, symbols

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from evaluate_sm_hessian_blocks import block
from replay_candidate_exact import exact_coefficients


def coefficients(w):
    c, b, s = exact_coefficients()
    c = dict(c)
    c["lambdaPhiphi1"] = Rational(0)
    c["mphi2"] = 60*w
    c["z6"] = Rational(3, 100)*sqrt(60)*s
    c["zK"] = Rational(3, 100)*s
    c["zEta"] = Rational(3, 10)*b**3
    return c


def main():
    w = symbols("w", real=True)
    h = block((0, 0, 1, -3), coefficients(w))
    p = Poly(factor(h.det()), w, extension=sqrt(15))
    assert p.degree() == 2, p
    print("EXACT_DETERMINANT_POLYNOMIAL", factor(p.as_expr()), flush=True)
    for i, q in enumerate(p.all_coeffs()):
        print("COEFFICIENT", i, q, flush=True)
    roots = p.nroots(n=65, maxsteps=300)
    for root in roots:
        print("ROOT_W", N(root, 65), "ROOT_U_AT_MIXED_MINUS_0.002",
              N(root+Rational(1, 500), 65), flush=True)


if __name__ == "__main__":
    main()
