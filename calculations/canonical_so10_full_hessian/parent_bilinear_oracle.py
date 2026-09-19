"""Exact, calculation-local second-directional oracle for PARENT_ACTION_V1.

This evaluates all 24 Hermitian and five complex parent invariant
monomials on exact raw tensor states. B(u,v) is obtained by polarization of
the t^2 coefficient of V(vacuum+t direction). Raw VEVs are Phi=diag(-2x6,
+3x4), Sigma=V, phi=0, S=1, i.e. omega=sqrt(60), sigma=4sqrt(2), v=sqrt(2)
in the normalized convention. Tangent coordinates use the same raw tensors.

This module supplies an oracle, not a complete SM-irrep basis or spectrum.
"""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import sys

from sympy import I, Matrix, Rational, conjugate, simplify, zeros

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "canonical_so10_scalar_reconstruction"
VACUUM = HERE.parent / "canonical_so10_vacuum_kernel"
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(VACUUM))

from certify_sigma_quartics import quartics
from certify_simple_invariant_slots import k_entry, t_entry
from test_eta1_invariant import conjugate as form_conjugate, contraction_vector_on_a
from verify_eta1_doublet_mixing import vacuum_form

from check_charged_singlet_goldstone import form_at, norm, quadratic
from check_gauge_orbit_quadratics import exact_mixed_l, sparse_entries


PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
assert sha256((PARENT / "PARENT_ACTION_V1.md").read_bytes()).hexdigest() == PARENT_HASH

REAL_NAMES = (
    "mPhi2", "mSigma2", "mphi2", "mS2", "muPhi", "muPhiPhi",
    "lambdaPhi1", "lambdaPhi2", "lambdaPhiSigma1", "lambdaPhiSigma2",
    "lambdaPhiphi1", "lambdaPhiphi2", "lambdaPhiS", "lambdaSigma1",
    "lambdaSigma2", "lambdaSigma3", "lambdaSigma4", "lambdaSigmaphi1",
    "lambdaSigmaphi2", "lambdaPhiVector1", "lambdaPhiVector2",
    "lambdaSigmaS", "lambdaVectorS", "lambdaS",
)
COMPLEX_NAMES = ("z6", "z4", "zK", "zEta", "zD")
assert len(REAL_NAMES) == 24 and len(COMPLEX_NAMES) == 5


@dataclass(frozen=True)
class State:
    Phi: Matrix
    Sigma: dict
    phi: tuple
    S: object


def zero_state():
    return State(zeros(10), {}, (0,)*10, 0)


def vacuum_state():
    return State(Matrix.diag(*([-2]*6+[3]*4)), vacuum_form(), (0,)*10, 1)


def state_add(a, b):
    return State(a.Phi+b.Phi, form_at(a.Sigma, b.Sigma, 1),
                 tuple(x+y for x, y in zip(a.phi, b.phi)), a.S+b.S)


def state_scale(a, k):
    assert isinstance(k, int)
    return State(k*a.Phi,
                 {key: (k*z[0], k*z[1]) for key, z in a.Sigma.items()
                  if k*z[0] or k*z[1]},
                 tuple(k*x for x in a.phi), k*a.S)


def real_part_check(name, z):
    assert simplify(z-conjugate(z)) == 0, (name, z)
    return simplify(z)


def invariant_values(state):
    P, F, x, s = state.Phi, state.Sigma, state.phi, state.S
    p2 = (P*P).trace()
    p3 = (P*P*P).trace()
    p4 = (P*P*P*P).trace()
    n = norm(F)
    u = sum(conjugate(z)*z for z in x)
    t = sum(z*z for z in x)
    abs_s2 = conjugate(s)*s
    q = quartics(F)
    support = tuple(i for i, z in enumerate(x) if z != 0)
    phi_phi_herm = sum(conjugate(x[i])*P[i, j]*x[j]
                        for i in support for j in support)
    P2 = P*P
    phi_P2_phi = sum(conjugate(x[i])*P2[i, j]*x[j]
                       for i in support for j in support)
    kterm = sum(conjugate(x[i])*k_entry(F, i, j)*x[j]
                for i in support for j in support)
    tcache = {}
    def tval(i, j):
        key = (i, j)
        if key not in tcache:
            tcache[key] = t_entry(F, i, j)
        return tcache[key]
    phi_t = sum(value*tval(i, j) for i, j, value in sparse_entries(P))
    vector_t = sum(x[i]*tval(i, j)*x[j]
                   for i in support for j in support)
    vector_P = sum(P[i, j]*x[i]*x[j]
                   for i in support for j in support)
    eta = sum(x[i]*complex_pair(contraction_vector_on_a(
                  F, F, form_conjugate(F), i)) for i in support)
    result = {
        "mPhi2": p2, "mSigma2": n, "mphi2": u, "mS2": abs_s2,
        "muPhi": p3, "muPhiPhi": phi_phi_herm,
        "lambdaPhi1": p2*p2, "lambdaPhi2": p4,
        "lambdaPhiSigma1": p2*n,
        "lambdaPhiSigma2": exact_mixed_l(P, F),
        "lambdaPhiphi1": p2*u,
        "lambdaPhiphi2": phi_P2_phi,
        "lambdaPhiS": p2*abs_s2,
        "lambdaSigma1": q[0], "lambdaSigma2": q[1],
        "lambdaSigma3": q[2], "lambdaSigma4": q[5],
        "lambdaSigmaphi1": n*u,
        "lambdaSigmaphi2": kterm,
        "lambdaPhiVector1": u*u,
        "lambdaPhiVector2": t*conjugate(t),
        "lambdaSigmaS": n*abs_s2,
        "lambdaVectorS": u*abs_s2,
        "lambdaS": abs_s2*abs_s2,
        "z6": t*conjugate(s),
        "z4": phi_t*s,
        "zK": vector_P*conjugate(s),
        "zEta": eta,
        "zD": vector_t,
    }
    assert set(result) == set(REAL_NAMES) | set(COMPLEX_NAMES)
    for name in REAL_NAMES:
        result[name] = real_part_check(name, result[name])
    return result


def complex_pair(z):
    return z[0]+I*z[1]


_q_cache = {}


def second_coefficients(direction):
    """Return one coefficient of t^2 for each frozen parent monomial."""
    key = state_key(direction)
    if key in _q_cache:
        return _q_cache[key]
    base = vacuum_state()
    samples = {t: invariant_values(state_add(base, state_scale(direction, t)))
               for t in (-2, -1, 0, 1, 2)}
    result = {name: simplify(quadratic({t: samples[t][name] for t in samples}))
              for name in REAL_NAMES+COMPLEX_NAMES}
    _q_cache[key] = result
    return result


def state_key(a):
    return (tuple(a.Phi), tuple(sorted(a.Sigma.items())), a.phi, a.S)


def bilinear_coefficients(u, v):
    """Exact B(u,v) per monomial; complex slots still need Hermitian completion."""
    qu = second_coefficients(u)
    qv = second_coefficients(v)
    qs = second_coefficients(state_add(u, v))
    return {name: simplify(qs[name]-qu[name]-qv[name])
            for name in REAL_NAMES+COMPLEX_NAMES}


def parent_bilinear(u, v, coefficients):
    """Physical real bilinear for chosen exact real and complex couplings."""
    b = bilinear_coefficients(u, v)
    assert set(coefficients) == set(REAL_NAMES) | set(COMPLEX_NAMES)
    return simplify(sum(coefficients[n]*b[n] for n in REAL_NAMES)
                    +sum(coefficients[n]*b[n]
                         +conjugate(coefficients[n]*b[n])
                         for n in COMPLEX_NAMES))


if __name__ == "__main__":
    base = invariant_values(vacuum_state())
    assert base["mPhi2"] == 60 and base["mSigma2"] == 32
    assert base["lambdaPhiSigma2"] == -480
    assert base["lambdaSigma1"] == 1024
    assert all(base[n] == 0 for n in COMPLEX_NAMES)
    print("ALL_29_PARENT_MONOMIALS_EVALUATED_AT_RAW_VACUUM; 34 real coefficient directions")
