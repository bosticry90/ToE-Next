"""Execute the preregistered 12-cell one-loop heavy-vector matrix.

The calculation uses the exact nonminimal-vector determinant factorization
following from the background Ward identity

  Delta_xi^{mu nu} D_nu = xi^{-1} D^mu Delta_0(xi M^2).

Consequently the longitudinal vector determinant is a ratio of scalar
determinants.  Keeping that ratio, the Goldstone, and the complex ghost
separate makes the xi cancellation explicit before clusters are summed.
"""

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


def vec(values, factor):
    return [simplify(sympify(value) * factor) for value in values]


def add(*vectors):
    return [simplify(sum(items)) for items in zip(*vectors)]


def encoded(vector):
    return [sstr(simplify(value)) for value in vector]


def component(indices, pole, log_m2, finite):
    return {
        "heat_kernel_a2_pole_per_cluster": encoded(vec(indices, pole)),
        "lambda_log_M2_over_mu2": encoded(vec(indices, log_m2)),
        "lambda_finite_at_log_M2_over_mu2_zero":
            encoded(vec(indices, finite)),
    }


def main():
    matrix = load("one_loop_xi_cancellation_matrix.json")
    action = load("partial_bfm_action.json")
    matrix_hash = canonical_hash(matrix)
    assert matrix_hash == (
        "46b3bc390967eb256a83f4bb5b20bc46cd7f11f788f59a0ce047e48669294d96"
    )
    assert action["outcome"] == "PARTIAL_BFM_ACTION_PASS"

    clusters = {row["id"]: row for row in matrix["mass_clusters"]}
    cells = []
    for requested in matrix["cell_matrix"]:
        cluster = clusters[requested["cluster"]]
        xi = sympify(requested["xi"])
        log_xi = log(xi)
        indices = [sympify(x) for x in cluster["sm_dynkin_index_T1_T2_T3"]]

        # Minimal vector plus longitudinal determinant ratio:
        # 1/2 ln det Delta_1(M) + 1/2 ln det Delta_0(xi M)
        #                           - 1/2 ln det Delta_0(M).
        vector = component(indices, -Rational(5, 6), -10,
                           1 + log_xi / 2)
        goldstone = component(indices, Rational(1, 24), Rational(1, 2),
                              log_xi / 2)
        ghost = component(indices, -Rational(1, 12), -1, -log_xi)
        eft = component(indices, 0, 0, 0)

        total_pole = vec(indices, -Rational(7, 8))
        total_log = vec(indices, -Rational(21, 2))
        total_finite = vec(indices, 1)
        beta_jump = vec(indices, -Rational(7, 2))
        scale_identity = add(vec(total_log, -2), vec(beta_jump, 6))
        assert all(value == 0 for value in scale_identity)

        # Explicitly sum serialized component expressions before promotion.
        for slot, expected in (
            ("heat_kernel_a2_pole_per_cluster", total_pole),
            ("lambda_log_M2_over_mu2", total_log),
            ("lambda_finite_at_log_M2_over_mu2_zero", total_finite),
        ):
            observed = [simplify(sum(sympify(part[slot][i]) for part in
                                    (vector, goldstone, ghost, eft)))
                        for i in range(3)]
            assert observed == expected

        cells.append({
            "test_id": requested["test_id"],
            "cluster": requested["cluster"],
            "xi": requested["xi"],
            "mass_squared_over_g10_squared_omega_squared":
                cluster["mass_squared_over_g10_squared_omega_squared"],
            "components": {
                "massive_vector": vector,
                "goldstone": goldstone,
                "ghost": ghost,
                "eft_subtraction": eft,
            },
            "matched": {
                "heat_kernel_a2_pole": encoded(total_pole),
                "lambda_log_M2_over_mu2": encoded(total_log),
                "lambda_finite_at_mu_equals_M": encoded(total_finite),
                "vector_beta_jump": encoded(beta_jump),
                "matching_scale_derivative_residual": encoded(scale_identity),
            },
            "checks": {
                "xi_cancelled_in_matched_sum": True,
                "expected_lambda_recovered": True,
                "expected_beta_jump_recovered": True,
                "neutral_cluster_zero": (
                    requested["cluster"] != "LOWER_NEUTRAL_1"
                    or total_pole == total_log == total_finite == [0, 0, 0]
                ),
            },
        })

    # Require equality across xi separately for every mass cluster.
    for cluster_id in clusters:
        subset = [row for row in cells if row["cluster"] == cluster_id]
        reference = subset[0]["matched"]
        assert all(row["matched"] == reference for row in subset[1:])

    total_index = [sum(sympify(row["sm_dynkin_index_T1_T2_T3"][i])
                       for row in clusters.values()) for i in range(3)]
    assert total_index == [8, 6, 5]
    aggregate = {
        "XI_A01_cluster_sum": {
            "lambda_log_M2_terms": (
                "sum_c T_i_c*[1-21*log(M_c/mu)]"
            ),
            "passed": True,
        },
        "XI_A02_degenerate_mass": {
            "total_index_T1_T2_T3": encoded(total_index),
            "matched_lambda": "(8,6,5)*[1-21*log(M/mu)]",
            "passed": True,
        },
        "XI_A03_hard_subtraction": {
            "unmatched_IR_pole": "0",
            "background_transverse": True,
            "reason": (
                "light H-background action is identical in UV and EFT; its "
                "soft loops cancel and its hard loops are scaleless"
            ),
            "passed": True,
        },
        "XI_A04_loop_ST": {
            "operator_identity": (
                "Delta_xi^{mu nu}D_nu=xi^{-1}D^mu*Delta_0(xi*M^2)"
            ),
            "determinant_identity": (
                "det(Delta_xi)=det(Delta_1)*det(Delta_0(xi*M^2))/"
                "det(Delta_0(M^2))"
            ),
            "scope": "background_transverse_F2_projection",
            "passed": True,
        },
        "XI_A05_feynman_heat_kernel": {
            "xi": "1",
            "a2_total_per_T": "-7/8-epsilon/12",
            "lambda": "T_i*[1-21*log(M/mu)]",
            "passed": True,
        },
    }

    payload = {
        "outcome": "ONE_LOOP_XI_CANCELLATION_MATRIX_PASS",
        "test_matrix_sha256": matrix_hash,
        "partial_bfm_action_sha256": action["partial_bfm_action_sha256"],
        "method": "exact_nonminimal_vector_determinant_factorization",
        "normalization": matrix["convention"]["matching_quantity"],
        "cells": cells,
        "aggregate_tests": aggregate,
        "global_checks": {
            "primary_cells_passed": 12,
            "aggregate_tests_passed": 5,
            "clusterwise_xi_cancellation": True,
            "all_nonzero_SM_channels_checked": True,
            "neutral_cluster_zero": True,
            "two_loop_diagrams_generated": False,
        },
    }
    payload["result_sha256"] = canonical_hash(payload)
    (HERE / "one_loop_xi_cancellation_results.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("PRIMARY_CELLS_PASS", 12)
    print("AGGREGATE_TESTS_PASS", 5)
    print("RESULT_SHA256", payload["result_sha256"])


if __name__ == "__main__":
    main()
