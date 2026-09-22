"""Audit UVP_C10."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_c10_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["comparison"]["maximum_residual"]=="0"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256") and l["tests"][22]["status"]=="PASS" and l["tests"][23]["authorization"]=="READY"
 print("UVP_C10_EVIDENCE_AUDIT_PASS"); print("NEXT_AUTHORIZED_TEST UVP_C11")
if __name__=="__main__": main()
