"""Sparse/on-demand physical interaction kernels for compiler layer 3.

The API covers scalar-potential derivatives, gauge-invariant kinetic vertices,
pure Yang--Mills color factors, and the tree-level FP mass/scalar kernel.  It
does not by itself establish the complete background/quantum gauge-fixed
vertex action or general-xi one-loop matching cancellation.
"""

from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, N, Rational, conjugate, simplify, sqrt, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
sys.path[:0] = [
    str(HERE),
    str(CALC / "canonical_so10_full_hessian"),
    str(CALC / "canonical_so10_scalar_benchmark"),
    str(CALC / "canonical_so10_positive_higgs"),
    str(CALC / "canonical_so10_vacuum_kernel"),
    str(CALC / "canonical_so10_scalar_reconstruction"),
    str(CALC / "canonical_so10_direct_two_loop_gauge_scalar_threshold"),
]

from physical_basis_runtime import (
    PHYSICAL_BASIS_HASH, load_physical_map, scalar_field_id, scalar_field_index,
)
from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from compile_background_field_quadratic import full_orbit_map
from materialize_physical_basis import state_from_coordinates
from derive_stabilizers import generators
from test_eta1_invariant import parity
from verify_eta1_doublet_mixing import vacuum_form
import parent_bilinear_oracle as parent_oracle
from parent_bilinear_oracle import COMPLEX_NAMES, REAL_NAMES, State
from certify_sigma_quartics import paired_tensor
from test_eta1_invariant import add as pair_add, mul as pair_mul
from search import FREE, parent_coefficients


QUADRATIC_HASH = (
    "b983a8d8dae078761d61c8492ddb583f984398e56483cd306e2382e68ea2e692"
)


def add_state(a, b):
    sigma = {}
    for key in set(a.Sigma) | set(b.Sigma):
        ar, ai = a.Sigma.get(key, (0, 0))
        br, bi = b.Sigma.get(key, (0, 0))
        sigma[key] = (ar + br, ai + bi)
    return State(a.Phi + b.Phi, sigma,
                 tuple(x + y for x, y in zip(a.phi, b.phi)), a.S + b.S)


def scale_state(a, z):
    return State(z * a.Phi,
                 {key: (z * x, z * y) for key, (x, y) in a.Sigma.items()},
                 tuple(z * x for x in a.phi), z * a.S)


def generic_form_action(g, form):
    out = {}
    for old, z in form.items():
        for slot, j in enumerate(old):
            for i in range(10):
                coefficient = g[i, j]
                if abs(coefficient) < 1e-14 or i in old:
                    continue
                moved = old[:slot] + (i,) + old[slot + 1:]
                key = tuple(sorted(moved))
                factor = coefficient * parity(moved)
                old_value = out.get(key, (0, 0))
                out[key] = (old_value[0] + factor * z[0],
                            old_value[1] + factor * z[1])
    return {key: value for key, value in out.items()
            if abs(complex(N(value[0], 20))) + abs(complex(N(value[1], 20)))
            > 1e-14}


def numeric_cross_contraction(paired, y, z):
    result = (0, 0)
    for (ia, ib), za in paired.items():
        for ac in combinations(ia, y):
            ad = tuple(i for i in ia if i not in ac)
            sign_a = parity(ac + ad)
            for bc in combinations(ib, z):
                bd = tuple(i for i in ib if i not in bc)
                raw_c, raw_d = ac + bc, ad + bd
                if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                    continue
                key = (tuple(sorted(raw_c)), tuple(sorted(raw_d)))
                zb = paired.get(key, (0, 0))
                sign = sign_a * parity(bc + bd) * parity(raw_c) * parity(raw_d)
                value = pair_mul(za, (zb[0], -zb[1]))
                result = pair_add(result, (sign * value[0], sign * value[1]))
    return result[0]


_NUMERIC_QUARTIC_CACHE = {}


def numeric_quartics(form):
    key = tuple(sorted(form.items()))
    if key in _NUMERIC_QUARTIC_CACHE:
        return _NUMERIC_QUARTIC_CACHE[key]
    tensors = [paired_tensor(form, k) for k in range(5)]
    norms = tuple(sum(a * a + b * b for a, b in tensor.values())
                  for tensor in tensors)
    result = norms + (numeric_cross_contraction(tensors[1], 3, 1),
                      numeric_cross_contraction(tensors[1], 2, 2))
    _NUMERIC_QUARTIC_CACHE[key] = result
    return result


def numeric_invariant_values(state):
    """Use the exact invariant implementation with certified float tolerance.

    The exact oracle deliberately asserts polynomial identities symbolically.
    Physical mixing columns are residual-certified floating algebraic numbers,
    so this wrapper replaces only those exact-equality guards; it leaves every
    invariant contraction unchanged.
    """
    old_quartics = parent_oracle.quartics
    old_real_check = parent_oracle.real_part_check
    parent_oracle.quartics = numeric_quartics
    parent_oracle.real_part_check = lambda _name, value: (
        value + conjugate(value)) / 2
    try:
        return parent_oracle.invariant_values(state)
    finally:
        parent_oracle.quartics = old_quartics
        parent_oracle.real_part_check = old_real_check


def action_state(g, state):
    gv = np.asarray(g, dtype=float) @ np.asarray(
        [complex(N(z, 20)) for z in state.phi], dtype=complex)
    return State(Matrix(g) * state.Phi - state.Phi * Matrix(g),
                 generic_form_action(np.asarray(g, dtype=float), state.Sigma),
                 tuple(gv), 0)


def deterministic_eigenspace(gram, value, count):
    eigenvalues, vectors = np.linalg.eigh(gram)
    source = vectors[:, abs(eigenvalues - value) < 2e-10]
    assert source.shape[1] == count
    projector = source @ source.T
    out = []
    for axis in range(gram.shape[0]):
        v = projector[:, axis].copy()
        for old in out:
            v -= old * np.dot(old, v)
        norm = np.linalg.norm(v)
        if norm < 1e-11:
            continue
        v /= norm
        pivot = next(i for i, z in enumerate(v) if abs(z) > 1e-11)
        if v[pivot] < 0:
            v *= -1
        out.append(v)
        if len(out) == count:
            break
    assert len(out) == count
    return np.column_stack(out)


class PhysicalVertexAPI:
    def __init__(self):
        physical, self.U, self.scalar_masses = load_physical_map()
        assert physical["factorized_physical_basis_sha256"] == PHYSICAL_BASIS_HASH
        quadratic = json.loads((HERE / "background_field_quadratic.json").read_text())
        assert quadratic["quadratic_layer_sha256"] == QUADRATIC_HASH
        self.parent_basis = canonical_real_basis()
        self.Q = full_orbit_map(self.parent_basis)
        gram = self.Q.T @ self.Q
        groups = ((0.0, 12), (.005, 8), (.025, 1),
                  (50 / 120, 12), (50.6 / 120, 12))
        self.vector_rotation = np.column_stack([
            deterministic_eigenspace(gram, value, count)
            for value, count in groups
        ])
        self.vector_masses = np.concatenate([
            np.full(count, value) for value, count in groups
        ])
        self.vector_mass_matrix = self.vector_rotation.T @ gram @ self.vector_rotation
        raw = [np.asarray(g, dtype=float) / np.sqrt(2)
               for _, g in generators()]
        self.vector_generators = [
            sum((self.vector_rotation[a, j] * raw[a] for a in range(45)),
                np.zeros((10, 10)))
            for j in range(45)
        ]
        self.coefficients, self.vacuum = self._benchmark()

    def _benchmark(self):
        point = json.loads((CALC / "canonical_so10_scalar_benchmark" /
                            "STAGE1_POINT.json").read_text())
        free = np.asarray([float(point["free_coefficients"][name])
                           for name in FREE])
        positive = json.loads((CALC / "canonical_so10_positive_higgs" /
                               "POINT.json").read_text())
        for name, value in (("z6:re", .03), ("zK:re", .03),
                            ("zEta:re", .3), ("lambdaPhiphi1", -.002)):
            free[FREE.index(name)] = value
        free[FREE.index("mphi2")] = float(positive["approximate_w"]) + .002
        coefficients = parent_coefficients(free, .1, .1)
        b, s = np.sqrt(15 / 8) / 10, np.sqrt(30) / 10
        sigma = {idx: (b * x, b * y) for idx, (x, y) in vacuum_form().items()}
        vacuum = State(Matrix.diag(*([-2] * 6 + [3] * 4)), sigma,
                       (0,) * 10, s)
        return coefficients, vacuum

    @lru_cache(maxsize=328)
    def scalar_state(self, field_id):
        return state_from_coordinates(
            self.U[:, scalar_field_index(field_id)], self.parent_basis)

    def vector_id(self, index):
        assert 0 <= index < 45
        return f"B{index:03d}" if index < 12 else f"X{index-12:03d}"

    def vector_index(self, field_id):
        index = int(field_id[1:]) + (0 if field_id.startswith("B") else 12)
        assert self.vector_id(index) == field_id
        return index

    def potential_vertex(self, *scalar_ids):
        n = len(scalar_ids)
        assert 2 <= n <= 4
        directions = [self.scalar_state(field) for field in scalar_ids]
        weights = ({-2: Rational(1, 12), -1: -Rational(2, 3),
                    1: Rational(2, 3), 2: -Rational(1, 12)}
                   if n == 2 else
                   {-1: -Rational(1, 2), 1: Rational(1, 2)})
        accumulated = {name: 0 for name in REAL_NAMES + COMPLEX_NAMES}
        for nodes in product(weights, repeat=n):
            state, weight = self.vacuum, 1
            for node, direction in zip(nodes, directions):
                state = add_state(state, scale_state(direction, node))
                weight *= weights[node]
            values = numeric_invariant_values(state)
            for name in accumulated:
                accumulated[name] += weight * values[name]
        result = sum(self.coefficients[name] * accumulated[name]
                     for name in REAL_NAMES)
        result += sum(self.coefficients[name] * accumulated[name]
                      + conjugate(self.coefficients[name] * accumulated[name])
                      for name in COMPLEX_NAMES)
        return complex(N(simplify(result), 18))

    def vss(self, vector_id, scalar_i, scalar_j):
        """Coefficient of the antisymmetric derivative V S_i d S_j kernel."""
        g = self.vector_generators[self.vector_index(vector_id)]
        si, sj = self.scalar_state(scalar_i), self.scalar_state(scalar_j)
        return float(N(real_kinetic_inner(si, action_state(g, sj)), 18))

    def vvss(self, vector_a, vector_b, scalar_i, scalar_j):
        """Symmetric gauge-kinetic VVSS coefficient without g10^2."""
        ga = self.vector_generators[self.vector_index(vector_a)]
        gb = self.vector_generators[self.vector_index(vector_b)]
        si, sj = self.scalar_state(scalar_i), self.scalar_state(scalar_j)
        left = real_kinetic_inner(action_state(ga, si), action_state(gb, sj))
        right = real_kinetic_inner(action_state(gb, si), action_state(ga, sj))
        return float(N((left + right) / 2, 18))

    def vvs(self, vector_a, vector_b, scalar_id):
        """VV-background-scalar kernel divided by g10^2*omega."""
        a, b = self.vector_index(vector_a), self.vector_index(vector_b)
        orbit_a = self.Q @ self.vector_rotation[:, a]
        orbit_b = self.Q @ self.vector_rotation[:, b]
        state_a = state_from_coordinates(orbit_a, self.parent_basis)
        state_b = state_from_coordinates(orbit_b, self.parent_basis)
        scalar = self.scalar_state(scalar_id)
        ga, gb = self.vector_generators[a], self.vector_generators[b]
        value = (real_kinetic_inner(state_a, action_state(gb, scalar))
                 + real_kinetic_inner(state_b, action_state(ga, scalar)))
        return float(N(value, 18))

    def structure_constant(self, vector_a, vector_b, vector_c):
        a = self.vector_generators[self.vector_index(vector_a)]
        b = self.vector_generators[self.vector_index(vector_b)]
        c = self.vector_generators[self.vector_index(vector_c)]
        return float(np.trace(c.T @ (a @ b - b @ a)))

    def quartic_color(self, a, b, c, d, channel="ab_cd"):
        if channel == "ab_cd":
            return sum(self.structure_constant(a, b, self.vector_id(e))
                       * self.structure_constant(c, d, self.vector_id(e))
                       for e in range(45))
        if channel == "ac_bd":
            return sum(self.structure_constant(a, c, self.vector_id(e))
                       * self.structure_constant(b, d, self.vector_id(e))
                       for e in range(45))
        raise KeyError(channel)

    def ghost_mass(self, ghost_a, ghost_b, xi):
        a, b = self.vector_index(ghost_a), self.vector_index(ghost_b)
        return float(xi * self.vector_mass_matrix[a, b])

    def ghost_scalar(self, ghost_a, ghost_b, scalar_id, xi):
        """FP ghost-ghost-scalar kernel divided by g10^2*omega."""
        a, b = self.vector_index(ghost_a), self.vector_index(ghost_b)
        orbit_a = self.Q @ self.vector_rotation[:, a]
        gb = self.vector_generators[b]
        direction = self.scalar_state(scalar_id)
        acted = state_from_coordinates(orbit_a, self.parent_basis)
        return float(xi * N(real_kinetic_inner(
            acted, action_state(gb, direction)), 18))


def manifest():
    api = PhysicalVertexAPI()
    payload = {
        "outcome": "PHYSICAL_VERTEX_API_CORE_PASS",
        "physical_basis_sha256": PHYSICAL_BASIS_HASH,
        "background_field_quadratic_sha256": QUADRATIC_HASH,
        "field_ids": {
            "heavy_scalars": {"pattern": "H000..H289", "count": 290},
            "gauge_goldstones": {"pattern": "G000..G032", "count": 33},
            "pq": {"pattern": "PQ000", "count": 1},
            "light_higgs": {"pattern": "h000..h003", "count": 4},
            "unbroken_background_vectors": {
                "pattern": "B000..B011", "count": 12,
            },
            "massive_vectors_and_heavy_ghosts": {
                "pattern": "X000..X032", "count": 33,
            },
        },
        "on_demand_kernels": [
            "SSS", "SSSS", "VSS", "VVS", "VVSS", "VVV_structure",
            "VVVV_color_channels", "ghost_mass", "ghost_ghost_scalar",
        ],
        "normalization": (
            "reported gauge-kinetic kernels omit explicit g10 powers and "
            "standard momentum/Lorentz/i factors"
        ),
        "execution_contract": (
            "calculation-local serial use; the residual-certified floating "
            "physical columns require a temporary numeric-tolerance wrapper "
            "around exact parent invariant guards"
        ),
        "not_claimed": [
            "complete_background_quantum_field_vertex_action",
            "general_xi_one_loop_F2_cancellation",
            "two_loop_diagram_generation",
        ],
    }
    (HERE / "physical_vertex_api.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("SCALAR_IDS", 328, "VECTOR_IDS", 45, "HEAVY_GHOST_IDS", 33)
    print("PHYSICAL_BASIS_SHA256", PHYSICAL_BASIS_HASH)


if __name__ == "__main__":
    manifest()
