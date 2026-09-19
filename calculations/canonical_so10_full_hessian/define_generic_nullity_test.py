"""Freeze a stationary exact witness and the per-irrep rank acceptance test.

This script defines, but does not execute, the full-Hessian rank test:
the missing parent-action blocks must be computed before a pass is possible.
An attained rank 294 at this witness would certify maximal generic rank on
the stationary parameter branch, because symmetry bounds rank by 294.
"""

from collections import Counter

from sympy import I, Matrix, Rational, diff, simplify, sqrt

from decompose_sm_tangent import (
    BAR_SIGMA, PHI, SIGMA, VEC, Z, adjoint_char, decompose, dimension,
)
from parent_bilinear_oracle import COMPLEX_NAMES, REAL_NAMES
from derive_vacuum import main as derive_vacuum


def exact_stationary_witness():
    """Nonzero rational/Gaussian-rational couplings at raw VEV amplitudes."""
    free_real = [name for name in REAL_NAMES
                 if name not in ("mPhi2", "mSigma2", "mS2")]
    c = {name: Rational(j+2, j+5) for j, name in enumerate(free_real)}
    c.update({name: Rational(j+1, 7)+I*Rational(j+2, 11)
              for j, name in enumerate(COMPLEX_NAMES)})
    lphi = c["lambdaPhi1"]+Rational(7, 60)*c["lambdaPhi2"]
    lmix = c["lambdaPhiSigma1"]-c["lambdaPhiSigma2"]/4
    c["mPhi2"] = -Rational(3, 2)*c["muPhi"]-120*lphi-32*lmix-c["lambdaPhiS"]
    c["mSigma2"] = -60*lmix-64*c["lambdaSigma1"]-c["lambdaSigmaS"]
    c["mS2"] = -60*c["lambdaPhiS"]-32*c["lambdaSigmaS"]-2*c["lambdaS"]
    assert set(c) == set(REAL_NAMES) | set(COMPLEX_NAMES)
    assert all(c[name] != 0 for name in c)
    return c


def expected_block_ranks():
    total = Counter()
    for char in (PHI, SIGMA, BAR_SIGMA, VEC, VEC, Counter({Z: 2})):
        total.update(decompose(char))
    broken = decompose(adjoint_char()) - Counter({
        (1, 1, 0, 0): 1, (0, 0, 2, 0): 1, (0, 0, 0, 0): 1,
    })
    required_kernel = broken + Counter({(0, 0, 0, 0): 1})
    expected = {irrep: (multiplicity, required_kernel[irrep],
                        multiplicity-required_kernel[irrep])
                for irrep, multiplicity in total.items()}
    assert all(rank >= 0 for _, _, rank in expected.values())
    assert sum(dimension(r)*m for r, (m, _, _) in expected.items()) == 328
    assert sum(dimension(r)*k for r, (_, k, _) in expected.items()) == 34
    assert sum(dimension(r)*rank for r, (_, _, rank) in expected.items()) == 294
    return expected


def main():
    c = exact_stationary_witness()
    v0, (omega, sigma, vs), symbols = derive_vacuum()
    substitution = {omega: sqrt(60), sigma: 4*sqrt(2), vs: sqrt(2)}
    substitution.update({symbol: c[name] for name, symbol in symbols.items()})
    assert all(simplify(diff(v0, x).subs(substitution)) == 0
               for x in (omega, sigma, vs))
    lphi = c["lambdaPhi1"]+Rational(7, 60)*c["lambdaPhi2"]
    lmix = c["lambdaPhiSigma1"]-c["lambdaPhiSigma2"]/4
    w, s, v = sqrt(60), 4*sqrt(2), sqrt(2)
    radial = Matrix([
        [3*c["muPhi"]*w/sqrt(60)+8*lphi*w*w,
         4*lmix*w*s, 2*c["lambdaPhiS"]*w*v],
        [4*lmix*w*s, 8*c["lambdaSigma1"]*s*s,
         2*c["lambdaSigmaS"]*s*v],
        [2*c["lambdaPhiS"]*w*v,
         2*c["lambdaSigmaS"]*s*v, 2*c["lambdaS"]*v*v],
    ])
    assert simplify(radial.det()) != 0
    expected = expected_block_ranks()
    print("EXACT_STATIONARY_WITNESS_DEFINED: 29 nonzero parent coefficients; neutral radial rank=3")
    print("raw VEV: omega=sqrt(60), sigma=4sqrt(2), v=sqrt(2)")
    for irrep in sorted(expected):
        multiplicity, nullity, rank = expected[irrep]
        print(irrep, "multiplicity", multiplicity,
              "required nullity", nullity, "target rank", rank)
    print("FULL_GENERIC_NULLITY_TEST_NOT_YET_EXECUTED: target 34 null/294 rank")


if __name__ == "__main__":
    main()
