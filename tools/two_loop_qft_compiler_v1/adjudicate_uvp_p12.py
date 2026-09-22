"""Adjudicate UVP_P12."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_p12_primary.json"); r=load("uvp_p12_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:11]); row=l["tests"][11]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 assert p["normalized_UV_residue"]==r["normalized_UV_residue"]=="1"; assert p["uv_ir"]["ir_pole"] is False and r["uv_ir"]["ir_pole"] is False; assert p["nonlocal_UV_structures"]==r["nonlocal_UV_structures"]==[]
 u={"schema_version":1,"test_id":"UVP_P12","classification":{"offshell":p["uv_ir"],"auxiliary_mass":r["uv_ir"]},"reason":"both nonexceptional momentum and positive auxiliary mass regulate IR independently"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p12_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_P12","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"offshell_UV_residue":"1","auxiliary_mass_UV_residue":"1","residue_difference":"0","IR_poles":"none"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p12_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":None,"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":None,"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"normalized_UV_residue":"1","primary_minus_replay":"0","IR_poles":"none","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"nonexceptional_offshell_and_auxiliary_mass_extractions_agree_without_IR_contamination","evidence_files":["uvp_p12_primary.json","uvp_p12_independent_replay.json","uvp_p12_uv_ir_provenance.json","uvp_p12_evidence.json"]})
 l["tests"][12]["authorization"]="READY"; l["counters"].update({"executed":12,"passed":12,"not_run_or_locked":27,"engine_executed":12,"engine_passed":12}); assert l["tests"][:11]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_P12_PASS"); print("OFFSHELL_AND_AUX_UV_RESIDUE 1"); print("NEXT_TEST UVP_P13"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
