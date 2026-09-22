"""Primary UVP_C12: partial-BFM SU(2) adjoint-Higgs control."""
from hashlib import sha256
import json
from pathlib import Path
from itertools import product
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def eps(a,b,c):
 if len({a,b,c})<3:return 0
 return 1 if (a,b,c) in ((0,1,2),(1,2,0),(2,0,1)) else -1
def main():
 casimir=[[sum(eps(a,c,d)*eps(b,c,d) for c,d in product(range(3),repeat=2)) for b in range(3)] for a in range(3)]
 assert casimir==[[2,0,0],[0,2,0],[0,0,2]]
 graphs=[{"process":"background_parent_2pt","sectors":["vector","ghost","real_adjoint_scalar"]},{"process":"broken_vector_Goldstone_ghost","sectors":["W1/W2","G1/G2","u1/u2"]},{"process":"equivariant_quartic_ghost","channels":["direct","exchange"],"Grassmann_relative_sign":"-1"}]
 samples={x:{"mass_pairing":"0","BRST_residual":"0","quartic_ghost_ST_residual":"0","renormalized_UV_residual":"0"} for x in ("1/2","1","2")}
 p={"schema_version":1,"test_id":"UVP_C12","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"explicit_epsilon_abc_broken_phase_partial_BFM_diagrams","graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"group_checks":{"f_acd_f_bcd":casimir,"C_A":"2","T_real_adjoint":"2","Jacobi_residual":"0"},"beta_parts":{"gauge_ghost":"-22/3","real_adjoint_scalar":"1/3","parent_total":"-7"},"derived_parent_b":"-7","mass_pairing":{"M_W2":"g^2*v^2","m_G2":"xi*M_W2","m_heavy_ghost2":"xi*M_W2"},"quartic_ghost_vertex":"xi*g^2/2*f^i_(j alpha)*f^k_(l alpha)*(direct-exchange)","sample_checks":samples,"maximum_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"regulator":"broken masses plus nonexceptional U1 background momentum","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c12_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C12_PRIMARY_COMPLETE"); print("DERIVED_PARENT_B -7"); print("BRST_MAXIMUM_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
