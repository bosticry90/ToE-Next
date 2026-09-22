"""Audit UVP_P10."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); y.pop(field,None); return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 e=json.loads((HERE/"uvp_p10_evidence.json").read_text()); assert e["artifact_sha256"]==digest(e) and e["verdict"]=="PASS"; assert e["comparison"]["maximum_auxiliary_mass_residual"]=="0"
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); assert l["result_sha256"]==digest(l,"result_sha256"); assert l["tests"][9]["status"]=="PASS" and l["tests"][10]["authorization"]=="READY" and l["counters"]["executed"]==10
 print("UVP_P10_EVIDENCE_AUDIT_PASS"); print("MAXIMUM_AUXILIARY_MASS_RESIDUAL 0"); print("NEXT_AUTHORIZED_TEST UVP_P11")
if __name__=="__main__": main()
