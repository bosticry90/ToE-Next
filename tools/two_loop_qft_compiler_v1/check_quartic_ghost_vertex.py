"""Regress the ordered quartic-ghost derivative and flow channels."""

import json
from pathlib import Path

from quartic_ghost_vertex import differentiated_terms, vertex_channels


HERE = Path(__file__).resolve().parent


def main():
    terms = differentiated_terms()
    channels = vertex_channels()
    assert [row["grassmann_permutation_sign"] for row in terms] == [1, -1, -1, 1]
    assert [row["channel"] for row in channels] == ["direct", "exchange"]
    assert [row["coefficient_sign"] for row in channels] == [1, -1]
    inventory = json.loads((HERE / "layer4_species_diagrams.json").read_text())
    records = [row for row in inventory["diagrams"]
               if "quartic_ghost_vertex_term" in row]
    assert len(records) == 8
    assert {row["quartic_ghost_vertex_term"]["channel"]
            for row in records} == {"direct", "exchange"}
    assert all(row["statistics_sign"] in ("-1", "1") for row in records)
    payload = {
        "outcome": "ORDERED_QUARTIC_GHOST_VERTEX_PASS",
        "raw_grassmann_derivative_signs": [1, -1, -1, 1],
        "antisymmetrized_vertex": (
            "xi*(f[a,b,A]*f[c,d,A]-f[c,b,A]*f[a,d,A])"
        ),
        "flow_channels": [row["channel"] for row in channels],
        "base_graphs": 4,
        "ordered_channel_records": len(records),
        "all_statistics_signs_resolved": True,
    }
    (HERE / "quartic_ghost_vertex_regression.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("ORDERED_CHANNEL_RECORDS", len(records))


if __name__ == "__main__":
    main()

