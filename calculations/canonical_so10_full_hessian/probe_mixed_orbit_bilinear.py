"""Exact adversarial mixed Hessian probes against gauge orbit vectors.

Checks g^T H h=0 for one deterministic generic Phi+Sigma variation h and
representatives of each raw orbit pattern. This does not certify H*g=0 on
the full 328-real-dimensional tangent (phi and S probes are absent).
"""

import sys
from pathlib import Path

from sympy import Matrix, simplify, symbols, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))

from certify_sigma_quartics import generated_form
from verify_eta1_doublet_mixing import vacuum_form

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_stabilizers import form_action, generators

from check_gauge_orbit_quadratics import (
    on_shell_expression, quadratic_coefficients,
)
from check_charged_singlet_goldstone import form_at


def main():
    parameters = symbols("omega sigma vs mPhi2 mSigma2 muPhi "
                         "lambdaPhi1 lambdaPhi2 lambdaPhiSigma1 "
                         "lambdaPhiSigma2 lambdaPhiS lambdaSigma1 "
                         "lambdaSigma2 lambdaSigma3 lambdaSigma4 "
                         "lambdaSigmaS", real=True)
    phi0 = Matrix.diag(*([-2]*6+[3]*4))
    vacuum = vacuum_form()
    hphi = zeros(10)
    hphi[0, 0], hphi[1, 1] = 1, -1
    hphi[0, 6] = hphi[6, 0] = 2
    hphi[2, 8] = hphi[8, 2] = -1
    hsigma = generated_form(31, 8)
    ch = quadratic_coefficients(hphi, hsigma, vacuum, phi0)
    candidates = {(0, 1), (0, 2), (0, 6), (6, 8)}
    tested = 0
    for name, g in generators():
        if name not in candidates:
            continue
        dphi = g*phi0-phi0*g
        dsigma = form_action(g, vacuum)
        cg = quadratic_coefficients(dphi, dsigma, vacuum, phi0)
        csum = quadratic_coefficients(dphi+hphi,
                                       form_at(dsigma, hsigma, 1),
                                       vacuum, phi0)
        cross = tuple(simplify(csum[k]-cg[k]-ch[k]) for k in range(12))
        assert cross[-1] == 0, (name, "z4", cross[-1])
        assert on_shell_expression(cross, parameters) == 0, (name, cross)
        tested += 1
        print(name, "mixed Phi+Sigma probe PASS")
    assert tested == len(candidates)
    print("FOUR_MIXED_ORBIT_BILINEAR_PROBES_PASS; not full H*g")


if __name__ == "__main__":
    main()
