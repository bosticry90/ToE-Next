"""Deterministic structured quartic-ray screen for the frozen scalar point."""

from itertools import combinations
from pathlib import Path
import sys

from sympy import I, Matrix, N, Rational, conjugate, simplify, zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from evaluate_sm_hessian_blocks import rational_representatives, realified_representative
from parent_bilinear_oracle import (
    State, REAL_NAMES, invariant_values, state_add, state_scale, vacuum_state,
)
from replay_candidate_exact import exact_coefficients

COMPLEX_QUARTICS = ("z4", "zK", "zEta", "zD")
MAX_RAYS = 200


def coefficients():
    c, b, s = exact_coefficients()
    c = dict(c)
    c["lambdaPhiphi1"] = -Rational(1, 500)
    c["zK"] = Rational(3, 100)*s
    c["zEta"] = Rational(3, 10)*b**3
    return c


def parts():
    z = zeros(10)
    v = vacuum_state()
    pdiag = Matrix.diag(1, -1, *([0]*8))
    poff = zeros(10)
    poff[0, 1] = poff[1, 0] = 1
    reps = rational_representatives()
    ds = next(obj for sector, _, obj in reps[(0, 0, 1, -3)]
              if sector == "Sigma")
    dv = next(obj for sector, _, obj in reps[(0, 0, 1, -3)]
              if sector == "phi")
    cv = next(obj for sector, _, obj in reps[(0, 1, 0, -2)]
              if sector == "phi")
    fs = realified_representative("Sigma", ds)
    fv = realified_representative("phi", dv)
    fc = realified_representative("phi", cv)
    empty = (0,)*10
    return (
        ("Phi_PS", State(v.Phi, {}, empty, 0)),
        ("Phi_diag", State(pdiag, {}, empty, 0)),
        ("Phi_offdiag", State(poff, {}, empty, 0)),
        ("Sigma_singlet", State(z, v.Sigma, empty, 0)),
        ("Sigma_doublet_re", fs.real),
        ("Sigma_doublet_im", fs.imag),
        ("phi_doublet_re", fv.real),
        ("phi_doublet_im", fv.imag),
        ("phi_color_re", fc.real),
        ("phi_color_im", fc.imag),
        ("S_re", State(z, {}, empty, 1)),
        ("S_im", State(z, {}, empty, I)),
    )


def quartic(state, c):
    inv = invariant_values(state)
    value = sum(c[name]*inv[name] for name in REAL_NAMES[6:])
    value += sum(c[name]*inv[name]+conjugate(c[name]*inv[name])
                 for name in COMPLEX_QUARTICS)
    value = simplify(value)
    assert simplify(value-conjugate(value)) == 0
    return value


def candidates(basis):
    for name, state in basis:
        yield name, state
    for (name_a, a), (name_b, b) in combinations(basis, 2):
        for factor in (1, -1, 2):
            yield f"{name_a}{factor:+d}{name_b}", state_add(a, state_scale(b, factor))
    lookup = dict(basis)
    for names in (
        ("Phi_PS", "Sigma_singlet", "S_re"),
        ("Phi_PS", "Sigma_singlet", "phi_doublet_re"),
        ("Phi_PS", "phi_doublet_re", "S_re"),
        ("Sigma_singlet", "phi_doublet_re", "S_re"),
    ):
        yield "+".join(names), state_add(state_add(lookup[names[0]],
                                              lookup[names[1]]), lookup[names[2]])


def main():
    c = coefficients()
    assert simplify(c["lambdaPhi1"]+c["lambdaPhi2"]/10) == Rational(52268, 10**9)
    assert c["lambdaPhiVector1"] == c["lambdaPhiVector2"] == Rational(1, 10)
    assert c["lambdaS"] > 0
    basis = parts()
    witness = state_add(basis[0][1], basis[3][1])
    assert simplify(quartic(state_scale(witness, 2), c)-16*quartic(witness, c)) == 0
    tested = 0
    best = None
    for name, ray in candidates(basis):
        if tested == MAX_RAYS:
            break
        q = quartic(ray, c)
        tested += 1
        value = N(q, 50)
        if best is None or value < best[0]:
            best = value, name, q
        if tested <= 12 or tested % 25 == 0:
            print("RAY", tested, name, value, flush=True)
        if value < -Rational(1, 10**10):
            print("NEGATIVE_QUARTIC_RAY", tested, name, flush=True)
            print("EXACT_Q", q, flush=True)
            print("NUMERIC_Q", N(q, 80), "SYMPY_SIGN", q.is_negative, flush=True)
            assert q.is_negative or N(q, 80) < -Rational(1, 10**10)
            print("GLOBAL_RUNAWAY_DIRECTION_FOUND", flush=True)
            return
    print("BFB_UNRESOLVED", "structured_rays_tested", tested,
          "minimum_tested", best[1], best[0],
          "exact_quartic", best[2], flush=True)


if __name__ == "__main__":
    main()
