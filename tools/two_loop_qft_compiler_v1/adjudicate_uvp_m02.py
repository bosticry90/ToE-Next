"""Adjudicate UVP_M02."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_m02_primary.json"); r=load("uvp_m02_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:27]); row=l["tests"][27]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["derived_residues","irrep_identity_checks","scalar_cubic_quartic_p2_pole","sample_xi_max_residual","maximum_residual"]: assert p[k]==r[k]
 assert p["maximum_residual"]=="0" and all(v["off_diagonal_residual"]==v["diagonal_spread"]=="0" for v in p["irrep_identity_checks"].values())
 u={"schema_version":1,"test_id":"UVP_M02","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"nonexceptional derivative projectors separate IR and scalar-potential loops have no p2 pole"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_m02_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_M02","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"four_field_residues":p["derived_residues"],"irrep_identity_max_residual":"0","maximum_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_m02_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"scalar_field_residues":p["derived_residues"],"maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"parent_action_graphs_match_independent_covariant_symbol_and_all_irrep_matrices_are_identity","evidence_files":["uvp_m02_primary.json","uvp_m02_independent_replay.json","uvp_m02_uv_ir_provenance.json","uvp_m02_evidence.json"]})
 l["tests"][28]["authorization"]="READY"; l["overall_status"]="CANONICAL_RUNNING"; l["authority"]="ENGINE_GATE_AUTHORITY"; l["counters"].update({"executed":28,"passed":28,"not_run_or_locked":11,"canonical_executed":1,"canonical_passed":1}); l["promotion"].update({"engine_gate":"PASS","counterterm_compiler":"BLOCKED","layer6_authorized":False}); assert l["tests"][:27]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_M02_PASS"); print("FOUR_SCALAR_FIELD_RESIDUES_DERIVED"); print("NEXT_TEST UVP_M03"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
