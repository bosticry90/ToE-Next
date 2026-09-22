"""Adjudicate UVP_P11."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_p11_primary.json"); r=load("uvp_p11_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:10]); row=l["tests"][10]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["normalized_UV_residue","normalized_IR_residue","dimensionally_regularized_sum","split_scale_derivative_of_sum","uv_ir"]: assert p[k]==r[k]
 assert p["normalized_UV_residue"]=="1" and p["normalized_IR_residue"]=="-1" and p["dimensionally_regularized_sum"]=="0"
 u={"schema_version":1,"test_id":"UVP_P11","classification":p["uv_ir"],"reason":"scaleless_DR_zero_is_explicit_plus_UV_minus_IR_cancellation"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p11_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_P11","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"UV_residue":"1","IR_residue":"-1","DR_sum":"0","maximum_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p11_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":None,"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":None,"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"UV_residue":"1","IR_residue":"-1","DR_sum":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"UV_and_IR_poles_separately_recorded_before_scaleless_cancellation","evidence_files":["uvp_p11_primary.json","uvp_p11_independent_replay.json","uvp_p11_uv_ir_provenance.json","uvp_p11_evidence.json"]})
 l["tests"][11]["authorization"]="READY"; l["counters"].update({"executed":11,"passed":11,"not_run_or_locked":28,"engine_executed":11,"engine_passed":11}); assert l["tests"][:10]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_P11_PASS"); print("UV_IR_RESIDUES +1 -1"); print("NEXT_TEST UVP_P12"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
