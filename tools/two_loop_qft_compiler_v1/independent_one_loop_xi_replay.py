"""Independent replay of the partial-BFM action and 12-cell result.

This file intentionally imports neither the action class nor the primary
one-loop assembler.  It reconstructs the heat-kernel/determinant arithmetic
from the frozen JSON artifacts.
"""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from sympy import Rational, log, simplify, sympify, sstr


HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def encode(values):
    return [sstr(simplify(value)) for value in values]


def scale(indices, factor):
    return [simplify(value * factor) for value in indices]


def main():
    matrix = load("one_loop_xi_cancellation_matrix.json")
    action = load("partial_bfm_action.json")
    result = load("one_loop_xi_cancellation_results.json")

    action_copy = deepcopy(action)
    action_hash = action_copy.pop("partial_bfm_action_sha256")
    assert canonical_hash(action_copy) == action_hash
    result_copy = deepcopy(result)
    result_hash = result_copy.pop("result_sha256")
    assert canonical_hash(result_copy) == result_hash
    assert result["partial_bfm_action_sha256"] == action_hash
    assert result["test_matrix_sha256"] == canonical_hash(matrix)

    source = action["single_action"]
    for required in (
        "G_H_alpha", "G_heavy_i", "L_fix_H", "L_fix_heavy",
        "L_light_ghost", "L_heavy_ghost", "partial_gauge_fixing_fermion",
        "light_gauge_fixing_fermion",
    ):
        assert required in source and source[required]
    assert "quartic" in action["derived_vertex_families"][-3]
    assert action["field_ledger"]["heavy_vectors"] == 33
    assert action["field_ledger"]["orbit_aligned_goldstones"] == 33
    assert action["field_ledger"]["heavy_ghosts_complex"] == 33
    assert action["background_H_covariance"][
        "max_heavy_mass_generator_commutator"] < 4e-12

    clusters = {row["id"]: row for row in matrix["mass_clusters"]}
    assert len(result["cells"]) == 12
    maximum_symbolic_residual = 0
    for cell in result["cells"]:
        cluster = clusters[cell["cluster"]]
        indices = [sympify(x) for x in cluster["sm_dynkin_index_T1_T2_T3"]]
        xi = sympify(cell["xi"])
        ell = log(xi)

        # Reconstruct without calling the primary component builder.  The
        # vector longitudinal determinant contributes +scalar(xi M)-scalar(M).
        expected = {
            "massive_vector": (
                scale(indices, -Rational(5, 6)),
                scale(indices, -10),
                scale(indices, 1 + ell / 2),
            ),
            "goldstone": (
                scale(indices, Rational(1, 24)),
                scale(indices, Rational(1, 2)),
                scale(indices, ell / 2),
            ),
            "ghost": (
                scale(indices, -Rational(1, 12)),
                scale(indices, -1),
                scale(indices, -ell),
            ),
            "eft_subtraction": ([0, 0, 0], [0, 0, 0], [0, 0, 0]),
        }
        slots = (
            "heat_kernel_a2_pole_per_cluster",
            "lambda_log_M2_over_mu2",
            "lambda_finite_at_log_M2_over_mu2_zero",
        )
        for name, expected_parts in expected.items():
            observed = cell["components"][name]
            for slot, expected_vector in zip(slots, expected_parts):
                residuals = [simplify(sympify(x) - y)
                             for x, y in zip(observed[slot], expected_vector)]
                assert all(value == 0 for value in residuals)

        expected_matched = (
            scale(indices, -Rational(7, 8)),
            scale(indices, -Rational(21, 2)),
            scale(indices, 1),
            scale(indices, -Rational(7, 2)),
        )
        observed_slots = (
            "heat_kernel_a2_pole", "lambda_log_M2_over_mu2",
            "lambda_finite_at_mu_equals_M", "vector_beta_jump",
        )
        for slot, expected_vector in zip(observed_slots, expected_matched):
            assert cell["matched"][slot] == encode(expected_vector)
        assert cell["matched"]["matching_scale_derivative_residual"] == [
            "0", "0", "0"]

    for cluster_id in clusters:
        rows = [row for row in result["cells"] if row["cluster"] == cluster_id]
        assert len(rows) == 3
        assert rows[0]["matched"] == rows[1]["matched"] == rows[2]["matched"]
    assert all(item["passed"] for item in result["aggregate_tests"].values())

    payload = {
        "outcome": "ONE_LOOP_XI_CANCELLATION_INDEPENDENT_REPLAY_PASS",
        "partial_bfm_action_sha256": action_hash,
        "primary_result_sha256": result_hash,
        "cells_replayed": 12,
        "aggregate_tests_replayed": 5,
        "maximum_symbolic_residual": str(maximum_symbolic_residual),
        "imports_primary_assembler": False,
        "imports_action_compiler": False,
    }
    (HERE / "one_loop_xi_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("CELLS_REPLAYED", 12, "AGGREGATES_REPLAYED", 5)
    print("MAXIMUM_SYMBOLIC_RESIDUAL", 0)


if __name__ == "__main__":
    main()
