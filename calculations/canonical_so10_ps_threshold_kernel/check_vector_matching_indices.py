"""Exact broken-vector indices and one-loop matching-scale slope checks.

For alpha_low^-1=alpha_high^-1-lambda/(12*pi), a heavy vector logarithm
-21*T_V*ln(M/nu) has d(lambda)/dln(nu)=+21*T_V. Its beta jump is
b_high-b_low=-7*T_V/2 after the eaten-Goldstone scalar is removed.
This checks the universal coefficient but does NOT evaluate gauge-fixing-
dependent intermediate diagrams or certify finite model-specific matching.
"""

from sympy import Rational as Q, simplify


def main():
    # Upper coset (6,2,2): SO(6)=SU4 six has index 1; SU2 doublet 1/2.
    upper = (Q(4), Q(6), Q(6))  # (SU4, SU2L, SU2R)
    c10 = Q(8)
    c_ps = (Q(4), Q(2), Q(2))
    for t, c in zip(upper, c_ps):
        # Pure-gauge beta discontinuity plus one real eaten Goldstone.
        assert -Q(11, 3)*(c10-c)+t/6 == -Q(7, 2)*t
        assert c10-c == t

    # Lower coset: (3,1,+2/3)+c.c., (1,1,+1)+c.c., and Y=0 singlet.
    t3 = Q(1)  # 3 + bar3
    t2 = Q(0)
    t1 = 2*Q(3, 5)*Q(4, 9)*3 + 2*Q(3, 5)
    assert t1 == Q(14, 5)
    lower = (t1, t2, t3)
    # High-side tree projection alpha1^-1=(2/5)alpha4^-1+(3/5)alphaR^-1.
    high_c = (Q(2, 5)*4+Q(3, 5)*2, Q(2), Q(4))
    low_c = (Q(0), Q(2), Q(3))
    for t, ch, cl in zip(lower, high_c, low_c):
        assert ch-cl == t
        assert -Q(11, 3)*(ch-cl)+t/6 == -Q(7, 2)*t
    # Matching-scale derivative of -lambda/(12pi) cancels the beta jump.
    for t in upper+lower:
        d_lambda_d_log_nu = 21*t
        b_high_minus_low = -Q(7, 2)*t
        assert simplify(d_lambda_d_log_nu+6*b_high_minus_low) == 0
    print("VECTOR_INDEX_AND_LOG_SCALE_CHECK_PASS",
          "upper (4,6,6)", "lower (14/5,0,1)",
          "finite Casimir differences equal the corresponding coset indices")


if __name__ == "__main__":
    main()
