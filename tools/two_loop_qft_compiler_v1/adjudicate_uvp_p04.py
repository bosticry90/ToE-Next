"""Adjudicate UVP_P04 and advance only to P05 on exact tensor agreement."""

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
    primary = load_verified("uvp_p04_primary.json")
    replay = load_verified("uvp_p04_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    evidence_schema = json.loads((HERE / "uvp_p04_evidence_schema.json").read_text(
        encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)

    prior_rows = deepcopy(ledger["tests"][:3])
    row = ledger["tests"][3]
    assert [item["status"] for item in prior_rows] == ["PASS"] * 3
    assert row["test_id"] == "UVP_P04"
    assert row["status"] == "NOT_RUN" and row["authorization"] == "READY"
    assert row["attempt"] == 0 and ledger["counters"]["executed"] == 3
    assert all(test["status"] not in {"PASS", "BLOCKED", "FAIL", "RUNNING"}
               for test in ledger["tests"][4:])

    p = sp.sympify(primary["normalized_tensor_residue_coefficient"])
    r = sp.sympify(replay["normalized_tensor_residue_coefficient"])
    residue_difference = sp.simplify(p - r)
    p_contraction = sp.sympify(primary["contraction_residual"])
    r_contraction = sp.sympify(replay["contraction_residual"])
    p_shift = sp.sympify(primary["adversarial_premature_d4"][
        "missed_finite_shift_exact_minus_shortcut_in_1_over_16pi2_units"])
    r_shift = sp.sympify(replay[
        "adversarial_finite_shift_exact_minus_shortcut_in_1_over_16pi2_units"])
    shift_difference = sp.simplify(p_shift - r_shift)
    passed = (
        residue_difference == 0 and p_contraction == 0 and r_contraction == 0
        and shift_difference == 0 and p_shift == -sp.Symbol("m2") / 4
        and not primary["adversarial_premature_d4"]["used_by_promoted_route"]
        and primary["tensor_reduction_coefficient_before_laurent"]
        == "1/(4-2*epsilon)"
        and primary["tensor_pole_expression"] == replay["tensor_pole_expression"]
        and primary["uv_ir"] == replay["uv_ir"]
    )
    if not passed:
        raise AssertionError("UVP_P04 tensor reduction or d=4 adversarial check failed")

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_P04",
        "mass_domain": "m2>0",
        "classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "reason": (
            "the_original_massive_tensor_integral_has_no_IR_pole; the_local_"
            "logarithmic_UV_coefficient_is_extracted_after_exact_d_dimensional_"
            "tensor_reduction"
        ),
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p04_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")

    evidence = {
        "schema_version": 1,
        "test_id": "UVP_P04",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "convention": {
            "dimension": "d=4-2*epsilon",
            "euclidean_integral": (
                "mu^(2*epsilon)*Integral_E[d^d k/(2*pi)^d*"
                "k_mu*k_nu/(k^2+m2)^2]"
            ),
            "tensor_identity": "T_mu_nu=delta_mu_nu*S/d",
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "mass_domain": "m2>0",
        },
        "primary": primary,
        "independent_replay": replay,
        "comparison": {
            "residue_difference": str(residue_difference),
            "primary_contraction_residual": str(p_contraction),
            "replay_contraction_residual": str(r_contraction),
            "tensor_pole_expression_equal": True,
        },
        "adversarial_d4_check": {
            "premature_d4_used_by_promoted_route": False,
            "pole_residue_unchanged": True,
            "missed_finite_shift_exact_minus_shortcut_in_1_over_16pi2_units": str(
                p_shift),
            "primary_replay_shift_difference": str(shift_difference),
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
    (HERE / "uvp_p04_evidence.json").write_text(
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
            "normalized_tensor_residue_coefficient": primary[
                "normalized_tensor_residue_coefficient"],
            "tensor_structure": "delta_mu_nu",
            "pole_unit": "1/(16*pi^2*epsilon_bar)",
            "tensor_pole_expression": primary["tensor_pole_expression"],
            "primary_minus_replay": str(residue_difference),
            "maximum_contraction_residual": "0",
            "premature_d4_missed_finite_shift": str(p_shift),
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "primary_d_dimensional_tensor_reduction_equals_independent_"
            "Schwinger_Gaussian_replay_with_exact_contraction_and_d4_"
            "adversarial_checks"
        ),
        "evidence_files": [
            "uvp_p04_primary.json", "uvp_p04_independent_replay.json",
            "uvp_p04_uv_ir_provenance.json", "uvp_p04_evidence.json",
        ],
    })
    ledger["tests"][4]["authorization"] = "READY"
    ledger["counters"].update({
        "executed": 4, "passed": 4, "not_run_or_locked": 35,
        "engine_executed": 4, "engine_passed": 4,
    })
    assert ledger["tests"][:3] == prior_rows
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("UVP_P04_PASS")
    print("TENSOR_RESIDUE_COEFFICIENT", primary[
        "normalized_tensor_residue_coefficient"])
    print("CONTRACTION_RESIDUAL 0")
    print("PREMATURE_D4_MISSED_FINITE_SHIFT", p_shift)
    print("NEXT_TEST UVP_P05")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
