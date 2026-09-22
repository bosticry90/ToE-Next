"""Adjudicate UVP_P05 and advance only to P06 on exact tensor agreement."""

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
    primary = load_verified("uvp_p05_primary.json")
    replay = load_verified("uvp_p05_independent_replay.json")
    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    evidence_schema = json.loads((HERE / "uvp_p05_evidence_schema.json").read_text(
        encoding="utf-8"))
    ledger_schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text(
        encoding="utf-8"))
    assert ledger["result_sha256"] == canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)

    prior_rows = deepcopy(ledger["tests"][:4])
    row = ledger["tests"][4]
    assert [item["status"] for item in prior_rows] == ["PASS"] * 4
    assert row["test_id"] == "UVP_P05"
    assert row["status"] == "NOT_RUN" and row["authorization"] == "READY"
    assert row["attempt"] == 0 and ledger["counters"]["executed"] == 4
    assert all(test["status"] not in {"PASS", "BLOCKED", "FAIL", "RUNNING"}
               for test in ledger["tests"][5:])

    p4, p6 = primary["rank4"], primary["rank6"]
    r4, r6 = replay["rank4"], replay["rank6"]
    rank4_set_difference = sorted(set(p4["pairings"]) ^ set(r4["pairings"]))
    rank6_set_difference = sorted(set(p6["pairings"]) ^ set(r6["pairings"]))
    rank4_residue_difference = sp.simplify(
        sp.sympify(p4["normalized_residue_per_pairing"])
        - sp.sympify(r4["normalized_residue_per_pairing"]))
    rank6_residue_difference = sp.simplify(
        sp.sympify(p6["normalized_residue_per_pairing"])
        - sp.sympify(r6["normalized_residue_per_pairing"]))
    contraction_keys = [
        "rank6_to_rank4_residual", "rank4_to_rank2_residual",
        "rank2_to_scalar_residual", "rank4_to_scalar_residual",
        "rank6_to_scalar_residual",
    ]
    primary_contractions = primary["recursive_contractions"]
    replay_contractions = replay["recursive_contractions"]
    contraction_equal = all(
        primary_contractions[key] == replay_contractions[key] == "0"
        for key in contraction_keys)
    p4_shift = sp.sympify(p4["premature_d4_missed_finite_shift_per_pairing"])
    p6_shift = sp.sympify(p6["premature_d4_missed_finite_shift_per_pairing"])
    r4_shift = sp.sympify(r4["premature_d4_missed_finite_shift_per_pairing"])
    r6_shift = sp.sympify(r6["premature_d4_missed_finite_shift_per_pairing"])
    shift_residual = sp.simplify((p4_shift - r4_shift) + (p6_shift - r6_shift))
    epsilon = sp.Symbol("epsilon")
    d_dimension = 4 - 2 * epsilon
    rank4_denominator_residual = sp.simplify(
        sp.sympify(p4["dimension_denominator"])
        - d_dimension * (d_dimension + 2))
    rank6_denominator_residual = sp.simplify(
        sp.sympify(p6["dimension_denominator"])
        - d_dimension * (d_dimension + 2) * (d_dimension + 4))

    passed = (
        p4["pairing_count"] == r4["pairing_count"] == 3
        and p6["pairing_count"] == r6["pairing_count"] == 15
        and not rank4_set_difference and not rank6_set_difference
        and rank4_residue_difference == rank6_residue_difference == 0
        and rank4_denominator_residual == 0
        and rank6_denominator_residual == 0
        and p4["permutation_checks_passed"] == 24
        and p6["permutation_checks_passed"] == 720
        and contraction_equal and shift_residual == 0
        and p4_shift == sp.Rational(5, 144)
        and p6_shift == sp.Rational(13, 2304)
        and not p4["premature_d4_used_by_promoted_route"]
        and not p6["premature_d4_used_by_promoted_route"]
        and primary["uv_ir"] == replay["uv_ir"]
    )
    if not passed:
        raise AssertionError("UVP_P05 pairing, contraction, or dimensional check failed")

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_P05",
        "mass_domain": "m2>0",
        "classification": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "rstar_required": False,
        },
        "reason": (
            "the_massive_rank4_and_rank6_vacuum_integrals_are_IR_finite; "
            "their_logarithmic_UV_moments_are_reduced_with_exact_d_"
            "dimensional_pairing_denominators"
        ),
    }
    uv_ir["artifact_sha256"] = canonical_hash(uv_ir)
    (HERE / "uvp_p05_uv_ir_provenance.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8")

    evidence = {
        "schema_version": 1,
        "test_id": "UVP_P05",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "primary": primary,
        "independent_replay": replay,
        "pairing_comparison": {
            "rank4_count": p4["pairing_count"],
            "rank6_count": p6["pairing_count"],
            "rank4_set_difference": rank4_set_difference,
            "rank6_set_difference": rank6_set_difference,
            "rank4_residue_difference": str(rank4_residue_difference),
            "rank6_residue_difference": str(rank6_residue_difference),
        },
        "recursive_contractions": {
            **{key: primary_contractions[key] for key in contraction_keys},
            "primary_replay_equal": contraction_equal,
        },
        "permutation_symmetry": {
            "rank4_checks": p4["permutation_checks_passed"],
            "rank6_checks": p6["permutation_checks_passed"],
            "all_pass": True,
        },
        "adversarial_d4_check": {
            "premature_d4_used_by_promoted_route": False,
            "rank4_missed_finite_shift": str(p4_shift),
            "rank6_missed_finite_shift": str(p6_shift),
            "primary_replay_shift_residual": str(shift_residual),
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
    (HERE / "uvp_p05_evidence.json").write_text(
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
            "rank4_pairing_count": 3,
            "rank6_pairing_count": 15,
            "rank4_normalized_residue_per_pairing": p4[
                "normalized_residue_per_pairing"],
            "rank6_normalized_residue_per_pairing": p6[
                "normalized_residue_per_pairing"],
            "maximum_pairing_or_contraction_residual": "0",
            "rank4_premature_d4_missed_finite_shift": str(p4_shift),
            "rank6_premature_d4_missed_finite_shift": str(p6_shift),
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "recursive_primary_and_permutation_orbit_Gaussian_replay_agree_"
            "on_all_rank4_rank6_pairings_coefficients_symmetries_and_"
            "recursive_contractions"
        ),
        "evidence_files": [
            "uvp_p05_primary.json", "uvp_p05_independent_replay.json",
            "uvp_p05_uv_ir_provenance.json", "uvp_p05_evidence.json",
        ],
    })
    ledger["tests"][5]["authorization"] = "READY"
    ledger["counters"].update({
        "executed": 5, "passed": 5, "not_run_or_locked": 34,
        "engine_executed": 5, "engine_passed": 5,
    })
    assert ledger["tests"][:4] == prior_rows
    ledger.pop("result_sha256")
    ledger["result_sha256"] = canonical_hash(ledger, "result_sha256")
    Draft202012Validator(ledger_schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("UVP_P05_PASS")
    print("PAIRING_COUNTS 3 15")
    print("RANK4_PER_PAIRING_RESIDUE", p4["normalized_residue_per_pairing"])
    print("RANK6_PER_PAIRING_RESIDUE", p6["normalized_residue_per_pairing"])
    print("MAXIMUM_PAIRING_OR_CONTRACTION_RESIDUAL 0")
    print("NEXT_TEST UVP_P06")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
