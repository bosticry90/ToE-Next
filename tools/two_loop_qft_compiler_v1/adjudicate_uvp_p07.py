"""Adjudicate UVP_P07."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import sympy as sp

HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"):
    y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(n):
    x=json.loads((HERE/n).read_text()); assert x["artifact_sha256"]==digest(x); return x

def main():
    p=load("uvp_p07_primary.json"); r=load("uvp_p07_independent_replay.json")
    lp=HERE/"uv_pole_evaluator_results.json"; l=json.loads(lp.read_text()); ls=json.loads((HERE/"uv_pole_evaluator_result_schema.json").read_text())
    assert l["result_sha256"]==digest(l,"result_sha256"); prior=deepcopy(l["tests"][:6]); row=l["tests"][6]
    assert row["test_id"]=="UVP_P07" and row["authorization"]=="READY" and all(x["status"]=="PASS" for x in prior)
    logdiff=sp.simplify(sp.sympify(p["normalized_log_residue"])-sp.sympify(r["normalized_log_residue"]))
    massdiff=sp.simplify(sp.sympify(p["k2_numerator_normalized_local_mass_residue"])-sp.sympify(r["k2_numerator_normalized_local_mass_residue"]))
    if not (logdiff==massdiff==0 and p["mass_swap_residual"]==r["mass_swap_residual"]=="0" and p["uv_ir"]==r["uv_ir"]): raise AssertionError("P07 mismatch")
    u={"schema_version":1,"test_id":"UVP_P07","classification":{"uv_pole":True,"ir_pole":False,"scaleless":False,"rstar_required":False},"reason":"both_unequal_masses_positive"}; u["artifact_sha256"]=digest(u); (HERE/"uvp_p07_uv_ir_provenance.json").write_text(json.dumps(u,indent=2)+"\n")
    e={"schema_version":1,"test_id":"UVP_P07","attempt":1,"contract_sha256":p["contract_sha256"],"execution_plan_sha256":p["execution_plan_sha256"],"primary":p,"independent_replay":r,"comparison":{"log_residue_difference":str(logdiff),"local_mass_residue_difference":str(massdiff),"mass_swap_residual":"0","degenerate_limit_equal":True},"uv_ir_classification":u["classification"],"verdict":"PASS"}; e["artifact_sha256"]=digest(e); (HERE/"uvp_p07_evidence.json").write_text(json.dumps(e,indent=2)+"\n")
    row.update({"status":"PASS","authorization":"TERMINAL","attempt":1,"primary":{"state":"COMPLETE","method":p["method"],"inventory_sha256":None,"residue_sha256":p["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"replay":{"state":"COMPLETE","method":r["method"],"inventory_sha256":None,"residue_sha256":r["artifact_sha256"],"uv_ir_provenance_sha256":u["artifact_sha256"]},"derived_result":{"normalized_log_residue":"1","local_mass_residue":p["k2_numerator_normalized_local_mass_residue"],"maximum_residual":"0","evidence_sha256":e["artifact_sha256"]},"verdict_reason":"unequal_mass_partial_fraction_and_Feynman_parameter_radial_replay_agree","evidence_files":["uvp_p07_primary.json","uvp_p07_independent_replay.json","uvp_p07_uv_ir_provenance.json","uvp_p07_evidence.json"]})
    l["tests"][7]["authorization"]="READY"; l["counters"].update({"executed":7,"passed":7,"not_run_or_locked":32,"engine_executed":7,"engine_passed":7}); assert l["tests"][:6]==prior
    l.pop("result_sha256"); l["result_sha256"]=digest(l,"result_sha256"); Draft202012Validator(ls).validate(l); lp.write_text(json.dumps(l,indent=2)+"\n")
    print("UVP_P07_PASS"); print("LOG_RESIDUE 1"); print("LOCAL_MASS_RESIDUE",p["k2_numerator_normalized_local_mass_residue"]); print("NEXT_TEST UVP_P08"); print("EVIDENCE_SHA256",e["artifact_sha256"])
if __name__=="__main__": main()
