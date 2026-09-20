"""Independent direct-parent replay of the rounded scalar candidate.

No generated affine block cache is used. This reconstructs the rescaled
parent coefficients over exact radicals, reevaluates all 35 Hessian blocks
from the parent oracle, and checks high-precision generalized eigenvalues.
"""

from pathlib import Path
import json
import sys

import mpmath as mp
from sympy import I, N, Rational, sqrt, simplify, diff

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import block, rational_representatives
from compile_sm_multiplicity_representatives import kinetic_inner
from parent_bilinear_oracle import REAL_NAMES, COMPLEX_NAMES
from search import FREE, DEGREES
sys.path.insert(0, str(HERE.parent / "canonical_so10_vacuum_kernel"))
from derive_vacuum import main as derive_vacuum

mp.mp.dps = 60


def exact_coefficients():
    point = json.loads((HERE / "STAGE1_POINT.json").read_text())
    assert point["x_sigma_over_omega"] == "0.1"
    assert point["y_v_over_omega"] == "0.1"
    z = {name: Rational(point["free_coefficients"][name]) for name in FREE}
    omega, x, y = sqrt(60), Rational(1, 10), Rational(1, 10)
    sigma, vs = x*omega, y*omega
    c = {name: z[name] for name in REAL_NAMES if name in z}
    for name in COMPLEX_NAMES:
        c[name] = z[name+":re"]+I*z[name+":im"]
    c["mphi2"] *= omega**2
    c["muPhi"] *= omega
    c["muPhiPhi"] *= omega
    c["z6"] *= omega
    lphi = c["lambdaPhi1"]+Rational(7, 60)*c["lambdaPhi2"]
    lmix = c["lambdaPhiSigma1"]-c["lambdaPhiSigma2"]/4
    c["mPhi2"] = (-Rational(3, 2)*c["muPhi"]
                   -2*lphi*omega**2-lmix*sigma**2
                   -c["lambdaPhiS"]*vs**2/2)
    c["mSigma2"] = (-lmix*omega**2-2*c["lambdaSigma1"]*sigma**2
                    -c["lambdaSigmaS"]*vs**2/2)
    c["mS2"] = (-c["lambdaPhiS"]*omega**2
                -c["lambdaSigmaS"]*sigma**2-c["lambdaS"]*vs**2)
    b, s = x*sqrt(Rational(15, 8)), y*sqrt(30)
    effective = {name: simplify(value*b**DEGREES.get(name, (0, 0))[0]
                                *s**DEGREES.get(name, (0, 0))[1])
                 for name, value in c.items()}
    return effective, b, s


def mp_complex(z):
    real, imag = z.as_real_imag()
    return mp.mpc(str(N(real, 65)), str(N(imag, 65)))


def kinetic_diag(label, b, s):
    values = []
    for sector, _, obj in rational_representatives()[label]:
        if sector == "Phi":
            g = 2*kinetic_inner(obj, obj, "matrix")
        elif sector in ("Sigma", "SigmaBar"):
            g = b*b*kinetic_inner(obj, obj, "form")
        elif sector in ("phi", "phiBar"):
            g = kinetic_inner(obj, obj, "vector")
        else:
            g = s*s
        values.append(mp.mpf(str(N(g, 65))))
    return values


def main():
    coefficients, b, s = exact_coefficients()
    original = {name: simplify(value/b**DEGREES.get(name, (0, 0))[0]
                               /s**DEGREES.get(name, (0, 0))[1])
                for name, value in coefficients.items()}
    v0, (omega, sigma, vs), symbols = derive_vacuum()
    substitution = {omega: sqrt(60), sigma: sqrt(60)/10, vs: sqrt(60)/10}
    substitution.update({symbol: original[name] for name, symbol in symbols.items()})
    assert all(simplify(diff(v0, field).subs(substitution)) == 0
               for field in (omega, sigma, vs))
    print("EXACT_ACTION_TADPOLES_PASS", flush=True)
    if "--tadpoles-only" in sys.argv:
        return
    expected = expected_block_ranks()
    worst = (mp.inf, None)
    color = (mp.inf, None)
    max_zero = mp.mpf(0)
    real_rank = 0
    for label in sorted(expected):
        h_exact = block(label, coefficients)
        m, k, target_rank = expected[label]
        assert h_exact.rank() == target_rank, (label, "rank")
        g = kinetic_diag(label, b, s)
        h = mp.matrix(m)
        for i in range(m):
            for j in range(m):
                h[i, j] = mp_complex(h_exact[i, j]) / mp.sqrt(g[i]*g[j])
        eigenvalues, _ = mp.eighe(h)
        ordered = sorted((eigenvalues[i] for i in range(m)), key=lambda a: abs(a))
        if k:
            max_zero = max(max_zero, max(abs(q) for q in ordered[:k]))
        physical = ordered[k:]
        assert len(physical) == target_rank
        if physical:
            low = min(physical)
            assert low > 0, (label, "tachyon", low)
            if low < worst[0]:
                worst = (low, label)
            if (label[0] or label[1]) and low < color[0]:
                color = (low, label)
        real_rank += dimension(label)*target_rank
        print("EXACT_BLOCK_PASS", label, "rank", target_rank,
              "minimum_physical", mp.nstr(min(physical), 15)
              if physical else "none", flush=True)
    assert real_rank == 294
    assert max_zero < mp.mpf("1e-40")
    assert color[0]/60 > mp.mpf("1e-4")
    print("DIRECT_PARENT_STAGE1_REPLAY_PASS rank=294 nullity=34",
          "min_m2", mp.nstr(worst[0], 30), "min_label", worst[1],
          "min_colored_m2", mp.nstr(color[0], 30), "color_label", color[1],
          "max_zero", mp.nstr(max_zero, 10), flush=True)


if __name__ == "__main__":
    main()
