"""Numerical polynomial bounds for one declared *different-theory* PS family.

The family passes through the positive-Higgs point at x=0.1. It varies
specified parent coefficients with x and solves all three singlet tadpoles.
It is a quadratic power-counting witness, not the physical threshold EFT.
"""

from hashlib import sha256
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
for name in ("canonical_so10_scalar_benchmark", "canonical_so10_ps_threshold_kernel",
             "canonical_so10_ps_interval_eft", "canonical_so10_full_hessian"):
    sys.path.insert(0, str(CALC / name))

from check_ps_mass_limit import fixed_couplings, load_blocks, endpoint_block
from evaluate_sm_hessian_blocks import rational_representatives
from check_candidate_split import ps_origin

PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"
X_STAR = 0.1
OMEGA = np.sqrt(60.0)


def verify_sources():
    for path, expected in (
        (CALC / "canonical_so10_scalar_reconstruction" / "PARENT_ACTION_V1.md", PARENT_HASH),
        (CALC / "canonical_so10_positive_higgs" / "POINT.json", POINT_HASH),
    ):
        assert sha256(path.read_bytes()).hexdigest() == expected, path


def family(x, original):
    """Explicit coefficient deformation: x is sigma/omega=v/omega."""
    ratio = x / X_STAR
    c = dict(original)
    for name in ("muPhi", "lambdaPhi1", "lambdaPhi2", "mphi2",
                 "muPhiPhi", "lambdaPhiphi1", "lambdaPhiphi2"):
        c[name] *= ratio**2
    for name in ("z6", "zK"):
        c[name] *= ratio
    sigma, vs = x * OMEGA, x * OMEGA
    lphi = c["lambdaPhi1"] + 7*c["lambdaPhi2"]/60
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    c["mPhi2"] = (-1.5*c["muPhi"]*OMEGA/np.sqrt(60)
                  -2*lphi*OMEGA**2-lmix*sigma**2
                  -.5*c["lambdaPhiS"]*vs**2)
    c["mSigma2"] = (-lmix*OMEGA**2-2*c["lambdaSigma1"]*sigma**2
                    -.5*c["lambdaSigmaS"]*vs**2)
    c["mS2"] = (-c["lambdaPhiS"]*OMEGA**2
                -c["lambdaSigmaS"]*sigma**2-c["lambdaS"]*vs**2)
    return c


def hessian_block(label, coeff, c, x):
    return endpoint_block(label, coeff, c, 1.0, x*np.sqrt(15/8),
                          x*np.sqrt(30))/60


def tadpole_residuals(c, x):
    sigma, vs = x*OMEGA, x*OMEGA
    lphi = c["lambdaPhi1"] + 7*c["lambdaPhi2"]/60
    lmix = c["lambdaPhiSigma1"] - c["lambdaPhiSigma2"]/4
    return (
        c["mPhi2"] + 1.5*c["muPhi"]*OMEGA/np.sqrt(60)
        + 2*lphi*OMEGA**2 + lmix*sigma**2
        + .5*c["lambdaPhiS"]*vs**2,
        c["mSigma2"] + lmix*OMEGA**2 + 2*c["lambdaSigma1"]*sigma**2
        + .5*c["lambdaSigmaS"]*vs**2,
        c["mS2"] + c["lambdaPhiS"]*OMEGA**2
        + c["lambdaSigmaS"]*sigma**2 + c["lambdaS"]*vs**2,
    )


def main():
    verify_sources()
    original = fixed_couplings()
    at_point = family(X_STAR, original)
    assert max(abs(at_point[name]-original[name]) for name in original) < 2e-10
    assert max(abs(z) for z in tadpole_residuals(original, X_STAR)) < 1e-10
    blocks = load_blocks()
    reps = rational_representatives()
    upper_min = float("inf")
    lower_bound = float("inf")
    mixing_bound = 0.0
    schur_bound = 0.0
    low_intercept = 0.0
    low_norm_bound = 0.0
    max_poly_check = 0.0
    for label, coeff in blocks.items():
        origins = [ps_origin(sector, obj) for sector, _, obj in reps[label]]
        hi = [i for i, name in enumerate(origins) if name in ("126_k1", "126_k2")]
        lo = [i for i in range(len(origins)) if i not in hi]
        # The same monomial and coefficient powers imply degree <= 4 in x.
        nodes = np.array([0., .025, .05, .075, .1])
        values = [hessian_block(label, coeff, family(x, original), x) for x in nodes]
        vandermonde = np.vander(nodes, N=5, increasing=True)
        poly = np.linalg.solve(vandermonde, np.stack(values).reshape(5, -1))
        poly = poly.reshape(5, *values[0].shape)
        at_probe = hessian_block(label, coeff, family(.037, original), .037)
        replay = sum(poly[k]*(.037**k) for k in range(5))
        max_poly_check = max(max_poly_check, float(np.max(abs(at_probe-replay))))
        if lo:
            low_intercept = max(low_intercept,
                float(np.linalg.norm(values[0][np.ix_(lo, lo)], 2)))
            local_low = sum(float(np.linalg.norm(poly[k][np.ix_(lo, lo)], 2))
                            *X_STAR**k for k in range(1, 5))
            low_norm_bound = max(low_norm_bound, local_low)
        if not hi:
            continue
        h0 = values[0][np.ix_(hi, hi)]
        eig0 = float(np.linalg.eigvalsh(h0)[0])
        upper_min = min(upper_min, eig0)
        assert not lo or np.linalg.norm(values[0][np.ix_(lo, hi)]) < 1e-9
        hh_change = sum(float(np.linalg.norm(poly[k][np.ix_(hi, hi)], 2))
                        * X_STAR**k for k in range(1, 5))
        local_lower = eig0 - hh_change
        lower_bound = min(lower_bound, local_lower)
        if lo:
            mixed = sum(float(np.linalg.norm(poly[k][np.ix_(lo, hi)], 2))
                        * X_STAR**k for k in range(1, 5))
            mixing_bound = max(mixing_bound, mixed)
            if local_lower > 0:
                schur_bound = max(schur_bound, mixed**2/local_lower)
    assert max_poly_check < 2e-10, max_poly_check
    print("DECLARED_JOINT_FAMILY_PASS_THROUGH_POINT", True)
    print("POLYNOMIAL_REPLAY_MAX_ERROR", max_poly_check)
    print("LOW_SIDE_X0_MAX_BLOCK_NORM", low_intercept,
          "UNIFORM_LOW_NORM_BOUND", low_norm_bound)
    print("HEAVY_MIN_X0", upper_min, "UNIFORM_TRIANGLE_LOWER", lower_bound)
    print("MIXING_NORM_BOUND", mixing_bound,
          "SCHUR_NORM_BOUND", schur_bound if lower_bound > 0 else None)
    for x in (0., .025, .05, .075, .1):
        c = family(x, original)
        assert max(abs(z) for z in tadpole_residuals(c, x)) < 1e-10
        minimum = float("inf")
        largest_mixed = 0.0
        largest_schur = 0.0
        largest_low_block = 0.0
        for label, coeff in blocks.items():
            h = hessian_block(label, coeff, c, x)
            origins = [ps_origin(sector, obj) for sector, _, obj in reps[label]]
            hi = [i for i, name in enumerate(origins) if name in ("126_k1", "126_k2")]
            lo = [i for i in range(len(origins)) if i not in hi]
            if lo:
                largest_low_block = max(largest_low_block, float(np.linalg.norm(
                    h[np.ix_(lo, lo)], 2)))
            if not hi:
                continue
            hhh = h[np.ix_(hi, hi)]
            minimum = min(minimum, float(np.linalg.eigvalsh(hhh)[0]))
            if lo:
                hlh = h[np.ix_(lo, hi)]
                largest_mixed = max(largest_mixed, float(np.linalg.norm(hlh, 2)))
                largest_schur = max(largest_schur, float(np.linalg.norm(
                    hlh@np.linalg.solve(hhh, hlh.conj().T), 2)))
        print("JOINT_FAMILY_POINT", x, minimum, largest_low_block,
              largest_mixed, largest_schur)
    print("DECLARED_JOINT_FAMILY_QUADRATIC_DIAGNOSTIC_ONLY")


if __name__ == "__main__":
    main()
