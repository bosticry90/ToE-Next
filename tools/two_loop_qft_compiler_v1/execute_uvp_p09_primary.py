"""Primary UVP_P09: exact one-loop total-derivative/IBP identity."""
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
    # Common normalization and (m^2)^(-epsilon) are immaterial to the identity.
    j2 = sp.gamma(e)
    j3_times_m2 = sp.gamma(1 + e)/2
    k2_over_denom3 = sp.simplify(j2 - j3_times_m2)
    exact_residual = sp.simplify(d*j2 - 4*k2_over_denom3)
    bad_residual = sp.simplify(4*j2 - 4*k2_over_denom3)
    bad_finite = sp.limit(bad_residual, e, 0)
    payload = {
        "schema_version": 1,
        "test_id": "UVP_P09",
        "attempt": 1,
        "contract_sha256": CH,
        "execution_plan_sha256": PH,
        "method": "denominator_decomposition_plus_gamma_recurrence_in_exact_d",
        "identity": "0=integral[d/(k2+m2)^2-4*k2/(k2+m2)^3]",
        "d": "4-2*epsilon",
        "J2_kernel": "Gamma(epsilon)",
        "m2_J3_kernel": "Gamma(1+epsilon)/2",
        "K_kernel": str(k2_over_denom3),
        "exact_d_residual": str(exact_residual),
        "normalized_UV_pole_residual": "0",
        "premature_d4_exact_residual": str(bad_residual),
        "premature_d4_missed_finite": str(bad_finite),
        "uv_ir": {"uv_pole": True, "ir_pole": False, "scaleless": False, "mass_domain": "m2>0", "rstar_required": False},
    }
    assert exact_residual == 0 and bad_finite == 2
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_p09_primary.json").write_text(json.dumps(payload, indent=2) + "\n")
    print("UVP_P09_PRIMARY_COMPLETE")
    print("EXACT_D_IBP_RESIDUAL", exact_residual)
    print("PREMATURE_D4_MISSED_FINITE", bad_finite)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])

if __name__ == "__main__":
    main()
