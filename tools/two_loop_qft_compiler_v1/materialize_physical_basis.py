"""Materialize the frozen benchmark's factorized 328-real physical basis."""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from sympy import I, Matrix, N, Rational, sqrt, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
FULL = CALC / "canonical_so10_full_hessian"
BENCH = CALC / "canonical_so10_scalar_benchmark"
POS = CALC / "canonical_so10_positive_higgs"
VAC = CALC / "canonical_so10_vacuum_kernel"
SCALAR = CALC / "canonical_so10_scalar_reconstruction"
sys.path[:0] = [str(HERE), str(FULL), str(BENCH), str(POS), str(VAC), str(SCALAR)]

from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from compile_all_weight_basis import (
    generate_copy, tangent_coordinates, conjugate_label, representation_matrix,
)
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import representatives, rational_representatives
from search import FREE, affine_matrices, load_blocks
from validate_candidate import kinetic_diag
from derive_stabilizers import generators, form_action, phase_complex_structure
from verify_eta1_doublet_mixing import vacuum_form
from parent_bilinear_oracle import State


ZERO_TOL = 2e-9
ORTHO_TOL = 3e-10


def numeric(z):
    return float(N(z, 30))


def load_weight_map():
    data = json.loads((HERE / "sm_weight_basis.json").read_text(encoding="utf-8"))
    assert data["outcome"] == "CANONICAL_FULL_SM_WEIGHT_BASIS_PASS"
    U = np.zeros((328, 328), dtype=float)
    metadata = []
    for j, entry in enumerate(data["columns"]):
        metadata.append(entry["metadata"])
        for i, z in entry["sparse_parent_coordinates"]:
            U[i, j] = numeric(z)
    assert np.max(abs(U.T @ U-np.eye(328))) < 2e-12
    return data, U, metadata


def frozen_blocks():
    point = json.loads((BENCH / "STAGE1_POINT.json").read_text())
    free = np.asarray([float(point["free_coefficients"][name]) for name in FREE])
    positive = json.loads((POS / "POINT.json").read_text())
    free[FREE.index("z6:re")] = .03
    free[FREE.index("zK:re")] = .03
    free[FREE.index("zEta:re")] = .3
    free[FREE.index("lambdaPhiphi1")] = -.002
    free[FREE.index("mphi2")] = float(positive["approximate_w"])+.002
    affine = affine_matrices(load_blocks(), .1, .1)
    metric = {label: kinetic_diag(label, .1, .1) for label in affine}
    result = {}
    for label, mats in affine.items():
        h = np.einsum("j,jab->ab", free, mats)
        h = h/np.sqrt(np.outer(metric[label], metric[label]))
        h = .5*(h+h.conj().T)
        result[label] = h
    return result


def fix_eigenvectors(values, vectors):
    order = np.argsort(values)
    values = np.asarray(values)[order]
    vectors = np.asarray(vectors, dtype=complex)[:, order].copy()
    for j in range(vectors.shape[1]):
        pivot = next(i for i, z in enumerate(vectors[:, j]) if abs(z) > 1e-12)
        vectors[:, j] *= np.exp(-1j*np.angle(vectors[pivot, j]))
        if vectors[pivot, j].real < 0:
            vectors[:, j] *= -1
    return values, vectors


def gram_schmidt(columns, expected, against=(), tolerance=1e-10):
    out = [np.asarray(v, dtype=float).copy() for v in against]
    fixed = len(out)
    for candidate in columns:
        v = np.asarray(candidate, dtype=float).copy()
        for old in out:
            v -= old*np.dot(old, v)
        norm = np.linalg.norm(v)
        if norm < tolerance:
            continue
        v /= norm
        pivot = next(i for i, z in enumerate(v) if abs(z) > tolerance)
        if v[pivot] < 0:
            v *= -1
        out.append(v)
        if len(out)-fixed == expected:
            break
    assert len(out)-fixed == expected, (len(out)-fixed, expected)
    return out[fixed:]


def phase_fixed_complex_columns(label, parent_basis):
    d = dimension(label)
    columns = []
    for sector, _, highest in representatives()[label]:
        for obj in generate_copy(highest, sector, d):
            u = tangent_coordinates(sector, obj, parent_basis)
            columns.append(np.asarray([complex(N(z, 30)) for z in u], dtype=complex))
    return np.column_stack(columns)


def block_complex_columns(label, parent_basis):
    """Canonical parent columns for the normalized block-representative basis.

    The saved affine Hessian blocks use rationalized highest-weight copies.
    Their kinetic normalization removes the benchmark field rescalings, but
    their copy phases need not equal the independently frozen all-weight
    convention.  This bridge makes that phase change explicit.
    """
    columns = []
    for sector, _, obj in rational_representatives()[label]:
        u = tangent_coordinates(sector, obj, parent_basis)
        u = np.asarray([complex(N(z, 30)) for z in u], dtype=complex)
        u /= np.linalg.norm(u)
        columns.append(u)
    B = np.column_stack(columns)
    assert np.max(abs(B.conj().T@B-np.eye(B.shape[1]))) < 2e-11
    return B


def preliminary_mass_basis(weight_U, metadata, blocks, parent_basis):
    by_label = defaultdict(list)
    for j, meta in enumerate(metadata):
        by_label[tuple(meta["label"])].append(j)
    physical_columns, masses, descriptors = [], [], []
    block_rotations = {}
    consumed = set()
    max_eigen_residual = 0.0
    for label in sorted(blocks):
        if label in consumed:
            continue
        bar = conjugate_label(label)
        h = blocks[label]
        d, m = dimension(label), h.shape[0]
        if bar != label:
            chosen = min(label, bar)
            if label != chosen:
                continue
            W = phase_fixed_complex_columns(chosen, parent_basis)
            W = W[:, ::d]
            B = block_complex_columns(chosen, parent_basis)
            C = W.conj().T@B
            assert np.max(abs(C.conj().T@C-np.eye(m))) < 2e-11
            h_weight = C@h@C.conj().T
            assert np.max(abs(h_weight-h_weight.conj().T)) < 2e-10
            values, vectors = fix_eigenvectors(*np.linalg.eigh(h_weight))
            max_eigen_residual = max(max_eigen_residual,
                float(np.max(abs(h_weight@vectors-vectors*values))))
            lookup = {}
            for j in by_label[chosen]:
                meta = metadata[j]
                lookup[(meta["copy"], meta["state"], meta["realification"])] = weight_U[:, j]
            assert len(lookup) == 2*m*d
            for mode in range(m):
                for state in range(d):
                    re_col = np.zeros(328)
                    im_col = np.zeros(328)
                    for copy in range(m):
                        z = vectors[copy, mode]
                        x = lookup[(copy, state, "re")]
                        y = lookup[(copy, state, "im")]
                        re_col += z.real*x-z.imag*y
                        im_col += z.imag*x+z.real*y
                    physical_columns.extend((re_col, im_col))
                    masses.extend((float(values[mode]), float(values[mode])))
                    descriptors.extend((
                        {"label": list(chosen), "mode": mode, "state": state,
                         "realification": "re"},
                        {"label": list(chosen), "mode": mode, "state": state,
                         "realification": "im"},
                    ))
            block_rotations[str(chosen)] = {
                "eigenvalues": [float(x) for x in values],
                "eigenvectors_columns": [[[float(z.real), float(z.imag)] for z in vectors[:, j]]
                                          for j in range(m)],
            }
            consumed.update((label, bar))
        else:
            indices = by_label[label]
            Uself = weight_U[:, indices]
            assert Uself.shape[1] == m*d
            if m == 1:
                value = float(h[0, 0].real)
                for ordinal in range(d):
                    physical_columns.append(Uself[:, ordinal])
                    masses.append(value)
                    descriptors.append({"label": list(label), "mode": 0,
                                        "self_conjugate_state": ordinal})
                block_rotations[str(label)] = {
                    "eigenvalues": [value], "eigenvectors_columns": [[[1.0, 0.0]]],
                }
            else:
                assert label == (0, 0, 0, 0) and d == 1
                B = block_complex_columns(label, parent_basis)
                C = Uself.T @ B
                assert np.max(abs(C.conj().T@C-np.eye(m))) < 2e-11
                hr = C@h@C.conj().T
                assert np.max(abs(hr.imag)) < 2e-10
                hr = .5*(hr.real+hr.real.T)
                values, vectors = fix_eigenvectors(*np.linalg.eigh(hr))
                vectors = vectors.real
                max_eigen_residual = max(max_eigen_residual,
                    float(np.max(abs(hr@vectors-vectors*values))))
                for mode in range(m):
                    physical_columns.append(Uself@vectors[:, mode])
                    masses.append(float(values[mode]))
                    descriptors.append({"label": list(label), "mode": mode,
                                        "self_conjugate_state": 0})
                block_rotations[str(label)] = {
                    "eigenvalues": [float(x) for x in values],
                    "real_eigenvectors_columns": vectors.tolist(),
                }
            consumed.add(label)
    U = np.column_stack(physical_columns)
    masses = np.asarray(masses)
    assert U.shape == (328, 328)
    assert np.max(abs(U.T@U-np.eye(328))) < ORTHO_TOL
    return U, masses, descriptors, block_rotations, max_eigen_residual


def state_coordinates(state, parent_basis):
    return np.asarray([numeric(real_kinetic_inner(e.state, state))
                       for e in parent_basis])


def explicit_symmetry_basis(parent_basis):
    b = sqrt(Rational(15, 8))/10
    s = sqrt(30)/10
    phi0 = Matrix.diag(*([-2]*6+[3]*4))
    sigma0 = vacuum_form()
    orbit_candidates = []
    for _, g in generators():
        dphi = g*phi0-phi0*g
        raw = form_action(g, sigma0)
        dsigma = {idx: (b*a, b*c) for idx, (a, c) in raw.items()}
        orbit_candidates.append(state_coordinates(
            State(dphi, dsigma, (0,)*10, 0), parent_basis))
    gauge = gram_schmidt(orbit_candidates, 33, tolerance=2e-11)

    pq_sigma = {}
    for idx, (a, c) in sigma0.items():
        pq_sigma[idx] = (-2*b*c, 2*b*a)
    pq = state_coordinates(State(zeros(10), pq_sigma, (0,)*10, -4*I*s),
                           parent_basis)
    pq = gram_schmidt([pq], 1, against=gauge, tolerance=2e-11)[0]
    return np.column_stack(gauge), pq


def state_from_coordinates(v, parent_basis):
    phi = zeros(10)
    sigma = {}
    vector = [0] * 10
    singlet = 0
    for coefficient, entry in zip(v, parent_basis):
        if abs(coefficient) < 1e-14:
            continue
        state = entry.state
        phi += coefficient*state.Phi
        for idx, (a, b) in state.Sigma.items():
            old = sigma.get(idx, (0, 0))
            sigma[idx] = (old[0]+coefficient*a, old[1]+coefficient*b)
        vector = [x+coefficient*y for x, y in zip(vector, state.phi)]
        singlet += coefficient*state.S
    return State(phi, sigma, tuple(vector), singlet)


def weight_generator_matrix(g, weight_U, metadata, parent_basis):
    """Generator action in the exact all-weight basis.

    Complex irrep pairs use their already-certified representation matrices.
    Only the 16 self-conjugate real columns are replayed through parent tensor
    coordinates, avoiding a costly dense 328-by-328 parent reprojection.
    """
    A = np.zeros((328, 328), dtype=float)
    by_label = defaultdict(list)
    for j, meta in enumerate(metadata):
        by_label[tuple(meta["label"])].append(j)
    for label, indices in by_label.items():
        if conjugate_label(label) != label:
            d = dimension(label)
            first_sector, _, highest = representatives()[label][0]
            states = generate_copy(highest, first_sector, d)
            M = np.asarray(representation_matrix(states, first_sector, g),
                           dtype=complex)
            lookup = {(metadata[j]["copy"], metadata[j]["state"],
                       metadata[j]["realification"]): j for j in indices}
            copies = max(metadata[j]["copy"] for j in indices)+1
            for copy in range(copies):
                for i in range(d):
                    xi, yi = lookup[(copy, i, "re")], lookup[(copy, i, "im")]
                    for j in range(d):
                        xj, yj = lookup[(copy, j, "re")], lookup[(copy, j, "im")]
                        a, b = M[i, j].real, M[i, j].imag
                        A[xi, xj] = a
                        A[yi, xj] = -b
                        A[xi, yj] = b
                        A[yi, yj] = a
        else:
            Uself = weight_U[:, indices]
            for local_j, global_j in enumerate(indices):
                state = state_from_coordinates(weight_U[:, global_j], parent_basis)
                transformed = State(
                    g*state.Phi-state.Phi*g,
                    form_action(g, state.Sigma),
                    tuple(g*Matrix(state.phi)), 0)
                coordinates = state_coordinates(transformed, parent_basis)
                A[np.ix_(indices, [global_j])] = (
                    Uself.T@coordinates).reshape(-1, 1)
    assert np.max(abs(A+A.T)) < 3e-9
    return A


def scalar_index_replay(U, weight_U, metadata, parent_basis):
    j0 = phase_complex_structure(((0, 1),))
    j1 = phase_complex_structure(((2, 3),))
    j2 = phase_complex_structure(((4, 5),))
    j3 = phase_complex_structure(((6, 7),))
    j4 = phase_complex_structure(((8, 9),))
    gens = {
        "color_cartan": j0-j1,
        "weak_cartan": j3-j4,
        "hypercharge_y6": 2*(j0+j1+j2)-3*(j3+j4),
    }
    transformed = {}
    R = weight_U.T@U
    assert np.max(abs(R.T@R-np.eye(328))) < 5e-9
    for name, g in gens.items():
        Aweight = weight_generator_matrix(g, weight_U, metadata, parent_basis)
        Ap = R.T@Aweight@R
        assert np.max(abs(Ap+Ap.T)) < 5e-10
        transformed[name] = Ap
    heavy = slice(0, 290)
    traces = {name: -float(np.trace(A[heavy, heavy]@A[heavy, heavy]))
              for name, A in transformed.items()}
    beta = np.asarray([
        traces["hypercharge_y6"]/360,
        traces["weak_cartan"]/24,
        traces["color_cartan"]/24,
    ])
    expected = np.asarray([377/30, 77/6, 79/6])
    assert np.max(abs(beta-expected)) < 2e-8, (beta, expected)
    return traces, beta


def stable_hash(U):
    serial = [[format(float(z), ".17g") for z in U[:, j]] for j in range(328)]
    packed = json.dumps(serial, separators=(",", ":"))
    return sha256(packed.encode("utf-8")).hexdigest()


def sparse_vector(v, tolerance=2e-14):
    return [[i, format(float(z), ".17g")] for i, z in enumerate(v)
            if abs(z) > tolerance]


def main():
    weight_data, weight_U, metadata = load_weight_map()
    parent_basis = canonical_real_basis()
    blocks = frozen_blocks()
    Upre, masses, descriptors, rotations, eigen_residual = preliminary_mass_basis(
        weight_U, metadata, blocks, parent_basis)

    zero_indices = np.where(abs(masses) < ZERO_TOL)[0]
    heavy_indices = np.where(masses > ZERO_TOL)[0]
    assert len(zero_indices) == 38, (len(zero_indices), masses[zero_indices])
    assert len(heavy_indices) == 290 and np.all(masses[heavy_indices] > 0)
    Zpre = Upre[:, zero_indices]
    Hcols = Upre[:, heavy_indices]
    gauge, pq = explicit_symmetry_basis(parent_basis)
    symmetry = np.column_stack((gauge, pq))
    assert symmetry.shape == (328, 34)
    assert np.max(abs(symmetry.T@symmetry-np.eye(34))) < 2e-10
    symmetry_outside_zero = np.max(abs(symmetry-Zpre@(Zpre.T@symmetry)))
    assert symmetry_outside_zero < 3e-9, symmetry_outside_zero
    higgs = gram_schmidt([Zpre[:, j] for j in range(38)], 4,
                         against=[symmetry[:, j] for j in range(34)],
                         tolerance=2e-9)
    higgs = np.column_stack(higgs)
    zeros_physical = np.column_stack((gauge, pq, higgs))
    assert zeros_physical.shape == (328, 38)
    U = np.column_stack((Hcols, zeros_physical))
    final_masses = np.r_[masses[heavy_indices], np.zeros(38)]
    orthogonality = float(np.max(abs(U.T@U-np.eye(328))))
    assert orthogonality < 4e-9, orthogonality
    assert np.linalg.matrix_rank(U, tol=1e-9) == 328

    Hpre = (Upre*masses)@Upre.T
    Hfinal = (U*final_masses)@U.T
    hessian_roundtrip = float(np.max(abs(Hpre-Hfinal)))
    assert hessian_roundtrip < 2e-8, hessian_roundtrip
    inverse_residual = float(np.max(abs(U.T@U-np.eye(328))))
    traces, beta = scalar_index_replay(U, weight_U, metadata, parent_basis)

    basis_hash = stable_hash(U)
    special_zero_columns = {
        "gauge_33": [sparse_vector(gauge[:, j]) for j in range(33)],
        "pq_1": sparse_vector(pq),
        "higgs_4": [sparse_vector(higgs[:, j]) for j in range(4)],
    }
    heavy_spectrum = [float(x) for x in masses[heavy_indices]]
    factorized_authority = {
        "sm_weight_map_sha256": weight_data["real_weight_map_sha256"],
        "multiplicity_rotations": rotations,
        "special_zero_columns": special_zero_columns,
        "heavy_mass_spectrum_real_directions": heavy_spectrum,
    }
    factorized_hash = sha256(json.dumps(
        factorized_authority, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    payload = {
        "outcome": "CANONICAL_328_PHYSICAL_BASIS_PASS",
        "parent_component_basis_sha256": (
            "c66398b6321988b643af5c12fdbea86c3a2589b7b139450770c6ef72c31a3b5e"),
        "sm_weight_map_sha256": weight_data["real_weight_map_sha256"],
        "physical_basis_sha256_float17_column_major": basis_hash,
        "factorized_physical_basis_sha256": factorized_hash,
        "hash_authority": (
            "factorized_physical_basis_sha256 is reproducible authority; "
            "dense float17 hash is a same-run diagnostic"
        ),
        "factorization": "U_parent_to_weights * U_multiplicity * U_zero_light",
        "disposition": {
            "positive_heavy_real": 290,
            "gauge_goldstone_real": 33,
            "pq_real": 1,
            "light_higgs_real": 4,
            "total": 328,
        },
        "certificates": {
            "max_kinetic_orthogonality_residual": orthogonality,
            "rank_tolerance_1e_9": 328,
            "max_block_eigen_residual": eigen_residual,
            "max_hessian_roundtrip_residual": hessian_roundtrip,
            "max_certified_inverse_residual": inverse_residual,
            "max_symmetry_vector_outside_preliminary_nullspace": float(
                symmetry_outside_zero),
            "minimum_heavy_mass_squared": float(np.min(masses[heavy_indices])),
            "maximum_absolute_zero_mass_squared_before_replacement": float(
                np.max(abs(masses[zero_indices]))),
        },
        "heavy_scalar_one_loop_beta_indices_order_1_2_3": beta.tolist(),
        "heavy_generator_squared_traces": traces,
        "known_index_target_order_1_2_3": [377/30, 77/6, 79/6],
        "multiplicity_rotations": rotations,
        "special_zero_columns": special_zero_columns,
        "heavy_mass_spectrum_real_directions": heavy_spectrum,
        "not_started": [
            "background_field_gauge_fixing",
            "bulk_physical_vertex_generation",
            "two_loop_diagram_generation",
            "counterterms",
            "integral_reduction_and_master_evaluation",
        ],
    }
    (HERE / "physical_basis.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("DISPOSITION", payload["disposition"])
    print("PHYSICAL_BASIS_SHA256", basis_hash)
    print("MAX_ORTHO_RESIDUAL", orthogonality)
    print("MAX_HESSIAN_ROUNDTRIP_RESIDUAL", hessian_roundtrip)
    print("HEAVY_SCALAR_BETA_INDEX_REPLAY", beta.tolist())


if __name__ == "__main__":
    main()
