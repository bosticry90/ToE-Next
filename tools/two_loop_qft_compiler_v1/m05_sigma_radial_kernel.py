"""Exact M05 scalar contraction including the radial Sigma invariants.

This extends the 11-direction Phi+phi+S checkpoint by the four quartics that
depend on Sigma only through N=|Sigma|^2:

    p2*N, N^2, N*u, N*|S|^2.

All 328 canonical real internal directions participate.  The result is a
15-direction implementation regression, not the complete M05 residue; the
non-radial Sigma tensors remain outstanding.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Matrix, Rational, simplify, zeros


from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from m05_parent_scalar_kernel import (
    ACTIVE_QUARTICS, _active_polynomial_terms, _hessian_from_terms,
)
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from m05_parent_scalar_kernel import projector_backgrounds


HERE = Path(__file__).resolve().parent
RADIAL_SIGMA_NAMES = (
    "lambdaPhiSigma1", "lambdaSigma1", "lambdaSigmaphi1",
    "lambdaSigmaS",
)
NAMES = ACTIVE_QUARTICS + RADIAL_SIGMA_NAMES


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def _sparse(matrix):
    return {(i, j): matrix[i, j]
            for i in range(matrix.rows) for j in range(matrix.cols)
            if matrix[i, j] != 0}


def _dot(left, right):
    if len(left) > len(right):
        left, right = right, left
    return simplify(sum(value * right.get(key, 0)
                        for key, value in left.items()))


def _outer_hessian(point, left_slice, right_slice, right_factor=1):
    """Hessian of (x.x)*right_factor*(y.y) on disjoint slices."""
    result = {}
    left_norm = sum(point[i] ** 2 for i in left_slice)
    right_norm = right_factor * sum(point[i] ** 2 for i in right_slice)
    for i in left_slice:
        result[(i, i)] = result.get((i, i), 0) + 2 * right_norm
    for j in right_slice:
        result[(j, j)] = result.get((j, j), 0) + 2 * right_factor * left_norm
    for i in left_slice:
        if point[i] == 0:
            continue
        for j in right_slice:
            if point[j] == 0:
                continue
            value = 4 * right_factor * point[i] * point[j]
            result[(i, j)] = result.get((i, j), 0) + value
            result[(j, i)] = result.get((j, i), 0) + value
    return {key: simplify(value) for key, value in result.items() if value != 0}


def _radial_square_hessian(point, sector_slice):
    norm = sum(point[i] ** 2 for i in sector_slice)
    result = {(i, i): 4 * norm for i in sector_slice}
    for i in sector_slice:
        if point[i] == 0:
            continue
        for j in sector_slice:
            if point[j] != 0:
                result[(i, j)] = result.get((i, j), 0) + 8 * point[i] * point[j]
    return {key: simplify(value) for key, value in result.items() if value != 0}


def _full_coordinates(state, basis):
    return tuple(simplify(real_kinetic_inner(entry.state, state))
                 for entry in basis)


def _active_point(full_point):
    return full_point[:54] + full_point[306:326] + full_point[326:328]


def _embed_active(hessian):
    mapping = tuple(range(54)) + tuple(range(306, 328))
    return {(mapping[i], mapping[j]): hessian[i, j]
            for i in range(76) for j in range(76)
            if hessian[i, j] != 0}


def _hessians(background, basis, active_terms):
    point = _full_coordinates(background, basis)
    active = _active_point(point)
    result = [_embed_active(_hessian_from_terms(rows, active))
              for rows in active_terms]
    phi = range(0, 54)
    sigma = range(54, 306)
    vector = range(306, 326)
    singlet = range(326, 328)
    result.extend((
        _outer_hessian(point, phi, sigma),
        _radial_square_hessian(point, sigma),
        _outer_hessian(point, sigma, vector, right_factor=Rational(1, 2)),
        _outer_hessian(point, sigma, singlet, right_factor=Rational(1, 2)),
    ))
    assert len(result) == 15
    return result


def compute_kernel():
    basis = canonical_real_basis()
    assert len(basis) == 328
    active_basis = [entry for entry in basis if entry.sector != "Sigma"]
    _, active_terms = _active_polynomial_terms(active_basis)
    all_backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]
    full_name_index = {name: index for index, name in enumerate(REAL_DIRECTION_NAMES)}
    selected_columns = [full_name_index[name] for name in NAMES]
    full_eval = Matrix([[24 * value for value in physical_quartics(state)]
                        for state in all_backgrounds])
    sub_eval = full_eval[:, selected_columns]
    _, row_pivots = sub_eval.T.rref()
    assert len(row_pivots) == 15
    projector = sub_eval[list(row_pivots), :]
    assert projector.rank() == 15

    diagonal = []
    inventories = []
    for row in row_pivots:
        hessians = _hessians(all_backgrounds[row], basis, active_terms)
        matrix = zeros(15)
        for a in range(15):
            for b in range(a, 15):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "background_row": row,
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv()
    projected = []
    for output in range(15):
        matrix = zeros(15)
        for witness, value in enumerate(diagonal):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal):
        replay = zeros(15)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    sigma_index = NAMES.index("lambdaSigma1")
    assert projected[sigma_index][sigma_index, sigma_index] == 1040
    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(NAMES, projected)
    }
    inventory = {
        "parent_internal_real_directions": 328,
        "quartic_directions": list(NAMES),
        "projector_rows": list(row_pivots),
        "projector_rank": 15,
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_SIGMA_RADIAL_SCALAR_SUBTHEORY_PASS",
        "authority": "IMPLEMENTATION_REGRESSION_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 15,
        "projection_residual": "0",
        "lambdaSigma1_squared_control": "1040",
        "missing_for_M05": [
            "non-radial Sigma quartics lambdaSigma2/3/4",
            "lambdaPhiSigma2 and lambdaSigmaphi2",
            "z4 zEta zD real/imaginary contractions",
            "partial-BFM gauge completion",
            "complete independent replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_kernel()
    (HERE / "uvp_m05_sigma_radial_subtheory.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("LAMBDA_SIGMA1_SQUARED", result["lambdaSigma1_squared_control"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
