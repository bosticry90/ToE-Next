"""Audit UVP_M01 and the exact engine checkpoint."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_m01_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["comparison"]["derived_b10"]=="-34/3"
 g=json.loads((HERE/"uv_pole_engine_gate_result.json").read_text()); assert g["artifact_sha256"]==digest(g) and g["outcome"]=="ONE_LOOP_UV_POLE_EVALUATOR_PASS"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256") and all(x["status"]=="PASS" for x in l["tests"][:27]); assert l["tests"][27]["authorization"]=="READY" and l["counters"]["executed"]==27 and l["promotion"]["engine_gate"]=="PASS" and l["promotion"]["layer6_authorized"] is False
 print("UVP_M01_ENGINE_GATE_AUDIT_PASS"); print("ENGINE_GATE 27/27"); print("NEXT_AUTHORIZED_TEST UVP_M02"); print("LAYER6_AUTHORIZED false")
if __name__=="__main__": main()
