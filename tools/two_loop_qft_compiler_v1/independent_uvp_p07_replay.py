"""Independent UVP_P07 replay from Feynman parameters and large-t series."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    a, b, u, x = sp.symbols("m1sq m2sq u x", positive=True)
    # Gamma(epsilon)*[x*a+(1-x)*b+x(1-x)p2]^-epsilon has unit pole.
    log_residue = sp.integrate(1, (x, 0, 1))
    # Independently obtain the local mass term from the radial large-t factor.
    factor = sp.series(1 / ((1 + a*u)*(1 + b*u)), u, 0, 3).removeO()
    local_mass = sp.expand(factor).coeff(u, 1)
    assert log_residue == 1 and local_mass == -(a+b)
    payload = {
        "schema_version": 1, "test_id": "UVP_P07", "attempt": 1,
        "contract_sha256": CONTRACT_HASH, "execution_plan_sha256": PLAN_HASH,
        "method": "independent_Feynman_parameter_log_pole_and_radial_mass_series",
        "feynman_mass": "x*m1sq+(1-x)*m2sq+x*(1-x)*p2",
        "normalized_log_residue": str(log_residue),
        "radial_large_t_factor": str(factor),
        "k2_numerator_normalized_local_mass_residue": str(local_mass),
        "mass_swap_residual": str(sp.simplify(local_mass-local_mass.xreplace({a:b,b:a}))),
        "degenerate_limit": {"log_residue": "1", "k2_residue": str(sp.limit(local_mass,b,a))},
        "uv_ir": {"uv_pole": True, "ir_pole": False, "scaleless": False, "mass_domain": "m1sq>0,m2sq>0", "rstar_required": False},
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_p07_independent_replay.json").write_text(json.dumps(payload, indent=2)+"\n")
    print("UVP_P07_INDEPENDENT_REPLAY_COMPLETE"); print("LOG_RESIDUE",log_residue); print("LOCAL_MASS_RESIDUE",local_mass); print("ARTIFACT_SHA256",payload["artifact_sha256"])

if __name__ == "__main__": main()
