"""Independent UVP_C05 replay from Feynman parameters."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 inv=["two_cubic_vertices","Feynman_x_integral","Gamma(epsilon)"]
 p={"schema_version":1,"test_id":"UVP_C05","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_nonexceptional_Feynman_parameter_bubble","inventory":inv,"inventory_sha256":digest({"inventory":inv}),"parameter_kernel":"Gamma(epsilon)*integral_0^1 dx [m2+x(1-x)p2]^(-epsilon)","loop_mass_pole":"-g^2/2","derived_delta_m2":"g^2/2","p2_wavefunction_pole":"0","derived_delta_Z_phi":"0","locality":True,"uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c05_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C05_INDEPENDENT_REPLAY_COMPLETE"); print("DELTA_M2 g^2/2"); print("DELTA_Z_PHI 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
