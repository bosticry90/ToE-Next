"""Audit the seam between the component basis and physical mass basis."""

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
    reps = rational_representatives()
    copies = sum(len(entries) for entries in reps.values())
    reconstructed_dimension = sum(
        dimension(label) * len(entries) for label, entries in reps.items())
    assert component["dimensions"]["total"] == 328
    assert len(reps) == 35 and copies == 65
    assert reconstructed_dimension == 328

    payload = {
        "outcome": "PHYSICAL_VERTEX_MATERIALIZATION_BLOCKED",
        "component_basis": "PASS_328_REAL",
        "sm_irrep_classes": 35,
        "highest_weight_multiplicity_representatives": 65,
        "dimension_reconstructed_from_irreps": reconstructed_dimension,
        "existing_authority": (
            "highest_weight copies and multiplicity Hessian blocks; sufficient "
            "for spectrum/rank, not complete interaction vertices"
        ),
        "missing_first_object": (
            "complete all-weight parent-to-irrep map and 328-component "
            "parent-to-physical mass transformation"
        ),
        "acceptance_tests": [
            "exact kinetic unitarity",
            "full Hessian reconstruction from multiplicity blocks",
            "290 heavy plus 38 zero/light disposition",
            "conjugate-irrep consistency",
            "recovery of all passed block eigenvalues",
        ],
        "background_field_gauge_authorized": False,
        "finite_C1_GS": None,
    }
    (HERE / "compiler_status.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("EXISTING_HIGHEST_WEIGHT_REPS", copies, "IRREP_CLASSES", len(reps))
    print("DIMENSION_RECONSTRUCTION_PASS", reconstructed_dimension)


if __name__ == "__main__":
    main()
