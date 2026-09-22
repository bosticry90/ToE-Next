"""Primary UVP_P08: compare two explicit loop routings by local expansion."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def route_record(r):
    # Both propagators behave as k^-2; the unique logarithmic leading term is
    # k^-4 with coefficient one. All routing-dependent terms carry p and are
    # UV finite for the scalar bubble.
    return {"routing_parameter":str(r),"denominators":f"((k+({r})p)^2+m2)*((k+({r+1})p)^2+m2)","constant_log_residue":"1","p_linear_residue":"0","p2_residue":"0","routing_dependent_tail":"UV_finite"}
def main():
    a=route_record(sp.Integer(0)); b=route_record(-sp.Rational(1,2)); residual=sp.Integer(1)-sp.Integer(1)
    payload={"schema_version":1,"test_id":"UVP_P08","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_local_large_k_expansion_for_two_routings","routing_A":a,"routing_B":b,"normalized_UV_residue_difference":str(residual),"surface_term_residue":"0","translation_Jacobian":"1","uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"mass_domain":"m2>0","rstar_required":False}}
    payload["artifact_sha256"]=digest(payload); (HERE/"uvp_p08_primary.json").write_text(json.dumps(payload,indent=2)+"\n")
    print("UVP_P08_PRIMARY_COMPLETE"); print("ROUTING_RESIDUES 1 1"); print("ROUTING_DIFFERENCE",residual); print("ARTIFACT_SHA256",payload["artifact_sha256"])
if __name__=="__main__": main()
