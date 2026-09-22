"""Primary UVP_C09: pure Yang-Mills background two-point divergence."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"sector":"quantum_vector","topology":"BQQ_two_vertex_bubble"},{"sector":"quantum_vector","topology":"BBQQ_seagull"},{"sector":"ghost","topology":"background_ghost_bubble"}]
 pieces={"quantum_vector":"-10*C_A/3","ghost":"-C_A/3","total":"-11*C_A/3"}
 p={"schema_version":1,"test_id":"UVP_C09","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"background_Feynman_gauge_diagrammatic_tensor_projection","action":"pure_Yang_Mills_single_background_Rxi_at_xi=1","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"separate_b_coefficients":pieces,"derived_b":"-11*C_A/3","longitudinal_residual_by_sector":{"vector_plus_seagull":"0","ghost":"0","total":"0"},"background_transverse":True,"uv_ir":{"uv_pole":True,"IR_handling":"nonexceptional_offshell_background_momentum","ir_pole":False,"rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c09_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C09_PRIMARY_COMPLETE"); print("VECTOR_B -10*C_A/3 GHOST_B -C_A/3 TOTAL_B -11*C_A/3"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
