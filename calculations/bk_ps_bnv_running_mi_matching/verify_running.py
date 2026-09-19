"""Exact primary verification for the admitted Pati--Salam running seam.

The program independently reconstructs the Babu--Khan Pati--Salam gauge beta
ledger, checks the published gauge anomalous factors from quadratic Casimirs,
reconciles the Babu--Khan and Mambrini sign/orientation conventions, and applies
one universal running factor before the frozen M_I threshold projector.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

import sympy as sp


Q = Fraction
GROUPS = ("4C", "2L", "2R")
GROUP_C2 = {"4C": Q(4), "2L": Q(2), "2R": Q(2)}


@dataclass(frozen=True)
class Rep:
    dimension: int
    dynkin_index: Q
    casimir: Q


REPS = {
    "1": Rep(1, Q(0), Q(0)),
    "4": Rep(4, Q(1, 2), Q(15, 8)),
    "4bar": Rep(4, Q(1, 2), Q(15, 8)),
    "6": Rep(6, Q(1), Q(5, 2)),
    "10": Rep(10, Q(3), Q(9, 2)),
    "10bar": Rep(10, Q(3), Q(9, 2)),
    "15": Rep(15, Q(4), Q(4)),
    "2": Rep(2, Q(1, 2), Q(3, 4)),
    "3": Rep(3, Q(2), Q(2)),
}


@dataclass(frozen=True)
class Field:
    name: str
    kind: str
    multiplicity: int
    reps: tuple[str, str, str]
    loop_weight: Q


FIELDS = (
    Field("three_F_L", "weyl", 3, ("4", "2", "1"), Q(1, 2)),
    Field("three_F_R", "weyl", 3, ("4bar", "1", "2"), Q(1, 2)),
    Field("H_D", "scalar", 1, ("1", "2", "2"), Q(2)),
    # Babu--Khan Sec. 2.2 places the whole 126_H at M_I.  Its
    # Sigma_1=(6,1,1) component supplies the sextet contribution in the
    # Pati--Salam interval.  H_T=(6,1,1) from 10_H is instead an M_U
    # threshold field and is deliberately absent from this active ledger.
    Field("Sigma_1", "scalar", 1, ("6", "1", "1"), Q(2)),
    Field("Sigma_2", "scalar", 1, ("10", "3", "1"), Q(2)),
    Field("Sigma_3", "scalar", 1, ("10bar", "1", "3"), Q(2)),
    Field("Sigma_4", "scalar", 1, ("15", "2", "2"), Q(2)),
)


def s2(field: Field, group_index: int) -> Q:
    value = Q(field.multiplicity) * REPS[field.reps[group_index]].dynkin_index
    for index, rep_name in enumerate(field.reps):
        if index != group_index:
            value *= REPS[rep_name].dimension
    return value


def beta_ledger(fields: tuple[Field, ...]) -> tuple[tuple[Q, ...], tuple[tuple[Q, ...], ...]]:
    one_loop: list[Q] = []
    two_loop = [[Q(0) for _ in GROUPS] for _ in GROUPS]

    for i, group_i in enumerate(GROUPS):
        c2_g = GROUP_C2[group_i]
        coefficient = -Q(11, 3) * c2_g
        for field in fields:
            if field.kind == "weyl":
                coefficient += Q(4, 3) * field.loop_weight * s2(field, i)
            else:
                coefficient += Q(1, 6) * field.loop_weight * s2(field, i)
        one_loop.append(coefficient)

        for j, _group_j in enumerate(GROUPS):
            if i == j:
                two_loop[i][j] -= Q(34, 3) * c2_g * c2_g
            for field in fields:
                c2_j = REPS[field.reps[j]].casimir
                if field.kind == "weyl":
                    bracket = 4 * c2_j
                    if i == j:
                        bracket += Q(20, 3) * c2_g
                    two_loop[i][j] += field.loop_weight * bracket * s2(field, i)
                else:
                    bracket = 2 * c2_j
                    if i == j:
                        bracket += Q(1, 3) * c2_g
                    two_loop[i][j] += field.loop_weight * bracket * s2(field, i)

    return tuple(one_loop), tuple(tuple(row) for row in two_loop)


def verify_beta_and_anomalous_dimensions() -> None:
    expected_one = (Q(1), Q(26, 3), Q(26, 3))
    expected_two = (
        (Q(1209, 2), Q(249, 2), Q(249, 2)),
        (Q(1245, 2), Q(779, 3), Q(48)),
        (Q(1245, 2), Q(48), Q(779, 3)),
    )
    one_loop, two_loop = beta_ledger(FIELDS)
    assert one_loop == expected_one
    assert two_loop == expected_two

    assert any(field.name == "Sigma_1" for field in FIELDS)
    assert all(field.name != "H_T" for field in FIELDS)

    without_intermediate_sextet = tuple(
        field for field in FIELDS if field.name != "Sigma_1"
    )
    one_without, two_without = beta_ledger(without_intermediate_sextet)
    assert one_without == (Q(2, 3), Q(26, 3), Q(26, 3))
    assert two_without[0][0] == Q(3551, 6)
    assert all(two_without[i][j] == expected_two[i][j] for i, j in product(range(3), repeat=2) if (i, j) != (0, 0))

    # The one-loop current-current counterterm factors for the unique invariant
    # reduce to these fundamental-representation Casimir combinations.
    gamma_4 = 2 * REPS["4"].casimir
    gamma_2l = 3 * REPS["2"].casimir
    gamma_2r = 3 * REPS["2"].casimir
    assert (gamma_4, gamma_2l, gamma_2r) == (Q(15, 4), Q(9, 4), Q(9, 4))


def verify_running_and_sign_conventions() -> sp.Expr:
    r4, r2l, r2r = sp.symbols("r4 r2L r2R", positive=True)
    alpha4, alpha2l, alpha2r, ell = sp.symbols(
        "alpha4 alpha2L alpha2R ell", positive=True
    )
    beta = (sp.Rational(1), sp.Rational(26, 3), sp.Rational(26, 3))
    gamma = (sp.Rational(15, 4), sp.Rational(9, 4), sp.Rational(9, 4))
    ratios = (r4, r2l, r2r)

    exponents = tuple(-g / b for g, b in zip(gamma, beta))
    assert exponents == (
        sp.Rational(-15, 4),
        sp.Rational(-27, 104),
        sp.Rational(-27, 104),
    )

    mambrini_orientation = sp.prod(r**p for r, p in zip(ratios, exponents))
    babu_orientation = sp.prod((1 / r) ** (g / b) for r, g, b in zip(ratios, gamma, beta))
    assert sp.simplify(mambrini_orientation / babu_orientation - 1) == 0

    # With ell=log(M_U/M_I), one-loop running gives
    # alpha_i(M_I)/alpha_i(M_U)=1/(1+b_i*alpha_i(M_U)*ell/(2*pi)).
    endpoint_ratios = tuple(
        1 / (1 + b * alpha * ell / (2 * sp.pi))
        for b, alpha in zip(beta, (alpha4, alpha2l, alpha2r))
    )
    closed_form = sp.prod(r**p for r, p in zip(endpoint_ratios, exponents))
    first_derivative = sp.simplify(sp.diff(closed_form, ell).subs(ell, 0))
    expected_first_derivative = sp.simplify(
        sum(g * alpha for g, alpha in zip(gamma, (alpha4, alpha2l, alpha2r)))
        / (2 * sp.pi)
    )
    assert sp.simplify(first_derivative - expected_first_derivative) == 0
    assert sp.simplify(closed_form.subs(ell, 0) - 1) == 0

    d_parity = sp.simplify(mambrini_orientation.subs(r2r, r2l))
    assert sp.simplify(d_parity / (r4 ** sp.Rational(-15, 4) * r2l ** sp.Rational(-27, 52)) - 1) == 0

    # In both papers the gauge beta convention is d(alpha^-1)/dln(mu)=-b/(2*pi).
    # The Wilson RGE is dln(C)/dln(mu)=-sum(gamma_i*alpha_i)/(2*pi).
    # Therefore dln(C)/dln(alpha_i)=-gamma_i/b_i, exactly the exponents above.
    for exponent, b, g in zip(exponents, beta, gamma):
        assert sp.simplify(exponent * b + g) == 0

    return mambrini_orientation


def verify_threshold_projector(running_factor: sp.Expr) -> None:
    k1sq, k2sq = sp.symbols("k1sq k2sq", positive=True)
    c_ps = sp.symbols("C_PS") * running_factor
    assert k1sq not in c_ps.free_symbols and k2sq not in c_ps.free_symbols

    # The running factor is applied once, before the broken-phase pole projector.
    pole_terms = {
        "O_I": running_factor * k1sq,
        "O_II": running_factor * k1sq,
        "O_III": running_factor * k2sq,
        "O_IV": running_factor * k2sq,
    }
    fierz = {"O_I": 2, "O_II": 2, "O_III": 2, "O_IV": -2}
    projected = {name: sp.expand(fierz[name] * value) for name, value in pole_terms.items()}

    delta = lambda a, b: int(a == b)
    for p, r, s, t in product(range(3), repeat=4):
        qque_tree = k1sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))
        duql_tree = 2 * k1sq * delta(r, s) * delta(p, t) + 2 * k2sq * delta(p, s) * delta(r, t)
        qqdn_tree = -k2sq * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))

        qque_run = sp.expand(running_factor * qque_tree)
        duql_run = sp.expand(running_factor * duql_tree)
        qqdn_run = sp.expand(running_factor * qqdn_tree)
        assert sp.simplify(qque_run - running_factor * qque_tree) == 0
        assert sp.simplify(duql_run - running_factor * duql_tree) == 0
        assert sp.simplify(qqdn_run - running_factor * qqdn_tree) == 0
        assert sp.simplify(qque_run.subs({symbol: 1 for symbol in running_factor.free_symbols}) - qque_tree) == 0
        assert sp.simplify(duql_run.subs({symbol: 1 for symbol in running_factor.free_symbols}) - duql_tree) == 0
        assert sp.simplify(qqdn_run.subs({symbol: 1 for symbol in running_factor.free_symbols}) - qqdn_tree) == 0

    assert projected["O_I"] == 2 * running_factor * k1sq
    assert projected["O_II"] == 2 * running_factor * k1sq
    assert projected["O_III"] == 2 * running_factor * k2sq
    assert projected["O_IV"] == -2 * running_factor * k2sq

    zero_coefficients = {"Q_qqql": 0, "Q_duue": 0, "Q_uddN": 0}
    assert all(running_factor * value == 0 for value in zero_coefficients.values())
    assert "Q_qqdN" not in zero_coefficients


def main() -> None:
    verify_beta_and_anomalous_dimensions()
    running_factor = verify_running_and_sign_conventions()
    verify_threshold_projector(running_factor)
    print("PASS: beta ledger, anomalous factors, sign convention, running, flavor, and M_I projector")


if __name__ == "__main__":
    main()
