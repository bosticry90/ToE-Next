"""Small public wrapper around the promoted exact DAG verifier."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import strict_json_file
from .contracts import CandidatePacketV1, PhysicsProfileV1
from .dag import ExactDagVerifierV1
from .sources import SourceResolverV1


def verify_candidate(
    profile: PhysicsProfileV1,
    candidate: CandidatePacketV1,
    source_root: Path,
) -> dict[str, Any]:
    """Recompute a finite exact DAG and return a bounded verification receipt."""

    root = source_root.resolve(strict=True)
    resolver = SourceResolverV1(root, profile.source_declarations)
    result = ExactDagVerifierV1(profile, resolver).verify(candidate)
    return {
        "schema_id": "VPCExactCoreReceiptV1",
        "status": "PASS",
        "authority_ceiling": "EXACT_DAG_RECOMPUTATION_ONLY",
        "profile_id": profile.profile_id,
        "profile_hash": profile.contract_hash,
        "candidate_hash": candidate.candidate_hash,
        "graph_hash": result.graph_hash,
        "outputs": result.output_data(),
        "node_receipts": [row.to_dict() for row in result.receipts],
        "output_ancestry": {key: list(value) for key, value in result.ancestry.items()},
    }


def verify_paths(profile_path: Path, candidate_path: Path, source_root: Path) -> dict[str, Any]:
    """Load strict JSON inputs, then invoke :func:`verify_candidate`."""

    profile = PhysicsProfileV1.from_dict(strict_json_file(profile_path))
    candidate = CandidatePacketV1.from_dict(strict_json_file(candidate_path))
    return verify_candidate(profile, candidate, source_root)
