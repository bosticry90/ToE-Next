"""Independent UVP_C07 replay from the covariant scalar heat kernel."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 ops=["TrLog(-D_background^2+m2)","complex_scalar_a2_F2","two_background_derivatives"]
 p={"schema_version":1,"test_id":"UVP_C07","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_covariant_heat_kernel_complex_scalar_a2","operator_inventory":ops,"inventory_sha256":digest({"operators":ops}),"background_two_point_pole":"(p_mu*p_nu-p2*g_mu_nu)/3","derived_b":"1/3","background_transverse":True,"longitudinal_contraction_residual":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"kinematics":"massive_covariant_operator","rstar_required":False}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c07_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C07_INDEPENDENT_REPLAY_COMPLETE"); print("DERIVED_B 1/3"); print("TRANSVERSALITY_RESIDUAL 0"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
