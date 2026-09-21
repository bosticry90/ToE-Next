"""Runtime reconstruction of the frozen factorized 328-physical basis."""

from ast import literal_eval
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
from sympy import N, sympify


HERE = Path(__file__).resolve().parent
PHYSICAL_BASIS_HASH = (
    "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e"
)


def conjugate_label(label):
    p, q, n, y6 = label
    return (q, p, n, -y6)


def sparse_vector(entries):
    out = np.zeros(328)
    for i, z in entries:
        out[i] = float(z)
    return out


def load_weight_map():
    data = json.loads((HERE / "sm_weight_basis.json").read_text(encoding="utf-8"))
    W = np.zeros((328, 328))
    metadata = []
    for j, entry in enumerate(data["columns"]):
        metadata.append(entry["metadata"])
        for i, z in entry["sparse_parent_coordinates"]:
            W[i, j] = float(N(sympify(z), 30))
    return data, W, metadata


def load_physical_map():
    physical = json.loads((HERE / "physical_basis.json").read_text(encoding="utf-8"))
    assert physical["factorized_physical_basis_sha256"] == PHYSICAL_BASIS_HASH
    weights, W, metadata = load_weight_map()
    by_label = defaultdict(list)
    for j, meta in enumerate(metadata):
        by_label[tuple(meta["label"])].append(j)
    rotations = {literal_eval(key): value
                 for key, value in physical["multiplicity_rotations"].items()}
    columns, masses = [], []
    for label in sorted(rotations):
        rotation = rotations[label]
        values = np.asarray(rotation["eigenvalues"], dtype=float)
        indices = by_label[label]
        if conjugate_label(label) != label:
            V = np.asarray([[complex(re, im) for re, im in column]
                            for column in rotation["eigenvectors_columns"]],
                           dtype=complex).T
            multiplicity = V.shape[0]
            dimension = len(indices) // (2 * multiplicity)
            lookup = {(metadata[j]["copy"], metadata[j]["state"],
                       metadata[j]["realification"]): W[:, j] for j in indices}
            for mode in range(multiplicity):
                for state in range(dimension):
                    real, imag = np.zeros(328), np.zeros(328)
                    for copy in range(multiplicity):
                        z = V[copy, mode]
                        x = lookup[(copy, state, "re")]
                        y = lookup[(copy, state, "im")]
                        real += z.real * x - z.imag * y
                        imag += z.imag * x + z.real * y
                    columns.extend((real, imag))
                    masses.extend((values[mode], values[mode]))
        elif "real_eigenvectors_columns" in rotation:
            V = np.asarray(rotation["real_eigenvectors_columns"], dtype=float)
            Uself = W[:, indices]
            for mode in range(V.shape[1]):
                columns.append(Uself @ V[:, mode])
                masses.append(values[mode])
        else:
            for j in indices:
                columns.append(W[:, j])
                masses.append(values[0])
    Upre = np.column_stack(columns)
    masses = np.asarray(masses)
    heavy = np.where(masses > 2e-9)[0]
    special = physical["special_zero_columns"]
    Z = np.column_stack(
        [sparse_vector(x) for x in special["gauge_33"]]
        + [sparse_vector(special["pq_1"])]
        + [sparse_vector(x) for x in special["higgs_4"]])
    U = np.column_stack((Upre[:, heavy], Z))
    physical_masses = np.r_[masses[heavy], np.zeros(38)]
    assert U.shape == (328, 328)
    assert np.max(abs(U.T @ U - np.eye(328))) < 4e-9
    return physical, U, physical_masses


def scalar_field_id(index):
    assert 0 <= index < 328
    if index < 290:
        return f"H{index:03d}"
    if index < 323:
        return f"G{index-290:03d}"
    if index == 323:
        return "PQ000"
    return f"h{index-324:03d}"


def scalar_field_index(field_id):
    if field_id.startswith("H"):
        index = int(field_id[1:])
    elif field_id.startswith("G"):
        index = 290 + int(field_id[1:])
    elif field_id == "PQ000":
        index = 323
    elif field_id.startswith("h"):
        index = 324 + int(field_id[1:])
    else:
        raise KeyError(field_id)
    assert scalar_field_id(index) == field_id
    return index
