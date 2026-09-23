"""Exact M05 scalar contraction including the mixed Phi-Sigma tensor.

This extends the rank-20 Sigma-bilinear implementation checkpoint by the
non-factorized Hermitian invariant

    (1 / (2 3!)) Phi_ij Phi_kl Sigma_ikabc Sigma*_jlabc.

The canonical form storage sums over sorted triples, so the explicit 3!
is already accounted for and the polynomial below carries the remaining
factor 1/2, matching ``exact_mixed_l``.  The result is a rank-21 scalar
subtheory over all 328 real internal directions.  It is an implementation
regression only, not the complete UVP_M05 result.
"""

from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path

from sympy import Matrix, Rational, simplify, zeros

from compile_real_field_basis import canonical_real_basis
from m05_parent_scalar_kernel import projector_backgrounds
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from m05_sigma_bilinear_kernel import (
    NAMES as BILINEAR_NAMES, _hessian, _linear_maps, _ordered_sigma,
    build_polynomials,
)
from m05_sigma_radial_kernel import _dot, _full_coordinates, _hessians


HERE = Path(__file__).resolve().parent
NEW_NAME = "lambdaPhiSigma2"
NAMES = BILINEAR_NAMES + (NEW_NAME,)


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def build_phi_sigma_terms(basis):
    """Return factorized linear-form terms for lambdaPhiSigma2.

    Keeping each quartic as a product of four sparse linear forms avoids a
    costly global monomial expansion.  The Hessian and value are still
    exhaustive and exact on every requested background.
    """
    sigma, _, _, parent_phi = _linear_maps(basis)
    result = []
    triples = tuple(combinations(range(10), 3))

    # Cache every ordered Sigma_(i,k,a,b,c) linear form.  Repeated indices
    # correctly map to the zero polynomial through _ordered_sigma.
    sigma_at = {
        (i, k, triple): _ordered_sigma((i, k) + triple, sigma)
        for triple in triples for i in range(10) for k in range(10)
    }
    for triple in triples:
        left_pairs = [
            (i, k, sigma_at[(i, k, triple)])
            for i in range(10) for k in range(10)
            if sigma_at[(i, k, triple)]
        ]
        for i, k, left in left_pairs:
            for j, l, right in left_pairs:
                pij = parent_phi[i][j]
                pkl = parent_phi[k][l]
                if not pij or not pkl:
                    continue
                conjugated = {key: value.conjugate()
                              for key, value in right.items()}
                result.append((Rational(1, 2), pij, pkl, left, conjugated))
    assert result
    return result


def _linear_value(linear, point):
    return sum(coefficient * point[key[0]]
               for key, coefficient in linear.items())


def _mixed_value(terms, point):
    total = 0
    for coefficient, *factors in terms:
        value = coefficient
        for factor in factors:
            value *= _linear_value(factor, point)
            if value == 0:
                break
        total += value
    return simplify(total)


def _mixed_hessian(terms, point):
    """Exact background-local Hessian of the factorized quartic.

    The invariant is quadratic in Phi and quadratic in Sigma.  Assemble its
    Phi-Phi, Sigma-Sigma, and mixed blocks directly.  This avoids scanning
    all 12 ordered factor pairs and, more importantly, avoids constructing
    outer products whose two undifferentiated background factors vanish.
    """
    result = {}

    def add_outer(left, right, factor, transpose=False):
        if factor == 0:
            return
        for ir, cr in left.items():
            for js, cs in right.items():
                key = (ir[0], js[0])
                result[key] = result.get(key, 0) + factor * cr * cs
                if transpose:
                    reverse = (js[0], ir[0])
                    result[reverse] = result.get(reverse, 0) + factor * cr * cs

    for coefficient, p1, p2, s1, s2 in terms:
        vp1 = _linear_value(p1, point)
        vp2 = _linear_value(p2, point)
        vs1 = _linear_value(s1, point)
        vs2 = _linear_value(s2, point)
        add_outer(p1, p2, coefficient * vs1 * vs2, transpose=True)
        add_outer(s1, s2, coefficient * vp1 * vp2, transpose=True)
        add_outer(p1, s1, coefficient * vp2 * vs2, transpose=True)
        add_outer(p1, s2, coefficient * vp2 * vs1, transpose=True)
        add_outer(p2, s1, coefficient * vp1 * vs2, transpose=True)
        add_outer(p2, s2, coefficient * vp1 * vs1, transpose=True)
    return {key: simplify(value) for key, value in result.items()
            if value != 0}


def compute_kernel():
    basis = canonical_real_basis()
    active_basis = [entry for entry in basis if entry.sector != "Sigma"]
    from m05_parent_scalar_kernel import _active_polynomial_terms
    _, active_terms = _active_polynomial_terms(active_basis)
    bilinear_polynomials = build_polynomials(basis)
    mixed_terms = build_phi_sigma_terms(basis)
    backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]

    full_indices = {name: index for index, name in enumerate(REAL_DIRECTION_NAMES)}
    # Four unrelated Sigma-bearing witnesses directly replay the canonical
    # parent invariant oracle, independently of the contraction projection.
    for background in backgrounds[11:15]:
        point = _full_coordinates(background, basis)
        expected = physical_quartics(background)[full_indices[NEW_NAME]]
        assert _mixed_value(mixed_terms, point) == expected

    full_eval = Matrix([[24 * value for value in physical_quartics(state)]
                        for state in backgrounds])
    selected_columns = [full_indices[name] for name in NAMES]
    sub_eval = full_eval[:, selected_columns]
    _, row_pivots = sub_eval.T.rref()
    assert len(row_pivots) == 21
    projector = sub_eval[list(row_pivots), :]
    assert projector.rank() == 21

    diagonal, inventories = [], []
    for row in row_pivots:
        background = backgrounds[row]
        point = _full_coordinates(background, basis)
        hessians = _hessians(background, basis, active_terms)
        hessians.extend(_hessian(poly, point) for poly in bilinear_polynomials)
        hessians.append(_mixed_hessian(mixed_terms, point))
        matrix = zeros(21)
        for a in range(21):
            for b in range(a, 21):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "background_row": row,
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv()
    projected = []
    for output in range(21):
        matrix = zeros(21)
        for witness, value in enumerate(diagonal):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal):
        replay = zeros(21)
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
        "projector_rank": 21,
        "lambdaPhiSigma2_factorized_terms": len(mixed_terms),
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_PHI_SIGMA_MIXED_SCALAR_SUBTHEORY_PASS",
        "authority": "IMPLEMENTATION_REGRESSION_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 21,
        "projection_residual": "0",
        "direct_parent_oracle_regression_backgrounds": 4,
        "direct_parent_oracle_residual": "0",
        "missing_for_M05": [
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
    (HERE / "uvp_m05_phi_sigma_mixed_subtheory.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("FACTORIZED_TERMS",
          result["inventory"]["lambdaPhiSigma2_factorized_terms"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
