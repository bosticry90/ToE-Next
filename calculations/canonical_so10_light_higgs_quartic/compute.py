"""Tree-level relaxed Higgs quartic at the frozen canonical Stage 2 point.

All polynomial samples are exact rational tensor states evaluated through the
frozen parent invariant implementation. Only the final contractions use
high-precision numerical coefficients (the tuning is algebraic).
"""

from functools import lru_cache
from pathlib import Path
import sys

import mpmath as mp
from sympy import I, N, Rational, conjugate, sympify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "canonical_so10_full_hessian"))
sys.path.insert(0, str(ROOT / "canonical_so10_scalar_benchmark"))

from compile_sm_multiplicity_representatives import RAISING, action, kinetic_inner
from evaluate_sm_hessian_blocks import (
    block, rational_representatives, realified_representative,
)
from parent_bilinear_oracle import (
    State, COMPLEX_NAMES, REAL_NAMES, invariant_values, state_add,
    vacuum_state, zero_state,
)
from replay_candidate_exact import kinetic_diag
from replay_stage2_exact import effective_coefficients, polynomial_and_root

mp.mp.dps = 70
LABEL_H = (0, 0, 1, -3)
LABEL_S = (0, 0, 0, 0)
LABEL_T0 = (0, 0, 2, 0)
LABEL_TN = (0, 0, 2, -6)
PRECISIONS = (11, 15)


def mpval(value):
    z = sympify(value)
    a, b = z.as_real_imag()
    return mp.mpc(str(N(a, 75)), str(N(b, 75)))


def rat(value, digits):
    return Rational(mp.nstr(value, digits + 4, strip_zeros=False)).limit_denominator(10**digits)


def scale(state, number):
    return State(state.Phi * number,
                 {idx: (number*a, number*b)
                  for idx, (a, b) in state.Sigma.items()},
                 tuple(number*z for z in state.phi), number*state.S)


def add(*states):
    out = zero_state()
    for one in states:
        out = state_add(out, one)
    return out


def canonical_norm2(state, b, s):
    form = {idx: a+I*c for idx, (a, c) in state.Sigma.items()}
    phi = sum(conjugate(z)*z for z in state.phi)
    return mp.re(mpval(sum(state.Phi.multiply_elementwise(state.Phi))
                            +2*b*b*kinetic_inner(form, form, "form")
                            +2*phi+2*s*s*conjugate(state.S)*state.S))


def parent_coefficients_numeric():
    _, _, root, _ = polynomial_and_root()
    c, b, s = effective_coefficients(root)
    return {name: mpval(value) for name, value in c.items()}, mpval(b).real, mpval(s).real


@lru_cache(maxsize=1)
def direct_light_eigenvector():
    # The direct-parent block avoids a double-precision compiler eigenvector
    # whose O(1e-15) residual leaks into the Goldstone-source Ward test.
    u_mp = polynomial_and_root()[3]
    u_rational = Rational(mp.nstr(u_mp, 65))
    coefficients, b_exact, s_exact = effective_coefficients(u_rational)
    hraw = block(LABEL_H, coefficients)
    g = kinetic_diag(LABEL_H, b_exact, s_exact)
    h = mp.matrix(4)
    for i in range(4):
        for j in range(4):
            h[i, j] = mpval(hraw[i, j])/mp.sqrt(g[i]*g[j])
    values, vectors = mp.eighe(h)
    assert abs(values[0]) < mp.mpf("1e-55") and values[1] > 1, values
    c = [vectors[j, 0]/mp.sqrt(g[j]) for j in range(4)]
    print("DIRECT_PARENT_LIGHT_EIGEN", mp.nstr(values[0], 12), flush=True)
    return c, values


def light_state(digits, b, s):
    c, values = direct_light_eigenvector()
    reps = rational_representatives()[LABEL_H]
    basis = [realified_representative(sector, obj) for sector, _, obj in reps]
    # The calculated block is real at this point to double precision; retain
    # both real and imaginary coefficients if this changes in later replays.
    states = []
    for value, tangent in zip(c, basis):
        states.append(add(scale(tangent.real, rat(value.real, digits)),
                          scale(tangent.imag, -rat(value.imag, digits))))
    neutral = add(*states)
    phase = add(*(add(scale(tangent.real, rat(-value.imag, digits)),
                       scale(tangent.imag, -rat(value.real, digits)))
                  for value, tangent in zip(c, basis)))
    assert abs(canonical_norm2(neutral, b, s)-mp.mpf("0.5")) < mp.mpf("1e-8")
    assert abs(canonical_norm2(phase, b, s)-mp.mpf("0.5")) < mp.mpf("1e-8")
    return neutral, phase, values


def heavy_basis():
    reps = rational_representatives()
    sing = [realified_representative(sector, obj)
            for sector, _, obj in reps[LABEL_S]]
    assert [x[0] for x in reps[LABEL_S]] == [
        "Phi", "Sigma", "SigmaBar", "S", "SBar"]
    s_basis = [sing[0].real, sing[1].real, sing[1].imag,
               sing[3].real, sing[3].imag]
    # Lower the SU(2)_L highest-weight Y=0 triplet once to its Q=0 member.
    sector, _, obj = reps[LABEL_T0][0]
    assert sector == "Phi"
    lowered = action(RAISING[2].conjugate(), obj, "matrix")
    t0 = realified_representative(sector, lowered)
    assert t0.imag == zero_state()
    tn = [realified_representative(sector, obj)
          for sector, _, obj in reps[LABEL_TN]]
    assert len(tn) == 2
    return (s_basis, [t0.real],
            [tn[0].real, tn[0].imag, tn[1].real, tn[1].imag])


def potential(state, coefficients):
    inv = invariant_values(state)
    result = sum(coefficients[n]*mpval(inv[n]) for n in REAL_NAMES)
    result += sum(2*mp.re(coefficients[n]*mpval(inv[n])) for n in COMPLEX_NAMES)
    assert abs(mp.im(result)) < mp.mpf("1e-45")*max(1, abs(result))
    return mp.re(result)


def quartic_coeff(potential_at):
    p0 = potential_at(0)
    s1 = potential_at(1)+potential_at(-1)-2*p0
    s2 = potential_at(2)+potential_at(-2)-2*p0
    return (s2-4*s1)/24


def quadratic_coeff(potential_at):
    p0 = potential_at(0)
    s1 = potential_at(1)+potential_at(-1)-2*p0
    s2 = potential_at(2)+potential_at(-2)-2*p0
    return (16*s1-s2)/24


class Evaluator:
    def __init__(self, coefficients):
        self.c = coefficients
        self.base = vacuum_state()
        self.calls = 0

    def value(self, direction):
        self.calls += 1
        return potential(add(self.base, direction), self.c)

    def q(self, direction):
        return quadratic_coeff(lambda t: self.value(scale(direction, t)))

    def direct4(self, h):
        return quartic_coeff(lambda t: self.value(scale(h, t)))

    def source(self, h, x):
        def d(t):
            center = scale(h, t)
            return (self.value(add(center, x))-
                    self.value(add(center, scale(x, -1))))/2
        return (d(1)+d(-1)-2*d(0))/2


def hessian_block(evaluator, directions):
    q = [evaluator.q(x) for x in directions]
    m = len(q)
    return mp.matrix(m, m), q


def build_hessian(evaluator, groups):
    out = []
    for group in groups:
        matrix, q = hessian_block(evaluator, group)
        for i in range(len(group)):
            matrix[i, i] = 2*q[i]
            for j in range(i):
                matrix[i, j] = matrix[j, i] = (
                    evaluator.q(add(group[i], group[j]))-q[i]-q[j])
        out.append(matrix)
        print("HESSIAN_BLOCK", len(group), "calls", evaluator.calls, flush=True)
    return out


def relaxed(evaluator, h, groups, matrices):
    direct = evaluator.direct4(h)
    correction = mp.mpf(0)
    sources = []
    solves = []
    for group, H in zip(groups, matrices):
        j = mp.matrix([evaluator.source(h, x) for x in group])
        eig, U = mp.eigsy(H)
        scale0 = max(abs(x) for x in eig)
        zeros0 = [i for i, value in enumerate(eig)
                  if abs(value) < mp.mpf("1e-40")*scale0]
        if len(group) == 5:
            assert len(zeros0) == 2, (eig, zeros0)
        else:
            assert not zeros0, (eig, zeros0)
        inv = mp.matrix(len(group), len(group))
        block_correction = mp.mpf(0)
        max_null_source = mp.mpf(0)
        for k, eigenvalue in enumerate(eig):
            overlap = sum(U[i, k]*j[i] for i in range(len(group)))
            if k in zeros0:
                max_null_source = max(max_null_source, abs(overlap))
                assert abs(overlap) < mp.mpf("1e-16"), (k, overlap)
            else:
                assert eigenvalue > 0
                block_correction += overlap**2/(2*eigenvalue)
                for i in range(len(group)):
                    for l in range(len(group)):
                        inv[i, l] += U[i, k]*U[l, k]/eigenvalue
        sources.append(j)
        solves.append(-inv*j)
        correction += block_correction
        print("SOURCE_BLOCK", len(group), "j_norm", mp.nstr(mp.norm(j), 15),
              "eigen_min_positive", mp.nstr(min(x for x in eig if x > mp.mpf("1e-20")), 15),
              "quartic_subtraction_raw", mp.nstr(block_correction, 20),
              "max_null_source", mp.nstr(max_null_source, 8),
              "calls", evaluator.calls, flush=True)
    return direct, correction, direct-correction, sources, solves


def schur_correction(H, j):
    eigenvalues, U = mp.eigsy(H)
    threshold = mp.mpf("1e-40")*max(abs(x) for x in eigenvalues)
    result = mp.mpf(0)
    for k, value in enumerate(eigenvalues):
        projection = sum(U[i, k]*j[i] for i in range(len(j)))
        if abs(value) <= threshold:
            assert abs(projection) < mp.mpf("1e-16")
        else:
            result += projection**2/(2*value)
    return result


def main():
    c, b, s = parent_coefficients_numeric()
    groups = heavy_basis()
    print("HEAVY_NEUTRAL_SOURCE_DIMENSIONS", [len(g) for g in groups], flush=True)
    evaluator = Evaluator(c)
    matrices = build_hessian(evaluator, groups)
    output = {}
    for digits in PRECISIONS:
        h, phase, eig = light_state(digits, b, s)
        print("LIGHT", digits, "m2", eig[0], "kinetic", mp.nstr(canonical_norm2(h,b,s),20), flush=True)
        direct, correction, effective, sources, solves = relaxed(
            evaluator, h, groups, matrices)
        kinetic = canonical_norm2(h, b, s)
        lam = 4*effective/(kinetic**2)
        print("QUARTIC", digits, "direct", mp.nstr(4*direct/kinetic**2, 25),
              "heavy_subtraction", mp.nstr(4*correction/kinetic**2, 25),
              "relaxed", mp.nstr(lam, 30), flush=True)
        output[str(digits)] = (lam, direct, correction)
        if digits == PRECISIONS[-1]:
            # An invertible heavy-coordinate shear cannot change the
            # relaxed quartic, even in the singular Goldstone block.
            transformed = mp.mpf(0)
            for H, j in zip(matrices, sources):
                T = mp.eye(len(j))
                if len(j) > 1:
                    T[0, 1] = mp.mpf(2)/3
                    T[1, 0] = -mp.mpf(1)/5
                transformed += schur_correction(T.T*H*T, T.T*j)
            assert abs(transformed-correction) < mp.mpf("1e-16")
            print("HEAVY_BASIS_SHEAR_REPLAY", mp.nstr(transformed, 30), flush=True)
            # Independent polynomial-along-valley coefficient: it uses one
            # assembled heavy shift and nine direct parent evaluations,
            # rather than the source/Hessian contraction.
            xopt = add(*(scale(x, rat(solve[i], 15))
                         for group, solve in zip(groups, solves)
                         for i, x in enumerate(group)))
            f = lambda t: evaluator.value(add(scale(h, Rational(t)),
                                             scale(xopt, Rational(t*t))))
            nodes = list(range(-4, 5))
            vals = mp.matrix([f(t) for t in nodes])
            vand = mp.matrix([[mp.mpf(t)**k for k in range(9)] for t in nodes])
            replay4 = mp.lu_solve(vand, vals)[4]
            assert abs(replay4-effective) < mp.mpf("1e-8"), (replay4, effective)
            print("VALLEY_POLYNOMIAL_REPLAY", mp.nstr(replay4, 30), flush=True)
            # Higgs phase rotation is a nontrivial gauge/rephasing check.
            _, _, phased, _, _ = relaxed(evaluator, phase, groups, matrices)
            assert abs(phased-effective) < mp.mpf("1e-7"), (phased, effective)
            print("HIGGS_PHASE_REPLAY", mp.nstr(phased, 30), flush=True)
    assert abs(output["11"][0]-output["15"][0]) < mp.mpf("1e-6")
    print("FINAL_LAMBDA_EFF", mp.nstr(output["15"][0], 35),
          "total_parent_evaluations", evaluator.calls, flush=True)


if __name__ == "__main__":
    main()
