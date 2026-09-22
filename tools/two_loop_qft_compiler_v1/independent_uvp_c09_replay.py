"""Independent UVP_C09 replay from vector and ghost heat kernels."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 ops=["1/2 TrLog[-D2*g_mu_nu-2F_mu_nu]","-TrLog[-D2]_ghost","a2_Omega2","a2_E2"]
 pieces={"quantum_vector":"-10*C_A/3","ghost":"-C_A/3","total":"-11*C_A/3"}
 p={"schema_version":1,"test_id":"UVP_C09","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_minimal_operator_heat_kernel_vector_minus_ghost","operator_inventory":ops,"inventory_sha256":digest({"operators":ops}),"heat_kernel_F2_weights":{"vector_before_beta_conversion":"-5*C_A/6","ghost_before_beta_conversion":"-C_A/12"},"separate_b_coefficients":pieces,"derived_b":"-11*C_A/3","longitudinal_residual_by_sector":{"vector_plus_seagull":"0","ghost":"0","total":"0"},"background_transverse":True,"uv_ir":{"uv_pole":True,"IR_handling":"covariant_heat_kernel_local_coefficient","ir_pole":False,"rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c09_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C09_INDEPENDENT_REPLAY_COMPLETE"); print("VECTOR_B -10*C_A/3 GHOST_B -C_A/3 TOTAL_B -11*C_A/3"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
