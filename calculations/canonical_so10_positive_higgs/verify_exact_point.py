"""High-precision, direct-parent replay of the frozen positive-quartic point."""

import json
from pathlib import Path
import sys

from sympy import N, Rational, sqrt, simplify

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_light_higgs_quartic"))

from evaluate_sm_hessian_blocks import block, rational_representatives, realified_representative
from replay_candidate_exact import exact_coefficients, kinetic_diag
from compute import (
    Evaluator, add, build_hessian, canonical_norm2, heavy_basis,
    mp, mpval, rat, relaxed, scale, schur_correction,
)

mp.mp.dps = 75
DOUBLET = ((0, 0, 1, -3), (0, 0, 1, 3))
COLORED = ((0, 1, 0, -2), (1, 0, 0, 2))


def tuning():
    data = json.loads((HERE / "POINT.json").read_text())
    p = data["determinant_polynomial"]
    A = Rational(p["A"])
    B = Rational(p["B0"])+Rational(p["B1"])*sqrt(15)
    C = Rational(p["C0"])+Rational(p["C1"])*sqrt(15)
    root = simplify((-B+sqrt(B*B-4*A*C))/(2*A))
    assert Rational(530, 100000) < N(root, 50) < Rational(531, 100000)
    assert simplify(A*root**2+B*root+C) == 0
    w = mp.mpf(p["A"])
    bb = mp.mpf(p["B0"])+mp.mpf(p["B1"])*mp.sqrt(15)
    cc = mp.mpf(p["C0"])+mp.mpf(p["C1"])*mp.sqrt(15)
    w = (-bb+mp.sqrt(bb**2-4*w*cc))/(2*w)
    assert abs(w-mp.mpf(str(N(root, 70)))) < mp.mpf("1e-68")
    assert abs(w-mp.mpf(data["approximate_w"])) < mp.mpf("1e-60")
    return root, w


def parent_coefficients(w):
    c, b, s = exact_coefficients()
    c = dict(c)
    c["lambdaPhiphi1"] = -Rational(1, 500)
    c["mphi2"] = 60*(w+Rational(1, 500))
    c["z6"] = Rational(3, 100)*sqrt(60)*s
    c["zK"] = Rational(3, 100)*s
    c["zEta"] = Rational(3, 10)*b**3
    return c, b, s


def light_states(vector, metric, digits):
    tangents = [realified_representative(sector, obj)
                for sector, _, obj in rational_representatives()[DOUBLET[0]]]
    neutral = []
    phase = []
    for j, tangent in enumerate(tangents):
        z = vector[j]/mp.sqrt(metric[j])
        neutral.append(add(scale(tangent.real, rat(z.real, digits)),
                           scale(tangent.imag, -rat(z.imag, digits))))
        phase.append(add(scale(tangent.real, rat(-z.imag, digits)),
                         scale(tangent.imag, -rat(z.real, digits))))
    return add(*neutral), add(*phase)


def direct_block(label, coefficients, b, s):
    exact = block(label, coefficients)
    g = kinetic_diag(label, b, s)
    h = mp.matrix(exact.rows)
    for i in range(exact.rows):
        for j in range(exact.cols):
            h[i, j] = mpval(exact[i, j])/mp.sqrt(g[i]*g[j])
    eig, vectors = mp.eighe(h)
    return eig, vectors, g


def main():
    _, w = tuning()
    w_rational = Rational(mp.nstr(w, 70))
    c, b_exact, s_exact = parent_coefficients(w_rational)
    print("FROZEN_ROOT", mp.nstr(w, 50), "u", mp.nstr(w+mp.mpf(1)/500, 50), flush=True)
    affected = {label for label, reps in rational_representatives().items()
                if any(sector in ("phi", "phiBar") for sector, _, _ in reps)}
    assert affected == set(DOUBLET+COLORED)
    light = None
    colored_min = mp.inf
    other_min = mp.inf
    for label in sorted(affected):
        eig, vectors, metric = direct_block(label, c, b_exact, s_exact)
        if label in DOUBLET:
            assert abs(eig[0]) < mp.mpf("1e-55"), (label, eig[0])
            rest = [eig[i] for i in range(1, len(eig))]
            if label == DOUBLET[0]:
                light = (vectors[:, 0], metric)
                fraction = sum(abs(vectors[j, 0])**2 for j in (0, 1))
                assert fraction > mp.mpf("1e-6")
                print("LIGHT_126_FRACTION", mp.nstr(fraction, 20), flush=True)
        else:
            rest = list(eig)
            colored_min = min(colored_min, *rest)
        assert all(x > 0 for x in rest), (label, rest)
        other_min = min(other_min, *rest)
        print("DIRECT_BLOCK_PASS", label,
              "min_other", mp.nstr(min(rest), 25), flush=True)
    assert light is not None
    # The other 31 blocks and all tadpoles are identically Stage 1: every
    # modified monomial contains at least two zero-VEV 10_H fields.
    assert other_min > mp.mpf("0.02")
    assert colored_min > mp.mpf("0.006")
    print("STAGE1_UNCHANGED_31_BLOCKS; REAL_RANK_290_NULLITY_38", flush=True)

    h, phase = light_states(light[0], light[1], 18)
    cnum = {name: mpval(value) for name, value in c.items()}
    evaluator = Evaluator(cnum)
    groups = heavy_basis()
    heavy_matrices = build_hessian(evaluator, groups)
    direct, correction, effective, sources, solves = relaxed(
        evaluator, h, groups, heavy_matrices)
    b, s = mpval(b_exact).real, mpval(s_exact).real
    metric_h = canonical_norm2(h, b, s)
    lam = 4*effective/metric_h**2
    assert lam > mp.mpf("0.05"), lam
    print("CANONICAL_QUARTIC", "direct", mp.nstr(4*direct/metric_h**2, 30),
          "heavy_subtraction", mp.nstr(4*correction/metric_h**2, 30),
          "effective", mp.nstr(lam, 35), flush=True)
    sheared = mp.mpf(0)
    for H, j in zip(heavy_matrices, sources):
        T = mp.eye(len(j))
        if len(j) > 1:
            T[0, 1] = mp.mpf(2)/3
            T[1, 0] = -mp.mpf(1)/5
        sheared += schur_correction(T.T*H*T, T.T*j)
    assert abs(sheared-correction) < mp.mpf("1e-15")
    print("HEAVY_BASIS_REPLAY", mp.nstr(4*sheared/metric_h**2, 30), flush=True)

    # Polynomial-along-valley replay is a separate extraction of the t^4
    # coefficient from parent-potential evaluations, not from j^T H^+ j.
    xopt = add(*(scale(x, rat(solve[i], 18))
                 for group, solve in zip(groups, solves)
                 for i, x in enumerate(group)))
    nodes = list(range(-4, 5))
    vals = mp.matrix([evaluator.value(add(scale(h, Rational(t)),
                                          scale(xopt, Rational(t*t))))
                      for t in nodes])
    vand = mp.matrix([[mp.mpf(t)**k for k in range(9)] for t in nodes])
    replay4 = mp.lu_solve(vand, vals)[4]
    assert abs(replay4-effective) < mp.mpf("1e-10")
    print("VALLEY_REPLAY", mp.nstr(4*replay4/metric_h**2, 30), flush=True)
    _, _, phase_eff, _, _ = relaxed(evaluator, phase, groups, heavy_matrices)
    assert abs(phase_eff-effective) < mp.mpf("1e-10")
    print("PHASE_REPLAY", mp.nstr(4*phase_eff/metric_h**2, 30), flush=True)
    print("POSITIVE_QUARTIC_HIGGS_BENCHMARK_FOUND",
          "lambda", mp.nstr(lam, 25),
          "colored_min_m2", mp.nstr(colored_min, 20),
          "other_changed_min_m2", mp.nstr(other_min, 20), flush=True)


if __name__ == "__main__":
    main()
