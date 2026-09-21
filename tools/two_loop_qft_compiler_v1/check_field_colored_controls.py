"""Field-colored two-loop controls using primary and independent engines."""

import json
from pathlib import Path

from enumerate_layer4_species_diagrams import assign
from independent_species_diagram_replay import canonical, enumerate_recursive


HERE = Path(__file__).resolve().parent


def row(vertex_id, external, fields):
    return {"vertex_id": vertex_id,
            "external_background_legs": external,
            "internal_fields": sorted(fields)}


def catalogs():
    return {
        "real_phi4": [
            row("phi4_0", 0, ("H", "H", "H", "H")),
            row("phi4_1", 1, ("H", "H", "H")),
            row("phi4_2", 2, ("H", "H")),
        ],
        "cubic_scalar": [
            row("phi3_0", 0, ("H", "H", "H")),
            row("phi3_1", 1, ("H", "H")),
            row("phi3_2", 2, ("H",)),
        ],
        "scalar_QED": [
            row("qHH", 0, ("q", "H", "H")),
            row("qqHH", 0, ("q", "q", "H", "H")),
            row("AHH", 1, ("H", "H")),
            row("AqHH", 1, ("q", "H", "H")),
            row("AAHH", 2, ("H", "H")),
        ],
        "Yang_Mills_ghost": [
            row("qqq", 0, ("q", "q", "q")),
            row("qqqq", 0, ("q", "q", "q", "q")),
            row("cbarcq", 0, ("cbar", "c", "q")),
            row("Aqq", 1, ("q", "q")),
            row("Aqqq", 1, ("q", "q", "q")),
            row("Acbarc", 1, ("cbar", "c")),
            row("Acbarcq", 1, ("cbar", "c", "q")),
            row("AAqq", 2, ("q", "q")),
            row("AAcbarc", 2, ("cbar", "c")),
        ],
        "Abelian_Higgs_Rxi": [
            row("qHH", 0, ("q", "H", "H")),
            row("qGG", 0, ("q", "G", "G")),
            row("qqHH", 0, ("q", "q", "H", "H")),
            row("qqGG", 0, ("q", "q", "G", "G")),
            row("HHH", 0, ("H", "H", "H")),
            row("HGG", 0, ("H", "G", "G")),
            row("HHHH", 0, ("H", "H", "H", "H")),
            row("HHGG", 0, ("H", "H", "G", "G")),
            row("GGGG", 0, ("G", "G", "G", "G")),
            row("cbarcH", 0, ("cbar", "c", "H")),
            row("AHH", 1, ("H", "H")),
            row("AGG", 1, ("G", "G")),
            row("AqHH", 1, ("q", "H", "H")),
            row("AqGG", 1, ("q", "G", "G")),
            row("Acbarc", 1, ("cbar", "c")),
            row("AAHH", 2, ("H", "H")),
            row("AAGG", 2, ("G", "G")),
            row("AAcbarc", 2, ("cbar", "c")),
        ],
    }


def main():
    topology_data = json.loads((HERE / "layer4_topologies.json").read_text())
    results = {}
    for name, rows in catalogs().items():
        lookup = {(r["external_background_legs"], tuple(r["internal_fields"])): r
                  for r in rows}
        primary_set, replay_set = set(), set()
        for topology in topology_data["two_loop_topologies"]:
            for diagram in assign(topology, lookup):
                lines = tuple(edge["line_assignment"]
                              for edge in diagram["ordered_field_assignments"])
                primary_set.add((topology["topology_id"], canonical(
                    topology, tuple(diagram["vertex_ids"]), lines)))
            replay_set.update((topology["topology_id"], key)
                              for key in enumerate_recursive(topology, lookup))
        assert primary_set == replay_set, name
        assert primary_set, name
        results[name] = {
            "field_colored_two_loop_diagrams": len(primary_set),
            "primary_minus_independent": 0,
            "independent_minus_primary": 0,
        }
    payload = {
        "outcome": "FIELD_COLORED_CONTROL_THEORIES_PASS",
        "controls": results,
        "engines": [
            "Cartesian_edge_coloring_plus_automorphism_quotient",
            "recursive_edge_assignment_plus_independent_canonicalization",
        ],
    }
    (HERE / "layer4_field_colored_controls.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    for name, result in results.items():
        print(name, result["field_colored_two_loop_diagrams"])


if __name__ == "__main__":
    main()

