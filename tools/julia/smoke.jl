using Nemo
using OrdinaryDiffEq

matrix_value = matrix(QQ, 2, 2, [1, 2, 3, 5])
@assert det(matrix_value) == -1

function decay!(du, u, _parameters, _time)
    du[1] = -u[1]
end

problem = OrdinaryDiffEq.ODEProblem(decay!, [1.0], (0.0, 1.0))
solution = OrdinaryDiffEq.solve(problem, OrdinaryDiffEq.Tsit5(); reltol=1e-9, abstol=1e-11)
@assert abs(solution(1.0)[1] - exp(-1.0)) < 1e-7

println(
    "JULIA_ENVIRONMENT_PASS Julia=", VERSION,
    " Nemo=", Base.pkgversion(Nemo),
    " OrdinaryDiffEq=", Base.pkgversion(OrdinaryDiffEq),
)
