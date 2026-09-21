"""Audit promotion layer 4 and its independent enumerations."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ACTION_HASH = "2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491"


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main():
    compiler = load("compiler_status.json")
    topologies = load("layer4_topologies.json")
    replay = load("layer4_topology_independent_replay.json")
    controls = load("layer4_topology_controls.json")
    catalog = load("layer4_vertex_catalog.json")
    species = load("layer4_species_diagrams.json")
    species_replay = load("layer4_species_independent_replay.json")
    ghost = load("quartic_ghost_vertex_regression.json")
    field_controls = load("layer4_field_colored_controls.json")
    one_loop = load("layer4_one_loop_regression.json")

    assert compiler.get("layer3_outcome_preserved", compiler["outcome"]) == (
        "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS")
    assert compiler["complete_partial_bfm_action"]["sha256"] == ACTION_HASH
    assert topologies["outcome"] == "MODEL_INDEPENDENT_TWO_POINT_TOPOLOGY_ENGINE_PASS"
    assert topologies["counts"]["one_loop_1PI_topologies"] == 2
    assert topologies["counts"]["two_loop_1PI_topologies"] == 9
    assert all(len(row["momentum_routing"]["chord_edge_ordinals"])
               == row["loop_order"]
               for row in (topologies["one_loop_topologies"]
                           + topologies["two_loop_topologies"]))
    assert replay["outcome"] == "INDEPENDENT_TOPOLOGY_REPLAY_PASS"
    assert replay["one_loop_topologies"] == 2
    assert replay["two_loop_topologies"] == 9
    assert controls["outcome"] == "SMALL_THEORY_TOPOLOGY_CONTROLS_PASS"
    assert catalog["outcome"] == "LAYER4_INDEX_SUMMED_VERTEX_CATALOG_PASS"
    assert catalog["immutable_partial_bfm_action_sha256"] == ACTION_HASH
    assert species["immutable_partial_bfm_action_sha256"] == ACTION_HASH
    assert species["diagram_count"] == 1900
    assert species["quartic_ghost_base_graphs"] == 4
    assert species["quartic_ghost_ordered_channel_records"] == 8
    assert species["unresolved_quartic_ghost_statistics_diagrams"] == 0
    assert species["all_statistics_signs_resolved"] is True
    assert species["all_symbolic_numerator_denominator_skeletons_present"] is True
    assert species["outcome"] == "CANONICAL_SPECIES_DIAGRAM_ASSIGNMENT_PASS"
    assert species_replay["outcome"] == (
        "INDEPENDENT_CANONICAL_SPECIES_ENUMERATION_PASS")
    assert species_replay["final_records"] == 1900
    assert species_replay["maximum_symmetry_denominator_residual"] == 0
    assert species_replay["statistics_sign_mismatches"] == 0
    assert ghost["outcome"] == "ORDERED_QUARTIC_GHOST_VERTEX_PASS"
    assert ghost["ordered_channel_records"] == 8
    assert field_controls["outcome"] == "FIELD_COLORED_CONTROL_THEORIES_PASS"
    assert one_loop["outcome"] == (
        "LAYER3_ONE_LOOP_DIAGRAM_INVENTORY_REGRESSION_PASS")
    assert one_loop["required_heavy_vector_goldstone_ghost_diagrams"] == 6

    compiler.update({
        "outcome": "TWO_LOOP_DIAGRAM_GENERATOR_PASS",
        "layer3_outcome_preserved": (
            "BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS"),
        "layer4_topology_engine": "PASS_2_ONE_LOOP_9_TWO_LOOP_1PI",
        "layer4_topology_inventory_sha256": topologies[
            "topology_inventory_sha256"],
        "layer4_independent_topology_replay": replay["outcome"],
        "layer4_small_theory_controls": controls["outcome"],
        "layer4_field_colored_controls": field_controls["outcome"],
        "layer4_vertex_catalog": "PASS_168_INDEX_SUMMED_SIGNATURES",
        "layer4_vertex_catalog_sha256": catalog["vertex_catalog_sha256"],
        "layer4_species_assignment": species["outcome"],
        "layer4_species_diagram_count": species["diagram_count"],
        "layer4_species_inventory_sha256": species[
            "species_inventory_sha256"],
        "layer4_quartic_ghost_base_graphs": 4,
        "layer4_quartic_ghost_ordered_channel_records": 8,
        "layer4_unresolved_quartic_ghost_diagrams": 0,
        "layer4_ordered_quartic_ghost_vertex": ghost["outcome"],
        "layer4_one_loop_inventory_regression": one_loop["outcome"],
        "layer4_blocker": None,
        "layer4_independent_complete_field_assignment_replay": species_replay[
            "outcome"],
        "layer5_counterterm_derivation_authorized": True,
        "next_gate": "ONE_LOOP_COUNTERTERM_COMPILER_LAYER_5",
    })
    (HERE / "compiler_status.json").write_text(
        json.dumps(compiler, indent=2) + "\n", encoding="utf-8")
    print(compiler["outcome"])
    print("TOPOLOGY_ENGINE PASS")
    print("SPECIES_DIAGRAMS", species["diagram_count"])
    print("ORDERED_QUARTIC_GHOST_CHANNEL_RECORDS", 8)
    print("LAYER5_COUNTERTERMS AUTHORIZED=true")


if __name__ == "__main__":
    main()
