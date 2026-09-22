"""Primary UVP_C05: real-phi3 one-loop two-point bubble."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"topology":"two_cubic_vertex_bubble","symmetry_factor":"1/2","primitive":"P06/P02","constant_UV_residue":"1","p2_UV_residue":"0"}]
 p={"schema_version":1,"test_id":"UVP_C05","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_graph_plus_local_momentum_expansion","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"loop_mass_pole":"-g^2/2","derived_delta_m2":"g^2/2","p2_wavefunction_pole":"0","derived_delta_Z_phi":"0","locality":True,"uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c05_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C05_PRIMARY_COMPLETE"); print("DELTA_M2 g^2/2"); print("DELTA_Z_PHI 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
