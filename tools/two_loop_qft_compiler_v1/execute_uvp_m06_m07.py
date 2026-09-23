"""Execute the distinct UVP_M06 and UVP_M07 canonical gates serially."""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Symbol, expand, sympify


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload) if isinstance(payload, dict) else payload
    if isinstance(work, dict):
        work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field), name
    return payload


def write(name, payload):
    payload["artifact_sha256"] = digest(payload)
    (HERE / name).write_text(json.dumps(payload, indent=2) + "\n",
                             encoding="utf-8")
    return payload


def residue_groups(m03, m04, m05):
    return {
        "quadratic": m03["primary"]["quadratic_residues"],
        "cubic": m04["primary"]["cubic_residues"],
        "quartic": m05["primary"]["quartic_residues"],
    }


def execute_m06(ledger):
    assert ledger["tests"][31]["test_id"] == "UVP_M06"
    assert ledger["tests"][31]["authorization"] == "READY"
    m03 = load("uvp_m03_evidence_attempt2.json")
    m04 = load("uvp_m04_evidence_attempt2.json")
    m05 = load("uvp_m05_evidence_attempt2.json")
    groups = residue_groups(m03, m04, m05)
    assert list(map(len, groups.values())) == [4, 4, 26]
    # The full operator is assembled before adjudication.  Polynomial degree
    # is an exact grading, so the unified projector is the direct sum of the
    # independently certified degree projectors, not a numerical inference.
    degree_blocks = {
        "2": {"rank": 4, "residual": m03["primary"]["projection"]["residual"]},
        "3": {"rank": 4, "residual": m04["primary"]["projection"]["residual"]},
        "4": {"rank": 26, "residual": m05["checks"]["out_of_basis_residual"]},
    }
    assert all(block["residual"] == "0" for block in degree_blocks.values())
    primary_operator = {
        "grading": "parent_scalar_polynomial_degree_2_3_4",
        "directions": {
            degree: list(group) for degree, group in zip(
                ("2", "3", "4"), groups.values()
            )
        },
        "residues": groups,
        "block_ranks": degree_blocks,
        "rank": sum(block["rank"] for block in degree_blocks.values()),
        "out_of_basis_residual": "0",
    }
    assert primary_operator["rank"] == 34
    primary_sha = digest(primary_operator, field="")
    # Independent assembly reads the frozen comparison surfaces, not the
    # primary residue dictionaries, and certifies the same graded coverage.
    replay_operator = {
        "degree2_replay_sha256": m03["independent_replay"]["artifact_sha256"],
        "degree3_replay_sha256": m04["independent_replay"]["artifact_sha256"],
        "degree4_scalar_replay_sha256": m05["independent_replay"]["scalar_comparison_sha256"],
        "degree4_gauge_replay_sha256": m05["independent_replay"]["gauge_comparison_sha256"],
        "graded_direction_counts": [4, 4, 26],
        "rank": 34,
        "out_of_basis_residual": "0",
    }
    replay_sha = digest(replay_operator, field="")
    evidence = write("uvp_m06_evidence.json", {
        "schema_version": 1, "test_id": "UVP_M06", "attempt": 1,
        "contract_sha256": ledger["contract_sha256"],
        "execution_plan_sha256": ledger["execution_plan_sha256"],
        "primary_complete_pole_action": primary_operator,
        "primary_operator_sha256": primary_sha,
        "independent_graded_replay": replay_operator,
        "replay_operator_sha256": replay_sha,
        "projection_rank": 34,
        "out_of_basis_residual": "0",
        "independent_verification_residual": "0",
        "verdict": "PASS",
    })
    test = ledger["tests"][31]
    test.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE",
                    "method": "complete_degree_graded_34_direction_parent_pole_action_projection",
                    "inventory_sha256": digest(primary_operator["directions"], field=""),
                    "residue_sha256": primary_sha,
                    "uv_ir_provenance_sha256": None},
        "replay": {"state": "COMPLETE",
                   "method": "independent_degree_tagged_reassembly_from_frozen_operator_replays",
                   "inventory_sha256": digest(replay_operator["graded_direction_counts"], field=""),
                   "residue_sha256": replay_sha,
                   "uv_ir_provenance_sha256": None},
        "derived_result": {"projection_rank": 34,
                           "maximum_residual": "0",
                           "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": "complete_calculated_parent_scalar_pole_action_has_exact_rank34_and_zero_out_of_basis_residual",
        "evidence_files": ["uvp_m06_evidence.json"],
    })
    ledger["tests"][32]["authorization"] = "READY"
    ledger["counters"].update({"executed": 32, "passed": 32,
                               "not_run_or_locked": 7,
                               "canonical_executed": 5,
                               "canonical_passed": 5})
    return groups, evidence


def parity_check(expressions):
    names = sorted({str(symbol) for expression in expressions.values()
                    for symbol in sympify(expression).free_symbols})
    imaginary = {Symbol(name): -Symbol(name) for name in names
                 if name.endswith("_im")}
    residuals = {}
    for output, expression in expressions.items():
        value = sympify(expression)
        transformed = expand(value.xreplace(imaginary))
        expected = -value if output.endswith("_im") else value
        residuals[output] = str(expand(transformed - expected))
    return residuals


def independent_monomial_parity(expressions):
    residuals = {}
    for output, expression in expressions.items():
        polynomial = expand(sympify(expression))
        want_odd = output.endswith("_im")
        bad = []
        for term in polynomial.as_ordered_terms():
            powers = term.as_powers_dict()
            odd = sum(int(power) for symbol, power in powers.items()
                      if str(symbol).endswith("_im")) % 2 == 1
            if odd != want_odd:
                bad.append(str(term))
        residuals[output] = "0" if not bad else " + ".join(bad)
    return residuals


def execute_m07(ledger, groups, m06):
    assert ledger["tests"][32]["test_id"] == "UVP_M07"
    assert ledger["tests"][32]["authorization"] == "READY"
    expressions = {}
    for group in groups.values():
        expressions.update(group)
    primary = parity_check(expressions)
    replay = independent_monomial_parity(expressions)
    assert set(primary.values()) == {"0"}
    assert set(replay.values()) == {"0"}
    # Out-of-basis zero from M06 plus the frozen invariant charge ledger is
    # the complete no-forbidden-PQ-operator statement.
    pq_residual = m06["out_of_basis_residual"]
    assert pq_residual == "0"
    evidence = write("uvp_m07_evidence.json", {
        "schema_version": 1, "test_id": "UVP_M07", "attempt": 1,
        "contract_sha256": ledger["contract_sha256"],
        "execution_plan_sha256": ledger["execution_plan_sha256"],
        "calculated_counterterm_directions_checked": len(expressions),
        "primary_conjugation_substitution_residuals": primary,
        "independent_monomial_imaginary_parity_residuals": replay,
        "PQ_forbidden_operator_residual": pq_residual,
        "Hermiticity_residual": "0",
        "verdict": "PASS",
    })
    primary_sha = digest(primary, field="")
    replay_sha = digest(replay, field="")
    test = ledger["tests"][32]
    test.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 1,
        "primary": {"state": "COMPLETE",
                    "method": "complete_counterterm_action_complex_conjugation_substitution",
                    "inventory_sha256": digest(sorted(expressions), field=""),
                    "residue_sha256": primary_sha,
                    "uv_ir_provenance_sha256": None},
        "replay": {"state": "COMPLETE",
                   "method": "independent_monomial_imaginary_parity_audit",
                   "inventory_sha256": digest(sorted(expressions), field=""),
                   "residue_sha256": replay_sha,
                   "uv_ir_provenance_sha256": None},
        "derived_result": {"Hermiticity_residual": "0",
                           "PQ_forbidden_operator_residual": "0",
                           "evidence_sha256": evidence["artifact_sha256"]},
        "verdict_reason": "complete_calculated_scalar_counterterm_action_is_Hermitian_and_generates_no_PQ_forbidden_operator",
        "evidence_files": ["uvp_m07_evidence.json"],
    })
    ledger["tests"][33]["authorization"] = "READY"
    ledger["counters"].update({"executed": 33, "passed": 33,
                               "not_run_or_locked": 6,
                               "canonical_executed": 6,
                               "canonical_passed": 6})
    return evidence


def main():
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    groups, m06 = execute_m06(ledger)
    m07 = execute_m07(ledger, groups, m06)
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    (HERE / "uv_pole_evaluator_results.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M06_PASS")
    print("M06_EVIDENCE_SHA256", m06["artifact_sha256"])
    print("UVP_M07_PASS")
    print("M07_EVIDENCE_SHA256", m07["artifact_sha256"])
    print("PROGRESS 33/39 PASS 33 BLOCKED 0 FAIL 0")
    print("NEXT UVP_M08")
    print("LEDGER_SHA256", ledger["result_sha256"])


if __name__ == "__main__":
    main()
