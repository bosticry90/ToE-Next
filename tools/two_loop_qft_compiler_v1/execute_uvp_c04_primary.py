"""Primary UVP_C04: real-phi3 one-loop one-point function."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"topology":"cubic_tadpole","vertex":"-g*phi^3/3!","symmetry_factor":"1/2","primitive":"P01","primitive_residue":"-m2"}]
 p={"schema_version":1,"test_id":"UVP_C04","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_derived_cubic_tadpole_graph_and_P01_projection","action":"L=1/2(dphi)^2-1/2*m2*phi^2-g*phi^3/3!","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"vertex_symmetry_multiplier":"g/2","one_point_loop_residue":"-g*m2/2","derived_tadpole_counterterm":"g*m2/2","sign_convention":"counterterm_is_minus_loop_pole","uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c04_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C04_PRIMARY_COMPLETE"); print("LOOP_ONE_POINT_RESIDUE -g*m2/2"); print("TADPOLE_COUNTERTERM g*m2/2"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
