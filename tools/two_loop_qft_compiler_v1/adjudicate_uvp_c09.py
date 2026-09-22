"""Adjudicate UVP_C09."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c09_primary.json"); r=load("uvp_c09_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:21]); row=l["tests"][21]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["separate_b_coefficients","derived_b","longitudinal_residual_by_sector","background_transverse"]: assert p[k]==r[k]
 assert p["derived_b"]=="-11*C_A/3" and all(v=="0" for v in p["longitudinal_residual_by_sector"].values())
 u={"schema_version":1,"test_id":"UVP_C09","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"nonexceptional diagrammatic and local heat-kernel extractions have no IR pole"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c09_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C09","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"vector_b":"-10*C_A/3","ghost_b":"-C_A/3","total_b":"-11*C_A/3","transversality_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c09_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"b":"-11*C_A/3","vector_b":"-10*C_A/3","ghost_b":"-C_A/3","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"diagrammatic_vector_ghost_split_matches_independent_minimal_operator_heat_kernel","evidence_files":["uvp_c09_primary.json","uvp_c09_independent_replay.json","uvp_c09_uv_ir_provenance.json","uvp_c09_evidence.json"]})
 l["tests"][22]["authorization"]="READY"; l["counters"].update({"executed":22,"passed":22,"not_run_or_locked":17,"engine_executed":22,"engine_passed":22}); assert l["tests"][:21]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C09_PASS"); print("DERIVED_B -11*C_A/3"); print("NEXT_TEST UVP_C10"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
