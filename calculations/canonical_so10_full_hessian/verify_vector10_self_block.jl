# Independent exact Julia replay of the VEV-induced K and T tensors.
# Uses ordered antisymmetric components; it does not import Python routines.

const G = Complex{BigInt}
const ZZ = G(0, 0)

function parity_of(t)
    isodd(sum(t[i] > t[j] for i in 1:length(t) for j in (i+1):length(t))) ? -1 : 1
end

function component(form, tup)
    length(unique(tup)) == 5 || return ZZ
    key = Tuple(sort(collect(tup)))
    return parity_of(tup)*get(form, key, ZZ)
end

v = Dict{NTuple{5,Int},G}()
for mask in 0:31
    idx = ntuple(k -> 2*(k-1) + (((mask >> (k-1)) & 1) == 1 ? 0 : 1), 5)
    v[idx] = (G(1, 0),G(0, 1),G(-1, 0),G(0, -1))[mod(count_ones(mask),4)+1]
end

foursets = [(a,b,c,d) for a in 0:6 for b in (a+1):7
            for c in (b+1):8 for d in (c+1):9]
K = [sum(component(v, (i, q...))*conj(component(v, (j, q...)))
         for q in foursets) for i in 0:9, j in 0:9]
T = [sum(component(v, (i, q...))*component(v, (j, q...))
         for q in foursets) for i in 0:9, j in 0:9]
J = zeros(Int, 10, 10)
for a in 1:2:9
    J[a,a+1] = -1
    J[a+1,a] = 1
end
expected = [G(i == j ? 16 : 0, -16*J[i+1,j+1]) for i in 0:9, j in 0:9]
@assert K == expected
@assert T == zeros(G, 10, 10)
println("PASS independent K=16(I-iJ5), T=0 exact index replay")
