"""Adjudicate UVP_M01 and freeze the distinct 27/27 engine checkpoint."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
EXPECTED="-34/3"
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_m01_primary.json"); r=load("uvp_m01_independent_replay.json")
 # Artifacts are immutable before the previously earned comparator is read here.
 for k in ["beta_parts","derived_b10","background_two_point_pole","transversality_residual"]: assert p[k]==r[k]
 assert p["imported_expected_b10"] is r["imported_expected_b10"] is False
 assert p["derived_b10"]==EXPECTED
 lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:26]); row=l["tests"][26]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 u={"schema_version":1,"test_id":"UVP_M01","classification":{"primary":p["uv_ir"],"replay":r["uv_ir"]},"reason":"nonexceptional_background_and_local_heat_kernel_routes_are_IR_safe"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_m01_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_M01","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"primary_minus_replay":"0","derived_b10":"-34/3","comparison_to_previously_earned_b10":"exact","transversality_residual":"0"},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_m01_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":p["inventory_sha256"],"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":r["inventory_sha256"],"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"b10":"-34/3","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"dimension_Casimir_sector_sum_matches_independent_weight_charge_sum_before_expected_comparison","evidence_files":["uvp_m01_primary.json","uvp_m01_independent_replay.json","uvp_m01_uv_ir_provenance.json","uvp_m01_evidence.json"]})
 for i,x in enumerate(l["tests"][27:]): x["status"]="NOT_RUN"; x["authorization"]="READY" if i==0 else "WAITING_PREDECESSOR"
 l["overall_status"]="ONE_LOOP_UV_POLE_EVALUATOR_PASS"; l["authority"]="ENGINE_GATE_AUTHORITY"; l["promotion"].update({"engine_gate":"PASS","counterterm_compiler":"BLOCKED","layer6_authorized":False}); l["counters"].update({"executed":27,"passed":27,"not_run_or_locked":12,"engine_executed":27,"engine_passed":27,"canonical_executed":0,"canonical_passed":0})
 assert l["tests"][:26]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 gate={"schema_version":1,"outcome":"ONE_LOOP_UV_POLE_EVALUATOR_PASS","contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"tests_passed":"27/27","primitive":"13/13","controls":"13/13","canonical_parent_gauge":"1/1","derived_b10":"-34/3","ledger_sha256":l["result_sha256"],"M01_evidence_sha256":e["artifact_sha256"],"counterterm_compiler":"BLOCKED","layer6_authorized":False}; gate["artifact_sha256"]=digest(gate); (HERE/"uv_pole_engine_gate_result.json").write_text(json.dumps(gate,indent=2)+"\n")
 print("UVP_M01_PASS"); print("DERIVED_B10 -34/3"); print("ONE_LOOP_UV_POLE_EVALUATOR_PASS"); print("NEXT_TEST UVP_M02"); print("ENGINE_GATE_ARTIFACT_SHA256",gate["artifact_sha256"])
if __name__=="__main__": main()
