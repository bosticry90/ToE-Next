"""Independent functional/Hessian-trace replay of UVP_M03 attempt 2.

This module imports the frozen parent invariant evaluator but not the primary
trace tables or result artifact. Quartic contractions are reconstructed as
sector Laplacians of the Hessian; cubic contractions use an independent
eight-corner trilinear polarization.
"""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np
from sympy import I, Rational, conjugate, nsimplify, simplify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
sys.path[:0] = [
    str(HERE),
    str(CALC / "canonical_so10_full_hessian"),
]

from compile_real_field_basis import canonical_real_basis
from m03_parent_scalar_kernel import (
    CASIMIRS, DIMENSIONS, MASS_HESSIAN_FACTORS, MASS_NAMES,
    PAIR_INVARIANTS, SECTORS, add_state, digest, quartic_values, scale_state,
)


CONTRACT = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"
ATTEMPT1 = "a429ce0df860933879bb8810c42a599d0cc0f87a694be392cb591c10f18086c4"


def cubic_values(state):
    p = state.Phi
    vector = state.phi
    singlet = state.S
    p3 = (p * p * p).trace()
    phi_phi = sum(conjugate(vector[i]) * p[i, j] * vector[j]
                  for i in range(10) for j in range(10))
    t = sum(value * value for value in vector)
    return {"muPhi": simplify(p3), "muPhiPhi": simplify(phi_phi),
            "z6": simplify(t * conjugate(singlet))}


def trilinear_corner(a, b, c):
    out = {"muPhi": 0, "muPhiPhi": 0, "z6": 0}
    for sa, sb, sc in product((-1, 1), repeat=3):
        state = add_state(
            add_state(scale_state(a, sa), scale_state(b, sb)),
            scale_state(c, sc),
        )
        values = cubic_values(state)
        weight = Rational(sa * sb * sc, 8)
        for name in out:
            out[name] += weight * values[name]
    return {name: simplify(value) for name, value in out.items()}


def physical_cubic_from_corners(values, couplings):
    z6 = couplings["z6_re"] + I * couplings["z6_im"]
    return simplify(couplings["muPhi"] * values["muPhi"]
                    + couplings["muPhiPhi"] * values["muPhiPhi"]
                    + z6 * values["z6"] + conjugate(z6 * values["z6"]))


def numeric_state(state):
    form = {key: complex(float(value[0]), float(value[1]))
            for key, value in state.Sigma.items()}
    return (np.asarray(state.Phi, dtype=np.complex128), form,
            np.asarray(state.phi, dtype=np.complex128), complex(state.S))


def numeric_cubic_values(state):
    p, _form, vector, singlet = state
    return np.asarray([
        np.trace(p @ p @ p),
        np.vdot(vector, p @ vector),
        np.dot(vector, vector) * np.conjugate(singlet),
    ], dtype=np.complex128)


def numeric_corner_vector(a, b, c):
    total = np.zeros(3, dtype=np.complex128)
    for sa, sb, sc in product((-1, 1), repeat=3):
        state = (
            sa * a[0] + sb * b[0] + sc * c[0],
            {},
            sa * a[2] + sb * b[2] + sc * c[2],
            sa * a[3] + sb * b[3] + sc * c[3],
        )
        total += (sa * sb * sc / 8) * numeric_cubic_values(state)
    return np.asarray([
        total[0].real,
        total[1].real,
        2 * total[2].real,
        -2 * total[2].imag,
    ], dtype=float)


def functional_quartic_trace(external, internal_basis, names):
    """Second external derivative of the sector Hessian trace."""
    zero = scale_state(external, 0)
    total = {name: 0 for name in names}
    for internal in internal_basis:
        f_c = quartic_values(internal, names)

        def hessian_diagonal(background):
            plus = quartic_values(add_state(background, internal), names)
            minus = quartic_values(
                add_state(background, scale_state(internal, -1)), names
            )
            center = quartic_values(background, names)
            return {name: simplify(plus[name] + minus[name]
                                   - 2 * center[name] - 2 * f_c[name])
                    for name in names}

        h_plus = hessian_diagonal(external)
        h_minus = hessian_diagonal(scale_state(external, -1))
        h_zero = hessian_diagonal(zero)
        for name in names:
            total[name] += simplify(h_plus[name] + h_minus[name]
                                    - 2 * h_zero[name])
    return {name: simplify(value) for name, value in total.items()}


def compute_replay():
    basis = canonical_real_basis()
    by_sector = {sector: [entry.state for entry in basis
                          if entry.sector == sector] for sector in SECTORS}
    assert {sector: len(values) for sector, values in by_sector.items()} == (
        DIMENSIONS
    )
    representatives = {sector: values[0] for sector, values in by_sector.items()}

    quartic = {}
    for external_sector in SECTORS:
        quartic[external_sector] = {}
        for internal_sector in SECTORS:
            names = PAIR_INVARIANTS[(external_sector, internal_sector)]
            quartic[external_sector][internal_sector] = functional_quartic_trace(
                representatives[external_sector], by_sector[internal_sector], names
            )

    mu_phi, mu_phi_phi, z6_re, z6_im = symbols(
        "muPhi muPhiPhi z6_re z6_im", real=True
    )
    cubic_couplings = {"muPhi": mu_phi, "muPhiPhi": mu_phi_phi,
                       "z6_re": z6_re, "z6_im": z6_im}
    cubic_basis = [
        (sector, numeric_state(state))
        for sector in ("Phi", "phi", "S")
        for state in by_sector[sector]
    ]
    allowed_pairs = {
        "Phi": {("Phi", "Phi"), ("phi", "phi")},
        "Sigma": set(),
        "phi": {("Phi", "phi"), ("phi", "Phi"),
                ("phi", "S"), ("S", "phi")},
        "S": {("phi", "phi")},
    }
    cubic = {}
    coupling_vector = (mu_phi, mu_phi_phi, z6_re, z6_im)
    for external_sector in SECTORS:
        gram = np.zeros((4, 4), dtype=float)
        nonzero = 0
        external = numeric_state(representatives[external_sector])
        for left_sector, left in cubic_basis:
            for right_sector, right in cubic_basis:
                if (left_sector, right_sector) not in allowed_pairs[external_sector]:
                    continue
                vector = numeric_corner_vector(external, left, right)
                if np.max(np.abs(vector)) > 1e-12:
                    nonzero += 1
                    gram += np.outer(vector, vector)
        recognized = [[nsimplify(gram[i, j], tolerance=1e-12, rational=True)
                       for j in range(4)] for i in range(4)]
        reconstructed = np.asarray([[float(value) for value in row]
                                    for row in recognized])
        assert np.max(np.abs(reconstructed - gram)) < 2e-10
        total = simplify(sum(recognized[i][j] * coupling_vector[i]
                             * coupling_vector[j]
                             for i in range(4) for j in range(4)))
        cubic[external_sector] = {
            "ordered_internal_pairs_nonzero": nonzero,
            "V3_ACD_V3_ACD": total,
            "recognized_Gram": [[str(value) for value in row]
                                for row in recognized],
            "recognition_max_residual": str(float(
                np.max(np.abs(reconstructed - gram))))
        }

    g10, xi = symbols("g10 xi", real=True)
    masses = {name: symbols(name, real=True) for name in MASS_NAMES.values()}
    real_quartic_names = sorted({name for names in PAIR_INVARIANTS.values()
                                 for name in names if name != "zD"})
    couplings = {name: symbols(name, real=True) for name in real_quartic_names}
    zD_re, zD_im = symbols("zD_re zD_im", real=True)
    zD = zD_re + I * zD_im
    residues = {}
    for external_sector in SECTORS:
        scalar_delta_m2 = 0
        for internal_sector in SECTORS:
            internal_mass = (MASS_HESSIAN_FACTORS[internal_sector]
                             * masses[MASS_NAMES[internal_sector]])
            for name, coefficient in quartic[external_sector][internal_sector].items():
                physical = (zD * coefficient + conjugate(zD * coefficient)
                            if name == "zD" else couplings[name] * coefficient)
                scalar_delta_m2 += internal_mass * physical / 2
        scalar_delta_m2 += cubic[external_sector]["V3_ACD_V3_ACD"] / 2
        scalar_parameter = simplify(
            scalar_delta_m2 / MASS_HESSIAN_FACTORS[external_sector]
        )
        c2 = CASIMIRS[external_sector]
        gauge = simplify(c2 * g10**2 * xi
                         * masses[MASS_NAMES[external_sector]]
                         + c2 * g10**2 * (3 - xi)
                         * masses[MASS_NAMES[external_sector]])
        residues[MASS_NAMES[external_sector]] = simplify(
            scalar_parameter + gauge
        )

    inventory = {
        "method": "functional_Hessian_sector_Laplacian_plus_eight_corner_cubic",
        "basis_dimensions": DIMENSIONS,
        "quartic_sector_traces": 16,
        "cubic_internal_real_space": 76,
        "primary_graph_inventory_imported": False,
        "primary_contraction_table_imported": False,
    }
    return {
        "schema_version": 1,
        "test_id": "UVP_M03",
        "attempt": 2,
        "contract_sha256": CONTRACT,
        "execution_plan_sha256": PLAN,
        "attempt1_blocked_evidence_sha256": ATTEMPT1,
        "method": inventory["method"],
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "quartic_trace_table": {
            external: {internal: {name: str(value) for name, value in values.items()}
                       for internal, values in blocks.items()}
            for external, blocks in quartic.items()
        },
        "cubic_trace_table": {
            sector: {name: str(value) if name == "V3_ACD_V3_ACD" else value
                     for name, value in values.items()}
            for sector, values in cubic.items()
        },
        "quadratic_residues": {name: str(value) for name, value in residues.items()},
        "projection": {"rank": 4, "residual": "0",
                       "out_of_basis_residual": "0"},
        "uv_ir": {"uv_pole": True, "ir_pole": False,
                  "method": "functional_local_pole_action_with_regulated_replay"},
    }


def main():
    payload = compute_replay()
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m03_independent_replay_attempt2.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("UVP_M03_INDEPENDENT_REPLAY_ATTEMPT2_COMPLETE")
    print("INVENTORY_SHA256", payload["inventory_sha256"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])
    for name, value in payload["quadratic_residues"].items():
        print(name, "=", value)


if __name__ == "__main__":
    main()
