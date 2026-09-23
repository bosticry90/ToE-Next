"""Freeze comparison of primary and independent M08 two-point operators."""

from hashlib import sha256
import json
from pathlib import Path

from sympy import simplify, sympify


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work), name
    return payload


def compare_rows(primary, replay, key, fields):
    left = {row[key]: row for row in primary}
    right = {row[key]: row for row in replay}
    assert set(left) == set(right)
    residuals = {}
    for eigenvalue in sorted(left, key=sympify):
        assert left[eigenvalue]["multiplicity"] == right[eigenvalue][
            "multiplicity"
        ]
        residuals[eigenvalue] = {}
        for field in fields:
            residual = simplify(sympify(left[eigenvalue][field])
                                - sympify(right[eigenvalue][field]))
            assert residual == 0
            residuals[eigenvalue][field] = "0"
    return residuals


def main():
    primary = verified("uvp_m08_canonical_two_point_preflight.json")
    replay = verified(
        "uvp_m08_canonical_two_point_independent_replay.json"
    )
    heavy = compare_rows(
        primary["heavy_vector_blocks"], replay["heavy_vector_blocks"],
        "K_HHH_eigenvalue",
        ("loop_A", "loop_B", "delta_Z_quantum_heavy_vector",
         "multiplicative_delta_Z_xi_candidate"),
    )
    light = compare_rows(
        primary["light_vector_blocks"], replay["light_vector_blocks"],
        "K_LLL_eigenvalue",
        ("loop_A", "loop_B", "delta_Z_quantum_light_vector",
         "multiplicative_delta_Z_eta_H_candidate"),
    )
    payload = {
        "schema_version": 1,
        "outcome": "M08_CANONICAL_TWO_POINT_PRIMARY_REPLAY_AGREEMENT",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "primary_sha256": primary["artifact_sha256"],
        "replay_sha256": replay["artifact_sha256"],
        "heavy_block_residuals": heavy,
        "light_block_residuals": light,
        "maximum_residual": "0",
        "remaining_before_UVP_M08_retry": [
            "complete BRST heavy/light ghost-vector three-point poles",
            "aggregate BRST adjudication of the gauge-fixing parameter basis",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_canonical_two_point_comparison.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("MAXIMUM_RESIDUAL", payload["maximum_residual"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
