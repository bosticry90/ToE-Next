"""Audit promotion layer 2: the complete factorized physical basis."""

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL = ROOT / "calculations/canonical_so10_full_hessian"
sys.path.insert(0, str(FULL))

from evaluate_sm_hessian_blocks import rational_representatives
from decompose_sm_tangent import dimension


def main():
    component = json.loads((HERE / "real_field_basis.json").read_text(
        encoding="utf-8"))
    weights = json.loads((HERE / "sm_weight_basis.json").read_text(
        encoding="utf-8"))
    physical = json.loads((HERE / "physical_basis.json").read_text(
        encoding="utf-8"))
    reps = rational_representatives()
    copies = sum(len(entries) for entries in reps.values())
    reconstructed_dimension = sum(
        dimension(label) * len(entries) for label, entries in reps.items())
    assert component["dimensions"]["total"] == 328
    assert len(reps) == 35 and copies == 65
    assert reconstructed_dimension == 328
    assert weights["outcome"] == "CANONICAL_FULL_SM_WEIGHT_BASIS_PASS"
    assert weights["rank"] == 328 and weights["real_columns"] == 328
    assert physical["outcome"] == "CANONICAL_328_PHYSICAL_BASIS_PASS"
    assert physical["parent_component_basis_sha256"] == component["full_basis_sha256"]
    assert physical["sm_weight_map_sha256"] == weights["real_weight_map_sha256"]
    assert physical["disposition"] == {
        "positive_heavy_real": 290,
        "gauge_goldstone_real": 33,
        "pq_real": 1,
        "light_higgs_real": 4,
        "total": 328,
    }
    certificates = physical["certificates"]
    assert certificates["rank_tolerance_1e_9"] == 328
    assert certificates["max_kinetic_orthogonality_residual"] < 4e-9
    assert certificates["max_hessian_roundtrip_residual"] < 2e-8
    assert certificates["max_symmetry_vector_outside_preliminary_nullspace"] < 3e-9
    expected_indices = [377/30, 77/6, 79/6]
    assert max(abs(a-b) for a, b in zip(
        physical["heavy_scalar_one_loop_beta_indices_order_1_2_3"],
        expected_indices)) < 2e-8

    payload = {
        "outcome": "CANONICAL_328_PHYSICAL_BASIS_PASS",
        "component_basis": "PASS_328_REAL",
        "full_sm_weight_basis": "PASS_328_REAL_EXACT_ORTHONORMAL",
        "physical_basis": "PASS_290_PLUS_33_PLUS_1_PLUS_4",
        "weight_map_sha256": weights["real_weight_map_sha256"],
        "factorized_physical_basis_sha256": (
            physical["factorized_physical_basis_sha256"]),
        "sm_irrep_classes": 35,
        "highest_weight_multiplicity_representatives": 65,
        "dimension_reconstructed_from_irreps": reconstructed_dimension,
        "earned_authority": (
            "complete factorized parent-to-physical scalar transformation, "
            "explicit symmetry/light zero disposition, and transformed "
            "unbroken-generator index replay"
        ),
        "numerical_certificates": certificates,
        "next_gate": "BACKGROUND_FIELD_GAUGE_GHOST_AND_VERTEX_LAYER",
        "background_field_gauge_started": False,
        "bulk_physical_vertex_generation_started": False,
        "finite_C1_GS": None,
    }
    (HERE / "compiler_status.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("EXISTING_HIGHEST_WEIGHT_REPS", copies, "IRREP_CLASSES", len(reps))
    print("DIMENSION_RECONSTRUCTION_PASS", reconstructed_dimension)
    print("FACTORIZED_PHYSICAL_BASIS_SHA256",
          payload["factorized_physical_basis_sha256"])


if __name__ == "__main__":
    main()
