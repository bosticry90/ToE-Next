"""Independent bounded audit of the non-Sigma M05 implementation surface.

This does not adjudicate UVP_M05.  It independently rebuilds the quartic
projector through the canonical invariant oracle and checks an analytic
pure-singlet contraction.  The complete replay remains part of the missing
full 26-direction implementation.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys

from sympy import I, Matrix, conjugate, simplify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [
    str(HERE),
    str(ROOT / "calculations" / "canonical_so10_full_hessian"),
]

from m05_parent_scalar_kernel import ACTIVE_QUARTICS, projector_backgrounds
from parent_bilinear_oracle import invariant_values


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def physical_quartics(state):
    raw = invariant_values(state)
    values = []
    for name in ACTIVE_QUARTICS:
        if name == "zK_re":
            value = raw["zK"] + conjugate(raw["zK"])
        elif name == "zK_im":
            value = I * raw["zK"] + conjugate(I * raw["zK"])
        else:
            value = raw[name]
        values.append(simplify(value))
    return values


def main():
    artifact = json.loads((HERE / "uvp_m05_active_scalar_subspace.json").read_text(
        encoding="utf-8"
    ))
    work = dict(artifact)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work)

    # This route calls the complete parent invariant oracle and does not read
    # the primary sparse-polynomial monomial lists.
    replay = Matrix([[24 * value for value in physical_quartics(q)]
                     for q in projector_backgrounds()])
    primary = Matrix([[simplify(value) for value in row]
                      for row in artifact["projector_matrix"]])
    assert replay == primary
    assert replay.rank() == 11

    # Independent O(N) radial controls.  Phi uses p2=sum q_A^2, whereas
    # complex phi and S use u=(1/2)sum q_A^2. Direct differentiation gives
    # 4(N+8), (N+8), and (N+8), respectively, in this pole convention.
    names = list(ACTIVE_QUARTICS)
    radial_controls = {
        "lambdaPhi1": ("lambdaPhi1", 4 * (54 + 8)),
        "lambdaPhiVector1": ("lambdaPhiVector1", 20 + 8),
        "lambdaS": ("lambdaS", 2 + 8),
    }
    for output, (coupling, expected) in radial_controls.items():
        index = names.index(coupling)
        table = Matrix([[simplify(value) for value in row]
                        for row in artifact["coefficient_tables"][output]])
        assert table[index, index] == expected

    audit = {
        "outcome": "M05_ACTIVE_SCALAR_SUBSPACE_AUDIT_PASS",
        "authority": "IMPLEMENTATION_CHECKPOINT_ONLY_NOT_UVP_M05_PASS",
        "primary_artifact_sha256": embedded,
        "independent_projector_method": "full_parent_invariant_oracle",
        "projector_rank": replay.rank(),
        "projector_residual": "0",
        "independent_ON_radial_controls": {
            "lambdaPhi1_squared": "248",
            "lambdaPhiVector1_squared": "28",
            "lambdaS_squared": "10",
        },
        "ON_radial_control_residual": "0",
        "full_M05_still_missing": [
            "Sigma-containing scalar contractions",
            "rank-26 projector",
            "partial-BFM gauge completion",
            "inventory-independent complete replay",
        ],
    }
    audit["artifact_sha256"] = digest(audit)
    (HERE / "uvp_m05_active_scalar_subspace_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )
    print(audit["outcome"])
    print("ARTIFACT_SHA256", audit["artifact_sha256"])


if __name__ == "__main__":
    main()
