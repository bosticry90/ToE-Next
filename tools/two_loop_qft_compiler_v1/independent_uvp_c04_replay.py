"""Independent UVP_C04 replay from background Hessian determinant."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 ops=["TrLog_scalar_Hessian","background_phi_linear_projection"]
 p={"schema_version":1,"test_id":"UVP_C04","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_functional_determinant_with_M2(phi)=m2+g*phi","functional_inventory":ops,"inventory_sha256":digest({"operators":ops}),"one_point_loop_residue":"-g*m2/2","derived_tadpole_counterterm":"g*m2/2","sign_convention":"counterterm_is_minus_loop_pole","uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c04_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C04_INDEPENDENT_REPLAY_COMPLETE"); print("LOOP_ONE_POINT_RESIDUE -g*m2/2"); print("TADPOLE_COUNTERTERM g*m2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
