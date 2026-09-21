"""Freeze the centered-C1 magnitude/alignment test before C1_GS exists."""

import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "canonical_so10_direct_two_loop_heavy_threshold" / "two_loop_boundary.json"


def main() -> None:
    old = json.loads(SOURCE.read_text())
    target = np.asarray(old["finite_threshold_demand"][
        "C1_equivalent_centered_required"], dtype=float)
    assert abs(target.sum()) < 1e-10
    norm = float(np.linalg.norm(target))
    unit = target / norm
    result = {
        "status": "PREREGISTERED_BEFORE_C1_GS",
        "target_centered_C1": target.tolist(),
        "target_norm": norm,
        "target_unit_vector": unit.tolist(),
        "actual_centered_C1_GS": None,
        "comparison_when_available": {
            "center": "c=C1_GS-mean(C1_GS)",
            "magnitude_ratio": "rho=norm(c)/norm(target)",
            "alignment": "cos_theta=dot(c,target)/(norm(c)*norm(target))",
            "beneficial_projection": "dot(c,target)/dot(target,target)",
            "mandatory_physical_test": "insert full convention-consistent GS threshold and refit all three channels",
        },
        "interpretation": {
            "positive_alignment": "moves in the required C1-equivalent direction",
            "negative_alignment": "moves against the required direction",
            "zero_norm": "no nonuniversal GS finite threshold",
            "no_pass_fail": "Yukawa-dependent threshold remains undefined",
        },
    }
    (HERE / "comparison_gate.json").write_text(json.dumps(result, indent=2) + "\n")
    print("C1_GS_COMPARISON_PREREGISTERED", norm, unit.tolist())


if __name__ == "__main__":
    main()
