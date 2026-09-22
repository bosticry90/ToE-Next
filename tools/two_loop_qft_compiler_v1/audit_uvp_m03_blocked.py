"""Audit the fail-fast M03 blocked transition."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_m03_blocked_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="BLOCKED" and e["comparison"]["physics_failure"] is False
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert all(x["status"]=="PASS" for x in l["tests"][:28]); assert l["tests"][28]["status"]=="BLOCKED"; assert all(x["status"]=="NOT_RUN" for x in l["tests"][29:]); assert l["counters"]=={"total_required":39,"executed":29,"passed":28,"blocked":1,"failed":0,"not_run_or_locked":10,"engine_required":27,"engine_executed":27,"engine_passed":27,"canonical_required":12,"canonical_executed":2,"canonical_passed":1}; assert l["promotion"]=={"engine_gate":"PASS","counterterm_compiler":"BLOCKED","layer6_authorized":False}
 print("UVP_M03_BLOCKED_EVIDENCE_AUDIT_PASS"); print("PROGRESS 29/39 PASSED 28 BLOCKED 1"); print("ENGINE_GATE PASS"); print("COUNTERTERM_COMPILER BLOCKED"); print("LAYER6_AUTHORIZED false")
if __name__=="__main__": main()
