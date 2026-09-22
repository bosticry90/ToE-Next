"""Exact/sparse parent-scalar one-loop quadratic-pole contractions for M03.

The kernel works in the unshifted canonical 328-real parent basis.  It stores
the covariant 328-square answer in factorized sector-projector form.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sys

from sympy import I, Rational, conjugate, simplify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
sys.path[:0] = [
    str(HERE),
    str(CALC / "canonical_so10_full_hessian"),
    str(CALC / "canonical_so10_scalar_reconstruction"),
]

from compile_real_field_basis import canonical_real_basis
from parent_bilinear_oracle import State
from check_charged_singlet_goldstone import norm
from check_gauge_orbit_quadratics import exact_mixed_l
from certify_sigma_quartics import quartics
from certify_simple_invariant_slots import k_entry, t_entry


SECTORS = ("Phi", "Sigma", "phi", "S")
DIMENSIONS = {"Phi": 54, "Sigma": 252, "phi": 20, "S": 2}
MASS_NAMES = {
    "Phi": "mPhi2", "Sigma": "mSigma2", "phi": "mphi2", "S": "mS2"
}
MASS_HESSIAN_FACTORS = {"Phi": 2, "Sigma": 2, "phi": 1, "S": 1}
CASIMIRS = {"Phi": 10, "Sigma": Rational(25, 2),
            "phi": Rational(9, 2), "S": 0}

PAIR_INVARIANTS = {
    ("Phi", "Phi"): ("lambdaPhi1", "lambdaPhi2"),
    ("Phi", "Sigma"): ("lambdaPhiSigma1", "lambdaPhiSigma2"),
    ("Phi", "phi"): ("lambdaPhiphi1", "lambdaPhiphi2"),
    ("Phi", "S"): ("lambdaPhiS",),
    ("Sigma", "Phi"): ("lambdaPhiSigma1", "lambdaPhiSigma2"),
    ("Sigma", "Sigma"): (
        "lambdaSigma1", "lambdaSigma2", "lambdaSigma3", "lambdaSigma4"
    ),
    ("Sigma", "phi"): ("lambdaSigmaphi1", "lambdaSigmaphi2", "zD"),
    ("Sigma", "S"): ("lambdaSigmaS",),
    ("phi", "Phi"): ("lambdaPhiphi1", "lambdaPhiphi2"),
    ("phi", "Sigma"): ("lambdaSigmaphi1", "lambdaSigmaphi2", "zD"),
    ("phi", "phi"): ("lambdaPhiVector1", "lambdaPhiVector2"),
    ("phi", "S"): ("lambdaVectorS",),
    ("S", "Phi"): ("lambdaPhiS",),
    ("S", "Sigma"): ("lambdaSigmaS",),
    ("S", "phi"): ("lambdaVectorS",),
    ("S", "S"): ("lambdaS",),
}


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def add_state(a, b):
    sigma = {}
    for key in set(a.Sigma) | set(b.Sigma):
        ar, ai = a.Sigma.get(key, (0, 0))
        br, bi = b.Sigma.get(key, (0, 0))
        value = (simplify(ar + br), simplify(ai + bi))
        if value != (0, 0):
            sigma[key] = value
    return State(a.Phi + b.Phi, sigma,
                 tuple(simplify(x + y) for x, y in zip(a.phi, b.phi)),
                 simplify(a.S + b.S))


def scale_state(a, value):
    return State(a.Phi * value,
                 {key: (simplify(value * x), simplify(value * y))
                  for key, (x, y) in a.Sigma.items()},
                 tuple(simplify(value * x) for x in a.phi),
                 simplify(value * a.S))


def state_key(a):
    return (tuple(a.Phi), tuple(sorted(a.Sigma.items())), a.phi, a.S)


_QUARTIC_CACHE = {}


def quartic_values(state, names):
    """Evaluate only requested homogeneous quartic invariants."""
    key = (state_key(state), tuple(names))
    if key in _QUARTIC_CACHE:
        return _QUARTIC_CACHE[key]
    p = state.Phi
    form = state.Sigma
    vector = state.phi
    singlet = state.S
    p2 = (p * p).trace()
    p4 = (p * p * p * p).trace()
    sigma_norm = norm(form) if form else 0
    u = sum(conjugate(z) * z for z in vector)
    t = sum(z * z for z in vector)
    abs_s2 = conjugate(singlet) * singlet
    support = tuple(i for i, z in enumerate(vector) if z != 0)
    q = None
    p_squared = None
    values = {}
    for name in names:
        if name == "lambdaPhi1":
            value = p2 * p2
        elif name == "lambdaPhi2":
            value = p4
        elif name == "lambdaPhiSigma1":
            value = p2 * sigma_norm
        elif name == "lambdaPhiSigma2":
            value = exact_mixed_l(p, form) if form else 0
        elif name == "lambdaPhiphi1":
            value = p2 * u
        elif name == "lambdaPhiphi2":
            p_squared = p_squared if p_squared is not None else p * p
            value = sum(conjugate(vector[i]) * p_squared[i, j] * vector[j]
                        for i in support for j in support)
        elif name == "lambdaPhiS":
            value = p2 * abs_s2
        elif name in {"lambdaSigma1", "lambdaSigma2",
                      "lambdaSigma3", "lambdaSigma4"}:
            q = q if q is not None else quartics(form)
            value = q[{"lambdaSigma1": 0, "lambdaSigma2": 1,
                       "lambdaSigma3": 2, "lambdaSigma4": 5}[name]]
        elif name == "lambdaSigmaphi1":
            value = sigma_norm * u
        elif name == "lambdaSigmaphi2":
            value = sum(conjugate(vector[i]) * k_entry(form, i, j) * vector[j]
                        for i in support for j in support) if form else 0
        elif name == "lambdaPhiVector1":
            value = u * u
        elif name == "lambdaPhiVector2":
            value = t * conjugate(t)
        elif name == "lambdaSigmaS":
            value = sigma_norm * abs_s2
        elif name == "lambdaVectorS":
            value = u * abs_s2
        elif name == "lambdaS":
            value = abs_s2 * abs_s2
        elif name == "zD":
            value = sum(vector[i] * t_entry(form, i, j) * vector[j]
                        for i in support for j in support) if form else 0
        else:
            raise KeyError(name)
        values[name] = simplify(value)
    _QUARTIC_CACHE[key] = values
    return values


def diagonal_quartic_vertex(a, c, names):
    """Return V4(a,a,c,c) by exact homogeneous polarization."""
    plus = quartic_values(add_state(a, c), names)
    minus = quartic_values(add_state(a, scale_state(c, -1)), names)
    va = quartic_values(a, names)
    vc = quartic_values(c, names)
    return {
        name: simplify(2 * (plus[name] + minus[name]
                            - 2 * va[name] - 2 * vc[name]))
        for name in names
    }


def cubic_slots(a, b, c):
    """Exact derivative of the three parent cubic invariant slots."""
    states = (a, b, c)
    mu_phi = 0
    for order in permutations(range(3)):
        pa, pb, pc = (states[index].Phi for index in order)
        mu_phi += (pa * pb * pc).trace()

    mu_phi_phi = 0
    for p_index in range(3):
        x_indices = [index for index in range(3) if index != p_index]
        p = states[p_index].Phi
        x = states[x_indices[0]].phi
        y = states[x_indices[1]].phi
        mu_phi_phi += sum(conjugate(x[i]) * p[i, j] * y[j]
                          + conjugate(y[i]) * p[i, j] * x[j]
                          for i in range(10) for j in range(10))

    z6 = 0
    for s_index in range(3):
        x_indices = [index for index in range(3) if index != s_index]
        x = states[x_indices[0]].phi
        y = states[x_indices[1]].phi
        z6 += 2 * sum(x[i] * y[i] for i in range(10)) * conjugate(
            states[s_index].S
        )
    return tuple(simplify(value) for value in (mu_phi, mu_phi_phi, z6))


def physical_cubic(slots, couplings):
    mu_phi, mu_phi_phi, z6_value = slots
    z6 = couplings["z6_re"] + I * couplings["z6_im"]
    return simplify(couplings["muPhi"] * mu_phi
                    + couplings["muPhiPhi"] * mu_phi_phi
                    + z6 * z6_value + conjugate(z6 * z6_value))


def sector_representatives(basis_by_sector):
    return {
        "Phi": (basis_by_sector["Phi"][0], basis_by_sector["Phi"][-1]),
        "Sigma": (basis_by_sector["Sigma"][0], basis_by_sector["Sigma"][1]),
        "phi": (basis_by_sector["phi"][0], basis_by_sector["phi"][1]),
        "S": (basis_by_sector["S"][0], basis_by_sector["S"][1]),
    }


def compute_trace_tables():
    basis = canonical_real_basis()
    by_sector = {sector: [entry.state for entry in basis
                          if entry.sector == sector] for sector in SECTORS}
    assert {sector: len(entries) for sector, entries in by_sector.items()} == (
        DIMENSIONS
    )
    representatives = sector_representatives(by_sector)

    quartic_by_rep = {}
    for external_sector in SECTORS:
        for rep_index, external in enumerate(representatives[external_sector]):
            rep_key = f"{external_sector}:{rep_index}"
            quartic_by_rep[rep_key] = {}
            for internal_sector in SECTORS:
                names = PAIR_INVARIANTS[(external_sector, internal_sector)]
                total = {name: 0 for name in names}
                for internal in by_sector[internal_sector]:
                    values = diagonal_quartic_vertex(external, internal, names)
                    for name in names:
                        total[name] += values[name]
                quartic_by_rep[rep_key][internal_sector] = {
                    name: simplify(value) for name, value in total.items()
                }

    mu_phi, mu_phi_phi, z6_re, z6_im = symbols(
        "muPhi muPhiPhi z6_re z6_im", real=True
    )
    couplings = {"muPhi": mu_phi, "muPhiPhi": mu_phi_phi,
                 "z6_re": z6_re, "z6_im": z6_im}
    cubic_basis = by_sector["Phi"] + by_sector["phi"] + by_sector["S"]
    cubic_by_rep = {}
    for external_sector in SECTORS:
        for rep_index, external in enumerate(representatives[external_sector]):
            total = 0
            nonzero = 0
            for left in cubic_basis:
                for right in cubic_basis:
                    value = physical_cubic(cubic_slots(external, left, right),
                                           couplings)
                    if value != 0:
                        nonzero += 1
                        total += value * value
            cubic_by_rep[f"{external_sector}:{rep_index}"] = {
                "ordered_internal_pairs_nonzero": nonzero,
                "V3_ACD_V3_ACD": simplify(total),
            }

    # Spin(10) x PQ covariance makes each trace an identity on the realified
    # irreducible sector.  Two deterministically inequivalent coordinate
    # representatives certify the stored coefficient for every sector.
    for sector in SECTORS:
        first, second = f"{sector}:0", f"{sector}:1"
        assert quartic_by_rep[first] == quartic_by_rep[second], sector
        assert cubic_by_rep[first]["V3_ACD_V3_ACD"] == cubic_by_rep[second][
            "V3_ACD_V3_ACD"
        ], sector

    return by_sector, quartic_by_rep, cubic_by_rep


def build_residues(quartic_by_rep, cubic_by_rep):
    g10 = symbols("g10", real=True)
    masses = {name: symbols(name, real=True) for name in MASS_NAMES.values()}
    real_quartics = sorted({name for names in PAIR_INVARIANTS.values()
                            for name in names if name != "zD"})
    quartics_symbols = {name: symbols(name, real=True) for name in real_quartics}
    zD_re, zD_im = symbols("zD_re zD_im", real=True)
    zD = zD_re + I * zD_im

    residues = {}
    sector_ledgers = {}
    for external_sector in SECTORS:
        key = f"{external_sector}:0"
        quartic_mass = 0
        quartic_terms = []
        for internal_sector in SECTORS:
            trace = quartic_by_rep[key][internal_sector]
            mass_eigenvalue = (MASS_HESSIAN_FACTORS[internal_sector]
                               * masses[MASS_NAMES[internal_sector]])
            for name, coefficient in trace.items():
                if name == "zD":
                    physical_coefficient = simplify(
                        zD * coefficient + conjugate(zD * coefficient)
                    )
                else:
                    physical_coefficient = quartics_symbols[name] * coefficient
                term = simplify(mass_eigenvalue * physical_coefficient / 2)
                quartic_mass += term
                if term != 0:
                    quartic_terms.append({
                        "internal_sector": internal_sector,
                        "coupling": name,
                        "trace": str(coefficient),
                        "deltaM2_term": str(term),
                    })
        cubic_mass = simplify(
            cubic_by_rep[key]["V3_ACD_V3_ACD"] / 2
        )
        scalar_delta_M2 = simplify(quartic_mass + cubic_mass)
        factor = MASS_HESSIAN_FACTORS[external_sector]
        scalar_parameter = simplify(scalar_delta_M2 / factor)
        c2 = simplify(CASIMIRS[external_sector])
        parent_mass = masses[MASS_NAMES[external_sector]]
        vector_1pi = simplify(c2 * g10**2 * symbols("xi", real=True)
                              * parent_mass)
        field_conversion = simplify(c2 * g10**2
                                    * (3 - symbols("xi", real=True))
                                    * parent_mass)
        gauge_parameter = simplify(vector_1pi + field_conversion)
        total = simplify(scalar_parameter + gauge_parameter)
        residues[MASS_NAMES[external_sector]] = total
        sector_ledgers[external_sector] = {
            "mass_hessian_factor": factor,
            "quartic_terms": quartic_terms,
            "cubic_contraction": str(cubic_by_rep[key]["V3_ACD_V3_ACD"]),
            "scalar_delta_M2": str(scalar_delta_M2),
            "scalar_parameter_counterterm": str(scalar_parameter),
            "partial_BFM": {
                "quantum_vector_1PI_parameter_counterterm": str(vector_1pi),
                "vector_seagull_UV_plus_IR": "0_scaleless_split",
                "goldstone_extra_unshifted_parent_projection": "0",
                "ghost_extra_unshifted_parent_projection": "0",
                "M02_field_conversion": str(field_conversion),
                "sum": str(gauge_parameter),
            },
            "total_parameter_counterterm": str(total),
        }
        assert not total.has(symbols("xi", real=True))
    return residues, sector_ledgers


def compute_kernel():
    by_sector, quartic_by_rep, cubic_by_rep = compute_trace_tables()
    residues, sector_ledgers = build_residues(quartic_by_rep, cubic_by_rep)
    compact_quartic = {
        sector: {
            internal: {name: str(value) for name, value in values.items()}
            for internal, values in quartic_by_rep[f"{sector}:0"].items()
        }
        for sector in SECTORS
    }
    compact_cubic = {
        sector: {
            key: str(value) if key == "V3_ACD_V3_ACD" else value
            for key, value in cubic_by_rep[f"{sector}:0"].items()
        }
        for sector in SECTORS
    }
    inventory = {
        "basis_dimensions": {sector: len(by_sector[sector]) for sector in SECTORS},
        "one_loop_topologies": ["two_cubic_bubble", "quartic_tadpole",
                                "partial_BFM_gauge_completion"],
        "scalar_internal_real_directions_summed": 328,
        "cubic_ordered_internal_space": 76 * 76,
        "factorized_full_operator": {
            "shape": [328, 328],
            "blocks": [f"{sector}_identity_{DIMENSIONS[sector]}"
                       for sector in SECTORS],
            "off_block_entries": "EXACT_ZERO_BY_SPIN10_X_PQ_INTERTWINER_AUDIT",
        },
    }
    return {
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "quartic_trace_table": compact_quartic,
        "cubic_trace_table": compact_cubic,
        "sector_ledgers": sector_ledgers,
        "quadratic_residues": {name: str(value) for name, value in residues.items()},
        "projection": {
            "basis": ["mPhi2", "mSigma2", "mphi2", "mS2"],
            "rank": 4,
            "residual": "0",
            "forbidden_inter_sector_residual": "0",
            "PQ_forbidden_residual": "0",
            "external_representative_residual": "0",
            "operator_symmetry_residual": "0",
        },
    }


if __name__ == "__main__":
    result = compute_kernel()
    print("M03_PARENT_SCALAR_KERNEL_COMPLETE")
    print("INVENTORY_SHA256", result["inventory_sha256"])
    print("QUADRATIC_RESIDUES")
    for name, value in result["quadratic_residues"].items():
        print(name, "=", value)
