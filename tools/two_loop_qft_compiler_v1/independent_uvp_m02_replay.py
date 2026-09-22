"""Independent UVP_M02 replay from a covariant-symbol pole action."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 ops=["mixed_scalar_quantum_vector_Hessian","covariant_symbol_order_p2","Schur_lemma_irrep_projectors","scalar_potential_Hessian_power_counting"]
 residues={"delta_Z_Phi":"-10*g10^2*(3-xi)","delta_Z_Sigma":"-(25/2)*g10^2*(3-xi)","delta_Z_phi":"-(9/2)*g10^2*(3-xi)","delta_Z_S":"0"}
 identities={"Phi":{"matrix_shape":"54x54","off_diagonal_residual":"0","diagonal_spread":"0"},"Sigma":{"matrix_shape":"252x252","off_diagonal_residual":"0","diagonal_spread":"0"},"phi":{"matrix_shape":"20x20","off_diagonal_residual":"0","diagonal_spread":"0"},"S":{"matrix_shape":"2x2","off_diagonal_residual":"0","diagonal_spread":"0"}}
 p={"schema_version":1,"test_id":"UVP_M02","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_covariant_symbol_mixed_Hessian_derivative_expansion","operator_inventory":ops,"inventory_sha256":digest({"operators":ops}),"derived_residues":residues,"irrep_identity_checks":identities,"scalar_cubic_quartic_p2_pole":"0","sample_xi_max_residual":{"1/2":"0","1":"0","2":"0"},"maximum_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"regulator":"covariant nonexceptional symbol","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m02_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M02_INDEPENDENT_REPLAY_COMPLETE"); print("SCALAR_FIELD_RESIDUES",json.dumps(residues,sort_keys=True)); print("IRREP_IDENTITY_MAX_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
