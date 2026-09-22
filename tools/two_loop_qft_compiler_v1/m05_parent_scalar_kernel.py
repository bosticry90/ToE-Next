"""Exact sparse UVP_M05 quartic-contraction kernel.

This module implements the complete scalar ``V4*V4`` contraction and exact
invariant projection for the Phi+phi+S closed subspace.  It is deliberately
not advertised as the full M05 kernel: the Sigma-containing invariant blocks
and the partial-BFM gauge-generated quartics remain required before M05 can be
rerun.  Keeping that boundary explicit prevents a successful subspace test
from being mistaken for the 26-direction canonical result.

For a homogeneous quartic potential with Hessian H2(q),

    V_div^(1)|_4 = 1/4 Tr[H2(q)^2].

Equivalently, the diagonal fourth derivative of the pole is

    R(q,q,q,q) = 3/2 sum_(A,B) V4(q,q,e_A,e_B)^2.

The implementation evaluates this identity in the canonical real basis and
projects the result on exact quartic invariant witnesses.  No dense rank-four
tensor is materialized.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import I, Matrix, Poly, conjugate, simplify, symbols, zeros

from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from m03_parent_scalar_kernel import add_state, digest
from m04_parent_scalar_kernel import (
    QUARTIC_NAMES, quartic_vector,
)
from parent_bilinear_oracle import State


HERE = Path(__file__).resolve().parent

ACTIVE_SECTORS = ("Phi", "phi", "S")
ACTIVE_QUARTICS = QUARTIC_NAMES


def _state(diagonal=(), off_diagonal=(), vector=(), singlet=0):
    """Create a rational/Gaussian-rational projector background."""
    phi = [0] * 10
    p = zeros(10)
    assert len(diagonal) in (0, 10)
    for i, value in enumerate(diagonal):
        p[i, i] = value
    assert simplify(p.trace()) == 0
    for i, j, value in off_diagonal:
        assert i < j
        p[i, j] = p[j, i] = value
    for i, value in vector:
        phi[i] = value
    return State(p, {}, tuple(phi), singlet)


def projector_backgrounds():
    """Eleven exact witnesses selected by deterministic rank growth.

    Their fourth-derivative evaluation matrix has full rank 11.  The
    witnesses contain no Sigma component, so they certify precisely the
    Phi+phi+S quartic subspace and nothing beyond it.
    """
    return (
        _state((-1, 0, 0, 0, 0, 1, 0, 2, 2, -4),
               ((0, 5, 2), (6, 9, -2))),
        _state(singlet=-2 + 2 * I),
        _state((1, -2, 1, 0, 0, 1, -1, 2, 2, -4),
               vector=((1, -2 - I), (8, 2 + I)), singlet=-2),
        _state((-2, 1, -2, 1, 1, -1, -2, 2, 1, 1),
               singlet=-2 + 2 * I),
        _state((0, -2, 1, 0, -2, 1, 2, -1, -2, 3),
               ((0, 7, -1),)),
        _state((-1, 1, 0, -1, 0, 1, -2, 0, 1, 1),
               vector=((0, -1 - 2 * I),), singlet=2 - I),
        _state((2, 2, 1, 2, -1, -1, 0, 0, 1, -6),
               vector=((6, 2 * I), (7, -2 - 2 * I)), singlet=-2 + I),
        _state(vector=((3, 1 + 2 * I),)),
        _state(vector=((1, -1 + 2 * I), (2, -2 - 2 * I),
                       (7, -2 + 2 * I))),
        _state((1, -2, -1, -2, 2, 2, -1, -2, 1, 2),
               ((3, 4, 1),), vector=((0, 1 - I),), singlet=2 + 2 * I),
        _state((2, 0, 1, -1, -2, -2, -1, -2, -1, 6),
               ((2, 7, -1), (3, 7, -2)),
               vector=((0, I), (4, -2)), singlet=2 + I),
    )


def evaluation_matrix(backgrounds=None):
    backgrounds = backgrounds or projector_backgrounds()
    matrix = Matrix([[24 * value for value in quartic_vector(q)]
                     for q in backgrounds])
    assert matrix.shape == (11, 11)
    assert matrix.rank() == 11
    assert matrix.det() != 0
    return matrix


def _active_polynomial_terms(active_basis):
    """Build the eleven quartics once as sparse degree-four polynomials."""
    coordinates = symbols("y0:76", real=True)
    p = zeros(10)
    x = [0] * 10
    s = 0
    for coordinate, entry in zip(coordinates, active_basis):
        p += coordinate * entry.state.Phi
        x = [left + coordinate * right
             for left, right in zip(x, entry.state.phi)]
        s += coordinate * entry.state.S
    p2 = (p * p).trace()
    p4 = (p * p * p * p).trace()
    u = sum(conjugate(value) * value for value in x)
    t = sum(value * value for value in x)
    abs_s2 = conjugate(s) * s
    p_squared = p * p
    phi_p2_phi = sum(conjugate(x[i]) * p_squared[i, j] * x[j]
                       for i in range(10) for j in range(10))
    vector_p = sum(p[i, j] * x[i] * x[j]
                   for i in range(10) for j in range(10))
    zk = vector_p * conjugate(s)
    expressions = (
        p2 * p2, p4, p2 * u, phi_p2_phi, p2 * abs_s2,
        u * u, t * conjugate(t), u * abs_s2, abs_s2 * abs_s2,
        zk + conjugate(zk), I * zk + conjugate(I * zk),
    )
    terms = [Poly(expression, *coordinates).terms()
             for expression in expressions]
    assert all(all(sum(monomial) == 4 for monomial, _ in rows)
               for rows in terms)
    return coordinates, terms


def _coordinates(state, active_basis):
    values = tuple(simplify(real_kinetic_inner(entry.state, state))
                   for entry in active_basis)
    reconstructed = zeros(10)
    for value, entry in zip(values, active_basis):
        reconstructed += value * entry.state.Phi
    assert reconstructed == state.Phi
    return values


def _hessian_from_terms(terms, point):
    """Evaluate an exact quartic Hessian from sparse monomials."""
    dimension = len(point)
    hessian = [[0 for _ in range(dimension)] for _ in range(dimension)]
    for powers, coefficient in terms:
        support = [index for index, power in enumerate(powers) if power]
        for i in support:
            for j in support:
                if i == j and powers[i] < 2:
                    continue
                multiplier = powers[i] * (powers[j] - int(i == j))
                value = coefficient * multiplier
                for index in support:
                    remaining = powers[index] - int(index == i) - int(index == j)
                    if remaining:
                        value *= point[index] ** remaining
                if value != 0:
                    hessian[i][j] += value
    return Matrix(hessian)


def _coefficient_matrix(q, active_basis, polynomial_terms):
    """Return the 11x11 coefficient matrix in R(q,q,q,q)."""
    point = _coordinates(q, active_basis)
    hessians = [_hessian_from_terms(rows, point) for rows in polynomial_terms]
    size = len(ACTIVE_QUARTICS)
    result = zeros(size)
    for a in range(size):
        for b in range(a, size):
            # _hessian_from_terms returns d2 I = V4(q,q,.,.)/2.
            # Hence (3/2) sum V4_a V4_b = 6 Tr(H_a H_b).
            value = simplify(6 * sum(
                hessians[a][i, j] * hessians[b][i, j]
                for i in range(76) for j in range(76)
            ))
            result[a, b] = result[b, a] = value
    nonzero = []
    for i in range(76):
        for j in range(i, 76):
            if any(hessian[i, j] != 0 for hessian in hessians):
                nonzero.append((active_basis[i].name, active_basis[j].name,
                                1 if i == j else 2))
    assert result == result.T
    return result, nonzero


def compute_active_scalar_kernel():
    basis = [entry for entry in canonical_real_basis()
             if entry.sector in ACTIVE_SECTORS]
    assert len(basis) == 76
    backgrounds = projector_backgrounds()
    projector = evaluation_matrix(backgrounds)
    _, polynomial_terms = _active_polynomial_terms(basis)

    diagonal_matrices = []
    inventories = []
    for index, background in enumerate(backgrounds):
        matrix, nonzero = _coefficient_matrix(
            background, basis, polynomial_terms
        )
        diagonal_matrices.append(matrix)
        inventories.append({
            "background": index,
            "unordered_internal_pairs": 76 * 77 // 2,
            "nonzero_unordered_internal_pairs": len(nonzero),
            "nonzero_pair_sha256": digest(nonzero),
        })

    inverse = projector.inv()
    projected = []
    for output in range(len(ACTIVE_QUARTICS)):
        matrix = zeros(len(ACTIVE_QUARTICS))
        for witness, diagonal in enumerate(diagonal_matrices):
            matrix += inverse[output, witness] * diagonal
        matrix = matrix.applyfunc(simplify)
        assert matrix == matrix.T
        projected.append(matrix)

    # Exact round trip on every projector witness.
    for witness, diagonal in enumerate(diagonal_matrices):
        replay = zeros(len(ACTIVE_QUARTICS))
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == diagonal

    inventory = {
        "scope": "Phi+phi+S_scalar_V4V4_subspace",
        "parent_real_directions_total": 328,
        "active_internal_real_directions": 76,
        "Sigma_directions_deliberately_not_claimed": 252,
        "quartic_directions_certified": len(ACTIVE_QUARTICS),
        "quartic_direction_names": list(ACTIVE_QUARTICS),
        "sparse_polynomial_monomial_counts": [len(rows)
                                               for rows in polynomial_terms],
        "projector_rank": projector.rank(),
        "projector_determinant": str(projector.det()),
        "background_inventories": inventories,
    }
    coefficient_tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(ACTIVE_QUARTICS, projected)
    }
    payload = {
        "schema_version": 1,
        "authority": "M05_SCALAR_SUBSPACE_IMPLEMENTATION_NOT_GATE_PASS",
        "functional_identity": "R4(q)=3/2*sum_AB[V4(q,q,eA,eB)^2]",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "projector_matrix": [[str(value) for value in row]
                             for row in projector.tolist()],
        "coefficient_tables": coefficient_tables,
        "projection_rank": 11,
        "projection_residual": "0",
        "external_permutation_residual": "0_by_fourth_derivative_polarization",
        "not_yet_authorized": [
            "Sigma-containing scalar V4V4 contractions",
            "complete 26-real-direction projector",
            "partial-BFM gauge/Goldstone/ghost quartic completion",
            "UVP_M05 attempt 2 adjudication",
        ],
    }
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["artifact_sha256"] = sha256(packed.encode()).hexdigest()
    return payload


if __name__ == "__main__":
    result = compute_active_scalar_kernel()
    (HERE / "uvp_m05_active_scalar_subspace.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print("M05_ACTIVE_SCALAR_SUBSPACE_COMPLETE")
    print("PROJECTOR_RANK", result["projection_rank"])
    print("INVENTORY_SHA256", result["inventory_sha256"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
