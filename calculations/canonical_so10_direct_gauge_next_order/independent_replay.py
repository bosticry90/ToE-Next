"""Independent-coordinate replay of the coupled SM running.

The primary implementation evolves g_i.  This replay evolves A_i=alpha_i^-1
directly with a different integrator and verifies the high-scale flow and the
central matching residual without reusing the primary gauge-coordinate ODE.
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root


HERE = Path(__file__).resolve().parent
CALC = HERE.parent
PI = math.pi
LOOP = 16 * PI**2

B1 = np.asarray([41 / 10, -19 / 6, -7.0])
B2 = np.asarray([[199 / 50, 27 / 10, 44 / 5],
                 [9 / 10, 35 / 6, 12],
                 [11 / 10, 9 / 2, -26]], dtype=float)
CYT = np.asarray([17 / 10, 3 / 2, 2.0])
CYB = np.asarray([1 / 2, 3 / 2, 2.0])
CYTAU = np.asarray([3 / 2, 1 / 2, 0.0])


def beta_inverse(_, state):
    A = state[:3]
    yt, yb, ytau, lam = state[3:]
    alpha = 1 / A
    g2 = 4 * PI * alpha
    yuk = CYT * yt**2 + CYB * yb**2 + CYTAU * ytau**2
    dA = (-B1 / (2 * PI) - (B2 @ alpha) / (8 * PI**2)
          + yuk / (32 * PI**3))
    dyt = yt * (4.5 * yt**2 + 1.5 * yb**2 + ytau**2
                - 17 / 20 * g2[0] - 9 / 4 * g2[1] - 8 * g2[2]) / LOOP
    dyb = yb * (1.5 * yt**2 + 4.5 * yb**2 + ytau**2
                - 1 / 4 * g2[0] - 9 / 4 * g2[1] - 8 * g2[2]) / LOOP
    dytau = ytau * (3 * yt**2 + 3 * yb**2 + 2.5 * ytau**2
                    - 9 / 4 * g2[0] - 9 / 4 * g2[1]) / LOOP
    tr2 = 3 * yt**2 + 3 * yb**2 + ytau**2
    tr4 = 3 * yt**4 + 3 * yb**4 + ytau**4
    dlam = (24 * lam**2 - (9 / 5 * g2[0] + 9 * g2[1]) * lam
            + 27 / 200 * g2[0]**2 + 9 / 20 * g2[0] * g2[1]
            + 9 / 8 * g2[1]**2 + 4 * lam * tr2 - 2 * tr4) / LOOP
    return np.concatenate((dA, [dyt, dyb, dytau, dlam]))


def main():
    result = json.loads((HERE / "next_order.json").read_text())
    A0 = np.asarray(json.loads(
        (CALC / "canonical_so10_direct_gauge_matching" /
         "direct_matching.json").read_text()
    )["frozen_inputs_MZ"]["alpha_inverse_GUT_order_1_2_3"])
    MZ = 91.1876
    mt = result["rge"]["weak_scale_boundary_mu_GeV"]
    weak = np.asarray(result["rge"]["weak_scale_boundary_yt_yb_ytau_lambda"])
    tmt = math.log(mt / MZ)

    def mismatch(low):
        sol = solve_ivp(beta_inverse, (0, tmt), np.concatenate((A0, low)),
                        method="DOP853", rtol=2e-12, atol=1e-14)
        assert sol.success
        return sol.y[3:, -1] - weak

    low = root(mismatch, result["rge"]["solved_MZ_boundary_yt_yb_ytau_lambda"])
    assert low.success
    sol = solve_ivp(beta_inverse, (0, math.log(1e19 / MZ)),
                    np.concatenate((A0, low.x)), method="DOP853",
                    rtol=2e-12, atol=1e-14, dense_output=True)
    assert sol.success

    scalar_log = json.loads((CALC / "canonical_so10_matrix_threshold" /
                             "scalar_matrix_log.json").read_text())
    scalar = np.asarray(scalar_log["lambda_scalar_SM_order_1_2_3"])
    bscalar = np.asarray([377 / 30, 77 / 6, 79 / 6])
    vectors = [(0.005, np.asarray([14 / 5, 0, 1.])),
               (0.025, np.zeros(3)),
               (50 / 120, np.asarray([5., 3., 2.])),
               (50.6 / 120, np.asarray([1 / 5, 3., 2.]))]

    def residual(x, kappa=1.0):
        g, omega = np.exp(x)
        lam_s = scalar - 6 * bscalar * math.log(kappa)
        lam_v = sum((ind * (1 - 21 * math.log(g * math.sqrt(m2) / kappa))
                     for m2, ind in vectors), np.zeros(3))
        high = 4 * PI / g**2 - (lam_s + lam_v) / (12 * PI)
        return high - sol.sol(math.log(kappa * omega / MZ))[:3]

    central = result["central_refit"]
    fit = least_squares(residual, np.log([central["g10"], central["omega_GeV"]]),
                        xtol=1e-13, ftol=1e-13, gtol=1e-13)
    rr = residual(fit.x)
    reference = np.asarray(central["residual_inverse_couplings"])
    assert np.max(abs(rr - reference)) < 2e-8
    assert abs(np.exp(fit.x[0]) - central["g10"]) < 2e-9
    assert abs(np.exp(fit.x[1]) / central["omega_GeV"] - 1) < 2e-8
    print("INVERSE_COUPLING_REPLAY_PASS")
    print("g10 omega", *np.exp(fit.x))
    print("residual", rr.tolist())


if __name__ == "__main__":
    main()
