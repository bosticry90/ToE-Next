"""Numerical decomposition of exact PS intercept formulas at frozen point.

The cancellation index is descriptive, not a naturalness theorem:
sum(abs(contributions))/abs(sum(contributions)). All masses are normalized
by the benchmark omega^2=60. No parameter is varied by this script.
"""

from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_ps_interval_eft"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_ps_threshold_kernel"))
from probe_quadratic import stationary_omega
from check_ps_mass_limit import fixed_couplings


def show(name, contributions):
    terms = [float(z)/60 for z in contributions]
    total = sum(terms)
    index = sum(abs(z) for z in terms)/abs(total) if total else float("inf")
    print(name, "terms_over_omega2", [round(z, 12) for z in terms],
          "sum", round(total, 12), "cancellation_index", round(index, 6))


def main():
    c = fixed_couplings()
    a = stationary_omega(c, 0)/np.sqrt(60)
    s = .1*np.sqrt(30)
    show("54_20prime_tadpole_reduced",
         [20*a*a*c["lambdaPhi2"], -15*a*c["muPhi"]])
    show("54_9_tadpole_reduced",
         [80*a*a*c["lambdaPhi2"], 15*a*c["muPhi"]])
    show("54_radial_tadpole_reduced",
         [3*a*c["muPhi"], 480*a*a*c["lambdaPhi1"],
          56*a*a*c["lambdaPhi2"]])
    triplet = [2*c["mSigma2"], 120*a*a*c["lambdaPhiSigma1"],
               -30*a*a*c["lambdaPhiSigma2"], 2*c["lambdaSigmaS"]*s*s]
    show("126_triplet", triplet)
    for tag, p in (("10_sextet", -2), ("10_bidoublet", 3)):
        parts = [c["mphi2"], p*a*c["muPhiPhi"],
                 60*a*a*c["lambdaPhiphi1"], p*p*a*a*c["lambdaPhiphi2"],
                 s*s*c["lambdaVectorS"],
                 -2*s*abs(c["z6"]+p*a*c["zK"])]
        show(tag+"_lower_real_mass", parts)
    print("ASSUMPTION_COST_DECOMPOSITION_PASS")


if __name__ == "__main__":
    main()
