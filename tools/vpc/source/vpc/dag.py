"""Typed declarative DAG verifier for the trusted exact path."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping

from .canonical import canonical_data, digest
from .contracts import CandidatePacketV1, PhysicsProfileV1, ResourceLimitsV1
from .dimensions import DimensionQuotientV1, DimensionVectorV1
from .errors import CalculatorError, require
from .exact import ExactAtomV1, ExactBooleanV1, ExactRuntimeV1, ExactTensorV1, ExactValueV1, RationalFunctionV1
from .sources import SourceResolverV1


TRUSTED_DOMAIN_NEUTRAL_OPERATIONS = {
    "SOURCE_DECODE", "LITERAL", "OUTPUT_BIND", "ADD", "SUB", "MUL", "DIV",
    "NEG", "POW_INT", "MAKE_TENSOR", "INDEX", "MATMUL",
    "EQUAL", "ALL", "SELECT", "CLASSIFY_ZERO",
}


@dataclass(frozen=True)
class ValueTypeV1:
    mathematical_kind: str
    semantic_type: str
    dimension: DimensionVectorV1
    unit_convention: str
    index_spaces: tuple[str, ...]
    representation_tags: tuple[str, ...]
    domain: Mapping[str, Any]
    shape: tuple[int, ...] | None = None

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], profile: PhysicsProfileV1) -> "ValueTypeV1":
        legacy = {"mathematical_kind", "semantic_type", "dimension", "unit_convention", "index_spaces", "representation_tags", "domain"}
        require(set(value) in {frozenset(legacy), frozenset({*legacy, "shape"})}, "VALUE_TYPE_FIELDS")
        require(value["mathematical_kind"] in {"EXACT_SCALAR", "EXACT_TENSOR", "EXACT_BOOLEAN", "EXACT_ATOM", "EXACT_DOCUMENT", "INTERVAL", "NUMERICAL_SCALAR", "NUMERICAL_VECTOR"}, "MATHEMATICAL_KIND")
        require(value["semantic_type"] in profile.semantic_types, "SEMANTIC_TYPE")
        require(value["unit_convention"] in profile.unit_conventions, "UNIT_CONVENTION")
        spaces = tuple(value["index_spaces"])
        require(all(space in profile.index_spaces for space in spaces), "INDEX_SPACE")
        tags = tuple(value["representation_tags"])
        require(all(tag in profile.representation_tags for tag in tags), "REPRESENTATION_TAG")
        raw_shape = value.get("shape")
        require(raw_shape is None or (isinstance(raw_shape, list) and all(type(size) is int and size >= 0 for size in raw_shape)), "VALUE_TYPE_SHAPE")
        shape = None if raw_shape is None else tuple(raw_shape)
        return cls(value["mathematical_kind"], value["semantic_type"], DimensionVectorV1.decode(value["dimension"], profile.dimensions), value["unit_convention"], spaces, tags, dict(value["domain"]), shape)

    def to_dict(self) -> dict[str, Any]:
        result = {"mathematical_kind": self.mathematical_kind, "semantic_type": self.semantic_type, "dimension": self.dimension.to_list(), "unit_convention": self.unit_convention, "index_spaces": list(self.index_spaces), "representation_tags": list(self.representation_tags), "domain": dict(self.domain)}
        if self.shape is not None:
            result["shape"] = list(self.shape)
        return result


@dataclass(frozen=True)
class NodeV1:
    node_id: str
    kind: str
    operation: str
    parents: tuple[str, ...]
    parameters: Mapping[str, Any]
    value_type: ValueTypeV1
    claimed_value: Mapping[str, Any]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], profile: PhysicsProfileV1) -> "NodeV1":
        require(set(value) == {"node_id", "kind", "operation", "parents", "parameters", "value_type", "claimed_value"}, "NODE_FIELDS", str(value.get("node_id", "")))
        identity = value["node_id"]
        require(isinstance(identity, str) and identity, "NODE_ID")
        require(value["kind"] in {"SOURCE", "LITERAL", "DERIVED", "OUTPUT"}, "NODE_KIND", identity)
        require(value["operation"] in profile.permitted_operations, "UNTRUSTED_OR_UNKNOWN_OPERATION", identity)
        parents = tuple(value["parents"])
        require(len(set(parents)) == len(parents) and all(isinstance(parent, str) and parent for parent in parents), "PARENT_LIST", identity)
        return cls(identity, value["kind"], value["operation"], parents, dict(value["parameters"]), ValueTypeV1.from_dict(value["value_type"], profile), dict(value["claimed_value"]))

    def to_dict(self) -> dict[str, Any]:
        return {"node_id": self.node_id, "kind": self.kind, "operation": self.operation, "parents": list(self.parents), "parameters": dict(self.parameters), "value_type": self.value_type.to_dict(), "claimed_value": dict(self.claimed_value)}


@dataclass(frozen=True)
class NodeReceiptV1:
    node_id: str
    kind: str
    operation: str
    parents: tuple[str, ...]
    value_digest: str
    claimed_value_digest: str
    status: str
    source_receipt: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {"node_id": self.node_id, "kind": self.kind, "operation": self.operation, "parents": list(self.parents), "value_digest": self.value_digest, "claimed_value_digest": self.claimed_value_digest, "status": self.status}
        if self.source_receipt is not None:
            result["source_receipt"] = dict(self.source_receipt)
        return result


@dataclass(frozen=True)
class TypeSignatureReceiptV1:
    node_id: str
    expected: Mapping[str, Any]
    observed: Mapping[str, Any]
    applicable_axes: tuple[str, ...]
    actual_value_shape: tuple[int, ...] | None
    status: str = "TRUSTED_SIGNATURE_MATCHED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "expected": dict(self.expected),
            "observed": dict(self.observed),
            "applicable_axes": list(self.applicable_axes),
            "actual_value_shape": None if self.actual_value_shape is None else list(self.actual_value_shape),
            "status": self.status,
        }


@dataclass(frozen=True)
class EvaluationResultV1:
    graph_hash: str
    values: Mapping[str, ExactValueV1]
    outputs: Mapping[str, ExactValueV1]
    receipts: tuple[NodeReceiptV1, ...]
    ancestry: Mapping[str, tuple[str, ...]]
    type_signature_receipts: tuple[TypeSignatureReceiptV1, ...] = ()

    def output_data(self) -> dict[str, Any]:
        return {root: value.to_dict() for root, value in self.outputs.items()}


def _value_data(value: ExactValueV1) -> dict[str, Any]:
    return value.to_dict()


def _same_metadata(left: ValueTypeV1, right: ValueTypeV1) -> bool:
    return left == right


class ExactDagVerifierV1:
    def __init__(self, profile: PhysicsProfileV1, resolver: SourceResolverV1, limits: ResourceLimitsV1 | None = None) -> None:
        self.profile = profile
        self.limits = limits or ResourceLimitsV1()
        self.resolver = resolver
        self.exact = ExactRuntimeV1(profile.algebraic_field, profile.symbols, self.limits)
        self.dimensions = DimensionQuotientV1(profile.dimensions)

    def _validate_graph(self, packet: CandidatePacketV1) -> tuple[dict[str, NodeV1], tuple[str, ...], str]:
        graph = packet.graph
        require(set(graph) == {"nodes", "edges"}, "GRAPH_FIELDS")
        raw_nodes = graph["nodes"]
        require(isinstance(raw_nodes, list) and 0 < len(raw_nodes) <= self.limits.dag_nodes, "DAG_NODE_LIMIT")
        nodes: dict[str, NodeV1] = {}
        for raw in raw_nodes:
            node = NodeV1.from_dict(raw, self.profile)
            require(node.node_id not in nodes, "DUPLICATE_NODE", node.node_id)
            nodes[node.node_id] = node
        expected_edges = {(parent, node.node_id) for node in nodes.values() for parent in node.parents}
        raw_edges = graph["edges"]
        require(isinstance(raw_edges, list) and all(isinstance(edge, list) and len(edge) == 2 and all(isinstance(item, str) for item in edge) for edge in raw_edges), "EDGE_SCHEMA")
        actual_edges = {tuple(edge) for edge in raw_edges}
        require(len(actual_edges) == len(raw_edges), "DUPLICATE_EDGE")
        require(actual_edges == expected_edges, "PARENT_EDGE_DISAGREEMENT")
        require(all(parent in nodes and child in nodes for parent, child in actual_edges), "MISSING_PARENT")
        roots = {identity for identity, node in nodes.items() if node.kind == "OUTPUT"}
        require(roots == set(self.profile.output_roots), "OUTPUT_ROOT_SET")
        require(set(packet.claimed_outputs) == roots, "CLAIMED_OUTPUT_SET")
        source_bindings = {row.get("node_id"): row.get("reference") for row in packet.source_bindings}
        require(len(source_bindings) == len(packet.source_bindings), "DUPLICATE_SOURCE_BINDING")
        expected_sources = {identity for identity, node in nodes.items() if node.kind == "SOURCE"}
        require(set(source_bindings) == expected_sources, "SOURCE_BINDING_SET")
        for identity in expected_sources:
            require(nodes[identity].parameters == {"reference": source_bindings[identity]}, "SOURCE_BINDING_MISMATCH", identity)
        indegree = {identity: len(node.parents) for identity, node in nodes.items()}
        children = {identity: [] for identity in nodes}
        for parent, child in actual_edges:
            children[parent].append(child)
        ready = deque(sorted(identity for identity, degree in indegree.items() if degree == 0))
        order: list[str] = []
        while ready:
            identity = ready.popleft()
            order.append(identity)
            for child in sorted(children[identity]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
        require(len(order) == len(nodes), "CYCLIC_DAG")
        graph_hash = digest({"nodes": [nodes[key].to_dict() for key in sorted(nodes)], "edges": [list(edge) for edge in sorted(actual_edges)]}, "CandidateGraphV1")
        return nodes, tuple(order), graph_hash

    def _require_same_additive_type(self, node: NodeV1, parents: list[NodeV1]) -> None:
        require(len(parents) == 2, "ADDITIVE_TYPE_MISMATCH", node.node_id)
        reference = parents[0].value_type
        for candidate in (parents[1].value_type, node.value_type):
            require(
                candidate.mathematical_kind == reference.mathematical_kind
                and candidate.semantic_type == reference.semantic_type
                and candidate.unit_convention == reference.unit_convention
                and candidate.index_spaces == reference.index_spaces
                and candidate.representation_tags == reference.representation_tags
                and candidate.domain == reference.domain
                and self.dimensions.equivalent(candidate.dimension, reference.dimension),
                "ADDITIVE_TYPE_MISMATCH", node.node_id,
            )

    def _require_exact_domain(self, node: NodeV1, parents: list[NodeV1]) -> None:
        require(node.value_type.domain == {"kind": "EXACT"} and all(parent.value_type.domain == {"kind": "EXACT"} for parent in parents), "EXACT_DOMAIN_REQUIRED", node.node_id)

    def _require_common_convention(self, node: NodeV1, parents: list[NodeV1]) -> None:
        require(all(parent.value_type.unit_convention == node.value_type.unit_convention for parent in parents), "UNIT_CONVENTION_MISMATCH", node.node_id)

    def _check_signature(self, node: NodeV1, parent_nodes: list[NodeV1], values: list[ExactValueV1]) -> None:
        operation = node.operation
        self._require_exact_domain(node, parent_nodes)
        self._require_common_convention(node, parent_nodes)
        if operation == "SOURCE_DECODE":
            require(node.kind == "SOURCE" and not parent_nodes and set(node.parameters) == {"reference"}, "SOURCE_SIGNATURE", node.node_id)
        elif operation == "LITERAL":
            require(node.kind == "LITERAL" and not parent_nodes and not node.parameters, "LITERAL_SIGNATURE", node.node_id)
        elif operation == "OUTPUT_BIND":
            require(node.kind == "OUTPUT" and len(parent_nodes) == 1 and not node.parameters and _same_metadata(node.value_type, parent_nodes[0].value_type), "OUTPUT_BIND_SIGNATURE", node.node_id)
        elif operation in {"ADD", "SUB"}:
            require(not node.parameters, "OPERATION_PARAMETERS", node.node_id)
            self._require_same_additive_type(node, parent_nodes)
        elif operation == "NEG":
            require(len(parent_nodes) == 1 and not node.parameters and _same_metadata(node.value_type, parent_nodes[0].value_type), "NEG_SIGNATURE", node.node_id)
        elif operation in {"MUL", "DIV"}:
            require(len(parent_nodes) == 2 and not node.parameters, "MULTIPLICATIVE_SIGNATURE", node.node_id)
            expected = parent_nodes[0].value_type.dimension + (parent_nodes[1].value_type.dimension if operation == "MUL" else parent_nodes[1].value_type.dimension.scale(-1))
            self.dimensions.require_equivalent(node.value_type.dimension, expected, node.node_id)
            left, right, result = parent_nodes[0].value_type, parent_nodes[1].value_type, node.value_type
            if operation == "DIV":
                require(left.mathematical_kind == right.mathematical_kind == result.mathematical_kind == "EXACT_SCALAR", "DIV_SCALAR_ONLY", node.node_id)
                require(result.semantic_type == left.semantic_type and result.index_spaces == left.index_spaces and result.representation_tags == left.representation_tags, "MULTIPLICATIVE_TYPE_MISMATCH", node.node_id)
            elif left.mathematical_kind == right.mathematical_kind == "EXACT_SCALAR":
                require(result.mathematical_kind == "EXACT_SCALAR" and result.semantic_type in {left.semantic_type, right.semantic_type} and not result.index_spaces, "MULTIPLICATIVE_TYPE_MISMATCH", node.node_id)
            elif "EXACT_SCALAR" in {left.mathematical_kind, right.mathematical_kind}:
                tensor = right if left.mathematical_kind == "EXACT_SCALAR" else left
                require(result.mathematical_kind == "EXACT_TENSOR" and result.semantic_type == tensor.semantic_type and result.index_spaces == tensor.index_spaces and result.representation_tags == tensor.representation_tags, "MULTIPLICATIVE_TYPE_MISMATCH", node.node_id)
            else:
                require(left.mathematical_kind == right.mathematical_kind == result.mathematical_kind == "EXACT_TENSOR" and left.semantic_type == right.semantic_type == result.semantic_type and left.index_spaces == right.index_spaces == result.index_spaces and left.representation_tags == right.representation_tags == result.representation_tags, "MULTIPLICATIVE_TYPE_MISMATCH", node.node_id)
        elif operation == "POW_INT":
            require(len(parent_nodes) == 1 and set(node.parameters) == {"exponent"} and type(node.parameters["exponent"]) is int, "POWER_SIGNATURE", node.node_id)
            self.dimensions.require_equivalent(node.value_type.dimension, parent_nodes[0].value_type.dimension.scale(node.parameters["exponent"]), node.node_id)
            require(node.value_type.mathematical_kind == parent_nodes[0].value_type.mathematical_kind == "EXACT_SCALAR" and node.value_type.semantic_type == parent_nodes[0].value_type.semantic_type and node.value_type.index_spaces == parent_nodes[0].value_type.index_spaces and node.value_type.representation_tags == parent_nodes[0].value_type.representation_tags, "POWER_TYPE_MISMATCH", node.node_id)
        elif operation == "MAKE_TENSOR":
            shape = tuple(node.parameters.get("shape", ()))
            require(node.value_type.mathematical_kind == "EXACT_TENSOR" and shape and all(type(size) is int and size > 0 for size in shape), "MAKE_TENSOR_SIGNATURE", node.node_id)
            count = 1
            for size in shape: count *= size
            require(count == len(parent_nodes) == len(values) and all(parent.value_type.mathematical_kind == "EXACT_SCALAR" for parent in parent_nodes), "MAKE_TENSOR_ARITY", node.node_id)
            require(all(self.dimensions.equivalent(parent.value_type.dimension, node.value_type.dimension) for parent in parent_nodes), "MAKE_TENSOR_DIMENSION", node.node_id)
            require(len(node.value_type.index_spaces) == len(shape) and all(self.profile.index_spaces[space] == size for space, size in zip(node.value_type.index_spaces, shape)), "MAKE_TENSOR_INDEX_SPACE", node.node_id)
            require(all(parent.value_type.semantic_type == node.value_type.semantic_type and not parent.value_type.index_spaces and parent.value_type.representation_tags == node.value_type.representation_tags for parent in parent_nodes), "MAKE_TENSOR_TYPE_MISMATCH", node.node_id)
        elif operation == "INDEX":
            require(len(parent_nodes) == 1 and isinstance(values[0], ExactTensorV1) and set(node.parameters) == {"indices"}, "INDEX_SIGNATURE", node.node_id)
            parent = parent_nodes[0].value_type
            require(node.value_type.mathematical_kind == "EXACT_SCALAR" and node.value_type.semantic_type == parent.semantic_type and not node.value_type.index_spaces and node.value_type.representation_tags == parent.representation_tags and self.dimensions.equivalent(node.value_type.dimension, parent.dimension), "INDEX_TYPE_MISMATCH", node.node_id)
            require(len(parent.index_spaces) == len(values[0].shape), "INDEX_SPACE_ARITY", node.node_id)
        elif operation == "MATMUL":
            require(len(parent_nodes) == 2 and all(isinstance(value, ExactTensorV1) for value in values) and not node.parameters, "MATMUL_SIGNATURE", node.node_id)
            self.dimensions.require_equivalent(node.value_type.dimension, parent_nodes[0].value_type.dimension + parent_nodes[1].value_type.dimension, node.node_id)
            left, right = parent_nodes[0].value_type, parent_nodes[1].value_type
            require(node.value_type.mathematical_kind == "EXACT_TENSOR" and len(left.index_spaces) == len(right.index_spaces) == len(node.value_type.index_spaces) == 2 and left.index_spaces[1] == right.index_spaces[0] and node.value_type.index_spaces == (left.index_spaces[0], right.index_spaces[1]) and node.value_type.semantic_type in {left.semantic_type, right.semantic_type}, "MATMUL_TYPE_MISMATCH", node.node_id)
        elif operation == "EQUAL":
            require(len(parent_nodes) == 2 and not node.parameters and node.value_type.mathematical_kind == "EXACT_BOOLEAN", "EQUAL_SIGNATURE", node.node_id)
            require(_same_metadata(parent_nodes[0].value_type, parent_nodes[1].value_type) and not node.value_type.index_spaces and self.dimensions.equivalent(node.value_type.dimension, DimensionVectorV1(tuple(Fraction(0) for _ in self.profile.dimensions.basis))), "EQUAL_TYPE_MISMATCH", node.node_id)
        elif operation == "ALL":
            require(parent_nodes and not node.parameters and node.value_type.mathematical_kind == "EXACT_BOOLEAN" and all(parent.value_type.mathematical_kind == "EXACT_BOOLEAN" for parent in parent_nodes), "ALL_SIGNATURE", node.node_id)
        elif operation == "SELECT":
            require(len(parent_nodes) == 3 and not node.parameters and parent_nodes[0].value_type.mathematical_kind == "EXACT_BOOLEAN" and _same_metadata(parent_nodes[1].value_type, parent_nodes[2].value_type) and _same_metadata(node.value_type, parent_nodes[1].value_type), "SELECT_SIGNATURE", node.node_id)
        elif operation == "CLASSIFY_ZERO":
            require(len(parent_nodes) == 1 and not node.parameters and parent_nodes[0].value_type.mathematical_kind in {"EXACT_SCALAR", "EXACT_TENSOR"} and node.value_type.mathematical_kind == "EXACT_ATOM", "CLASSIFY_ZERO_SIGNATURE", node.node_id)
        else:
            raise CalculatorError("UNTRUSTED_OR_UNKNOWN_OPERATION", node.node_id)

    def _evaluate(self, node: NodeV1, parents: list[ExactValueV1]) -> tuple[ExactValueV1, Mapping[str, Any] | None]:
        operation = node.operation
        if operation == "SOURCE_DECODE":
            resolved = self.resolver.resolve(node.parameters["reference"])
            require(isinstance(resolved.value, dict), "SOURCE_EXACT_VALUE_OBJECT", node.node_id)
            return self.exact.decode(resolved.value), resolved.receipt()
        if operation == "LITERAL":
            return self.exact.decode(node.claimed_value), None
        if operation == "OUTPUT_BIND":
            return parents[0], None
        if operation in {"ADD", "SUB", "MUL"}:
            return self.exact.elementwise(operation, parents[0], parents[1]), None
        if operation == "DIV":
            require(all(isinstance(value, RationalFunctionV1) for value in parents), "DIV_SCALAR_ONLY", node.node_id)
            return self.exact.divide(parents[0], parents[1]), None
        if operation == "NEG":
            value = parents[0]
            if isinstance(value, RationalFunctionV1): return self.exact.negate(value), None
            return ExactTensorV1(value.shape, tuple(self.exact.negate(item) for item in value.entries)), None
        if operation == "POW_INT":
            require(isinstance(parents[0], RationalFunctionV1), "POWER_SCALAR_ONLY", node.node_id)
            return self.exact.power(parents[0], node.parameters["exponent"]), None
        if operation == "MAKE_TENSOR":
            require(all(isinstance(value, RationalFunctionV1) for value in parents), "MAKE_TENSOR_SCALARS", node.node_id)
            return self.exact.tensor(node.parameters["shape"], parents), None
        if operation == "INDEX":
            tensor = parents[0]
            indices = tuple(node.parameters["indices"])
            require(len(indices) == len(tensor.shape) and all(type(index) is int and 0 <= index < size for index, size in zip(indices, tensor.shape)), "TENSOR_INDEX", node.node_id)
            flat = 0
            for index, size in zip(indices, tensor.shape): flat = flat * size + index
            return tensor.entries[flat], None
        if operation == "MATMUL":
            return self.exact.matmul(parents[0], parents[1]), None
        if operation == "EQUAL":
            return ExactBooleanV1(_value_data(parents[0]) == _value_data(parents[1])), None
        if operation == "ALL":
            require(all(isinstance(value, ExactBooleanV1) for value in parents), "ALL_BOOLEAN_ONLY", node.node_id)
            return ExactBooleanV1(all(value.value for value in parents)), None
        if operation == "SELECT":
            require(isinstance(parents[0], ExactBooleanV1), "SELECT_BOOLEAN", node.node_id)
            return parents[1] if parents[0].value else parents[2], None
        if operation == "CLASSIFY_ZERO":
            value = parents[0]
            zero = self.exact.rational(0)
            is_zero = self.exact.equal(value, zero) if isinstance(value, RationalFunctionV1) else all(self.exact.equal(item, zero) for item in value.entries)
            return ExactAtomV1("ENUM", "EVALUATED_ZERO" if is_zero else "EVALUATED_NONZERO"), None
        raise CalculatorError("UNTRUSTED_OR_UNKNOWN_OPERATION", node.node_id)

    def verify(self, packet: CandidatePacketV1) -> EvaluationResultV1:
        nodes, order, graph_hash = self._validate_graph(packet)
        values: dict[str, ExactValueV1] = {}
        receipts: list[NodeReceiptV1] = []
        for identity in order:
            node = nodes[identity]
            parent_nodes = [nodes[parent] for parent in node.parents]
            parent_values = [values[parent] for parent in node.parents]
            self._check_signature(node, parent_nodes, parent_values)
            value, source_receipt = self._evaluate(node, parent_values)
            claimed = self.exact.decode(node.claimed_value)
            require(_value_data(value) == _value_data(claimed), "RECOMPUTATION_MISMATCH", identity)
            values[identity] = value
            value_digest = digest(_value_data(value), "ExactNodeValueV1")
            receipts.append(NodeReceiptV1(identity, node.kind, node.operation, node.parents, value_digest, digest(_value_data(claimed), "ExactNodeValueV1"), "RESOLVED_OR_RECOMPUTED_AND_EQUAL", source_receipt))
        outputs = {root: values[root] for root in self.profile.output_roots}
        for root, value in outputs.items():
            claimed = self.exact.decode(packet.claimed_outputs[root])
            require(_value_data(value) == _value_data(claimed), "EMITTED_ROOT_MISMATCH", root)
        ancestry: dict[str, tuple[str, ...]] = {}
        for root in self.profile.output_roots:
            active: set[str] = set()
            pending = [root]
            while pending:
                identity = pending.pop()
                if identity not in active:
                    active.add(identity)
                    pending.extend(nodes[identity].parents)
            require(any(nodes[identity].kind == "SOURCE" for identity in active), "OUTPUT_WITHOUT_SOURCE", root)
            ancestry[root] = tuple(sorted(active))
        active_all = set().union(*(set(row) for row in ancestry.values()))
        require(active_all == set(nodes), "DECORATIVE_NODE")
        return EvaluationResultV1(graph_hash, values, outputs, tuple(receipts), ancestry)
