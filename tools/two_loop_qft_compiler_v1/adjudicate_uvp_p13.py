"""Adjudicate UVP_P13."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n): x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x
def main():
 p=load("uvp_p13_primary.json"); r=load("uvp_p13_independent_replay.json"); lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); s=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:12]); row=l["tests"][12]; assert row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
 for k in ["pairing_count","expected_pairing_count","pairings","dimension_denominator","dimension_denominator_at_d4","normalized_residue_per_pairing","recursive_contractions","premature_d4_missed_finite_shift_per_pairing","uv_ir"]: assert p[k]==r[k]
 assert p["pairing_count"]==105 and p["normalized_residue_per_pairing"]=="1/1920" and all(v=="0" for v in p["recursive_contractions"].values())
 u={"schema_version":1,"test_id":"UVP_P13","classification":p["uv_ir"],"reason":"massive_rank8_logarithmic_primitive_has_no_IR_pole"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p13_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
 e={"schema_version":1,"test_id":"UVP_P13","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"pairing_set_primary_minus_replay":[],"pairing_set_replay_minus_primary":[],"pairing_count":105,"per_pairing_residue":"1/1920","maximum_contraction_residual":"0"},"uv_ir_classification":p["uv_ir"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p13_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
 row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":digest({"pairings":p["pairings"]}),"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":digest({"pairings":r["pairings"]}),"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"pairing_count":105,"per_pairing_residue":"1/1920","maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"exact_105_pairing_rank8_reduction_and_independent_permutation_orbit_replay","evidence_files":["uvp_p13_primary.json","uvp_p13_independent_replay.json","uvp_p13_uv_ir_provenance.json","uvp_p13_evidence.json"]})
 l["tests"][13]["authorization"]="READY"; l["counters"].update({"executed":13,"passed":13,"not_run_or_locked":26,"engine_executed":13,"engine_passed":13}); assert l["tests"][:12]==prior; l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(s).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
 print("UVP_P13_PASS"); print("PAIRING_COUNT 105"); print("PRIMITIVE_SUITE 13/13"); print("NEXT_TEST UVP_C01"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
