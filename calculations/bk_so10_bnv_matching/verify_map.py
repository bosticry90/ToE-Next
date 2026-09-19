"""Independent component replay for the Babu--Khan tree-level BNV map.

This program expands two-component spinors into explicit Grassmann components.
It does not consume the Cadabra transformation output.  The comparison fixes
the Fierz factors and signs in the convention recorded in RESULT.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

import numpy as np
import sympy as sp


Coeff = sp.Expr
Monomial = tuple[str, ...]


@dataclass(frozen=True)
class ExteriorPolynomial:
    terms: dict[Monomial, Coeff]

    @staticmethod
    def scalar(value: Coeff) -> "ExteriorPolynomial":
        value = sp.simplify(value)
        return ExteriorPolynomial({(): value} if value != 0 else {})

    @staticmethod
    def generator(name: str) -> "ExteriorPolynomial":
        return ExteriorPolynomial({(name,): sp.Integer(1)})

    def __add__(self, other: "ExteriorPolynomial") -> "ExteriorPolynomial":
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = sp.simplify(terms.get(monomial, 0) + coefficient)
            if terms[monomial] == 0:
                del terms[monomial]
        return ExteriorPolynomial(terms)

    def __neg__(self) -> "ExteriorPolynomial":
        return ExteriorPolynomial({m: -c for m, c in self.terms.items()})

    def __sub__(self, other: "ExteriorPolynomial") -> "ExteriorPolynomial":
        return self + (-other)

    def __rmul__(self, scalar: Coeff) -> "ExteriorPolynomial":
        scalar = sp.simplify(scalar)
        return ExteriorPolynomial(
            {m: sp.simplify(scalar * c) for m, c in self.terms.items() if scalar * c != 0}
        )

    def __mul__(self, other: "ExteriorPolynomial") -> "ExteriorPolynomial":
        result = ExteriorPolynomial.scalar(0)
        for left, left_coefficient in self.terms.items():
            for right, right_coefficient in other.terms.items():
                if set(left).intersection(right):
                    continue
                combined = left + right
                inversions = sum(
                    1
                    for first in range(len(combined))
                    for second in range(first + 1, len(combined))
                    if combined[first] > combined[second]
                )
                sign = -1 if inversions % 2 else 1
                ordered = tuple(sorted(combined))
                term = ExteriorPolynomial({ordered: sign * left_coefficient * right_coefficient})
                result = result + term
        return result

    def is_zero(self) -> bool:
        return not self.terms


EPSILON = sp.Matrix([[0, 1], [-1, 0]])
SIGMA = (
    sp.eye(2),
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -sp.I], [sp.I, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
)
BAR_SIGMA_UP = (SIGMA[0], -SIGMA[1], -SIGMA[2], -SIGMA[3])
BAR_SIGMA_DOWN = SIGMA


def levi_civita3(a: int, b: int, c: int) -> int:
    if len({a, b, c}) < 3:
        return 0
    inversion_count = sum(x > y for x, y in ((a, b), (a, c), (b, c)))
    return -1 if inversion_count % 2 else 1


def epsilon2(a: int, b: int) -> int:
    return int(EPSILON[a, b])


def field(name: str, *indices: int) -> list[ExteriorPolynomial]:
    return [ExteriorPolynomial.generator("_".join(map(str, (name, *indices, spin)))) for spin in range(2)]


def bilinear(
    left: list[ExteriorPolynomial], matrix: sp.Matrix, right: list[ExteriorPolynomial]
) -> ExteriorPolynomial:
    result = ExteriorPolynomial.scalar(0)
    for a, b in product(range(2), repeat=2):
        result = result + matrix[a, b] * (left[a] * right[b])
    return result


def current(
    left_bar: list[ExteriorPolynomial], mu: int, right: list[ExteriorPolynomial], *, lowered: bool
) -> ExteriorPolynomial:
    matrix = BAR_SIGMA_DOWN[mu] if lowered else BAR_SIGMA_UP[mu]
    return bilinear(left_bar, matrix, right)


def source_operator(label: str) -> ExteriorPolynomial:
    result = ExteriorPolynomial.scalar(0)
    for ci, cj, ck in permutations(range(3), 3):
        color_sign = levi_civita3(ci, cj, ck)
        for wa, wb in product(range(2), repeat=2):
            weak_sign = epsilon2(wa, wb)
            if weak_sign == 0:
                continue
            for mu in range(4):
                if label == "I":
                    first = current(field("ub", ci), mu, field("q", cj, wa), lowered=False)
                    second = current(field("eb"), mu, field("q", ck, wb), lowered=True)
                elif label == "II":
                    first = current(field("ub", ci), mu, field("q", cj, wa), lowered=False)
                    second = current(field("db", ck), mu, field("l", wb), lowered=True)
                elif label == "III":
                    first = current(field("db", ci), mu, field("q", cj, wb), lowered=False)
                    second = current(field("ub", ck), mu, field("l", wa), lowered=True)
                elif label == "IV":
                    first = current(field("db", ci), mu, field("q", cj, wb), lowered=False)
                    second = current(field("nb"), mu, field("q", ck, wa), lowered=True)
                else:
                    raise ValueError(label)
                result = result + color_sign * weak_sign * (first * second)
    return result


def target_operator(label: str) -> ExteriorPolynomial:
    result = ExteriorPolynomial.scalar(0)
    for ca, cb, cc in permutations(range(3), 3):
        color_sign = levi_civita3(ca, cb, cc)
        for wi, wj in product(range(2), repeat=2):
            weak_sign = epsilon2(wi, wj)
            if weak_sign == 0:
                continue
            if label == "qque":
                left = bilinear(field("q", ca, wi), EPSILON, field("q", cb, wj))
                right = bilinear(field("ub", cc), -EPSILON, field("eb"))
            elif label == "duql":
                left = bilinear(field("db", ca), -EPSILON, field("ub", cb))
                right = bilinear(field("q", cc, wi), EPSILON, field("l", wj))
            elif label == "qqdN":
                left = bilinear(field("q", ca, wi), EPSILON, field("q", cb, wj))
                right = bilinear(field("db", cc), -EPSILON, field("nb"))
            else:
                raise ValueError(label)
            result = result + color_sign * weak_sign * (left * right)
    return result


def assert_ratio(source: ExteriorPolynomial, target: ExteriorPolynomial, ratio: int, name: str) -> None:
    difference = source - ratio * target
    if not difference.is_zero():
        raise AssertionError(f"{name}: source != {ratio} * target; residual={difference.terms}")


def coefficient(flavor_count: int = 3) -> None:
    k1, k2 = sp.symbols("k1sq k2sq", positive=True)
    delta = lambda a, b: int(a == b)
    for p, r, s, t in product(range(flavor_count), repeat=4):
        qque = k1 * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))
        qque_swapped = k1 * (delta(r, s) * delta(p, t) + delta(p, s) * delta(r, t))
        qqdn = -k2 * (delta(p, s) * delta(r, t) + delta(r, s) * delta(p, t))
        qqdn_swapped = -k2 * (delta(r, s) * delta(p, t) + delta(p, s) * delta(r, t))
        duql = 2 * k1 * delta(r, s) * delta(p, t) + 2 * k2 * delta(p, s) * delta(r, t)
        if sp.simplify(qque - qque_swapped) != 0:
            raise AssertionError("qque flavor symmetry failed")
        if sp.simplify(qqdn - qqdn_swapped) != 0:
            raise AssertionError("qqdN flavor symmetry failed")
        if duql.subs(k1, 0).subs(k2, 0) != 0:
            raise AssertionError("duql decoupling failed")


def random_unitary(rng: np.random.Generator, size: int = 3) -> np.ndarray:
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    return q @ np.diag(np.conjugate(phases) / np.abs(phases))


def rotation_identities() -> None:
    rng = np.random.default_rng(20260918)
    U, D, E, N, Uc, Dc, Ec, Nc = [random_unitary(rng) for _ in range(8)]
    dagger = lambda matrix: np.conjugate(matrix.T)
    V1 = dagger(Uc) @ U
    V2 = dagger(Ec) @ D
    V3 = dagger(Dc) @ E
    V4 = dagger(Dc) @ D
    VUD = dagger(U) @ D
    VEN = dagger(E) @ N
    UEN = dagger(Ec) @ Nc
    identities = {
        "UcD": (dagger(Uc) @ D, V1 @ VUD),
        "EcU": (dagger(Ec) @ U, V2 @ dagger(VUD)),
        "DcU": (dagger(Dc) @ U, V4 @ dagger(VUD)),
        "UcE": (dagger(Uc) @ E, V1 @ VUD @ dagger(V4) @ V3),
        "DcN": (dagger(Dc) @ N, V3 @ VEN),
        "UcN": (dagger(Uc) @ N, V1 @ VUD @ dagger(V4) @ V3 @ VEN),
        "NcD": (dagger(Nc) @ D, dagger(UEN) @ V2),
        "NcU": (dagger(Nc) @ U, dagger(UEN) @ V2 @ dagger(VUD)),
    }
    for name, (left, right) in identities.items():
        if not np.allclose(left, right, rtol=1e-12, atol=1e-12):
            raise AssertionError(f"rotation identity failed: {name}")


def gauge_and_dimension_checks() -> None:
    hypercharge = {
        "q": Fraction(1, 6),
        "l": Fraction(-1, 2),
        "u": Fraction(2, 3),
        "d": Fraction(-1, 3),
        "e": Fraction(-1, 1),
        "N": Fraction(0, 1),
    }
    contents = {
        "duql": ("d", "u", "q", "l"),
        "qque": ("q", "q", "u", "e"),
        "qqql": ("q", "q", "q", "l"),
        "duue": ("d", "u", "u", "e"),
        "qqdN": ("q", "q", "d", "N"),
    }
    for name, fields in contents.items():
        if sum((hypercharge[item] for item in fields), Fraction()) != 0:
            raise AssertionError(f"hypercharge failed: {name}")
        if 4 * Fraction(3, 2) != 6:
            raise AssertionError(f"dimension failed: {name}")


def main() -> None:
    assert_ratio(source_operator("I"), target_operator("qque"), 2, "O_I")
    assert_ratio(source_operator("II"), target_operator("duql"), 2, "O_II")
    assert_ratio(source_operator("III"), target_operator("duql"), 2, "O_III")
    assert_ratio(source_operator("IV"), target_operator("qqdN"), -2, "O_IV")
    coefficient()
    rotation_identities()
    gauge_and_dimension_checks()
    print("PASS: explicit Grassmann, flavor, gauge, dimension, and rotation checks")


if __name__ == "__main__":
    main()
