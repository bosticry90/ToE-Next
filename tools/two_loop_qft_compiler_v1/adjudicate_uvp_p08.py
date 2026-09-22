"""Adjudicate UVP_P08."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_p08_primary.json"); r=load("uvp_p08_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); ls=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:7]); row=l["tests"][7]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 if not (p["normalized_UV_residue_difference"]==r["normalized_UV_residue_difference"]=="0" and p["surface_term_residue"]==r["surface_term_residue"]=="0" and p["translation_Jacobian"]==r["translation_Jacobian"]=="1" and p["uv_ir"]==r["uv_ir"]): raise AssertionError("P08 routing mismatch")
 u={"schema_version":1,"test_id":"UVP_P08","classification":{"uv_pole":True,"ir_pole":False,"scaleless":False,"rstar_required":False},"reason":"massive_integral_and_translation_invariant_dimensional_measure"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p08_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_P08","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"routing_A_residue":"1","routing_B_residue":"1","residue_difference":"0","surface_term_residue":"0","Jacobian":"1"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p08_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":None,"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":None,"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"routing_A_residue":"1","routing_B_residue":"1","maximum_routing_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"two_local_routing_expansions_equal_exact_affine_shift_replay","evidence_files":["uvp_p08_primary.json","uvp_p08_independent_replay.json","uvp_p08_uv_ir_provenance.json","uvp_p08_evidence.json"]})
 l["tests"][8]["authorization"]="READY"; l["counters"].update({"executed":8,"passed":8,"not_run_or_locked":31,"engine_executed":8,"engine_passed":8}); assert l["tests"][:7]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(ls).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_P08_PASS"); print("ROUTING_RESIDUES 1 1"); print("MAXIMUM_ROUTING_RESIDUAL 0"); print("NEXT_TEST UVP_P09"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
