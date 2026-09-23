"""Independent SO(10) structure-contraction replay for M08 preflight.

The replay constructs the raw antisymmetric-generator structure constants
from Kronecker-index commutator identities and rotates them into the immutable
physical vector basis.  It does not call PartialBFMAction.structure or the
primary structure-constant routine.
"""

from hashlib import sha256
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from physical_vertex_api import PhysicalVertexAPI


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def raw_structure_constants():
    pairs = tuple(combinations(range(10), 2))
    lookup = {pair: index for index, pair in enumerate(pairs)}
    result = np.zeros((45, 45, 45))

    def add(output, left, right, coefficient):
        if left == right:
            return
        pair = (left, right) if left < right else (right, left)
        sign = 1 if left < right else -1
        output[lookup[pair]] += coefficient * sign / np.sqrt(2)

    for first, (a, b) in enumerate(pairs):
        for second, (c, d) in enumerate(pairs):
            output = np.zeros(45)
            if b == c:
                add(output, a, d, 1)
            if a == c:
                add(output, b, d, -1)
            if b == d:
                add(output, a, c, -1)
            if a == d:
                add(output, b, c, 1)
            result[first, second, :] = output
    return result


def serial(matrix):
    return [[format(float(value), ".15g") for value in row]
            for row in matrix]


def spectrum(matrix, tolerance=1e-8):
    values = np.linalg.eigvalsh((matrix + matrix.T) / 2)
    groups = []
    for value in values:
        if not groups or abs(value - groups[-1][0]) > tolerance:
            groups.append([float(value), 1])
        else:
            groups[-1][1] += 1
    return [{
        "eigenvalue": str(Fraction(value).limit_denominator(120)),
        "multiplicity": multiplicity,
    } for value, multiplicity in groups]


def main():
    primary = json.loads(
        (HERE / "uvp_m08_group_contraction_preflight.json").read_text()
    )
    api = PhysicalVertexAPI()
    rotation = api.vector_rotation
    raw = raw_structure_constants()
    physical = np.einsum(
        "ia,jb,kc,ijk->abc", rotation, rotation, rotation, raw,
        optimize=True,
    )
    domains = {
        "full_adjoint": (range(45), range(45), range(45)),
        "heavy_heavy_heavy": (range(12, 45), range(12, 45), range(12, 45)),
        "heavy_heavy_light": (range(12, 45), range(12, 45), range(12)),
        "light_light_light": (range(12), range(12), range(12)),
        "light_heavy_heavy": (range(12), range(12, 45), range(12, 45)),
    }
    rows = {}
    maximum_residual = 0.0
    for name, (external, left, right) in domains.items():
        external, left, right = map(list, (external, left, right))
        block = physical[np.ix_(external, left, right)]
        matrix = np.einsum("abc,dbc->ad", block, block)
        primary_matrix = np.asarray(
            [[float(value) for value in row]
             for row in primary["contractions"][name]["matrix"]]
        )
        residual = float(np.max(abs(matrix - primary_matrix)))
        maximum_residual = max(maximum_residual, residual)
        frozen = serial(matrix)
        rows[name] = {
            "matrix_sha256": digest(frozen),
            "matrix": frozen,
            "spectrum": spectrum(matrix),
            "primary_matrix_sha256": primary["contractions"][name]
                ["matrix_sha256"],
            "maximum_primary_replay_residual": format(residual, ".12g"),
        }
    assert maximum_residual < 2e-12
    payload = {
        "schema_version": 1,
        "outcome": "M08_GROUP_CONTRACTION_INDEPENDENT_REPLAY_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": "raw_SO10_Kronecker_commutator_then_physical_rotation",
        "primary_structure_routine_imported": False,
        "immutable_physical_basis_sha256": (
            "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e"
        ),
        "primary_group_artifact_sha256": primary["artifact_sha256"],
        "comparisons": rows,
        "maximum_primary_replay_residual": format(maximum_residual, ".12g"),
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_group_contraction_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("MAXIMUM_PRIMARY_REPLAY_RESIDUAL",
          payload["maximum_primary_replay_residual"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
