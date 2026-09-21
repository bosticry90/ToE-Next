"""Exact on-demand scalar vertex compiler for PARENT_ACTION_V1.

The compiler differentiates the frozen invariant polynomial directly.  It is
the scalar-potential front end needed by a future two-loop hard-region
compiler; it is not a diagram generator or a two-loop matching result.
"""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

from sympy import I, Matrix, Rational, conjugate, diff, simplify, symbols, zeros


HERE = Path(__file__).resolve().parent
CALC = HERE.parent
FULL = CALC / "canonical_so10_full_hessian"
sys.path.insert(0, str(FULL))
sys.path.insert(0, str(CALC / "canonical_so10_scalar_reconstruction"))

from parent_bilinear_oracle import (
    COMPLEX_NAMES, REAL_NAMES, State, bilinear_coefficients, invariant_values,
    vacuum_state,
)
from evaluate_sm_hessian_blocks import (
    rational_representatives, realified_representative,
)
from verify_eta1_doublet_mixing import doublet_form


PARENT_HASH = "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
POINT_HASH = "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816"


def verify() -> None:
    assert sha256((CALC / "canonical_so10_scalar_reconstruction" /
                   "PARENT_ACTION_V1.md").read_bytes()).hexdigest() == PARENT_HASH
    assert sha256((CALC / "canonical_so10_positive_higgs" /
                   "POINT.json").read_bytes()).hexdigest() == POINT_HASH


def add_state(a: State, b: State) -> State:
    sigma = {}
    for key in set(a.Sigma) | set(b.Sigma):
        ar, ai = a.Sigma.get(key, (0, 0))
        br, bi = b.Sigma.get(key, (0, 0))
        value = (simplify(ar + br), simplify(ai + bi))
        if value != (0, 0):
            sigma[key] = value
    return State(a.Phi + b.Phi, sigma,
                 tuple(simplify(x + y) for x, y in zip(a.phi, b.phi)),
                 simplify(a.S + b.S))


def scale_state(a: State, z) -> State:
    return State(a.Phi * z,
                 {key: (simplify(z * value[0]), simplify(z * value[1]))
                  for key, value in a.Sigma.items()},
                 tuple(simplify(z * x) for x in a.phi), simplify(z * a.S))


def zero_state() -> State:
    return State(zeros(10), {}, (0,) * 10, 0)


def directional_vertex_coefficients(directions):
    """Return one exact n-th derivative for every parent monomial.

    Integer/rational samples are used because the exact self-dual quartic
    implementation has internal Gaussian-integer identities.  For n=2 a
    degree-four exact first-derivative stencil is tensorized.  For n=3,4 the
    central stencil is exact by total-degree counting: every selected monomial
    is odd in all n variables and the parent degree is at most four.
    """
    n = len(directions)
    assert 2 <= n <= 4
    if n == 2:
        weights = {
            -2: Rational(1, 12), -1: -Rational(2, 3),
            1: Rational(2, 3), 2: -Rational(1, 12),
        }
    else:
        weights = {-1: -Rational(1, 2), 1: Rational(1, 2)}
    out = {name: 0 for name in REAL_NAMES + COMPLEX_NAMES}
    for nodes in product(weights, repeat=n):
        state = vacuum_state()
        weight = 1
        for node, direction in zip(nodes, directions):
            state = add_state(state, scale_state(direction, node))
            weight *= weights[node]
        values = invariant_values(state)
        for name in out:
            out[name] += weight * values[name]
    return {name: simplify(value) for name, value in out.items()}


def physical_vertex(directions, coefficients):
    raw = directional_vertex_coefficients(directions)
    return simplify(
        sum(coefficients[name] * raw[name] for name in REAL_NAMES)
        + sum(coefficients[name] * raw[name]
              + conjugate(coefficients[name] * raw[name])
              for name in COMPLEX_NAMES)
    )


def selected_directions():
    base = vacuum_state()
    phi0 = State(base.Phi, {}, (0,) * 10, 0)
    sigma0 = State(zeros(10), base.Sigma, (0,) * 10, 0)
    sreal = State(zeros(10), {}, (0,) * 10, 1)
    simag = State(zeros(10), {}, (0,) * 10, I)
    doublet = (0, 0, 1, -3)
    reps = rational_representatives()[doublet]
    sigma_entry = next((sector, obj) for sector, _, obj in reps
                       if sector == "Sigma")
    phi_entry = next((sector, obj) for sector, _, obj in reps
                     if sector == "phi")
    sigma_doublet = realified_representative(*sigma_entry).real
    phi_doublet = realified_representative(*phi_entry).real
    sigma_eta = State(zeros(10), doublet_form(6), (0,) * 10, 0)
    unit = [0] * 10
    unit[6] = 1
    phi_unit = State(zeros(10), {}, tuple(unit), 0)
    return (phi0, sigma0, sreal, simag, sigma_doublet, phi_doublet,
            sigma_eta, phi_unit)


def main() -> None:
    verify()
    (phi0, sigma0, sreal, simag, sigma_d, phi_d,
     sigma_eta, phi_unit) = selected_directions()

    # Regression: the new generic derivative compiler exactly reproduces the
    # already certified second-directional oracle for unrelated directions.
    for u, v in ((phi0, sreal), (sigma0, sigma_d), (sreal, simag),
                 (sigma_d, phi_d)):
        direct = directional_vertex_coefficients((u, v))
        old = bilinear_coefficients(u, v)
        assert direct == old

    # Cubic and quartic tensors are symmetric because the fields commute.
    cubic = directional_vertex_coefficients((phi0, sigma0, sigma_d))
    cubic_swap = directional_vertex_coefficients((sigma_d, phi0, sigma0))
    assert cubic == cubic_swap
    quartic = directional_vertex_coefficients((sigma0, sigma0, sigma_eta, phi_unit))
    quartic_swap = directional_vertex_coefficients((phi_unit, sigma0, sigma_eta, sigma0))
    assert quartic == quartic_swap
    assert quartic["zEta"] != 0

    # Elementary coupling regressions exercise cubic and quartic slots with
    # independently recognizable field content.
    z6 = directional_vertex_coefficients((phi_unit, phi_unit, sreal))
    assert z6["z6"] != 0
    # Expanding around <Phi> != 0 turns Phi.phi.phi.S* into a cubic as well.
    # This is an important background-VEV contribution, not contamination of
    # the z6 slot.
    assert z6["zK"] != 0
    assert all(z6[name] == 0 for name in COMPLEX_NAMES
               if name not in ("z6", "zK"))
    pure_s = directional_vertex_coefficients((sreal,) * 4)
    assert pure_s["lambdaS"] == 24
    assert all(pure_s[name] == 0 for name in REAL_NAMES if name != "lambdaS")

    # Degree is bounded by four.  Differentiating a compiled fourth vertex
    # once more is therefore identically zero; the explicit pure-S polynomial
    # supplies a cheap exact control without extending the public API to n=5.
    t = symbols("t", real=True)
    vals = invariant_values(add_state(vacuum_state(), scale_state(sreal, t)))
    assert simplify(diff(vals["lambdaS"], t, 5)) == 0

    payload = {
        "outcome": "SCALAR_VERTEX_ORACLE_PASS",
        "authority": "ON_DEMAND_EXACT_SCALAR_POTENTIAL_DERIVATIVES_ONLY",
        "parent_action_sha256": PARENT_HASH,
        "benchmark_point_sha256": POINT_HASH,
        "second_derivative_regression_pairs": 4,
        "cubic_permutation": "PASS",
        "quartic_permutation": "PASS",
        "selected_exact_controls": {
            "zEta_quartic": str(quartic["zEta"]),
            "z6_cubic": str(z6["z6"]),
            "zK_vev_induced_cubic": str(z6["zK"]),
            "lambdaS_fourth_derivative": str(pure_s["lambdaS"]),
        },
        "degree_above_four": "ZERO",
        "not_supplied": [
            "gauge_goldstone_ghost_feynman_rules",
            "diagram_generation",
            "one_loop_counterterms",
            "two_loop_tensor_reduction",
            "massive_vacuum_master_evaluation",
            "finite_C1_GS",
        ],
    }
    (HERE / "scalar_vertex_oracle.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("SCALAR_VERTEX_ORACLE_PASS")
    print("SECOND_DERIVATIVE_REGRESSION_PASS pairs=4")
    print("CUBIC_PERMUTATION_PASS")
    print("QUARTIC_PERMUTATION_PASS zEta=", quartic["zEta"])
    print("PHI_PHI_S_CUBIC_PASS z6=", z6["z6"], "zK=", z6["zK"])
    print("PURE_S_QUARTIC_PASS lambdaS=", pure_s["lambdaS"])
    print("DEGREE_FOUR_CLOSURE_PASS")


if __name__ == "__main__":
    main()
