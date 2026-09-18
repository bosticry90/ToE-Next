"""Exact dimension vectors modulo profile-declared natural-unit relations."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .contracts import DimensionSystemV1
from .errors import require


def _rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], tuple[int, ...]]:
    if not rows:
        return rows, ()
    width = len(rows[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(width):
        chosen = next((row for row in range(pivot_row, len(rows)) if rows[row][column]), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [item / scale for item in rows[pivot_row]]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [left - factor * right for left, right in zip(rows[row], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return [row for row in rows if any(row)], tuple(pivots)


@dataclass(frozen=True)
class DimensionVectorV1:
    exponents: tuple[Fraction, ...]

    @classmethod
    def decode(cls, values: Iterable[str | int | Fraction], system: DimensionSystemV1) -> "DimensionVectorV1":
        vector = tuple(Fraction(value) for value in values)
        require(len(vector) == len(system.basis), "DIMENSION_VECTOR_ARITY")
        if system.exponent_domain == "INTEGER":
            require(all(value.denominator == 1 for value in vector), "NONINTEGER_DIMENSION")
        return cls(vector)

    def to_list(self) -> list[str]:
        return [str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}" for value in self.exponents]

    def __add__(self, other: "DimensionVectorV1") -> "DimensionVectorV1":
        require(len(self.exponents) == len(other.exponents), "DIMENSION_VECTOR_ARITY")
        return DimensionVectorV1(tuple(a + b for a, b in zip(self.exponents, other.exponents)))

    def __sub__(self, other: "DimensionVectorV1") -> "DimensionVectorV1":
        require(len(self.exponents) == len(other.exponents), "DIMENSION_VECTOR_ARITY")
        return DimensionVectorV1(tuple(a - b for a, b in zip(self.exponents, other.exponents)))

    def scale(self, power: int) -> "DimensionVectorV1":
        require(type(power) is int, "DIMENSION_POWER")
        return DimensionVectorV1(tuple(power * value for value in self.exponents))


class DimensionQuotientV1:
    """Canonical quotient-space comparison for natural-unit conventions."""

    def __init__(self, system: DimensionSystemV1) -> None:
        self.system = system
        rows = [[Fraction(item) for item in row] for row in system.quotient_relations]
        self.relations, self.pivots = _rref(rows)

    def normal_form(self, value: DimensionVectorV1) -> DimensionVectorV1:
        result = list(value.exponents)
        for row, pivot in zip(self.relations, self.pivots):
            factor = result[pivot]
            if factor:
                result = [left - factor * right for left, right in zip(result, row)]
        return DimensionVectorV1(tuple(result))

    def equivalent(self, left: DimensionVectorV1, right: DimensionVectorV1) -> bool:
        return self.normal_form(left) == self.normal_form(right)

    def require_equivalent(self, left: DimensionVectorV1, right: DimensionVectorV1, location: str = "") -> None:
        require(self.equivalent(left, right), "DIMENSION_MISMATCH", location)
