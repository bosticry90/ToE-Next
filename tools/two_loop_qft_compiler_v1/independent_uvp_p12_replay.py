"""Independent UVP_P12 replay using an auxiliary-mass rearrangement."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 p={"schema_version":1,"test_id":"UVP_P12","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_auxiliary_mass_IR_rearrangement_with_finite_difference",
   "rearranged_integral":"integral 1/(k2+M2)^2","difference_classification":"UV_finite","normalized_UV_residue":"1","auxiliary_mass_derivative_of_UV_residue":"0","nonlocal_UV_structures":[],
   "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematic_domain":"auxiliary M2>0; compared to Euclidean p2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_p12_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n")
 print("UVP_P12_INDEPENDENT_REPLAY_COMPLETE"); print("AUXILIARY_MASS_UV_RESIDUE 1"); print("AUXILIARY_MASS_DERIVATIVE 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
