"""Independent replay of the M03 implementation dependency audit."""
from hashlib import sha256
import ast,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CH="6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"; PH="54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def functions(path):
 tree=ast.parse(path.read_text()); return sorted(n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
def main():
 vertex_funcs=functions(HERE/"physical_vertex_api.py")
 scalar_funcs=functions(ROOT/"calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/compile_scalar_vertices.py")
 supplied=set(vertex_funcs+scalar_funcs)
 required_names={"enumerate_parent_scalar_one_loop_2pt","contract_all_V3_V3","contract_all_M2_V4","project_four_quadratic_poles"}
 absent=sorted(required_names-supplied)
 assert absent==sorted(required_names)
 inventory={"AST_scanned_modules":["physical_vertex_api.py","compile_scalar_vertices.py"],"available_function_count":len(supplied),"required_entry_points":sorted(required_names),"absent_entry_points":absent}
 p={"schema_version":1,"test_id":"UVP_M03","attempt":1,"contract_sha256":CH,"execution_plan_sha256":PH,"method":"independent_AST_API_surface_and_artifact_manifest_audit","inventory":inventory,"inventory_sha256":digest(inventory),"all_four_quadratic_directions_derived":False,"residue_values":None,"blocker_code":"M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING","classification":"IMPLEMENTATION_BLOCK_NOT_PHYSICS_FAIL","uv_ir":{"status":"NOT_EVALUATED","reason":"independent amplitude inventory cannot be constructed from promoted APIs"}}
 p["artifact_sha256"]=digest(p); (HERE/"uvp_m03_independent_blocker_replay.json").write_text(json.dumps(p,indent=2)+"\n"); print("UVP_M03_INDEPENDENT_BLOCKER_REPLAY_COMPLETE"); print("MISSING_ENTRY_POINTS",len(absent)); print("ARTIFACT_SHA256",p["artifact_sha256"])
if __name__=="__main__": main()
