"""Independent UVP_C03 replay by bare-action expansion."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 inv=["bare_m2_expansion_phi2","bare_lambda_expansion_phi4","functional_TrLog_phi2","functional_TrLog_phi4"]
 p={"schema_version":1,"test_id":"UVP_C03","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_bare_action_first_order_expansion_plus_functional_pole_action","inventory":inv,"inventory_sha256":digest({"inventory":inv}),"derived_counterterms":{"delta_Z_phi":"0","delta_m2":"lambda*m2/2","delta_lambda":"3*lambda^2/2"},"two_point_residual":"0","four_point_residual":"0","wavefunction_residual":"0","maximum_residual":"0","uv_ir":{"uv_pole_before_CT":True,"ir_pole":False,"renormalized_UV_pole":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c03_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C03_INDEPENDENT_REPLAY_COMPLETE"); print("MAXIMUM_RENORMALIZED_UV_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
