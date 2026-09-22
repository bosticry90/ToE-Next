"""Adjudicate UVP_P06 and advance only to P07 on exact local agreement."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import sympy as sp


HERE = Path(__file__).resolve().parent


def canonical_hash(payload, hash_field="artifact_sha256"):
    work = dict(payload)
    work.pop(hash_field, None)
    return sha256(json.dumps(work, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload["artifact_sha256"] == canonical_hash(payload)
    return payload


def main():
    primary = load_verified("uvp_p06_primary.json")
    replay = load_verified("uvp_p06_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(encoding="utf-8"))
    evidence_schema = json.loads((HERE / "uvp_p06_evidence_schema.json").read_text(encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    prior = deepcopy(ledger["tests"][:5])
    row = ledger["tests"][5]
    assert [item["status"] for item in prior] == ["PASS"] * 5
    assert row["test_id"] == "UVP_P06" and row["authorization"] == "READY"

    p2 = primary["two_point_primitive"]["normalized_UV_coefficients"]
    r2 = replay["two_point_normalized_UV_coefficients"]
    labels = ["constant", "p_linear", "p2"]
    residuals = {key: str(sp.simplify(sp.sympify(p2[key]) - sp.sympify(r2[key]))) for key in labels}
    pv = sp.sympify(primary["one_derivative_primitive"]["normalized_p_mu_UV_coefficient"])
    rv = sp.sympify(replay["one_derivative_normalized_p_mu_UV_coefficient"])
    vector_residual = sp.simplify(pv - rv)
    max_residual = "0" if all(value == "0" for value in residuals.values()) and vector_residual == 0 else "NONZERO"
    passed = (
        max_residual == "0" and p2 == {"constant": "1", "p_linear": "0", "p2": "0"}
        and pv == -sp.Rational(1, 2)
        and primary["locality"]["forbidden_structures_present"] == []
        and replay["locality"]["forbidden_structures_present"] == []
        and primary["two_point_primitive"]["first_omitted_terms_UV_finite"]
        and primary["one_derivative_primitive"]["first_omitted_terms_UV_finite"]
        and primary["uv_ir"] == replay["uv_ir"]
    )
    if not passed:
        raise AssertionError("UVP_P06 local Taylor comparison failed")

    uv_ir = {
        "schema_version": 1, "test_id": "UVP_P06", "mass_domain": "m2>0",
        "classification": {"uv_pole": True, "ir_pole": False, "scaleless": False, "rstar_required": False},
        "reason": "massive_nonexceptional_primitives_have_no_IR_pole_and_no_IR_rearrangement_is_used",
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p06_uv_ir_provenance.json").write_text(json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")
    evidence = {
        "schema_version": 1, "test_id": "UVP_P06", "attempt": 1,
        "contract_sha256": primary["contract_sha256"],
        "execution_plan_sha256": primary["execution_plan_sha256"],
        "primary": primary, "independent_replay": replay,
        "local_coefficients": {"constant": "1", "p_linear": "0", "p2": "0", "p_mu": "-1/2", "maximum_residual": max_residual},
        "locality": {"local_polynomial_only": True, "forbidden_structures_present": []},
        "tail_power_counting": {"two_point_beyond_p2": "UV_finite", "one_derivative_beyond_p_mu": "UV_finite"},
        "routing_diagnostic": {"scalar_residual": "0", "vector_covariance": "PASS", "authority": "SUPPORTING_ONLY_P08_REMAINS_DEDICATED_ROUTING_GATE"},
        "uv_ir_classification": uv_ir["classification"], "verdict": "PASS",
    }
    evidence["artifact_sha256"] = canonical_hash(evidence)
    Draft202012Validator(evidence_schema).validate(evidence)
    (HERE / "uvp_p06_evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    row.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE", "method": primary["method"], "inventory_sha256": None, "residue_sha256": primary["artifact_sha256"], "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": replay["method"], "inventory_sha256": None, "residue_sha256": replay["artifact_sha256"], "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "derived_result": {"two_point_constant": "1", "two_point_p2": "0", "one_derivative_p_mu": "-1/2", "maximum_local_coefficient_residual": "0", "nonlocal_structures": 0, "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": "local_integrand_Taylor_projector_equals_nonexceptional_Feynman_parameter_replay_through_required_orders",
        "evidence_files": ["uvp_p06_primary.json", "uvp_p06_independent_replay.json", "uvp_p06_uv_ir_provenance.json", "uvp_p06_evidence.json"],
    })
    ledger["tests"][6]["authorization"] = "READY"
    ledger["counters"].update({"executed": 6, "passed": 6, "not_run_or_locked": 33, "engine_executed": 6, "engine_passed": 6})
    assert ledger["tests"][:5] == prior
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print("UVP_P06_PASS")
    print("LOCAL_COEFFICIENTS 1 0 -1/2")
    print("NONLOCAL_STRUCTURES 0")
    print("NEXT_TEST UVP_P07")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
