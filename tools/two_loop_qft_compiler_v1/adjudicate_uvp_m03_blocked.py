"""Record UVP_M03 as the first fail-fast BLOCKED test."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_m03_primary_blocker.json"); r=load("uvp_m03_independent_blocker_replay.json"); assert p["blocker_code"]==r["blocker_code"] and p["classification"]==r["classification"] and not p["all_four_quadratic_directions_derived"] and not r["all_four_quadratic_directions_derived"]
 lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:28]); row=l["tests"][28]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 u={"schema_version":1,"test_id":"UVP_M03","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"UV_IR_classification_deferred_because_required_1PI_integrands_do_not_exist"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_m03_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_M03","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"blocker_agreement":True,"blocker_code":p["blocker_code"],"physics_failure":False,"residues_derived":False},"uv_ir_classification":u["classification"],"verdict":"BLOCKED"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_m03_blocked_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"BLOCKED","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"residues_derived":False,"blocker_code":p["blocker_code"],"classification":p["classification"],"evidence_sha256":e["artifact_sha256"]},"verdict_reason":"required_exhaustive_parent_scalar_2pt_contraction_and_projection_kernel_is_not_implemented","evidence_files":["uvp_m03_primary_blocker.json","uvp_m03_independent_blocker_replay.json","uvp_m03_uv_ir_provenance.json","uvp_m03_blocked_evidence.json"]})
 l["overall_status"]="CANONICAL_BLOCKED"; l["authority"]="ENGINE_GATE_AUTHORITY"; l["counters"].update({"executed":29,"passed":28,"blocked":1,"failed":0,"not_run_or_locked":10,"canonical_executed":2,"canonical_passed":1}); l["promotion"].update({"engine_gate":"PASS","counterterm_compiler":"BLOCKED","layer6_authorized":False}); assert l["tests"][:28]==prior; assert all(x["status"]=="NOT_RUN" and x["authorization"]=="WAITING_PREDECESSOR" for x in l["tests"][29:]); l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_M03_BLOCKED"); print("BLOCKER_CODE",p["blocker_code"]); print("FAIL_FAST_STOP 29/39"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
