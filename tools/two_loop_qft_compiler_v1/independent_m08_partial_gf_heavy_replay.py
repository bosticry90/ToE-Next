"""Independent large-momentum replay of the heavy mixed V-q two-point pole.

No primary M08 Lorentz kernel is imported.  The qVV rule is rederived from
``-(d.V)^2/(2*xi)`` and the UV pole is obtained with an auxiliary-mass vacuum
expansion rather than the primary Feynman-parameter implementation.
"""

from hashlib import sha256
import json
from math import factorial
from pathlib import Path

from sympy import (Poly, Rational, Symbol, binomial, expand, factorial2,
                   simplify)


HERE = Path(__file__).resolve().parent
D = 4
P = Symbol("P", real=True)
m2 = Symbol("Maux2", positive=True)
xi = Symbol("xi", positive=True)
eta = Symbol("eta_H", positive=True)
k = tuple(Symbol(f"k{index}", real=True) for index in range(D))
p = (P,) + (0,) * (D - 1)
kp = tuple(k[index] + p[index] for index in range(D))
X = 2 * k[0] * P + P**2


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def delta(a, b):
    return Rational(1) if a == b else Rational(0)


def ym_one(mu, a, b):
    return (delta(mu, a) * (p[b] - k[b])
            + delta(a, b) * (p[mu] + 2 * k[mu])
            + delta(b, mu) * (-2 * p[a] - k[a]))


def ym_two(nu, aa, bb):
    return (delta(nu, aa) * (k[bb] - p[bb])
            + delta(aa, bb) * (-p[nu] - 2 * k[nu])
            + delta(bb, nu) * (2 * p[aa] + k[aa]))


def gf_one(mu, a, b):
    return (p[mu] * delta(b, a) - k[a] * delta(b, mu)) / xi


def gf_two(nu, aa, bb):
    return (-p[nu] * delta(bb, aa) + k[aa] * delta(bb, nu)) / xi


def propagator(left, right, momentum, gauge):
    return (
        (delta(left, right), 1),
        (-(1 - gauge) * momentum[left] * momentum[right], 2),
    )


def vacuum_monomial_pole(exponents, denominator_power):
    if any(power % 2 for power in exponents):
        return Rational(0)
    rank = sum(exponents) // 2
    angular_denominator = Rational(1)
    for offset in range(rank):
        angular_denominator *= D + 2 * offset
    angular_numerator = Rational(1)
    for power in exponents:
        angular_numerator *= (Rational(1) if power == 0
                              else factorial2(power - 1))
    ultraviolet_degree = 2 + rank - denominator_power
    if ultraviolet_degree < 0:
        return Rational(0)
    radial = (Rational((-1) ** ultraviolet_degree,
                       factorial(ultraviolet_degree))
              * Rational(factorial(rank + 1),
                         factorial(denominator_power - 1))
              * m2 ** ultraviolet_degree)
    return simplify(angular_numerator / angular_denominator * radial)


def vacuum_integrate(polynomial, denominator_power):
    result = 0
    for exponents, coefficient in Poly(expand(polynomial), *k).terms():
        result += coefficient * vacuum_monomial_pole(
            exponents, denominator_power)
    return simplify(result)


def local_pole(numerator, power_k, power_kp):
    result = 0
    for order in range(3):
        coefficient = (-1) ** order * binomial(
            power_kp + order - 1, order)
        term = expand(numerator * coefficient * X**order)
        term = sum(value * P**power for (power,), value in
                   Poly(term, P).terms() if power <= 2)
        result += vacuum_integrate(
            term, power_k + power_kp + order)
    return simplify(result)


def component(mu, nu):
    result = 0
    for a in range(D):
        for b in range(D):
            left = ym_one(mu, a, b) + gf_one(mu, a, b)
            if left == 0:
                continue
            for aa in range(D):
                for bb in range(D):
                    right = ym_two(nu, aa, bb) + gf_two(nu, aa, bb)
                    if right == 0:
                        continue
                    for n1, d1 in propagator(a, aa, k, xi):
                        if n1 == 0:
                            continue
                        for n2, d2 in propagator(b, bb, kp, eta):
                            if n2 == 0:
                                continue
                            result += local_pole(left * right * n1 * n2,
                                                 d1, d2)
    # Per ordered-pair convention; the group ledger supplies 2*K_HHL.
    return simplify(Rational(1, 2) * result)


def p2(expression):
    return simplify(expand(expression).coeff(P, 2))


def main():
    transverse = p2(component(1, 1))
    longitudinal = p2(component(0, 0))
    coefficient_a = transverse
    coefficient_b = simplify(longitudinal - transverse)
    assert not coefficient_a.has(m2)
    assert not coefficient_b.has(m2)
    action = json.loads((HERE / "partial_bfm_action.json").read_text(
        encoding="utf-8"))
    payload = {
        "schema_version": 1,
        "outcome": "M08_HEAVY_MIXED_PARTIAL_GF_2POINT_INDEPENDENT_REPLAY",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action[
            "partial_bfm_action_sha256"],
        "method": "independent_auxiliary_mass_large_momentum_vacuum_expansion",
        "primary_kernel_imported": False,
        "primary_UV_reducer_imported": False,
        "group_factor_convention": "ordered_sum_2*K_HHL",
        "coefficients": {"A": str(coefficient_a), "B": str(coefficient_b)},
        "auxiliary_mass_residual": "0",
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "IRR": "common_auxiliary_mass_with_local_Taylor_projection",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_heavy_mixed_partial_gf_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("A", coefficient_a)
    print("B", coefficient_b)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
