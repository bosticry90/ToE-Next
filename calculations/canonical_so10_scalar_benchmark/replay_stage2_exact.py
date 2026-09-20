"""Direct-parent exact changed-block replay for the tuned Higgs point.

Only four SM irrep blocks contain a 10_H or its conjugate. Every Stage 2
parameter change contains at least one 10_H field, while <10_H>=0; hence the
other 31 blocks and all vacuum tadpoles are identical to the exact Stage 1
certificate. The tuned mass is an exact algebraic doublet-determinant root.
"""

import json
from pathlib import Path
import sys

import mpmath as mp
from sympy import Poly, Rational, sqrt, simplify, symbols, N

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import block, rational_representatives
from replay_candidate_exact import exact_coefficients, kinetic_diag, mp_complex

mp.mp.dps = 70
DOUBLETS = ((0, 0, 1, -3), (0, 0, 1, 3))


def polynomial_and_root():
    data = json.loads((HERE / "STAGE2_POINT.json").read_text())
    p = data["determinant_polynomial"]
    a = Rational(p["A"])
    bb = Rational(p["B0"])+Rational(p["B1"])*sqrt(15)
    cc = Rational(p["C0"])+Rational(p["C1"])*sqrt(15)
    root = simplify((-bb+sqrt(bb*bb-4*a*cc))/(2*a))
    assert -Rational(14, 100) < N(root, 40) < -Rational(13, 100)
    aa_mp = mp.mpf(p["A"])
    bb_mp = mp.mpf(p["B0"])+mp.mpf(p["B1"])*mp.sqrt(15)
    cc_mp = mp.mpf(p["C0"])+mp.mpf(p["C1"])*mp.sqrt(15)
    u_mp = (-bb_mp+mp.sqrt(bb_mp**2-4*aa_mp*cc_mp))/(2*aa_mp)
    assert abs(u_mp-mp.mpf(str(N(root, 65)))) < mp.mpf("1e-60")
    return data, (a, bb, cc), root, u_mp


def effective_coefficients(u):
    coefficients, b, s = exact_coefficients()
    c = dict(coefficients)
    c["mphi2"] = 60*u
    c["z6"] = Rational(3, 10)*sqrt(60)*s
    c["zK"] = Rational(3, 10)*s
    c["zEta"] = Rational(3, 10)*b**3
    return c, b, s


def direct_eigen(label, h_symbolic, u, u_mp, b, s):
    k = expected_block_ranks()[label][1]+int(label in DOUBLETS)
    g = kinetic_diag(label, b, s)
    m = h_symbolic.rows
    h = mp.matrix(m)
    for i in range(m):
        for j in range(m):
            expr = h_symbolic[i, j]
            assert simplify(expr.diff(u, 2)) == 0
            h[i, j] = (mp_complex(expr.subs(u, 0))
                       +u_mp*mp_complex(expr.diff(u))) / mp.sqrt(g[i]*g[j])
    eig, vectors = mp.eighe(h)
    order = sorted(range(m), key=lambda i: abs(eig[i]))
    if k:
        assert max(abs(eig[i]) for i in order[:k]) < mp.mpf("1e-50"), (
            label, [mp.nstr(eig[i], 20) for i in order[:k]])
    physical = [eig[i] for i in order[k:]]
    assert all(value > 0 for value in physical), (label, physical)
    mix = None
    if label in DOUBLETS:
        zero_vector = [vectors[j, order[0]] for j in range(m)]
        mix = sum(abs(zero_vector[j])**2 for j in (0, 1))
    print("STAGE2_CHANGED_BLOCK_PASS", label,
          "remaining_min", mp.nstr(min(physical), 25) if physical else "none",
          "126_fraction", mp.nstr(mix, 12) if mix is not None else "n/a",
          flush=True)
    return min(physical) if physical else mp.inf, mix


def main():
    _, poly_coeffs, root, u_mp = polynomial_and_root()
    u = symbols("u", real=True)
    coefficients, b, s = effective_coefficients(u)
    affected = {label for label, reps in rational_representatives().items()
                if any(sector in ("phi", "phiBar") for sector, _, _ in reps)}
    expected_affected = set(DOUBLETS) | {(0, 1, 0, -2), (1, 0, 0, 2)}
    assert affected == expected_affected, affected
    print("STAGE2_AFFECTED_IRREPS", sorted(affected), flush=True)
    global_min = mp.inf
    fractions = []
    for label in sorted(affected):
        h = block(label, coefficients)
        if label in DOUBLETS:
            p = Poly(h.det(), u)
            assert p.degree() == 2
            ratio = simplify(p.all_coeffs()[0]/poly_coeffs[0])
            assert all(simplify(q-ratio*r) == 0
                       for q, r in zip(p.all_coeffs(), poly_coeffs)), label
            assert simplify(p.as_expr().subs(u, root)) == 0
        low, mix = direct_eigen(label, h, u, u_mp, b, s)
        global_min = min(global_min, low)
        if mix is not None:
            fractions.append(mix)
    assert all(value > mp.mpf("1e-8") for value in fractions)
    assert global_min > 0
    # Unchanged 31 blocks retain the Stage 1 exact positive spectrum.
    print("DIRECT_PARENT_STAGE2_CHANGED_BLOCKS_PASS", "u", mp.nstr(u_mp, 45),
          "changed_min_m2", mp.nstr(global_min, 25),
          "real_rank=290 nullity=38 with Stage1 unchanged-block certificate",
          flush=True)


if __name__ == "__main__":
    main()
