"""Fail-closed M03 capability audit for the four parent quadratic poles."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PARENT=ROOT/"calculations/canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md"
PARENT_HASH="01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 assert sha256(PARENT.read_bytes()).hexdigest()==PARENT_HASH
 oracle=json.loads((ROOT/"calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/scalar_vertex_oracle.json").read_text())
 contract=json.loads((HERE/"layer5_counterterm_contract.json").read_text())
 assert oracle["outcome"]=="SCALAR_VERTEX_ORACLE_PASS" and "one_loop_counterterms" in oracle["not_supplied"]
 assert contract["all_slot_pole_residues_derived"] is False and "delta_parent_quadratic_4" in contract["missing_required_one_loop_residues"]
 required=[
  "complete parent-origin V3_ACD contraction V3_BCD over 328 real fields",
  "complete parent-origin V4_ABCD contraction with the four quadratic mass operators",
  "gauge/Goldstone/ghost scalar two-point constant-pole assembly in the frozen partial-BFM scheme",
  "projection onto mPhi2,mSigma2,mphi2,mS2 after M02 field residues",
 ]
 available=["on-demand selected directional scalar derivatives","physical-basis sparse vertex queries","two-loop background-F2 species inventory","M02 universal p2 residues"]
 missing=["exhaustive parent scalar two-point one-loop inventory","exact summed V3/V4 contraction backend","quadratic pole projector with gauge-sector completion"]
 inventory={"targets":["mPhi2","mSigma2","mphi2","mS2"],"required_contractions":required,"available_surfaces":available,"missing_capabilities":missing}
 p={"schema_version":1,"test_id":"UVP_M03","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"primary_capability_audit_before_residue_materialization","parent_action_sha256":PARENT_HASH,"inventory":inventory,"inventory_sha256":digest(inventory),"attempted_formula":"R_AB=(1/4)*d_A*d_B Tr[H_scalar(q)^2]+gauge_Goldstone_ghost_poles-field_CT_contribution","all_four_quadratic_directions_derived":False,"residue_values":None,"blocker_code":"M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING","classification":"IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL","uv_ir":{"status":"NOT_EVALUATED","reason":"1PI amplitudes not materialized"}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m03_primary_blocker.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M03_PRIMARY_BLOCKED"); print("BLOCKER",p["blocker_code"]); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
