"""Exact fieldwise-rephasing rank for selected phase-sensitive invariants."""

from fractions import Fraction

CHI4 = (2, 0, 1)       # Sigma Sigma Phi S
CHI6 = (0, 2, -1)      # phi phi S*
ETA1 = (1, 1, 0)       # Sigma Sigma Sigma* phi
KAPPA = CHI6           # Phi phi phi S*
PQ = (1, -1, -2)       # proportional to (qSigma,qphi,qS)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def main():
    assert all(dot(row, PQ) == 0 for row in (CHI4, CHI6, ETA1, KAPPA))
    assert tuple(CHI4[i] + CHI6[i] for i in range(3)) == tuple(2 * x for x in ETA1)
    assert CHI4[0] * CHI6[1] - CHI4[1] * CHI6[0] == 4  # rank at least two
    assert Fraction(1, 2) * CHI4[0] + Fraction(1, 2) * CHI6[0] == ETA1[0]
    print("Generic nonzero chi4 and chi6 leave exactly one scalar-field U(1): PQ.")
    print("If eta1 is nonzero, 2 arg(eta1)-arg(chi4)-arg(chi6) is rephasing invariant.")
    print("Phi phi phi S* has the chi6 phase vector; its relative phase is also invariant if both occur.")
    print("With one copy of each irrep, Schur's lemma makes this the full connected commuting internal symmetry check for generic nonzero chi4,chi6.")
    print("Discrete/global quotients and pointwise symmetry when couplings vanish remain open.")


if __name__ == "__main__":
    main()
