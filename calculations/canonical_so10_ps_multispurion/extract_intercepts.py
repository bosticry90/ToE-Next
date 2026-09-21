"""Exact PS-symmetric quadratic intercepts from PARENT_ACTION_V1.

Representative directions are fixed by the certified tensor projectors.
Second variations are extracted invariant-by-invariant, before numeric
benchmark substitution. Off-shell epsilon dependence is not inferred here.
"""

from pathlib import Path
import sys

import numpy as np
from sympy import I, Matrix, Rational, conjugate, simplify, sqrt, symbols, zeros

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
for name in ("canonical_so10_full_hessian", "canonical_so10_ps_threshold_kernel",
             "canonical_so10_scalar_benchmark", "canonical_so10_ps_interval_eft"):
    sys.path.insert(0, str(CALC / name))

from parent_bilinear_oracle import (State, REAL_NAMES, COMPLEX_NAMES,
                                    invariant_values, state_add, state_scale)
from compile_sm_multiplicity_representatives import projected
from check_charged_singlet_goldstone import norm, quadratic
from check_ps_mass_limit import PHI_DEGREES, fixed_couplings
from search import DEGREES
from probe_quadratic import stationary_omega

A, S = symbols("a s", real=True)
COEFFICIENTS = {n: symbols(n, real=True) for n in REAL_NAMES}
COEFFICIENTS.update({n: symbols(n+"_re", real=True)
                        +I*symbols(n+"_im", real=True) for n in COMPLEX_NAMES})


def base():
    return State(Matrix.diag(*([-2]*6+[3]*4)), {}, (0,)*10, 1)


def direction_54(i, j):
    x = zeros(10)
    x[i, i], x[j, j] = 1, -1
    return State(x, {}, (0,)*10, 0), 2


def direction_phi_radial():
    return State(Matrix.diag(*([-2]*6+[3]*4)), {}, (0,)*10, 0), 60


def direction_s(imaginary=False):
    return State(zeros(10), {}, (0,)*10, I if imaginary else 1), 2


def direction_10(i, imaginary=False):
    x = [0]*10
    x[i] = I if imaginary else 1
    return State(zeros(10), {}, tuple(x), 0), 2


def direction_126(idx, imaginary=False):
    f = projected({idx: 2*I if imaginary else 2}, I)
    form = {key: tuple(z.as_real_imag()) for key, z in f.items()}
    assert norm(form) == 2
    return State(zeros(10), form, (0,)*10, 0), 2


def quadratic_slots(d):
    b = base()
    values = {t: invariant_values(state_add(b, state_scale(d, t)))
              for t in (-2, -1, 0, 1, 2)}
    return {n: simplify(quadratic({t: values[t][n] for t in values}))
            for n in REAL_NAMES+COMPLEX_NAMES}


def symbolic_potential_coeff(q, sector):
    answer = 0
    for n, raw in q.items():
        if raw == 0:
            continue
        npower = PHI_DEGREES.get(n, 0)-(2 if sector == "Phi" else
                                           1 if sector == "PhiS" else 0)
        spower = DEGREES.get(n, (0, 0))[1]-(2 if sector == "S" else
                                           1 if sector == "PhiS" else 0)
        assert npower >= 0 and spower >= 0, (n, sector)
        part = simplify(raw*A**npower*S**spower)
        if n in COMPLEX_NAMES:
            answer += COEFFICIENTS[n]*part+conjugate(COEFFICIENTS[n]*part)
        else:
            answer += COEFFICIENTS[n]*part
    return simplify(answer)


def mass_expression(q, metric, sector):
    return simplify(2*symbolic_potential_coeff(q, sector)/metric)


def bench_value(expr, c, a, s):
    values = {A: a, S: s}
    for n in REAL_NAMES:
        values[COEFFICIENTS[n]] = float(c[n])
    for n in COMPLEX_NAMES:
        values[symbols(n+"_re", real=True)] = float(c[n].real)
        values[symbols(n+"_im", real=True)] = float(c[n].imag)
    return float(expr.evalf(subs=values))


def matrix_expression(d1, d2, sector):
    q1, q2 = quadratic_slots(d1[0]), quadratic_slots(d2[0])
    combined = quadratic_slots(state_add(d1[0], d2[0]))
    cross = {n: simplify(combined[n]-q1[n]-q2[n]) for n in combined}
    cross_sector = "PhiS" if sector == "singlet" else sector
    first_sector = "Phi" if sector == "singlet" else sector
    second_sector = "S" if sector == "singlet" else sector
    return Matrix([[mass_expression(q1, d1[1], first_sector),
                    simplify(symbolic_potential_coeff(cross, cross_sector)
                             /sqrt(d1[1]*d2[1]))],
                   [simplify(symbolic_potential_coeff(cross, cross_sector)
                             /sqrt(d1[1]*d2[1])),
                    mass_expression(q2, d2[1], second_sector)]])


def main():
    c = fixed_couplings()
    omega = np.sqrt(60)
    a = stationary_omega(c, 0)/omega
    s = .1*np.sqrt(30)
    tests = [
        ("54_20prime", direction_54(0, 1), "Phi", .0252798208219),
        ("54_9", direction_54(6, 7), "Phi", .0253727511650),
        ("126_triplet", direction_126((0, 1, 2, 6, 7)), "Sigma", -.0249635399367),
    ]
    for label, direction, sector, expected in tests:
        expr = mass_expression(quadratic_slots(direction[0]), direction[1], sector)
        val = bench_value(expr, c, a, s)/60
        assert abs(val-expected) < 3e-9, (label, val, expected)
        print(label, "m2=", expr, "m2/omega2=", val)
        if label.startswith("54_"):
            stationary_mphi = (-Rational(3, 2)*COEFFICIENTS["muPhi"]*A
                                -120*COEFFICIENTS["lambdaPhi1"]*A**2
                                -14*COEFFICIENTS["lambdaPhi2"]*A**2
                                -COEFFICIENTS["lambdaPhiS"]*S**2)
            reduced = simplify(expr.subs(COEFFICIENTS["mPhi2"], stationary_mphi))
            target = ((20 if label == "54_20prime" else 80)
                      *COEFFICIENTS["lambdaPhi2"]*A**2
                      +(-15 if label == "54_20prime" else 15)
                      *COEFFICIENTS["muPhi"]*A)
            assert simplify(reduced-target) == 0
            print(label, "after_Phi_tadpole=", reduced)
    matrices = [
        ("10_sextet", direction_10(0), direction_10(0, True), "phi",
         (.00447890228337, .0107742457054)),
        ("10_bidoublet", direction_10(6), direction_10(6, True), "phi",
         (.000802114996783, .0125723032993)),
        ("126_6", direction_126((0, 6, 7, 8, 9)),
         direction_126((0, 6, 7, 8, 9), True), "Sigma",
         (1.10687123995, 1.13719556161)),
        ("126_15", direction_126((0, 1, 6, 7, 8)),
         direction_126((0, 1, 6, 7, 8), True), "Sigma",
         (.254204614829, .269366775657)),
    ]
    for label, d1, d2, sector, expected in matrices:
        mat = matrix_expression(d1, d2, sector)
        numeric = np.asarray([[bench_value(mat[i, j], c, a, s) for j in range(2)]
                              for i in range(2)], dtype=float)/60
        actual = tuple(np.linalg.eigvalsh(numeric))
        assert np.allclose(actual, expected, rtol=1e-8, atol=3e-9), (label, actual, expected)
        print(label, "M2=", mat, "eigen_m2/omega2=", actual)
    singlet = matrix_expression(direction_phi_radial(), direction_s(), "singlet")
    singlet_num = np.asarray([[bench_value(singlet[i, j], c, a, s)
                               for j in range(2)] for i in range(2)], dtype=float)/60
    assert np.allclose(np.linalg.eigvalsh(singlet_num),
                       (.00144012505765, .02), rtol=1e-8, atol=3e-9)
    pq_phase = mass_expression(quadratic_slots(direction_s(True)[0]), 2, "S")
    assert abs(bench_value(pq_phase, c, a, s)/60) < 1e-10
    print("54_S_radial", "M2=", singlet, "eigen_m2/omega2=",
          tuple(np.linalg.eigvalsh(singlet_num)))
    print("PQ_phase", "m2=", pq_phase)
    stationary_mphi = (-Rational(3, 2)*COEFFICIENTS["muPhi"]*A
                        -120*COEFFICIENTS["lambdaPhi1"]*A**2
                        -14*COEFFICIENTS["lambdaPhi2"]*A**2
                        -COEFFICIENTS["lambdaPhiS"]*S**2)
    radial_reduced = simplify(singlet[0, 0].subs(COEFFICIENTS["mPhi2"],
                                                  stationary_mphi))
    assert simplify(radial_reduced-(3*COEFFICIENTS["muPhi"]*A
             +480*COEFFICIENTS["lambdaPhi1"]*A**2
             +56*COEFFICIENTS["lambdaPhi2"]*A**2)) == 0
    print("54_radial_after_Phi_tadpole=", radial_reduced)
    print("PS_INTERCEPT_EXACT_COEFFICIENTS_PASS")


if __name__ == "__main__":
    main()
