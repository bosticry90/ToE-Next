"""Compare primary and independently generated M08 three-point inventories."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def primary_key(row):
    return (row["topology"], tuple(sorted(row["vertex_ids"])),
            row["quartic_ghost_channel"],
            row["UV_disposition"].startswith("POWER_COUNTED"))


def replay_key(row):
    return (row["topology"], tuple(sorted(row["vertex_ids"])),
            row["quartic_ghost_channel"], row["power_counted_zero"])


def expanded_difference(left, right):
    difference = left - right
    return [repr(key) for key, count in sorted(difference.items())
            for _ in range(count)]


def main():
    primary = json.loads((HERE /
        "uvp_m08_brst_three_point_primary_inventory.json").read_text())
    replay = json.loads((HERE /
        "uvp_m08_brst_inventory_independent_replay.json").read_text())
    comparisons = {}
    for process in primary["records"]:
        pset = Counter(primary_key(row) for row in primary["records"][process])
        rset = Counter(replay_key(row) for row in replay["records"][process])
        p_minus_r = expanded_difference(pset, rset)
        r_minus_p = expanded_difference(rset, pset)
        assert not p_minus_r and not r_minus_p
        comparisons[process] = {
            "primary_records": sum(pset.values()),
            "replay_records": sum(rset.values()),
            "primary_minus_replay": p_minus_r,
            "replay_minus_primary": r_minus_p,
            "semantic_multiset_sha256": digest(sorted(
                (repr(key), count) for key, count in pset.items())),
        }
    payload = {
        "schema_version": 1,
        "outcome": "M08_BRST_PRIMARY_REPLAY_INVENTORY_AGREEMENT",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "primary_inventory_sha256": primary["inventory_sha256"],
        "replay_inventory_sha256": replay["inventory_sha256"],
        "comparison_basis": (
            "topology_vertex_multiset_quartic_channel_UV_disposition"
        ),
        "comparisons": comparisons,
        "maximum_set_difference": 0,
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_inventory_comparison.json").write_text(
        json.dumps(payload, indent=2) + "\n")
    print(payload["outcome"])
    print("MAXIMUM_SET_DIFFERENCE 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
