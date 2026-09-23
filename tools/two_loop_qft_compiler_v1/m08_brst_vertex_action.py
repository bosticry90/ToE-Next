"""Action-derived M08 ghost/vector vertex surface.

This module is implementation evidence only.  It expands the immutable
partial-BFM action into the tree signatures needed by the three canonical
ghost--vector 1PI processes.  Coefficients remain index tensors evaluated by
``PartialBFMAction``; no independently maintained numerical vertex table is
introduced.
"""

from hashlib import sha256
import json
from pathlib import Path

from partial_bfm_action import PartialBFMAction


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def build_vertex_surface():
    # ``momentum_rule`` uses incoming momenta.  pbar and pghost name the
    # antighost and ghost momenta.  The rules follow by differentiating the
    # displayed action, not by copying a Feynman-rule catalog.
    cubic = [
        {
            "vertex_id": "HGH_ubar_u_V",
            "fields": ["ubar_H", "u_H", "V_H"],
            "source": "bar_u_i*f_i_j_k*V_k_mu*d_mu*u_j",
            "momentum_rule": "pghost_mu",
            "color_method": "heavy_ghost_vector_derivative",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "HGH_ubar_u_q",
            "fields": ["ubar_H", "u_H", "q_L"],
            "source": "-bar_u_i*d_squared*u_i",
            "momentum_rule": "(pbar-pghost)_mu",
            "color_method": "heavy_ghost_light_quantum_vector",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "LGH_cbar_c_q",
            "fields": ["cbar_L", "c_L", "q_L"],
            "source": "-bar_c_alpha*partial_mu*(partial_mu*c+f*q*c)",
            "momentum_rule": "pbar_mu",
            "color_method": "light_ghost_quantum_vector",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "YM_V_V_V",
            "fields": ["V_H", "V_H", "V_H"],
            "source": "parent_Yang_Mills",
            "momentum_rule": "standard_three_vector",
            "color_method": "structure",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "YM_q_V_V",
            "fields": ["q_L", "V_H", "V_H"],
            "source": "parent_Yang_Mills",
            "momentum_rule": "standard_three_vector",
            "color_method": "structure",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "YM_q_q_q",
            "fields": ["q_L", "q_L", "q_L"],
            "source": "parent_Yang_Mills",
            "momentum_rule": "standard_three_vector",
            "color_method": "structure",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "HGH_ubar_u_G",
            "fields": ["ubar_H", "u_H", "G_H"],
            "source": "xi*bar_u*(f*M*chi)*u",
            "momentum_rule": "1",
            "color_method": "heavy_ghost_goldstone",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 1,
        },
        {
            "vertex_id": "HGH_ubar_u_S",
            "fields": ["ubar_H", "u_H", "S_phys"],
            "source": "xi*bar_u*(f*x*varphi)*u",
            "momentum_rule": "1",
            "color_method": "heavy_ghost_scalar",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 1,
        },
        {
            "vertex_id": "KIN_q_G_G",
            "fields": ["q_L", "G_H", "G_H"],
            "source": "canonical_scalar_kinetic_action",
            "momentum_rule": "scalar_current",
            "color_method": "vss",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "KIN_V_G_G",
            "fields": ["V_H", "G_H", "G_H"],
            "source": "canonical_scalar_kinetic_action",
            "momentum_rule": "scalar_current",
            "color_method": "vss",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "KIN_q_S_S",
            "fields": ["q_L", "S_phys", "S_phys"],
            "source": "canonical_scalar_kinetic_action",
            "momentum_rule": "scalar_current",
            "color_method": "vss",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
        {
            "vertex_id": "KIN_V_S_S",
            "fields": ["V_H", "S_phys", "S_phys"],
            "source": "canonical_scalar_kinetic_action",
            "momentum_rule": "scalar_current",
            "color_method": "vss",
            "coupling_power_g10": 1,
            "dimensionful_coupling_power": 0,
        },
    ]
    quartic = [
        {
            "vertex_id": "HGH4_ubar_u_V_V",
            "fields": ["ubar_H", "u_H", "V_H", "V_H"],
            "source": "bar_u*f_i_k_alpha*f_alpha_l_j*V_k*V_l*u",
            "momentum_rule": "metric_mu_nu",
            "color_method": "heavy_ghost_two_heavy_vectors_vertex",
            "coupling_power_g10": 2,
        },
        {
            "vertex_id": "HGH4_ubar_u_V_q",
            "fields": ["ubar_H", "u_H", "V_H", "q_L"],
            "source": "bar_u*f_i_j_k*V_k*d_mu*u_j|linear_q",
            "momentum_rule": "metric_mu_nu",
            "color_method": "heavy_ghost_mixed_vector_vertex",
            "coupling_power_g10": 2,
        },
        {
            "vertex_id": "HGH4_ubar_u_q_q",
            "fields": ["ubar_H", "u_H", "q_L", "q_L"],
            "source": "-bar_u*d_squared*u|quadratic_q",
            "momentum_rule": "metric_mu_nu",
            "color_method": "heavy_ghost_two_light_vectors_vertex",
            "coupling_power_g10": 2,
        },
        {
            "vertex_id": "HGH4_ubar_u_ubar_u",
            "fields": ["ubar_H", "u_H", "ubar_H", "u_H"],
            "source": "equivariant_quartic_heavy_ghost",
            "momentum_rule": "1",
            "color_method": "heavy_ghost_quartic_direct_minus_exchange",
            "coupling_power_g10": 2,
        },
    ]
    return cubic, quartic


def main():
    action = PartialBFMAction()
    cubic, quartic = build_vertex_surface()

    # Exercise every newly exposed action-derived color method on certified
    # field IDs.  This is a facade regression, not a residue calculation.
    hi, hj, hk = action.heavy_vector_ids[:3]
    la, lb = action.light_vector_ids[:2]
    samples = {
        "HGH_ubar_u_V": action.heavy_ghost_vector_derivative(hi, hj, hk),
        "HGH_ubar_u_q": action.heavy_ghost_light_quantum_vector(hi, hj, la),
        "LGH_cbar_c_q": action.light_ghost_quantum_vector(la, lb, la),
        "HGH4_ubar_u_V_V": action.heavy_ghost_two_heavy_vectors_vertex(
            hi, hj, hk, hi),
        "HGH4_ubar_u_V_q": action.heavy_ghost_mixed_vector_vertex(
            hi, hj, hk, la),
        "HGH4_ubar_u_q_q": action.heavy_ghost_two_light_vectors_vertex(
            hi, hj, la, lb),
    }
    payload = {
        "schema_version": 1,
        "outcome": "M08_ACTION_DERIVED_BRST_VERTEX_SURFACE_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action.manifest()[
            "partial_bfm_action_sha256"],
        "derivation_policy": (
            "all_vertices_are_differentiated_facades_over_the_frozen_action"
        ),
        "covariant_derivative": {
            "d_mu": "unbroken_H_covariant_derivative",
            "quantum_q_vertex_materialized": True,
            "mixed_V_q_seagull_materialized": True,
        },
        "cubic_vertices": cubic,
        "quartic_vertices": quartic,
        "sample_action_method_values": {
            key: format(float(value), ".17g")
            for key, value in samples.items()
        },
        "external_processes": [
            ["ubar_H", "u_H", "V_H"],
            ["ubar_H", "u_H", "q_L"],
            ["cbar_L", "c_L", "q_L"],
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_vertex_surface.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("CUBIC_VERTICES", len(cubic))
    print("QUARTIC_VERTICES", len(quartic))
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
