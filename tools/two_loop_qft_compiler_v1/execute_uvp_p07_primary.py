"""Primary UVP_P07: unequal-mass bubble by exact partial fractions."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"

def digest(x): return sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    a, b = sp.symbols("m1sq m2sq", positive=True)
    tad_a, tad_b = -a, -b
    bubble = sp.simplify((tad_a - tad_b) / (b - a))
    num_a, num_b = a / (a - b), b / (b - a)
    k2_bubble = sp.simplify(num_a * tad_a + num_b * tad_b)
    assert bubble == 1 and k2_bubble == -(a + b)
    payload = {
        "schema_version": 1, "test_id": "UVP_P07", "attempt": 1,
        "contract_sha256": CONTRACT_HASH, "execution_plan_sha256": PLAN_HASH,
        "method": "exact_unequal_mass_partial_fraction_UV_projection",
        "integral": "Integral_E[1/((k2+m1sq)*(k2+m2sq))]",
        "partial_fraction_identity": "[1/(k2+m1sq)-1/(k2+m2sq)]/(m2sq-m1sq)",
        "normalized_log_residue": str(bubble),
        "mass_swap_residual": str(sp.simplify(bubble - bubble.xreplace({a: b, b: a}))),
        "k2_numerator_normalized_local_mass_residue": str(k2_bubble),
        "k2_mass_swap_residual": str(sp.simplify(k2_bubble - k2_bubble.xreplace({a: b, b: a}))),
        "degenerate_limit": {"log_residue": str(sp.limit(bubble, b, a)), "k2_residue": str(sp.limit(k2_bubble, b, a))},
        "uv_ir": {"uv_pole": True, "ir_pole": False, "scaleless": False, "mass_domain": "m1sq>0,m2sq>0", "rstar_required": False},
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_p07_primary.json").write_text(json.dumps(payload, indent=2)+"\n")
    print("UVP_P07_PRIMARY_COMPLETE"); print("LOG_RESIDUE", bubble); print("LOCAL_MASS_RESIDUE", k2_bubble); print("ARTIFACT_SHA256", payload["artifact_sha256"])

if __name__ == "__main__": main()
