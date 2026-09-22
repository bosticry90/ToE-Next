"""Adjudicate UVP_C08."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c08_primary.json"); r=load("uvp_c08_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:20]); row=l["tests"][20]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["two_point_loop_pole","vertex_longitudinal_loop_pole","Ward_residual","derived_counterterms","sample_checks","maximum_renormalized_UV_residual","uv_ir"]: assert p[k]==r[k]
 assert p["Ward_residual"]==p["maximum_renormalized_UV_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C08","classification":p["uv_ir"],"reason":"offshell_or_mass_regulated_amplitudes_are_IR_safe_and_scaleless_seagull_is_split"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c08_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C08","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"Ward_residual":"0","maximum_renormalized_UV_residual":"0","xi_samples":[0,1,2]},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c08_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"Ward_residual":"0","maximum_renormalized_UV_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"general_xi_graph_calculation_matches_independent_covariant_pole_action","evidence_files":["uvp_c08_primary.json","uvp_c08_independent_replay.json","uvp_c08_uv_ir_provenance.json","uvp_c08_evidence.json"]})
 l["tests"][21]["authorization"]="READY"; l["counters"].update({"executed":21,"passed":21,"not_run_or_locked":18,"engine_executed":21,"engine_passed":21}); assert l["tests"][:20]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C08_PASS"); print("WARD_RESIDUAL 0"); print("NEXT_TEST UVP_C09"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
