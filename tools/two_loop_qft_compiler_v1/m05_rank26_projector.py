"""Freeze an exact rank-26 projector for the canonical quartic invariant basis.

The first eleven witnesses are the non-Sigma subtheory projector.  Fifteen
additional deterministic Gaussian-integer Sigma-bearing states complete the
rank.  This is an M05 implementation artifact, not an M05 residue or pass.
"""

from hashlib import sha256
import json
from pathlib import Path
from random import Random
import sys

from sympy import I, Matrix, conjugate, simplify, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [
    str(HERE),
    str(ROOT / "calculations" / "canonical_so10_scalar_reconstruction"),
    str(ROOT / "calculations" / "canonical_so10_full_hessian"),
]

from certify_sigma_quartics import generated_form
from m05_parent_scalar_kernel import projector_backgrounds
from parent_bilinear_oracle import State, invariant_values


REAL_QUARTICS = (
    "lambdaPhi1", "lambdaPhi2", "lambdaPhiSigma1",
    "lambdaPhiSigma2", "lambdaPhiphi1", "lambdaPhiphi2",
    "lambdaPhiS", "lambdaSigma1", "lambdaSigma2", "lambdaSigma3",
    "lambdaSigma4", "lambdaSigmaphi1", "lambdaSigmaphi2",
    "lambdaPhiVector1", "lambdaPhiVector2", "lambdaSigmaS",
    "lambdaVectorS", "lambdaS",
)
COMPLEX_QUARTICS = ("z4", "zK", "zEta", "zD")
REAL_DIRECTION_NAMES = REAL_QUARTICS + tuple(
    component for name in COMPLEX_QUARTICS
    for component in (f"{name}_re", f"{name}_im")
)
SELECTED_SIGMA_SEEDS = tuple(range(1, 15)) + (18,)


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def physical_quartics(state):
    raw = invariant_values(state)
    values = [raw[name] for name in REAL_QUARTICS]
    for name in COMPLEX_QUARTICS:
        values.extend((
            simplify(raw[name] + conjugate(raw[name])),
            simplify(I * raw[name] + conjugate(I * raw[name])),
        ))
    return tuple(simplify(value) for value in values)


def sigma_backgrounds():
    """Replay the fixed-seed discovery stream exactly through seed 18."""
    rng = Random(2605)
    selected = []
    for seed in range(1, 19):
        form = generated_form(seed, 4 + seed % 7)
        p = zeros(10)
        diagonal = [rng.randint(-2, 2) for _ in range(9)]
        diagonal.append(-sum(diagonal))
        for i, value in enumerate(diagonal):
            p[i, i] = value
        for _ in range(rng.randint(0, 2)):
            i, j = sorted(rng.sample(range(10), 2))
            p[i, j] = p[j, i] = rng.choice((-2, -1, 1, 2))
        vector = [0] * 10
        for i in rng.sample(range(10), rng.randint(1, 3)):
            vector[i] = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        singlet = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        if seed in SELECTED_SIGMA_SEEDS:
            selected.append((seed, State(p, form, tuple(vector), singlet)))
    assert tuple(seed for seed, _ in selected) == SELECTED_SIGMA_SEEDS
    return selected


def compute_projector():
    active = list(projector_backgrounds())
    sigma = sigma_backgrounds()
    backgrounds = active + [state for _, state in sigma]
    assert len(backgrounds) == 26
    matrix = Matrix([[24 * value for value in physical_quartics(state)]
                     for state in backgrounds])
    assert matrix.rank() == 26
    determinant = simplify(matrix.det())
    assert determinant != 0
    rows = [[str(value) for value in row] for row in matrix.tolist()]
    inventory = {
        "real_quartic_directions": list(REAL_DIRECTION_NAMES),
        "active_witnesses": 11,
        "Sigma_bearing_witnesses": 15,
        "selected_Sigma_seeds": list(SELECTED_SIGMA_SEEDS),
        "fixed_rng_seed": 2605,
        "projector_rank": 26,
        "projector_determinant": str(determinant),
        "projector_matrix_sha256": digest(rows),
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_RANK26_QUARTIC_PROJECTOR_PASS",
        "authority": "IMPLEMENTATION_COMPONENT_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "projector_matrix": rows,
        "projection_rank": 26,
        "projection_residual": "NOT_APPLICABLE_UNTIL_FULL_POLE_EXISTS",
        "missing_for_M05": [
            "Sigma-containing V4V4 pole contractions",
            "partial-BFM gauge/Goldstone/ghost quartic completion",
            "complete inventory-independent residue replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_projector()
    (HERE / "uvp_m05_rank26_projector.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("MATRIX_SHA256", result["inventory"]["projector_matrix_sha256"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
