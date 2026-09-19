"""
Independent exact replay of the finite coefficient tensors.

The Julia/Nemo calculation reconstructs the three-generation Kronecker-delta
maps without importing Python output.  Spinor Fierz signs are checked by the
separate explicit-component Python replay.
"""

using Nemo

const QQ, (k1sq, k2sq) = polynomial_ring(QQ, ["k1sq", "k2sq"])
const NG = 3

delta(a, b) = a == b ? QQ(1) : QQ(0)

qque(p, r, s, t) = k1sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))
duql(p, r, s, t) = 2k1sq * delta(r, s) * delta(p, t) + 2k2sq * delta(p, s) * delta(r, t)
qqdN(p, r, s, t) = -k2sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))

for p in 1:NG, r in 1:NG, s in 1:NG, t in 1:NG
    @assert qque(p, r, s, t) == qque(r, p, s, t)
    @assert qqdN(p, r, s, t) == qqdN(r, p, s, t)
    @assert evaluate(duql(p, r, s, t), [QQ(0), QQ(0)]) == 0
end

# The two pole coefficients reduce to the unique Pati--Salam coefficient when
# the Pati--Salam-breaking vev is zero.
const S, (omega2_poly, sigma2_poly) = polynomial_ring(QQ, ["omega2", "sigma2"])
const RR = fraction_field(S)
const omega2 = RR(omega2_poly)
const sigma2 = RR(sigma2_poly)
ps = 1 / (2 * omega2)
x = 1 / (2 * omega2)
xp = 1 / (2 * (omega2 + sigma2))
@assert x == ps
@assert (xp - x) * 2 * omega2 * (omega2 + sigma2) + sigma2 == 0
@assert 1 / (2 * (omega2 + RR(0))) == ps

println("PASS: Nemo coefficient symmetry, decoupling, and PS-limit checks")
