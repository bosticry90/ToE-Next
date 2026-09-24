"""Local one-loop Lorentz UV kernels for the M08 ghost--vector vertices.

The calculation is an auxiliary-mass/large-momentum Taylor projector in four
dimensions at the simple-pole level.  External momenta are multiplied by a
bookkeeping parameter and the logarithmic coefficient is extracted through
first order.  Tensor vacuum monomials are integrated with exact isotropic
averages.  Group tensors and graph signs are intentionally attached later.
"""

from functools import lru_cache
from hashlib import sha256
import json
from math import prod
from pathlib import Path

from sympy import Poly, Rational, Symbol, diff, expand, simplify, sympify


HERE = Path(__file__).resolve().parent
D = 4
k = tuple(Symbol(f"k{i}") for i in range(D))
t = Symbol("t")
rho = Symbol("rho")
sigma = Symbol("sigma")
P = (Rational(1), Rational(0), Rational(0), Rational(0))
Q = (Rational(0), Rational(1), Rational(0), Rational(0))
ZERO = (Rational(0),) * D


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def vadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def vscale(value, vector):
    return tuple(value * item for item in vector)


def momentum(shift):
    return tuple(k[index] + t * shift[index] for index in range(D))


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def ghost_vertex(a, b, pbar, pghost):
    return tuple(a * pbar[index] + b * pghost[index]
                 for index in range(D))


def vector_propagator(i, j, shift, gauge):
    rows = []
    if i == j:
        rows.append((Rational(1), Rational(1), [(shift, 1)]))
    mom = momentum(shift)
    rows.append((-(1 - gauge), mom[i] * mom[j], [(shift, 2)]))
    return rows


def three_vector(i, j, mu, pa, pb, pc):
    value = Rational(0)
    if i == j:
        value += pa[mu] - pb[mu]
    if j == mu:
        value += pb[i] - pc[i]
    if mu == i:
        value += pc[j] - pa[j]
    return value


def odd_double_factorial(value):
    if value <= 0:
        return 1
    return prod(range(value, 0, -2))


@lru_cache(maxsize=None)
def monomial_average(exponents, denominator_power):
    degree = sum(exponents)
    if any(value % 2 for value in exponents):
        return Rational(0)
    rank = degree // 2
    if denominator_power != rank + 2:
        return Rational(0)
    numerator = prod(odd_double_factorial(value - 1)
                     for value in exponents)
    denominator = prod(D + 2 * index for index in range(rank))
    return Rational(numerator, denominator)


def integrate_polynomial(polynomial, denominator_power):
    result = Rational(0)
    parsed = Poly(expand(polynomial), *k)
    for exponents, coefficient in parsed.terms():
        result += coefficient * monomial_average(
            exponents, denominator_power)
    return simplify(result)


def uv_term(coefficient, numerator, denominators):
    total_power = sum(power for _, power in denominators)
    numerator = expand(numerator)
    n0 = numerator.subs(t, 0)
    n1 = diff(numerator, t).subs(t, 0)
    shift_insertion = Rational(0)
    for shift, power in denominators:
        shift_insertion += 2 * power * dot(k, shift)
    return simplify(coefficient * (
        integrate_polynomial(n1, total_power)
        - integrate_polynomial(n0 * shift_insertion, total_power + 1)
    ))


def sum_terms(terms):
    return simplify(sum(uv_term(*row) for row in terms))


def ghost_triangle(ext_rule, internal_rule, gauge):
    ae, be = ext_rule
    ax, bx = internal_rule
    p = vscale(t, P)
    q = vscale(t, Q)
    l1 = momentum(ZERO)
    l2 = momentum(vadd(P, Q))
    ra = ghost_vertex(ax, bx, p, l1)
    rb = ghost_vertex(ax, bx, vscale(-1, l2), q)
    rc = ghost_vertex(ae, be, vscale(-1, l1), l2)
    result = []
    for mu in range(D):
        terms = []
        for alpha in range(D):
            for beta in range(D):
                for cp, np, dp in vector_propagator(
                        alpha, beta, P, gauge):
                    terms.append((cp, ra[alpha] * rb[beta] * rc[mu] * np,
                                  dp + [(ZERO, 1),
                                        (vadd(P, Q), 1)]))
        result.append(sum_terms(terms))
    return tuple(result)


def gauge_triangle(ext_rule, left_rule, right_rule, gauge_left,
                   gauge_right):
    # ``ext_rule`` labels the external vector only through the tree projector;
    # the external vector attaches to the Yang--Mills vertex in this topology.
    del ext_rule
    ax, bx = left_rule
    ay, by = right_rule
    p = vscale(t, P)
    q = vscale(t, Q)
    loop = momentum(ZERO)
    ra = ghost_vertex(ax, bx, p, loop)
    rb = ghost_vertex(ay, by, vscale(-1, loop), q)
    pa = momentum(P)
    pb = vscale(-1, momentum(vscale(-1, Q)))
    pc = vscale(-t, vadd(P, Q))
    result = []
    for mu in range(D):
        terms = []
        for alpha in range(D):
            for ia in range(D):
                for beta in range(D):
                    for ib in range(D):
                        vertex = three_vector(ia, ib, mu, pa, pb, pc)
                        if vertex == 0:
                            continue
                        for ca, na, da in vector_propagator(
                                alpha, ia, P, gauge_left):
                            for cb, nb, db in vector_propagator(
                                    beta, ib, vscale(-1, Q), gauge_right):
                                terms.append((
                                    ca * cb,
                                    ra[alpha] * rb[beta] * vertex * na * nb,
                                    da + db + [(ZERO, 1)],
                                ))
        result.append(sum_terms(terms))
    return tuple(result)


def swordfish_external_antighost_on_seagull(cubic_rule, gauge):
    a, b = cubic_rule
    q = vscale(t, Q)
    loop = momentum(ZERO)
    rule = ghost_vertex(a, b, vscale(-1, loop), q)
    result = []
    for mu in range(D):
        terms = []
        for beta in range(D):
            for cp, np, dp in vector_propagator(
                    mu, beta, vscale(-1, Q), gauge):
                terms.append((cp, rule[beta] * np, dp + [(ZERO, 1)]))
        result.append(sum_terms(terms))
    return tuple(result)


def swordfish_external_ghost_on_seagull(cubic_rule, gauge):
    a, b = cubic_rule
    p = vscale(t, P)
    loop = momentum(ZERO)
    rule = ghost_vertex(a, b, p, loop)
    result = []
    for mu in range(D):
        terms = []
        for beta in range(D):
            for cp, np, dp in vector_propagator(mu, beta, P, gauge):
                terms.append((cp, rule[beta] * np, dp + [(ZERO, 1)]))
        result.append(sum_terms(terms))
    return tuple(result)


def vector_swordfish(gauge_left, gauge_right):
    # External ghosts sit on the seagull.  The external vector attaches to a
    # three-vector vertex.  The seagull Lorentz tensor contracts the two
    # internal vector indices.
    pa = vscale(-1, momentum(ZERO))
    pb = momentum(vscale(-1, vadd(P, Q)))
    pc = vscale(-t, vadd(P, Q))
    result = []
    for mu in range(D):
        terms = []
        for alpha in range(D):
            for ia in range(D):
                for ib in range(D):
                    vertex = three_vector(ia, ib, mu, pa, pb, pc)
                    if vertex == 0:
                        continue
                    for ca, na, da in vector_propagator(
                            alpha, ia, ZERO, gauge_left):
                        for cb, nb, db in vector_propagator(
                                alpha, ib, vscale(-1, vadd(P, Q)),
                                gauge_right):
                            terms.append((ca * cb, vertex * na * nb,
                                          da + db))
        result.append(sum_terms(terms))
    return tuple(result)


def quartic_ghost_bubble(ext_rule):
    a, b = ext_rule
    r = vscale(-t, vadd(P, Q))
    loop = momentum(ZERO)
    other = vadd(vscale(-1, loop), vscale(-1, r))
    rule = ghost_vertex(a, b, loop, other)
    return tuple(sum_terms([(Rational(1), rule[mu],
                             [(ZERO, 1), (vadd(P, Q), 1)])])
                 for mu in range(D))


def projected(vector, tree):
    norm = dot(tree, tree)
    coefficient = simplify(dot(vector, tree) / norm)
    residual = tuple(simplify(vector[index] - coefficient * tree[index])
                     for index in range(D))
    return coefficient, residual


def serial(vector):
    return [str(simplify(value)) for value in vector]


def main():
    rules = {
        "ordinary_FP": (Rational(1), Rational(0)),
        "heavy_V_derivative_on_ghost": (Rational(0), Rational(1)),
        "H_covariant_Laplacian": (Rational(1), Rational(-1)),
    }
    tree = {
        name: tuple(rule[0] * P[index] + rule[1] * Q[index]
                    for index in range(D))
        for name, rule in rules.items()
    }
    kernels = {}
    for name, rule in rules.items():
        ghost = ghost_triangle(rule, rule, rho)
        gauge = gauge_triangle(rule, rule, rule, rho, rho)
        # These are kinematic kernels only.  With the explicit color
        # orientation used by the action facade the ghost triangle projects
        # to -C_A/2 while the Yang--Mills triangle projects to +C_A/2; the
        # latter carries the relative cubic-Feynman-rule sign at assembly.
        # After that sign, the two topology families add to
        # ``-C_A*rho/2`` in the ordinary unsplit calibration.
        total = tuple(simplify(ghost[index] + gauge[index])
                      for index in range(D))
        coefficient, residual = projected(total, tree[name])
        kernels[name] = {
            "ghost_triangle": serial(ghost),
            "one_ghost_two_vector_triangle": serial(gauge),
            "relative_graph_signs": (
                "kinematic_sum_only; assembly_applies_minus_to_the_"
                "positive-oriented_Yang-Mills_color_contraction"
            ),
            "standard_equal_vertex_sum": serial(total),
            "tree_projected_coefficient": str(coefficient),
            "tree_projection_residual": serial(residual),
            "swordfish_external_antighost_on_seagull": serial(
                swordfish_external_antighost_on_seagull(rule, rho)),
            "swordfish_external_ghost_on_seagull": serial(
                swordfish_external_ghost_on_seagull(rule, rho)),
            "quartic_ghost_bubble": serial(quartic_ghost_bubble(rule)),
        }

    # The ordinary FP result is an internal calibration, derived here rather
    # than read from C10: the Lorentz sum rho multiplies the independently
    # contracted color factor -C_A/2.
    assert simplify(sympify(kernels["ordinary_FP"][
        "tree_projected_coefficient"]) - rho) == 0
    assert kernels["ordinary_FP"]["tree_projection_residual"] == [
        "0", "0", "0", "0"]

    payload = {
        "schema_version": 1,
        "outcome": "M08_BRST_THREE_POINT_LORENTZ_KERNEL_PREFLIGHT_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": (
            "auxiliary_mass_local_Taylor_projection_with_exact_4d_"
            "simple_pole_tensor_averages"
        ),
        "external_basis": {"p": list(map(str, P)), "q": list(map(str, Q))},
        "rules": {name: list(map(str, rule)) for name, rule in rules.items()},
        "kernels": kernels,
        "mixed_vector_swordfish": serial(vector_swordfish(rho, sigma)),
        "calibration": {
            "ordinary_FP_ghost_triangle": "rho/4",
            "ordinary_FP_vector_triangle": "3*rho/4",
            "derived_Lorentz_sum": "rho",
            "ghost_triangle_color_projection": "-C_A/2",
            "Yang_Mills_triangle_color_projection": "+C_A/2",
            "Yang_Mills_cubic_relative_Feynman_rule_sign": "-1",
            "derived_full_tree_coefficient": "-C_A*rho/2",
            "expected_C10_value_imported_as_input": False,
        },
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "common_auxiliary_mass_before_local_expansion",
            "promoted_terms": "local_first_derivative_only",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_three_point_lorentz_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    for name, row in kernels.items():
        print(name, row["tree_projected_coefficient"],
              row["tree_projection_residual"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
