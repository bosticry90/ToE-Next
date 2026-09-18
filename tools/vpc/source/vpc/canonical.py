"""Canonical serialization, hashing, and bounded strict JSON input."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, BinaryIO

from .errors import CalculatorError, require


CANONICAL_DOMAIN = "VERIFIED_PHYSICS_CALCULATOR_CANONICAL_JSON_v1"


def fraction_text(value: Fraction | int | str) -> str:
    value = value if isinstance(value, Fraction) else Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_data(value: Any) -> Any:
    """Return the JSON data model used for all trusted identities.

    Binary floats are deliberately excluded.  Numerical algorithms must emit
    decimal or hexadecimal strings and record their precision/rounding policy.
    """
    if is_dataclass(value):
        value = asdict(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Fraction):
        return {"fraction": fraction_text(value)}
    if value is None or type(value) in (bool, int, str):
        return value
    if isinstance(value, float):
        raise CalculatorError("BINARY_FLOAT_NOT_CANONICAL")
    if isinstance(value, (list, tuple)):
        return [canonical_data(item) for item in value]
    if isinstance(value, dict):
        require(all(isinstance(key, str) for key in value), "NON_STRING_MAP_KEY")
        return {key: canonical_data(value[key]) for key in sorted(value)}
    if hasattr(value, "to_dict"):
        return canonical_data(value.to_dict())
    raise CalculatorError("UNSUPPORTED_CANONICAL_TYPE", detail=type(value).__name__)


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_data(value), ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("ascii")


def digest(value: Any, domain: str) -> str:
    require(isinstance(domain, str) and domain, "HASH_DOMAIN_REQUIRED")
    body = domain.encode("utf-8") + b"\0" + canonical_bytes(value)
    return hashlib.sha256(body).hexdigest()


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _json_preflight(raw: bytes, *, max_depth: int, max_string_bytes: int) -> None:
    depth = 0
    in_string = False
    escaped = False
    string_bytes = 0
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 0x5C:
                escaped = True
            elif byte == 0x22:
                in_string = False
                string_bytes = 0
            else:
                string_bytes += 1
                require(string_bytes <= max_string_bytes, "JSON_STRING_LIMIT")
            continue
        if byte == 0x22:
            in_string = True
        elif byte in (0x7B, 0x5B):
            depth += 1
            require(depth <= max_depth, "JSON_DEPTH_LIMIT")
        elif byte in (0x7D, 0x5D):
            depth -= 1
            require(depth >= 0, "JSON_STRUCTURE")
    require(not in_string and depth == 0, "JSON_STRUCTURE")


def _validate_json_tree(value: Any, *, max_container_members: int) -> None:
    if isinstance(value, list):
        require(len(value) <= max_container_members, "JSON_CONTAINER_LIMIT")
        for item in value:
            _validate_json_tree(item, max_container_members=max_container_members)
    elif isinstance(value, dict):
        require(len(value) <= max_container_members, "JSON_CONTAINER_LIMIT")
        for item in value.values():
            _validate_json_tree(item, max_container_members=max_container_members)


def strict_json_bytes(
    raw: bytes,
    *,
    max_bytes: int = 64 * 1024 * 1024,
    max_depth: int = 64,
    max_string_bytes: int = 64 * 1024,
    max_container_members: int = 65_536,
) -> Any:
    require(type(raw) is bytes and len(raw) <= max_bytes, "BUNDLE_SIZE_LIMIT")
    _json_preflight(raw, max_depth=max_depth, max_string_bytes=max_string_bytes)

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY", key)
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=object_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(CalculatorError("NONFINITE_JSON", detail=token)),
            parse_float=lambda token: (_ for _ in ()).throw(CalculatorError("BINARY_FLOAT_INPUT_FORBIDDEN", detail=token)),
        )
    except UnicodeDecodeError as exc:
        raise CalculatorError("JSON_UTF8") from exc
    except json.JSONDecodeError as exc:
        raise CalculatorError("JSON_SYNTAX", detail=str(exc)) from exc
    _validate_json_tree(value, max_container_members=max_container_members)
    return value


def bounded_read(handle: BinaryIO, max_bytes: int) -> bytes:
    raw = handle.read(max_bytes + 1)
    require(len(raw) <= max_bytes, "BUNDLE_SIZE_LIMIT")
    return raw


def strict_json_file(path: Path, **limits: int) -> Any:
    with path.open("rb") as handle:
        return strict_json_bytes(bounded_read(handle, int(limits.get("max_bytes", 64 * 1024 * 1024))), **limits)
