"""Compile the all-33-vector partial-background-field R_xi quadratic layer.

This gate constructs the gauge orbit in the passed canonical 328-real basis.
It certifies vector/Goldstone/ghost mass pairing and the explicit Goldstone
identity for arbitrary positive xi.  It does not claim the finite one-loop
general-xi cancellation or compile interaction vertices.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, Rational, sqrt, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
sys.path[:0] = [
    str(HERE),
    str(CALC / "canonical_so10_vacuum_kernel"),
    str(CALC / "canonical_so10_scalar_reconstruction"),
]

from compile_real_field_basis import canonical_real_basis
from materialize_physical_basis import state_coordinates
from derive_stabilizers import form_action, generators, phase_complex_structure
from verify_eta1_doublet_mixing import vacuum_form
from parent_bilinear_oracle import State


PHYSICAL_BASIS_HASH = (
    "af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e"
)


def sparse_vector(entries):
    out = np.zeros(328)
    for i, value in entries:
        out[i] = float(value)
    return out


def physical_goldstones(physical):
    return np.column_stack([
        sparse_vector(column)
        for column in physical["special_zero_columns"]["gauge_33"]
    ])


def full_orbit_map(parent_basis):
    """Return Q with M_V^2/(g10^2 omega^2)=Q.T Q."""
    phi0 = Matrix.diag(*([-2] * 6 + [3] * 4))
    sigma_scale = sqrt(Rational(15, 8)) / 10
    sigma0 = vacuum_form()
    columns = []
    for _, raw_generator in generators():
        dphi = (raw_generator * phi0 - phi0 * raw_generator) / sqrt(2)
        raw_sigma = form_action(raw_generator, sigma0)
        dsigma = {
            idx: (sigma_scale * a / sqrt(2), sigma_scale * b / sqrt(2))
            for idx, (a, b) in raw_sigma.items()
        }
        orbit = state_coordinates(
            State(dphi, dsigma, (0,) * 10, 0), parent_basis)
        columns.append(orbit / np.sqrt(60.0))
    return np.column_stack(columns)


def adjoint_matrix(t, gens):
    pairs = [pair for pair, _ in gens]
    slots = tuple(zip(*pairs))
    return np.column_stack([
        np.asarray(t @ np.asarray(g, dtype=float)
                   - np.asarray(g, dtype=float) @ t, dtype=float)[slots]
        for _, g in gens
    ])


def index_ledger(gram):
    gens = generators()
    j = [np.asarray(phase_complex_structure(((2 * k, 2 * k + 1),)),
                    dtype=float) for k in range(5)]
    sm = (
        (2 * (j[0] + j[1] + j[2]) - 3 * (j[3] + j[4])) / np.sqrt(60),
        (j[3] - j[4]) / 2,
        (j[0] - j[1]) / 2,
    )
    eigenvalues, vectors = np.linalg.eigh(gram)
    groups = ((.005, 8), (.025, 1), (50 / 120, 12), (50.6 / 120, 12))
    rows = []
    for t in sm:
        adjoint = adjoint_matrix(t, gens)
        assert np.max(abs(gram @ adjoint - adjoint @ gram)) < 2e-10
        insertion = -adjoint @ adjoint
        rows.append([
            float(np.trace((q := vectors[:, abs(eigenvalues-value) < 1e-9]).T
                           @ insertion @ q).real)
            for value, count in groups
        ])
    by_group = np.asarray(rows).T
    assert np.allclose(by_group[0], [14 / 5, 0, 1])
    assert np.allclose(by_group[1], [0, 0, 0])
    assert np.allclose(by_group[2], [5, 3, 2])
    assert np.allclose(by_group[3], [1 / 5, 3, 2])
    assert np.allclose(np.sum(by_group, axis=0), [8, 6, 5])
    return by_group


def main():
    physical = json.loads((HERE / "physical_basis.json").read_text(
        encoding="utf-8"))
    assert physical["factorized_physical_basis_sha256"] == PHYSICAL_BASIS_HASH
    parent_basis = canonical_real_basis()
    Q = full_orbit_map(parent_basis)
    assert Q.shape == (328, 45)
    gram = Q.T @ Q
    eigenvalues = np.linalg.eigvalsh(gram)
    expected = ((0.0, 12), (.005, 8), (.025, 1), (50 / 120, 12),
                (50.6 / 120, 12))
    for value, count in expected:
        assert np.count_nonzero(abs(eigenvalues-value) < 2e-10) == count

    left, singular, _ = np.linalg.svd(Q, full_matrices=False)
    positive = singular > 1e-9
    orbit_goldstones = left[:, positive]
    stored_goldstones = physical_goldstones(physical)
    projector_residual = float(np.max(abs(
        orbit_goldstones @ orbit_goldstones.T
        - stored_goldstones @ stored_goldstones.T)))
    assert projector_residual < 3e-9

    vector_positive = np.sort(eigenvalues[eigenvalues > 1e-10])
    scalar_positive = np.sort(singular[positive] ** 2)
    assert np.max(abs(vector_positive-scalar_positive)) < 2e-12
    xi_residuals = {}
    for xi in (.5, 1.0, 2.0):
        ghost = xi * vector_positive
        goldstone = xi * scalar_positive
        residual = float(np.max(abs(ghost-goldstone)))
        assert residual < 2e-12
        xi_residuals[format(xi, ".1f")] = residual

    indices = index_ledger(gram)
    payload = {
        "outcome": "BACKGROUND_FIELD_QUADRATIC_LAYER_PASS",
        "physical_basis_sha256": PHYSICAL_BASIS_HASH,
        "gauge_convention": (
            "partial background-field R_xi: F_A=Dbar.A_A-"
            "xi*g10*omega*(Q^T eta)_A"
        ),
        "vector_mass_operator": "g10^2*omega^2*Q^T*Q",
        "goldstone_gauge_fixing_mass_operator": (
            "xi*g10^2*omega^2*Q*Q^T on image(Q)"
        ),
        "complex_ghost_mass_operator": "xi*g10^2*omega^2*Q^T*Q",
        "counts": {
            "unbroken_sm_vectors": 12,
            "massive_vectors": 33,
            "real_gauge_goldstones": 33,
            "complex_heavy_ghosts": 33,
        },
        "mass_squared_over_g10_squared_omega_squared": [
            {"value": value, "multiplicity": count}
            for value, count in expected if value
        ],
        "max_goldstone_orbit_projector_residual": projector_residual,
        "xi_mass_pairing_residuals": xi_residuals,
        "vector_sm_indices_by_mass_group_order_1_2_3": indices.tolist(),
        "total_massive_vector_sm_index": np.sum(indices, axis=0).tolist(),
        "lower_ps_sm_broken_vector_index": indices[0].tolist(),
        "outside_quadratic_sublayer_authority": [
            "general_xi_one_loop_F2_cancellation",
            "complete_background_quantum_vector_goldstone_ghost_vertices",
            "sparse_physical_vertex_api_core",
            "two_loop_diagram_generation",
        ],
    }
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["quadratic_layer_sha256"] = sha256(packed.encode()).hexdigest()
    (HERE / "background_field_quadratic.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("MASSIVE_VECTOR_GOLDSTONE_GHOST_COUNT", 33)
    print("MAX_GOLDSTONE_PROJECTOR_RESIDUAL", projector_residual)
    print("TOTAL_VECTOR_SM_INDEX", payload["total_massive_vector_sm_index"])
    print("LOWER_VECTOR_SM_INDEX", payload["lower_ps_sm_broken_vector_index"])
    print("QUADRATIC_LAYER_SHA256", payload["quadratic_layer_sha256"])


if __name__ == "__main__":
    main()
