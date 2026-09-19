"""Exact Babu--Khan scalar convention-translation obstruction.

The decisive test is internal to the printed vacuum potential (Eq. 27) and
its stated stationarity equations (Eq. 28). It does not rely on Eq. 30.
"""

import sympy as sp


def main():
    w, sig, v = sp.symbols('omega sigma v_s', nonzero=True, real=True)
    mu2, nu2, mus2 = sp.symbols('mu2 nu2 mus2', real=True)
    a, b, c = sp.symbols('a b c', real=True)
    lam0, alpha, beta = sp.symbols('lambda0 alpha beta', real=True)
    chi1, chi2, chi3 = sp.symbols('chi1 chi2 chi3', real=True)

    # Source Eq. (27), literally, with the high-scale weak-doublet vevs zero.
    printed_vacuum = (
        -sp.Rational(6, 5)*mu2*w**2
        +sp.Rational(4, 25)*c*w**3
        +sp.Rational(36, 25)*a*w**4
        +sp.Rational(42, 125)*b*w**4
        -nu2*sig**2/2 + lam0*sig**4
        +sp.Rational(3, 5)*(alpha-beta)*w**2*sig**2
        -mus2*v**2/2 + chi1*v**4/4
        +chi2*sig**2*v**2/4
        +sp.Rational(3, 5)*chi3*w**2*v**2
    )
    tw = sp.solve(sp.diff(printed_vacuum, w), mu2)[0]
    ts = sp.solve(sp.diff(printed_vacuum, sig), nu2)[0]
    tv = sp.solve(sp.diff(printed_vacuum, v), mus2)[0]

    # Eq. (28)'s omega row is a positive control: it IS the derivative
    # of Eq. (27). The nu row has lambda0*sigma², not 4*lambda0*sigma².
    printed_mu2 = (sp.Rational(12, 5)*a*w**2
                   +sp.Rational(14, 25)*b*w**2
                   +c*w/5 +(alpha-beta)*sig**2/2
                   +chi3*v**2/2)
    assert sp.simplify(tw-printed_mu2) == 0
    assert sp.diff(ts, lam0) == 4*sig**2
    printed_nu_lambda_coefficient = sig**2
    assert sp.simplify(sp.diff(ts, lam0)
                       -printed_nu_lambda_coefficient) == 3*sig**2
    assert sp.diff(tv, chi1) == v**2
    # The PDF prints chi1*v_s (dimension one) in the mu_s² row; this is
    # another warning, but the lambda0 obstruction alone decides the gate.

    # Canonical parent convention. 54: 1/2 tr(dPhi)^2, complex 126:
    # 1/(2*5!) dSigma dSigma*, complex 10: dphi*dphi, singlet: dS*dS.
    # The already-replayed self-dual Eq. (26) singlet gives
    # N=(Sigma Sigma*)/5! = sigma² and S=v_s/sqrt(2).
    tr_phi2 = sp.Rational(12, 5)*w**2
    n126 = sig**2
    s_abs2 = v**2/2
    literal_nu = -nu2*n126/2
    literal_lambda = lam0*n126**2/4
    literal_alpha = alpha*tr_phi2*n126/2
    # Direct antisymmetric-pair counting gives beta coefficient -6/5.
    literal_beta = -sp.Rational(6, 5)*beta*w**2*sig**2
    literal_chi2 = chi2*sp.factorial(5)*n126*s_abs2
    literal_chi3 = chi3*tr_phi2*s_abs2
    expected = {
        'nu2': literal_nu.coeff(nu2),
        'lambda0': literal_lambda.coeff(lam0),
        'alpha': literal_alpha.coeff(alpha),
        'beta': literal_beta.coeff(beta),
        'chi2': literal_chi2.coeff(chi2),
        'chi3': literal_chi3.coeff(chi3),
    }
    printed = {key: sp.diff(printed_vacuum, var) for key, var in (
        ('nu2', nu2), ('lambda0', lam0), ('alpha', alpha),
        ('beta', beta), ('chi2', chi2), ('chi3', chi3))}
    vacuum_only_ratios = {key: sp.simplify(expected[key]/printed[key])
                          for key in expected}
    assert vacuum_only_ratios == {
        'nu2': 1, 'lambda0': sp.Rational(1, 4),
        'alpha': 2, 'beta': 2,
        'chi2': 240, 'chi3': 2,
    }

    # If both Eqs. (27) and (28) use the same printed lambda0 and sigma,
    # no invertible global constant coupling map can turn 4 into 1:
    # differentiating the mapped Eq. (27) still multiplies sigma^4 by 4.
    z = sp.symbols('z', nonzero=True)
    assert sp.diff(z*sig**4, sig)/sig == 4*z*sig**2
    assert sp.simplify(4*z*sig**2-z*sig**2) != 0

    # Complete accessible singlet Hessian of Eq. (27), using its OWN
    # stationarity relations, not the inconsistent printed Eq. (28).
    # The source defines S54=-sqrt(12/5)*omega, S126=sigma/sqrt(2),
    # S_S=v_s/sqrt(2). Their canonical real radial fluctuations have
    # coordinates (-sqrt(12/5)*delta_omega, delta_sigma, delta_v_s).
    variables = (w, sig, v)
    jac_inv = sp.diag(-sp.sqrt(sp.Rational(5, 12)), 1, 1)
    source_stationary = {mu2: tw, nu2: ts, mus2: tv}
    hessian = sp.hessian(printed_vacuum, variables)
    canonical_hessian = sp.simplify(
        jac_inv*hessian.subs(source_stationary)*jac_inv)
    printed_singlet_matrix = sp.Matrix([
        [c*w/10 +sp.Rational(12, 5)*a*w**2
         +sp.Rational(14, 25)*b*w**2,
         -sp.sqrt(sp.Rational(3, 5))*(alpha-beta)*sig*w,
         -sp.sqrt(sp.Rational(3, 5))*chi3*w*v],
        [-sp.sqrt(sp.Rational(3, 5))*(alpha-beta)*sig*w,
         lam0*sig**2/4, chi2*sig*v/2],
        [-sp.sqrt(sp.Rational(3, 5))*chi3*w*v,
         chi2*sig*v/2, chi1*v**2],
    ])
    # Five of six independent entries follow a common "half Hessian"
    # convention; the 126 radial lambda0 entry alone does not.
    residual = sp.simplify(canonical_hessian/2-printed_singlet_matrix)
    assert residual == sp.diag(0, sp.Rational(15, 4)*lam0*sig**2, 0)

    print('PASS: Eq. 27 omega tadpole reproduces printed Eq. 28 omega row')
    print('FAIL: Eq. 27 sigma tadpole needs 4*lambda0*sigma^2; Eq. 28 prints 1*lambda0*sigma^2')
    print('PARENT -> PRINTED VACUUM-ONLY COEFFICIENT RATIOS:', vacuum_only_ratios)
    print('EQ. 27 -> EQ. 30 HALF-HESSIAN RESIDUAL:', residual)
    print('NO_SINGLE_TRANSLATION_RECONCILES_SOURCE for generic nonzero lambda0 and sigma')


if __name__ == '__main__':
    main()
