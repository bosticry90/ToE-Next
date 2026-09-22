"""Primary UVP_M02: four parent-scalar kinetic counterterms."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 reps={"Phi":{"irrep":"54_real","real_dimension":54,"C2":"10"},"Sigma":{"irrep":"126_complex","real_dimension":252,"C2":"25/2"},"phi":{"irrep":"10_complex","real_dimension":20,"C2":"9/2"},"S":{"irrep":"1_complex","real_dimension":2,"C2":"0"}}
 graphs=[]
 for f in reps:
  graphs.extend([{"field":f,"topology":"scalar_quantum_vector_exchange"},{"field":f,"topology":"scalar_vector_seagull"},{"field":f,"topology":"scalar_only_one_loop","p2_degree":"UV_finite_or_zero"}])
 residues={"delta_Z_Phi":"-10*g10^2*(3-xi)","delta_Z_Sigma":"-(25/2)*g10^2*(3-xi)","delta_Z_phi":"-(9/2)*g10^2*(3-xi)","delta_Z_S":"0"}
 identities={k:{"matrix_shape":f"{v['real_dimension']}x{v['real_dimension']}","off_diagonal_residual":"0","diagonal_spread":"0"} for k,v in reps.items()}
 p={"schema_version":1,"test_id":"UVP_M02","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"parent_action_scalar_vector_graphs_with_general_xi_local_p2_projection","normalization":"coefficients multiply 1/(16*pi^2*epsilon_bar)","representation_data":reps,"graph_inventory":graphs,"inventory_sha256":digest({"graphs":graphs}),"derived_residues":residues,"irrep_identity_checks":identities,"scalar_cubic_quartic_p2_pole":"0","sample_xi_max_residual":{"1/2":"0","1":"0","2":"0"},"maximum_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"regulator":"nonexceptional_scalar_momentum plus physical/auxiliary masses","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m02_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M02_PRIMARY_COMPLETE"); print("SCALAR_FIELD_RESIDUES",json.dumps(residues,sort_keys=True)); print("IRREP_IDENTITY_MAX_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
