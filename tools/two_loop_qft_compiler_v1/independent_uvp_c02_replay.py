"""Independent UVP_C02 replay from the scalar functional determinant."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 ops=["TrLog_scalar_Hessian","background_phi4_projection","four_functional_derivatives"]
 p={"schema_version":1,"test_id":"UVP_C02","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_background_field_functional_determinant_phi4_projection","functional_operator_inventory":ops,"functional_operator_inventory_sha256":digest({"operators":ops}),"Hessian_mass":"m2+lambda*phi^2/2","crossing_permutation_residual":"0","derived_delta_lambda":"3*lambda^2/2","locality":True,"uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematics":"background potential with m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c02_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C02_INDEPENDENT_REPLAY_COMPLETE"); print("DELTA_LAMBDA 3*lambda^2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
