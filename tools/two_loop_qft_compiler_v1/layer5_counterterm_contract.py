"""Compile the earned layer-5 counterterm contract.

This module deliberately separates two notions that are easy to conflate:

* the counterterm *action/slot structure*, fixed by multiplicative
  renormalization of the frozen parent action; and
* the one-loop pole residues multiplying that structure.

The first is derived here.  Only the parent gauge/background-field residue is
already fixed by an earned calculation.  Missing pole residues remain named
dependencies rather than being fitted from future two-loop cancellations.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent

ACTION_HASH = "2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491"
PHYSICAL_BASIS_HASH = (
    "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e"
)
TOPOLOGY_HASH = "778fe1a80234f7f5fc3c9cbdd02d465bf351f2958d509ef16fc9d2a6c0806021"
VERTEX_HASH = "1a7ddef7a9df34c8827317325ee4f34d0ac09e684c4cba99dded88da6667b567"
SPECIES_HASH = "46f35ed04bff58cd9afd3673da724c376209cac0cd3cd4a15ff252d6ad1ae837"


# Multiplicities refer to the unshifted parent fields; a conjugate has the
# same wave-function counterterm as its field.  These 29 rows are precisely
# the 24 real and five complex coefficient families of PARENT_ACTION_V1.
MONOMIALS = {
    "mPhi2": (2, {"Phi": 2}),
    "mSigma2": (2, {"Sigma": 2}),
    "mphi2": (2, {"phi": 2}),
    "mS2": (2, {"S": 2}),
    "muPhi": (3, {"Phi": 3}),
    "muPhiPhi": (3, {"Phi": 1, "phi": 2}),
    "z6": (3, {"phi": 2, "S": 1}),
    "lambdaPhi1": (4, {"Phi": 4}),
    "lambdaPhi2": (4, {"Phi": 4}),
    "lambdaPhiSigma1": (4, {"Phi": 2, "Sigma": 2}),
    "lambdaPhiSigma2": (4, {"Phi": 2, "Sigma": 2}),
    "lambdaPhiphi1": (4, {"Phi": 2, "phi": 2}),
    "lambdaPhiphi2": (4, {"Phi": 2, "phi": 2}),
    "lambdaPhiS": (4, {"Phi": 2, "S": 2}),
    "lambdaSigma1": (4, {"Sigma": 4}),
    "lambdaSigma2": (4, {"Sigma": 4}),
    "lambdaSigma3": (4, {"Sigma": 4}),
    "lambdaSigma4": (4, {"Sigma": 4}),
    "lambdaSigmaphi1": (4, {"Sigma": 2, "phi": 2}),
    "lambdaSigmaphi2": (4, {"Sigma": 2, "phi": 2}),
    "lambdaPhiVector1": (4, {"phi": 4}),
    "lambdaPhiVector2": (4, {"phi": 4}),
    "lambdaSigmaS": (4, {"Sigma": 2, "S": 2}),
    "lambdaVectorS": (4, {"phi": 2, "S": 2}),
    "lambdaS": (4, {"S": 4}),
    "z4": (4, {"Phi": 1, "Sigma": 2, "S": 1}),
    "zK": (4, {"Phi": 1, "phi": 2, "S": 1}),
    "zEta": (4, {"Sigma": 3, "phi": 1}),
    "zD": (4, {"Sigma": 2, "phi": 2}),
}

COMPLEX_COEFFICIENTS = {"z6", "z4", "zK", "zEta", "zD"}


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def field_factor(counts):
    terms = []
    for field in ("Phi", "Sigma", "phi", "S"):
        count = counts.get(field, 0)
        if count:
            terms.append(f"{count}/2*deltaZ_{field}")
    return " + ".join(terms) if terms else "0"


def parameter_rows():
    rows = []
    for name, (degree, counts) in MONOMIALS.items():
        mu_power = degree - 2
        rows.append({
            "coefficient": name,
            "coefficient_reality": (
                "complex_plus_Hermitian_conjugate"
                if name in COMPLEX_COEFFICIENTS else "real"
            ),
            "field_degree": degree,
            "field_multiplicities": counts,
            "bare_definition": (
                f"{name}_0=mu^({mu_power}*epsilon)*({name}+delta_{name})"
            ),
            "expanded_operator_coefficient": (
                f"delta_{name} + {name}*({field_factor(counts)})"
            ),
        })
    return rows


SLOT_KERNELS = {
    "field": {
        "expression": "CT_FIELD(line)=deltaZ_line*D_inverse_kinetic(line)",
        "provenance": "bare_field_expansion",
        "residue_dependency": "field_two_point_UV_pole",
    },
    "mass": {
        "expression": "CT_MASS(line)=deltaM2_line",
        "provenance": "parent_mass_and_shifted_potential_counterterm",
        "residue_dependency": "parent_scalar_and_vector_mass_UV_poles",
    },
    "gauge_parameter": {
        "expression": (
            "CT_GAUGE_PARAMETER(line)=delta_xi*d(D_inverse_line)/d_xi"
        ),
        "provenance": "single_frozen_partial_BFM_BRST_action",
        "residue_dependency": "quantum_vector_gauge_parameter_UV_pole",
    },
    "gauge_coupling": {
        "expression": (
            "CT_G_VERTEX=(delta_g*d/dg+1/2*sum_external_deltaZ)"
            "*V_tree"
        ),
        "provenance": "bare_gauge_and_field_expansion",
        "residue_dependency": "delta_g_known_other_field_residues_required",
    },
    "VEV": {
        "expression": "CT_VEV=sum_r(delta_v_r*d(V_tree)/d(v_r))",
        "provenance": "frozen_FJ_like_explicit_tadpole_shift",
        "residue_dependency": "one_point_UV_poles_and_background_scalar_Z",
    },
    "tadpole": {
        "expression": "CT_TADPOLE=sum_r(delta_t_r*d(V_tree)/d(t_r))",
        "provenance": "frozen_FJ_like_explicit_tadpole_shift",
        "residue_dependency": "one_point_UV_poles",
    },
    "vertex": {
        "expression": (
            "CT_VERTEX=[sum_a(delta_c_a*d/dc_a)+"
            "1/2*sum_fields(deltaZ_field*q_field*d/dq_field)]*V_tree"
        ),
        "provenance": "parent_Spin10_invariant_counterterm_action",
        "residue_dependency": "parent_2_3_4_point_UV_poles",
    },
}


def slot_rows(topology):
    rows = []
    for slot in topology["one_loop_with_counterterm_slots"]:
        kernel = SLOT_KERNELS[slot["counterterm_kind"]]
        rows.append({
            **slot,
            "coefficient": kernel["expression"],
            "coefficient_status": "STRUCTURAL_EXPRESSION_POPULATED_RESIDUE_PENDING",
            "provenance": kernel["provenance"],
            "residue_dependency": kernel["residue_dependency"],
        })
    return rows


def manifest():
    topology = json.loads((HERE / "layer4_topologies.json").read_text(
        encoding="utf-8"))
    catalog = json.loads((HERE / "layer4_vertex_catalog.json").read_text(
        encoding="utf-8"))
    species = json.loads((HERE / "layer4_species_diagrams.json").read_text(
        encoding="utf-8"))
    assert topology["topology_inventory_sha256"] == TOPOLOGY_HASH
    assert catalog["vertex_catalog_sha256"] == VERTEX_HASH
    assert species["species_inventory_sha256"] == SPECIES_HASH
    assert topology["immutable_partial_bfm_action_sha256"] == ACTION_HASH
    assert len(topology["one_loop_with_counterterm_slots"]) == 21

    b10 = Fraction(-34, 3)
    gauge = {
        "pole_unit": "P10=g10^2/(16*pi^2*epsilon_bar)",
        "b10": str(b10),
        "deltaZ_g10": f"({b10 / 2})*P10",
        "deltaZ_background_Spin10": f"({-b10})*P10",
        "background_Ward_identity": (
            "deltaZ_g10+1/2*deltaZ_background_Spin10=0"
        ),
        "ward_identity_residual": str(b10 / 2 + (-b10) / 2),
        "authority": "earned_parent_one_loop_beta_replay",
    }
    required = [
        "deltaZ_quantum_Spin10_in_partial_BFM_Rxi",
        "deltaZ_Phi", "deltaZ_Sigma", "deltaZ_phi", "deltaZ_S",
        "deltaZ_heavy_ghost", "deltaZ_light_ghost", "delta_xi",
        "delta_parent_quadratic_4", "delta_parent_cubic_4_real_directions",
        "delta_parent_quartic_26_real_directions",
        "delta_v_Phi", "delta_v_Sigma", "delta_v_S",
        "delta_t_Phi", "delta_t_Sigma", "delta_t_S",
        "selected_scalar_2_and_3_point_UV_pole_controls",
    ]
    payload = {
        "outcome": "LAYER5_COUNTERTERM_ACTION_STRUCTURE_PASS_RESIDUES_BLOCKED",
        "immutable_inputs": {
            "partial_bfm_action_sha256": ACTION_HASH,
            "physical_basis_sha256": PHYSICAL_BASIS_HASH,
            "layer4_topology_sha256": TOPOLOGY_HASH,
            "layer4_vertex_catalog_sha256": VERTEX_HASH,
            "layer4_species_inventory_sha256": SPECIES_HASH,
        },
        "scheme": {
            "regularization": "dimensional_regularization_d_4_minus_2epsilon",
            "subtraction": "MSbar",
            "field_renormalization": "q0=Z_q^(1/2)*q",
            "coefficient_scaling": "c_n0=mu^((n-2)*epsilon)*(c_n+delta_c_n)",
            "tadpole_VEV_prescription": (
                "FJ_like_explicit_tadpole_shift: parent parameters remain MSbar; "
                "v0=Z_background_scalar^(1/2)*(v+Delta_v); Delta_v and delta_t "
                "are fixed from the same renormalized one_point conditions and "
                "are used in scalar, Goldstone, ghost, and vector sectors"
            ),
            "forbidden": "mixing_tadpole_or_VEV_prescriptions_between_sectors",
        },
        "parent_operator_basis": {
            "real_coefficient_families": 24,
            "complex_coefficient_families": 5,
            "real_Hermitian_directions": 34,
            "rows": parameter_rows(),
            "bare_expansion_closure": "PASS_SAME_29_MONOMIAL_FAMILIES",
            "radiative_pole_closure": "NOT_YET_TESTED_MISSING_ONE_LOOP_POLE_EVALUATOR",
        },
        "known_gauge_counterterm": gauge,
        "goldstone_mass_counterterm_identity": (
            "delta(xi*M_V^2)=M_V^2*delta_xi+xi*deltaM_V^2; "
            "deltaM_V^2 is derived from delta_g, background-field/VEV shifts, "
            "and the same parent kinetic action"
        ),
        "counterterm_slots": slot_rows(topology),
        "slot_count": 21,
        "all_slot_structures_populated": True,
        "all_slot_pole_residues_derived": False,
        "missing_required_one_loop_residues": required,
        "blocking_layer": (
            "one_loop_1PI_UV_pole_evaluator_for_parent_scalar_1_2_3_4_point_"
            "and_partial_BFM_quantum_vector_ghost_amplitudes"
        ),
        "not_started": [
            "tensor_IBP_reduction", "master_integral_evaluation",
            "two_loop_amplitude_assembly", "finite_C1_GS",
        ],
    }
    payload["counterterm_contract_sha256"] = canonical_hash(payload)
    return payload


def main():
    payload = manifest()
    (HERE / "layer5_counterterm_contract.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("PARENT_MONOMIAL_FAMILIES", len(payload["parent_operator_basis"]["rows"]))
    print("COUNTERTERM_SLOTS_STRUCTURALLY_POPULATED", payload["slot_count"])
    print("KNOWN_GAUGE_WARD_RESIDUAL", payload["known_gauge_counterterm"]["ward_identity_residual"])
    print("MISSING_POLE_RESIDUES", len(payload["missing_required_one_loop_residues"]))
    print("COUNTERTERM_CONTRACT_SHA256", payload["counterterm_contract_sha256"])


if __name__ == "__main__":
    main()
