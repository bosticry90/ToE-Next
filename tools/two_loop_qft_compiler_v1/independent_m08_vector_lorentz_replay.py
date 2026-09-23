"""Independent auxiliary-mass/Taylor replay of the M08 vector Lorentz pole.

This implementation does not import the primary Feynman-parameter kernel.  It
expands the second propagator at large loop momentum through external order
p^2 and evaluates the resulting massive vacuum UV residues.
"""

from collections import defaultdict
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
rho = Symbol("rho", real=True)
sigma = Symbol("sigma", real=True)
k = tuple(Symbol(f"k{index}", real=True) for index in range(D))
p = (P,) + (0,) * (D - 1)
kp = tuple(k[index] + p[index] for index in range(D))
X = 2 * k[0] * P + P**2


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def delta(a, b):
    return Rational(1) if a == b else Rational(0)


def v1(mu, a, b):
    return (delta(mu, a) * (p[b] - k[b])
            + delta(a, b) * (p[mu] + 2 * k[mu])
            + delta(b, mu) * (-2 * p[a] - k[a]))


def v2(nu, aa, bb):
    return (delta(nu, aa) * (k[bb] - p[bb])
            + delta(aa, bb) * (-p[nu] - 2 * k[nu])
            + delta(bb, nu) * (2 * p[aa] + k[aa]))


def propagator(left, right, momentum, gauge_parameter):
    return (
        (delta(left, right), 1),
        (-(1 - gauge_parameter) * momentum[left] * momentum[right], 2),
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
            exponents, denominator_power
        )
    return simplify(result)


def large_momentum_pole(numerator, power_k, power_kp):
    expanded = 0
    for order in range(3):
        coefficient = (-1) ** order * binomial(
            power_kp + order - 1, order
        )
        term = expand(numerator * coefficient * X**order)
        # Only terms through external degree two can enter the local two-point
        # counterterm.  Higher powers are dropped before vacuum integration.
        term = sum(value * P**power for (power,), value in
                   Poly(term, P).terms() if power <= 2)
        expanded += vacuum_integrate(
            term, power_k + power_kp + order
        )
    return simplify(expanded)


def vector_component(mu, nu):
    terms = defaultdict(lambda: Rational(0))
    for a in range(D):
        for b in range(D):
            left = v1(mu, a, b)
            if left == 0:
                continue
            for aa in range(D):
                for bb in range(D):
                    right = v2(nu, aa, bb)
                    if right == 0:
                        continue
                    for n1, d1 in propagator(a, aa, k, rho):
                        for n2, d2 in propagator(b, bb, kp, sigma):
                            if n1 != 0 and n2 != 0:
                                terms[(d1, d2)] += left * right * n1 * n2
    return simplify(Rational(1, 2) * sum(
        large_momentum_pole(value, first, second)
        for (first, second), value in terms.items()
    ))


def ghost_component(mu, nu):
    return simplify(large_momentum_pole(k[mu] * kp[nu], 1, 1))


def p2(expression):
    return simplify(expand(expression).coeff(P, 2))


def main():
    transverse = p2(vector_component(1, 1))
    longitudinal = p2(vector_component(0, 0))
    vector_A = transverse
    vector_B = simplify(longitudinal - transverse)
    ghost_transverse = p2(ghost_component(1, 1))
    ghost_longitudinal = p2(ghost_component(0, 0))
    ghost_A = ghost_transverse
    ghost_B = simplify(ghost_longitudinal - ghost_transverse)
    assert not any(value.has(m2) for value in
                   (vector_A, vector_B, ghost_A, ghost_B))
    payload = {
        "schema_version": 1,
        "outcome": "M08_VECTOR_LORENTZ_INDEPENDENT_REPLAY_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": "auxiliary_mass_large_momentum_Taylor_vacuum_poles",
        "primary_Feynman_parameter_kernel_imported": False,
        "coefficients": {
            "vector_bubble_A_p2_metric": str(vector_A),
            "vector_bubble_B_p_mu_p_nu": str(vector_B),
            "ghost_bubble_A_p2_metric": str(ghost_A),
            "ghost_bubble_B_p_mu_p_nu": str(ghost_B),
        },
        "auxiliary_mass_residual": "0",
        "external_order": "p_squared",
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "IRR": "common_auxiliary_mass_with_local_Taylor_projection",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_vector_lorentz_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    for key, value in payload["coefficients"].items():
        print(key, value)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
