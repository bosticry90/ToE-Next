"""Regress the complete partial-BFM action façade and new ghost sector."""

import json
import math
from pathlib import Path

from partial_bfm_action import PartialBFMAction


HERE = Path(__file__).resolve().parent


def main():
    action = PartialBFMAction()
    manifest = action.manifest()
    assert manifest["outcome"] == "PARTIAL_BFM_ACTION_PASS"
    assert manifest["field_ledger"]["heavy_vectors"] == 33
    assert manifest["field_ledger"]["heavy_ghosts_complex"] == 33
    assert manifest["field_ledger"]["light_ghosts_complex"] == 12

    max_mass_pairing = 0.0
    for xi in (.5, 1.0, 2.0):
        for field in action.heavy_vector_ids:
            index = action.invariant.vector_index(field)
            residual = abs(action.heavy_ghost_mass(field, field, xi)
                           - xi * action.invariant.vector_masses[index])
            max_mass_pairing = max(max_mass_pairing, residual)
    assert max_mass_pairing < 2e-12

    # Locate a nonzero H action on the heavy-vector representation.  This
    # supplies a nonzero quartic equivariant-ghost control without baking a
    # basis-dependent index choice into the test.
    control = None
    for alpha in action.light_vector_ids:
        for left in action.heavy_vector_ids:
            for right in action.heavy_vector_ids:
                value = action.structure(left, right, alpha)
                if abs(value) > 1e-10:
                    control = (left, right, alpha, value)
                    break
            if control:
                break
        if control:
            break
    assert control is not None
    left, right, alpha, structure = control
    q_half = action.heavy_ghost_quartic(left, right, left, right, .5)
    q_one = action.heavy_ghost_quartic(left, right, left, right, 1.0)
    q_two = action.heavy_ghost_quartic(left, right, left, right, 2.0)
    assert abs(q_one) > 1e-12
    assert abs(q_one - 2*q_half) < 2e-12
    assert abs(q_two - 2*q_one) < 2e-12
    assert abs(action.heavy_ghost_quartic(
        right, left, left, right, 1.0) + q_one) < 2e-12
    assert abs(action.heavy_ghost_quartic(
        left, right, right, left, 1.0) + q_one) < 2e-12

    derivative = action.heavy_ghost_vector_derivative(left, right, alpha)
    assert abs(derivative-structure) < 2e-12
    background = action.heavy_ghost_background_vector(left, right, alpha)
    assert abs(background-structure) < 2e-12
    goldstone = action.heavy_ghost_goldstone(left, right, left, 1.0)
    assert math.isfinite(goldstone)

    light_control = None
    for a in action.light_vector_ids:
        for b in action.light_vector_ids:
            for c in action.light_vector_ids:
                value = action.light_ghost_vector(a, b, c)
                if abs(value) > 1e-10:
                    light_control = (a, b, c, value)
                    break
            if light_control:
                break
        if light_control:
            break
    assert light_control is not None

    # The façade must reproduce its invariant parent backend rather than
    # maintain a competing gauge-invariant vertex implementation.
    delegated_vss = action.vss("X000", "H000", "H001")
    backend_vss = action.invariant.vss("X000", "H000", "H001")
    assert abs(delegated_vss-backend_vss) < 2e-12

    payload = {
        "outcome": "PARTIAL_BFM_ACTION_REGRESSION_PASS",
        "partial_bfm_action_sha256": manifest["partial_bfm_action_sha256"],
        "max_heavy_ghost_mass_pairing_residual": max_mass_pairing,
        "max_goldstone_pairing_orthogonality_residual":
            action.goldstone_pairing_residual,
        "max_goldstone_pairing_reconstruction_residual":
            action.goldstone_reconstruction_residual,
        "max_heavy_mass_H_covariance_residual":
            action.max_h_covariance_mass_commutator,
        "quartic_heavy_ghost_control": {
            "heavy_i": left,
            "heavy_j": right,
            "light_alpha": alpha,
            "structure_constant": structure,
            "kernel_at_xi_1": q_one,
            "xi_scaling_pass": True,
            "grassmann_pair_antisymmetry_pass": True,
        },
        "invariant_backend_delegation_pass": True,
        "heavy_ghost_background_vertex_pass": True,
        "heavy_ghost_goldstone_vertex_finite": goldstone,
        "light_ghost_vertex_control": {
            "antighost": light_control[0],
            "ghost": light_control[1],
            "vector": light_control[2],
            "coefficient": light_control[3],
        },
    }
    (HERE / "partial_bfm_action_regression.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("MAX_HEAVY_GHOST_MASS_PAIRING_RESIDUAL", max_mass_pairing)
    print("QUARTIC_HEAVY_GHOST_CONTROL", left, right, alpha, q_one)


if __name__ == "__main__":
    main()
