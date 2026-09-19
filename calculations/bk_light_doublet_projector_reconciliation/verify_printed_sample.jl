"""Independent exact Nemo replay of the printed Table 2 contradiction."""

using Nemo

l2, l4, lp = QQ(-17, 100), QQ(48, 100), QQ(17, 100)
beta, sigma, omega = QQ(1, 80000), QQ(865000000000000), QQ(13800000000000000)
printed_triplet = QQ(217000000000000)

d11 = 8 * (l2 + l4 - 2 * lp) * sigma^2 + beta * omega^2
triplet_mass_sq = 4 * (3 * l2 + 3 * l4 + 4 * lp) * sigma^2
@assert d11 < 0
@assert triplet_mass_sq > 100 * printed_triplet^2

# A candidate 10^13 exponent removes these two large contradictions; this
# alone does not reconstruct the unprinted precise sample or prove a typo.
sigma_alternative = sigma / 10
d11_alternative = 8 * (l2 + l4 - 2 * lp) * sigma_alternative^2 + beta * omega^2
triplet_alternative_sq = 4 * (3 * l2 + 3 * l4 + 4 * lp) * sigma_alternative^2
@assert d11_alternative > 0
@assert QQ(9, 10) < triplet_alternative_sq / printed_triplet^2 < QQ(11, 10)

println("PASS: exact printed Table 2 D11 is negative and triplet mass-squared exceeds Table 3 by >100x")
println("ALTERNATIVE ONLY: changing sigma exponent to 10^13 removes those contradictions")
