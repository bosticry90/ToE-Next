"""Audit the frozen promotion-layer-3 authority boundary and result.

The preregistered matrix remains immutable.  Promotion requires the complete
partial-BFM action artifact, all twelve general-xi cells, all five aggregate
tests, and an implementation-independent symbolic replay.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PHYSICAL_HASH = (
    "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e"
)
QUADRATIC_HASH = (
    "b983a8d8dae078761d61c8492ddb583f984398e56483cd306e2382e68ea2e692"
)


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def validate_closure_spec():
    matrix = load("one_loop_xi_cancellation_matrix.json")
    assert matrix["outcome"] == "LAYER3_CLOSURE_TEST_MATRIX_PREREGISTERED"
    immutable = matrix["immutable_inputs"]
    assert immutable["physical_basis_sha256"] == PHYSICAL_HASH
    assert immutable["background_field_quadratic_sha256"] == QUADRATIC_HASH
    assert immutable["parent_action_sha256"] == (
        "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed"
    )
    xis = matrix["xi_values"]
    assert xis == ["1/2", "1", "2"]
    clusters = matrix["mass_clusters"]
    assert sum(row["multiplicity_real_vectors"] for row in clusters) == 33
    total_index = [
        sum(Fraction(row["sm_dynkin_index_T1_T2_T3"][i])
            for row in clusters)
        for i in range(3)
    ]
    assert total_index == [Fraction(8), Fraction(6), Fraction(5)]
    expected_cells = {(row["id"], xi) for row, xi in product(clusters, xis)}
    actual_cells = {(row["cluster"], row["xi"])
                    for row in matrix["cell_matrix"]}
    assert actual_cells == expected_cells and len(matrix["cell_matrix"]) == 12
    assert len({row["test_id"] for row in matrix["cell_matrix"]}) == 12
    assert len(matrix["aggregate_tests"]) == 5
    assert matrix["acceptance"]["clusterwise_pass_required"] is True
    assert matrix["promotion_policy"][
        "two_loop_diagram_enumeration_before_pass"] is False

    task = (HERE / "LAYER3_CLOSURE_TASK.md").read_text(encoding="utf-8")
    for required in (
        PHYSICAL_HASH, QUADRATIC_HASH, "one_loop_xi_cancellation_matrix.json",
        "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS",
        "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_FAIL",
        "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_BLOCKED",
    ):
        assert required in task
    packed = json.dumps(matrix, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def validate_closure_result(closure_hash):
    required = (
        "partial_bfm_action.json",
        "partial_bfm_action_regression.json",
        "one_loop_xi_cancellation_results.json",
        "one_loop_xi_independent_replay.json",
    )
    if not all((HERE / name).exists() for name in required):
        return None
    action, action_regression, result, replay = (load(name) for name in required)
    assert action["outcome"] == "PARTIAL_BFM_ACTION_PASS"
    assert action_regression["outcome"] == "PARTIAL_BFM_ACTION_REGRESSION_PASS"
    assert action_regression["partial_bfm_action_sha256"] == (
        action["partial_bfm_action_sha256"])
    assert action_regression["quartic_heavy_ghost_control"][
        "xi_scaling_pass"] is True
    assert action_regression["quartic_heavy_ghost_control"][
        "grassmann_pair_antisymmetry_pass"] is True
    assert result["outcome"] == "ONE_LOOP_XI_CANCELLATION_MATRIX_PASS"
    assert replay["outcome"] == (
        "ONE_LOOP_XI_CANCELLATION_INDEPENDENT_REPLAY_PASS")
    assert result["test_matrix_sha256"] == closure_hash
    assert result["partial_bfm_action_sha256"] == (
        action["partial_bfm_action_sha256"])
    assert replay["partial_bfm_action_sha256"] == (
        action["partial_bfm_action_sha256"])
    assert result["global_checks"]["primary_cells_passed"] == 12
    assert result["global_checks"]["aggregate_tests_passed"] == 5
    assert result["global_checks"]["clusterwise_xi_cancellation"] is True
    assert result["global_checks"]["two_loop_diagrams_generated"] is False
    assert replay["cells_replayed"] == 12
    assert replay["aggregate_tests_replayed"] == 5
    assert replay["maximum_symbolic_residual"] == "0"
    return action, action_regression, result, replay


def main():
    quadratic = load("background_field_quadratic.json")
    manifest = load("physical_vertex_api.json")
    regression = load("physical_vertex_api_regression.json")

    assert quadratic["outcome"] == "BACKGROUND_FIELD_QUADRATIC_LAYER_PASS"
    assert manifest["outcome"] == "PHYSICAL_VERTEX_API_CORE_PASS"
    assert regression["outcome"] == "PHYSICAL_VERTEX_API_CORE_REGRESSION_PASS"
    for record in (quadratic, manifest, regression):
        assert record["physical_basis_sha256"] == PHYSICAL_HASH
    assert quadratic["quadratic_layer_sha256"] == QUADRATIC_HASH
    assert manifest["background_field_quadratic_sha256"] == QUADRATIC_HASH
    assert regression["background_field_quadratic_sha256"] == QUADRATIC_HASH

    assert quadratic["counts"] == {
        "unbroken_sm_vectors": 12,
        "massive_vectors": 33,
        "real_gauge_goldstones": 33,
        "complex_heavy_ghosts": 33,
    }
    assert max(quadratic["xi_mass_pairing_residuals"].values()) < 1e-12
    assert quadratic["max_goldstone_orbit_projector_residual"] < 2e-12
    assert max(abs(x-y) for x, y in zip(
        quadratic["total_massive_vector_sm_index"], [8, 6, 5])) < 2e-12
    assert max(abs(x-y) for x, y in zip(
        quadratic["lower_ps_sm_broken_vector_index"], [14/5, 0, 1])) < 2e-12

    residual_names = [key for key in regression if key.endswith("residual")]
    assert max(regression[key] for key in residual_names) < 5e-8
    assert regression["inherited_exact_scalar_controls"] == {
        "zEta_quartic": "384",
        "z6_cubic": "2",
        "zK_vev_induced_cubic": "6",
        "lambdaS_fourth_derivative": "24",
    }
    closure_hash = validate_closure_spec()
    closure = validate_closure_result(closure_hash)
    promoted = closure is not None

    payload = {
        "outcome": ("BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS" if promoted
                    else "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_BLOCKED"),
        "physical_basis_sha256": PHYSICAL_HASH,
        "background_field_quadratic": "PASS",
        "background_field_quadratic_sha256": QUADRATIC_HASH,
        "physical_vertex_api_core": "PASS_CALCULATION_LOCAL_ON_DEMAND",
        "physical_vertex_api_core_regressions": "PASS",
        "general_xi_values_checked_at_quadratic_and_tree_ward_level": [0.5, 1.0, 2.0],
        "one_loop_vector_F2": {
            "feynman_gauge": "PASS_INHERITED_T_TIMES_1_MINUS_21_LOG_M_OVER_MU",
            "general_xi_cancellation": (
                "PASS_EXACT_CLUSTERWISE_AT_0P5_1_2" if promoted
                else "NOT_DERIVED"),
        },
        "blocking_requirements": ([] if promoted else [
            "complete_partial_BFM_background_quantum_gauge_fixed_vertex_action",
            "general_xi_UV_minus_EFT_one_loop_F2_assembly",
            "explicit_vector_goldstone_ghost_xi_cancellation_at_0.5_1_2",
            "selected_loop_level_Slavnov_Taylor_replay_in_the_same_prescription",
        ]),
        "two_loop_diagram_enumeration_authorized": promoted,
        "layer3_closure_spec": {
            "outcome": ("EXECUTED_UNCHANGED_PASS" if promoted
                        else "PREREGISTERED_NO_LOOP_RESULT"),
            "one_loop_xi_test_matrix_sha256": closure_hash,
            "primary_cells": 12,
            "aggregate_tests": 5,
            "xi_values": [0.5, 1.0, 2.0],
            "mass_clusters": 4,
        },
        "finite_C1_GS": None,
        "preserved_physics_status": {
            "heavy_threshold": "DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED",
            "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
            "bfb": "BFB_UNRESOLVED",
        },
    }
    if promoted:
        action, action_regression, result, replay = closure
        payload["complete_partial_bfm_action"] = {
            "outcome": action["outcome"],
            "sha256": action["partial_bfm_action_sha256"],
            "quartic_heavy_ghost_included": True,
            "goldstone_pairing_residual": action["goldstone_pairing"][
                "max_orthogonality_residual"],
            "heavy_mass_H_covariance_residual": action[
                "background_H_covariance"][
                    "max_heavy_mass_generator_commutator"],
            "action_regression": action_regression["outcome"],
        }
        payload["one_loop_xi_cancellation_result"] = {
            "outcome": result["outcome"],
            "sha256": result["result_sha256"],
            "primary_cells": 12,
            "aggregate_tests": 5,
            "independent_replay": replay["outcome"],
            "maximum_symbolic_residual": "0",
        }
        payload["next_gate"] = "TWO_LOOP_DIAGRAM_ENUMERATION_LAYER_4"
    (HERE / "compiler_status.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("BACKGROUND_FIELD_QUADRATIC PASS")
    print("PHYSICAL_VERTEX_API_CORE PASS")
    print("GENERAL_XI_ONE_LOOP_F2_CANCELLATION",
          "PASS" if promoted else "NOT_DERIVED")
    print("LAYER3_CLOSURE_TEST_MATRIX_SHA256", closure_hash)
    print("TWO_LOOP_DIAGRAM_ENUMERATION AUTHORIZED=" +
          ("true" if promoted else "false"))


if __name__ == "__main__":
    main()
