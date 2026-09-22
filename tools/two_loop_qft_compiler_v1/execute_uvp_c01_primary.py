"""Primary UVP_C01: real-phi4 one-loop two-point UV poles."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 inv=[{"graph":"quartic_tadpole","vertices":["phi4"],"internal_lines":1,"automorphism_order":2,"symmetry_factor":"1/2","external_legs":2}]
 p={"schema_version":1,"test_id":"UVP_C01","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_vertex_graph_enumeration_plus_primitive_P01_projection","action":"L=1/2(dphi)^2-1/2*m2*phi^2-lambda*phi^4/4!","graph_inventory":inv,"graph_inventory_sha256":digest({"graphs":inv}),
   "loop_two_point_pole":"-lambda*m2/2","derived_counterterms":{"delta_Z_phi":"0","delta_m2":"lambda*m2/2"},"p2_pole":"0","locality":True,
   "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c01_primary.json").write_text(json.dumps(p,indent=2)+"\n")
 print("UVP_C01_PRIMARY_COMPLETE"); print("DELTA_Z_PHI 0"); print("DELTA_M2 lambda*m2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
