"""Adjudicate UVP_P02 and advance only to P03 on exact agreement."""

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
    primary = load_verified("uvp_p02_primary.json")
    replay = load_verified("uvp_p02_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    evidence_schema = json.loads((HERE / "uvp_p02_evidence_schema.json").read_text(
        encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)

    p01_before = deepcopy(ledger["tests"][0])
    row = ledger["tests"][1]
    assert p01_before["test_id"] == "UVP_P01" and p01_before["status"] == "PASS"
    assert row["test_id"] == "UVP_P02"
    assert row["status"] == "NOT_RUN" and row["authorization"] == "READY"
    assert row["attempt"] == 0 and ledger["counters"]["executed"] == 1
    assert all(test["status"] not in {"PASS", "BLOCKED", "FAIL", "RUNNING"}
               for test in ledger["tests"][2:])

    p_residue = sp.sympify(primary["normalized_residue"])
    r_residue = sp.sympify(replay["normalized_residue"])
    difference = sp.simplify(p_residue - r_residue)
    p_mass_derivative = sp.sympify(primary["mass_derivative_of_residue"])
    r_mass_derivative = sp.sympify(replay["mass_derivative_of_residue"])
    passed = (
        difference == 0 and p_mass_derivative == 0 and r_mass_derivative == 0
        and primary["pole_expression"] == replay["pole_expression"]
        and primary["uv_ir"] == replay["uv_ir"]
        and primary["mass_dependent_tail_classification"] == "UV_finite"
    )
    if not passed:
        raise AssertionError("UVP_P02 residue, mass-independence, or replay mismatch")

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_P02",
        "mass_domain": "m2>0",
        "classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "reason": (
            "positive_mass_removes_IR_singularity; only_the_mass_independent_"
            "t^(-1-epsilon)_coefficient_is_logarithmically_UV_divergent"
        ),
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p02_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")

    convention = {
        "dimension": "d=4-2*epsilon",
        "minkowski_integral": (
            "mu^(2*epsilon)*Integral[d^d k/(2*pi)^d * (-i)/(k^2-m2+i0)^2]"
        ),
        "wick_rotated_integral": (
            "mu^(2*epsilon)*Integral_E[d^d k_E/(2*pi)^d * 1/(k_E^2+m2)^2]"
        ),
        "measure": "d^d k/(2*pi)^d",
        "epsilon_bar": "1/epsilon_bar=1/epsilon-gamma_E+log(4*pi)",
        "pole_unit": "1/(16*pi^2*epsilon_bar)",
        "mass_domain": "m2>0",
    }
    evidence = {
        "schema_version": 1,
        "test_id": "UVP_P02",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "convention": convention,
        "primary": primary,
        "independent_replay": replay,
        "mass_independence": {
            "primary_derivative": str(p_mass_derivative),
            "replay_derivative": str(r_mass_derivative),
            "finite_mass_terms_excluded": True,
        },
        "uv_ir_classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "comparison": {
            "normalized_residue_difference": str(difference),
            "pole_expression_equal": True, "convention_equal": True,
        },
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = canonical_hash(evidence)
    Draft202012Validator.check_schema(evidence_schema)
    Draft202012Validator(evidence_schema).validate(evidence)
    (HERE / "uvp_p02_evidence.json").write_text(
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
            "mass_derivative_of_residue": str(p_mass_derivative),
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "pole_expression": primary["pole_expression"],
            "primary_minus_replay": str(difference),
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "primary_mass_independent_log_UV_projector_equals_independent_"
            "two_propagator_Gamma_function_replay_exactly"
        ),
        "evidence_files": [
            "uvp_p02_primary.json", "uvp_p02_independent_replay.json",
            "uvp_p02_uv_ir_provenance.json", "uvp_p02_evidence.json",
        ],
    })
    ledger["tests"][2]["authorization"] = "READY"
    ledger["counters"].update({
        "executed": 2, "passed": 2, "not_run_or_locked": 37,
        "engine_executed": 2, "engine_passed": 2,
    })
    assert ledger["tests"][0] == p01_before
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("UVP_P02_PASS")
    print("NORMALIZED_RESIDUE", primary["normalized_residue"])
    print("MASS_DERIVATIVE", p_mass_derivative)
    print("NEXT_TEST UVP_P03")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
