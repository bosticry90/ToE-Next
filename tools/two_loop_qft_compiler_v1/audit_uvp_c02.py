"""Audit UVP_C02."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_c02_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="PASS"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256") and l["tests"][14]["status"]=="PASS" and l["tests"][15]["authorization"]=="READY"
 print("UVP_C02_EVIDENCE_AUDIT_PASS"); print("NEXT_AUTHORIZED_TEST UVP_C03")
if __name__=="__main__": main()
