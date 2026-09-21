"""Independent replay of the serialized factorized 328-physical basis.

This script does not import the physical-basis materializer.  It reconstructs
the complete transformation from the saved exact all-weight map, small block
rotations and explicit special-zero columns, then rechecks its hash and core
linear-algebra certificates.
"""

from ast import literal_eval
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from sympy import N, sympify


HERE = Path(__file__).resolve().parent
ZERO_TOL = 2e-9


def label_bar(label):
    p, q, n, y6 = label
    return (q, p, n, -y6)


def load_weight_map():
    data = json.loads((HERE / "sm_weight_basis.json").read_text(encoding="utf-8"))
    U = np.zeros((328, 328))
    metadata = []
    for j, entry in enumerate(data["columns"]):
        metadata.append(entry["metadata"])
        for i, z in entry["sparse_parent_coordinates"]:
            U[i, j] = float(N(sympify(z), 30))
    return data, U, metadata


def vector(entries):
    out = np.zeros(328)
    for i, z in entries:
        out[i] = float(z)
    return out


def stable_hash(U):
    serial = [[format(float(z), ".17g") for z in U[:, j]] for j in range(328)]
    return sha256(json.dumps(serial, separators=(",", ":")).encode()).hexdigest()


def main():
    physical = json.loads((HERE / "physical_basis.json").read_text(encoding="utf-8"))
    weights, W, metadata = load_weight_map()
    assert physical["sm_weight_map_sha256"] == weights["real_weight_map_sha256"]
    by_label = defaultdict(list)
    for j, meta in enumerate(metadata):
        by_label[tuple(meta["label"])].append(j)

    columns, masses = [], []
    rotations = {literal_eval(key): value
                 for key, value in physical["multiplicity_rotations"].items()}
    for label in sorted(rotations):
        rotation = rotations[label]
        values = np.asarray(rotation["eigenvalues"], dtype=float)
        indices = by_label[label]
        if label_bar(label) != label:
            complex_columns = rotation["eigenvectors_columns"]
            V = np.asarray([[complex(re, im) for re, im in column]
                            for column in complex_columns], dtype=complex).T
            multiplicity = V.shape[0]
            dimension = len(indices)//(2*multiplicity)
            lookup = {(metadata[j]["copy"], metadata[j]["state"],
                       metadata[j]["realification"]): W[:, j] for j in indices}
            for mode in range(multiplicity):
                for state in range(dimension):
                    re_col, im_col = np.zeros(328), np.zeros(328)
                    for copy in range(multiplicity):
                        z = V[copy, mode]
                        x = lookup[(copy, state, "re")]
                        y = lookup[(copy, state, "im")]
                        re_col += z.real*x-z.imag*y
                        im_col += z.imag*x+z.real*y
                    columns.extend((re_col, im_col))
                    masses.extend((values[mode], values[mode]))
        elif "real_eigenvectors_columns" in rotation:
            V = np.asarray(rotation["real_eigenvectors_columns"], dtype=float)
            Uself = W[:, indices]
            for mode in range(V.shape[1]):
                columns.append(Uself@V[:, mode])
                masses.append(values[mode])
        else:
            assert len(values) == 1
            for j in indices:
                columns.append(W[:, j])
                masses.append(values[0])

    Upre = np.column_stack(columns)
    masses = np.asarray(masses)
    assert Upre.shape == (328, 328)
    heavy = np.where(masses > ZERO_TOL)[0]
    zero = np.where(abs(masses) < ZERO_TOL)[0]
    assert (len(heavy), len(zero)) == (290, 38)
    special = physical["special_zero_columns"]
    Z = np.column_stack(
        [vector(x) for x in special["gauge_33"]]
        + [vector(special["pq_1"])]
        + [vector(x) for x in special["higgs_4"]])
    U = np.column_stack((Upre[:, heavy], Z))
    identity_residual = float(np.max(abs(U.T@U-np.eye(328))))
    zero_subspace_residual = float(np.max(abs(Z-Upre[:, zero]@(Upre[:, zero].T@Z))))
    assert identity_residual < 4e-9
    assert zero_subspace_residual < 4e-9
    assert np.linalg.matrix_rank(U, 1e-9) == 328
    rebuilt_hash = stable_hash(U)
    factorized = {
        "sm_weight_map_sha256": physical["sm_weight_map_sha256"],
        "multiplicity_rotations": physical["multiplicity_rotations"],
        "special_zero_columns": physical["special_zero_columns"],
        "heavy_mass_spectrum_real_directions": (
            physical["heavy_mass_spectrum_real_directions"]),
    }
    factorized_hash = sha256(json.dumps(
        factorized, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    assert factorized_hash == physical["factorized_physical_basis_sha256"]

    final_masses = np.r_[masses[heavy], np.zeros(38)]
    H0 = (Upre*masses)@Upre.T
    H1 = (U*final_masses)@U.T
    roundtrip = float(np.max(abs(H0-H1)))
    assert roundtrip < 2e-8
    expected = np.asarray([377/30, 77/6, 79/6])
    beta = np.asarray(physical["heavy_scalar_one_loop_beta_indices_order_1_2_3"])
    assert np.max(abs(beta-expected)) < 2e-8
    assert physical["disposition"] == {
        "positive_heavy_real": 290,
        "gauge_goldstone_real": 33,
        "pq_real": 1,
        "light_higgs_real": 4,
        "total": 328,
    }
    print("INDEPENDENT_328_PHYSICAL_BASIS_REPLAY_PASS")
    print("FACTORIZED_PHYSICAL_BASIS_SHA256", factorized_hash)
    print("REBUILT_DENSE_FLOAT17_SHA256_DIAGNOSTIC", rebuilt_hash)
    print("MAX_ORTHOGONALITY_RESIDUAL", identity_residual)
    print("MAX_ZERO_SUBSPACE_RESIDUAL", zero_subspace_residual)
    print("MAX_HESSIAN_ROUNDTRIP_RESIDUAL", roundtrip)


if __name__ == "__main__":
    main()
