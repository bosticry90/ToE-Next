"""Exact five-real-direction SM-singlet Hessian from parent-action V0.

The VEV ansatz contains one real 54 singlet and one complex singlet in each
of 126 and S. We replace the two radial moduli in the *generated* V0 by
Cartesian real/imaginary coordinates, then differentiate. This is not a
separately entered potential.
"""

from sympy import Matrix, Rational, Symbol, diff, expand, simplify, solve, sqrt, zeros

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_vacuum import main as parent_vacuum


def main():
    v0, (omega, sigma, vs), coeff = parent_vacuum()
    sr, si, vr, vi = [Symbol(x, real=True) for x in ("sigmaR", "sigmaI", "vR", "vI")]
    # V0 contains only even powers of sigma and vs; the substitutions are
    # exact because the two VEV phases do not enter any parent invariant.
    potential = expand(v0.subs({sigma: sqrt(sr**2+si**2),
                                vs: sqrt(vr**2+vi**2)}))
    variables = (omega, sr, si, vr, vi)
    base = {sr: sigma, si: 0, vr: vs, vi: 0}
    tadpoles = [simplify(diff(potential, x).subs(base)) for x in variables]
    assert tadpoles[2] == tadpoles[4] == 0
    masses = solve([tadpoles[i] for i in (0, 1, 3)],
                   [coeff["mPhi2"], coeff["mSigma2"], coeff["mS2"]],
                   dict=True)[0]
    h = Matrix(5, 5, lambda i, j: simplify(
        diff(potential, variables[i], variables[j]).subs(base).subs(masses)))
    assert h == h.T
    gauge_phase = Matrix([0, 0, sigma, 0, 0])
    pq_phase = Matrix([0, 0, 2*sigma, 0, -4*vs])
    assert h*gauge_phase == zeros(5, 1)
    assert h*pq_phase == zeros(5, 1)
    assert Matrix.hstack(gauge_phase, pq_phase).rank() == 2
    # Ordering (omega,sigmaR,sigmaI,vR,vI): the radial restriction must
    # agree exactly with the prior three-dimensional action derivative.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                           "canonical_so10_vacuum_kernel"))
    from derive_radial_hessian import main as radial_main
    radial = radial_main()
    # main() returns the 3x3 matrix after printing its derivation.
    assert h.extract([0, 1, 3], [0, 1, 3]) == radial
    exact_witness = {omega: 4, sigma: 2, vs: 1,
                     coeff["muPhi"]: 0, coeff["lambdaPhi1"]: Rational(1, 10),
                     coeff["lambdaPhi2"]: 0, coeff["lambdaPhiSigma1"]: 0,
                     coeff["lambdaPhiSigma2"]: 0, coeff["lambdaPhiS"]: 0,
                     coeff["lambdaSigma1"]: Rational(1, 5),
                     coeff["lambdaSigmaS"]: 0,
                     coeff["lambdaS"]: Rational(1, 7)}
    assert h.subs(exact_witness).rank() == 3
    print("neutral singlet 5x5 Hessian on stationary branch:")
    print(h)
    print("EXPLICIT_NEUTRAL_GAUGE_AND_PQ_NULL_VECTORS_PASS; exact neutral witness rank=3")
    return h


if __name__ == "__main__":
    main()
