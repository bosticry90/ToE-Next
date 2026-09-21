"""Regression and tree-level Ward checks for the on-demand vertex core."""

import json
from pathlib import Path

import numpy as np

from physical_basis_runtime import PHYSICAL_BASIS_HASH
from physical_vertex_api import PhysicalVertexAPI, QUADRATIC_HASH


HERE = Path(__file__).resolve().parent


def main():
    api = PhysicalVertexAPI()
    assert api.U.shape == (328, 328)
    assert len(api.vector_generators) == 45
    assert sum(api.vector_masses > 1e-10) == 33

    # Gauge-generator antisymmetry in the physical scalar metric.
    a, i, j = "X000", "H000", "H001"
    vss_ij = api.vss(a, i, j)
    vss_ji = api.vss(a, j, i)
    assert abs(vss_ij + vss_ji) < 2e-10

    # The seagull kernel is symmetric in both vector and scalar pairs.
    q1 = api.vvss("X000", "X001", "H000", "H001")
    q2 = api.vvss("X001", "X000", "H000", "H001")
    q3 = api.vvss("X000", "X001", "H001", "H000")
    assert max(abs(q1-q2), abs(q1-q3)) < 2e-10

    # Pure-gauge structure constants are antisymmetric and obey Jacobi.
    ids = [api.vector_id(k) for k in (0, 12, 24, 36)]
    for x, y, z in ((ids[0], ids[1], ids[2]),
                    (ids[1], ids[2], ids[3])):
        assert abs(api.structure_constant(x, y, z)
                   + api.structure_constant(y, x, z)) < 2e-12
    jacobi = 0.0
    for e in range(45):
        ve = api.vector_id(e)
        jacobi += (
            api.structure_constant(ids[0], ids[1], ve)
            * api.structure_constant(ve, ids[2], ids[3])
            + api.structure_constant(ids[1], ids[2], ve)
            * api.structure_constant(ve, ids[0], ids[3])
            + api.structure_constant(ids[2], ids[0], ve)
            * api.structure_constant(ve, ids[1], ids[3]))
    assert abs(jacobi) < 2e-11

    # For each xi, the diagonal heavy-ghost mass is xi times the vector mass.
    max_pairing = 0.0
    for xi in (.5, 1.0, 2.0):
        for index in range(12, 45):
            field = api.vector_id(index)
            difference = abs(api.ghost_mass(field, field, xi)
                             - xi*api.vector_masses[index])
            max_pairing = max(max_pairing, difference)
    assert max_pairing < 2e-12

    # Tree-level FP/Goldstone Ward relation: for a diagonal massive vector,
    # the ghost-ghost-scalar kernel equals xi/2 times the VVS kernel.
    ward_residuals = []
    for xi in (.5, 1.0, 2.0):
        lhs = api.ghost_scalar("X000", "X000", "H000", xi)
        rhs = xi*api.vvs("X000", "X000", "H000")/2
        ward_residuals.append(abs(lhs-rhs))
    assert max(ward_residuals) < 3e-10

    # The scalar-potential API is permutation symmetric in physical IDs.
    # These certified physical columns are pure S/Phi directions, so this
    # test exercises the transformed API without repeatedly recomputing a
    # changing dense self-dual-form quartic during a regression run.
    cubic_a = api.potential_vertex("H003", "H029", "H030")
    cubic_b = api.potential_vertex("H030", "H003", "H029")
    scalar_permutation_residual = abs(cubic_a-cubic_b)
    assert scalar_permutation_residual < 5e-8

    quartic_a = api.potential_vertex("H003", "H003", "H029", "H030")
    quartic_b = api.potential_vertex("H030", "H003", "H003", "H029")
    scalar_quartic_permutation_residual = abs(quartic_a-quartic_b)
    assert scalar_quartic_permutation_residual < 5e-8

    # The two stored four-vector color channels inherit the same pair
    # symmetries as products of structure constants.
    color_a = api.quartic_color(ids[0], ids[1], ids[2], ids[3])
    color_b = api.quartic_color(ids[2], ids[3], ids[0], ids[1])
    gauge_quartic_pair_residual = abs(color_a-color_b)
    assert gauge_quartic_pair_residual < 2e-11

    inherited_scalar = json.loads((HERE.parents[1] / "calculations" /
        "canonical_so10_direct_two_loop_gauge_scalar_threshold" /
        "scalar_vertex_oracle.json").read_text())
    controls = inherited_scalar["selected_exact_controls"]
    assert controls == {
        "zEta_quartic": "384",
        "z6_cubic": "2",
        "zK_vev_induced_cubic": "6",
        "lambdaS_fourth_derivative": "24",
    }

    payload = {
        "outcome": "PHYSICAL_VERTEX_API_CORE_REGRESSION_PASS",
        "physical_basis_sha256": PHYSICAL_BASIS_HASH,
        "background_field_quadratic_sha256": QUADRATIC_HASH,
        "max_vss_antisymmetry_residual": abs(vss_ij+vss_ji),
        "max_vvss_exchange_residual": max(abs(q1-q2), abs(q1-q3)),
        "jacobi_residual": abs(jacobi),
        "max_vector_ghost_mass_pairing_residual": max_pairing,
        "max_tree_fp_vvs_ward_residual": max(ward_residuals),
        "physical_scalar_cubic_permutation_residual": scalar_permutation_residual,
        "physical_scalar_quartic_permutation_residual":
            scalar_quartic_permutation_residual,
        "gauge_quartic_pair_residual": gauge_quartic_pair_residual,
        "inherited_exact_scalar_controls": controls,
    }
    (HERE / "physical_vertex_api_regression.json").write_text(
        json.dumps(payload, indent=2) + "\n")
    print(payload["outcome"])
    for key, value in payload.items():
        if key.endswith("residual"):
            print(key, value)


if __name__ == "__main__":
    main()
