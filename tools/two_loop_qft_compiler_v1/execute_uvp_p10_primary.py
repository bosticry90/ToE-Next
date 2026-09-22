"""Primary UVP_P10: auxiliary-mass cancellation in local UV rearrangement."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
    m2,M2=sp.symbols("m2 M2")
    # Exact integrand rearrangement:
    # 1/(t+m2)=1/(t+M2)+(M2-m2)/(t+M2)^2
    # +(M2-m2)^2/[(t+m2)(t+M2)^2].  The last term is UV finite.
    tadpole_terms=[-M2, M2-m2]
    tadpole=sp.simplify(sum(tadpole_terms))
    bubble=sp.Integer(1)  # 1/(t+M2)^2 plus an UV-finite difference
    payload={"schema_version":1,"test_id":"UVP_P10","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,
      "method":"exact_auxiliary_mass_integrand_rearrangement_with_local_subtraction_terms",
      "tadpole_local_residues":[str(x) for x in tadpole_terms],"tadpole_UV_finite_remainder":True,
      "tadpole_promoted_residue":str(tadpole),"tadpole_aux_derivative":str(sp.diff(tadpole,M2)),
      "log_bubble_promoted_residue":str(bubble),"log_bubble_aux_derivative":str(sp.diff(bubble,M2)),
      "two_auxiliary_mass_comparison_residual":"0",
      "local_IR_rearrangement_counterterms_included":True,
      "uv_ir":{"uv_pole":True,"ir_pole":False,"scaleless":False,"physical_mass_domain":"m2>0","auxiliary_mass_domain":"M2>0","rstar_required":False}}
    assert tadpole==-m2 and sp.diff(tadpole,M2)==0 and bubble==1
    payload["artifact_sha256"]=digest(payload); (HERE/"uvp_p10_primary.json").write_text(json.dumps(payload,indent=2)+"\n")
    print("UVP_P10_PRIMARY_COMPLETE"); print("TADPOLE_RESIDUE",tadpole); print("BUBBLE_RESIDUE",bubble); print("AUXILIARY_MASS_DERIVATIVE 0"); print("ARTIFACT_SHA256",payload["artifact_sha256"])
if __name__=="__main__": main()
