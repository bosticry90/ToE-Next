"""Adjudicate UVP_C07."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c07_primary.json"); r=load("uvp_c07_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:19]); row=l["tests"][19]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["background_two_point_pole","derived_b","background_transverse","longitudinal_contraction_residual"]: assert p[k]==r[k]
 assert p["uv_ir"]["uv_pole"]==r["uv_ir"]["uv_pole"] is True and p["uv_ir"]["ir_pole"]==r["uv_ir"]["ir_pole"] is False
 assert p["derived_b"]=="1/3" and p["longitudinal_contraction_residual"]=="0" and p["mass_term_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C07","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"massive_or_nonexceptional_scalar_QED_background_two_point_is_IR_safe"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c07_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C07","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"b":"1/3","transversality_residual":"0","mass_term_residual":"0","maximum_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c07_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"b":"1/3","transversality_residual":"0","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"bubble_plus_seagull_tensor_projection_matches_covariant_heat_kernel","evidence_files":["uvp_c07_primary.json","uvp_c07_independent_replay.json","uvp_c07_uv_ir_provenance.json","uvp_c07_evidence.json"]})
 l["tests"][20]["authorization"]="READY"; l["counters"].update({"executed":20,"passed":20,"not_run_or_locked":19,"engine_executed":20,"engine_passed":20}); assert l["tests"][:19]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C07_PASS"); print("DERIVED_B 1/3"); print("TRANSVERSALITY_RESIDUAL 0"); print("NEXT_TEST UVP_C08"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
