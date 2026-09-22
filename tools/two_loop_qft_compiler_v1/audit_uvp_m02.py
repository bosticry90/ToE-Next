"""Audit UVP_M02."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_m02_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["comparison"]["maximum_residual"]=="0"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256") and all(x["status"]=="PASS" for x in l["tests"][:28]) and l["tests"][28]["authorization"]=="READY"; assert l["promotion"]["engine_gate"]=="PASS" and l["promotion"]["counterterm_compiler"]=="BLOCKED" and l["promotion"]["layer6_authorized"] is False
 print("UVP_M02_EVIDENCE_AUDIT_PASS"); print("CANONICAL_PROGRESS 1/12"); print("NEXT_AUTHORIZED_TEST UVP_M03")
if __name__=="__main__": main()
