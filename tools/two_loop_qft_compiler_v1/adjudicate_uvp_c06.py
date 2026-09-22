"""Adjudicate UVP_C06."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c06_primary.json"); r=load("uvp_c06_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:18]); row=l["tests"][18]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior); assert p["normalized_UV_residue"]==r["normalized_UV_residue"]=="0" and p["derived_delta_g"]==r["derived_delta_g"]=="0"
 u={"schema_version":1,"test_id":"UVP_C06","classification":p["uv_ir"],"reason":"massive_three_propagator_triangle_is_UV_and_IR_finite"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c06_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C06","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"UV_residue":"0","delta_g":"0","maximum_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c06_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"UV_residue":"0","delta_g":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"negative_superficial_degree_and_independent_Gamma_replay_both_UV_finite","evidence_files":["uvp_c06_primary.json","uvp_c06_independent_replay.json","uvp_c06_uv_ir_provenance.json","uvp_c06_evidence.json"]})
 l["tests"][19]["authorization"]="READY"; l["counters"].update({"executed":19,"passed":19,"not_run_or_locked":20,"engine_executed":19,"engine_passed":19}); assert l["tests"][:18]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C06_PASS"); print("TRIANGLE_UV_RESIDUE 0"); print("NEXT_TEST UVP_C07"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
