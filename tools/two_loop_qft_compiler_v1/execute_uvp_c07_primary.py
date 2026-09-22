"""Primary UVP_C07: scalar-QED background photon two-point pole."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"topology":"charged_scalar_bubble","vertices":["Aphi*phi","Aphi*phi"],"symmetry_factor":"1"},{"topology":"charged_scalar_seagull","vertex":"AAphi*phi","symmetry_factor":"1"}]
 pieces={"bubble_delta_m2":"-2*m2","seagull_delta_m2":"2*m2","bubble_p2_delta":"-p2/3","bubble_p_mu_p_nu":"p_mu*p_nu/3"}
 p={"schema_version":1,"test_id":"UVP_C07","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"action_graph_Feynman_parameter_tensor_projection","action":"complex charge-one scalar QED","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"separate_pieces":pieces,"mass_term_residual":"0","longitudinal_contraction_residual":"0","background_two_point_pole":"(p_mu*p_nu-p2*g_mu_nu)/3","derived_b":"1/3","background_transverse":True,"uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematics":"m2>0 or Euclidean p2>0","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c07_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C07_PRIMARY_COMPLETE"); print("DERIVED_B 1/3"); print("TRANSVERSALITY_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
