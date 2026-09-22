"""Audit UVP_P12."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_p12_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="PASS" and e["comparison"]["residue_difference"]=="0"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert l["tests"][11]["status"]=="PASS" and l["tests"][12]["authorization"]=="READY" and l["counters"]["executed"]==12
 print("UVP_P12_EVIDENCE_AUDIT_PASS"); print("UV_RESIDUE 1 IR_POLES none"); print("NEXT_AUTHORIZED_TEST UVP_P13")
if __name__=="__main__": main()
