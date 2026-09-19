"""Exact singlet-radial Hessian, differentiated from the generated V0."""

from sympy import Matrix, solve, simplify

from derive_vacuum import main as derive_vacuum


def main():
    potential, fields, coefficients = derive_vacuum()
    omega, sigma, v = fields
    hessian = Matrix([[simplify(potential.diff(a, b)) for b in fields]
                      for a in fields])
    assert hessian == hessian.T
    tadpoles = [potential.diff(field) for field in fields]
    nonzero_branch = [simplify(tadpoles[i]/fields[i]) for i in range(3)]
    mass_names = ("mPhi2", "mSigma2", "mS2")
    substitutions = solve(nonzero_branch,
                          [coefficients[name] for name in mass_names], dict=True)
    assert len(substitutions) == 1
    on_shell = hessian.subs(substitutions[0]).applyfunc(simplify)
    print("stationarity mass substitutions:", substitutions[0])
    print("singlet radial Hessian on nonzero-VEV stationary branch:")
    print(on_shell)
    assert simplify(on_shell[0, 1] - 4*(coefficients["lambdaPhiSigma1"]-
                coefficients["lambdaPhiSigma2"]/4)*omega*sigma) == 0
    assert simplify(on_shell[1, 1]-8*coefficients["lambdaSigma1"]*sigma*sigma) == 0
    assert simplify(on_shell[2, 2]-2*coefficients["lambdaS"]*v*v) == 0
    print("SINGLET_RADIAL_HESSIAN_PASS; no positivity claim")
    return on_shell


if __name__ == "__main__":
    main()
