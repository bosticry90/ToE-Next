"""Exact 126-only Hessian check on one charged SU(2)R gauge orbit.

The chosen generator (6,8) commutes with Phi0. Evaluate each parent
invariant on Sigma0+t*(g Sigma0), extract the t^2 coefficient exactly,
and substitute the action-derived Sigma tadpole. This is one orbit check,
not the complete charged/colored Hessian block.
"""

import sys
from pathlib import Path

from sympy import Rational, simplify, symbols, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from certify_sigma_quartics import quartics
from certify_simple_invariant_slots import pair_counts, t_entry
from verify_eta1_doublet_mixing import vacuum_form

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_stabilizers import form_action


def form_at(v, dv, t):
    out = {}
    for key in set(v) | set(dv):
        a, b = v.get(key, (0, 0))
        x, y = dv.get(key, (0, 0))
        z = (a+t*x, b+t*y)
        if z != (0, 0):
            out[key] = z
    return out


def quadratic(values):
    # f(t) has degree at most four. This 5-point central formula returns
    # the exact coefficient of t^2 (not f'' itself).
    return Rational(1, 24)*(-values[2]+16*values[1]-30*values[0]
                            +16*values[-1]-values[-2])


def norm(form):
    return sum(a*a+b*b for a, b in form.values())


def main():
    v = vacuum_form()
    g = zeros(10)
    g[6, 8], g[8, 6] = 1, -1
    dv = form_action(g, v)
    assert dv
    d = [-2]*6+[3]*4
    vals = {}
    for t in (-2, -1, 0, 1, 2):
        f = form_at(v, dv, t)
        pair = pair_counts(f)
        q = quartics(f)
        vals[t] = (
            norm(f),
            sum(d[i]*d[j]*pair[i, j] for i in range(10)
                for j in range(i+1, 10)),
            q[0], q[1], q[2], q[5],
            sum(d[i]*t_entry(f, i, i) for i in range(10)),
        )
    coeffs = [simplify(quadratic({t: vals[t][k] for t in vals}))
              for k in range(7)]
    print("raw t^2 coefficients N,L,Q0,Q1,Q2,X131,PhiT:", coeffs)
    omega, sigma, vs = symbols("omega sigma vs", real=True, nonzero=True)
    m, lps1, lps2, ls1, ls2, ls3, ls4, lss = symbols(
        "mSigma2 lambdaPhiSigma1 lambdaPhiSigma2 lambdaSigma1 "
        "lambdaSigma2 lambdaSigma3 lambdaSigma4 lambdaSigmaS", real=True)
    # Phi=omega diag(d)/sqrt(60), Sigma=sigma V/(4sqrt(2)),
    # S=vs/sqrt(2), so the parent action fixes these scale factors.
    second = ((m+lps1*omega**2+lss*vs**2/2)*sigma**2*coeffs[0]/32
              +lps2*omega**2*sigma**2*coeffs[1]/(60*32)
              +sigma**4*(ls1*coeffs[2]+ls2*coeffs[3]
                           +ls3*coeffs[4]+ls4*coeffs[5])/1024)
    assert coeffs[6] == 0  # z4 term cannot lift this gauge direction.
    stationarity_mass = -lps1*omega**2+lps2*omega**2/4-2*ls1*sigma**2-lss*vs**2/2
    assert simplify(second.subs(m, stationarity_mass)) == 0
    print("CHARGED_SU2R_GOLDSTONE_DIRECTION_PASS after Sigma tadpole")


if __name__ == "__main__":
    main()
