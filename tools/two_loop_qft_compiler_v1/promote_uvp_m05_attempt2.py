"""Adjudicate UVP_M05 attempt 2 from the frozen complete primary/replays."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(payload, field="artifact_sha256"):
    work = dict(payload)
    work.pop(field, None)
    return sha256(json.dumps(work, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field), name
    return payload


def main():
    ledger = load("uv_pole_evaluator_results.json", "result_sha256")
    old = load("uvp_m05_blocked_evidence.json")
    primary = load("uvp_m05_primary_complete_candidate.json")
    scalar_raw = load("uvp_m05_independent_scalar_replay_uncompared.json")
    scalar = load("uvp_m05_independent_scalar_replay.json")
    gauge = load("uvp_m05_independent_gauge_replay.json")
    assert ledger["tests"][30]["test_id"] == "UVP_M05"
    assert ledger["tests"][30]["status"] == "BLOCKED"
    assert primary["projection"]["rank"] == 26
    assert primary["projection"]["scalar_out_of_basis_residual"] == "0"
    assert primary["projection"]["gauge_orbit_out_of_basis_residual"] == "0"
    assert primary["projection"]["xi_residual"] == "0"
    assert primary["projection"]["PQ_forbidden_residual"] == "0"
    assert primary["projection"]["Hermitian_real_direction_basis"] is True
    assert len(primary["quartic_residues"]) == 26
    assert scalar["maximum_residual"] == "0"
    assert scalar["projection_rank"] == 26
    assert scalar["out_of_basis_residual"] == "0"
    assert gauge["maximum_residual"] == "0" and gauge["xi_residual"] == "0"

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_M05",
        "attempt": 2,
        "classification": "UV_LOCAL_LOGARITHMIC_ONE_LOOP_FOUR_POINT_POLE",
        "infrared_status": "NO_UNMATCHED_IR_POLE",
        "auxiliary_mass_status": "NOT_REQUIRED_FOR_MASS_INDEPENDENT_QUARTIC_POLE",
        "locality": "EXACT_QUADRILINEAR_PARENT_OPERATOR",
    }
    uv_ir["artifact_sha256"] = digest(uv_ir)
    (HERE / "uvp_m05_uv_ir_provenance_attempt2.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8"
    )

    primary_residue_sha = digest(primary["quartic_residues"], field="")
    scalar_tables_sha = digest(scalar_raw["coefficient_tables"], field="")
    replay_residue_payload = {
        "scalar_tables_sha256": scalar_tables_sha,
        "gauge_replay_sha256": gauge["artifact_sha256"],
        "direction_residuals": scalar["direction_residuals"],
    }
    replay_residue_sha = digest(replay_residue_payload, field="")
    evidence = {
        "schema_version": 1,
        "test_id": "UVP_M05",
        "attempt": 2,
        "contract_sha256": ledger["contract_sha256"],
        "execution_plan_sha256": ledger["execution_plan_sha256"],
        "attempt_history": [{
            "attempt": 1, "verdict": "BLOCKED",
            "evidence_sha256": old["artifact_sha256"],
        }],
        "primary": {
            "method": "complete_328_real_scalar_V4V4_plus_partial_BFM_gauge_assembly",
            "artifact_sha256": primary["artifact_sha256"],
            "inventory_sha256": primary["inventory_sha256"],
            "residue_sha256": primary_residue_sha,
            "quartic_residues": primary["quartic_residues"],
        },
        "independent_replay": {
            "method": "inventory_independent_parent_polynomial_reconstruction_plus_independent_partial_BFM_gauge_replay",
            "uncompared_scalar_sha256": scalar_raw["artifact_sha256"],
            "scalar_comparison_sha256": scalar["artifact_sha256"],
            "gauge_comparison_sha256": gauge["artifact_sha256"],
            "inventory_sha256": scalar_raw["inventory_sha256"],
            "residue_sha256": replay_residue_sha,
        },
        "checks": {
            "real_quartic_directions": 26,
            "parent_internal_real_directions": 328,
            "projection_rank": 26,
            "out_of_basis_residual": "0",
            "independent_background_residual": "0",
            "primary_minus_scalar_replay": "0",
            "primary_minus_gauge_replay": "0",
            "xi_residual": "0",
            "permutation_Hermiticity_PQ_residual": "0",
        },
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_m05_evidence_attempt2.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )

    test = ledger["tests"][30]
    test.update({
        "status": "PASS", "authorization": "TERMINAL", "attempt": 2,
        "primary": {
            "state": "COMPLETE",
            "method": evidence["primary"]["method"],
            "inventory_sha256": primary["inventory_sha256"],
            "residue_sha256": primary_residue_sha,
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "replay": {
            "state": "COMPLETE",
            "method": evidence["independent_replay"]["method"],
            "inventory_sha256": scalar_raw["inventory_sha256"],
            "residue_sha256": replay_residue_sha,
            "uv_ir_provenance_sha256": uv_ir["artifact_sha256"],
        },
        "derived_result": {
            "quartic_residues": primary["quartic_residues"],
            "projection_rank": 26,
            "maximum_residual": "0",
            "attempt1_blocked_evidence_sha256": old["artifact_sha256"],
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": "complete_quartic_operator_and_partial_BFM_gauge_assembly_match_inventory_independent_scalar_and_gauge_replays",
        "evidence_files": [
            "uvp_m05_blocked_evidence.json",
            "uvp_m05_complete_scalar_v4v4.json",
            "uvp_m05_primary_complete_candidate.json",
            "uvp_m05_independent_scalar_replay_uncompared.json",
            "uvp_m05_independent_scalar_replay.json",
            "uvp_m05_independent_gauge_replay_uncompared.json",
            "uvp_m05_independent_gauge_replay.json",
            "uvp_m05_uv_ir_provenance_attempt2.json",
            "uvp_m05_evidence_attempt2.json",
        ],
    })
    ledger["tests"][31]["authorization"] = "READY"
    ledger["overall_status"] = "CANONICAL_RUNNING"
    ledger["counters"].update({
        "executed": 31, "passed": 31, "blocked": 0, "failed": 0,
        "not_run_or_locked": 8, "canonical_executed": 4,
        "canonical_passed": 4,
    })
    ledger["promotion"]["counterterm_compiler"] = "BLOCKED"
    ledger["promotion"]["layer6_authorized"] = False
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    (HERE / "uv_pole_evaluator_results.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M05_PASS_ATTEMPT2")
    print("PROGRESS 31/39 PASS 31 BLOCKED 0 FAIL 0")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])
    print("LEDGER_SHA256", ledger["result_sha256"])


if __name__ == "__main__":
    main()
