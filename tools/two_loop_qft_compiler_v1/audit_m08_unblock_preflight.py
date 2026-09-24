"""Audit non-authoritative M08 implementation progress and authority ceiling."""

from hashlib import sha256
import json
from pathlib import Path

from sympy import sympify


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


def main():
    group = verified("uvp_m08_group_contraction_preflight.json")
    ghost = verified("uvp_m08_ghost_2point_preflight.json")
    vector = verified("uvp_m08_vector_2point_lorentz_preflight.json")
    vector_replay = verified(
        "uvp_m08_vector_lorentz_independent_replay.json"
    )
    group_replay = verified(
        "uvp_m08_group_contraction_independent_replay.json"
    )
    assembly = verified("uvp_m08_canonical_two_point_preflight.json")
    assembly_replay = verified(
        "uvp_m08_canonical_two_point_independent_replay.json"
    )
    comparison = verified("uvp_m08_canonical_two_point_comparison.json")
    ledger = json.loads((HERE / "uv_pole_evaluator_results.json").read_text())
    status = json.loads((HERE / "compiler_status.json").read_text())

    assert group["authority"] == "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY"
    assert ghost["authority"] == "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY"
    assert ghost["immutable_inputs"]["group_contraction_artifact_sha256"] == (
        group["artifact_sha256"]
    )
    assert float(group["completeness"][
        "heavy_HHH_plus_2HHL_equals_8_identity_maximum_residual"
    ]) < 1e-12
    assert float(group["completeness"][
        "light_LLL_plus_LHH_equals_8_identity_maximum_residual"
    ]) < 1e-12
    assert sympify(ghost["kinematic_coefficient"]) == sympify(
        "(3-xi)/4"
    )
    assert ghost["primary_minus_replay"] == "0"
    assert len(ghost["heavy_ghost_kinetic_operator"]["spectrum"]) == 5
    assert len(ghost["light_ghost_kinetic_operator"]["spectrum"]) == 3
    assert ghost["covariant_derivative_expansion"][
        "heavy_ghost_light_quantum_vector_bubble_included"
    ] is True
    assert float(group_replay["maximum_primary_replay_residual"]) < 2e-12
    assert vector["kinematic_pole_coefficients"][
        "formal_full_FP_transversality_residual"
    ] == "0"
    assert vector["kinematic_pole_coefficients"][
        "derived_ordinary_YM_delta_Z_Q"
    ] == "13/6 - xi/2"
    for key, value in vector_replay["coefficients"].items():
        assert sympify(value) == sympify(
            vector["kinematic_pole_coefficients"][key]
        )
    assert assembly["pre_BRST_diagnostic"][
        "primary_vs_independent_vector_Lorentz_residual"
    ] == "0"
    assert assembly_replay["primary_canonical_assembly_imported"] is False
    assert comparison["maximum_residual"] == "0"
    assert comparison["primary_sha256"] == assembly["artifact_sha256"]
    assert comparison["replay_sha256"] == assembly_replay["artifact_sha256"]

    summary = ledger["counters"]
    assert summary["executed"] == 34
    assert summary["passed"] == 33
    assert summary["blocked"] == 1
    assert summary["failed"] == 0
    assert ledger["tests"][33]["test_id"] == "UVP_M08"
    assert ledger["tests"][33]["status"] == "BLOCKED"
    assert ledger["tests"][33]["attempt"] == 1
    assert status["layer5a_M08"] == "BLOCKED"
    assert status["next_gate"] == (
        "REASSEMBLE_M08_HEAVY_PARTIAL_GF_BRST_RESIDUES_AND_COMPLETE_"
        "INDEPENDENT_REPLAY"
    )
    assert status["layer5a_M08_two_point_comparison_sha256"] == (
        comparison["artifact_sha256"]
    )
    assert status["layer5a_M08_pre_BRST_heavy_gauge_parameter_blocks"] == 5
    assert status["layer5a_M08_pre_BRST_light_gauge_parameter_blocks"] == 3
    assert ledger["promotion"]["counterterm_compiler"] == "BLOCKED"
    assert status["layer6_tensor_IBP_reduction_authorized"] is False

    print("M08_UNBLOCK_PREFLIGHT_AUDIT_PASS")
    print("GROUP_ARTIFACT_SHA256", group["artifact_sha256"])
    print("GHOST_2POINT_ARTIFACT_SHA256", ghost["artifact_sha256"])
    print("VECTOR_LORENTZ_ARTIFACT_SHA256", vector["artifact_sha256"])
    print("TWO_POINT_COMPARISON_SHA256", comparison["artifact_sha256"])
    print("AUTHORITY_REMAINS_34_OF_39_M08_BLOCKED_ATTEMPT1")


if __name__ == "__main__":
    main()
