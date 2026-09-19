"""Exact off-diagonal Hessian-row probes of broken-gauge directions.

These probes are deliberately not advertised as a complete irrep-block
certification.  They check B(e,g)=0, rather than only B(g,g)=0, for
representatives that exercise distinct parent-field mixings.
"""

from sympy import Rational, simplify, symbols, zeros

from parent_bilinear_oracle import (
    COMPLEX_NAMES, REAL_NAMES, State, bilinear_coefficients,
    vacuum_state,
)
from verify_oracle_controls import sigma_direction, vector_direction
from derive_stabilizers import form_action, generators
from verify_eta1_doublet_mixing import doublet_form


PARAMETERS = dict(zip(REAL_NAMES, symbols(" ".join(REAL_NAMES), real=True)))


def gauge_direction(pair):
    g = dict(generators())[pair]
    base = vacuum_state()
    return State(g*base.Phi-base.Phi*g, form_action(g, base.Sigma), (0,)*10, 0)


def phi_direction(i, j):
    p = zeros(10)
    p[i, j] = p[j, i] = 1
    return State(p, {}, (0,)*10, 0)


def stationary_residue(row):
    c = PARAMETERS
    lphi = c["lambdaPhi1"] + Rational(7, 60)*c["lambdaPhi2"]
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    masses = {
        c["mPhi2"]: -Rational(3, 2)*c["muPhi"] - 120*lphi
                     - 32*lmix - c["lambdaPhiS"],
        c["mSigma2"]: -60*lmix - 64*c["lambdaSigma1"]
                       - c["lambdaSigmaS"],
        c["mS2"]: -60*c["lambdaPhiS"] - 32*c["lambdaSigmaS"]
                   - 2*c["lambdaS"],
    }
    real_residue = simplify(sum(c[n]*row[n] for n in REAL_NAMES).subs(masses))
    complex_residue = {n: simplify(row[n]) for n in COMPLEX_NAMES}
    return real_residue, complex_residue


def check(name, probe, orbit):
    row = bilinear_coefficients(probe, orbit)
    real_residue, complex_residue = stationary_residue(row)
    assert real_residue == 0, (name, "real", real_residue)
    assert all(v == 0 for v in complex_residue.values()), (
        name, "complex", complex_residue)
    print(name, "B(e,g)=0 PASS")


def main():
    g_cross = gauge_direction((0, 6))
    g_weak = gauge_direction((6, 8))
    check("cross-block 54", phi_direction(0, 6), g_cross)
    check("cross-block 126-doublet", sigma_direction(doublet_form(6)), g_cross)
    check("cross-block 10-vector", vector_direction(6), g_cross)
    check("weak-block 126-doublet", sigma_direction(doublet_form(6)), g_weak)
    print("FOUR_EXACT_OFF_DIAGONAL_GOLDSTONE_ROW_PROBES_PASS; not full H*g")


if __name__ == "__main__":
    main()
