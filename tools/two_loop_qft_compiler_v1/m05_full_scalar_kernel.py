"""Complete exact 26-direction scalar V4*V4 kernel for M05.

This combines every previously validated quartic Hessian backend and computes
all cross-couplings in the frozen 328-real parent basis.  The resulting
scalar pole is projected onto all 26 real Hermitian quartic directions and
checked on two independent backgrounds.  Gauge/Goldstone/ghost completion
and the inventory-independent replay remain separate requirements, so this
artifact alone cannot pass UVP_M05.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Matrix, simplify, zeros

from compile_real_field_basis import canonical_real_basis
from m05_parent_scalar_kernel import (
    ACTIVE_QUARTICS, _active_polynomial_terms, projector_backgrounds,
)
from m05_rank26_projector import (
    REAL_DIRECTION_NAMES, physical_quartics, sigma_backgrounds,
)
from m05_sigma_radial_kernel import (
    NAMES as RADIAL_NAMES, _dot, _full_coordinates, _hessians,
)
from m05_sigma_bilinear_kernel import (
    BILINEAR_NAMES, _hessian, build_polynomials,
)
from m05_phi_sigma_mixed_kernel import (
    _mixed_hessian, build_phi_sigma_terms,
)
from m05_pure_sigma_kernel import (
    _build_second_derivatives, _sigma_hessians,
)
from m05_zeta_kernel import (
    _extra_backgrounds, _physical_hessians, _raw_hessian, build_zeta_terms,
)


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def _embed_sigma(hessian):
    return {(i + 54, j + 54): value for (i, j), value in hessian.items()}


def _complete_hessians(background, point, basis, active_terms,
                       bilinear_polynomials, mixed_terms,
                       sigma_basis, sigma_forms, second1, second1_dual, second2,
                       zeta_terms):
    by_name = dict(zip(
        RADIAL_NAMES, _hessians(background, basis, active_terms)
    ))
    by_name.update({
        name: _hessian(poly, point)
        for name, poly in zip(BILINEAR_NAMES, bilinear_polynomials)
    })
    by_name["lambdaPhiSigma2"] = _mixed_hessian(mixed_terms, point)

    if background.Sigma:
        pure = _sigma_hessians(
            background.Sigma, sigma_basis, sigma_forms,
            second1, second1_dual, second2,
        )
        by_name.update({
            "lambdaSigma2": _embed_sigma(pure[1]),
            "lambdaSigma3": _embed_sigma(pure[2]),
            "lambdaSigma4": _embed_sigma(pure[3]),
        })
        zeta_re, zeta_im = _physical_hessians(
            _raw_hessian(zeta_terms, point)
        )
    else:
        by_name.update({
            "lambdaSigma2": {}, "lambdaSigma3": {}, "lambdaSigma4": {},
        })
        zeta_re, zeta_im = {}, {}
    by_name["zEta_re"] = zeta_re
    by_name["zEta_im"] = zeta_im

    assert set(by_name) == set(REAL_DIRECTION_NAMES), (
        sorted(set(REAL_DIRECTION_NAMES) - set(by_name)),
        sorted(set(by_name) - set(REAL_DIRECTION_NAMES)),
    )
    return tuple(by_name[name] for name in REAL_DIRECTION_NAMES)


def compute_kernel():
    basis = canonical_real_basis()
    active_basis = [entry for entry in basis if entry.sector != "Sigma"]
    _, active_terms = _active_polynomial_terms(active_basis)
    bilinear_polynomials = build_polynomials(basis)
    mixed_terms = build_phi_sigma_terms(basis)
    zeta_terms = build_zeta_terms(basis)
    sigma_basis = [entry for entry in basis if entry.sector == "Sigma"]
    sigma_forms = [entry.state.Sigma for entry in sigma_basis]

    print("FULL_SCALAR_SIGMA_CACHE_START", flush=True)
    second1, second1_dual, second2 = _build_second_derivatives(sigma_forms)
    print("FULL_SCALAR_SIGMA_CACHE_DONE", len(second1), flush=True)

    backgrounds = list(projector_backgrounds()) + [
        state for _, state in sigma_backgrounds()
    ]
    assert len(backgrounds) == 26
    projector = Matrix([[24 * value for value in physical_quartics(state)]
                        for state in backgrounds])
    assert projector.rank() == 26

    all_backgrounds = backgrounds + _extra_backgrounds()
    diagonal = []
    inventories = []
    for ordinal, background in enumerate(all_backgrounds, 1):
        print("FULL_SCALAR_BACKGROUND", ordinal, "OF", len(all_backgrounds),
              flush=True)
        point = _full_coordinates(background, basis)
        hessians = _complete_hessians(
            background, point, basis, active_terms,
            bilinear_polynomials, mixed_terms,
            sigma_basis, sigma_forms, second1, second1_dual, second2,
            zeta_terms,
        )
        matrix = zeros(26)
        for a in range(26):
            for b in range(a, 26):
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
        matrix = zeros(26)
        for witness, value in enumerate(diagonal[:26]):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal[:26]):
        replay = zeros(26)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    for offset, background in enumerate(all_backgrounds[26:], 26):
        row = [24 * value for value in physical_quartics(background)]
        replay = zeros(26)
        for output, matrix in enumerate(projected):
            replay += row[output] * matrix
        assert replay.applyfunc(simplify) == diagonal[offset]

    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(REAL_DIRECTION_NAMES, projected)
    }
    inventory = {
        "parent_internal_real_directions": 328,
        "input_quartic_directions": list(REAL_DIRECTION_NAMES),
        "output_quartic_directions": list(REAL_DIRECTION_NAMES),
        "projector_backgrounds": 26,
        "independent_backgrounds": 2,
        "projector_rank": 26,
        "mixed_PhiSigma_factorized_terms": len(mixed_terms),
        "zEta_factorized_terms": len(zeta_terms),
        "Sigma_pair_second_derivatives_per_k": len(second1),
        "background_inventories": inventories,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_COMPLETE_SCALAR_V4V4_PASS",
        "authority": "IMPLEMENTATION_COMPONENT_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 26,
        "projection_residual": "0",
        "independent_background_residual": "0",
        "external_permutation_symmetry": "INHERITED_FROM_HESSIAN_TRACE_AND_EXACT_POLARIZATION",
        "Hermitian_real_direction_basis": True,
        "missing_for_M05": [
            "partial-BFM vector/Goldstone/ghost quartic completion",
            "M02 field conversion in the completed gauge ledger",
            "exact xi cancellation",
            "complete inventory-independent full-operator replay",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_kernel()
    (HERE / "uvp_m05_complete_scalar_v4v4.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("PROJECTOR_RANK", result["projection_rank"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
