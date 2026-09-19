# Independent exact Julia replay of the eta1 singlet-VEV doublet-mixing entry.
# This uses ordered index loops rather than the Python script's combination cache.

const G = Complex{BigInt}
const ZZ = complex(big(0), big(0))

function signperm(indices)
    inv = 0
    for i in 1:length(indices), j in (i + 1):length(indices)
        inv += indices[i] > indices[j]
    end
    return isodd(inv) ? -1 : 1
end

function value(form::Dict{NTuple{5,Int},G}, idx::NTuple{5,Int})
    length(unique(idx)) == 5 || return ZZ
    key = Tuple(sort(collect(idx)))
    return signperm(idx) * get(form, key, ZZ)
end

function vev()
    out = Dict{NTuple{5,Int},G}()
    for mask in 0:31
        idx = ntuple(k -> 2 * (k - 1) + (((mask >> (k - 1)) & 1) == 1 ? 0 : 1), 5)
        out[idx] = (G(1, 0), G(0, 1), G(-1, 0), G(0, -1))[mod(count_ones(mask), 4) + 1]
    end
    return out
end

function doublet(weak)
    out = Dict{NTuple{5,Int},G}()
    for color4 in ((2, 3, 4, 5), (0, 1, 4, 5), (0, 1, 2, 3))
        idx = (color4..., weak)
        other = Tuple(i for i in 0:9 if !(i in idx))
        out[idx] = G(1, 0)
        out[other] = -G(0, signperm((idx..., other...)))
    end
    return out
end

conjform(form) = Dict(k => conj(v) for (k, v) in form)

function contract(a, b, c, n)
    total = ZZ
    for i in 0:8, j in (i + 1):9, l in 0:8, m in (l + 1):9
        va = value(a, (i, j, l, m, n))
        va == ZZ && continue
        for p in 0:7, q in (p + 1):8, r in (q + 1):9
            vb = value(b, (i, j, p, q, r))
            vb == ZZ && continue
            vc = value(c, (l, m, p, q, r))
            total += va * vb * vc
        end
    end
    return total
end

v = vev()
e = doublet(6)
@assert length(v) == 32
@assert length(e) == 6
@assert sum(abs2, values(v)) == 32
@assert sum(abs2, values(e)) == 6
barv = conjform(v)
bare = conjform(e)
b66 = contract(e, v, barv, 6) + contract(v, e, barv, 6)
b67 = contract(e, v, barv, 7) + contract(v, e, barv, 7)
bar66 = contract(v, v, bare, 6)
@assert b66 == G(192, 0)
@assert b67 == G(0, -192)
@assert bar66 == ZZ
println("PASS independent exact ordered-loop replay: B66=", b66, ", B67=", b67, ", Bbar66=", bar66)
