"""Adjudicate UVP_P09 and advance the frozen ledger only on PASS."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent

def digest(x, field="artifact_sha256"):
    y = dict(x); y.pop(field, None)
    return sha256(json.dumps(y, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def load(name):
    x = json.loads((HERE / name).read_text())
    assert x["artifact_sha256"] == digest(x)
    return x

def main():
    p = load("uvp_p09_primary.json")
    r = load("uvp_p09_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text())
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text())
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    prior = deepcopy(ledger["tests"][:8])
    row = ledger["tests"][8]
    assert row["test_id"] == "UVP_P09" and row["authorization"] == "READY"
    assert all(x["status"] == "PASS" for x in prior)
    keys = ["exact_d_residual", "normalized_UV_pole_residual", "premature_d4_missed_finite", "uv_ir"]
    assert all(p[k] == r[k] for k in keys)
    assert p["exact_d_residual"] == p["normalized_UV_pole_residual"] == "0"
    provenance = {"schema_version": 1, "test_id": "UVP_P09", "classification": p["uv_ir"], "reason": "massive_IBP_primitive_has_UV_poles_but_no_IR_singularity"}
    provenance["artifact_sha256"] = digest(provenance)
    (HERE / "uvp_p09_uv_ir_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    evidence = {"schema_version": 1, "test_id": "UVP_P09", "attempt": 1, "contract_sha256": p["contract_sha256"], "execution_plan_sha256": p["execution_plan_sha256"], "primary": p, "independent_replay": r, "comparison": {"exact_d_IBP_residual": "0", "UV_pole_residual": "0", "premature_d4_missed_finite": p["premature_d4_missed_finite"]}, "uv_ir_classification": p["uv_ir"], "verdict": "PASS"}
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_p09_evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    row.update({"status": "PASS", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE", "method": p["method"], "inventory_sha256": None, "residue_sha256": p["artifact_sha256"], "uv_ir_provenance_sha256": provenance["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": r["method"], "inventory_sha256": None, "residue_sha256": r["artifact_sha256"], "uv_ir_provenance_sha256": provenance["artifact_sha256"]},
        "derived_result": {"exact_d_IBP_residual": "0", "maximum_residual": "0", "premature_d4_missed_finite": p["premature_d4_missed_finite"], "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": "exact_d_total_derivative_identity_and_independent_Gaussian_replay",
        "evidence_files": ["uvp_p09_primary.json", "uvp_p09_independent_replay.json", "uvp_p09_uv_ir_provenance.json", "uvp_p09_evidence.json"]})
    ledger["tests"][9]["authorization"] = "READY"
    ledger["counters"].update({"executed": 9, "passed": 9, "not_run_or_locked": 30, "engine_executed": 9, "engine_passed": 9})
    assert ledger["tests"][:8] == prior
    ledger.pop("result_sha256")
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    Draft202012Validator(schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    print("UVP_P09_PASS")
    print("EXACT_D_IBP_RESIDUAL 0")
    print("NEXT_TEST UVP_P10")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])

if __name__ == "__main__":
    main()
