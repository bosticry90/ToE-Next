"""Independent exact Julia/Nemo replay of the first fail-fast boundary."""

using Nemo

function fundamental_casimir(n)
    # Sum the squares of the usual n(n-1) off-diagonal SU(n) generators
    # and n-1 normalized Cartan generators. No closed Casimir formula is used.
    squares = matrix(QQ, n, n, [QQ(0) for _ in 1:(n * n)])
    for i in 1:n, j in (i + 1):n
        squares[i, i] += QQ(1, 2)
        squares[j, j] += QQ(1, 2)
    end
    for k in 1:(n - 1)
        weight = QQ(1, 2 * k * (k + 1))
        for i in 1:k
            squares[i, i] += weight
        end
        squares[k + 1, k + 1] += k^2 * weight
    end
    @assert all(squares[i, j] == 0 for i in 1:n for j in 1:n if i != j)
    @assert all(squares[i, i] == squares[1, 1] for i in 1:n)
    return squares[1, 1]
end

c4 = fundamental_casimir(4)
c2 = fundamental_casimir(2)
@assert c4 == QQ(15, 8)
@assert c2 == QQ(3, 4)
dirac = (3 * (c4 + c4), 3c2, 3c2)
left = (3 * (c4 + c4), 6c2, QQ(0))
right = (3 * (c4 + c4), QQ(0), 6c2)
@assert dirac == (QQ(45, 4), QQ(9, 4), QQ(9, 4))
@assert left == (QQ(45, 4), QQ(9, 2), QQ(0))
@assert right == (QQ(45, 4), QQ(0), QQ(9, 2))

D = matrix(QQ, 4, 4, [
    QQ(1, 3), QQ(-1), QQ(0), QQ(-1),
    QQ(-1), QQ(6), QQ(0), QQ(0),
    QQ(0), QQ(0), QQ(1), QQ(-2),
    QQ(-1), QQ(0), QQ(-2), QQ(10),
])
v = matrix(QQ, 4, 1, [QQ(6), QQ(1), QQ(2), QQ(1)])
@assert D * v == zero_matrix(QQ, 4, 1)
@assert det(D) == 0
@assert D[1, 1] == QQ(1, 3) > 0
@assert det(D[1:2, 1:2]) == 1
@assert det(D[1:3, 1:3]) == 1
r, s = QQ(2), QQ(3)
source_d11 = D[1, 4]^2 / (D[4, 4] - r^2 * D[3, 3]) - D[1, 2] / s
correct_d11 = D[1, 4]^2 / (D[4, 4] - r^2 * D[3, 3]) - D[1, 2] / (r * s)
@assert source_d11 == QQ(1, 2)
@assert correct_d11 == D[1, 1] == QQ(1, 3)

println("PASS: independent generator-square gauge terms")
println("STOP: published scalar-projector D11 identity fails exact zero-mode replay")
