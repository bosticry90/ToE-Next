"""Audit UVP_P11."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_p11_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="PASS"; assert e["comparison"]["UV_residue"]=="1" and e["comparison"]["IR_residue"]=="-1"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert l["tests"][10]["status"]=="PASS" and l["tests"][11]["authorization"]=="READY" and l["counters"]["executed"]==11
 print("UVP_P11_EVIDENCE_AUDIT_PASS"); print("UV_RESIDUE 1 IR_RESIDUE -1"); print("NEXT_AUTHORIZED_TEST UVP_P12")
if __name__=="__main__": main()
