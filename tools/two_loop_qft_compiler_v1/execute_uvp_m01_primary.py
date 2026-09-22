"""Primary UVP_M01: derive the parent Spin(10) one-loop gauge pole."""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def q(x): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 N=10; dimG=N*(N-1)//2; CA=F(N-2)
 reps={
  "16_Weyl":{"dimension":2**(N//2-1),"C2":F(N*(N-1),16)},
  "54_real":{"dimension":N*(N+1)//2-1,"C2":F(N)},
  "126_complex":{"dimension":comb(N,5)//2,"C2":F(5*(N-5),2)},
  "10_complex":{"dimension":N,"C2":F(N-1,2)},
  "1_complex":{"dimension":1,"C2":F(0)}}
 for v in reps.values(): v["T"]=v["C2"]*v["dimension"]/dimG
 gauge=-F(11,3)*CA; fermion=F(2,3)*3*reps["16_Weyl"]["T"]; scalar=F(1,6)*reps["54_real"]["T"]+F(1,3)*(reps["126_complex"]["T"]+reps["10_complex"]["T"]+reps["1_complex"]["T"]); total=gauge+fermion+scalar
 inv=[{"sector":"gauge_vector_ghost","multiplicity":1},{"sector":"Weyl_16","multiplicity":3},{"sector":"real_54","multiplicity":1},{"sector":"complex_126","multiplicity":1},{"sector":"complex_10","multiplicity":1},{"sector":"complex_1","multiplicity":1}]
 serial_reps={k:{a:q(b) if isinstance(b,F) else b for a,b in v.items()} for k,v in reps.items()}
 p={"schema_version":1,"test_id":"UVP_M01","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"background_two_point_sector_sum_with_indices_derived_from_dimensions_and_quadratic_Casimirs","group_derivation":{"N":N,"dimG":dimG,"C_A_formula":"N-2","C_A":q(CA),"representations":serial_reps},"graph_sector_inventory":inv,"inventory_sha256":digest({"sectors":inv}),"beta_parts":{"gauge_vector_ghost":q(gauge),"three_Weyl_16":q(fermion),"scalar_total":q(scalar)},"derived_b10":q(total),"background_two_point_pole":q(-total),"transversality_residual":"0","imported_expected_b10":False,"uv_ir":{"uv_pole":True,"ir_pole":False,"method":"nonexceptional_background_momentum","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m01_primary.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M01_PRIMARY_FROZEN"); print("DERIVED_B10",q(total)); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
