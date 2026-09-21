"""Freeze the layer-5A UV-pole evaluator contract and minimum controls.

This file emits a test specification only.  It contains no UV-pole evaluator
and no model counterterm residue.
"""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent

HASHES = {
    "parent_action_sha256": "01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed",
    "partial_bfm_action_sha256": "2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491",
    "physical_basis_sha256": "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e",
    "layer4_topology_sha256": "778fe1a80234f7f5fc3c9cbdd02d465bf351f2958d509ef16fc9d2a6c0806021",
    "layer4_vertex_catalog_sha256": "1a7ddef7a9df34c8827317325ee4f34d0ac09e684c4cba99dded88da6667b567",
    "layer4_species_inventory_sha256": "46f35ed04bff58cd9afd3673da724c376209cac0cd3cd4a15ff252d6ad1ae837",
    "layer5_counterterm_contract_sha256": "87cf0b4966451c62168552284cb1c709c5e3247d8e1b8241e34d4b78116c48f1",
}

V1_CONTRACT_SHA256 = (
    "f4cf741afed95657b8c8c80ff178147189f35c7db42a8fdcea95e8ed3ae3f588"
)


def primitive(test_id, target, requirement, adversary):
    return {
        "test_id": test_id,
        "target": target,
        "requirement": requirement,
        "adversarial_failure": adversary,
    }


def theory(test_id, theory_name, amplitude, requirement, convention):
    return {
        "test_id": test_id,
        "theory": theory_name,
        "amplitude": amplitude,
        "requirement": requirement,
        "normalization_convention": convention,
    }


def model(test_id, target, requirement):
    return {"test_id": test_id, "target": target, "requirement": requirement}


def canonical_hash(payload):
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(packed.encode()).hexdigest()


def build():
    primitives = [
        primitive("UVP_P01", "massive_rank0_tadpole",
                  "exact_1_over_epsilon_bar_pole_in_frozen_Euclidean_to_Minkowski_convention",
                  "wrong_mass_sign_or_d_minus_4_normalization"),
        primitive("UVP_P02", "massive_rank0_log_bubble",
                  "mass_independent_logarithmic_UV_residue",
                  "retaining_finite_mass_terms_in_the_pole"),
        primitive("UVP_P03", "doubled_propagator_mass_derivative",
                  "commutes_with_mass_derivative_of_the_tadpole_pole",
                  "wrong_doubled_line_power_or_sign"),
        primitive("UVP_P04", "rank2_tensor_vacuum_integral",
                  "d_dimensional_symmetric_tensor_reduction_before_epsilon_expansion",
                  "setting_d_equal_4_before_pole_times_epsilon_terms_are_resolved"),
        primitive("UVP_P05", "rank4_and_rank6_tensor_vacuum_integrals",
                  "exact_metric_symmetrization_and_dimension_denominators",
                  "missing_pairings_or_wrong_tensor_multiplicity"),
        primitive("UVP_P06", "external_momentum_Taylor_expansion",
                  "local_expansion_through_p_squared_for_two_point_functions_and_one_derivative_for_three_point_functions",
                  "under_expansion_or_nonlocal_pole_output"),
        primitive("UVP_P07", "unequal_mass_bubble",
                  "UV_pole_independent_of_mass_routing_while_local_mass_terms_remain_correct",
                  "mass_assignment_dependent_log_pole"),
        primitive("UVP_P08", "loop_momentum_routing_shift",
                  "identical_UV_residue_for_two_independent_routings",
                  "surface_term_or_routing_dependence"),
        primitive("UVP_P09", "one_loop_total_derivative_IBP_identity",
                  "zero_exact_residual_in_d_dimensions",
                  "four_dimensional_tensor_reduction_used_too_early"),
        primitive("UVP_P10", "auxiliary_mass_independence",
                  "cancel_auxiliary_mass_after_all_local_IR_rearrangement_counterterms_are_included",
                  "unphysical_auxiliary_mass_in_final_counterterm"),
        primitive("UVP_P11", "scaleless_integral_UV_IR_split",
                  "record_UV_and_IR_poles_separately_before_their_dimensional_regularization_sum_is_zero",
                  "declaring_scaleless_zero_to_mean_zero_UV_pole"),
        primitive("UVP_P12", "massless_offshell_bubble",
                  "nonexceptional_offshell_replay_agrees_with_auxiliary_mass_UV_residue_and_has_explicit_IR_status",
                  "spurious_IR_pole_classified_as_UV"),
        primitive("UVP_P13", "rank8_tensor_vacuum_integral",
                  "exact_105_pairing_metric_symmetrization_and_d_times_d_plus_2_times_d_plus_4_times_d_plus_6_denominator",
                  "declared_rank8_capability_without_direct_primitive_validation"),
    ]

    phi4 = "L=1/2*(dphi)^2-1/2*m2*phi^2-lambda*phi^4/4!, d=4-2epsilon"
    phi3 = "L=1/2*(dphi)^2-1/2*m2*phi^2-g*phi^3/3!, d=4-2epsilon"
    controls = [
        theory("UVP_C01", "real_phi4", "one_loop_two_point",
               "deltaZ_phi=0_and_delta_m2_pole=lambda*m2/2_in_units_1_over_16pi2epsilonbar",
               phi4),
        theory("UVP_C02", "real_phi4", "one_loop_four_point_all_channels",
               "crossing_symmetric_delta_lambda_pole=3*lambda^2/2_in_units_1_over_16pi2epsilonbar",
               phi4),
        theory("UVP_C03", "real_phi4", "one_loop_renormalized_two_and_four_point",
               "zero_residual_UV_pole_after_derived_counterterms",
               phi4),
        theory("UVP_C04", "real_phi3_superrenormalizable", "one_loop_one_point",
               "action_derived_sign_and_magnitude_g*m2/2_times_the_tadpole_pole_unit",
               phi3),
        theory("UVP_C05", "real_phi3_superrenormalizable", "one_loop_two_point_bubble",
               "local_mass_pole_and_zero_p_squared_wavefunction_pole",
               phi3),
        theory("UVP_C06", "real_phi3_superrenormalizable", "one_loop_triangle",
               "UV_finite_three_point_function",
               phi3),
        theory("UVP_C07", "scalar_QED_one_complex_charge_one_scalar", "background_photon_two_point",
               "independently_derive_b=1/3_and_background_transversality",
               "beta_e=b*e^3/(16pi^2); background_operator=-F^2/4"),
        theory("UVP_C08", "scalar_QED_one_complex_charge_one_scalar", "scalar_two_point_and_scalar_photon_vertex",
               "general_xi_Ward_identity_and_zero_renormalized_UV_residual",
               "same_MSbar_Rxi_action_for_both_amplitudes"),
        theory("UVP_C09", "pure_Yang_Mills", "background_gauge_two_point",
               "independently_derive_b=-11*C_A/3_with_vector_and_ghost_parts_separate",
               "beta_g=b*g^3/(16pi^2); background_operator=-F^2/4"),
        theory("UVP_C10", "pure_Yang_Mills", "quantum_vector_ghost_and_gauge_parameter_two_point_set",
               "general_xi_BRST_Slavnov_Taylor_relations_and_zero_renormalized_UV_residual",
               "single_background_Rxi_BRST_action"),
        theory("UVP_C11", "Abelian_Higgs", "broken_phase_two_and_one_point_set",
               "background_b=1/3_Goldstone_ghost_xi_mass_pairing_and_consistent_tadpole_VEV_poles",
               "one_complex_charge_one_scalar_FJ_like_explicit_tadpole_shift"),
        theory("UVP_C12", "SU2_adjoint_Higgs_to_U1", "partial_BFM_broken_sector_set",
               "independently_derive_parent_b=-7_and_pass_equivariant_vector_Goldstone_ghost_quartic_ghost_BRST_checks",
               "one_real_adjoint_scalar; beta_g=b*g^3/(16pi^2)"),
        theory("UVP_C13", "SU2_adjoint_Higgs_to_U1", "UV_IR_rearranged_broken_two_point_set",
               "auxiliary_mass_and_nonexceptional_offshell_implementations_agree",
               "same_partial_BFM_Rxi_action_and_MSbar_subtraction"),
    ]

    canonical = [
        model("UVP_M01", "parent_background_gauge_two_point",
              "derive_b10=-34/3_without_importing_the_earned_value_as_output"),
        model("UVP_M02", "four_parent_scalar_kinetic_two_point_functions",
              "derive_deltaZ_Phi_deltaZ_Sigma_deltaZ_phi_deltaZ_S_and_irrep_identity_structure"),
        model("UVP_M03", "parent_scalar_quadratic_poles",
              "derive_all_four_real_quadratic_directions"),
        model("UVP_M04", "parent_scalar_cubic_poles",
              "derive_two_real_plus_one_complex_equals_four_real_cubic_directions"),
        model("UVP_M05", "parent_scalar_quartic_poles",
              "derive_18_real_plus_four_complex_equals_26_real_quartic_directions"),
        model("UVP_M06", "radiative_operator_projection",
              "exact_or_certified_full_rank_34_real_projection_onto_29_families_with_zero_out_of_basis_residual"),
        model("UVP_M07", "Hermitian_and_PQ_consistency",
              "complex_counterterms_pair_with_their_conjugates_and_no_PQ_forbidden_operator_is_generated"),
        model("UVP_M08", "partial_BFM_quantum_vector_heavy_light_ghost_and_xi_poles",
              "derive_all_missing_field_and_delta_xi_residues_and_pass_BRST_background_Ward_identities"),
        model("UVP_M09", "FJ_like_one_point_and_VEV_system",
              "derive_three_delta_v_and_three_delta_t_residues_from_one_frozen_prescription"),
        model("UVP_M10", "all_33_Goldstone_mass_relations",
              "delta_xi_MV2_equals_MV2_delta_xi_plus_xi_delta_MV2_exact_or_certified_for_every_broken_direction"),
        model("UVP_M11", "selected_renormalized_scalar_gauge_and_ghost_control_amplitudes",
              "zero_residual_one_loop_UV_pole_after_derived_counterterms"),
        model("UVP_M12", "layer5_counterterm_contract_consumption",
              "all_18_missing_residue_groups_derived_and_all_21_slots_receive_complete_coefficients"),
        model("UVP_M13", "independent_canonical_replay",
              "independent_diagram_inventory_and_canonicalization_or_inventory_independent_functional_completeness_plus_different_UV_reduction_reproduces_every_promoted_residue"),
    ]

    payload = {
        "schema_version": 2,
        "outcome": "ONE_LOOP_UV_POLE_EVALUATOR_CONTRACT_PREREGISTERED",
        "authority": "TEST_SPECIFICATION_ONLY_NO_UV_POLE_RESULT",
        "revision": {
            "supersedes_schema_version": 1,
            "supersedes_contract_sha256": V1_CONTRACT_SHA256,
            "changes": [
                "add_explicit_UVP_P13_rank8_tensor_primitive",
                "require_independent_diagram_inventory_or_functional_completeness_replay",
                "split_fail_fast_gate_into_27_test_evaluator_and_12_test_canonical_counterterm_phases",
            ],
            "scientific_results_changed": False,
        },
        "immutable_inputs": HASHES,
        "scope": {
            "loop_order": 1,
            "output": "exact_1_over_epsilon_bar_local_residue_only",
            "amplitudes": [
                "scalar_1_point", "scalar_2_point_through_p2",
                "scalar_3_point_through_one_derivative_when_present",
                "scalar_4_point_local", "quantum_vector_2_point_through_p2",
                "heavy_and_light_ghost_2_point_through_p2",
                "BRST_required_3_point_controls",
            ],
            "maximum_required_tensor_rank_preregistered": 8,
            "finite_parts": "FORBIDDEN_UNLESS_REQUIRED_TO_DISAMBIGUATE_UV_IR_ONLY",
            "layer6_tensor_IBP": "FORBIDDEN",
        },
        "primary_algorithm_contract": {
            "method": "large_loop_momentum_or_auxiliary_mass_local_expansion",
            "local_Taylor_order": "superficial_degree_of_divergence_per_amplitude",
            "tensor_reduction": "d_dimensional_before_epsilon_expansion",
            "pole_normalization": "d=4-2epsilon_and_1_over_epsilon_bar",
            "mass_support": "arbitrary_symbolic_non_degenerate_masses_and_zero_mass_limits",
            "routing": "deterministic_plus_independent_shift_replay",
            "locality": "no_log_external_momentum_or_inverse_external_invariant_in_pole_output",
        },
        "UV_IR_separation_contract": {
            "primary": "auxiliary_mass_IR_rearrangement_with_all_induced_local_IR_counterterms",
            "independent": "nonexceptional_offshell_or_Feynman_parameter_Gamma_function_residue_replay",
            "scaleless_integrals": "must_store_UV_and_IR_labels_separately_not_accept_bare_zero",
            "auxiliary_mass": "must_cancel_from_promoted_physical_counterterms",
            "massless_limits": "must_be_taken_after_UV_classification",
            "Rstar_requirement": "required_whenever_IR_rearrangement_creates_spurious_subdivergences",
        },
        "primitive_tests": primitives,
        "minimum_control_theories": controls,
        "canonical_model_tests": canonical,
        "counts": {
            "primitive_tests": len(primitives),
            "control_theory_tests": len(controls),
            "canonical_model_tests": len(canonical),
            "total_required_tests": len(primitives) + len(controls) + len(canonical),
        },
        "independent_replay": {
            "required": True,
            "primary_method_may_not_be_imported": True,
            "primary_diagram_inventory_may_not_be_imported": True,
            "minimum": "all_primitive_poles_all_control_theory_promoted_residues_and_every_canonical_residue_group",
            "allowed_design_A": (
                "independent_half_edge_or_functional_derivative_generation_"
                "with_independent_canonicalization_field_assignment_statistics_"
                "signs_and_symmetry_factors_then_independent_UV_reduction"
            ),
            "allowed_design_B": (
                "background_field_effective_action_or_heat_kernel_derivation_"
                "whose_completeness_does_not_depend_on_the_primary_graph_list"
            ),
            "diagrammatic_replay_artifacts": [
                "independent_diagram_set_hash_per_external_process",
                "primary_minus_replay_and_replay_minus_primary_set_differences",
                "symmetry_factor_and_Grassmann_sign_residuals",
                "independent_UV_residue_table",
            ],
            "functional_replay_artifacts": [
                "operator_trace_or_functional_derivative_completeness_certificate",
                "mapping_to_every_required_local_operator",
                "independent_UV_residue_table",
                "comparison_to_primary_diagrammatic_residues",
            ],
            "external_process_coverage": (
                "all_control_and_canonical_scalar_1_2_3_4_point_quantum_"
                "vector_ghost_and_BRST_vertex_processes"
            ),
            "mere_reuse_of_expected_beta_coefficients": "NOT_AN_INDEPENDENT_REPLAY",
            "same_incomplete_graph_list_evaluated_twice": "NOT_AN_INDEPENDENT_REPLAY",
        },
        "fail_fast_partition": {
            "phase_5A_engine": {
                "tests": "UVP_P01_through_UVP_P13_plus_UVP_C01_through_UVP_C13_plus_UVP_M01",
                "count": 27,
                "pass_outcome": "ONE_LOOP_UV_POLE_EVALUATOR_PASS",
                "counterterm_compiler_after_pass": "REMAINS_BLOCKED",
            },
            "phase_5B_canonical_counterterms": {
                "tests": "UVP_M02_through_UVP_M13",
                "count": 12,
                "pass_outcome": "ONE_LOOP_COUNTERTERM_COMPILER_PASS",
                "layer6_after_pass": "AUTHORIZED_BY_SEPARATE_AUDIT_ONLY",
            },
        },
        "promotion_policy": {
            "uv_evaluator_pass": "all_primitive_and_control_theory_tests_pass_and_evaluator_independently_derives_b10",
            "counterterm_compiler_pass": "all_canonical_tests_pass_all_18_residue_groups_are_derived_all_21_slots_complete_and_selected_renormalized_amplitudes_have_zero_UV_pole",
            "fail": "complete_primary_and_independent_calculations_agree_on_a_wrong_residue_nonlocal_pole_BRST_violation_or_out_of_basis_divergence",
            "blocked": "any_required_integrand_vertex_UV_IR_subtraction_projection_or_independent_replay_layer_is_unimplemented_or_ambiguous",
            "layer6_authorized_only_after": "ONE_LOOP_COUNTERTERM_COMPILER_PASS",
        },
        "preserved_dispositions": {
            "compiler": "ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED",
            "layer4": "TWO_LOOP_DIAGRAM_GENERATOR_PASS",
            "gauge_matching": "DIRECT_GAUGE_MATCHING_UNRESOLVED",
            "bfb": "BFB_UNRESOLVED",
            "finite_C1_GS": None,
        },
    }
    payload["uv_pole_evaluator_contract_sha256"] = canonical_hash(payload)
    return payload


def main():
    payload = build()
    (HERE / "one_loop_uv_pole_evaluator_contract.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("PRIMITIVE_TESTS", payload["counts"]["primitive_tests"])
    print("CONTROL_THEORY_TESTS", payload["counts"]["control_theory_tests"])
    print("CANONICAL_MODEL_TESTS", payload["counts"]["canonical_model_tests"])
    print("TOTAL_REQUIRED_TESTS", payload["counts"]["total_required_tests"])
    print("UV_POLE_EVALUATOR_CONTRACT_SHA256", payload["uv_pole_evaluator_contract_sha256"])


if __name__ == "__main__":
    main()
