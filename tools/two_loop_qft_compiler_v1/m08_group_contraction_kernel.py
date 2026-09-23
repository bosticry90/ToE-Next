"""Group-contraction preflight for canonical partial-BFM M08."""

from hashlib import sha256
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from partial_bfm_action import PartialBFMAction


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def rational(value, tolerance=1e-8):
    candidate = Fraction(float(value)).limit_denominator(120)
    if abs(float(candidate) - float(value)) > tolerance:
        raise ValueError(f"non-rational contraction value {value}")
    return str(candidate)


def serialized_matrix(matrix):
    # The deterministic physical vector basis contains algebraic rotations, so
    # individual off-diagonal entries need not be rational even though the
    # invariant spectra are.  The hash freezes their certified numerical form.
    return [[format(float(value), ".15g") for value in row]
            for row in matrix]


def spectrum(matrix, tolerance=1e-8):
    values = np.linalg.eigvalsh((matrix + matrix.T) / 2)
    groups = []
    for value in values:
        if not groups or abs(value - groups[-1][0]) > tolerance:
            groups.append([float(value), 1])
        else:
            groups[-1][1] += 1
    return [{"eigenvalue": rational(value), "multiplicity": count}
            for value, count in groups]


def main():
    action = PartialBFMAction()
    all_ids = [action.invariant.vector_id(index) for index in range(45)]
    all_indices = list(range(45))
    light = [action.invariant.vector_index(value)
             for value in action.light_vector_ids]
    heavy = [action.invariant.vector_index(value)
             for value in action.heavy_vector_ids]
    structure = np.asarray([[[action.structure(a, b, c) for c in all_ids]
                             for b in all_ids] for a in all_ids])
    contractions = {}
    matrices = {}
    for name, external, left, right in (
        ("full_adjoint", all_indices, all_indices, all_indices),
        ("heavy_heavy_heavy", heavy, heavy, heavy),
        ("heavy_heavy_light", heavy, heavy, light),
        ("light_light_light", light, light, light),
        ("light_heavy_heavy", light, heavy, heavy),
    ):
        block = structure[np.ix_(external, left, right)]
        matrix = np.einsum("abc,dbc->ad", block, block)
        matrices[name] = matrix
        serial = serialized_matrix(matrix)
        contractions[name] = {
            "shape": list(matrix.shape),
            "spectrum": spectrum(matrix),
            "maximum_off_diagonal": format(float(np.max(abs(
                matrix - np.diag(np.diag(matrix))))), ".12g"),
            "diagonal": [format(float(value), ".12g")
                         for value in np.diag(matrix)],
            "matrix_sha256": digest(serial),
            "matrix": serial,
        }
    # For a heavy external generator, the full adjoint contraction contains
    # both ordered mixed pairs (heavy, light) and (light, heavy).
    heavy_completeness = matrices["heavy_heavy_heavy"] + 2 * matrices[
        "heavy_heavy_light"] - 8 * np.eye(len(heavy))
    light_completeness = matrices["light_light_light"] + matrices[
        "light_heavy_heavy"] - 8 * np.eye(len(light))
    heavy_mass = np.diag(action.invariant.vector_masses[12:45])
    heavy_mass_commutators = {
        name: float(np.max(abs(heavy_mass @ matrices[name]
                                - matrices[name] @ heavy_mass)))
        for name in ("heavy_heavy_heavy", "heavy_heavy_light")
    }
    payload = {
        "schema_version": 1,
        "outcome": "M08_GROUP_CONTRACTION_PREFLIGHT_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "partial_BFM_action_sha256": action.manifest()[
            "partial_bfm_action_sha256"
        ],
        "contractions": contractions,
        "completeness": {
            "heavy_HHH_plus_2HHL_equals_8_identity_maximum_residual":
                format(float(np.max(abs(heavy_completeness))), ".12g"),
            "light_LLL_plus_LHH_equals_8_identity_maximum_residual":
                format(float(np.max(abs(light_completeness))), ".12g"),
            "heavy_mass_commutator_maximum_residuals": {
                name: format(value, ".12g")
                for name, value in heavy_mass_commutators.items()
            },
        },
        "full_Spin10_C_A_expected_only_as_post_derivation_regression": "8",
        "heavy_light_distinction_resolved": True,
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_group_contraction_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    for name, entry in contractions.items():
        print(name, entry["spectrum"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
