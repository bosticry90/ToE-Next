"""Primary UVP_M03 attempt 2 from exhaustive parent-basis contractions."""

from hashlib import sha256
import json
from pathlib import Path

from m03_parent_scalar_kernel import compute_kernel, digest


HERE = Path(__file__).resolve().parent
CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
ATTEMPT1 = "a429ce0df860933879bb8810c42a599d0cc0f87a694be392cb591c10f18086c4"


def main():
    specification = HERE / "M03_KERNEL_IMPLEMENTATION_SPEC.md"
    kernel = compute_kernel()
    payload = {
        "schema_version": 1,
        "test_id": "UVP_M03",
        "attempt": 2,
        "contract_sha256": CONTRACT,
        "execution_plan_sha256": PLAN,
        "attempt1_blocked_evidence_sha256": ATTEMPT1,
        "kernel_spec_sha256": sha256(specification.read_bytes()).hexdigest(),
        "method": "exhaustive_sparse_parent_vertex_contractions_in_328_real_basis",
        "normalization": "coefficients multiply 1/(16*pi^2*epsilon_bar)",
        **kernel,
        "sector_completeness": {
            "scalar": "COMPLETE_328_INTERNAL_REAL_DIRECTIONS",
            "quantum_vector": "COMPLETE_PARENT_COVARIANT_1PI_MASS_POLE",
            "goldstone": "COMPLETE_UNSHIFTED_PARENT_PROJECTION",
            "ghost": "COMPLETE_UNSHIFTED_PARENT_PROJECTION",
            "M02_field_counterterm": "INCLUDED_EXACTLY_ONCE",
        },
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "nonexceptional_or_auxiliary_mass_local_projection",
            "scaleless_gauge_seagull": {"UV": "retained", "IR": "retained",
                                         "sum": "0"},
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m03_primary_attempt2.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M03_PRIMARY_ATTEMPT2_COMPLETE")
    print("INVENTORY_SHA256", payload["inventory_sha256"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])
    for name, value in payload["quadratic_residues"].items():
        print(name, "=", value)


if __name__ == "__main__":
    main()
