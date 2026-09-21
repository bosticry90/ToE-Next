"""Use the generic layer-4 engine to recover the layer-3 heavy inventory."""

import json
from pathlib import Path

from enumerate_layer4_species_diagrams import assign
from layer4_vertex_catalog import manifest as catalog_manifest


HERE = Path(__file__).resolve().parent


def line_bases(diagram):
    return sorted(row["line_assignment"][0]
                  for row in diagram["ordered_field_assignments"])


def main():
    topologies = json.loads((HERE / "layer4_topologies.json").read_text())
    catalog = catalog_manifest()
    lookup = {
        (row["external_background_legs"], tuple(row["internal_fields"])): row
        for row in catalog["vertex_signatures"]
    }
    diagrams = []
    for topology in topologies["one_loop_topologies"]:
        diagrams.extend(assign(topology, lookup))

    expected = {
        (("BFM_A_V_V", "BFM_A_V_V"), ("V", "V")),
        (("BFM4_A_A_V_V",), ("V",)),
        (("BFM_A_G_G", "BFM_A_G_G"), ("G", "G")),
        (("BFM4_A_A_G_G",), ("G",)),
        (("BFM_A_ubar_u", "BFM_A_ubar_u"), ("U", "U")),
        (("BFM4_A_A_ubar_u",), ("U",)),
    }
    observed = set()
    for diagram in diagrams:
        vertices = tuple(sorted(diagram["vertex_ids"]))
        lines = tuple(line_bases(diagram))
        candidate = (vertices, lines)
        if candidate in expected:
            observed.add(candidate)
    assert observed == expected, (expected - observed, observed - expected)
    payload = {
        "outcome": "LAYER3_ONE_LOOP_DIAGRAM_INVENTORY_REGRESSION_PASS",
        "generic_one_loop_species_diagrams": len(diagrams),
        "required_heavy_vector_goldstone_ghost_diagrams": 6,
        "required_inventory": [
            {"vertex_ids": list(vertices), "line_bases": list(lines)}
            for vertices, lines in sorted(expected)
        ],
        "qualification": (
            "inventory_only; layer-3 determinant arithmetic remains the "
            "authority for the evaluated coefficient"
        ),
    }
    (HERE / "layer4_one_loop_regression.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("REQUIRED_HEAVY_DIAGRAMS", 6)


if __name__ == "__main__":
    main()

