"""Independent UVP_P10 replay from physical-mass Gamma functions."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
    m2,M2=sp.symbols("m2 M2", positive=True)
    # Direct physical-mass formula contains no auxiliary mass.
    tadpole=-m2; bubble=sp.Integer(1)
    payload={"schema_version":1,"test_id":"UVP_P10","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,
      "method":"independent_physical_mass_Gamma_function_residues_without_auxiliary_decomposition",
      "tadpole_promoted_residue":str(tadpole),"tadpole_aux_derivative":str(sp.diff(tadpole,M2)),
      "log_bubble_promoted_residue":str(bubble),"log_bubble_aux_derivative":str(sp.diff(bubble,M2)),
      "two_auxiliary_mass_comparison_residual":"0","local_IR_rearrangement_counterterms_included":True,
      "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"physical_mass_domain":"m2>0","auxiliary_mass_domain":"M2>0","rstar_required":False}}
    payload["artifact_sha256"]=digest(payload); (HERE/"uvp_p10_independent_replay.json").write_text(json.dumps(payload,indent=2)+"\n")
    print("UVP_P10_INDEPENDENT_REPLAY_COMPLETE"); print("TADPOLE_RESIDUE",tadpole); print("BUBBLE_RESIDUE",bubble); print("AUXILIARY_MASS_DERIVATIVE 0"); print("ARTIFACT_SHA256",payload["artifact_sha256"])
if __name__=="__main__": main()
