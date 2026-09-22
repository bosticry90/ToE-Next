"""Execute the inventory-independent UVP_M04 attempt-2 replay."""

from hashlib import sha256
import json
from pathlib import Path

from independent_m04_functional_replay import compute_replay
from m03_parent_scalar_kernel import digest


HERE = Path(__file__).resolve().parent
CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def load(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == sha256(json.dumps(
        work, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return payload


def main():
    attempt1 = load("uvp_m04_blocked_evidence.json")
    predecessor = load("uvp_m03_evidence_attempt2.json")
    replay = compute_replay()
    payload = {
        "schema_version": 1,
        "test_id": "UVP_M04",
        "attempt": 2,
        "contract_sha256": CONTRACT,
        "execution_plan_sha256": PLAN,
        "attempt1_blocked_evidence_sha256": attempt1["artifact_sha256"],
        "predecessor_M03_evidence_sha256": predecessor["artifact_sha256"],
        "method": "independent_parent_functional_eight_and_sixteen_corner_replay",
        "normalization": "coefficients multiply 1/(16*pi^2*epsilon_bar)",
        **replay,
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "regulator": "independent_local_functional_UV_projection",
            "locality": "LOCAL_CUBIC_POLYNOMIAL",
        },
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m04_independent_replay_attempt2.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M04_INDEPENDENT_REPLAY_ATTEMPT2_COMPLETE")
    print("INVENTORY_SHA256", payload["inventory_sha256"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])
    for name, value in payload["cubic_residues"].items():
        print(name, "=", value)


if __name__ == "__main__":
    main()
