"""Adjudicate UVP_P10."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_p10_primary.json"); r=load("uvp_p10_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:9]); row=l["tests"][9]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["tadpole_promoted_residue","tadpole_aux_derivative","log_bubble_promoted_residue","log_bubble_aux_derivative","two_auxiliary_mass_comparison_residual","uv_ir"]: assert p[k]==r[k]
 assert p["tadpole_promoted_residue"]=="-m2" and p["log_bubble_promoted_residue"]=="1" and p["tadpole_aux_derivative"]==p["log_bubble_aux_derivative"]=="0"
 u={"schema_version":1,"test_id":"UVP_P10","classification":p["uv_ir"],"reason":"positive physical and auxiliary masses protect IR while local UV residues cancel M2"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p10_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_P10","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"tadpole_residue":"-m2","bubble_residue":"1","maximum_auxiliary_mass_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p10_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":None,"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":None,"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"tadpole_residue":"-m2","bubble_residue":"1","maximum_auxiliary_mass_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"auxiliary_mass_cancels_after_all_local_IRR_terms","evidence_files":["uvp_p10_primary.json","uvp_p10_independent_replay.json","uvp_p10_uv_ir_provenance.json","uvp_p10_evidence.json"]})
 l["tests"][10]["authorization"]="READY"; l["counters"].update({"executed":10,"passed":10,"not_run_or_locked":29,"engine_executed":10,"engine_passed":10}); assert l["tests"][:9]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_P10_PASS"); print("MAXIMUM_AUXILIARY_MASS_RESIDUAL 0"); print("NEXT_TEST UVP_P11"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
