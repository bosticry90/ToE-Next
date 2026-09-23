"""Exact M05 contraction for quartics built from the Sigma K/T bilinears.

This extends the 15-direction radial-Sigma regression by

* phi^dagger K(Sigma,Sigma*) phi;
* Re/Im[T(Sigma,Sigma) phi phi]; and
* Re/Im[Phi T(Sigma,Sigma) S].

Together these form a rank-20 exact scalar subtheory over all 328 internal
real directions.  The four non-radial pure-Sigma/Phi-Sigma directions and
zEta remain outside this implementation checkpoint.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from sympy import I, Matrix, conjugate, simplify, sqrt, zeros

from compile_real_field_basis import canonical_real_basis
from m05_parent_scalar_kernel import projector_backgrounds
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from m05_sigma_radial_kernel import (
    NAMES as RADIAL_NAMES, _dot, _full_coordinates, _hessians,
)
from test_eta1_invariant import parity


HERE = Path(__file__).resolve().parent
BILINEAR_NAMES = (
    "lambdaSigmaphi2", "zD_re", "zD_im", "z4_re", "z4_im",
)
NAMES = RADIAL_NAMES + BILINEAR_NAMES


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def _poly_add(target, source, factor=1):
    for monomial, coefficient in source.items():
        value = target.get(monomial, 0) + factor * coefficient
        if value == 0:
            target.pop(monomial, None)
        else:
            target[monomial] = simplify(value)
    return target


def _poly_mul(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            key = tuple(sorted(a + b))
            out[key] = out.get(key, 0) + ca * cb
    return {key: simplify(value) for key, value in out.items() if value != 0}


def _poly_conjugate(poly):
    return {key: conjugate(value) for key, value in poly.items()}


def _linear_maps(basis):
    sigma = {}
    phi = [dict() for _ in range(10)]
    singlet = {}
    parent_phi = [[{} for _ in range(10)] for _ in range(10)]
    for coordinate, entry in enumerate(basis):
        if entry.sector == "Sigma":
            for key, (a, b) in entry.state.Sigma.items():
                sigma.setdefault(key, {})[coordinate] = simplify(a + I * b)
        elif entry.sector == "phi":
            for i, value in enumerate(entry.state.phi):
                if value != 0:
                    phi[i][(coordinate,)] = value
        elif entry.sector == "S" and entry.state.S != 0:
            singlet[(coordinate,)] = entry.state.S
        elif entry.sector == "Phi":
            for i in range(10):
                for j in range(10):
                    value = entry.state.Phi[i, j]
                    if value != 0:
                        parent_phi[i][j][(coordinate,)] = value
    return sigma, phi, singlet, parent_phi


def _ordered_sigma(indices, sigma):
    if len(set(indices)) != 5:
        return {}
    sign = parity(indices)
    return {(coordinate,): sign * value
            for coordinate, value in sigma.get(tuple(sorted(indices)), {}).items()}


def _sigma_bilinears(sigma):
    k = [[{} for _ in range(10)] for _ in range(10)]
    t = [[{} for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            kp, tp = {}, {}
            for four in combinations(range(10), 4):
                left = _ordered_sigma((i,) + four, sigma)
                right = _ordered_sigma((j,) + four, sigma)
                if not left or not right:
                    continue
                _poly_add(kp, _poly_mul(left, _poly_conjugate(right)))
                _poly_add(tp, _poly_mul(left, right))
            k[i][j], t[i][j] = kp, tp
    return k, t


def _physical_pair(raw):
    real = {}
    imag = {}
    for monomial, coefficient in raw.items():
        real[monomial] = simplify(coefficient + conjugate(coefficient))
        imag[monomial] = simplify(I * coefficient + conjugate(I * coefficient))
    return ({key: value for key, value in real.items() if value != 0},
            {key: value for key, value in imag.items() if value != 0})


def build_polynomials(basis):
    sigma, phi, singlet, parent_phi = _linear_maps(basis)
    k, t = _sigma_bilinears(sigma)
    hermitian = {}
    zd_raw = {}
    z4_raw = {}
    for i in range(10):
        for j in range(10):
            if k[i][j]:
                term = _poly_mul(_poly_conjugate(phi[i]), k[i][j])
                term = _poly_mul(term, phi[j])
                _poly_add(hermitian, term)
            if t[i][j]:
                _poly_add(zd_raw, _poly_mul(_poly_mul(phi[i], t[i][j]), phi[j]))
                if parent_phi[i][j]:
                    term = _poly_mul(parent_phi[i][j], t[i][j])
                    _poly_add(z4_raw, _poly_mul(term, singlet))
    zd_re, zd_im = _physical_pair(zd_raw)
    z4_re, z4_im = _physical_pair(z4_raw)
    result = (hermitian, zd_re, zd_im, z4_re, z4_im)
    assert all(all(len(monomial) == 4 for monomial in poly)
               for poly in result)
    return result


def _evaluate(poly, point):
    return simplify(sum(coefficient * _monomial_value(monomial, point)
                        for monomial, coefficient in poly.items()))


def _monomial_value(monomial, point):
    value = 1
    for coordinate in monomial:
        value *= point[coordinate]
    return value


def _hessian(poly, point):
    result = {}
    for monomial, coefficient in poly.items():
        powers = Counter(monomial)
        support = tuple(powers)
        for i in support:
            for j in support:
                if i == j and powers[i] < 2:
                    continue
                value = coefficient * powers[i] * (powers[j] - int(i == j))
                remaining = dict(powers)
                remaining[i] -= 1
                remaining[j] -= 1
                for coordinate, power in remaining.items():
                    if power:
                        value *= point[coordinate] ** power
                if value != 0:
                    result[(i, j)] = result.get((i, j), 0) + value
    return {key: simplify(value) for key, value in result.items() if value != 0}


def compute_kernel():
    basis = canonical_real_basis()
    active_basis = [entry for entry in basis if entry.sector != "Sigma"]
    from m05_parent_scalar_kernel import _active_polynomial_terms
    _, active_terms = _active_polynomial_terms(active_basis)
    polynomials = build_polynomials(basis)
    backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]

    # Direct parent-oracle equality for every new polynomial on three
    # algebraically unrelated Sigma-bearing backgrounds.
    full_indices = {name: index for index, name in enumerate(REAL_DIRECTION_NAMES)}
    for background in backgrounds[11:14]:
        point = _full_coordinates(background, basis)
        expected = physical_quartics(background)
        for name, poly in zip(BILINEAR_NAMES, polynomials):
            assert _evaluate(poly, point) == expected[full_indices[name]]

    full_eval = Matrix([[24 * value for value in physical_quartics(state)]
                        for state in backgrounds])
    selected_columns = [full_indices[name] for name in NAMES]
    sub_eval = full_eval[:, selected_columns]
    _, row_pivots = sub_eval.T.rref()
    assert len(row_pivots) == 20
    projector = sub_eval[list(row_pivots), :]
    assert projector.rank() == 20

    diagonal, inventories = [], []
    for row in row_pivots:
        background = backgrounds[row]
        point = _full_coordinates(background, basis)
        hessians = _hessians(background, basis, active_terms)
        hessians.extend(_hessian(poly, point) for poly in polynomials)
        matrix = zeros(20)
        for a in range(20):
            for b in range(a, 20):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "background_row": row,
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv()
    projected = []
    for output in range(20):
        matrix = zeros(20)
        for witness, value in enumerate(diagonal):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal):
        replay = zeros(20)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(NAMES, projected)
    }
    inventory = {
        "parent_internal_real_directions": 328,
        "quartic_directions": list(NAMES),
        "projector_rows": list(row_pivots),
        "projector_rank": 20,
        "polynomial_monomial_counts": {
            name: len(poly) for name, poly in zip(BILINEAR_NAMES, polynomials)
        },
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_SIGMA_BILINEAR_SCALAR_SUBTHEORY_PASS",
        "authority": "IMPLEMENTATION_REGRESSION_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 20,
        "projection_residual": "0",
        "direct_parent_oracle_regression_backgrounds": 3,
        "direct_parent_oracle_residual": "0",
        "missing_for_M05": [
            "lambdaPhiSigma2",
            "lambdaSigma2/3/4",
            "zEta real/imaginary",
            "partial-BFM gauge completion",
            "complete independent replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_kernel()
    (HERE / "uvp_m05_sigma_bilinear_subtheory.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("MONOMIAL_COUNTS", result["inventory"]["polynomial_monomial_counts"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
