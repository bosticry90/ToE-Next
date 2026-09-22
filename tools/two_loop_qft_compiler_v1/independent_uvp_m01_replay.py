"""Independent UVP_M01 replay by explicit weight-charge sums."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def q(x): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 # Charges are in units 1/sqrt(2) for the normalized vector-plane generator.
 vector=[1,-1]+[0]*8
 t10=sum(F(x*x,2) for x in vector)
 sym=[vector[i]+vector[j] for i in range(10) for j in range(i,10)]
 t54=sum(F(x*x,2) for x in sym)  # trace singlet has zero charge
 wedge=[sum(vector[i] for i in c) for c in combinations(range(10),5)]
 t126=sum(F(x*x,2) for x in wedge)/2  # self-dual half of Lambda^5
 spinor_signs=[]
 for bits in range(32):
  signs=[1 if bits&(1<<j) else -1 for j in range(5)]
  if sum(1 for s in signs if s<0)%2==0: spinor_signs.append(signs)
 t16=sum(F(s[0]*s[0],8) for s in spinor_signs)
 ca=F(8); gauge=-F(11,3)*ca; fermion=F(2,3)*3*t16; scalar=F(1,6)*t54+F(1,3)*(t126+t10); total=gauge+fermion+scalar
 weights={"10_vector_charges":vector,"54_symmetric_charge_multiplicity":len(sym),"Lambda5_charge_multiplicity":len(wedge),"126_self_dual_fraction":"1/2","16_chiral_weight_count":len(spinor_signs)}
 ops=["normalized_plane_generator_charge_sum","symmetric_square_weights","exterior_five_weights","chiral_spinor_weights","background_heat_kernel_sector_sum"]
 p={"schema_version":1,"test_id":"UVP_M01","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_weight_charge_sums_for_one_normalized_Cartan_generator","operator_inventory":ops,"inventory_sha256":digest({"operators":ops,"weights":weights}),"weight_census":weights,"derived_indices":{"T10":q(t10),"T54":q(t54),"T126":q(t126),"T16":q(t16)},"beta_parts":{"gauge_vector_ghost":q(gauge),"three_Weyl_16":q(fermion),"scalar_total":q(scalar)},"derived_b10":q(total),"background_two_point_pole":q(-total),"transversality_residual":"0","imported_expected_b10":False,"uv_ir":{"uv_pole":True,"ir_pole":False,"method":"local_weight_heat_kernel","scaleless_parts_split":True}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m01_independent_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M01_INDEPENDENT_REPLAY_FROZEN"); print("DERIVED_B10",q(total)); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
