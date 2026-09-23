"""Exact pure-Sigma M05 scalar regression for all four quartics.

The four independent invariants are represented by the radial norm square,
the norms of the k=1 and k=2 paired tensors, and the (1,3,1) crossed
contraction of the k=1 paired tensor.  Hessians are assembled from exact
bilinear paired-tensor derivatives in the 252-real canonical Sigma basis;
no dense rank-four field tensor is materialized.

This is a calculation-local M05 implementation regression.  It does not
include zEta or the partial-BFM gauge completion and therefore is not an
UVP_M05 pass.
"""

from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path

from sympy import Matrix, simplify, zeros

from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from m05_rank26_projector import physical_quartics, sigma_backgrounds
from m05_sigma_radial_kernel import _dot, _radial_square_hessian
from parent_bilinear_oracle import State
from certify_sigma_quartics import paired_tensor
from test_eta1_invariant import add, mul, parity


HERE = Path(__file__).resolve().parent
NAMES = ("lambdaSigma1", "lambdaSigma2", "lambdaSigma3", "lambdaSigma4")


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def _pair_scale(value, factor):
    return (factor * value[0], factor * value[1])


def _tensor_add(left, right, factor=1):
    out = dict(left)
    for key, value in right.items():
        out[key] = add(out.get(key, (0, 0)), _pair_scale(value, factor))
        if out[key] == (0, 0):
            out.pop(key)
    return out


def _paired_cross(left, right, k):
    """D2 paired_tensor[left,right], including both ordered cross terms."""
    out = {}
    for first, second in ((left, right), (right, left)):
        for ia, za in first.items():
            overlap_source = set(ia)
            for ib, zb in second.items():
                overlap = tuple(i for i in ia if i in ib and i in overlap_source)
                for shared in combinations(overlap, k):
                    rem_a = tuple(i for i in ia if i not in shared)
                    rem_b = tuple(i for i in ib if i not in shared)
                    sign = parity(shared + rem_a) * parity(shared + rem_b)
                    value = mul(za, zb)
                    value = _pair_scale(value, sign)
                    key = (rem_a, rem_b)
                    out[key] = add(out.get(key, (0, 0)), value)
    return {key: value for key, value in out.items() if value != (0, 0)}


def _norm_cross(left, right):
    common = set(left) & set(right)
    return simplify(2 * sum(
        left[key][0] * right[key][0] + left[key][1] * right[key][1]
        for key in common
    ))


def _cross_dual(first, y=3, z=1):
    """Map the first crossed-contraction slot to its sparse dual tensor."""
    dual = {}
    for (ia, ib), za in first.items():
        for ac in combinations(ia, y):
            ad = tuple(i for i in ia if i not in ac)
            sign_a = parity(ac + ad)
            for bc in combinations(ib, z):
                bd = tuple(i for i in ib if i not in bc)
                sign_b = parity(bc + bd)
                raw_c = ac + bc
                raw_d = ad + bd
                if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                    continue
                key = (tuple(sorted(raw_c)), tuple(sorted(raw_d)))
                sign = sign_a * sign_b * parity(raw_c) * parity(raw_d)
                dual[key] = add(dual.get(key, (0, 0)),
                                _pair_scale(za, sign))
    return {key: value for key, value in dual.items() if value != (0, 0)}


def _dual_inner(dual, second):
    result = (0, 0)
    for key in set(dual) & set(second):
        value = mul(dual[key], (second[key][0], -second[key][1]))
        result = add(result, value)
    return result


def _crossed_bilinear(left, left_dual, right, right_dual):
    value = add(_dual_inner(left_dual, right),
                _dual_inner(right_dual, left))
    assert simplify(value[1]) == 0
    return simplify(value[0])


def _sigma_coordinates(form, sigma_basis):
    state = State(zeros(10), form, (0,) * 10, 0)
    return tuple(simplify(real_kinetic_inner(entry.state, state))
                 for entry in sigma_basis)


def _pure_state(form):
    return State(zeros(10), form, (0,) * 10, 0)


def _build_second_derivatives(basis_forms):
    cache1, cache1_dual, cache2 = {}, {}, {}
    for i in range(len(basis_forms)):
        for j in range(i, len(basis_forms)):
            cache1[(i, j)] = _paired_cross(basis_forms[i], basis_forms[j], 1)
            cache1_dual[(i, j)] = _cross_dual(cache1[(i, j)])
            cache2[(i, j)] = _paired_cross(basis_forms[i], basis_forms[j], 2)
    return cache1, cache1_dual, cache2


def _sigma_hessians(form, sigma_basis, basis_forms,
                    second1, second1_dual, second2):
    point = _sigma_coordinates(form, sigma_basis)
    radial = _radial_square_hessian(point, range(252))
    base1 = paired_tensor(form, 1)
    base1_dual = _cross_dual(base1)
    base2 = paired_tensor(form, 2)
    first1 = [_paired_cross(form, direction, 1) for direction in basis_forms]
    first1_dual = [_cross_dual(value) for value in first1]
    first2 = [_paired_cross(form, direction, 2) for direction in basis_forms]
    q1, q2, crossed = {}, {}, {}
    for i in range(252):
        for j in range(i, 252):
            key = (i, j)
            h1 = second1[key]
            h1_dual = second1_dual[key]
            h2 = second2[key]
            v1 = simplify(_norm_cross(first1[i], first1[j])
                          + _norm_cross(base1, h1))
            v2 = simplify(_norm_cross(first2[i], first2[j])
                          + _norm_cross(base2, h2))
            vx = simplify(_crossed_bilinear(
                              first1[i], first1_dual[i],
                              first1[j], first1_dual[j])
                          + _crossed_bilinear(
                              base1, base1_dual, h1, h1_dual))
            for target, value in ((q1, v1), (q2, v2), (crossed, vx)):
                if value != 0:
                    target[(i, j)] = value
                    target[(j, i)] = value
    return (radial, q1, q2, crossed)


def compute_kernel():
    basis = canonical_real_basis()
    sigma_basis = [entry for entry in basis if entry.sector == "Sigma"]
    assert len(sigma_basis) == 252
    basis_forms = [entry.state.Sigma for entry in sigma_basis]

    candidates = [(seed, state.Sigma) for seed, state in sigma_backgrounds()]
    evaluations = Matrix([
        [24 * physical_quartics(_pure_state(form))[index]
         for index in (7, 8, 9, 10)]
        for _, form in candidates
    ])
    _, row_pivots = evaluations.T.rref()
    assert len(row_pivots) == 4
    projector = evaluations[list(row_pivots), :]
    assert projector.rank() == 4
    verification_rows = [row for row in range(len(candidates))
                         if row not in row_pivots][:1]

    print("PURE_SIGMA_D2_CACHE_START", flush=True)
    second1, second1_dual, second2 = _build_second_derivatives(basis_forms)
    print("PURE_SIGMA_D2_CACHE_DONE", len(second1), flush=True)

    rows = list(row_pivots) + verification_rows
    diagonal = []
    inventories = []
    for ordinal, row in enumerate(rows, 1):
        seed, form = candidates[row]
        print("PURE_SIGMA_BACKGROUND", ordinal, "OF", len(rows), "SEED", seed,
              flush=True)
        hessians = _sigma_hessians(
            form, sigma_basis, basis_forms, second1, second1_dual, second2
        )
        matrix = zeros(4)
        for a in range(4):
            for b in range(a, 4):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "seed": seed,
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv()
    projected = []
    for output in range(4):
        matrix = zeros(4)
        for witness, value in enumerate(diagonal[:4]):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal[:4]):
        replay = zeros(4)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    verification_residual = "0"
    for offset, row in enumerate(verification_rows, 4):
        replay = zeros(4)
        for output, matrix in enumerate(projected):
            replay += evaluations[row, output] * matrix
        assert replay.applyfunc(simplify) == diagonal[offset]

    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(NAMES, projected)
    }
    inventory = {
        "Sigma_internal_real_directions": 252,
        "quartic_directions": list(NAMES),
        "projector_seeds": [candidates[row][0] for row in row_pivots],
        "verification_seeds": [candidates[row][0] for row in verification_rows],
        "projector_rank": 4,
        "paired_tensor_second_derivatives_per_k": len(second1),
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_PURE_SIGMA_SCALAR_SUBTHEORY_PASS",
        "authority": "IMPLEMENTATION_REGRESSION_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 4,
        "projection_residual": "0",
        "independent_background_residual": verification_residual,
        "missing_for_M05": [
            "zEta real/imaginary full contraction",
            "combined 26-direction scalar assembly",
            "partial-BFM gauge completion",
            "complete independent replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_kernel()
    (HERE / "uvp_m05_pure_sigma_subtheory.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
