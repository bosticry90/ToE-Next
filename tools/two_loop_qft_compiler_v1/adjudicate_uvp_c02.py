"""Adjudicate UVP_C02."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c02_primary.json"); r=load("uvp_c02_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:14]); row=l["tests"][14]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 assert p["derived_delta_lambda"]==r["derived_delta_lambda"]=="3*lambda^2/2" and p["crossing_permutation_residual"]==r["crossing_permutation_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C02","classification":p["uv_ir"],"reason":"massive_or_nonexceptional_phi4_bubbles_have_no_IR_pole"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c02_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C02","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"delta_lambda":"3*lambda^2/2","crossing_residual":"0","maximum_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c02_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["graph_inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["functional_operator_inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"delta_lambda":"3*lambda^2/2","crossing_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"three_channel_graph_sum_matches_independent_functional_determinant","evidence_files":["uvp_c02_primary.json","uvp_c02_independent_replay.json","uvp_c02_uv_ir_provenance.json","uvp_c02_evidence.json"]})
 l["tests"][15]["authorization"]="READY"; l["counters"].update({"executed":15,"passed":15,"not_run_or_locked":24,"engine_executed":15,"engine_passed":15}); assert l["tests"][:14]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C02_PASS"); print("DELTA_LAMBDA 3*lambda^2/2"); print("NEXT_TEST UVP_C03"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
