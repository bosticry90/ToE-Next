"""Exploratory same-coefficient PS background and quadratic scaling probe.

This reuses the previously certified SM block compiler. The sigma=0
spectrum is a PS-representation diagnostic, not an admitted threshold ledger.
"""

from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_ps_threshold_kernel"))
from check_ps_mass_limit import clusters_at, fixed_couplings, load_blocks


def stationary_omega(c, sigma):
    lphi = c["lambdaPhi1"] + 7*c["lambdaPhi2"]/60
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    vs = .1*np.sqrt(60)
    polynomial = [4*lphi, 3*c["muPhi"]/np.sqrt(60),
                  2*c["mPhi2"] + 2*lmix*sigma**2
                  + c["lambdaPhiS"]*vs**2]
    roots = np.roots(polynomial)
    real = [float(z.real) for z in roots if abs(z.imag) < 1e-10 and z.real > 0]
    assert real, (sigma, roots)
    return min(real, key=lambda z: abs(z-np.sqrt(60)))


def tadpole_scaling_family(c, x):
    """A *different-theory* family varying only three relevant masses.

    It passes through the frozen point at x=.1. It is a power-counting
    comparator, never an alternative same-coefficient threshold spectrum.
    """
    q = dict(c)
    omega = np.sqrt(60)
    sigma, vs = x*omega, .1*omega
    lphi = q["lambdaPhi1"] + 7*q["lambdaPhi2"]/60
    lmix = q["lambdaPhiSigma1"] - q["lambdaPhiSigma2"]/4
    q["mPhi2"] = (-1.5*q["muPhi"]*omega/np.sqrt(60)
                   -2*lphi*omega**2-lmix*sigma**2
                   -.5*q["lambdaPhiS"]*vs**2)
    q["mSigma2"] = (-lmix*omega**2-2*q["lambdaSigma1"]*sigma**2
                     -.5*q["lambdaSigmaS"]*vs**2)
    q["mS2"] = (-q["lambdaPhiS"]*omega**2
                -q["lambdaSigmaS"]*sigma**2-q["lambdaS"]*vs**2)
    return q


def main():
    c = fixed_couplings()
    omega = np.sqrt(60)
    sigma = .1*omega
    vs = .1*omega
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    lhs_sigma = (2*c["mSigma2"]+2*lmix*omega**2
                 +4*c["lambdaSigma1"]*sigma**2
                 +c["lambdaSigmaS"]*vs**2)
    lhs_s = (c["mS2"]+c["lambdaPhiS"]*omega**2
             +c["lambdaSigmaS"]*sigma**2+c["lambdaS"]*vs**2)
    assert abs(lhs_sigma) < 1e-11 and abs(lhs_s) < 1e-11
    omega_ps = stationary_omega(c, 0.0)
    assert abs(stationary_omega(c, sigma)-omega) < 1e-10
    sigma_curvature = (2*c["mSigma2"]+2*lmix*omega_ps**2
                       +c["lambdaSigmaS"]*vs**2)
    print("omega_PS/omega_benchmark", omega_ps/omega)
    print("L_mix", lmix)
    print("sigma_radial_coefficient_at_PS", sigma_curvature,
          "over_omega2", sigma_curvature/omega**2)
    print("PS_stationary_singlet_check", lhs_s)
    blocks = load_blocks()
    clusters = clusters_at(blocks, c, omega_ps/omega, 0.0, .1*np.sqrt(30))
    negative = [(mass, dim) for mass, dim, _ in clusters if mass < -1e-10]
    zero = sum(dim for mass, dim, _ in clusters if abs(mass) < 1e-10)
    assert len(negative) == 1 and negative[0][1] == 120, negative
    assert zero == 25, zero
    print("PS_stationary_clusters", len(clusters), "real_dim", sum(x[1] for x in clusters))
    for mass, dim, _ in clusters:
        print(f"{mass:+.12g} {dim}")
    family = tadpole_scaling_family(c, .1)
    assert max(abs(family[key]-c[key]) for key in ("mPhi2", "mSigma2", "mS2")) < 1e-11
    for x in (0.0, .05):
        scaled = tadpole_scaling_family(c, x)
        alt = clusters_at(blocks, scaled, 1, x*np.sqrt(15/8), .1*np.sqrt(30))
        if x == 0:
            assert sum(dim for mass, dim, _ in alt if abs(mass) < 1e-10) == 145
        print("DIFFERENT_THEORY_TADPOLE_FAMILY", "x", x,
              "clusters", len(alt), "real_dim", sum(row[1] for row in alt))
        for mass, dim, _ in alt:
            print(f"{mass:+.12g} {dim}")


if __name__ == "__main__":
    main()
