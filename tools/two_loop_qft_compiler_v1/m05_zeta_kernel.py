"""Exact scalar-loop regression for the complex zEta quartic.

The canonical invariant is

    zEta * Sigma_ijlmn Sigma_ijpqr Sigma*_lmpqr phi_n + h.c.

in the normalization implemented by ``contraction_vector_on_a``.  This
module constructs the complete factorized contraction from canonical real
coordinate linear forms and evaluates its background-local Hessian.  The
zEta-only scalar pole is projected onto the full frozen 26-direction quartic
basis.  It is an implementation regression, not an UVP_M05 pass.
"""

from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path

from sympy import I, Matrix, conjugate, simplify, zeros

from compile_real_field_basis import canonical_real_basis
from m05_parent_scalar_kernel import projector_backgrounds
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from m05_sigma_bilinear_kernel import _linear_maps, _ordered_sigma
from m05_sigma_radial_kernel import _dot, _full_coordinates
from parent_bilinear_oracle import State, invariant_values
from certify_sigma_quartics import generated_form


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def build_zeta_terms(basis):
    sigma, phi, _, _ = _linear_maps(basis)
    terms = []
    ten = tuple(range(10))
    triples = tuple(combinations(ten, 3))
    for n in ten:
        x = phi[n]
        if not x:
            continue
        for shared_ab in combinations(ten, 2):
            if n in shared_ab:
                continue
            remaining = tuple(i for i in ten if i not in shared_ab)
            left_a = []
            for shared_ac in combinations(remaining, 2):
                a = _ordered_sigma(shared_ab + shared_ac + (n,), sigma)
                if a:
                    left_a.append((shared_ac, a))
            right_b = []
            for shared_bc in triples:
                b = _ordered_sigma(shared_ab + shared_bc, sigma)
                if b:
                    right_b.append((shared_bc, b))
            for shared_ac, a in left_a:
                for shared_bc, b in right_b:
                    c = _ordered_sigma(shared_ac + shared_bc, sigma)
                    if not c:
                        continue
                    cbar = {key: conjugate(value) for key, value in c.items()}
                    terms.append((x, a, b, cbar))
    assert terms
    return terms


def _linear_value(linear, point):
    return sum(coefficient * point[key[0]]
               for key, coefficient in linear.items())


def _raw_value(terms, point):
    result = 0
    for factors in terms:
        value = 1
        for factor in factors:
            value *= _linear_value(factor, point)
            if value == 0:
                break
        result += value
    return simplify(result)


def _raw_hessian(terms, point):
    result = {}

    def add_outer(left, right, factor):
        if factor == 0:
            return
        for ir, cr in left.items():
            for js, cs in right.items():
                key = (ir[0], js[0])
                reverse = (js[0], ir[0])
                value = factor * cr * cs
                result[key] = result.get(key, 0) + value
                result[reverse] = result.get(reverse, 0) + value

    for x, a, b, cbar in terms:
        vx = _linear_value(x, point)
        va = _linear_value(a, point)
        vb = _linear_value(b, point)
        vc = _linear_value(cbar, point)
        add_outer(x, a, vb * vc)
        add_outer(x, b, va * vc)
        add_outer(x, cbar, va * vb)
        add_outer(a, b, vx * vc)
        add_outer(a, cbar, vx * vb)
        add_outer(b, cbar, vx * va)
    return {key: simplify(value) for key, value in result.items()
            if value != 0}


def _physical_hessians(raw):
    real, imag = {}, {}
    for key, value in raw.items():
        re_value = simplify(value + conjugate(value))
        im_value = simplify(I * value + conjugate(I * value))
        if re_value != 0:
            real[key] = re_value
        if im_value != 0:
            imag[key] = im_value
    return real, imag


def _extra_backgrounds():
    out = []
    for seed in (19, 20):
        form = generated_form(seed, 7 + seed % 5)
        vector = tuple(
            (seed % 3 + 1) + I * ((2 * seed + i) % 3 - 1)
            if i in (seed % 10, (seed + 3) % 10, (seed + 7) % 10)
            else 0
            for i in range(10)
        )
        out.append(State(zeros(10), form, vector, 0))
    return out


def compute_kernel():
    basis = canonical_real_basis()
    terms = build_zeta_terms(basis)
    backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]
    assert len(backgrounds) == 26
    projector = Matrix([[24 * value for value in physical_quartics(state)]
                        for state in backgrounds])
    assert projector.rank() == 26

    zeta_index = REAL_DIRECTION_NAMES.index("zEta_re")
    # Replay the raw complex invariant directly before taking real/imaginary
    # physical combinations.
    for background in backgrounds[11:14]:
        point = _full_coordinates(background, basis)
        assert _raw_value(terms, point) == invariant_values(background)["zEta"]

    diagonal = []
    inventories = []
    all_backgrounds = backgrounds + _extra_backgrounds()
    for ordinal, background in enumerate(all_backgrounds, 1):
        point = _full_coordinates(background, basis)
        if all(point[index] == 0 for index in range(54, 306)):
            hessians = ({}, {})
        else:
            print("ZETA_BACKGROUND", ordinal, "OF", len(all_backgrounds),
                  flush=True)
            hessians = _physical_hessians(_raw_hessian(terms, point))
        matrix = zeros(2)
        for a in range(2):
            for b in range(a, 2):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "background": ordinal - 1,
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv()
    projected = []
    for output in range(26):
        matrix = zeros(2)
        for witness, value in enumerate(diagonal[:26]):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal[:26]):
        replay = zeros(2)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    extra_residual = "0"
    for offset, background in enumerate(all_backgrounds[26:], 26):
        row = [24 * value for value in physical_quartics(background)]
        replay = zeros(2)
        for output, matrix in enumerate(projected):
            replay += row[output] * matrix
        assert replay.applyfunc(simplify) == diagonal[offset]

    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(REAL_DIRECTION_NAMES, projected)
        if matrix != zeros(2)
    }
    inventory = {
        "parent_internal_real_directions": 328,
        "factorized_zEta_terms": len(terms),
        "input_directions": ["zEta_re", "zEta_im"],
        "output_directions_nonzero": list(tables),
        "full_projector_rank": 26,
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_ZETA_SCALAR_SUBTHEORY_PASS",
        "authority": "IMPLEMENTATION_REGRESSION_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 26,
        "projection_residual": "0",
        "independent_backgrounds": 2,
        "independent_background_residual": extra_residual,
        "direct_parent_oracle_regression_backgrounds": 3,
        "direct_parent_oracle_residual": "0",
        "zEta_direction_indices": [zeta_index, zeta_index + 1],
        "missing_for_M05": [
            "combined 26-direction scalar assembly and cross-couplings",
            "partial-BFM gauge completion",
            "complete independent replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_kernel()
    (HERE / "uvp_m05_zeta_subtheory.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("FACTORIZED_TERMS", result["inventory"]["factorized_zEta_terms"])
    print("NONZERO_OUTPUTS", result["inventory"]["output_directions_nonzero"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
