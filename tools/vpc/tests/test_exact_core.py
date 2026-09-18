from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "source"
sys.path.insert(0, str(SOURCE_ROOT))

from vpc import CalculatorError, verify_candidate  # noqa: E402
from vpc.canonical import canonical_bytes  # noqa: E402
from vpc.contracts import (  # noqa: E402
    AlgebraicFieldV1,
    CandidatePacketV1,
    DimensionSystemV1,
    PhysicsProfileV1,
)
from vpc.exact import ExactRuntimeV1  # noqa: E402


def _value_type() -> dict:
    return {
        "mathematical_kind": "EXACT_SCALAR",
        "semantic_type": "RATIONAL_SCALAR",
        "dimension": ["0"],
        "unit_convention": "DIMENSIONLESS",
        "index_spaces": [],
        "representation_tags": ["SMOKE"],
        "domain": {"kind": "EXACT"},
    }


def _fixture(root: Path) -> tuple[PhysicsProfileV1, CandidatePacketV1]:
    runtime = ExactRuntimeV1(AlgebraicFieldV1.rational(), ())
    source_document = {"input": runtime.rational(3).to_dict()}
    source_bytes = canonical_bytes(source_document)
    (root / "source.json").write_bytes(source_bytes)
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    declaration = {
        "path": "source.json",
        "sha256": source_hash,
        "byte_size": len(source_bytes),
        "media_type": "application/json",
    }
    profile = PhysicsProfileV1(
        "TOE_NEXT_VPC_EXACT_SMOKE_v1",
        (),
        AlgebraicFieldV1.rational(),
        DimensionSystemV1(("D",), "INTEGER", ()),
        ("DIMENSIONLESS",),
        ("RATIONAL_SCALAR",),
        {},
        ("SMOKE",),
        (declaration,),
        ("SOURCE_DECODE", "POW_INT", "OUTPUT_BIND"),
        ("OUTPUT.SQUARE",),
        {"OUTPUT.SQUARE": "smoke.square_of_three"},
    )
    reference = {
        "type": "JsonPointerValueRef",
        "artifact_path": "source.json",
        "artifact_sha256": source_hash,
        "pointer": "/input",
    }
    value_type = _value_type()
    three = runtime.rational(3).to_dict()
    nine = runtime.rational(9).to_dict()
    nodes = [
        {
            "node_id": "SOURCE.X",
            "kind": "SOURCE",
            "operation": "SOURCE_DECODE",
            "parents": [],
            "parameters": {"reference": reference},
            "value_type": value_type,
            "claimed_value": three,
        },
        {
            "node_id": "SQUARE",
            "kind": "DERIVED",
            "operation": "POW_INT",
            "parents": ["SOURCE.X"],
            "parameters": {"exponent": 2},
            "value_type": value_type,
            "claimed_value": nine,
        },
        {
            "node_id": "OUTPUT.SQUARE",
            "kind": "OUTPUT",
            "operation": "OUTPUT_BIND",
            "parents": ["SQUARE"],
            "parameters": {},
            "value_type": value_type,
            "claimed_value": nine,
        },
    ]
    candidate = CandidatePacketV1(
        "0" * 64,
        {"kind": "TOE_NEXT_SMOKE_FIXTURE", "trust": "UNTRUSTED_PROPOSAL"},
        {"nodes": nodes, "edges": [["SOURCE.X", "SQUARE"], ["SQUARE", "OUTPUT.SQUARE"]]},
        {"OUTPUT.SQUARE": nine},
        ({"node_id": "SOURCE.X", "reference": reference},),
    )
    return profile, candidate


class ExactCoreTests(unittest.TestCase):
    def test_recomputes_hash_bound_exact_claim(self) -> None:
        with TemporaryDirectory(prefix="toe-next-vpc-") as directory:
            profile, candidate = _fixture(Path(directory))
            receipt = verify_candidate(profile, candidate, Path(directory))
            self.assertEqual(receipt["status"], "PASS")
            self.assertEqual(receipt["authority_ceiling"], "EXACT_DAG_RECOMPUTATION_ONLY")

    def test_rejects_corrupted_claim(self) -> None:
        with TemporaryDirectory(prefix="toe-next-vpc-") as directory:
            root = Path(directory)
            profile, candidate = _fixture(root)
            corrupted = deepcopy(candidate.to_dict())
            runtime = ExactRuntimeV1(AlgebraicFieldV1.rational(), ())
            corrupted["graph"]["nodes"][1]["claimed_value"] = runtime.rational(8).to_dict()
            with self.assertRaises(CalculatorError):
                verify_candidate(profile, CandidatePacketV1.from_dict(corrupted), root)


if __name__ == "__main__":
    unittest.main()
