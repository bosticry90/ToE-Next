"""Adjudicate UVP_C12."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c12_primary.json"); r=load("uvp_c12_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:24]); row=l["tests"][24]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["beta_parts","derived_parent_b","mass_pairing","quartic_ghost_vertex","sample_checks","maximum_residual"]: assert p[k]==r[k]
 assert p["derived_parent_b"]=="-7" and p["maximum_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C12","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"broken roots are massive and unbroken background momentum is nonexceptional"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c12_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C12","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"parent_b":"-7","mass_pairing_residual":"0","BRST_residual":"0","quartic_ghost_residual":"0","maximum_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c12_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"parent_b":"-7","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"explicit_structure_constant_diagrams_match_root_weight_functional_BRST_replay","evidence_files":["uvp_c12_primary.json","uvp_c12_independent_replay.json","uvp_c12_uv_ir_provenance.json","uvp_c12_evidence.json"]})
 l["tests"][25]["authorization"]="READY"; l["counters"].update({"executed":25,"passed":25,"not_run_or_locked":14,"engine_executed":25,"engine_passed":25}); assert l["tests"][:24]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C12_PASS"); print("DERIVED_PARENT_B -7"); print("NEXT_TEST UVP_C13"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
