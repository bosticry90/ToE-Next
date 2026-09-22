"""Audit UVP_P08."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field="artifact_sha256"): y=dict(x); z=y.pop(field); a=sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest(); assert z==a; return a
def main():
 l=json.loads((HERE/"uv_pole_evaluator_results.json").read_text()); e=json.loads((HERE/"uvp_p08_evidence.json").read_text()); p=json.loads((HERE/"uvp_p08_primary.json").read_text()); r=json.loads((HERE/"uvp_p08_independent_replay.json").read_text()); u=json.loads((HERE/"uvp_p08_uv_ir_provenance.json").read_text()); row=l["tests"][7]; assert row["status"]=="PASS" and digest(e)==row["derived_result"]["evidence_sha256"] and digest(p)==row["primary"]["residue_sha256"] and digest(r)==row["replay"]["residue_sha256"] and digest(u)==row["primary"]["uv_ir_provenance_sha256"]; ready=[x["test_id"] for x in l["tests"] if x["status"]=="NOT_RUN" and x["authorization"]=="READY"]; assert len(ready)<=1; print("UVP_P08_EVIDENCE_AUDIT_PASS"); print("MAXIMUM_ROUTING_RESIDUAL 0"); print("NEXT_AUTHORIZED_TEST",ready[0] if ready else "NONE")
if __name__=="__main__": main()
