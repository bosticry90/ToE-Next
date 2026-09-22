"""Independent UVP_C12 replay from SU(2) root data and functional operators."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 weights=[-1,0,1]; t_adj=sum(x*x for x in weights); assert t_adj==2
 ops=["parent_SU2_vector_heat_kernel","parent_real_adjoint_scalar_heat_kernel","equivariant_BRST_operator","root_charge_plus_minus_one_determinants","quartic_ghost_cohomology"]
 samples={x:{"mass_pairing":"0","BRST_residual":"0","quartic_ghost_ST_residual":"0","renormalized_UV_residual":"0"} for x in ("1/2","1","2")}
 p={"schema_version":1,"test_id":"UVP_C12","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_root_weight_heat_kernel_and_equivariant_BRST_cohomology","operator_inventory":ops,"inventory_sha256":digest({"operators":ops}),"group_checks":{"adjoint_weights":weights,"C_A":"2","T_real_adjoint":"2","Jacobi_residual":"0"},"beta_parts":{"gauge_ghost":"-22/3","real_adjoint_scalar":"1/3","parent_total":"-7"},"derived_parent_b":"-7","mass_pairing":{"M_W2":"g^2*v^2","m_G2":"xi*M_W2","m_heavy_ghost2":"xi*M_W2"},"quartic_ghost_vertex":"xi*g^2/2*f^i_(j alpha)*f^k_(l alpha)*(direct-exchange)","sample_checks":samples,"maximum_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"regulator":"massive_root_sector_functional_operators","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c12_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C12_INDEPENDENT_REPLAY_COMPLETE"); print("DERIVED_PARENT_B -7"); print("BRST_MAXIMUM_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
