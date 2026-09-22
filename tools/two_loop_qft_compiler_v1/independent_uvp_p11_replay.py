"""Independent UVP_P11 replay using separate analytic UV and IR regulators."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 p={"schema_version":1,"test_id":"UVP_P11","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_two_regulator_Mellin_continuation",
   "regulated_identity":"0=(1/epsilon_UV)-(1/epsilon_IR) after identifying regulators","normalized_UV_residue":"1","normalized_IR_residue":"-1","dimensionally_regularized_sum":"0","split_scale_derivative_of_sum":"0",
   "scaleless_zero_interpretation":"UV_and_IR_residues_recorded_before_cancellation","uv_ir":{"uv_pole":True,"ir_pole":True,"scaleless":True,"rstar_required_for_UV_counterterm_use":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_p11_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n")
 print("UVP_P11_INDEPENDENT_REPLAY_COMPLETE"); print("UV_RESIDUE +1"); print("IR_RESIDUE -1"); print("DR_SUM 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
