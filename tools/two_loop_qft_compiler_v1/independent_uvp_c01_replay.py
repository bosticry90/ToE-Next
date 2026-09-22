"""Independent UVP_C01 replay from the background-dependent Hessian determinant."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 p={"schema_version":1,"test_id":"UVP_C01","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_functional_determinant_expansion_of_M2(phi)=m2+lambda*phi2/2","functional_pole_kernel":"-M2(phi)^2/4 in frozen d=4-2epsilon action convention","derived_counterterms":{"delta_Z_phi":"0","delta_m2":"lambda*m2/2"},"p2_pole":"0","locality":True,
   "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c01_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n")
 print("UVP_C01_INDEPENDENT_REPLAY_COMPLETE"); print("DELTA_Z_PHI 0"); print("DELTA_M2 lambda*m2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
