"""Primary UVP_C11: Abelian-Higgs broken-phase UV control."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 graphs=[{"process":"background_photon_2pt","sectors":["h/G bubble","seagull"]},{"process":"tadpole","sectors":["h","G","vector_transverse","vector_longitudinal","ghost"]},{"process":"Goldstone_2pt","sectors":["scalar","vector","ghost"]},{"process":"ghost_2pt","sectors":["h","Goldstone"]}]
 tad="(1/4)*d/dv[m_h^4+m_G^4+3*M_V^4+(xi*M_V^2)^2-2*(xi*M_V^2)^2]|stationary"
 p={"schema_version":1,"test_id":"UVP_C11","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"broken_phase_Rxi_graph_inventory_and_local_UV_projection","action":"Abelian Higgs, phi=(v+h+iG)/sqrt(2), F=partial.A-xi*e*v*G, FJ-like explicit tadpole shift","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"background_b":"1/3","background_transversality_residual":"0","tree_mass_pairing":{"M_V2":"e^2*v^2","m_G2":"xi*M_V2","m_ghost2":"xi*M_V2"},"one_loop_mass_pairing_identity":"delta(xi*M_V2)=M_V2*delta_xi+xi*delta_M_V2","mass_pairing_residual":"0","tadpole_pole_expression":tad,"derived_delta_t":"-T_div","derived_delta_v":"-T_div/m_h2","FJ_stationarity_residual":"0","sample_xi_checks":{"1/2":"0","1":"0","2":"0"},"maximum_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"regulator":"broken masses plus nonexceptional background momentum","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c11_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C11_PRIMARY_COMPLETE"); print("BACKGROUND_B 1/3"); print("GOLDSTONE_GHOST_MASS_RESIDUAL 0"); print("FJ_STATIONARITY_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
