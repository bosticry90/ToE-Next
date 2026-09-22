"""Audit the promoted UVP_P09 evidence and ledger transition."""
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
def digest(x, field="artifact_sha256"):
    y=dict(x); y.pop(field,None)
    return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
    e=json.loads((HERE/"uvp_p09_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e); assert e["verdict"]=="PASS"; assert e["comparison"]["exact_d_IBP_residual"]=="0"
    l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert l["tests"][8]["status"]=="PASS"; assert l["tests"][9]["authorization"]=="READY"; assert l["counters"]["executed"]==9
    print("UVP_P09_EVIDENCE_AUDIT_PASS"); print("EXACT_D_IBP_RESIDUAL 0"); print("NEXT_AUTHORIZED_TEST UVP_P10")
if __name__=="__main__": main()
