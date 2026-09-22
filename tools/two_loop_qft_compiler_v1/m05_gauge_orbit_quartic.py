"""Exact gauge-orbit quartic invariant needed by the M05 gauge completion.

For a parent scalar background q, define the gauge mass Gram matrix

    K_ab(q) = <T_a q, T_b q>

in the canonical real kinetic metric and normalized generator basis.  The
gauge-generated one-loop potential is proportional to Tr K(q)^2.  This module
projects that invariant polynomial on the frozen rank-26 scalar basis.  It
does not assign the partial-BFM loop coefficient or claim xi cancellation;
those remain part of the full M05 gauge-sector assembly.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys

from sympy import I, Matrix, simplify, sqrt, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [
    str(HERE),
    str(ROOT / "calculations" / "canonical_so10_vacuum_kernel"),
    str(ROOT / "calculations" / "canonical_so10_scalar_reconstruction"),
]

from certify_sigma_quartics import generated_form
from compile_real_field_basis import real_kinetic_inner
from derive_stabilizers import form_action, generators
from m05_parent_scalar_kernel import projector_backgrounds
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from parent_bilinear_oracle import State


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def gauge_action(raw_generator, state):
    normalization = sqrt(2)
    return State(
        (raw_generator * state.Phi - state.Phi * raw_generator) / normalization,
        {key: (a / normalization, b / normalization)
         for key, (a, b) in form_action(raw_generator, state.Sigma).items()},
        tuple(sum(raw_generator[i, j] * state.phi[j] for j in range(10))
              / normalization for i in range(10)),
        0,
    )


def orbit_quartic(state):
    orbit = [gauge_action(generator, state) for _, generator in generators()]
    total = 0
    for a, left in enumerate(orbit):
        for b in range(a, len(orbit)):
            value = real_kinetic_inner(left, orbit[b])
            total += (1 if a == b else 2) * value * value
    return simplify(total)


def verification_background():
    form = generated_form(901, 9)
    p = zeros(10)
    diagonal = (2, -1, 0, 1, -2, 1, 0, -1, 2, -2)
    for i, value in enumerate(diagonal):
        p[i, i] = value
    p[0, 7] = p[7, 0] = 2
    vector = (1 + 2 * I, 0, 0, -2, 0, I, 0, 0, 0, 1)
    return State(p, form, vector, 2 - I)


def compute_projection():
    backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]
    assert len(backgrounds) == 26
    invariant_matrix = Matrix([physical_quartics(state)
                               for state in backgrounds])
    assert invariant_matrix.rank() == 26
    values = Matrix([orbit_quartic(state) for state in backgrounds])
    coefficients = tuple(simplify(value)
                         for value in invariant_matrix.inv() * values)
    verify = verification_background()
    verification_residual = simplify(
        orbit_quartic(verify)
        - sum(coefficient * value for coefficient, value in zip(
            coefficients, physical_quartics(verify)
        ))
    )
    assert verification_residual == 0
    nonzero = {
        name: str(value) for name, value in zip(
            REAL_DIRECTION_NAMES, coefficients
        ) if value != 0
    }
    inventory = {
        "generator_count": 45,
        "generator_normalization": "Tr10(TaT Tb)=delta_ab",
        "kinetic_metric": "canonical_328_real",
        "projector_backgrounds": 26,
        "verification_backgrounds": 1,
        "nonzero_projected_directions": len(nonzero),
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_GAUGE_ORBIT_QUARTIC_PROJECTION_PASS",
        "authority": "GAUGE_INVARIANT_COMPONENT_ONLY_NOT_UVP_M05_PASS",
        "polynomial": "Tr[K(q)^2], K_ab=<Ta q,Tb q>",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "projected_coefficients": nonzero,
        "rank": 26,
        "verification_residual": "0",
        "not_assigned": [
            "partial-BFM one-loop prefactor",
            "vector/Goldstone/ghost sector split",
            "xi cancellation",
            "M02 field conversion",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_projection()
    (HERE / "uvp_m05_gauge_orbit_quartic.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("NONZERO_DIRECTIONS", result["inventory"]["nonzero_projected_directions"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
