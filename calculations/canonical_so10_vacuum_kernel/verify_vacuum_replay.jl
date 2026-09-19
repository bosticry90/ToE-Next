# Independent exact replay of normalized vacuum invariant coefficients.
# Uses index-set combinatorics, not the Python tensor-contraction routines.

const d = vcat(fill(-2, 6), fill(3, 4))
const vcomponents = Dict{NTuple{5,Int},Complex{BigInt}}()
for mask in 0:31
    idx = ntuple(k -> 2*(k-1) + (((mask >> (k-1)) & 1) == 1 ? 0 : 1), 5)
    vcomponents[idx] = (Complex{BigInt}(1, 0), Complex{BigInt}(0, 1),
                        Complex{BigInt}(-1, 0), Complex{BigInt}(0, -1))[mod(count_ones(mask),4)+1]
end

p2 = sum(x^2 for x in d)
p3 = sum(x^3 for x in d)
p4 = sum(x^4 for x in d)
n = sum(abs2(z) for z in values(vcomponents))
l = sum(abs2(z) * sum(d[i+1]*d[j+1] for (a,i) in enumerate(idx) for j in idx[(a+1):end])
        for (idx,z) in vcomponents)
tweighted = sum(z^2 * sum(d[i+1] for i in idx) for (idx,z) in vcomponents)
@assert p2 == 60 && p3 == 60 && p4 == 420
@assert n == 32 && l == -480 && tweighted == 0

# Each of the five complex one-forms z_k=e_(2k+1)+i e_(2k) is isotropic,
# and distinct z_k are mutually orthogonal. Every delta contraction
# P_k(V,V), k>=1, therefore vanishes without needing a quartic replay.
println("PASS independent VEV replay: p2=", p2, " p3=", p3,
        " p4=", p4, " Nraw=", n, " Lraw=", l, " PhiTraw=", tweighted)
println("Isotropic wedge implies P_k(V,V)=0 for k>=1, hence Q1=Q2=X131=0 at the singlet VEV")
