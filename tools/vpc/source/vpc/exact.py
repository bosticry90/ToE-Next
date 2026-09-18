"""Closed exact IR: rational functions over one canonical algebraic field."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
import operator
from typing import Any, Iterable, Mapping

import sympy as sp
from sympy.polys.domains import QQ

from .canonical import fraction_text
from .contracts import AlgebraicFieldV1, ResourceLimitsV1
from .errors import CalculatorError, require


def _fraction(value: str | int | Fraction) -> Fraction:
    require(not isinstance(value, bool), "BOOLEAN_IS_NOT_EXACT")
    result = value if isinstance(value, Fraction) else Fraction(value)
    return result


@dataclass(frozen=True)
class AlgebraicCoefficientV1:
    coordinates: tuple[Fraction, ...]  # low-to-high power basis

    @classmethod
    def decode(cls, value: Any, degree: int, limits: ResourceLimitsV1) -> "AlgebraicCoefficientV1":
        require(isinstance(value, list) and len(value) == degree, "ALGEBRAIC_COORDINATES")
        coordinates = tuple(_fraction(item) for item in value)
        require(all(max(abs(item.numerator).bit_length(), item.denominator.bit_length()) <= limits.input_integer_bits for item in coordinates), "INTEGER_LIMIT")
        return cls(coordinates)

    def to_list(self) -> list[str]:
        return [fraction_text(item) for item in self.coordinates]


@dataclass(frozen=True)
class PolynomialTermV1:
    powers: tuple[int, ...]
    coefficient: AlgebraicCoefficientV1


@dataclass(frozen=True)
class SparsePolynomialV1:
    terms: tuple[PolynomialTermV1, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"terms": [{"powers": list(term.powers), "coefficient": term.coefficient.to_list()} for term in self.terms]}


@dataclass(frozen=True)
class RationalFunctionV1:
    symbols: tuple[str, ...]
    numerator: SparsePolynomialV1
    denominator: SparsePolynomialV1

    def to_dict(self) -> dict[str, Any]:
        return {"kind": "RATIONAL_FUNCTION", "symbols": list(self.symbols), "numerator": self.numerator.to_dict(), "denominator": self.denominator.to_dict()}


@dataclass(frozen=True)
class ExactTensorV1:
    shape: tuple[int, ...]
    entries: tuple[RationalFunctionV1, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"kind": "TENSOR", "shape": list(self.shape), "entries": [entry.to_dict() for entry in self.entries]}


@dataclass(frozen=True)
class ExactBooleanV1:
    value: bool

    def to_dict(self) -> dict[str, Any]:
        return {"kind": "BOOLEAN", "value": self.value}


@dataclass(frozen=True)
class ExactAtomV1:
    atom_type: str
    value: str

    def __post_init__(self) -> None:
        require(self.atom_type in {"ENUM", "SYMBOL_TEXT", "IDENTIFIER"} and isinstance(self.value, str) and 0 < len(self.value) <= 65_536, "EXACT_ATOM")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": "ATOM", "atom_type": self.atom_type, "value": self.value}


ExactValueV1 = RationalFunctionV1 | ExactTensorV1 | ExactBooleanV1 | ExactAtomV1


class ExactRuntimeV1:
    """Normalizer and evaluator whose wire format is language-independent."""

    def __init__(self, field: AlgebraicFieldV1, symbols: Iterable[str], limits: ResourceLimitsV1 | None = None) -> None:
        self.field = field
        self.symbols = tuple(symbols)
        self.limits = limits or ResourceLimitsV1()
        require(len(self.symbols) <= self.limits.symbols and len(set(self.symbols)) == len(self.symbols), "SYMBOL_TABLE")
        self.gens = sp.symbols(self.symbols) if self.symbols else ()
        if self.symbols and not isinstance(self.gens, tuple):
            self.gens = (self.gens,)
        if field.field_id == "RATIONAL_FIELD":
            require(field.embedding == {"kind": "RATIONAL", "value": "0"} and tuple(field.minimal_polynomial) == ("0", "1"), "RATIONAL_FIELD_CANONICAL_FORM")
            self.domain = QQ
        else:
            require(field.degree <= self.limits.algebraic_degree, "ALGEBRAIC_DEGREE")
            alpha = sp.Symbol("_vpc_alpha")
            polynomial = sp.Poly(sum(sp.Rational(Fraction(coefficient).numerator, Fraction(coefficient).denominator) * alpha ** power for power, coefficient in enumerate(field.minimal_polynomial)), alpha, domain=QQ)
            require(polynomial.degree() == field.degree and polynomial.is_irreducible, "MINIMAL_POLYNOMIAL_REDUCIBLE")
            embedding = field.embedding
            if embedding["kind"] == "REAL_INTERVAL":
                require(set(embedding) == {"kind", "lower", "upper"}, "REAL_EMBEDDING_FIELDS")
                lower, upper = sp.Rational(embedding["lower"]), sp.Rational(embedding["upper"])
                require(lower < upper and polynomial.count_roots(lower, upper) == 1, "ALGEBRAIC_EMBEDDING_NOT_ISOLATING")
            elif embedding["kind"] == "COMPLEX_RECTANGLE":
                require(set(embedding) == {"kind", "real_lower", "real_upper", "imag_lower", "imag_upper"}, "COMPLEX_EMBEDDING_FIELDS")
                rl, ru = sp.Rational(embedding["real_lower"]), sp.Rational(embedding["real_upper"])
                il, iu = sp.Rational(embedding["imag_lower"]), sp.Rational(embedding["imag_upper"])
                require(rl < ru and il < iu and polynomial.count_roots(rl + il * sp.I, ru + iu * sp.I) == 1, "ALGEBRAIC_EMBEDDING_NOT_ISOLATING")
            else:
                raise CalculatorError("ALGEBRAIC_EMBEDDING_KIND")
            self.domain = QQ.alg_field_from_poly(polynomial, alias=field.primitive_element)

    def _coefficient_to_domain(self, coefficient: AlgebraicCoefficientV1):
        require(len(coefficient.coordinates) == self.field.degree, "ALGEBRAIC_COORDINATES")
        if self.domain == QQ:
            return QQ.convert(sp.Rational(coefficient.coordinates[0].numerator, coefficient.coordinates[0].denominator))
        high_to_low = [QQ.convert(sp.Rational(item.numerator, item.denominator)) for item in reversed(coefficient.coordinates)]
        while len(high_to_low) > 1 and high_to_low[0] == 0:
            high_to_low.pop(0)
        return self.domain.new(high_to_low)

    def _coefficient_from_domain(self, value) -> AlgebraicCoefficientV1:
        value = self.domain.convert(value)
        if self.domain == QQ:
            rational = Fraction(int(value.numerator), int(value.denominator))
            return AlgebraicCoefficientV1((rational,))
        raw = list(value.to_list())
        raw = [self.domain.dom.convert(item) for item in raw]
        raw = [Fraction(int(item.numerator), int(item.denominator)) for item in raw]
        raw = [Fraction(0)] * (self.field.degree - len(raw)) + raw
        return AlgebraicCoefficientV1(tuple(reversed(raw)))

    def _poly(self, value: Mapping[str, Any]) -> sp.Poly:
        require(set(value) == {"terms"} and isinstance(value["terms"], list), "POLYNOMIAL_SCHEMA")
        require(len(value["terms"]) <= self.limits.container_members, "POLYNOMIAL_TERM_LIMIT")
        terms: dict[tuple[int, ...], Any] = {}
        for row in value["terms"]:
            require(set(row) == {"powers", "coefficient"}, "POLYNOMIAL_TERM_SCHEMA")
            powers = tuple(row["powers"])
            require(len(powers) == len(self.symbols) and all(type(power) is int and 0 <= power <= 1_000_000 for power in powers), "POLYNOMIAL_POWERS")
            require(powers not in terms, "DUPLICATE_POLYNOMIAL_TERM")
            coefficient = AlgebraicCoefficientV1.decode(row["coefficient"], self.field.degree, self.limits)
            domain_value = self._coefficient_to_domain(coefficient)
            if domain_value:
                terms[powers] = domain_value
        if self.symbols:
            return sp.Poly.from_dict(terms, self.gens, domain=self.domain)
        constant = terms.get((), self.domain.zero)
        return sp.Poly(constant, sp.Symbol("_vpc_constant"), domain=self.domain)

    def _serialize_poly(self, polynomial: sp.Poly, *, constant_mode: bool = False) -> SparsePolynomialV1:
        rows: list[PolynomialTermV1] = []
        for powers, coefficient in polynomial.terms():
            if constant_mode:
                powers = ()
            converted = self._coefficient_from_domain(coefficient)
            require(all(max(abs(item.numerator).bit_length(), item.denominator.bit_length()) <= self.limits.intermediate_integer_bits for item in converted.coordinates), "INTERMEDIATE_INTEGER_LIMIT")
            if any(converted.coordinates):
                rows.append(PolynomialTermV1(tuple(int(item) for item in powers), converted))
        rows.sort(key=lambda row: row.powers, reverse=True)
        return SparsePolynomialV1(tuple(rows))

    def normalize(self, value: Mapping[str, Any]) -> RationalFunctionV1:
        require(set(value) == {"kind", "symbols", "numerator", "denominator"} and value["kind"] == "RATIONAL_FUNCTION", "RATIONAL_FUNCTION_SCHEMA")
        require(tuple(value["symbols"]) == self.symbols, "RATIONAL_FUNCTION_SYMBOL_TABLE")
        numerator, denominator = self._poly(value["numerator"]), self._poly(value["denominator"])
        require(not denominator.is_zero, "ZERO_DENOMINATOR")
        constant_mode = not self.symbols
        if numerator.is_zero:
            one = sp.Poly(self.domain.one, denominator.gens, domain=self.domain)
            return RationalFunctionV1(self.symbols, self._serialize_poly(numerator, constant_mode=constant_mode), self._serialize_poly(one, constant_mode=constant_mode))
        common = numerator.gcd(denominator)
        numerator, denominator = numerator.exquo(common), denominator.exquo(common)
        scale = denominator.LC()
        numerator, denominator = numerator.mul_ground(self.domain.one / scale), denominator.mul_ground(self.domain.one / scale)
        return RationalFunctionV1(self.symbols, self._serialize_poly(numerator, constant_mode=constant_mode), self._serialize_poly(denominator, constant_mode=constant_mode))

    def decode_scalar(self, value: Any) -> RationalFunctionV1:
        require(isinstance(value, Mapping), "EXACT_SCALAR_OBJECT")
        return self.normalize(value)

    def rational(self, value: str | int | Fraction) -> RationalFunctionV1:
        rational = _fraction(value)
        zero_powers = [0] * len(self.symbols)
        numerator = {"terms": [] if rational == 0 else [{"powers": zero_powers, "coefficient": [fraction_text(rational)] + ["0"] * (self.field.degree - 1)}]}
        denominator = {"terms": [{"powers": zero_powers, "coefficient": ["1"] + ["0"] * (self.field.degree - 1)}]}
        return self.normalize({"kind": "RATIONAL_FUNCTION", "symbols": list(self.symbols), "numerator": numerator, "denominator": denominator})

    def symbol(self, name: str) -> RationalFunctionV1:
        require(name in self.symbols, "UNKNOWN_SYMBOL", name)
        powers = [0] * len(self.symbols)
        powers[self.symbols.index(name)] = 1
        return self.normalize({"kind": "RATIONAL_FUNCTION", "symbols": list(self.symbols), "numerator": {"terms": [{"powers": powers, "coefficient": ["1"] + ["0"] * (self.field.degree - 1)}]}, "denominator": {"terms": [{"powers": [0] * len(self.symbols), "coefficient": ["1"] + ["0"] * (self.field.degree - 1)}]}})

    def algebraic(self, coordinates: Iterable[str | int | Fraction]) -> RationalFunctionV1:
        coefficient = AlgebraicCoefficientV1(tuple(_fraction(item) for item in coordinates))
        require(len(coefficient.coordinates) == self.field.degree, "ALGEBRAIC_COORDINATES")
        return self.normalize({"kind": "RATIONAL_FUNCTION", "symbols": list(self.symbols), "numerator": {"terms": [{"powers": [0] * len(self.symbols), "coefficient": coefficient.to_list()}]}, "denominator": {"terms": [{"powers": [0] * len(self.symbols), "coefficient": ["1"] + ["0"] * (self.field.degree - 1)}]}})

    def _as_polys(self, value: RationalFunctionV1) -> tuple[sp.Poly, sp.Poly]:
        require(value.symbols == self.symbols, "RATIONAL_FUNCTION_SYMBOL_TABLE")
        return self._poly(value.numerator.to_dict()), self._poly(value.denominator.to_dict())

    def _from_polys(self, numerator: sp.Poly, denominator: sp.Poly) -> RationalFunctionV1:
        raw = {"kind": "RATIONAL_FUNCTION", "symbols": list(self.symbols), "numerator": self._serialize_poly(numerator, constant_mode=not self.symbols).to_dict(), "denominator": self._serialize_poly(denominator, constant_mode=not self.symbols).to_dict()}
        return self.normalize(raw)

    def add(self, left: RationalFunctionV1, right: RationalFunctionV1) -> RationalFunctionV1:
        ln, ld = self._as_polys(left); rn, rd = self._as_polys(right)
        return self._from_polys(ln * rd + rn * ld, ld * rd)

    def negate(self, value: RationalFunctionV1) -> RationalFunctionV1:
        numerator, denominator = self._as_polys(value)
        return self._from_polys(-numerator, denominator)

    def subtract(self, left: RationalFunctionV1, right: RationalFunctionV1) -> RationalFunctionV1:
        return self.add(left, self.negate(right))

    def multiply(self, left: RationalFunctionV1, right: RationalFunctionV1) -> RationalFunctionV1:
        ln, ld = self._as_polys(left); rn, rd = self._as_polys(right)
        return self._from_polys(ln * rn, ld * rd)

    def divide(self, left: RationalFunctionV1, right: RationalFunctionV1) -> RationalFunctionV1:
        ln, ld = self._as_polys(left); rn, rd = self._as_polys(right)
        require(not rn.is_zero, "ZERO_DIVISOR")
        return self._from_polys(ln * rd, ld * rn)

    def power(self, value: RationalFunctionV1, exponent: int) -> RationalFunctionV1:
        require(type(exponent) is int and abs(exponent) <= 32, "POWER_LIMIT")
        numerator, denominator = self._as_polys(value)
        if exponent < 0:
            require(not numerator.is_zero, "ZERO_DIVISOR")
            numerator, denominator, exponent = denominator, numerator, -exponent
        return self._from_polys(numerator ** exponent, denominator ** exponent)

    def equal(self, left: RationalFunctionV1, right: RationalFunctionV1) -> bool:
        return left == right

    def parse_rational_text(self, text: str) -> RationalFunctionV1:
        """Parse only rational arithmetic and the frozen symbol table."""
        require(isinstance(text, str) and 0 < len(text) <= self.limits.scalar_text_chars, "SCALAR_TEXT_LIMIT")
        try:
            tree = ast.parse(text.replace("^", "**"), mode="eval")
        except (SyntaxError, ValueError) as exc:
            raise CalculatorError("EXACT_SYNTAX") from exc
        require(sum(1 for _ in ast.walk(tree)) <= self.limits.expression_nodes, "EXPRESSION_NODE_LIMIT")

        def visit(node: ast.AST) -> RationalFunctionV1:
            if isinstance(node, ast.Constant) and type(node.value) is int:
                require(abs(node.value).bit_length() <= self.limits.input_integer_bits, "INTEGER_LIMIT")
                return self.rational(node.value)
            if isinstance(node, ast.Name):
                return self.symbol(node.id)
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                value = visit(node.operand)
                return value if isinstance(node.op, ast.UAdd) else self.negate(value)
            if isinstance(node, ast.BinOp):
                left, right = visit(node.left), visit(node.right)
                if isinstance(node.op, ast.Add): return self.add(left, right)
                if isinstance(node.op, ast.Sub): return self.subtract(left, right)
                if isinstance(node.op, ast.Mult): return self.multiply(left, right)
                if isinstance(node.op, ast.Div): return self.divide(left, right)
                if isinstance(node.op, ast.Pow):
                    require(isinstance(node.right, ast.Constant) and type(node.right.value) is int, "POWER_REQUIRES_INTEGER")
                    return self.power(left, node.right.value)
            raise CalculatorError("UNSUPPORTED_EXACT_TRANSCENDENTAL_OR_SYNTAX")

        return visit(tree.body)

    def decode(self, value: Mapping[str, Any]) -> ExactValueV1:
        kind = value.get("kind")
        if kind == "RATIONAL_FUNCTION":
            return self.decode_scalar(value)
        if kind == "BOOLEAN":
            require(set(value) == {"kind", "value"} and type(value["value"]) is bool, "EXACT_BOOLEAN")
            return ExactBooleanV1(value["value"])
        if kind == "ATOM":
            require(set(value) == {"kind", "atom_type", "value"}, "EXACT_ATOM")
            return ExactAtomV1(value["atom_type"], value["value"])
        require(kind == "TENSOR" and set(value) == {"kind", "shape", "entries"}, "EXACT_VALUE_KIND")
        shape = tuple(value["shape"])
        require(shape and all(type(size) is int and size > 0 for size in shape), "TENSOR_SHAPE")
        count = reduce(operator.mul, shape, 1)
        require(count <= self.limits.tensor_entries and len(value["entries"]) == count, "TENSOR_ENTRY_COUNT")
        return ExactTensorV1(shape, tuple(self.decode_scalar(item) for item in value["entries"]))

    def tensor(self, shape: Iterable[int], entries: Iterable[RationalFunctionV1]) -> ExactTensorV1:
        result = ExactTensorV1(tuple(shape), tuple(entries))
        require(reduce(operator.mul, result.shape, 1) == len(result.entries) <= self.limits.tensor_entries, "TENSOR_ENTRY_COUNT")
        return result

    def elementwise(self, operation: str, left: ExactValueV1, right: ExactValueV1) -> ExactValueV1:
        function = {"ADD": self.add, "SUB": self.subtract, "MUL": self.multiply}.get(operation)
        require(function is not None, "ELEMENTWISE_OPERATION")
        require(isinstance(left, (RationalFunctionV1, ExactTensorV1)) and isinstance(right, (RationalFunctionV1, ExactTensorV1)), "ARITHMETIC_VALUE_REQUIRED")
        if isinstance(left, RationalFunctionV1) and isinstance(right, RationalFunctionV1):
            return function(left, right)
        if isinstance(left, ExactTensorV1) and isinstance(right, ExactTensorV1):
            require(left.shape == right.shape, "TENSOR_SHAPE")
            return ExactTensorV1(left.shape, tuple(function(a, b) for a, b in zip(left.entries, right.entries)))
        require(operation == "MUL", "SCALAR_TENSOR_OPERATION")
        scalar, tensor = (left, right) if isinstance(left, RationalFunctionV1) else (right, left)
        require(isinstance(scalar, RationalFunctionV1) and isinstance(tensor, ExactTensorV1), "SCALAR_TENSOR_OPERATION")
        return ExactTensorV1(tensor.shape, tuple(self.multiply(scalar, item) for item in tensor.entries))

    def matmul(self, left: ExactTensorV1, right: ExactTensorV1) -> ExactTensorV1:
        require(len(left.shape) == len(right.shape) == 2 and left.shape[1] == right.shape[0], "MATRIX_SHAPE")
        rows, common, columns = left.shape[0], left.shape[1], right.shape[1]
        entries = []
        for i in range(rows):
            for j in range(columns):
                value = self.rational(0)
                for k in range(common):
                    value = self.add(value, self.multiply(left.entries[i * common + k], right.entries[k * columns + j]))
                entries.append(value)
        return ExactTensorV1((rows, columns), tuple(entries))
