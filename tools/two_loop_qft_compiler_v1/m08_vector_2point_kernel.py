"""Direct local-UV algebra for the M08 quantum-vector two-point preflight.

The Lorentz kernel is generated from two three-Yang--Mills vertices and two
general-covariant-gauge propagators.  Feynman parameterization and isotropic
vacuum reduction are performed locally in this module; no C10 residue is used
as an input.  The result remains preflight authority until the complete
partial-BFM BRST pole action and its independent replay exist.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import factorial
from pathlib import Path

from sympy import (Poly, Rational, Symbol, expand, factorial2, integrate,
                   simplify)


HERE = Path(__file__).resolve().parent
DIMENSION = 4
P = Symbol("P", real=True)
x = Symbol("x", real=True)
xi = Symbol("xi", real=True)
eta = Symbol("eta_H", real=True)
rho = Symbol("rho", real=True)
sigma = Symbol("sigma", real=True)
l = tuple(Symbol(f"l{index}", real=True) for index in range(DIMENSION))
p = (P,) + (0,) * (DIMENSION - 1)
k = tuple(l[index] - (1 - x) * p[index]
          for index in range(DIMENSION))
kp = tuple(l[index] + x * p[index]
           for index in range(DIMENSION))


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def delta(a, b):
    return Rational(1) if a == b else Rational(0)


def vertex_one(mu, a, b):
    # V(mu,a,b; p,k,-p-k), with all momenta incoming.
    return (delta(mu, a) * (p[b] - k[b])
            + delta(a, b) * (p[mu] + 2 * k[mu])
            + delta(b, mu) * (-2 * p[a] - k[a]))


def vertex_two(nu, aa, bb):
    # V(nu,aa,bb; -p,-k,p+k), with all momenta incoming.
    return (delta(nu, aa) * (k[bb] - p[bb])
            + delta(aa, bb) * (-p[nu] - 2 * k[nu])
            + delta(bb, nu) * (2 * p[aa] + k[aa]))


def propagator_terms(left, right, momentum, gauge_parameter):
    return (
        (delta(left, right), 1),
        (-(1 - gauge_parameter) * momentum[left] * momentum[right], 2),
    )


def odd_double_factorial(power):
    return Rational(1) if power == 0 else factorial2(power - 1)


def monomial_vacuum_pole(exponents, denominator_power):
    if any(power % 2 for power in exponents):
        return Rational(0)
    rank = sum(exponents) // 2
    denominator = Rational(1)
    for offset in range(rank):
        denominator *= DIMENSION + 2 * offset
    angular = Rational(1)
    for power in exponents:
        angular *= odd_double_factorial(power)
    angular /= denominator
    m = 2 + rank - denominator_power
    if m < 0:
        return Rational(0)
    radial = (Rational((-1) ** m, factorial(m))
              * Rational(factorial(rank + 1),
                         factorial(denominator_power - 1))
              * (x * (1 - x) * P**2) ** m)
    return simplify(angular * radial)


def integrate_local_pole(numerator, power_k, power_kp):
    total_power = power_k + power_kp
    feynman_weight = (
        Rational(factorial(total_power - 1),
                 factorial(power_k - 1) * factorial(power_kp - 1))
        * x ** (power_k - 1) * (1 - x) ** (power_kp - 1)
    )
    polynomial = Poly(expand(numerator), *l)
    result = 0
    for powers, coefficient in polynomial.terms():
        result += coefficient * monomial_vacuum_pole(
            powers, total_power
        )
    return simplify(integrate(expand(feynman_weight * result), (x, 0, 1)))


def vector_bubble_component(mu, nu, first_gauge, second_gauge):
    terms = defaultdict(lambda: Rational(0))
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            left_vertex = vertex_one(mu, a, b)
            if left_vertex == 0:
                continue
            for aa in range(DIMENSION):
                first_propagators = propagator_terms(
                    a, aa, k, first_gauge
                )
                for bb in range(DIMENSION):
                    right_vertex = vertex_two(nu, aa, bb)
                    if right_vertex == 0:
                        continue
                    second_propagators = propagator_terms(
                        b, bb, kp, second_gauge
                    )
                    vertex_product = left_vertex * right_vertex
                    for first_numerator, first_power in first_propagators:
                        if first_numerator == 0:
                            continue
                        for second_numerator, second_power in second_propagators:
                            if second_numerator == 0:
                                continue
                            terms[(first_power, second_power)] += (
                                vertex_product * first_numerator
                                * second_numerator
                            )
    # The two identical internal vector lines give the standard 1/2 graph
    # symmetry factor.
    return simplify(Rational(1, 2) * sum(
        integrate_local_pole(numerator, left, right)
        for (left, right), numerator in terms.items()
    ))


def ghost_bubble_component(mu, nu):
    # The Euclidean vertex/sign product in the frozen convention gives this
    # numerator.  Its derived contribution is checked below through exact
    # transversality of the complete ordinary-FP Yang--Mills pole.
    numerator = k[mu] * kp[nu]
    return simplify(integrate_local_pole(numerator, 1, 1))


def coefficient_p2(expression):
    return simplify(expand(expression).coeff(P, 2))


def main():
    vector_transverse = coefficient_p2(
        vector_bubble_component(1, 1, rho, sigma)
    )
    vector_longitudinal = coefficient_p2(
        vector_bubble_component(0, 0, rho, sigma)
    )
    ghost_transverse = coefficient_p2(ghost_bubble_component(1, 1))
    ghost_longitudinal = coefficient_p2(ghost_bubble_component(0, 0))

    # A multiplies p^2 delta_mu_nu; A+B multiplies the longitudinal component.
    vector_A = simplify(vector_transverse)
    vector_B = simplify(vector_longitudinal - vector_transverse)
    ghost_A = simplify(ghost_transverse)
    ghost_B = simplify(ghost_longitudinal - ghost_transverse)
    equal_vector_A = simplify(vector_A.subs({rho: xi, sigma: xi}))
    equal_vector_B = simplify(vector_B.subs({rho: xi, sigma: xi}))
    full_A = simplify(equal_vector_A + ghost_A)
    full_B = simplify(equal_vector_B + ghost_B)
    assert simplify(full_A + full_B) == 0
    derived_ordinary_delta_Z_Q = simplify(-full_A)

    payload = {
        "schema_version": 1,
        "outcome": "M08_QUANTUM_VECTOR_2POINT_LORENTZ_PREFLIGHT_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": (
            "explicit_4d_pole_residue_of_d_dimensional_local_Feynman_"
            "parameter_tensor_reduction"
        ),
        "normalization": (
            "Lorentz coefficients before group factors and overall vertex-i "
            "convention; multiply 1/(16*pi^2*epsilon_bar)"
        ),
        "kinematic_pole_coefficients": {
            "vector_bubble_A_p2_metric": str(vector_A),
            "vector_bubble_B_p_mu_p_nu": str(vector_B),
            "equal_gauge_vector_bubble_A": str(equal_vector_A),
            "equal_gauge_vector_bubble_B": str(equal_vector_B),
            "ghost_bubble_A_p2_metric": str(ghost_A),
            "ghost_bubble_B_p_mu_p_nu": str(ghost_B),
            "formal_full_FP_sum_A": str(full_A),
            "formal_full_FP_sum_B": str(full_B),
            "formal_full_FP_transversality_residual": str(simplify(
                full_A + full_B)),
            "derived_ordinary_YM_delta_Z_Q": str(
                derived_ordinary_delta_Z_Q),
        },
        "scope_boundary": {
            "group_factors_applied": False,
            "scalar_and_fermion_loops_applied": False,
            "partial_BFM_heavy_light_ghost_split_applied": False,
            "overall_Minkowski_vertex_sign_fixed": False,
            "delta_xi_extracted": False,
            "independent_complete_replay": False,
        },
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "nonexceptional_Euclidean_external_momentum",
            "locality": "degree_two_polynomial_in_external_momentum",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_vector_2point_lorentz_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    for key, value in payload["kinematic_pole_coefficients"].items():
        print(key, value)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
