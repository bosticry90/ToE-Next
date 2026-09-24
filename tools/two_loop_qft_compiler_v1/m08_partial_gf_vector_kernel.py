"""Action-derived partial-gauge-fixing contribution to the light-vector pole.

This is implementation evidence for M08, not a gate adjudicator.  The frozen
heavy gauge function contains ``d_mu V_i^mu``.  Since ``d_mu`` is the full
unbroken-H covariant derivative (background plus light quantum connection),
``-(d.V)^2/(2*xi)`` supplies a qVV vertex in addition to the parent
Yang--Mills vertex.  Earlier M08 preflight algebra used only the latter.

The calculation below differentiates the gauge-fixing polynomial to obtain
the extra Lorentz vertex and evaluates the resulting heavy-vector bubble with
the same nonexceptional Feynman-parameter UV projector used for the primary
two-point calculation.  The old Yang--Mills-only result is retained for a
direct correction ledger.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Rational, Symbol, simplify

import m08_vector_2point_kernel as base


HERE = Path(__file__).resolve().parent
rho = Symbol("rho", positive=True)


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def gf_vertex_one(mu, a, b, gauge):
    """q_mu(p) V_a(k) V_b(-p-k), color f(q,V_a,V_b) stripped."""
    second = tuple(-base.p[index] - base.k[index]
                   for index in range(base.DIMENSION))
    # Direct differentiation of -(d.V)^2/(2*gauge), with
    # d.V_i = partial.V_i + g f(i,q,j) q.V_j.  The relative color
    # orientation f(i,q,j)=-f(q,i,j) is included here.
    return (base.k[a] * base.delta(mu, b)
            - second[b] * base.delta(mu, a)) / gauge


def gf_vertex_two(nu, aa, bb, gauge):
    """q_nu(-p) V_aa(-k) V_bb(p+k), same stripped color order."""
    first = tuple(-value for value in base.k)
    second = tuple(base.p[index] + base.k[index]
                   for index in range(base.DIMENSION))
    return (first[aa] * base.delta(nu, bb)
            - second[bb] * base.delta(nu, aa)) / gauge


def bubble_component(mu, nu, gauge, gf_weight):
    result = Rational(0)
    for a in range(base.DIMENSION):
        for b in range(base.DIMENSION):
            left = base.vertex_one(mu, a, b)
            left += gf_weight * gf_vertex_one(mu, a, b, gauge)
            if left == 0:
                continue
            for aa in range(base.DIMENSION):
                for bb in range(base.DIMENSION):
                    right = base.vertex_two(nu, aa, bb)
                    right += gf_weight * gf_vertex_two(nu, aa, bb, gauge)
                    if right == 0:
                        continue
                    for na, pa in base.propagator_terms(
                            a, aa, base.k, gauge):
                        if na == 0:
                            continue
                        for nb, pb in base.propagator_terms(
                                b, bb, base.kp, gauge):
                            if nb == 0:
                                continue
                            result += base.integrate_local_pole(
                                left * right * na * nb, pa, pb)
    return simplify(Rational(1, 2) * result)


def p2(expression):
    return simplify(expression.expand().coeff(base.P, 2))


def coefficients(gf_weight):
    transverse = p2(bubble_component(1, 1, rho, gf_weight))
    longitudinal = p2(bubble_component(0, 0, rho, gf_weight))
    return transverse, simplify(longitudinal - transverse)


def covariant_laplacian_ghost_component(mu, nu):
    """Heavy H-matter ghost loop from ``-ubar d^2 u``.

    Differentiating the covariant Laplacian gives the scalar-current rule
    ``(pbar-pghost)_mu``.  The Euclidean vertex/propagator convention used by
    the projector already contains the closed-Grassmann-loop sign, just as
    in ``base.ghost_bubble_component``; no second explicit minus is applied.
    """
    left = 2 * base.k[mu] + base.p[mu]
    right = 2 * base.k[nu] + base.p[nu]
    return simplify(base.integrate_local_pole(left * right, 1, 1))


def covariant_ghost_coefficients():
    transverse = p2(covariant_laplacian_ghost_component(1, 1))
    longitudinal = p2(covariant_laplacian_ghost_component(0, 0))
    return transverse, simplify(longitudinal - transverse)


def main():
    old_a, old_b = coefficients(Rational(0))
    new_a, new_b = coefficients(Rational(1))
    flipped_a, flipped_b = coefficients(Rational(-1))
    correction_a = simplify(new_a - old_a)
    correction_b = simplify(new_b - old_b)
    ghost_a, ghost_b = covariant_ghost_coefficients()
    complete_a = simplify(new_a + ghost_a)
    complete_b = simplify(new_b + ghost_b)

    payload = {
        "schema_version": 1,
        "outcome": "M08_PARTIAL_GF_QVV_VECTOR_KERNEL_DERIVED",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "source_operator": "-(d_mu V_i^mu)^2/(2*xi)",
        "derivation": (
            "direct_functional_differentiation_then_nonexceptional_"
            "Feynman_parameter_UV_projection"
        ),
        "color_factor": "K_LHH_on_the_external_light_adjoint",
        "yang_mills_only": {"A": str(old_a), "B": str(old_b)},
        "yang_mills_plus_partial_gauge_fixing": {
            "A": str(new_a), "B": str(new_b)},
        "adversarial_opposite_relative_sign": {
            "A": str(flipped_a), "B": str(flipped_b)},
        "partial_gauge_fixing_correction": {
            "A": str(correction_a), "B": str(correction_b)},
        "heavy_covariant_laplacian_ghost": {
            "A": str(ghost_a), "B": str(ghost_b)},
        "complete_heavy_H_matter_gauge_fixing_sector": {
            "A": str(complete_a), "B": str(complete_b),
            "transversality_residual": str(simplify(
                complete_a + complete_b)),
        },
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "nonexceptional_Euclidean_external_momentum",
            "locality": "degree_two_polynomial",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_partial_gf_vector_kernel.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("OLD", old_a, old_b)
    print("NEW", new_a, new_b)
    print("CORRECTION", correction_a, correction_b)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
