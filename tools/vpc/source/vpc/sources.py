"""Offline, hash-bound, typed source reference resolution."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from .canonical import bounded_read, strict_json_bytes
from .contracts import ResourceLimitsV1
from .errors import CalculatorError, require


def json_pointer(document: Any, pointer: str) -> Any:
    require(isinstance(pointer, str) and (pointer == "" or pointer.startswith("/")), "JSON_POINTER_SYNTAX")
    value = document
    if not pointer:
        return value
    for encoded in pointer[1:].split("/"):
        require("~" not in encoded.replace("~0", "").replace("~1", ""), "JSON_POINTER_ESCAPE")
        key = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            require(key in value, "SOURCE_LOCATOR_NOT_FOUND", pointer)
            value = value[key]
        elif isinstance(value, list):
            require(key.isdigit() and (key == "0" or not key.startswith("0")), "SOURCE_ARRAY_INDEX", pointer)
            index = int(key)
            require(index < len(value), "SOURCE_LOCATOR_NOT_FOUND", pointer)
            value = value[index]
        else:
            raise CalculatorError("SOURCE_LOCATOR_NOT_FOUND", pointer)
    return value


@dataclass(frozen=True)
class ResolvedSourceV1:
    reference_type: str
    artifact_path: str
    artifact_sha256: str
    canonical_locator: str
    value: Any

    def receipt(self) -> dict[str, Any]:
        return {"reference_type": self.reference_type, "artifact_path": self.artifact_path, "artifact_sha256": self.artifact_sha256, "canonical_locator": self.canonical_locator}


class SourceResolverV1:
    def __init__(self, root: Path, declarations: tuple[Mapping[str, Any], ...], limits: ResourceLimitsV1 | None = None) -> None:
        self.root = root.resolve(strict=True)
        self.limits = limits or ResourceLimitsV1()
        self.rows: dict[str, Mapping[str, Any]] = {}
        self.documents: dict[str, Any] = {}
        for row in declarations:
            require(set(row) == {"path", "sha256", "byte_size", "media_type"}, "SOURCE_DECLARATION_FIELDS")
            relative = row["path"]
            posix = PurePosixPath(relative)
            require(isinstance(relative, str) and not posix.is_absolute() and ".." not in posix.parts and "\\" not in relative and ":" not in relative, "SOURCE_PATH_ESCAPE", str(relative))
            require(relative not in self.rows, "DUPLICATE_SOURCE_PATH", relative)
            path = (self.root / Path(*posix.parts)).resolve(strict=True)
            require(path != self.root and self.root in path.parents, "SOURCE_PATH_ESCAPE", relative)
            with path.open("rb") as handle:
                raw = bounded_read(handle, self.limits.bundle_bytes)
            require(len(raw) == row["byte_size"], "SOURCE_BYTE_SIZE", relative)
            actual_hash = hashlib.sha256(raw).hexdigest()
            require(actual_hash == row["sha256"], "SOURCE_IDENTITY_MISMATCH", relative)
            require(row["media_type"] == "application/json", "UNSUPPORTED_TRUSTED_SOURCE_MEDIA", relative)
            self.rows[relative] = dict(row)
            self.documents[relative] = strict_json_bytes(raw, max_bytes=self.limits.bundle_bytes, max_depth=self.limits.json_depth, max_string_bytes=self.limits.string_bytes, max_container_members=self.limits.container_members)

    def _artifact(self, reference: Mapping[str, Any]) -> tuple[str, Any]:
        path = reference.get("artifact_path")
        require(path in self.rows, "SOURCE_NOT_ALLOWLISTED", str(path))
        require(reference.get("artifact_sha256") == self.rows[path]["sha256"], "SOURCE_REFERENCE_HASH", str(path))
        return path, self.documents[path]

    def resolve(self, reference: Mapping[str, Any]) -> ResolvedSourceV1:
        kind = reference.get("type")
        require(kind in {"JsonPointerValueRef", "UniqueTableCellRef", "TensorComponentRef", "NamedConventionRef"}, "SOURCE_REFERENCE_TYPE")
        path, document = self._artifact(reference)
        base = {"type", "artifact_path", "artifact_sha256"}
        if kind == "JsonPointerValueRef":
            require(set(reference) == base | {"pointer"}, "SOURCE_REFERENCE_FIELDS")
            pointer = reference["pointer"]
            value = json_pointer(document, pointer)
            locator = pointer
        elif kind == "UniqueTableCellRef":
            require(set(reference) == base | {"table_pointer", "match_field", "match_value", "value_pointer"}, "SOURCE_REFERENCE_FIELDS")
            rows = json_pointer(document, reference["table_pointer"])
            require(isinstance(rows, list), "SOURCE_TABLE_REQUIRED")
            matches = [(index, row) for index, row in enumerate(rows) if isinstance(row, dict) and row.get(reference["match_field"]) == reference["match_value"]]
            require(len(matches) == 1, "SOURCE_SELECTION_NOT_UNIQUE")
            index, row = matches[0]
            value = json_pointer(row, reference["value_pointer"])
            locator = f"{reference['table_pointer']}/{index}{reference['value_pointer']}"
        elif kind == "TensorComponentRef":
            require(set(reference) == base | {"pointer", "indices"}, "SOURCE_REFERENCE_FIELDS")
            value = json_pointer(document, reference["pointer"])
            locator = reference["pointer"]
            for index in reference["indices"]:
                require(type(index) is int and isinstance(value, list) and 0 <= index < len(value), "TENSOR_COMPONENT_INDEX")
                value = value[index]
                locator += f"/{index}"
        else:
            require(set(reference) == base | {"conventions_pointer", "name"}, "SOURCE_REFERENCE_FIELDS")
            conventions = json_pointer(document, reference["conventions_pointer"])
            require(isinstance(conventions, dict) and reference["name"] in conventions, "NAMED_CONVENTION_NOT_FOUND")
            value = conventions[reference["name"]]
            locator = f"{reference['conventions_pointer']}/{reference['name'].replace('~', '~0').replace('/', '~1')}"
        return ResolvedSourceV1(kind, path, self.rows[path]["sha256"], locator, value)
