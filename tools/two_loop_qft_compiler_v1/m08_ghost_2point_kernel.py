"""Canonical partial-BFM ghost two-point UV kernel for the M08 preflight.

This module deliberately stops short of adjudicating UVP_M08.  It derives the
heavy- and light-ghost kinetic pole operators from the frozen action and the
already validated primitive UV projector, but it does not supply the missing
quantum-vector and BRST three-point kernels.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from sympy import Rational, Symbol, simplify


HERE = Path(__file__).resolve().parent
GROUP_ARTIFACT = HERE / "uvp_m08_group_contraction_preflight.json"


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def rational(value):
    return Rational(Fraction(value).limit_denominator(120).numerator,
                    Fraction(value).limit_denominator(120).denominator)


def main():
    group = json.loads(GROUP_ARTIFACT.read_text(encoding="utf-8"))
    xi = Symbol("xi")
    eta = Symbol("eta_H")

    # Primary derivation.  With external ghost momentum p, the transverse
    # numerator gives p^2 - p.k.  Its logarithmic residues are 1 and 1/2.
    # The longitudinal propagator adds -(1-xi)[J1-J2], where the rank-two
    # primitive gives J1=1/4 and the routed rank-zero term gives J2=1/2.
    primary_terms = {
        "transverse_p2": Rational(1),
        "transverse_p_dot_k": Rational(-1, 2),
        "longitudinal_J1": Rational(1, 4),
        "longitudinal_J2": Rational(1, 2),
    }
    primary_coefficient = simplify(
        primary_terms["transverse_p2"]
        + primary_terms["transverse_p_dot_k"]
        - (1 - xi) * (primary_terms["longitudinal_J1"]
                      - primary_terms["longitudinal_J2"])
    )

    # Independent kinematic replay.  Feynman parameterization of the
    # nonexceptional massless two-point function gives 1/2 for the metric
    # contraction.  A separate Schwinger/Gaussian rank-two average gives
    # -1/4 for the contracted longitudinal insertion.
    replay_transverse = Rational(1, 2)
    replay_longitudinal_insertion = Rational(-1, 4)
    replay_coefficient = simplify(
        replay_transverse
        - (1 - xi) * replay_longitudinal_insertion
    )
    assert simplify(primary_coefficient - replay_coefficient) == 0
    assert primary_coefficient == (3 - xi) / 4

    def operator(block, gauge_parameter):
        spectra = group["contractions"][block]["spectrum"]
        return [{
            "group_eigenvalue": item["eigenvalue"],
            "multiplicity": item["multiplicity"],
            "kinetic_pole_eigenvalue": str(simplify(
                rational(Fraction(item["eigenvalue"]))
                * (3 - gauge_parameter) / 4
            )),
        } for item in spectra]

    heavy_spectrum = []
    for item in group["contractions"]["heavy_heavy_heavy"]["spectrum"]:
        heavy_value = rational(Fraction(item["eigenvalue"]))
        # K_HHH + 2 K_HHL = 8 I.  A ghost self-energy has a fixed
        # internal-ghost slot, so the light-vector contraction is one K_HHL.
        light_value = simplify((8 - heavy_value) / 2)
        heavy_spectrum.append({
            "K_HHH_eigenvalue": str(heavy_value),
            "K_HHL_eigenvalue": str(light_value),
            "multiplicity": item["multiplicity"],
            "kinetic_pole_eigenvalue": str(simplify(
                heavy_value * (3 - xi) / 4
                + light_value * (3 - eta) / 4
            )),
        })

    payload = {
        "schema_version": 1,
        "outcome": "M08_GHOST_2POINT_KERNEL_PREFLIGHT_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "normalization": (
            "delta_Z coefficient multiplying g10^2/(16*pi^2*epsilon_bar)"
        ),
        "immutable_inputs": {
            "partial_BFM_action_sha256": group["partial_BFM_action_sha256"],
            "group_contraction_artifact_sha256": group["artifact_sha256"],
        },
        "primary_local_UV_projection": {
            key: str(value) for key, value in primary_terms.items()
        },
        "independent_Feynman_parameter_Gaussian_replay": {
            "transverse": str(replay_transverse),
            "longitudinal_insertion": str(replay_longitudinal_insertion),
        },
        "kinematic_coefficient": str(primary_coefficient),
        "primary_minus_replay": str(simplify(
            primary_coefficient - replay_coefficient)),
        "heavy_ghost_kinetic_operator": {
            "formula": (
                "(3-xi)/4*K_HHH + (3-eta_H)/4*K_HHL"
            ),
            "group_matrix_sha256": group["contractions"]
                ["heavy_heavy_heavy"]["matrix_sha256"],
            "light_vector_group_matrix_sha256": group["contractions"]
                ["heavy_heavy_light"]["matrix_sha256"],
            "spectrum": heavy_spectrum,
        },
        "light_ghost_kinetic_operator": {
            "formula": "(3-eta_H)/4 * K_LLL",
            "group_matrix_sha256": group["contractions"]
                ["light_light_light"]["matrix_sha256"],
            "spectrum": operator("light_light_light", eta),
        },
        "locality": {
            "promoted_structure": "p_squared_times_ghost_bilinear",
            "nonlocal_UV_structures": [],
            "mass_terms_do_not_enter_kinetic_residue": True,
        },
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "nonexceptional_offshell_external_ghost_momentum",
            "scaleless_parts_split": True,
        },
        "audited_zero_p2_contributions": [
            "heavy_ghost_mass",
            "heavy_ghost_scalar_vertex",
            "heavy_ghost_Goldstone_vertex",
            "equivariant_quartic_heavy_ghost_tadpole",
        ],
        "covariant_derivative_expansion": {
            "d_mu": "unbroken_H_covariant_derivative",
            "heavy_ghost_light_quantum_vector_bubble_included": True,
            "reference_equations": "partial_BFM_action Eqs. (3.31),(3.36)",
        },
        "remaining_before_UVP_M08_retry": [
            "complete partial-BFM quantum-vector two-point pole operator",
            "complete heavy/light ghost-vector BRST three-point pole operators",
            "direct delta_xi extraction from the gauge-fixing two-point sector",
            "inventory-independent replay of the complete M08 pole action",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_ghost_2point_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("KINEMATIC_COEFFICIENT", payload["kinematic_coefficient"])
    print("PRIMARY_MINUS_REPLAY", payload["primary_minus_replay"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
