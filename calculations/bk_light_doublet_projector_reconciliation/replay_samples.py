"""Bounded replay of printed Babu--Khan scalar samples (arXiv:1507.06712v2).

Uses the published full doublet matrix and selected non-doublet mass formula,
never the disputed reduced Eq. (36). Input tables contain rounded values;
the unprinted 10_H common mass m^2 is eliminated by imposing one zero mode.
This is not an independent SO(10)-tensor expansion of the scalar potential.
"""

from math import sqrt

import numpy as np


CASES = {
    "table_2_as_printed": dict(
        l2=-0.17, l4=0.48, lp=0.17, beta=1.25e-5, chi4=-0.55,
        eta1=-0.002, chi6=-2.67e14, gamma1=-0.38, gamma2=0.52,
        sigma=8.65e14, omega=1.38e16, vs=9.36e10,
        printed_doublets=(2.23e14, 8.12e13, 1.13e12),
        printed_triplet=2.17e14,
    ),
    "table_2_sigma_exponent_minus_one_hypothesis": dict(
        l2=-0.17, l4=0.48, lp=0.17, beta=1.25e-5, chi4=-0.55,
        eta1=-0.002, chi6=-2.67e14, gamma1=-0.38, gamma2=0.52,
        sigma=8.65e13, omega=1.38e16, vs=9.36e10,
        printed_doublets=(2.23e14, 8.12e13, 1.13e12),
        printed_triplet=2.17e14,
    ),
    "table_4_as_printed": dict(
        l2=-0.17, l4=0.49, lp=0.17, beta=1.25e-5, chi4=-0.60,
        eta1=-0.002, chi6=-2.67e14, gamma1=-0.38, gamma2=0.52,
        sigma=8.56e13, omega=1.25e16, vs=9.36e10,
        printed_doublets=(2.23e14, 8.12e13, 1.13e12),
        printed_triplet=2.18e14,
    ),
}


def replay(case):
    l2, l4, lp = case["l2"], case["l4"], case["lp"]
    sigma, omega, vs = case["sigma"], case["omega"], case["vs"]
    # Published full (1,2,-1/2) matrix entries, Eq. (30) of PDF.
    d11 = 8 * (l2 + l4 - 2 * lp) * sigma**2 + case["beta"] * omega**2
    d12 = 2 * sqrt(2) * case["chi4"] * omega * vs
    d14 = 4 * sqrt(3) * case["eta1"] * sigma**2
    d22 = 4 * (3 * l2 + 3 * l4 + 4 * lp) * sigma**2 + case["beta"] * omega**2
    d34 = sqrt(2) * case["chi6"] * vs
    delta = (case["gamma2"] - case["gamma1"]) * sigma**2
    # An independent non-doublet scalar from the same published mass ledger.
    m_3313 = sqrt(4 * (3 * l2 + 3 * l4 + 4 * lp)) * sigma
    # The positive-heavy-mode condition needs D11>0 and this Schur complement>0.
    schur_a = d11 - d12**2 / d22
    result = dict(d11=d11, d22=d22, d12=d12, d14=d14,
                  schur_a=schur_a, m_3313=m_3313,
                  alphaH_over_betaH=-d22 / d12)
    if d11 <= 0 or schur_a <= 0:
        result["positive_heavy_zero_mode_possible"] = False
        return result

    # D33=x and D44=x+delta because the unprinted common 10_H m^2 cancels.
    # det(D)=0 gives x^2 + (delta-D14^2/A)x - D34^2 = 0.
    unit = 1e28
    roots = np.roots([1.0, (delta - d14**2 / schur_a) / unit,
                      -(d34 / unit) ** 2])
    x = max(roots) * unit
    assert x > 0
    D = np.array([[d11, d12, 0, d14],
                  [d12, d22, 0, 0],
                  [0, 0, x, d34],
                  [d14, 0, d34, x + delta]], dtype=float)
    values, vectors = np.linalg.eigh(D / 1e28)
    light = vectors[:, 0]
    result.update(
        positive_heavy_zero_mode_possible=True,
        heavy_masses=np.sqrt(values[1:] * 1e28),
        zero_eigenvalue_scaled=values[0],
        r=light[2] / light[3],
        s=(light[0] / light[1]) / (light[2] / light[3]),
        zero_residual=np.linalg.norm((D / 1e28) @ light),
    )
    # How much would the rounded first entry have to shift to realize r=69?
    # This gauges sensitivity; it is not a claim that the source did this.
    target_x = -d34 / 69.0
    target_a = d14**2 * target_x / (target_x * (target_x + delta) - d34**2)
    result["relative_d11_shift_for_r69"] = (
        target_a + d12**2 / d22
    ) / d11 - 1
    assert values[1] > 0 and result["zero_residual"] < 1e-11
    return result


if __name__ == "__main__":
    # Nearest-last-digit intervals for Table 2; even the most favorable
    # printed rounding cannot make its D11 positive at sigma=8.65e14.
    q_max = -0.165 + 0.485 - 2 * 0.165
    d11_max = 8 * q_max * (8.645e14) ** 2 + 1.255e-5 * (1.385e16) ** 2
    assert d11_max < 0
    print("Table 2 maximum D11 under nearest-last-digit rounding:", d11_max)
    outcomes = {name: replay(case) for name, case in CASES.items()}
    printed = outcomes["table_2_as_printed"]
    alternate = outcomes["table_2_sigma_exponent_minus_one_hypothesis"]
    second = outcomes["table_4_as_printed"]
    assert not printed["positive_heavy_zero_mode_possible"]
    assert printed["m_3313"] / CASES["table_2_as_printed"]["printed_triplet"] > 10
    assert alternate["positive_heavy_zero_mode_possible"]
    assert second["positive_heavy_zero_mode_possible"]
    for name, case in CASES.items():
        result = outcomes[name]
        print(name)
        for key, value in result.items():
            print(f"  {key}: {value}")
        print("  printed non-doublet mass:", case["printed_triplet"])
        print("  printed doublet masses (HTML table parse):", case["printed_doublets"])
