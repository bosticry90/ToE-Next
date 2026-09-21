"""Generate the complete exact SM-weight basis from certified highest weights.

The output is an exact real orthogonal parent-to-SM-irrep map.  Multiplicity
mass rotations and the special 290+38 physical disposition are deliberately
left to the next step.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys

from sympy import conjugate, I, Matrix, re, simplify, sqrt


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL = ROOT / "calculations/canonical_so10_full_hessian"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FULL))

from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from compile_sm_multiplicity_representatives import (
    RAISING, action, add_obj, coordinates, kinetic_inner, scale_obj,
)
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import representatives, realified_representative


KINDS = {
    "Phi": "matrix", "Sigma": "form", "SigmaBar": "form",
    "phi": "vector", "phiBar": "vector", "S": "singlet", "SBar": "singlet",
}
LOWERING = tuple(g.H for g in RAISING)


def flat(obj, kind):
    if kind == "singlet":
        return list(obj)
    return list(coordinates(obj, kind))


def canonicalize(obj, kind, old=(), fix_phase=False):
    for previous in old:
        coefficient = (sum(conjugate(a)*b for a, b in zip(previous, obj))
                       if kind == "singlet"
                       else kinetic_inner(previous, obj, kind))
        obj = obj - coefficient*previous if kind == "singlet" else add_obj(
            obj, previous, -coefficient)
    norm2 = (sum(conjugate(z)*z for z in obj) if kind == "singlet"
             else kinetic_inner(obj, obj, kind))
    norm2 = simplify(norm2)
    if norm2 == 0:
        return None
    obj = obj/sqrt(norm2) if kind == "singlet" else scale_obj(obj, 1/sqrt(norm2))
    if fix_phase:
        values = flat(obj, kind)
        pivot = next(simplify(z) for z in values if simplify(z) != 0)
        phase = simplify(conjugate(pivot)/sqrt(simplify(conjugate(pivot)*pivot)))
        obj = obj*phase if kind == "singlet" else scale_obj(obj, phase)
        pivot_after = next(simplify(z) for z in flat(obj, kind) if simplify(z) != 0)
        assert simplify(pivot_after-conjugate(pivot_after)) == 0
    return obj


def generate_copy(highest, sector, expected):
    kind = KINDS[sector]
    if kind == "singlet":
        assert expected == 1
        return [canonicalize(highest, kind, fix_phase=True)]
    basis = [canonicalize(highest, kind, fix_phase=True)]
    queue = [basis[0]]
    while queue and len(basis) < expected:
        current = queue.pop(0)
        for lowering in LOWERING:
            candidate = canonicalize(action(lowering, current, kind), kind, basis)
            if candidate is not None:
                basis.append(candidate)
                queue.append(candidate)
                if len(basis) == expected:
                    break
    assert len(basis) == expected, (sector, expected, len(basis))
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            value = kinetic_inner(a, b, kind)
            assert simplify(value-int(i == j)) == 0, (sector, i, j, value)
    return basis


def representation_matrix(states, sector, generator):
    kind = KINDS[sector]
    if kind == "singlet":
        return Matrix.zeros(len(states))
    return Matrix(len(states), len(states), lambda i, j: simplify(
        kinetic_inner(states[i], action(generator, states[j], kind), kind)))


def tangent_coordinates(sector, obj, parent_basis):
    tangent = realified_representative(sector, obj)
    factor = 1/sqrt(2) if sector == "Phi" else 1
    return Matrix([
        simplify(factor*(real_kinetic_inner(e.state, tangent.real)
                         + I*real_kinetic_inner(e.state, tangent.imag)))
        for e in parent_basis
    ])


def conjugate_label(label):
    p, q, n, y6 = label
    return (q, p, n, -y6)


def real_gram_schmidt(candidates, expected):
    out = []
    for candidate in candidates:
        v = candidate.applyfunc(simplify)
        for old in out:
            v -= (old.T*v)[0]*old
        norm2 = simplify((v.T*v)[0])
        if norm2 == 0:
            continue
        v = (v/sqrt(norm2)).applyfunc(simplify)
        pivot = next(z for z in v if z != 0)
        if pivot.could_extract_minus_sign():
            v = -v
        out.append(v)
        if len(out) == expected:
            break
    assert len(out) == expected, (len(out), expected)
    return out


def sparse_column(column):
    return [[i, str(simplify(z))] for i, z in enumerate(column) if z != 0]


def main():
    parent_basis = canonical_real_basis()
    reps = representatives()
    generated = {}
    complex_columns = {}
    for label in sorted(reps):
        expected = dimension(label)
        generated[label] = []
        complex_columns[label] = []
        for copy_index, (sector, _, highest) in enumerate(reps[label]):
            states = generate_copy(highest, sector, expected)
            generated[label].append((sector, states))
            for state_index, obj in enumerate(states):
                u = tangent_coordinates(sector, obj, parent_basis)
                assert simplify((u.H*u)[0]-1) == 0, (
                    label, copy_index, state_index, sector, (u.H*u)[0])
                complex_columns[label].append((copy_index, state_index, sector, u))
        # Equivalent multiplicity copies must use exactly the same internal
        # irrep basis, so one small Hessian rotation can be replicated across
        # every weight.  This is stricter than dimension closure.
        if len(generated[label]) > 1:
            reference_sector, reference_states = generated[label][0]
            reference = [representation_matrix(reference_states, reference_sector, g)
                         for g in RAISING + LOWERING]
            for sector, states in generated[label][1:]:
                current = [representation_matrix(states, sector, g)
                           for g in RAISING + LOWERING]
                assert current == reference, (label, reference_sector, sector)

    assert sum(len(columns) for columns in complex_columns.values()) == 328

    real_columns = []
    metadata = []
    consumed = set()
    for label in sorted(complex_columns):
        if label in consumed:
            continue
        bar = conjugate_label(label)
        assert bar in complex_columns
        if bar != label:
            chosen = min(label, bar)
            if label != chosen:
                continue
            cols = complex_columns[chosen]
            assert len(cols) == len(complex_columns[bar])
            # R and Rbar are orthogonal subspaces.  Hence real and imaginary
            # parts of a normalized R column, multiplied by sqrt(2), provide
            # a canonical real basis of R plus Rbar.
            for copy_index, state_index, sector, u in cols:
                assert all(simplify((u.T*v)[0]) == 0
                           for _, _, _, v in cols)
                for part, column in (("re", sqrt(2)*u.applyfunc(re)),
                                     ("im", sqrt(2)*u.applyfunc(
                                         lambda z: simplify((z-conjugate(z))/(2*I))))):
                    assert simplify((column.T*column)[0]-1) == 0
                    real_columns.append(column)
                    metadata.append({"label": list(chosen), "copy": copy_index,
                                     "state": state_index, "realification": part,
                                     "source_sector": sector})
            consumed.update((label, bar))
        else:
            candidates = []
            candidate_meta = []
            for copy_index, state_index, sector, u in complex_columns[label]:
                candidates.extend((u.applyfunc(re), u.applyfunc(
                    lambda z: simplify((z-conjugate(z))/(2*I)))))
                candidate_meta.extend(((copy_index, state_index, sector, "re"),
                                       (copy_index, state_index, sector, "im")))
            selected = real_gram_schmidt(candidates, len(complex_columns[label]))
            for ordinal, column in enumerate(selected):
                real_columns.append(column)
                metadata.append({"label": list(label), "self_conjugate_ordinal": ordinal,
                                 "realification": "exact_real_span"})
            consumed.add(label)

    assert len(real_columns) == 328
    U = Matrix.hstack(*real_columns)
    assert U.T*U == Matrix.eye(328)
    assert U.rank() == 328

    serial_columns = [sparse_column(column) for column in real_columns]
    serial = json.dumps(serial_columns, sort_keys=True, separators=(",", ":"))
    payload = {
        "outcome": "CANONICAL_FULL_SM_WEIGHT_BASIS_PASS",
        "parent_component_basis_sha256": (
            "c66398b6321988b643af5c12fdbea86c3a2589b7b139450770c6ef72c31a3b5e"),
        "sm_irrep_classes": len(reps),
        "highest_weight_copies": sum(len(v) for v in reps.values()),
        "complexified_weight_states": sum(len(v) for v in complex_columns.values()),
        "real_columns": len(real_columns),
        "kinetic_orthogonality": "EXACT_PASS",
        "rank": U.rank(),
        "real_weight_map_sha256": sha256(serial.encode("utf-8")).hexdigest(),
        "phase_convention": (
            "positive-real highest-weight pivot; fixed lowering order "
            "SU3_alpha1,SU3_alpha2,SU2_alpha; descendant phases inherited "
            "from lowering and exact Gram-Schmidt"
        ),
        "equivalent_copy_representation_matrices": "EXACT_PASS",
        "columns": [{"metadata": meta, "sparse_parent_coordinates": col}
                    for meta, col in zip(metadata, serial_columns)],
        "not_yet_applied": [
            "positive_higgs_multiplicity_mass_rotations",
            "33_gauge_plus_1_PQ_plus_4_Higgs_special_basis",
            "transformed_gauge_generators",
        ],
    }
    (HERE / "sm_weight_basis.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("COMPLEX_WEIGHT_STATES", payload["complexified_weight_states"])
    print("REAL_MAP_RANK", payload["rank"])
    print("REAL_WEIGHT_MAP_SHA256", payload["real_weight_map_sha256"])


if __name__ == "__main__":
    main()
