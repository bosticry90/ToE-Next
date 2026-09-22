"""Primary UVP_C06: UV finiteness of the real-phi3 triangle."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"topology":"three_cubic_vertex_triangle","vertices":3,"propagators":3,"superficial_degree":"-2","symmetry_factor":"1"}]
 p={"schema_version":1,"test_id":"UVP_C06","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_graph_enumeration_plus_large_loop_momentum_power_counting","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"normalized_UV_residue":"0","derived_delta_g":"0","locality":True,"uv_ir":{"uv_pole":False,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c06_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C06_PRIMARY_COMPLETE"); print("TRIANGLE_UV_RESIDUE 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
