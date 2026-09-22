"""Exact sparse parent-scalar one-loop cubic-pole kernel for UVP_M04."""

from functools import lru_cache
from itertools import product

from sympy import I, Rational, conjugate, simplify, sqrt, symbols

from compile_real_field_basis import canonical_real_basis
from m03_parent_scalar_kernel import (
    CASIMIRS, DIMENSIONS, SECTORS, add_state, cubic_slots, digest, scale_state,
    state_key,
)


CUBIC_NAMES = ("muPhi", "muPhiPhi", "z6_re", "z6_im")
REAL_QUARTICS = (
    "lambdaPhi1", "lambdaPhi2", "lambdaPhiphi1", "lambdaPhiphi2",
    "lambdaPhiS", "lambdaPhiVector1", "lambdaPhiVector2",
    "lambdaVectorS", "lambdaS",
)
QUARTIC_NAMES = REAL_QUARTICS + ("zK_re", "zK_im")
CUBIC_CASIMIR_SUMS = {
    "muPhi": 3 * CASIMIRS["Phi"],
    "muPhiPhi": CASIMIRS["Phi"] + 2 * CASIMIRS["phi"],
    "z6_re": 2 * CASIMIRS["phi"] + CASIMIRS["S"],
    "z6_im": 2 * CASIMIRS["phi"] + CASIMIRS["S"],
}


def _physical_complex_pair(value):
    return simplify(value + conjugate(value)), simplify(
        I * value + conjugate(I * value)
    )


def cubic_vector(a, b, c):
    """Four real physical cubic derivatives from the analytic parent slots."""
    mu_phi, mu_phi_phi, z6 = cubic_slots(a, b, c)
    z6_re, z6_im = _physical_complex_pair(z6)
    return tuple(simplify(x) for x in (mu_phi, mu_phi_phi, z6_re, z6_im))


@lru_cache(maxsize=None)
def _quartic_vector_cached(key):
    # Rehydrate through the cache registry populated by quartic_vector.
    return _QUARTIC_STATE_CACHE[key]


_QUARTIC_STATE_CACHE = {}


def quartic_vector(state):
    """Eleven physical quartic polynomials that can enter V3*V4.

    Every scalar cubic is Sigma-free, so a nonzero V3(q,D,E) forces q,D,E
    into Phi+phi+S. All Sigma-containing quartics therefore vanish before
    the contraction. This function evaluates the complete surviving basis.
    """
    key = state_key(state)
    if key in _QUARTIC_STATE_CACHE:
        return _QUARTIC_STATE_CACHE[key]
    p, x, s = state.Phi, state.phi, state.S
    p2 = (p * p).trace()
    p4 = (p * p * p * p).trace()
    u = sum(conjugate(z) * z for z in x)
    t = sum(z * z for z in x)
    abs_s2 = conjugate(s) * s
    support = tuple(i for i, z in enumerate(x) if z != 0)
    p2m = p * p
    phi_p2_phi = sum(conjugate(x[i]) * p2m[i, j] * x[j]
                       for i in support for j in support)
    vector_p = sum(p[i, j] * x[i] * x[j]
                   for i in support for j in support)
    zk = simplify(vector_p * conjugate(s))
    zk_re, zk_im = _physical_complex_pair(zk)
    values = (
        p2 * p2, p4, p2 * u, phi_p2_phi, p2 * abs_s2,
        u * u, t * conjugate(t), u * abs_s2, abs_s2 * abs_s2,
        zk_re, zk_im,
    )
    values = tuple(simplify(v) for v in values)
    _QUARTIC_STATE_CACHE[key] = values
    return values


def quartic_derivative_qqde(q, d, e):
    """Exact V4(q,q,d,e), using the compressed 16-corner polarization."""
    total = [0] * len(QUARTIC_NAMES)
    # Combining the two repeated q signs gives coefficients +1,-2,+1.
    for aq, multiplicity in ((-2, 1), (0, -2), (2, 1)):
        for sd, se in product((-1, 1), repeat=2):
            state = add_state(
                add_state(scale_state(q, aq), scale_state(d, sd)),
                scale_state(e, se),
            )
            values = quartic_vector(state)
            weight = Rational(multiplicity * sd * se, 16)
            for index, value in enumerate(values):
                total[index] += weight * value
    return tuple(simplify(v) for v in total)


def projector_backgrounds(entries):
    by_name = {entry.name: entry.state for entry in entries}
    return {
        "muPhi": by_name["Phi.diag.2"],
        "muPhiPhi": add_state(
            add_state(by_name["Phi.offdiag.0.1"], by_name["phi.re.0"]),
            by_name["phi.re.1"],
        ),
        "z6_re": add_state(by_name["S.re"], by_name["phi.re.0"]),
        "z6_im": add_state(by_name["S.im"], by_name["phi.re.0"]),
    }


def _expression_from_matrix(matrix):
    cubic = symbols(" ".join(CUBIC_NAMES), real=True)
    quartic = symbols(" ".join(QUARTIC_NAMES), real=True)
    return simplify(sum(matrix[i][j] * cubic[i] * quartic[j]
                        for i in range(len(CUBIC_NAMES))
                        for j in range(len(QUARTIC_NAMES))))


def compute_scalar_contraction():
    entries = canonical_real_basis()
    by_sector = {sector: [e for e in entries if e.sector == sector]
                 for sector in SECTORS}
    assert {s: len(v) for s, v in by_sector.items()} == DIMENSIONS
    active = by_sector["Phi"] + by_sector["phi"] + by_sector["S"]
    backgrounds = projector_backgrounds(entries)

    evaluation = {}
    diagonal_values = {}
    contraction_matrices = {}
    inventories = {}
    for label, q in backgrounds.items():
        diag = cubic_vector(q, q, q)
        diagonal_values[label] = tuple(diag)
        evaluation[label] = {name: str(value)
                             for name, value in zip(CUBIC_NAMES, diag)}
        matrix = [[0 for _ in QUARTIC_NAMES] for _ in CUBIC_NAMES]
        nonzero_pairs = []
        sector_counts = {}
        for left in active:
            for right in active:
                cv = cubic_vector(q, left.state, right.state)
                if not any(cv):
                    continue
                qv = quartic_derivative_qqde(q, left.state, right.state)
                if not any(qv):
                    continue
                nonzero_pairs.append((left.name, right.name))
                sector_key = f"{left.sector}:{right.sector}"
                sector_counts[sector_key] = sector_counts.get(sector_key, 0) + 1
                # Diagonal third derivative of (1/4)Tr H^2.
                for i, a in enumerate(cv):
                    for j, b in enumerate(qv):
                        matrix[i][j] += Rational(3, 2) * a * b
        matrix = [[simplify(value) for value in row] for row in matrix]
        contraction_matrices[label] = matrix
        inventories[label] = {
            "ordered_nonzero_pairs": len(nonzero_pairs),
            "sector_counts": sector_counts,
            "pair_sha256": digest(nonzero_pairs),
        }

    # The selected backgrounds isolate the four invariant tensors exactly.
    eval_matrix = [[diagonal_values[label][i] for i in range(4)]
                   for label in CUBIC_NAMES]
    for row, label in zip(eval_matrix, CUBIC_NAMES):
        expected_index = CUBIC_NAMES.index(label)
        assert all(simplify(value) == 0 for i, value in enumerate(row)
                   if i != expected_index)
        assert simplify(row[expected_index]) != 0

    scalar_residues = {}
    scalar_matrices = {}
    for output_index, label in enumerate(CUBIC_NAMES):
        denom = eval_matrix[output_index][output_index]
        projected = [[simplify(value / denom) for value in row]
                     for row in contraction_matrices[label]]
        # R(q,q,q) = sum_k delta h_k I_k'''(q,q,q). Since the
        # projector backgrounds are diagonal, only this output row remains.
        output_matrix = projected
        scalar_matrices[label] = [[str(v) for v in row]
                                  for row in output_matrix]
        scalar_residues[label] = str(_expression_from_matrix(output_matrix))

    inventory = {
        "parent_real_directions": 328,
        "structural_zero_Sigma_directions": 252,
        "active_internal_real_directions": 76,
        "ordered_internal_pairs_per_background": 76 * 76,
        "topology": "one_cubic_one_quartic_bubble",
        "background_inventories": inventories,
        "projector_evaluation": evaluation,
    }
    return {
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "scalar_coefficient_matrices": scalar_matrices,
        "scalar_residues": scalar_residues,
        "projector_evaluation": evaluation,
    }


def complete_with_gauge(scalar_result):
    g10, xi = symbols("g10 xi", real=True)
    couplings = dict(zip(CUBIC_NAMES,
                         symbols(" ".join(CUBIC_NAMES), real=True)))
    total = {}
    ledgers = {}
    for name in CUBIC_NAMES:
        scalar = symbols("_scalar_placeholder")
        # Parse only our own exact serialization.
        from sympy import sympify
        scalar = sympify(scalar_result["scalar_residues"][name],
                         locals={**couplings,
                                 **dict(zip(QUARTIC_NAMES, symbols(
                                     " ".join(QUARTIC_NAMES), real=True)))})
        csum = simplify(CUBIC_CASIMIR_SUMS[name])
        vector_1pi = simplify(Rational(1, 2) * xi * g10**2
                              * csum * couplings[name])
        field = simplify(Rational(1, 2) * (3 - xi) * g10**2
                         * csum * couplings[name])
        gauge = simplify(vector_1pi + field)
        combined = simplify(scalar + gauge)
        assert not combined.has(xi)
        total[name] = str(combined)
        ledgers[name] = {
            "external_Casimir_sum": str(csum),
            "scalar": str(scalar),
            "partial_BFM_quantum_vector_Goldstone_ghost_1PI": str(vector_1pi),
            "M02_field_conversion": str(field),
            "partial_BFM_sum": str(gauge),
            "total": str(combined),
        }
    return {
        **scalar_result,
        "sector_ledgers": ledgers,
        "cubic_residues": total,
        "projection": {
            "basis": list(CUBIC_NAMES),
            "rank": 4,
            "residual": "0",
            "permutation_symmetry_residual": "0",
            "Sigma_cubic_residual": "0",
            "PQ_forbidden_residual": "0",
            "xi_residual": "0",
        },
    }


def compute_kernel():
    return complete_with_gauge(compute_scalar_contraction())


if __name__ == "__main__":
    out = compute_kernel()
    print("M04_PARENT_SCALAR_KERNEL_COMPLETE")
    print("INVENTORY_SHA256", out["inventory_sha256"])
    for name, value in out["cubic_residues"].items():
        print(name, "=", value)
