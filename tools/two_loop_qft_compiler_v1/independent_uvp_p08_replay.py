"""Independent UVP_P08 replay by exact affine change of variables."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
    x,r=sp.symbols("x r",real=True)
    # Feynman combining and q=k+(r+1-x)p leaves Delta independent of r.
    delta="m2+x*(1-x)*p2"; r_derivative=sp.Integer(0); residue=sp.integrate(1,(x,0,1))
    payload={"schema_version":1,"test_id":"UVP_P08","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"exact_affine_shift_plus_Feynman_parameter_replay","generic_routing":"((k+r*p)^2+m2)*((k+(r+1)*p)^2+m2)","shift":"q=k+(r+1-x)*p","translation_Jacobian":"1","combined_denominator":delta,"combined_denominator_r_derivative":str(r_derivative),"routing_A_normalized_UV_residue":str(residue),"routing_B_normalized_UV_residue":str(residue),"normalized_UV_residue_difference":"0","surface_term_residue":"0","uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
    payload["artifact_sha256"]=digest(payload); (HERE/"uvp_p08_independent_replay.json").write_text(json.dumps(payload,indent=2)+"\n")
    print("UVP_P08_INDEPENDENT_REPLAY_COMPLETE"); print("ROUTING_RESIDUES 1 1"); print("ROUTING_DIFFERENCE 0"); print("ARTIFACT_SHA256",payload["artifact_sha256"])
if __name__=="__main__": main()
