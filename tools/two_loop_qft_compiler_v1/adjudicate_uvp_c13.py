"""Adjudicate UVP_C13."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_c13_primary.json"); r=load("uvp_c13_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:25]); row=l["tests"][25]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["derived_UV_residues","auxiliary_mass_derivative","local_IR_counterterm_sum_recorded","spurious_IR_pole_after_Rstar","maximum_residual"]: assert p[k]==r[k]
 assert p["derived_UV_residues"]["background_b"]=="-7" and p["maximum_residual"]=="0"
 u={"schema_version":1,"test_id":"UVP_C13","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"auxiliary_mass_plus_Rstar_and_nonexceptional_offshell_routes_agree"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_c13_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_C13","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"background_b":"-7","auxiliary_mass_derivative":"0","spurious_IR_pole":"0","maximum_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_c13_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"background_b":"-7","maximum_UV_IR_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"auxiliary_mass_Rstar_and_offshell_extractions_reproduce_complete_broken_control_residues","evidence_files":["uvp_c13_primary.json","uvp_c13_independent_replay.json","uvp_c13_uv_ir_provenance.json","uvp_c13_evidence.json"]})
 l["tests"][26]["authorization"]="READY"; l["counters"].update({"executed":26,"passed":26,"not_run_or_locked":13,"engine_executed":26,"engine_passed":26}); assert l["tests"][:25]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_C13_PASS"); print("CONTROL_SUITE 13/13"); print("NEXT_TEST UVP_M01"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
