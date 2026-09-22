"""Audit UVP_P13 and primitive-suite completion."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_p13_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="PASS" and e["comparison"]["pairing_count"]==105
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert all(x["status"]=="PASS" for x in l["tests"][:13]); assert l["tests"][13]["authorization"]=="READY" and l["counters"]["executed"]==13
 print("UVP_P13_EVIDENCE_AUDIT_PASS"); print("PRIMITIVE_SUITE 13/13"); print("NEXT_AUTHORIZED_TEST UVP_C01")
if __name__=="__main__": main()
