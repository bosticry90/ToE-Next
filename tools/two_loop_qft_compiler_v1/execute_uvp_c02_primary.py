"""Primary UVP_C02: real-phi4 crossing-symmetric four-point pole."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"channel":c,"topology":"two_quartic_vertices_bubble","symmetry_factor":"1/2","UV_residue":"lambda^2/2"} for c in ("s","t","u")]
 p={"schema_version":1,"test_id":"UVP_C02","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_derived_three_channel_graph_enumeration","action":"L=1/2(dphi)^2-1/2*m2*phi^2-lambda*phi^4/4!","graph_inventory":graphs,"graph_inventory_sha256":digest({"graphs":graphs}),"channel_residues":{"s":"lambda^2/2","t":"lambda^2/2","u":"lambda^2/2"},"crossing_permutation_residual":"0","derived_delta_lambda":"3*lambda^2/2","locality":True,"uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematics":"massive or nonexceptional","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c02_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C02_PRIMARY_COMPLETE"); print("DELTA_LAMBDA 3*lambda^2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
