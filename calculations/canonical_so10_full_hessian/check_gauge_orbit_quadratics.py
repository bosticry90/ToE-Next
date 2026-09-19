"""Exact second-directional action checks along all broken gauge orbits.

This tests g^T H g=0 for each broken generator after the parent tadpoles.
It does NOT establish the stronger full vector equation H g=0. Fields are
evaluated on straight tangent lines, not finite gauge orbits.
"""

import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from sympy import I, Matrix, Rational, simplify, sqrt, symbols, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from certify_sigma_quartics import quartics
from certify_simple_invariant_slots import t_entry
from test_eta1_invariant import component
from verify_eta1_doublet_mixing import vacuum_form

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_stabilizers import form_action, generators

from check_charged_singlet_goldstone import form_at, norm, quadratic


TRIPLES = tuple(combinations(range(10), 3))


def sparse_entries(matrix):
    return [(i, j, matrix[i, j]) for i in range(10) for j in range(10)
            if matrix[i, j] != 0]


def exact_mixed_l(phi, form):
    entries = sparse_entries(phi)
    result = 0
    for i, j, x in entries:
        for k, l, y in entries:
            for triple in TRIPLES:
                ar, ai = component(form, (i, k)+triple)
                br, bi = component(form, (j, l)+triple)
                if (ar or ai) and (br or bi):
                    result += x*y*(ar+I*ai)*(br-I*bi)
    return simplify(Rational(1, 2)*result)


def phi_t(phi, form):
    return simplify(sum(x*t_entry(form, i, j)
                        for i, j, x in sparse_entries(phi)))


def raw_values(phi, form):
    p2 = (phi*phi).trace()
    p3 = (phi*phi*phi).trace()
    p4 = (phi*phi*phi*phi).trace()
    n = norm(form)
    q = quartics(form)
    return (p2, p3, p2*p2, p4, n, p2*n, exact_mixed_l(phi, form),
            q[0], q[1], q[2], q[5], phi_t(phi, form))


def quadratic_coefficients(delta_phi, delta_sigma, vacuum, phi0):
    raw = {}
    for t in (-2, -1, 0, 1, 2):
        raw[t] = raw_values(phi0+t*delta_phi,
                            form_at(vacuum, delta_sigma, t))
    return tuple(simplify(quadratic({t: raw[t][k] for t in raw}))
                 for k in range(12))


def on_shell_expression(c, parameters):
    (omega, sigma, vs, mphi, msigma, mu, lp1, lp2, lps1, lps2,
     lphs, ls1, ls2, ls3, ls4, lss) = parameters
    second = (
        mphi*omega**2*c[0]/60
        +mu*omega**3*c[1]/(60*sqrt(60))
        +lp1*omega**4*c[2]/3600
        +lp2*omega**4*c[3]/3600
        +msigma*sigma**2*c[4]/32
        +lps1*omega**2*sigma**2*c[5]/(60*32)
        +lps2*omega**2*sigma**2*c[6]/(60*32)
        +lphs*omega**2*vs**2*c[0]/(60*2)
        +sigma**4*(ls1*c[7]+ls2*c[8]+ls3*c[9]+ls4*c[10])/1024
        +lss*sigma**2*vs**2*c[4]/(32*2))
    lphi = lp1+Rational(7, 60)*lp2
    lmix = lps1-lps2/4
    masses = {
        mphi: -Rational(3, 2)*mu*omega/sqrt(60)
              -2*lphi*omega**2-lmix*sigma**2-lphs*vs**2/2,
        msigma: -lmix*omega**2-2*ls1*sigma**2-lss*vs**2/2,
    }
    return simplify(second.subs(masses))


def check_one(name, g, vacuum, phi0, parameters):
    delta_phi = g*phi0-phi0*g
    delta_sigma = form_action(g, vacuum)
    if delta_phi == zeros(10) and not delta_sigma:
        return False
    c = quadratic_coefficients(delta_phi, delta_sigma, vacuum, phi0)
    assert simplify(c[-1]) == 0, (name, "z4", c[-1])
    residue = on_shell_expression(c, parameters)
    assert residue == 0, (name, residue, c)
    return c


def main():
    parameters = symbols("omega sigma vs mPhi2 mSigma2 muPhi "
                         "lambdaPhi1 lambdaPhi2 lambdaPhiSigma1 "
                         "lambdaPhiSigma2 lambdaPhiS lambdaSigma1 "
                         "lambdaSigma2 lambdaSigma3 lambdaSigma4 "
                         "lambdaSigmaS", real=True)
    phi0 = Matrix.diag(*([-2]*6+[3]*4))
    vacuum = vacuum_form()
    assert raw_values(phi0, vacuum)[6] == -480
    patterns = Counter()
    for name, g in generators():
        result = check_one(name, g, vacuum, phi0, parameters)
        if result is not False:
            patterns[result] += 1
    # The 45 standard SO(10) basis generators all move this VEV, although
    # their orbit vectors span only 33 dimensions: the 12 stabilizer
    # generators are nontrivial linear combinations of this basis.
    assert sum(patterns.values()) == 45
    print("exact raw quadratic patterns and multiplicities:")
    for pattern, multiplicity in patterns.items():
        print(multiplicity, pattern)
    print("ALL_45_LIE_BASIS_ORBIT_QUADRATICS_PASS; orbit rank=33; H*g not yet checked")


if __name__ == "__main__":
    main()
