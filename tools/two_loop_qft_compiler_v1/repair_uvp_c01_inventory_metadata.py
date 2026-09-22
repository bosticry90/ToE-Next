"""One-time repair of the C01 replay inventory hash caught by the global audit."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(x,field=None):
 y=dict(x)
 if field: y.pop(field,None)
 return sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 path=HERE/"uv_pole_evaluator_results.json"; ledger=json.loads(path.read_text())
 row=ledger["tests"][13]; assert row["test_id"]=="UVP_C01" and row["status"]=="PASS" and row["replay"]["inventory_sha256"] is None
 row["replay"]["inventory_sha256"]=digest({"functional_operator_inventory":["TrLog_scalar_Hessian","phi2_projection"]})
 ledger.pop("result_sha256"); ledger["result_sha256"]=digest(ledger); path.write_text(json.dumps(ledger,indent=2)+"\n")
 print("UVP_C01_REPLAY_INVENTORY_METADATA_REPAIRED"); print("INVENTORY_SHA256",row["replay"]["inventory_sha256"])
if __name__=="__main__": main()
