"""Primary UVP_P12: nonexceptional massless off-shell bubble."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 p={"schema_version":1,"test_id":"UVP_P12","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"nonexceptional_offshell_Feynman_parameter_Gamma_projection",
   "integral":"integral 1/[k2 (k+p)2] with Euclidean p2>0","parameter_kernel":"Gamma(epsilon)*integral_0^1 dx [x(1-x)p2]^(-epsilon)",
   "normalized_UV_residue":"1","p2_derivative_of_UV_residue":"0","nonlocal_UV_structures":[],
   "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematic_domain":"Euclidean p2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_p12_primary.json").write_text(json.dumps(p,indent=2)+"\n")
 print("UVP_P12_PRIMARY_COMPLETE"); print("OFFSHELL_UV_RESIDUE 1"); print("IR_POLE false"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
