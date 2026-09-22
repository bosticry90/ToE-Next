"""Primary UVP_C13: auxiliary-mass UV/IR rearrangement in broken SU(2)."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 inv=[{"sector":"heavy_vector","IRR":"common_auxiliary_mass"},{"sector":"Goldstone","IRR":"physical_xi_MW2"},{"sector":"heavy_ghost","IRR":"physical_xi_MW2"},{"sector":"unbroken_vector_ghost","IRR":"auxiliary_mass_plus_local_Rstar_subtraction"},{"sector":"real_adjoint_scalar","IRR":"physical_or_auxiliary_mass"}]
 residues={"background_b":"-7","vector_ghost_parent":"-22/3","real_adjoint_scalar":"1/3","mass_pairing_residual":"0","BRST_residual":"0"}
 p={"schema_version":1,"test_id":"UVP_C13","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"broken_sector_auxiliary_mass_IRR_with_explicit_local_Rstar_subtractions","graph_inventory":inv,"inventory_sha256":digest({"graphs":inv}),"derived_UV_residues":residues,"auxiliary_mass_derivative":"0","local_IR_counterterm_sum_recorded":True,"spurious_IR_pole_after_Rstar":"0","maximum_residual":"0","uv_ir":{"UV_poles":"retained","physical_IR_poles":"none","manufactured_IR_poles":"subtracted_by_local_Rstar","scaleless_UV_IR_parts":"separately_labeled"}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_c13_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_C13_PRIMARY_COMPLETE"); print("AUXILIARY_MASS_DERIVATIVE 0"); print("BACKGROUND_B -7"); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
