"""Small-theory topology and automorphism controls for layer 4."""

from fractions import Fraction
import json
from pathlib import Path

from diagram_topology import enumerate_two_point_topologies


HERE = Path(__file__).resolve().parent


def pick(rows, valences, external, edges):
    for row in rows:
        if (row["vertex_valences"] == valences
                and row["external_vertices_labelled"] == external
                and row["internal_edges"] == edges):
            return row
    raise AssertionError((valences, external, edges))


def main():
    one = enumerate_two_point_topologies(1)
    two = enumerate_two_point_topologies(2)
    assert len(one) == 2
    assert len(two) == 9

    # Manually known scalar controls with Feynman-rule vertex factorials
    # already absorbed: phi^4 tadpole 1/2, sunset 1/6, double-scoop 1/4.
    tadpole = pick(one, [4], [0, 0], [[0, 0]])
    sunset = pick(two, [4, 4], [0, 1],
                  [[0, 1], [0, 1], [0, 1]])
    double_scoop = pick(two, [4, 4], [0, 0],
                        [[0, 1], [0, 1], [1, 1]])
    assert Fraction(tadpole["uncolored_symmetry_factor"]) == Fraction(1, 2)
    assert Fraction(sunset["uncolored_symmetry_factor"]) == Fraction(1, 6)
    assert Fraction(double_scoop["uncolored_symmetry_factor"]) == Fraction(1, 4)

    phi3 = [row for row in two if row["vertex_valences"] == [3, 3, 3, 3]]
    mixed = [row for row in two if row["vertex_valences"] == [3, 3, 4]]
    assert len(phi3) == 2
    assert len(mixed) == 5

    payload = {
        "outcome": "SMALL_THEORY_TOPOLOGY_CONTROLS_PASS",
        "controls": {
            "real_phi4_one_loop_tadpole": "1/2",
            "real_phi4_two_loop_sunset": "1/6",
            "real_phi4_two_loop_double_scoop": "1/4",
            "cubic_scalar_two_loop_topology_count": 2,
            "mixed_cubic_quartic_two_loop_topology_count": 5,
            "scalar_QED_supported_valence_classes": [[3, 3, 3, 3], [3, 3, 4], [4, 4]],
            "Yang_Mills_ghost_supported_valence_classes": [[3, 3, 3, 3], [3, 3, 4], [4, 4]],
            "Abelian_Higgs_Rxi_supported_valence_classes": [[3, 3, 3, 3], [3, 3, 4], [4, 4]],
        },
        "qualification": (
            "scalar_QED_Yang_Mills_ghost_and_Abelian_Higgs_field-colored "
            "inventories remain part of the physical-assignment subgate"
        ),
    }
    (HERE / "layer4_topology_controls.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])


if __name__ == "__main__":
    main()

