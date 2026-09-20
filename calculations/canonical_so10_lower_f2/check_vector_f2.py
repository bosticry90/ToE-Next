"""Exact background-field F² check for the lower massive-vector sector.

Frozen partial BFM Feynman gauge zeta=1. This verifies the universal
vector+Goldstone+ghost finite/log ratio and its group coefficient only;
it does not calculate the full PS/SM matching or active-field subtraction.
"""

from sympy import Matrix, Rational as Q, Symbol, diff, limit, simplify


def main():
    eps = Symbol("eps")
    d = 4 - 2 * eps

    # For Delta_V=-D² delta_mu_nu -2 Omega_mu_nu+M² delta_mu_nu,
    # a_2|F²=(d/12-2) tr_R(Omega²). The Goldstone is a real scalar;
    # the complex FP ghost has twice its weight and the opposite sign.
    a_vector = Q(1, 2) * (d / 12 - 2)
    a_goldstone = Q(1, 2) * Q(1, 12)
    a_ghost = -Q(1, 12)
    a_total = simplify(a_vector + a_goldstone + a_ghost)
    a0 = a_total.subs(eps, 0)
    a1 = diff(a_total, eps)
    assert a_total == -Q(7, 8) - eps / 12
    assert a0 == -Q(7, 8) and a1 == -Q(1, 12)
    assert simplify(a0 / Q(1, 24)) == -21  # one real scalar comparator

    # Independently check the Lorentz E² trace sign on a nonzero two-plane:
    # tr_L[(-2F)^2]/(2 F_mu_nu F_mu_nu) = -2.
    x = Symbol("x", nonzero=True)
    f = Matrix([[0, x, 0, 0], [-x, 0, 0, 0],
                [0, 0, 0, 0], [0, 0, 0, 0]])
    assert simplify(((-2 * f) ** 2).trace() /
                    (2 * (f.T * f).trace())) == -2

    # In MSbar the d-dependent a_2 pole leaves a finite a1 term while
    # the log(M²/mu²) carries -a0. Explicitly expand the subtracted pole.
    log_m2_over_mu2 = Symbol("L")
    renormalized = simplify(limit(
        a_total * (1 / eps - log_m2_over_mu2) - a0 / eps,
        eps, 0))
    assert renormalized == Q(7, 8) * log_m2_over_mu2 - Q(1, 12)
    # The relative finite/log(M²) ratio fixes the vector finite constant
    # after calibrating the beta slope.
    finite_over_log_m2 = simplify(a1 / (-a0))
    assert finite_over_log_m2 == -Q(2, 21)
    lambda_log_m2 = -Q(21, 2)
    lambda_finite = simplify(lambda_log_m2 * finite_over_log_m2)
    assert lambda_finite == 1

    # Independently frozen group Casimirs and hypercharge projector.
    c_ps = (Q(4), Q(2), Q(2))  # SU4, SU2L, SU2R
    c_sm = (Q(0), Q(2), Q(3))  # U1, SU2L, SU3
    c_projected = (Q(2, 5) * c_ps[0] + Q(3, 5) * c_ps[2],
                   c_ps[1], c_ps[0])
    index = tuple(simplify(a - b) for a, b in zip(c_projected, c_sm))
    assert index == (Q(14, 5), Q(0), Q(1))
    assert tuple(lambda_finite * t for t in index) == index
    assert tuple(lambda_log_m2 * t for t in index) == (
        -Q(147, 5), Q(0), -Q(21, 2))

    # Convention: alpha_low^-1 = M[alpha_PS^-1] - lambda/(12*pi).
    # lambda_V=T*(1-21 log(M/mu)); d lambda/d log(mu)=21T.
    # d alpha^-1/d log(mu)=-b/(2*pi), b_high-b_low=-7T/2.
    for t in index:
        b_high_minus_low = -Q(7, 2) * t
        d_lambda_d_log_mu = 21 * t
        assert simplify(d_lambda_d_log_mu +
                        6 * b_high_minus_low) == 0

    # One complete 16_F gives the same projected PS and SM one-loop
    # fermion indices. The only fermion made heavy by the 126 singlet
    # VEV is nu_R, an SM singlet with zero (T1,T2,T3). This cancellation
    # does not require its unfitted Majorana mass.
    ps_per_generation = (Q(2), Q(2), Q(2))  # SU4, SU2L, SU2R Weyl T sums
    ps_projected = (Q(2, 5) * ps_per_generation[0] +
                    Q(3, 5) * ps_per_generation[2],
                    ps_per_generation[1], ps_per_generation[0])
    sm_per_generation = (
        Q(1, 10) + Q(4, 5) + Q(1, 5) + Q(3, 10) + Q(3, 5),
        3 * Q(1, 2) + Q(1, 2),
        2 * Q(1, 2) + Q(1, 2) + Q(1, 2),
    )
    assert ps_projected == sm_per_generation == (Q(2), Q(2), Q(2))
    assert tuple(Q(2, 3) * (a - b) for a, b in
                 zip(ps_projected, sm_per_generation)) == (0, 0, 0)

    print("LOWER_VECTOR_F2_FEYNMAN_GAUGE_PASS",
          "a2_F2=-(7/8)-(eps/12)",
          "vector_to_real_scalar_log=-21",
          "finite_over_logM2=-2/21",
          "lambda_vector=T*(1-21log(M/mu))",
          "T=(14/5,0,1)",
          "complete_16F_projected_beta_jump=0",
          "full_lower_boundary=NOT_DERIVED")


if __name__ == "__main__":
    main()
