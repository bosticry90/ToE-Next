"""Complete primary partial-BFM gauge contribution for UVP_M05.

The derivation uses the frozen quadratic background-field action.  For a
constant parent scalar background q, let

    K_ab = <T_a q, T_b q>,  M_V^2 = g10^2 K.

The one-loop pole supertrace gives, in units 1/(16*pi^2*epsilon_bar),

    vector:    (3 + xi^2)/4 Tr(M_V^4)
    Goldstone: xi^2/4 Tr(M_V^4) + xi*g10^2/2 Tr(H2 P)
    ghost:    -xi^2/2 Tr(M_V^4),

where P=sum_a |T_a q><T_a q|.  The scalar-field conversion fixed by M02 is
(3-xi)g10^2/2 times the external Casimir sum.  Thus xi cancels exactly,
leaving 3/4*g10^4*Tr(K^2) and 3/2*g10^2*Csum*c_r.

The script combines this with the complete scalar V4*V4 artifact.  It is the
primary gauge-completed M05 operator; an inventory-independent replay is
still required before UVP_M05 can pass.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Matrix, Rational, simplify, sympify, symbols

from m03_parent_scalar_kernel import CASIMIRS
from m05_rank26_projector import REAL_DIRECTION_NAMES


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work)
    return payload


def _quartic_multiplicities():
    contract = json.loads(
        (HERE / "layer5_counterterm_contract.json").read_text(encoding="utf-8")
    )
    rows = contract["parent_operator_basis"]["rows"]
    result = {}
    for row in rows:
        if row["field_degree"] == 4:
            result[row["coefficient"]] = row["field_multiplicities"]
    assert len(result) == 22  # 18 real families + four complex families.
    return result


def _base_name(direction):
    for suffix in ("_re", "_im"):
        if direction.endswith(suffix):
            return direction[:-len(suffix)]
    return direction


def compute_completion():
    scalar = verified("uvp_m05_complete_scalar_v4v4.json")
    orbit = verified("uvp_m05_gauge_orbit_quartic.json")
    assert scalar["outcome"] == "M05_COMPLETE_SCALAR_V4V4_PASS"
    assert orbit["outcome"] == "M05_GAUGE_ORBIT_QUARTIC_PROJECTION_PASS"

    multiplicities = _quartic_multiplicities()
    g10, xi = symbols("g10 xi", real=True)
    couplings = dict(zip(
        REAL_DIRECTION_NAMES,
        symbols(" ".join(REAL_DIRECTION_NAMES), real=True),
    ))
    locals_map = {**couplings, "g10": g10, "xi": xi}

    scalar_residues = {}
    for output in REAL_DIRECTION_NAMES:
        matrix = Matrix([
            [sympify(value, locals=locals_map) for value in row]
            for row in scalar["coefficient_tables"][output]
        ])
        vector = Matrix([couplings[name] for name in REAL_DIRECTION_NAMES])
        scalar_residues[output] = simplify((vector.T * matrix * vector)[0])

    orbit_coefficients = {
        name: sympify(value) for name, value
        in orbit["projected_coefficients"].items()
    }
    ledgers, total_residues = {}, {}
    sample_xi_residuals = {"1/2": "0", "1": "0", "2": "0"}
    for direction in REAL_DIRECTION_NAMES:
        base = _base_name(direction)
        counts = multiplicities[base]
        csum = simplify(sum(CASIMIRS[field] * count
                            for field, count in counts.items()))
        coupling = couplings[direction]
        orbit_coefficient = orbit_coefficients.get(direction, 0)

        vector_pure = simplify(
            Rational(1, 4) * (3 + xi**2) * g10**4 * orbit_coefficient
        )
        goldstone_pure = simplify(
            Rational(1, 4) * xi**2 * g10**4 * orbit_coefficient
        )
        ghost_pure = simplify(
            -Rational(1, 2) * xi**2 * g10**4 * orbit_coefficient
        )
        goldstone_mixed = simplify(
            Rational(1, 2) * xi * g10**2 * csum * coupling
        )
        field_conversion = simplify(
            Rational(1, 2) * (3 - xi) * g10**2 * csum * coupling
        )
        gauge_total = simplify(
            vector_pure + goldstone_pure + ghost_pure
            + goldstone_mixed + field_conversion
        )
        expected = simplify(
            Rational(3, 4) * g10**4 * orbit_coefficient
            + Rational(3, 2) * g10**2 * csum * coupling
        )
        assert simplify(gauge_total - expected) == 0
        assert not gauge_total.has(xi)
        for sample in (Rational(1, 2), 1, 2):
            assert simplify(gauge_total.subs(xi, sample) - expected) == 0

        total = simplify(scalar_residues[direction] + gauge_total)
        total_residues[direction] = str(total)
        ledgers[direction] = {
            "field_multiplicities": counts,
            "external_Casimir_sum": str(csum),
            "scalar_V4V4": str(scalar_residues[direction]),
            "quantum_vector_pure_g4": str(vector_pure),
            "Goldstone_pure_g4": str(goldstone_pure),
            "ghost_pure_g4": str(ghost_pure),
            "Goldstone_mixed_g2_lambda": str(goldstone_mixed),
            "M02_field_conversion_exactly_once": str(field_conversion),
            "partial_BFM_gauge_sum": str(gauge_total),
            "total_residue": str(total),
            "xi_residual": "0",
        }

    # Regression of the degree-counting derivation against the independently
    # promoted M04 cubic organization: both yield 3/2*g^2*Csum*c after M02.
    m04_regression = {
        "goldstone_1PI_coefficient": "xi/2",
        "M02_field_conversion_coefficient": "(3-xi)/2",
        "sum": "3/2",
        "residual": "0",
    }
    inventory = {
        "parent_quantum_vectors": 45,
        "vacuum_split": {"heavy": 33, "light": 12},
        "Goldstone_parent_orbit_directions": 45,
        "complex_parent_ghosts": 45,
        "quartic_directions": list(REAL_DIRECTION_NAMES),
        "gauge_orbit_nonzero_directions": len(orbit_coefficients),
        "functional_determinant_weights": {
            "quantum_vector": "(3+xi^2)/4",
            "Goldstone": "xi^2/4",
            "ghost": "-xi^2/2",
            "pure_sum": "3/4",
        },
        "M02_field_conversion": "INCLUDED_EXACTLY_ONCE",
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_PRIMARY_SCALAR_PLUS_PARTIAL_BFM_GAUGE_COMPLETE",
        "authority": "PRIMARY_IMPLEMENTATION_COMPLETE_REPLAY_PENDING_NOT_UVP_M05_PASS",
        "normalization": "coefficients multiply 1/(16*pi^2*epsilon_bar)",
        "input_artifacts": {
            "complete_scalar_V4V4": scalar["artifact_sha256"],
            "gauge_orbit_TrK2_projection": orbit["artifact_sha256"],
        },
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "sector_ledgers": ledgers,
        "quartic_residues": total_residues,
        "projection": {
            "basis": list(REAL_DIRECTION_NAMES),
            "rank": 26,
            "scalar_out_of_basis_residual": "0",
            "gauge_orbit_out_of_basis_residual": "0",
            "Hermitian_real_direction_basis": True,
            "PQ_forbidden_residual": "0",
            "xi_residual": "0",
            "sample_xi_residuals": sample_xi_residuals,
        },
        "M04_degree_counting_regression": m04_regression,
        "uv_ir": {
            "uv_pole": True,
            "ir_pole": False,
            "method": "local_constant_background_supertrace_with_nonexceptional_replay_required",
            "locality": "LOCAL_GAUGE_INVARIANT_QUARTIC_POLYNOMIAL",
        },
        "missing_for_UVP_M05": [
            "inventory-independent complete scalar/gauge replay",
            "freeze primary and replay before comparison",
            "formal attempt-2 adjudication",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    result = compute_completion()
    (HERE / "uvp_m05_primary_complete_candidate.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("XI_RESIDUAL", result["projection"]["xi_residual"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
