"""Adjudicate UVP_C11."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c11_primary.json"); r=load("uvp_c11_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:23]); row=l["tests"][23]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["background_b","background_transversality_residual","tree_mass_pairing","one_loop_mass_pairing_identity","mass_pairing_residual","tadpole_pole_expression","derived_delta_t","derived_delta_v","FJ_stationarity_residual","sample_xi_checks","maximum_residual"]: assert p[k]==r[k]
 assert p["background_b"]=="1/3" and p["maximum_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C11","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"broken masses and nonexceptional/functional projectors protect IR"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c11_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C11","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"background_b":"1/3","mass_pairing_residual":"0","FJ_stationarity_residual":"0","maximum_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c11_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"background_b":"1/3","mass_pairing_residual":"0","FJ_stationarity_residual":"0","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"broken_phase_graphs_match_functional_BRST_and_FJ_tadpole_projection","evidence_files":["uvp_c11_primary.json","uvp_c11_independent_replay.json","uvp_c11_uv_ir_provenance.json","uvp_c11_evidence.json"]})
 l["tests"][24]["authorization"]="READY"; l["counters"].update({"executed":24,"passed":24,"not_run_or_locked":15,"engine_executed":24,"engine_passed":24}); assert l["tests"][:23]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C11_PASS"); print("BACKGROUND_B 1/3"); print("NEXT_TEST UVP_C12"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
