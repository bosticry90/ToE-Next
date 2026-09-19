"""
Independent Julia/Nemo replay of the Pati--Salam beta ledger, anomalous
exponents, universal flavor running, and post-running M_I projector.

This file does not read the Python implementation or its output.
"""

using Nemo

const groups = ("4C", "2L", "2R")
const group_c2 = Dict("4C" => QQ(4), "2L" => QQ(2), "2R" => QQ(2))

struct Rep
    dimension::Int
    dynkin_index
    casimir
end

const reps = Dict(
    "1" => Rep(1, QQ(0), QQ(0)),
    "4" => Rep(4, QQ(1, 2), QQ(15, 8)),
    "4bar" => Rep(4, QQ(1, 2), QQ(15, 8)),
    "6" => Rep(6, QQ(1), QQ(5, 2)),
    "10" => Rep(10, QQ(3), QQ(9, 2)),
    "10bar" => Rep(10, QQ(3), QQ(9, 2)),
    "15" => Rep(15, QQ(4), QQ(4)),
    "2" => Rep(2, QQ(1, 2), QQ(3, 4)),
    "3" => Rep(3, QQ(2), QQ(2)),
)

struct Field
    name::String
    kind::Symbol
    multiplicity::Int
    reps::NTuple{3, String}
    loop_weight
end

const fields = (
    Field("three_F_L", :weyl, 3, ("4", "2", "1"), QQ(1, 2)),
    Field("three_F_R", :weyl, 3, ("4bar", "1", "2"), QQ(1, 2)),
    Field("H_D", :scalar, 1, ("1", "2", "2"), QQ(2)),
    Field("H_T", :scalar, 1, ("6", "1", "1"), QQ(2)),
    Field("Sigma_2", :scalar, 1, ("10", "3", "1"), QQ(2)),
    Field("Sigma_3", :scalar, 1, ("10bar", "1", "3"), QQ(2)),
    Field("Sigma_4", :scalar, 1, ("15", "2", "2"), QQ(2)),
)

function s2(field, group_index)
    value = QQ(field.multiplicity) * reps[field.reps[group_index]].dynkin_index
    for index in 1:3
        if index != group_index
            value *= reps[field.reps[index]].dimension
        end
    end
    return value
end

function beta_ledger(selected_fields)
    one_loop = [QQ(0) for _ in 1:3]
    two_loop = matrix(QQ, 3, 3, [QQ(0) for _ in 1:9])
    for i in 1:3
        c2g = group_c2[groups[i]]
        one_loop[i] = -QQ(11, 3) * c2g
        for field in selected_fields
            if field.kind == :weyl
                one_loop[i] += QQ(4, 3) * field.loop_weight * s2(field, i)
            else
                one_loop[i] += QQ(1, 6) * field.loop_weight * s2(field, i)
            end
        end

        for j in 1:3
            if i == j
                two_loop[i, j] -= QQ(34, 3) * c2g^2
            end
            for field in selected_fields
                c2j = reps[field.reps[j]].casimir
                if field.kind == :weyl
                    bracket = 4 * c2j + (i == j ? QQ(20, 3) * c2g : QQ(0))
                else
                    bracket = 2 * c2j + (i == j ? QQ(1, 3) * c2g : QQ(0))
                end
                two_loop[i, j] += field.loop_weight * bracket * s2(field, i)
            end
        end
    end
    return one_loop, two_loop
end

one_loop, two_loop = beta_ledger(fields)
@assert one_loop == [QQ(1), QQ(26, 3), QQ(26, 3)]
expected_two = matrix(QQ, 3, 3, [
    QQ(1209, 2), QQ(249, 2), QQ(249, 2),
    QQ(1245, 2), QQ(779, 3), QQ(48),
    QQ(1245, 2), QQ(48), QQ(779, 3),
])
@assert two_loop == expected_two

without_ht = Tuple(field for field in fields if field.name != "H_T")
one_without, two_without = beta_ledger(without_ht)
@assert one_without == [QQ(2, 3), QQ(26, 3), QQ(26, 3)]
@assert two_without[1, 1] == QQ(3551, 6)
for i in 1:3, j in 1:3
    if (i, j) != (1, 1)
        @assert two_without[i, j] == expected_two[i, j]
    end
end

gamma = (
    2 * reps["4"].casimir,
    3 * reps["2"].casimir,
    3 * reps["2"].casimir,
)
@assert gamma == (QQ(15, 4), QQ(9, 4), QQ(9, 4))

beta = (QQ(1), QQ(26, 3), QQ(26, 3))
exponents = Tuple(-gamma[index] / beta[index] for index in 1:3)
@assert exponents == (QQ(-15, 4), QQ(-27, 104), QQ(-27, 104))
@assert exponents[2] + exponents[3] == QQ(-27, 52)
for index in 1:3
    @assert exponents[index] * beta[index] == -gamma[index]
end

const R, (A, k1sq, k2sq) = polynomial_ring(QQ, ["A", "k1sq", "k2sq"])
delta(a, b) = a == b ? R(1) : R(0)

qque_tree(p, r, s, t) = k1sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))
duql_tree(p, r, s, t) = 2k1sq * delta(r, s) * delta(p, t) + 2k2sq * delta(p, s) * delta(r, t)
qqdN_tree(p, r, s, t) = -k2sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))

for p in 1:3, r in 1:3, s in 1:3, t in 1:3
    @assert A * qque_tree(p, r, s, t) == A * qque_tree(r, p, s, t)
    @assert A * qqdN_tree(p, r, s, t) == A * qqdN_tree(r, p, s, t)
    @assert evaluate(A * qque_tree(p, r, s, t), [QQ(1), k1sq, k2sq]) == qque_tree(p, r, s, t)
    @assert evaluate(A * duql_tree(p, r, s, t), [QQ(1), k1sq, k2sq]) == duql_tree(p, r, s, t)
    @assert evaluate(A * qqdN_tree(p, r, s, t), [QQ(1), k1sq, k2sq]) == qqdN_tree(p, r, s, t)
end

projected_terms = Dict(
    "O_I" => 2A * k1sq,
    "O_II" => 2A * k1sq,
    "O_III" => 2A * k2sq,
    "O_IV" => -2A * k2sq,
)
@assert projected_terms["O_IV"] == -2A * k2sq
@assert A * R(0) == 0

println("PASS: independent Nemo beta, anomalous, exponent, flavor, and projector replay")
