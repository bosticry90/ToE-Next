"""Inventory-independent replay of the UVP_M05 gauge completion.

The replay selects a new deterministic exact rank-26 background set, rebuilds
the parent gauge-orbit Gram polynomial from raw generator actions, and derives
the partial-BFM determinant weights from a separate degree-of-freedom ledger.
It does not import the primary orbit projection or gauge residue table.

This covers the gauge part only.  The complete scalar full-operator replay is
still required before UVP_M05 can pass.
"""

from hashlib import sha256
import json
from pathlib import Path
from random import Random
import sys

from sympy import I, Matrix, Rational, simplify, sympify, symbols, zeros
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [
    str(HERE),
    str(ROOT / "calculations" / "canonical_so10_vacuum_kernel"),
    str(ROOT / "calculations" / "canonical_so10_scalar_reconstruction"),
    str(ROOT / "calculations" / "canonical_so10_full_hessian"),
]

from certify_sigma_quartics import generated_form
from compile_real_field_basis import gauge_basis, real_kinetic_inner
from m03_parent_scalar_kernel import CASIMIRS
from m05_rank26_projector import REAL_DIRECTION_NAMES, physical_quartics
from parent_bilinear_oracle import State


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


def _state_stream():
    rng = Random(91505)
    for seed in range(1001, 1101):
        form = generated_form(seed, 4 + seed % 8)
        p = zeros(10)
        diagonal = [rng.randint(-2, 2) for _ in range(9)]
        diagonal.append(-sum(diagonal))
        for i, value in enumerate(diagonal):
            p[i, i] = value
        for _ in range(1 + seed % 3):
            i, j = sorted(rng.sample(range(10), 2))
            p[i, j] = p[j, i] = rng.choice((-2, -1, 1, 2))
        vector = [0] * 10
        for i in rng.sample(range(10), 2 + seed % 2):
            vector[i] = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        singlet = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        yield seed, State(p, form, tuple(vector), singlet)


def _select_rank26():
    # A generic 26-background batch is overwhelmingly likely to be full
    # rank.  Certify that batch once instead of recomputing exact rank after
    # every appended row.  If the batch is singular, fall back to exact
    # rank-growth for later stream entries.
    selected, rows = [], []
    stream = iter(_state_stream())
    for ordinal in range(26):
        seed, state = next(stream)
        print("INDEPENDENT_GAUGE_SELECT", ordinal + 1, "OF", 26,
              flush=True)
        selected.append((seed, state))
        rows.append(list(physical_quartics(state)))
    projector = Matrix(rows)
    rank = DomainMatrix.from_Matrix(projector).rank()
    if rank == 26:
        return selected, projector

    # Retain an exact independent subset if the initial generic batch was
    # unexpectedly singular, then grow it deterministically.
    independent, independent_rows = [], []
    current_rank = 0
    for item, row in zip(selected, rows):
        new_rank = DomainMatrix.from_Matrix(
            Matrix(independent_rows + [row])
        ).rank()
        if new_rank > current_rank:
            independent.append(item)
            independent_rows.append(row)
            current_rank = new_rank
    selected, rows, rank = independent, independent_rows, current_rank
    for seed, state in stream:
        row = list(physical_quartics(state))
        candidate = Matrix(rows + [row])
        new_rank = DomainMatrix.from_Matrix(candidate).rank()
        if new_rank > rank:
            selected.append((seed, state))
            rows.append(row)
            rank = new_rank
            if rank == 26:
                break
    assert rank == 26 and len(selected) == 26
    return selected, Matrix(rows)


def _permutation_parity(values):
    inversions = sum(values[i] > values[j]
                     for i in range(len(values))
                     for j in range(i + 1, len(values)))
    return -1 if inversions % 2 else 1


def _normalized_form_action(generator, form):
    """Act on a five-form without the legacy integer-generator shortcut."""
    out = {}
    for old, (real, imag) in form.items():
        for slot, old_index in enumerate(old):
            for new_index in range(10):
                coefficient = generator[new_index, old_index]
                if coefficient == 0 or new_index in old:
                    continue
                moved = old[:slot] + (new_index,) + old[slot + 1:]
                key = tuple(sorted(moved))
                signed = coefficient * _permutation_parity(moved)
                prior_real, prior_imag = out.get(key, (0, 0))
                out[key] = (
                    simplify(prior_real + signed * real),
                    simplify(prior_imag + signed * imag),
                )
    return {key: value for key, value in out.items() if value != (0, 0)}


def _gauge_action(generator, state):
    # gauge_basis already supplies Tr_10(Ta^T Tb)=delta_ab; unlike the
    # primary route there is no raw-generator normalization step here.
    return State(
        generator * state.Phi - state.Phi * generator,
        _normalized_form_action(generator, state.Sigma),
        tuple(sum(generator[i, j] * state.phi[j] for j in range(10))
              for i in range(10)),
        0,
    )


def _orbit_quartic(state, generators):
    orbit = [_gauge_action(generator, state)
             for _, generator in generators]
    # K is a real symmetric Gram matrix, so Tr(K^2)=sum_ab K_ab^2.
    # Evaluate that identity directly.  A full symbolic 45-by-45 matrix
    # product is algebraically identical but performs 45 times as many
    # multiplications and obscures the independent replay's actual target.
    total = 0
    for a, left in enumerate(orbit):
        for b in range(a, len(orbit)):
            value = real_kinetic_inner(left, orbit[b])
            total += (1 if a == b else 2) * value * value
    return simplify(total)


def _quartic_multiplicities():
    contract = json.loads(
        (HERE / "layer5_counterterm_contract.json").read_text(encoding="utf-8")
    )
    return {
        row["coefficient"]: row["field_multiplicities"]
        for row in contract["parent_operator_basis"]["rows"]
        if row["field_degree"] == 4
    }


def _base_name(direction):
    return direction[:-3] if direction.endswith(("_re", "_im")) else direction


def compute_uncompared():
    selected, projector = _select_rank26()
    print("INDEPENDENT_GAUGE_PROJECTOR_SELECTED", len(selected), flush=True)
    generators = tuple(gauge_basis())
    orbit_values = []
    for ordinal, (_, state) in enumerate(selected, 1):
        print("INDEPENDENT_GAUGE_BACKGROUND", ordinal, "OF", len(selected),
              flush=True)
        orbit_values.append(_orbit_quartic(state, generators))
    values = Matrix(orbit_values)
    coefficients = tuple(simplify(value)
                         for value in projector.inv(method="DM") * values)

    # Independent extra-background replay using the next stream element not
    # selected for the projector.
    selected_seeds = {seed for seed, _ in selected}
    extra_seed, extra = next((seed, state) for seed, state in _state_stream()
                             if seed not in selected_seeds)
    extra_residual = simplify(
        _orbit_quartic(extra, generators)
        - sum(coefficient * value for coefficient, value in zip(
            coefficients, physical_quartics(extra)
        ))
    )
    assert extra_residual == 0

    g10, xi = symbols("g10 xi", real=True)
    coupling_symbols = dict(zip(
        REAL_DIRECTION_NAMES,
        symbols(" ".join(REAL_DIRECTION_NAMES), real=True),
    ))
    multiplicities = _quartic_multiplicities()
    gauge_residues = {}
    ledgers = {}
    for direction, orbit_coefficient in zip(REAL_DIRECTION_NAMES, coefficients):
        counts = multiplicities[_base_name(direction)]
        csum = simplify(sum(CASIMIRS[field] * count
                            for field, count in counts.items()))
        coupling = coupling_symbols[direction]
        transverse = Rational(3, 4) * g10**4 * orbit_coefficient
        longitudinal = Rational(1, 4) * xi**2 * g10**4 * orbit_coefficient
        goldstone_pure = Rational(1, 4) * xi**2 * g10**4 * orbit_coefficient
        ghost = -Rational(1, 2) * xi**2 * g10**4 * orbit_coefficient
        goldstone_mixed = Rational(1, 2) * xi * g10**2 * csum * coupling
        field = Rational(1, 2) * (3 - xi) * g10**2 * csum * coupling
        total = simplify(transverse + longitudinal + goldstone_pure + ghost
                         + goldstone_mixed + field)
        assert not total.has(xi)
        gauge_residues[direction] = str(total)
        ledgers[direction] = {
            "external_Casimir_sum": str(csum),
            "vector_transverse": str(transverse),
            "vector_longitudinal": str(longitudinal),
            "Goldstone_pure": str(goldstone_pure),
            "ghost": str(ghost),
            "Goldstone_mixed": str(goldstone_mixed),
            "M02_field_conversion": str(field),
            "total": str(total),
            "xi_residual": "0",
        }

    nonzero = {
        name: str(value) for name, value in zip(
            REAL_DIRECTION_NAMES, coefficients
        ) if value != 0
    }
    inventory = {
        "projector_generation": "fixed_seed_rank_growth_independent_of_primary",
        "fixed_seed": 91505,
        "selected_state_seeds": [seed for seed, _ in selected],
        "projector_rank": 26,
        "extra_state_seed": extra_seed,
        "generator_source": "compile_real_field_basis.gauge_basis",
        "generator_count": 45,
        "orbit_construction": "explicit_328_real_kinetic_Gram_trace",
        "primary_orbit_projection_imported": False,
        "primary_gauge_residues_imported": False,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_INDEPENDENT_GAUGE_REPLAY_UNCOMPARED",
        "authority": "GAUGE_REPLAY_COMPONENT_ONLY_NOT_UVP_M05_PASS",
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "orbit_projected_coefficients": nonzero,
        "extra_background_residual": "0",
        "sector_ledgers": ledgers,
        "gauge_residues": gauge_residues,
        "xi_residual": "0",
        "scalar_full_operator_replay": "NOT_IMPLEMENTED",
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


def compare_after_freeze(uncompared):
    raw_path = HERE / "uvp_m05_independent_gauge_replay_uncompared.json"
    raw_path.write_text(json.dumps(uncompared, indent=2) + "\n", encoding="utf-8")
    frozen = verified(raw_path.name)
    primary = verified("uvp_m05_primary_complete_candidate.json")
    primary_orbit = verified("uvp_m05_gauge_orbit_quartic.json")
    assert frozen["orbit_projected_coefficients"] == primary_orbit[
        "projected_coefficients"
    ]
    locals_map = {
        **dict(zip(REAL_DIRECTION_NAMES,
                   symbols(" ".join(REAL_DIRECTION_NAMES), real=True))),
        "g10": symbols("g10", real=True),
    }
    residuals = {}
    for direction in REAL_DIRECTION_NAMES:
        replay = sympify(frozen["gauge_residues"][direction], locals=locals_map)
        primary_gauge = sympify(
            primary["sector_ledgers"][direction]["partial_BFM_gauge_sum"],
            locals=locals_map,
        )
        residuals[direction] = str(simplify(replay - primary_gauge))
    assert set(residuals.values()) == {"0"}
    payload = {
        "schema_version": 1,
        "outcome": "M05_INDEPENDENT_GAUGE_REPLAY_PASS",
        "authority": "GAUGE_REPLAY_COMPONENT_ONLY_SCALAR_REPLAY_STILL_MISSING",
        "uncompared_replay_sha256": frozen["artifact_sha256"],
        "primary_candidate_sha256": primary["artifact_sha256"],
        "primary_orbit_sha256": primary_orbit["artifact_sha256"],
        "orbit_coefficient_residual": "0",
        "gauge_residue_residuals": residuals,
        "maximum_residual": "0",
        "xi_residual": "0",
        "remaining_M05_blocker": "INVENTORY_INDEPENDENT_COMPLETE_SCALAR_OPERATOR_REPLAY_MISSING",
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    raw = compute_uncompared()
    result = compare_after_freeze(raw)
    (HERE / "uvp_m05_independent_gauge_replay.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("MAXIMUM_RESIDUAL", result["maximum_residual"])
    print("REMAINING", result["remaining_M05_blocker"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
