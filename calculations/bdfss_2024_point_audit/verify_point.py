"""Bounded audit of the printed normal-ordering point in arXiv:2409.03840.

No fitting, RG integration, or model adoption occurs here. The decimal inputs
below are transcribed from Appendix A, Eqs. (132)-(138), at their printed
precision. The mass relations are the paper's Eqs. (9)-(13).
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    r1 = complex(-3.23303e-3, 6.51103e-6)
    r2 = complex(-0.355963, 1.25289)
    phi = -1.35108
    c_r = 9.84658e12
    phase = complex(math.cos(phi), math.sin(phi))

    s = np.diag([6.67309e-9, 0.211339, 82.3132]).astype(complex)
    d = np.array(
        [
            [complex(-2.89062e-4, 4.87101e-4), complex(2.34361e-3, 3.43972e-3), complex(-5.44162e-3, 3.42227e-4)],
            [complex(2.34361e-3, 3.43972e-3), complex(4.61704e-2, -1.39879e-3), complex(-4.37217e-3, -5.40885e-1)],
            [complex(-5.44162e-3, 3.42227e-4), complex(-4.37217e-3, -5.40885e-1), complex(3.83674e-1, 2.9757e-2)],
        ],
        dtype=complex,
    )
    a = np.array(
        [
            [0, complex(1.10335e-3, 2.93066e-3), complex(-4.7391e-3, -1.62764e-4)],
            [complex(-1.10335e-3, -2.93066e-3), 0, complex(5.35481e-1, -1.00172e-1)],
            [complex(4.7391e-3, 1.62764e-4), complex(-5.35481e-1, 1.00172e-1), 0],
        ],
        dtype=complex,
    )
    assert np.allclose(d, d.T, rtol=0, atol=1e-14)
    assert np.allclose(a, -a.T, rtol=0, atol=1e-14)

    m_u = d + s + a
    m_d = d + r1 * s + phase * a
    m_e = d - 3 * r1 * s + r2 * a
    m_nu_d = d - 3 * s + r2.conjugate() * phase * a
    m_n = c_r * s
    assert all(np.isfinite(m).all() for m in (m_u, m_d, m_e, m_nu_d, m_n))

    # The positive diagonal M_N has a trivial Takagi matrix U=I. Independently
    # obtain its Takagi values as the singular values of the symmetric matrix.
    takagi_masses = np.sort(np.linalg.svd(m_n, compute_uv=False))
    assert np.allclose(np.eye(3).T @ m_n @ np.eye(3), np.diag(takagi_masses), rtol=1e-13, atol=1e-7)
    paper_masses = np.array([6.57e4, 2.08e12, 8.10e14])  # Eq. (59), rounded
    rel_mass_error = np.abs(takagi_masses / paper_masses - 1)
    assert np.max(rel_mass_error) < 1e-3

    # arXiv:2604.04021, Eqs. (7), (89)-(94): the corrected SO(10) reality
    # condition for a real 120_H has opposite conjugation signs for its PS
    # (1,2,2) and (15,2,2) components. Writing their up coefficients as x,y,
    # the down/charged-lepton antisymmetric coefficients are x*-y*, x*+3y*.
    # Consequently |q+r|=|2(x*+y*)/(x+y)|=2. In the 2024 point those same
    # coefficients are phase and r2. This test is invariant under rescaling A.
    reality_sum = phase + r2
    reality_modulus = abs(reality_sum)
    reality_residual = abs(reality_modulus - 2)
    assert reality_residual > 1.0  # decisively beyond printed rounding

    mu_fit = 2e16  # paper section 4.1, not a co-frozen gauge-threshold point
    mi_illustration = 1e14  # paper section 6, approximate only
    loop_log = math.log(mu_fit / mi_illustration) / (16 * math.pi**2)

    print("source = arXiv:2409.03840 Appendix A normal-ordering point")
    print(f"phase = {phase.real:.9f}{phase.imag:+.9f}j")
    print(f"r2 = {r2.real:.9f}{r2.imag:+.9f}j")
    print("M_N_GUT_GeV =", [f"{x:.8e}" for x in takagi_masses])
    print("max_relative_difference_from_rounded_Eq59 =", f"{np.max(rel_mass_error):.6e}")
    print("M3_over_illustrative_MI =", f"{takagi_masses[-1] / mi_illustration:.6f}")
    print("real_120_required_abs_phase_plus_r2 = 2")
    print("printed_abs_phase_plus_r2 =", f"{reality_modulus:.9f}")
    print("reality_modulus_residual =", f"{reality_residual:.9f}")
    print("log_MU_over_MI_over_16pi2 =", f"{loop_log:.9f}")
    print("matrix_reconstruction = PASS_AT_PRINTED_PRECISION")
    print("Takagi_check = PASS_AT_GUT_INPUT_SCALE")
    print("real_120_SO10_reality_check = FAIL_FOR_UNCHANGED_POINT")
    print("PS_flavor_omission = UNBOUNDED_BY_THIS_POINT")


if __name__ == "__main__":
    main()
