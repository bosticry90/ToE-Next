"""Versioned contracts and independent assurance axes for calculator v1."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
import re
from typing import Any, Iterable, Mapping

from .canonical import canonical_data, digest, fraction_text
from .errors import CalculatorError, require


IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def _identifier(value: str, location: str) -> str:
    require(isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None, "IDENTIFIER", location)
    return value


def _hash(value: str, location: str) -> str:
    require(isinstance(value, str) and HEX64.fullmatch(value) is not None, "SHA256", location)
    return value


def _keys(value: Mapping[str, Any], required: Iterable[str], optional: Iterable[str] = ()) -> None:
    required, optional = set(required), set(optional)
    require(isinstance(value, Mapping), "OBJECT_REQUIRED")
    require(set(value) == required | (set(value) & optional), "CONTRACT_FIELDS", detail=",".join(sorted(set(value) ^ required)))


class ExecutionStatus(str, Enum):
    NOT_RUN = "NOT_RUN"
    SUCCEEDED = "SUCCEEDED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"


class ReplayStatus(str, Enum):
    NOT_RUN = "NOT_RUN"
    MATCHED = "MATCHED"
    MISMATCHED = "MISMATCHED"


class VerificationClass(str, Enum):
    NONE = "NONE"
    DETERMINISTICALLY_RECOMPUTED = "DETERMINISTICALLY_RECOMPUTED"
    CROSSCHECKED_NUMERICAL = "CROSSCHECKED_NUMERICAL"
    VERIFIED_EXACT = "VERIFIED_EXACT"
    VERIFIED_ENCLOSURE = "VERIFIED_ENCLOSURE"


class ChallengeDisposition(str, Enum):
    NOT_RUN = "NOT_RUN"
    PASSED = "PASSED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class UncertaintySemantics(str, Enum):
    GUARANTEED_RANGE = "GUARANTEED_RANGE"
    LOCAL_LINEAR_COVARIANCE = "LOCAL_LINEAR_COVARIANCE"
    SAMPLED_DISTRIBUTION_ESTIMATE = "SAMPLED_DISTRIBUTION_ESTIMATE"


@dataclass(frozen=True)
class ResourceLimitsV1:
    bundle_bytes: int = 64 * 1024 * 1024
    json_depth: int = 64
    string_bytes: int = 64 * 1024
    scalar_text_chars: int = 2_048
    container_members: int = 65_536
    tensor_entries: int = 262_144
    dag_nodes: int = 4_096
    expression_nodes: int = 256
    symbols: int = 256
    input_integer_bits: int = 256
    intermediate_integer_bits: int = 16_384
    algebraic_degree: int = 64
    numerical_precision_bits: int = 2_560
    trusted_route_seconds: int = 1_800
    trusted_total_seconds: int = 5_400
    evidence_bytes: int = 256 * 1024 * 1024
    plugin_seconds: int = 60
    plugin_output_bytes: int = 10 * 1024 * 1024

    def __post_init__(self) -> None:
        for key, value in self.__dict__.items():
            require(type(value) is int and value > 0, "RESOURCE_LIMIT", key)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ResourceLimitsV1":
        require(set(value) == set(cls().__dict__), "RESOURCE_LIMIT_FIELDS")
        return cls(**dict(value))

    def to_dict(self) -> dict[str, int]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class AlgebraicFieldV1:
    field_id: str
    primitive_element: str
    minimal_polynomial: tuple[str, ...]  # low-to-high rational coefficients
    embedding: Mapping[str, Any]
    ordered_power_basis: tuple[str, ...]

    def __post_init__(self) -> None:
        _identifier(self.field_id, "field_id")
        _identifier(self.primitive_element, "primitive_element")
        require(2 <= len(self.minimal_polynomial) <= 65, "ALGEBRAIC_DEGREE")
        coefficients = tuple(Fraction(item) for item in self.minimal_polynomial)
        require(coefficients[-1] == 1, "MINIMAL_POLYNOMIAL_NOT_MONIC")
        degree = len(coefficients) - 1
        require(len(self.ordered_power_basis) == degree, "POWER_BASIS_LENGTH")
        expected = tuple("1" if i == 0 else self.primitive_element if i == 1 else f"{self.primitive_element}^{i}" for i in range(degree))
        require(self.ordered_power_basis == expected, "POWER_BASIS_ORDER")
        require(self.embedding.get("kind") in {"REAL_INTERVAL", "COMPLEX_RECTANGLE", "RATIONAL"}, "ALGEBRAIC_EMBEDDING_KIND")

    @property
    def degree(self) -> int:
        return len(self.minimal_polynomial) - 1

    @classmethod
    def rational(cls) -> "AlgebraicFieldV1":
        return cls("RATIONAL_FIELD", "alpha", ("0", "1"), {"kind": "RATIONAL", "value": "0"}, ("1",))

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AlgebraicFieldV1":
        _keys(value, ("schema_id", "field_id", "primitive_element", "minimal_polynomial", "embedding", "ordered_power_basis"))
        require(value["schema_id"] == "AlgebraicFieldV1", "SCHEMA_ID")
        return cls(value["field_id"], value["primitive_element"], tuple(value["minimal_polynomial"]), dict(value["embedding"]), tuple(value["ordered_power_basis"]))

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "AlgebraicFieldV1",
            "field_id": self.field_id,
            "primitive_element": self.primitive_element,
            "minimal_polynomial": list(self.minimal_polynomial),
            "embedding": dict(self.embedding),
            "ordered_power_basis": list(self.ordered_power_basis),
        }


@dataclass(frozen=True)
class DimensionSystemV1:
    basis: tuple[str, ...]
    exponent_domain: str
    quotient_relations: tuple[tuple[str, ...], ...]

    def __post_init__(self) -> None:
        require(self.basis and len(set(self.basis)) == len(self.basis), "DIMENSION_BASIS")
        require(self.exponent_domain in {"INTEGER", "RATIONAL"}, "DIMENSION_EXPONENT_DOMAIN")
        for row in self.quotient_relations:
            require(len(row) == len(self.basis), "DIMENSION_RELATION_ARITY")
            tuple(Fraction(item) for item in row)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DimensionSystemV1":
        _keys(value, ("basis", "exponent_domain", "quotient_relations"))
        return cls(tuple(value["basis"]), value["exponent_domain"], tuple(tuple(row) for row in value["quotient_relations"]))

    def to_dict(self) -> dict[str, Any]:
        return {"basis": list(self.basis), "exponent_domain": self.exponent_domain, "quotient_relations": [list(row) for row in self.quotient_relations]}


@dataclass(frozen=True)
class PhysicsProfileV1:
    profile_id: str
    symbols: tuple[str, ...]
    algebraic_field: AlgebraicFieldV1
    dimensions: DimensionSystemV1
    unit_conventions: tuple[str, ...]
    semantic_types: tuple[str, ...]
    index_spaces: Mapping[str, int]
    representation_tags: tuple[str, ...]
    source_declarations: tuple[Mapping[str, Any], ...]
    permitted_operations: tuple[str, ...]
    output_roots: tuple[str, ...]
    output_claims: Mapping[str, str]

    def __post_init__(self) -> None:
        _identifier(self.profile_id, "profile_id")
        require(len(self.symbols) == len(set(self.symbols)) <= 256, "SYMBOL_TABLE")
        for symbol in self.symbols:
            _identifier(symbol, "symbol")
        require(self.output_roots and len(set(self.output_roots)) == len(self.output_roots), "OUTPUT_ROOTS")
        require(self.unit_conventions and len(set(self.unit_conventions)) == len(self.unit_conventions), "UNIT_CONVENTIONS")
        require(self.semantic_types and len(set(self.semantic_types)) == len(self.semantic_types), "SEMANTIC_TYPES")
        require(set(self.output_claims) == set(self.output_roots), "OUTPUT_CLAIM_COVERAGE")
        require(self.permitted_operations and len(set(self.permitted_operations)) == len(self.permitted_operations), "OPERATION_SET")
        require(all(type(size) is int and size > 0 for size in self.index_spaces.values()), "INDEX_SPACE")

    @property
    def contract_hash(self) -> str:
        return digest(self.to_dict(), "PhysicsProfileV1")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "PhysicsProfileV1":
        _keys(value, ("schema_id", "profile_id", "symbols", "algebraic_field", "dimensions", "unit_conventions", "semantic_types", "index_spaces", "representation_tags", "source_declarations", "permitted_operations", "output_roots", "output_claims"))
        require(value["schema_id"] == "PhysicsProfileV1", "SCHEMA_ID")
        return cls(
            value["profile_id"], tuple(value["symbols"]), AlgebraicFieldV1.from_dict(value["algebraic_field"]),
            DimensionSystemV1.from_dict(value["dimensions"]), tuple(value["unit_conventions"]), tuple(value["semantic_types"]), dict(value["index_spaces"]),
            tuple(value["representation_tags"]), tuple(dict(row) for row in value["source_declarations"]),
            tuple(value["permitted_operations"]), tuple(value["output_roots"]), dict(value["output_claims"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "PhysicsProfileV1", "profile_id": self.profile_id, "symbols": list(self.symbols),
            "algebraic_field": self.algebraic_field.to_dict(), "dimensions": self.dimensions.to_dict(),
            "unit_conventions": list(self.unit_conventions), "semantic_types": list(self.semantic_types), "index_spaces": dict(self.index_spaces),
            "representation_tags": list(self.representation_tags), "source_declarations": [dict(row) for row in self.source_declarations],
            "permitted_operations": list(self.permitted_operations), "output_roots": list(self.output_roots),
            "output_claims": dict(self.output_claims),
        }


@dataclass(frozen=True)
class QMCPolicyV1:
    generator_family: str
    specification_version: str
    direction_table: str
    scrambling: str
    ordering: str
    sample_count_convention: str

    def __post_init__(self) -> None:
        require(self.generator_family == "SOBOL", "QMC_GENERATOR_FAMILY")
        require(self.specification_version == "VPC_SOBOL_UINT32_V1", "QMC_SPECIFICATION_VERSION")
        require(self.direction_table == "VPC_SOBOL_2D_BRATLEY_FOX_BASE_V1", "QMC_DIRECTION_TABLE")
        require(self.scrambling in {"NONE", "DIGITAL_XOR_SHA256_V1"}, "QMC_SCRAMBLING")
        require(self.ordering == "GRAY_CODE_INDEX_ORDER" and self.sample_count_convention == "FIRST_N_FROM_INDEX_ZERO", "QMC_ORDERING")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "QMCPolicyV1":
        _keys(value, ("generator_family", "specification_version", "direction_table", "scrambling", "ordering", "sample_count_convention"))
        return cls(**dict(value))

    def to_dict(self) -> dict[str, str]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class VerificationPolicyV1:
    policy_id: str
    freeze_timestamp: str
    python_verifier: str
    julia_verifier: str
    lean_verifier: str
    mandatory_challenge_hashes: tuple[str, ...]
    numerical_policy: Mapping[str, Any]
    qmc_policy: QMCPolicyV1
    resource_limits: ResourceLimitsV1 = field(default_factory=ResourceLimitsV1)
    trusted_network_access: str = "FORBIDDEN"

    def __post_init__(self) -> None:
        _identifier(self.policy_id, "policy_id")
        require(self.freeze_timestamp.endswith("Z"), "FREEZE_TIMESTAMP")
        require(self.trusted_network_access == "FORBIDDEN", "TRUSTED_NETWORK_POLICY")
        require(len(set(self.mandatory_challenge_hashes)) == len(self.mandatory_challenge_hashes), "CHALLENGE_HASH_DUPLICATE")
        for item in self.mandatory_challenge_hashes:
            _hash(item, "mandatory_challenge_hash")
        numerical_required = {
            "exact_language", "enclosure_promotion", "floating_agreement_ceiling", "trusted_ode_rhs",
            "ode_python_methods", "ode_julia_method", "ode_rtol_ceiling", "ode_atol_ceiling",
            "uncertainty_semantics",
        }
        require(set(self.numerical_policy) == numerical_required, "NUMERICAL_POLICY_FIELDS")
        require(self.numerical_policy["exact_language"] == "CANONICAL_MATH_V1_RATIONAL_FUNCTIONS", "EXACT_LANGUAGE_POLICY")
        require(self.numerical_policy["enclosure_promotion"] == "INDEPENDENT_CERTIFICATE_REQUIRED" and self.numerical_policy["floating_agreement_ceiling"] == "CROSSCHECKED_NUMERICAL", "NUMERICAL_ASSURANCE_POLICY")
        require(self.numerical_policy["trusted_ode_rhs"] == "DECLARATIVE_IR_ONLY", "TRUSTED_ODE_POLICY")
        require(tuple(self.numerical_policy["ode_python_methods"]) == ("DOP853", "RK45", "Radau") and self.numerical_policy["ode_julia_method"] == "Vern9", "ODE_ALGORITHM_POLICY")
        require(Fraction(self.numerical_policy["ode_rtol_ceiling"]) == Fraction("1/1000") and Fraction(self.numerical_policy["ode_atol_ceiling"]) == Fraction("1/1000"), "ODE_TOLERANCE_POLICY")
        require(tuple(self.numerical_policy["uncertainty_semantics"]) == tuple(item.value for item in UncertaintySemantics), "UNCERTAINTY_SEMANTICS_POLICY")

    @property
    def contract_hash(self) -> str:
        return digest(self.to_dict(), "VerificationPolicyV1")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "VerificationPolicyV1":
        _keys(value, ("schema_id", "policy_id", "freeze_timestamp", "python_verifier", "julia_verifier", "lean_verifier", "mandatory_challenge_hashes", "numerical_policy", "qmc_policy", "resource_limits", "trusted_network_access"))
        require(value["schema_id"] == "VerificationPolicyV1", "SCHEMA_ID")
        return cls(
            value["policy_id"], value["freeze_timestamp"], value["python_verifier"], value["julia_verifier"], value["lean_verifier"],
            tuple(value["mandatory_challenge_hashes"]), dict(value["numerical_policy"]), QMCPolicyV1.from_dict(value["qmc_policy"]),
            ResourceLimitsV1.from_dict(value["resource_limits"]), value["trusted_network_access"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "VerificationPolicyV1", "policy_id": self.policy_id, "freeze_timestamp": self.freeze_timestamp,
            "python_verifier": self.python_verifier, "julia_verifier": self.julia_verifier, "lean_verifier": self.lean_verifier,
            "mandatory_challenge_hashes": list(self.mandatory_challenge_hashes), "numerical_policy": dict(self.numerical_policy),
            "qmc_policy": self.qmc_policy.to_dict(), "resource_limits": self.resource_limits.to_dict(),
            "trusted_network_access": self.trusted_network_access,
        }


@dataclass(frozen=True)
class CalculationRequestV1:
    physics_profile_hash: str
    verification_policy_hash: str
    inputs: Mapping[str, Any]
    requested_roots: tuple[str, ...]
    execution_budgets: Mapping[str, int]
    stochastic_experiments: tuple[Mapping[str, Any], ...] = ()

    def __post_init__(self) -> None:
        _hash(self.physics_profile_hash, "physics_profile_hash")
        _hash(self.verification_policy_hash, "verification_policy_hash")
        require(self.requested_roots and len(set(self.requested_roots)) == len(self.requested_roots), "REQUEST_ROOTS")
        require(all(type(value) is int and value > 0 for value in self.execution_budgets.values()), "EXECUTION_BUDGET")
        canonical_data(self.inputs)
        canonical_data(self.stochastic_experiments)

    @property
    def computation_id(self) -> str:
        return digest(self.to_dict(), "CalculationRequestV1:computation")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CalculationRequestV1":
        _keys(value, ("schema_id", "physics_profile_hash", "verification_policy_hash", "inputs", "requested_roots", "execution_budgets", "stochastic_experiments"))
        require(value["schema_id"] == "CalculationRequestV1", "SCHEMA_ID")
        require("scientific_authority" not in value and "authority_binding_hash" not in value, "AUTHORITY_IN_COMPUTATION_ID")
        return cls(value["physics_profile_hash"], value["verification_policy_hash"], dict(value["inputs"]), tuple(value["requested_roots"]), dict(value["execution_budgets"]), tuple(dict(row) for row in value["stochastic_experiments"]))

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "CalculationRequestV1", "physics_profile_hash": self.physics_profile_hash,
            "verification_policy_hash": self.verification_policy_hash, "inputs": dict(self.inputs),
            "requested_roots": list(self.requested_roots), "execution_budgets": dict(self.execution_budgets),
            "stochastic_experiments": [dict(row) for row in self.stochastic_experiments],
        }


@dataclass(frozen=True)
class CandidatePacketV1:
    computation_id: str
    producer: Mapping[str, Any]
    graph: Mapping[str, Any]
    claimed_outputs: Mapping[str, Any]
    source_bindings: tuple[Mapping[str, Any], ...]
    generator_provenance: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        _hash(self.computation_id, "computation_id")
        require(self.producer.get("trust") == "UNTRUSTED_PROPOSAL", "PRODUCER_TRUST_LABEL")
        canonical_data(self.to_dict())

    @property
    def candidate_hash(self) -> str:
        return digest(self.to_dict(), "CandidatePacketV1")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CandidatePacketV1":
        _keys(value, ("schema_id", "computation_id", "producer", "graph", "claimed_outputs", "source_bindings"), ("generator_provenance",))
        require(value["schema_id"] == "CandidatePacketV1", "SCHEMA_ID")
        return cls(value["computation_id"], dict(value["producer"]), dict(value["graph"]), dict(value["claimed_outputs"]), tuple(dict(row) for row in value["source_bindings"]), dict(value["generator_provenance"]) if value.get("generator_provenance") is not None else None)

    def to_dict(self) -> dict[str, Any]:
        result = {
            "schema_id": "CandidatePacketV1", "computation_id": self.computation_id, "producer": dict(self.producer),
            "graph": dict(self.graph), "claimed_outputs": dict(self.claimed_outputs),
            "source_bindings": [dict(row) for row in self.source_bindings],
        }
        if self.generator_provenance is not None:
            result["generator_provenance"] = dict(self.generator_provenance)
        return result


@dataclass(frozen=True)
class ClaimAuthorityBindingV1:
    authority_state: str
    historical_label: str
    supporting_record_hashes: tuple[str, ...]
    scope: str
    limitations: tuple[str, ...]
    effective_time: str
    claim_ceiling: str

    def __post_init__(self) -> None:
        require(self.authority_state in {"UNBOUND", "PENDING", "WITHHELD", "REVIEWED_SUPPORTED", "TERMINALLY_ADJUDICATED"}, "AUTHORITY_STATE")
        for item in self.supporting_record_hashes:
            _hash(item, "supporting_record_hash")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClaimAuthorityBindingV1":
        _keys(value, ("authority_state", "historical_label", "supporting_record_hashes", "scope", "limitations", "effective_time", "claim_ceiling"))
        return cls(value["authority_state"], value["historical_label"], tuple(value["supporting_record_hashes"]), value["scope"], tuple(value["limitations"]), value["effective_time"], value["claim_ceiling"])

    def to_dict(self) -> dict[str, Any]:
        return {"authority_state": self.authority_state, "historical_label": self.historical_label, "supporting_record_hashes": list(self.supporting_record_hashes), "scope": self.scope, "limitations": list(self.limitations), "effective_time": self.effective_time, "claim_ceiling": self.claim_ceiling}


@dataclass(frozen=True)
class ScientificAuthorityBindingV1:
    profile_hash: str
    claim_bindings: Mapping[str, ClaimAuthorityBindingV1]
    calculator_profile_review_status: str = "SCIENTIFIC_REQUALIFICATION_NOT_EARNED"

    def __post_init__(self) -> None:
        _hash(self.profile_hash, "profile_hash")
        require(self.calculator_profile_review_status in {"NOT_REVIEWED", "SCIENTIFIC_REQUALIFICATION_NOT_EARNED", "REQUALIFIED", "WITHHELD"}, "PROFILE_REVIEW_STATUS")

    @property
    def binding_hash(self) -> str:
        return digest(self.to_dict(), "ScientificAuthorityBindingV1")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ScientificAuthorityBindingV1":
        _keys(value, ("schema_id", "profile_hash", "claim_bindings", "calculator_profile_review_status"))
        require(value["schema_id"] == "ScientificAuthorityBindingV1", "SCHEMA_ID")
        return cls(value["profile_hash"], {key: ClaimAuthorityBindingV1.from_dict(row) for key, row in value["claim_bindings"].items()}, value["calculator_profile_review_status"])

    def to_dict(self) -> dict[str, Any]:
        return {"schema_id": "ScientificAuthorityBindingV1", "profile_hash": self.profile_hash, "claim_bindings": {key: row.to_dict() for key, row in self.claim_bindings.items()}, "calculator_profile_review_status": self.calculator_profile_review_status}


@dataclass(frozen=True)
class AuthorityAttachmentV1:
    verification_receipt_hash: str
    authority_binding_hash: str

    def __post_init__(self) -> None:
        _hash(self.verification_receipt_hash, "verification_receipt_hash")
        _hash(self.authority_binding_hash, "authority_binding_hash")

    @property
    def attachment_hash(self) -> str:
        return digest(self.to_dict(), "AuthorityAttachmentV1")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AuthorityAttachmentV1":
        _keys(value, ("schema_id", "verification_receipt_hash", "authority_binding_hash"))
        require(value["schema_id"] == "AuthorityAttachmentV1", "SCHEMA_ID")
        return cls(value["verification_receipt_hash"], value["authority_binding_hash"])

    def to_dict(self) -> dict[str, str]:
        return {"schema_id": "AuthorityAttachmentV1", "verification_receipt_hash": self.verification_receipt_hash, "authority_binding_hash": self.authority_binding_hash}
