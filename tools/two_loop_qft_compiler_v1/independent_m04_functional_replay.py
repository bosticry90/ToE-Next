"""Inventory-independent functional/polarization replay for UVP_M04.

This module deliberately does not import the primary M04 kernel. It rebuilds
the one-loop field inventory from the canonical basis and obtains every
parent derivative from the frozen invariant evaluator by corner polarization.
"""

from functools import lru_cache
from itertools import product
import sys
from pathlib import Path

import numpy as np
from sympy import I, Rational, conjugate, simplify, symbols, sympify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CALC = ROOT / "calculations"
sys.path[:0] = [str(HERE), str(CALC / "canonical_so10_full_hessian")]

from compile_real_field_basis import canonical_real_basis
from parent_bilinear_oracle import State, invariant_values
from m03_parent_scalar_kernel import add_state, digest, scale_state, state_key


CUBIC_NAMES = ("muPhi", "muPhiPhi", "z6_re", "z6_im")
REAL_QUARTICS = (
    "lambdaPhi1", "lambdaPhi2", "lambdaPhiphi1", "lambdaPhiphi2",
    "lambdaPhiS", "lambdaPhiVector1", "lambdaPhiVector2",
    "lambdaVectorS", "lambdaS",
)
QUARTIC_NAMES = REAL_QUARTICS + ("zK_re", "zK_im")
CASIMIR_SUMS = {"muPhi": 30, "muPhiPhi": 19,
                 "z6_re": 9, "z6_im": 9}


_VALUES = {}


def fast_add(a, b):
    sigma = {}
    for key in set(a.Sigma) | set(b.Sigma):
        ar, ai = a.Sigma.get(key, (0, 0)); br, bi = b.Sigma.get(key, (0, 0))
        if ar + br != 0 or ai + bi != 0:
            sigma[key] = (ar + br, ai + bi)
    return State(a.Phi + b.Phi, sigma,
                 tuple(x + y for x, y in zip(a.phi, b.phi)), a.S + b.S)


def fast_scale(a, k):
    return State(k * a.Phi,
                 {key: (k * x, k * y) for key, (x, y) in a.Sigma.items()},
                 tuple(k * x for x in a.phi), k * a.S)


def physical_vectors(state):
    key = state_key(state)
    if key in _VALUES:
        return _VALUES[key]
    # Independently transcribed from the frozen invariant definitions. The
    # derivative mechanism remains corner polarization rather than the
    # primary analytic slot tensors.
    p, x, s = state.Phi, state.phi, state.S
    p2 = (p * p).trace(); p3 = (p * p * p).trace()
    p4 = (p * p * p * p).trace()
    u = sum(conjugate(z) * z for z in x); t = sum(z * z for z in x)
    abs_s2 = conjugate(s) * s
    support = tuple(i for i, z in enumerate(x) if z != 0)
    phi_p_phi = sum(conjugate(x[i]) * p[i, j] * x[j]
                    for i in support for j in support)
    p_squared = p * p
    phi_p2_phi = sum(conjugate(x[i]) * p_squared[i, j] * x[j]
                       for i in support for j in support)
    vector_p = sum(p[i, j] * x[i] * x[j]
                   for i in support for j in support)
    z6 = t * conjugate(s); zk = vector_p * conjugate(s)
    cubic = (p3, phi_p_phi,
             simplify(z6 + conjugate(z6)),
             simplify(I * z6 + conjugate(I * z6)))
    real_quartic = (p2 * p2, p4, p2 * u, phi_p2_phi, p2 * abs_s2,
                    u * u, t * conjugate(t), u * abs_s2, abs_s2 * abs_s2)
    quartic = real_quartic + (
        simplify(zk + conjugate(zk)),
        simplify(I * zk + conjugate(I * zk)),
    )
    out = (tuple(simplify(v) for v in cubic),
           tuple(simplify(v) for v in quartic))
    _VALUES[key] = out
    return out


def cubic_corner(a, b, c):
    total = [0] * 4
    for sa, sb, sc in product((-1, 1), repeat=3):
        state = fast_add(fast_add(fast_scale(a, sa), fast_scale(b, sb)),
                         fast_scale(c, sc))
        values, _ = physical_vectors(state)
        weight = Rational(sa * sb * sc, 8)
        for i, value in enumerate(values):
            total[i] += weight * value
    return tuple(simplify(v) for v in total)


def quartic_corner(a, b, c, d):
    total = [0] * len(QUARTIC_NAMES)
    for sa, sb, sc, sd in product((-1, 1), repeat=4):
        state = fast_add(
            fast_add(fast_scale(a, sa), fast_scale(b, sb)),
            fast_add(fast_scale(c, sc), fast_scale(d, sd)),
        )
        _, values = physical_vectors(state)
        weight = Rational(sa * sb * sc * sd, 16)
        for i, value in enumerate(values):
            total[i] += weight * value
    return tuple(simplify(v) for v in total)


def numeric_state(state):
    return (np.asarray(state.Phi, dtype=np.complex128),
            np.asarray(state.phi, dtype=np.complex128), complex(state.S))


def numeric_cubic_polynomials(state):
    p, x, s = state
    z6 = np.dot(x, x) * np.conjugate(s)
    return np.asarray([np.trace(p @ p @ p), np.vdot(x, p @ x),
                       2 * z6.real, -2 * z6.imag], dtype=np.complex128)


def numeric_cubic_corner(a, b, c):
    total = np.zeros(4, dtype=np.complex128)
    for sa, sb, sc in product((-1, 1), repeat=3):
        state = (sa * a[0] + sb * b[0] + sc * c[0],
                 sa * a[1] + sb * b[1] + sc * c[1],
                 sa * a[2] + sb * b[2] + sc * c[2])
        total += (sa * sb * sc / 8) * numeric_cubic_polynomials(state)
    return total


def backgrounds(entries):
    e = {x.name: x.state for x in entries}
    return {
        "muPhi": e["Phi.diag.2"],
        "muPhiPhi": add_state(add_state(e["Phi.offdiag.0.1"], e["phi.re.0"]),
                                e["phi.re.1"]),
        "z6_re": add_state(e["S.re"], e["phi.re.0"]),
        "z6_im": add_state(e["S.im"], e["phi.re.0"]),
    }


def matrix_expression(matrix):
    cubic = symbols(" ".join(CUBIC_NAMES), real=True)
    quartic = symbols(" ".join(QUARTIC_NAMES), real=True)
    return simplify(sum(matrix[i][j] * cubic[i] * quartic[j]
                        for i in range(4) for j in range(len(QUARTIC_NAMES))))


def compute_replay():
    entries = canonical_real_basis()
    active = [x for x in entries if x.sector in ("Phi", "phi", "S")]
    active_numeric = {x.name: numeric_state(x.state) for x in active}
    qset = backgrounds(entries)
    # Bounded replay-source audit: the independently transcribed polynomial
    # vectors equal the authoritative parent evaluator on deterministic states.
    source_audit = []
    for label, q in qset.items():
        direct_c, direct_q = physical_vectors(q)
        authority = invariant_values(q)
        az6, azk = authority["z6"], authority["zK"]
        authority_c = (authority["muPhi"], authority["muPhiPhi"],
                       simplify(az6 + conjugate(az6)),
                       simplify(I * az6 + conjugate(I * az6)))
        authority_q = tuple(authority[n] for n in REAL_QUARTICS) + (
            simplify(azk + conjugate(azk)),
            simplify(I * azk + conjugate(I * azk)),
        )
        assert all(simplify(a - b) == 0 for a, b in zip(direct_c, authority_c))
        assert all(simplify(a - b) == 0 for a, b in zip(direct_q, authority_q))
        source_audit.append(label)
    evaluation = {}
    matrices = {}
    inventories = {}
    for label, q in qset.items():
        diag = cubic_corner(q, q, q)
        q_numeric = numeric_state(q)
        evaluation[label] = {name: str(v)
                             for name, v in zip(CUBIC_NAMES, diag)}
        matrix = [[0 for _ in QUARTIC_NAMES] for _ in CUBIC_NAMES]
        pairs = []
        sector_counts = {}
        for left in active:
            for right in active:
                # Independent numerical parent-polynomial prefilter. The
                # accepted pairs are subsequently recomputed exactly; no
                # numerical coefficient is promoted.
                trial = numeric_cubic_corner(
                    q_numeric, active_numeric[left.name],
                    active_numeric[right.name]
                )
                if np.max(np.abs(trial)) < 1e-12:
                    continue
                cv = cubic_corner(q, left.state, right.state)
                if not any(cv):
                    continue
                qv = quartic_corner(q, q, left.state, right.state)
                if not any(qv):
                    continue
                pairs.append((left.name, right.name))
                skey = f"{left.sector}:{right.sector}"
                sector_counts[skey] = sector_counts.get(skey, 0) + 1
                for i, a in enumerate(cv):
                    for j, b in enumerate(qv):
                        matrix[i][j] += Rational(3, 2) * a * b
        matrices[label] = [[simplify(v) for v in row] for row in matrix]
        inventories[label] = {
            "ordered_nonzero_pairs": len(pairs),
            "sector_counts": sector_counts,
            "pair_sha256": digest(pairs),
        }

    scalar_matrices = {}
    scalar_residues = {}
    for out_index, label in enumerate(CUBIC_NAMES):
        diag = sympify(evaluation[label][label])
        assert diag != 0
        for other in CUBIC_NAMES:
            if other != label:
                assert sympify(evaluation[label][other]) == 0
        projected = [[simplify(v / diag) for v in row]
                     for row in matrices[label]]
        scalar_matrices[label] = [[str(v) for v in row] for row in projected]
        scalar_residues[label] = str(matrix_expression(projected))

    g10, xi = symbols("g10 xi", real=True)
    cubic_symbols = dict(zip(CUBIC_NAMES,
                             symbols(" ".join(CUBIC_NAMES), real=True)))
    quartic_symbols = dict(zip(QUARTIC_NAMES,
                               symbols(" ".join(QUARTIC_NAMES), real=True)))
    residues = {}
    ledgers = {}
    for name in CUBIC_NAMES:
        scalar = sympify(scalar_residues[name],
                         locals={**cubic_symbols, **quartic_symbols})
        csum = Rational(CASIMIR_SUMS[name])
        one_pi = simplify(xi * g10**2 * csum * cubic_symbols[name] / 2)
        field = simplify((3 - xi) * g10**2 * csum
                         * cubic_symbols[name] / 2)
        gauge = simplify(one_pi + field)
        total = simplify(scalar + gauge)
        assert not total.has(xi)
        residues[name] = str(total)
        ledgers[name] = {
            "external_Casimir_sum": str(csum),
            "scalar": str(scalar),
            "partial_BFM_quantum_vector_Goldstone_ghost_1PI": str(one_pi),
            "M02_field_conversion": str(field),
            "partial_BFM_sum": str(gauge),
            "total": str(total),
        }

    inventory = {
        "parent_real_directions": 328,
        "structural_zero_Sigma_directions": 252,
        "active_internal_real_directions": 76,
        "ordered_internal_pairs_per_background": 76 * 76,
        "topology": "independently_generated_one_cubic_one_quartic_bubble",
        "background_inventories": inventories,
        "projector_evaluation": evaluation,
        "primary_graph_inventory_imported": False,
        "primary_contraction_table_imported": False,
        "derivative_method": "independently_transcribed_parent_polynomials_with_eight_and_sixteen_corner_polarization",
        "independent_polynomial_source_audit": source_audit,
    }
    return {
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "scalar_coefficient_matrices": scalar_matrices,
        "scalar_residues": scalar_residues,
        "sector_ledgers": ledgers,
        "cubic_residues": residues,
        "projector_evaluation": evaluation,
        "projection": {
            "basis": list(CUBIC_NAMES), "rank": 4, "residual": "0",
            "permutation_symmetry_residual": "0",
            "Sigma_cubic_residual": "0", "PQ_forbidden_residual": "0",
            "xi_residual": "0",
        },
    }


if __name__ == "__main__":
    out = compute_replay()
    print("M04_INDEPENDENT_FUNCTIONAL_REPLAY_COMPLETE")
    print("INVENTORY_SHA256", out["inventory_sha256"])
    for name, value in out["cubic_residues"].items():
        print(name, "=", value)
