"""Audit UVP_C13 and control-suite completion."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_c13_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["comparison"]["maximum_residual"]=="0"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256") and all(x["status"]=="PASS" for x in l["tests"][:26]) and l["tests"][26]["authorization"]=="READY"
 print("UVP_C13_EVIDENCE_AUDIT_PASS"); print("CONTROL_SUITE 13/13"); print("NEXT_AUTHORIZED_TEST UVP_M01")
if __name__=="__main__": main()
