"""Replay complete Higgs-doublet blocks against the prior tensor derivation.

The comparator uses the independently derived weak-vector quadratic
matrices A,B,C,D,E in the earlier vacuum-kernel calculation. It projects
the exact highest-weight representatives into those coordinates, forms the
quadratic polynomial, and compares every 4x4 entry with the parent-action
bilinear oracle at the same stationary witness.
"""

import sys
from pathlib import Path

from sympy import I, Matrix, conjugate, simplify, sqrt, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_doublet_block import main as independent_doublet
from verify_eta1_doublet_mixing import doublet_form

from compile_sm_multiplicity_representatives import kinetic_inner
from evaluate_sm_hessian_blocks import (
    block, rational_representatives, realified_representative, witness,
)


def state_form(state):
    return {idx: a+I*b for idx, (a, b) in state.Sigma.items()}


def coordinates(tangent, sign=1):
    """Independent holomorphic and antiholomorphic weak-doublet coordinates."""
    a, b = tangent.real, tangent.imag
    fa, fb = state_form(a), state_form(b)
    hol = {idx: simplify(fa.get(idx, 0)+sign*I*fb.get(idx, 0))
           for idx in set(fa) | set(fb)}
    anti = {idx: simplify(conjugate(fa.get(idx, 0))
                          +sign*I*conjugate(fb.get(idx, 0)))
            for idx in set(fa) | set(fb)}
    e = [{idx: (p+I*q)/sqrt(3) for idx, (p, q) in doublet_form(j).items()}
         for j in range(6, 10)]
    ebar = [{idx: conjugate(z) for idx, z in form.items()} for form in e]
    x = Matrix([kinetic_inner(form, hol, "form") for form in e])
    xb = Matrix([kinetic_inner(form, anti, "form") for form in ebar])
    y = Matrix([a.phi[j]+sign*I*b.phi[j] for j in range(6, 10)])
    yb = Matrix([conjugate(a.phi[j])+sign*I*conjugate(b.phi[j])
                 for j in range(6, 10)])
    return x, xb, y, yb


def add_coords(u, v):
    return tuple(a+b for a, b in zip(u, v))


def quadratic(coords, matrices):
    x, xb, y, yb = coords
    a, b, c, d, e = matrices
    return simplify((x.T*a*xb + y.T*b*yb
                     +x.T*c*x + xb.T*c.conjugate()*xb
                     +y.T*d*y + yb.T*d.conjugate()*yb
                     +x.T*e*y + xb.T*e.conjugate()*yb)[0])


def comparator_matrices():
    matrices, (omega, sigma, vs, s, sbar) = independent_doublet(verbose=False)
    coefficients = witness()
    sub = {omega: sqrt(60), sigma: 4*sqrt(2), vs: sqrt(2),
           s: 1, sbar: 1}
    for matrix in matrices:
        for symbol in matrix.free_symbols:
            if str(symbol) in coefficients:
                sub[symbol] = coefficients[str(symbol)]
    return tuple(matrix.subs(sub).applyfunc(simplify) for matrix in matrices)


def main():
    matrices = comparator_matrices()
    for label in ((0, 0, 1, -3), (0, 0, 1, 3)):
        reps = rational_representatives()[label]
        tangents = [realified_representative(sector, obj)
                    for sector, _, obj in reps]
        expected = Matrix(4, 4, lambda i, j: simplify(
            quadratic(add_coords(coordinates(tangents[i], -1),
                                 coordinates(tangents[j], 1)), matrices)
            -quadratic(coordinates(tangents[i], -1), matrices)
            -quadratic(coordinates(tangents[j], 1), matrices)))
        observed = block(label)
        difference = (observed-expected).applyfunc(simplify)
        assert difference == zeros(4), (label, difference)
        print("INDEPENDENT_COMPLETE_DOUBLET_BLOCK_PASS", label, flush=True)


if __name__ == "__main__":
    main()
