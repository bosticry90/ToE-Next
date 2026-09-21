"""Independent bare-action expansion replay for the layer-5 contract.

This file intentionally does not import the primary counterterm compiler.
It reconstructs parent field multiplicities and slot dispatch rules from a
separate ledger, then compares them with the emitted artifact.
"""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


INDEPENDENT_COUNTS = {
    "mPhi2": {"Phi": 2}, "mSigma2": {"Sigma": 2},
    "mphi2": {"phi": 2}, "mS2": {"S": 2},
    "muPhi": {"Phi": 3}, "muPhiPhi": {"Phi": 1, "phi": 2},
    "z6": {"phi": 2, "S": 1},
    "lambdaPhi1": {"Phi": 4}, "lambdaPhi2": {"Phi": 4},
    "lambdaPhiSigma1": {"Phi": 2, "Sigma": 2},
    "lambdaPhiSigma2": {"Phi": 2, "Sigma": 2},
    "lambdaPhiphi1": {"Phi": 2, "phi": 2},
    "lambdaPhiphi2": {"Phi": 2, "phi": 2},
    "lambdaPhiS": {"Phi": 2, "S": 2},
    "lambdaSigma1": {"Sigma": 4}, "lambdaSigma2": {"Sigma": 4},
    "lambdaSigma3": {"Sigma": 4}, "lambdaSigma4": {"Sigma": 4},
    "lambdaSigmaphi1": {"Sigma": 2, "phi": 2},
    "lambdaSigmaphi2": {"Sigma": 2, "phi": 2},
    "lambdaPhiVector1": {"phi": 4},
    "lambdaPhiVector2": {"phi": 4},
    "lambdaSigmaS": {"Sigma": 2, "S": 2},
    "lambdaVectorS": {"phi": 2, "S": 2},
    "lambdaS": {"S": 4},
    "z4": {"Phi": 1, "Sigma": 2, "S": 1},
    "zK": {"Phi": 1, "phi": 2, "S": 1},
    "zEta": {"Sigma": 3, "phi": 1},
    "zD": {"Sigma": 2, "phi": 2},
}


def factor(counts):
    terms = []
    for field in ("Phi", "Sigma", "phi", "S"):
        if counts.get(field):
            terms.append(f"{counts[field]}/2*deltaZ_{field}")
    return " + ".join(terms) if terms else "0"


def main():
    primary = json.loads((HERE / "layer5_counterterm_contract.json").read_text(
        encoding="utf-8"))
    rows = {row["coefficient"]: row
            for row in primary["parent_operator_basis"]["rows"]}
    assert set(rows) == set(INDEPENDENT_COUNTS)
    for name, counts in INDEPENDENT_COUNTS.items():
        assert rows[name]["field_multiplicities"] == counts
        assert rows[name]["expanded_operator_coefficient"] == (
            f"delta_{name} + {name}*({factor(counts)})")

    allowed = {
        "field": "CT_FIELD(", "mass": "CT_MASS(",
        "gauge_parameter": "CT_GAUGE_PARAMETER(",
        "gauge_coupling": "CT_G_VERTEX=", "VEV": "CT_VEV=",
        "tadpole": "CT_TADPOLE=", "vertex": "CT_VERTEX=",
    }
    slots = primary["counterterm_slots"]
    assert len(slots) == 21
    assert len({row["slot_id"] for row in slots}) == 21
    for row in slots:
        assert allowed[row["counterterm_kind"]] in row["coefficient"]
        assert row["coefficient_status"] == (
            "STRUCTURAL_EXPRESSION_POPULATED_RESIDUE_PENDING")

    gauge = primary["known_gauge_counterterm"]
    assert gauge["b10"] == "-34/3"
    assert gauge["deltaZ_g10"] == "(-17/3)*P10"
    assert gauge["deltaZ_background_Spin10"] == "(34/3)*P10"
    assert gauge["ward_identity_residual"] == "0"

    payload = {
        "outcome": "LAYER5_BARE_ACTION_ROUNDTRIP_PASS",
        "imports_primary_compiler": False,
        "parent_monomial_families_replayed": 29,
        "counterterm_slots_replayed": 21,
        "background_Ward_identity_residual": "0",
        "qualification": (
            "structural bare-action expansion only; one-loop pole residues "
            "remain uncalculated"
        ),
    }
    (HERE / "layer5_counterterm_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("PARENT_MONOMIAL_FAMILIES_REPLAYED", 29)
    print("COUNTERTERM_SLOTS_REPLAYED", 21)
    print("BACKGROUND_WARD_IDENTITY_RESIDUAL", 0)


if __name__ == "__main__":
    main()
