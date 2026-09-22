"""Adjudicate UVP_M03 attempt 2 while preserving attempt-1 evidence."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
ATTEMPT1 = "a429ce0df860933879bb8810c42a599d0cc0f87a694be392cb591c10f18086c4"


def digest(payload, field="artifact_sha256"):
    work = dict(payload)
    work.pop(field, None)
    return sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def load(name, field="artifact_sha256"):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert payload[field] == digest(payload, field)
    return payload


def main():
    primary = load("uvp_m03_primary_attempt2.json")
    replay = load("uvp_m03_independent_replay_attempt2.json")
    attempt1 = load("uvp_m03_blocked_evidence.json")
    assert attempt1["artifact_sha256"] == ATTEMPT1
    assert attempt1["verdict"] == "BLOCKED"
    assert primary["attempt"] == replay["attempt"] == 2
    assert primary["attempt1_blocked_evidence_sha256"] == ATTEMPT1
    assert replay["attempt1_blocked_evidence_sha256"] == ATTEMPT1
    assert primary["quadratic_residues"] == replay["quadratic_residues"]
    assert primary["quartic_trace_table"] == replay["quartic_trace_table"]
    for sector in ("Phi", "Sigma", "phi", "S"):
        for key in ("ordered_internal_pairs_nonzero", "V3_ACD_V3_ACD"):
            assert primary["cubic_trace_table"][sector][key] == (
                replay["cubic_trace_table"][sector][key]
            )
    assert primary["projection"] == {
        "basis": ["mPhi2", "mSigma2", "mphi2", "mS2"],
        "rank": 4,
        "residual": "0",
        "forbidden_inter_sector_residual": "0",
        "PQ_forbidden_residual": "0",
        "external_representative_residual": "0",
        "operator_symmetry_residual": "0",
    }
    assert replay["projection"]["rank"] == 4
    assert replay["projection"]["residual"] == "0"
    assert replay["projection"]["out_of_basis_residual"] == "0"

    uv_ir = {
        "schema_version": 1,
        "test_id": "UVP_M03",
        "attempt": 2,
        "classification": {"primary": primary["uv_ir"],
                           "replay": replay["uv_ir"]},
        "reason": "regulated local parent two-point projection has UV poles and no IR pole",
    }
    uv_ir["artifact_sha256"] = digest(uv_ir)
    (HERE / "uvp_m03_uv_ir_provenance_attempt2.json").write_text(
        json.dumps(uv_ir, indent=2) + "\n", encoding="utf-8"
    )

    evidence = {
        "schema_version": 1,
        "test_id": "UVP_M03",
        "attempt": 2,
        "contract_sha256": primary["contract_sha256"],
        "execution_plan_sha256": primary["execution_plan_sha256"],
        "attempt_history": [{"attempt": 1, "verdict": "BLOCKED",
                             "evidence_sha256": ATTEMPT1}],
        "primary": primary,
        "independent_replay": replay,
        "comparison": {
            "quadratic_residue_residual": "0",
            "quartic_trace_table_residual": "0",
            "cubic_trace_table_residual": "0",
            "full_operator_projection_residual": "0",
            "rank": 4,
        },
        "uv_ir_classification": uv_ir["classification"],
        "verdict": "PASS",
    }
    evidence["artifact_sha256"] = digest(evidence)
    (HERE / "uvp_m03_evidence_attempt2.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )

    ledger_path = HERE / "uv_pole_evaluator_results.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["result_sha256"] == digest(ledger, "result_sha256")
    assert all(row["status"] == "PASS" for row in ledger["tests"][:28])
    row = ledger["tests"][28]
    assert row["test_id"] == "UVP_M03"
    assert row["status"] == "BLOCKED" and row["attempt"] == 1
    assert row["derived_result"]["evidence_sha256"] == ATTEMPT1
    row.update({
        "status": "PASS",
        "authorization": "TERMINAL",
        "attempt": 2,
        "primary": {"state": "COMPLETE", "method": primary["method"],
                    "inventory_sha256": primary["inventory_sha256"],
                    "residue_sha256": primary["artifact_sha256"],
                    "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "replay": {"state": "COMPLETE", "method": replay["method"],
                   "inventory_sha256": replay["inventory_sha256"],
                   "residue_sha256": replay["artifact_sha256"],
                   "uv_ir_provenance_sha256": uv_ir["artifact_sha256"]},
        "derived_result": {
            "quadratic_residues": primary["quadratic_residues"],
            "projection_rank": 4,
            "maximum_residual": "0",
            "attempt1_blocked_evidence_sha256": ATTEMPT1,
            "evidence_sha256": evidence["artifact_sha256"],
        },
        "verdict_reason": (
            "exhaustive_parent_contractions_match_independent_functional_Hessian_replay"
        ),
        "evidence_files": [
            "uvp_m03_primary_blocker.json",
            "uvp_m03_independent_blocker_replay.json",
            "uvp_m03_uv_ir_provenance.json",
            "uvp_m03_blocked_evidence.json",
            "uvp_m03_primary_attempt2.json",
            "uvp_m03_independent_replay_attempt2.json",
            "uvp_m03_uv_ir_provenance_attempt2.json",
            "uvp_m03_evidence_attempt2.json",
        ],
    })
    ledger["tests"][29]["authorization"] = "READY"
    ledger["overall_status"] = "CANONICAL_RUNNING"
    ledger["authority"] = "ENGINE_GATE_AUTHORITY"
    ledger["counters"].update({
        "executed": 29, "passed": 29, "blocked": 0, "failed": 0,
        "not_run_or_locked": 10, "canonical_executed": 2,
        "canonical_passed": 2,
    })
    ledger["promotion"] = {"engine_gate": "PASS",
                           "counterterm_compiler": "BLOCKED",
                           "layer6_authorized": False}
    ledger.pop("result_sha256")
    ledger["result_sha256"] = digest(ledger, "result_sha256")
    schema = json.loads((HERE / "uv_pole_evaluator_result_schema.json").read_text())
    Draft202012Validator(schema).validate(ledger)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print("UVP_M03_ATTEMPT2_PASS")
    print("FOUR_QUADRATIC_RESIDUES_DERIVED")
    print("NEXT_TEST UVP_M04")
    print("EVIDENCE_SHA256", evidence["artifact_sha256"])


if __name__ == "__main__":
    main()
