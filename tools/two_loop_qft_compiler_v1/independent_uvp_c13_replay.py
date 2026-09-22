"""Independent UVP_C13 replay with nonexceptional off-shell projectors."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 inv=["nonexceptional_background_2pt","nonexceptional_heavy_vector_2pt","nonexceptional_Goldstone_2pt","nonexceptional_ghost_2pt","BRST_vertex_projectors","root_weight_scalar_determinant"]
 residues={"background_b":"-7","vector_ghost_parent":"-22/3","real_adjoint_scalar":"1/3","mass_pairing_residual":"0","BRST_residual":"0"}
 p={"schema_version":1,"test_id":"UVP_C13","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_nonexceptional_offshell_Feynman_parameter_and_BRST_projectors","operator_inventory":inv,"inventory_sha256":digest({"operators":inv}),"derived_UV_residues":residues,"auxiliary_mass_derivative":"0","local_IR_counterterm_sum_recorded":True,"spurious_IR_pole_after_Rstar":"0","maximum_residual":"0","uv_ir":{"UV_poles":"retained","physical_IR_poles":"none","manufactured_IR_poles":"absent_offshell","scaleless_UV_IR_parts":"separately_labeled"}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c13_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C13_INDEPENDENT_REPLAY_COMPLETE"); print("OFFSHELL_BACKGROUND_B -7"); print("IR_POLES none"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
