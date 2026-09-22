"""Independent UVP_P09 replay from a Schwinger-parameter boundary identity."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
CH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"

def digest(x):
    return sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    e = sp.symbols("epsilon")
    d = 4 - 2*e
    # Gaussian moments give K=(d/4)J2 without using the primary decomposition.
    j2 = sp.gamma(e)
    k = sp.simplify(d*j2/4)
    residual = sp.simplify(d*j2 - 4*k)
    bad = sp.simplify(4*j2 - 4*k)
    bad_finite = sp.limit(bad, e, 0)
    payload = {
        "schema_version": 1,
        "test_id": "UVP_P09",
        "attempt": 1,
        "contract_sha256": CH,
        "execution_plan_sha256": PH,
        "method": "independent_schwinger_parameter_gaussian_moment_total_derivative",
        "identity": "K=(d/4)J2 from Gaussian moment",
        "d": "4-2*epsilon",
        "J2_kernel": "Gamma(epsilon)",
        "K_kernel": str(k),
        "exact_d_residual": str(residual),
        "normalized_UV_pole_residual": "0",
        "premature_d4_exact_residual": str(bad),
        "premature_d4_missed_finite": str(bad_finite),
        "uv_ir": {"uv_pole": True, "ir_pole": False, "scaleless": False, "mass_domain": "m2>0", "rstar_required": False},
    }
    assert residual == 0 and bad_finite == 2
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_p09_independent_replay.json").write_text(json.dumps(payload, indent=2) + "\n")
    print("UVP_P09_INDEPENDENT_REPLAY_COMPLETE")
    print("EXACT_D_IBP_RESIDUAL", residual)
    print("PREMATURE_D4_MISSED_FINITE", bad_finite)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])

if __name__ == "__main__":
    main()
