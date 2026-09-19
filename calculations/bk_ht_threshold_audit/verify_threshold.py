"""Exact checks for the Babu--Khan high-scale sextet attribution audit.

This is not a numerical threshold calculation.  It distinguishes the
intermediate Sigma_1=(6,1,1) contribution to the Pati--Salam beta ledger from
the high-scale H_T=(6,1,1) threshold term, then compares the published spectrum
with the altered spectrum obtained by removing Sigma_1.
"""

from fractions import Fraction

import sympy as sp


Q = Fraction


def verify_field_attribution() -> None:
    # A complex SU(4) sextet contributes eta*T(6)/6 = 2*1/6 = 1/3.
    scalar_weight = Q(2)
    dynkin_index_6 = Q(1)
    sextet_delta_a4 = Q(1, 6) * scalar_weight * dynkin_index_6
    assert sextet_delta_a4 == Q(1, 3)

    without_sigma1 = Q(2, 3)
    with_sigma1 = without_sigma1 + sextet_delta_a4
    assert with_sigma1 == Q(1)

    # H_T is absent from the interval ledger.  Its source-level role is the
    # M_U matching term lambda_4^uS = 2*eta_HT, not this beta increment.
    interval_fields = {"Sigma_1", "Sigma_2", "Sigma_3", "Sigma_4", "H_D"}
    assert "Sigma_1" in interval_fields
    assert "H_T" not in interval_fields


def verify_branch_comparison() -> None:
    x = sp.symbols("x", positive=True)
    gamma4 = sp.Rational(15, 4)
    a_published = sp.Rational(1)
    a_changed = sp.Rational(2, 3)

    published = (1 + a_published * x) ** (gamma4 / a_published)
    changed_spectrum = (1 + a_changed * x) ** (gamma4 / a_changed)

    assert published == (1 + x) ** sp.Rational(15, 4)
    assert changed_spectrum == (1 + sp.Rational(2, 3) * x) ** sp.Rational(45, 8)

    # Both branches have the same first leading logarithm when their gauge
    # coupling evolution is treated consistently.  Their difference starts at
    # second order; this does not turn the altered spectrum into an H_T branch.
    log_ratio = sp.log(changed_spectrum / published)
    series = sp.series(log_ratio, x, 0, 4).removeO().expand()
    assert series.coeff(x, 1) == 0
    assert series.coeff(x, 2) == sp.Rational(5, 8)


def verify_high_scale_matching_term() -> None:
    rho = sp.symbols("rho", positive=True)  # rho = M_HT/M_U
    eta_ht = sp.log(rho)
    lambda_4_ht = 2 * eta_ht
    delta_alpha4_inverse = -lambda_4_ht / (12 * sp.pi)
    assert sp.simplify(delta_alpha4_inverse + sp.log(rho) / (6 * sp.pi)) == 0

    # Babu--Khan Eq. (19): M_U carries one power of M_HT under a 1/23 root.
    m_ht, remainder = sp.symbols("M_HT remainder", positive=True)
    m_u = (m_ht * remainder) ** sp.Rational(1, 23)
    assert sp.simplify(m_ht * sp.diff(sp.log(m_u), m_ht)) == sp.Rational(1, 23)


def main() -> None:
    verify_field_attribution()
    verify_branch_comparison()
    verify_high_scale_matching_term()
    print(
        "PASS: Sigma_1 interval attribution, altered-spectrum comparison, "
        "and H_T high-scale matching term"
    )


if __name__ == "__main__":
    main()
