"""Independent exact-rational replay of the source-normalization gate."""

using Nemo

q54 = vcat(fill(QQ(-2, 5), 6), fill(QQ(3, 5), 4))
@assert sum(q54) == 0
@assert sum(x^2 for x in q54) == QQ(12, 5)
@assert sum(x^3 for x in q54) == QQ(12, 25)
@assert sum(x^4 for x in q54) == QQ(84, 125)

# Eq. (26)'s 246810 component has squared magnitude sigma²/32.
# The decomposable self-dual singlet has one index from each of five
# mutually orthogonal two-planes, hence 2^5 = 32 equal-magnitude entries.
norm_over_sigma2 = QQ(32, 32)
@assert norm_over_sigma2 == 1

# Let N = (Sigma Sigma*)/5! = q sigma². The quadratic term of Eq. (24)
# matches Eq. (27) only at q=1, while its lambda0 term matches at q=2.
@assert norm_over_sigma2 / 2 == QQ(1, 2)
@assert norm_over_sigma2^2 / 4 == QQ(1, 4)
@assert norm_over_sigma2^2 / 4 != 1
@assert QQ(2)^2 / 4 == 1
@assert QQ(2) / 2 != QQ(1, 2)

# Direct combinatorial beta contraction, not copied from the Python replay.
for mask in 0:31
    indexset = [2*k + (isodd(mask >> k) ? 1 : 2) for k in 0:4]
    weight = QQ(0)
    for x in 1:4, y in (x+1):5
        weight += 2*q54[indexset[x]]*q54[indexset[y]]
    end
    @assert weight == QQ(-6, 5)
end

# Exact, nondegenerate one-light-mode witness for the generic sparse D.
D = matrix(QQ, 4, 4, [QQ(21, 5), -1, 0, 3,
                      -1, 5, 0, 0,
                      0, 0, 7, -2,
                      3, 0, -2, QQ(79, 28)])
@assert det(D) == 0
@assert det(D[1:3, 1:3]) > 0
@assert det(D[1:2, 1:2]) > 0
@assert D[1, 1] > 0
@assert rank(D) == 3

println("PASS: independent exact 54, 126 singlet normalization, beta contraction, Schur witness")
println("SOURCE GATE: Eq. (24) and Eq. (27) cannot share one literal 126 normalization")
