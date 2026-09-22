"""Adjudicate UVP_C01."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c01_primary.json"); r=load("uvp_c01_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:13]); row=l["tests"][13]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 assert p["derived_counterterms"]==r["derived_counterterms"]=={"delta_Z_phi":"0","delta_m2":"lambda*m2/2"}; assert p["p2_pole"]==r["p2_pole"]=="0"
 u={"schema_version":1,"test_id":"UVP_C01","classification":p["uv_ir"],"reason":"massive_phi4_tadpole_has_UV_but_no_IR_pole"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c01_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C01","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"delta_Z_phi":"0","delta_m2":"lambda*m2/2","maximum_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c01_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["graph_inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":digest({"functional_operator_inventory":["TrLog_scalar_Hessian","phi2_projection"]}),"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"delta_Z_phi":"0","delta_m2":"lambda*m2/2","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"action_graph_and_independent_functional_determinant_phi4_two_point_agree","evidence_files":["uvp_c01_primary.json","uvp_c01_independent_replay.json","uvp_c01_uv_ir_provenance.json","uvp_c01_evidence.json"]})
 l["tests"][14]["authorization"]="READY"; l["counters"].update({"executed":14,"passed":14,"not_run_or_locked":25,"engine_executed":14,"engine_passed":14}); assert l["tests"][:13]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C01_PASS"); print("DELTA_Z_PHI 0 DELTA_M2 lambda*m2/2"); print("NEXT_TEST UVP_C02"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
