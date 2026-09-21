"""Adjudicate UVP_P03 and advance only to P04 on exact three-way agreement."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import sympy as sp


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def canonical_hash(payload, hash_field="artifact_sha256"):
    work = dict(payload)
    work.pop(hash_field, None)
    return sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload["artifact_sha256"] == canonical_hash(payload)
    assert payload["contract_sha256"] == CONTRACT_HASH
    assert payload["execution_plan_sha256"] == PLAN_HASH
    return payload


def main():
    primary = load_verified("uvp_p03_primary.json")
    replay = load_verified("uvp_p03_independent_replay.json")
    derivative = load_verified("uvp_p03_p01_derivative_relation.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    evidence_schema = json.loads((HERE / "uvp_p03_evidence_schema.json").read_text(
        encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)

    prior_rows = deepcopy(ledger["tests"][:2])
    row = ledger["tests"][2]
    assert [item["status"] for item in prior_rows] == ["PASS", "PASS"]
    assert row["test_id"] == "UVP_P03"
    assert row["status"] == "NOT_RUN" and row["authorization"] == "READY"
    assert row["attempt"] == 0 and ledger["counters"]["executed"] == 2
    assert all(test["status"] not in {"PASS", "BLOCKED", "FAIL", "RUNNING"}
               for test in ledger["tests"][3:])

    p = sp.sympify(primary["normalized_residue"])
    r = sp.sympify(replay["normalized_residue"])
    d = sp.sympify(derivative["normalized_derivative_prediction"])
    p_minus_r = sp.simplify(p - r)
    p_minus_d = sp.simplify(p - d)
    r_minus_d = sp.simplify(r - d)
    passed = (
        p_minus_r == 0 and p_minus_d == 0 and r_minus_d == 0
        and derivative["integrand_relation_residual"] == "0"
        and primary["pole_expression"] == replay["pole_expression"]
        == derivative["pole_expression"]
        and primary["uv_ir"] == replay["uv_ir"]
        and primary["remainder_after_radialization"]
        == "O(t^-2-epsilon)_UV_finite"
    )
    if not passed:
        raise AssertionError("UVP_P03 three-way consistency failed")

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_P03",
        "mass_domain": "m2>0",
        "classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "reason": (
            "positive_mass_removes_IR_singularity; direct_auxiliary_master_"
            "contains_the_log_UV_pole_and_the_exact_remainder_is_UV_finite"
        ),
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p03_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")

    evidence = {
        "schema_version": 1,
        "test_id": "UVP_P03",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "convention": {
            "dimension": "d=4-2*epsilon",
            "p01_integral": (
                "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d*"
                "(+i)/(k^2-m2+i0)]"
            ),
            "p03_integral": (
                "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d*"
                "(-i)/(k^2-m2+i0)^2]"
            ),
            "integrand_identity": "P03_integrand=-d(P01_integrand)/d(m2)",
            "pole_identity": "P03_pole=-d(P01_pole)/d(m2)",
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "mass_domain": "m2>0",
        },
        "primary": primary,
        "independent_replay": replay,
        "p01_derivative_relation": derivative,
        "three_way_comparison": {
            "primary_minus_replay": str(p_minus_r),
            "primary_minus_p01_derivative": str(p_minus_d),
            "replay_minus_p01_derivative": str(r_minus_d),
            "pole_expressions_equal": True,
        },
        "uv_ir_classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = canonical_hash(evidence)
    Draft202012Validator.check_schema(evidence_schema)
    Draft202012Validator(evidence_schema).validate(evidence)
    (HERE / "uvp_p03_evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    row.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 1,
        "primary": {
            "state": "COMPLETE", "method": primary["method"],
            "inventory_sha256": None,
            "residue_sha256": primary["artifact_sha256"],
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "replay": {
            "state": "COMPLETE", "method": replay["method"],
            "inventory_sha256": None,
            "residue_sha256": replay["artifact_sha256"],
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "derived_result": {
            "normalized_residue": primary["normalized_residue"],
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "pole_expression": primary["pole_expression"],
            "primary_minus_replay": str(p_minus_r),
            "primary_minus_p01_derivative": str(p_minus_d),
            "replay_minus_p01_derivative": str(r_minus_d),
            "p01_evidence_sha256": derivative["frozen_p01_evidence_sha256"],
            "derivative_relation_sha256": derivative["artifact_sha256"],
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "direct_doubled_line_projection_equals_independent_Gamma_replay_"
            "and_minus_mass_derivative_of_frozen_P01_pole_exactly"
        ),
        "evidence_files": [
            "uvp_p03_primary.json", "uvp_p03_independent_replay.json",
            "uvp_p03_p01_derivative_relation.json",
            "uvp_p03_uv_ir_provenance.json", "uvp_p03_evidence.json",
        ],
    })
    ledger["tests"][3]["authorization"] = "READY"
    ledger["counters"].update({
        "executed": 3, "passed": 3, "not_run_or_locked": 36,
        "engine_executed": 3, "engine_passed": 3,
    })
    assert ledger["tests"][:2] == prior_rows
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("UVP_P03_PASS")
    print("NORMALIZED_RESIDUE", primary["normalized_residue"])
    print("THREE_WAY_MAX_RESIDUAL 0")
    print("NEXT_TEST UVP_P04")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
