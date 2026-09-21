"""Fail-fast readiness audit for the requested finite two-loop threshold.

This audit distinguishes exact model inputs from the QFT machinery needed to
turn them into a renormalized two-loop background-field matching constant.
It must never infer a finite C1 coefficient from RG logarithms or from the
presence of the scalar-potential derivative oracle.
"""

from hashlib import sha256
import json
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

PARENT = ROOT / "calculations/canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md"
POINT = ROOT / "calculations/canonical_so10_positive_higgs/POINT.json"
DIRECT = ROOT / "calculations/canonical_so10_direct_gauge_matching/direct_matching.json"
BOUNDARY = ROOT / "calculations/canonical_so10_direct_two_loop_heavy_threshold/two_loop_boundary.json"
VERTEX = HERE / "scalar_vertex_oracle.json"
COMPARISON = HERE / "comparison_gate.json"

EXPECTED = {
    PARENT: "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed",
    POINT: "476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED.items():
        assert digest(path) == expected
    direct = json.loads(DIRECT.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    vertex = json.loads(VERTEX.read_text(encoding="utf-8"))
    comparison = json.loads(COMPARISON.read_text(encoding="utf-8"))

    assert direct["kernel"]["scalar_positive_real_directions"] == 290
    assert direct["kernel"]["massive_vectors"] == 33
    assert direct["kernel"]["vector_goldstone_ghost_sets"] == 33
    assert boundary["part_A_gauge_scalar"]["parent_b_one_loop"] == "-34/3"
    assert (boundary["part_A_gauge_scalar"]
            ["parent_B_two_loop_yukawa_independent"] == "10405/6")
    assert vertex["outcome"] == "SCALAR_VERTEX_ORACLE_PASS"
    assert comparison["status"] == "PREREGISTERED_BEFORE_C1_GS"
    assert comparison["actual_centered_C1_GS"] is None

    executable_probe = {
        name: shutil.which(name)
        for name in ("qgraf", "form", "tform", "tsil", "gcc", "clang", "cl")
    }
    layers = {
        "frozen_parent_action_and_point": "PASS",
        "physical_heavy_state_ledger": "PASS_290_SCALARS_33_VECTORS",
        "rg_logarithmic_two_loop_kernel": "PASS",
        "scalar_potential_directional_vertex_oracle": "PASS",
        "full_328_real_component_vertex_basis": "NOT_MATERIALIZED",
        "background_quantum_gauge_fixing_rules": "NOT_COMPILED",
        "vector_goldstone_ghost_interaction_vertices": "NOT_COMPILED",
        "two_loop_diagram_generation_and_symmetry_factors": "NOT_IMPLEMENTED",
        "one_loop_field_mass_gauge_vev_tadpole_counterterms": "NOT_IMPLEMENTED",
        "two_loop_tensor_IBP_reduction": "NOT_IMPLEMENTED",
        "validated_massive_vacuum_master_evaluator": "NOT_AVAILABLE",
        "gauge_parameter_cancellation": "NOT_TESTABLE",
        "finite_degenerate_mass_limits": "NOT_TESTABLE",
        "finite_C1_GS": "NOT_CALCULATED",
        "gauge_refit_with_C1_GS": "NOT_AUTHORIZED",
    }
    missing_required = [key for key, value in layers.items()
                        if value.startswith("NOT_")]
    assert missing_required

    payload = {
        "outcome": "DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED",
        "overall_gauge_disposition": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
        "preserved": [
            "DIRECT_ONE_LOOP_KERNEL_PASS",
            "DIRECT_SM_TWO_LOOP_RUNNING_PASS",
            "EXACT_TWO_LOOP_RG_LOG_KERNEL",
            "YUKAWA_CONVENTION_V1",
            "BFB_UNRESOLVED",
        ],
        "newly_earned": [
            "SCALAR_VERTEX_ORACLE_PASS",
            "C1_GS_COMPARISON_PREREGISTERED",
            "TWO_LOOP_COMPILER_LAYER_AUDIT_COMPLETE",
        ],
        "layers": layers,
        "missing_required_layers": missing_required,
        "executable_probe": executable_probe,
        "finite_C1_GS": None,
        "centered_target_C1": comparison["target_centered_C1"],
        "comparison_performed": False,
        "gauge_refit_performed": False,
        "interpretation": (
            "The canonical scalar-potential vertices are now available exactly "
            "on demand, but no renormalized two-loop background-field amplitude "
            "exists. RG logarithms do not determine its finite constant."
        ),
    }
    (HERE / "compiler_readiness.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("NEWLY_EARNED", ",".join(payload["newly_earned"]))
    print("MISSING_REQUIRED_LAYERS", len(missing_required))
    print("FINITE_C1_GS", payload["finite_C1_GS"])


if __name__ == "__main__":
    main()
