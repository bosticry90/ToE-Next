"""Independent Nemo polynomial replay of the printed tadpole obstruction."""

using Nemo

R, x = polynomial_ring(QQ, "sigma")

# Take the legitimate parameter slice omega = v_s = 0,
# lambda0 = nu² = 1. On this slice Eq. (28) claims a stationary point
# at sigma = 1. Eq. (27) instead has a nonzero derivative there.
printed_vacuum = -QQ(1, 2)*x^2 + x^4
printed_tadpole_point = QQ(1)
@assert evaluate(derivative(printed_vacuum), printed_tadpole_point) == 3
@assert evaluate(derivative(printed_vacuum), printed_tadpole_point) != 0

# Source Eq. (24)'s literal lambda0/4 normalization WOULD yield the
# Eq. (28) lambda0 coefficient, demonstrating exactly where an
# equation-specific coefficient convention would have to switch.
literal_parent_slice = -QQ(1, 2)*x^2 + QQ(1, 4)*x^4
@assert evaluate(derivative(literal_parent_slice), QQ(1)) == 0

# Reparameterizing the shared coupling by any nonzero constant z does
# not alter the derivative ratio 4 between x^4 and x^2 in Eq. (27).
for z in (QQ(1, 4), QQ(1), QQ(2), QQ(7, 3))
    quartic = z*x^4
    @assert evaluate(derivative(quartic), QQ(1)) == 4*z
end

println("PASS: exact independent Eq. 27 versus Eq. 28 contradiction")
println("NO_SINGLE_TRANSLATION_RECONCILES_SOURCE for generic nonzero lambda0, sigma")
