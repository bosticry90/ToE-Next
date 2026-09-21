"""Compile the exact canonical 328-real scalar and 45-generator bases.

This is phase 1a of TWO_LOOP_QFT_COMPILER_V1.  It materializes the parent
component basis in which later gauge actions and vertices can be compiled.
It does not diagonalize the physical Hessian or generate Feynman diagrams.
"""

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

from sympy import I, conjugate, eye, Matrix, re, simplify, sqrt, zeros


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL = ROOT / "calculations/canonical_so10_full_hessian"
sys.path.insert(0, str(FULL))

from parent_bilinear_oracle import State
from compile_sm_multiplicity_representatives import (
    HALF5, hodge, kinetic_inner, projected,
)


@dataclass(frozen=True)
class BasisVector:
    name: str
    sector: str
    state: State


def empty_state(*, Phi=None, Sigma=None, phi=None, S=0):
    return State(Phi if Phi is not None else zeros(10),
                 Sigma if Sigma is not None else {},
                 tuple(phi) if phi is not None else (0,) * 10, S)


def form_state(form):
    out = {}
    for idx, z in form.items():
        a, b = simplify(z).as_real_imag()
        if a != 0 or b != 0:
            out[idx] = (simplify(a), simplify(b))
    return out


def complex_form(state):
    return {idx: a + I*b for idx, (a, b) in state.Sigma.items()}


def real_kinetic_inner(a: State, b: State):
    """Real field-space metric defined by L_kin=(1/2)G_AB dq_A dq_B."""
    phi_part = sum(conjugate(x)*y for x, y in zip(a.phi, b.phi))
    sigma_a, sigma_b = complex_form(a), complex_form(b)
    sigma_part = kinetic_inner(sigma_a, sigma_b, "form")
    scalar_part = conjugate(a.S)*b.S
    matrix_part = kinetic_inner(a.Phi, b.Phi, "matrix")
    return simplify(2*re(matrix_part + sigma_part + phi_part + scalar_part))


def phi_basis():
    out = []
    # Symmetric off-diagonal directions.  The 1/sqrt(2) compensates the
    # all-i,j sum in (1/2)(D Phi_ij)^2.
    for i, j in combinations(range(10), 2):
        m = zeros(10)
        m[i, j] = m[j, i] = 1/sqrt(2)
        out.append(BasisVector(f"Phi.offdiag.{i}.{j}", "Phi",
                               empty_state(Phi=m)))
    # Orthonormal Cartan basis of real traceless diagonal matrices.
    for k in range(1, 10):
        m = zeros(10)
        scale = 1/sqrt(k*(k+1))
        for i in range(k):
            m[i, i] = scale
        m[k, k] = -k*scale
        out.append(BasisVector(f"Phi.diag.{k}", "Phi",
                               empty_state(Phi=m)))
    assert len(out) == 54
    return out


def sigma_basis():
    out = []
    for idx in HALF5:
        # 2 P_(+i)e_idx has unit complex kinetic norm.  Dividing by sqrt(2)
        # supplies the canonically normalized real and imaginary directions.
        unit = {key: simplify(sqrt(2)*z)
                for key, z in projected({idx: 1}, I).items()}
        assert simplify(kinetic_inner(unit, unit, "form")-
                        simplify(1/2)) == 0
        assert all(simplify(hodge(unit).get(key, 0)-I*unit.get(key, 0)) == 0
                   for key in set(unit) | set(hodge(unit)))
        out.append(BasisVector("Sigma.re." + ".".join(map(str, idx)),
                               "Sigma", empty_state(Sigma=form_state(unit))))
        iunit = {key: I*z for key, z in unit.items()}
        out.append(BasisVector("Sigma.im." + ".".join(map(str, idx)),
                               "Sigma", empty_state(Sigma=form_state(iunit))))
    assert len(out) == 252
    return out


def vector_and_singlet_basis():
    out = []
    for i in range(10):
        for tag, value in (("re", 1/sqrt(2)), ("im", I/sqrt(2))):
            v = [0] * 10
            v[i] = value
            out.append(BasisVector(f"phi.{tag}.{i}", "phi",
                                   empty_state(phi=v)))
    out.extend((
        BasisVector("S.re", "S", empty_state(S=1/sqrt(2))),
        BasisVector("S.im", "S", empty_state(S=I/sqrt(2))),
    ))
    return out


def canonical_real_basis():
    basis = phi_basis() + sigma_basis() + vector_and_singlet_basis()
    assert len(basis) == 328
    assert len({entry.name for entry in basis}) == 328
    return basis


def certify_gram(basis):
    # Cross-sector products vanish structurally; certify every within-sector
    # entry exactly.  This evaluates the complete 328x328 Gram claim without
    # spending time multiplying known zero fields across sectors.
    sectors = {}
    for entry in basis:
        sectors.setdefault(entry.sector, []).append(entry)
    tested = 0
    for entries in sectors.values():
        for i, a in enumerate(entries):
            for j, b in enumerate(entries):
                assert simplify(real_kinetic_inner(a.state, b.state)
                                - int(i == j)) == 0, (a.name, b.name)
                tested += 1
    assert sum(len(entries)**2 for entries in sectors.values()) == tested
    return tested


def gauge_basis():
    # Tr_10(T_a^T T_b)=delta_ab.  These match the normalization used by the
    # passed vector ledger (raw plane rotations divided by sqrt(2)).
    out = []
    for i, j in combinations(range(10), 2):
        g = zeros(10)
        g[i, j] = 1/sqrt(2)
        g[j, i] = -1/sqrt(2)
        out.append((f"T.{i}.{j}", g))
    gram = Matrix(45, 45, lambda a, b: simplify(
        (out[a][1].T*out[b][1]).trace()))
    assert gram == eye(45)
    return out


def sparse_state(state):
    return {
        "Phi": [[i, j, str(state.Phi[i, j])]
                for i in range(10) for j in range(10)
                if state.Phi[i, j] != 0],
        "Sigma": [[list(idx), str(a), str(b)]
                  for idx, (a, b) in sorted(state.Sigma.items())],
        "phi": [[i, str(z)] for i, z in enumerate(state.phi) if z != 0],
        "S": str(state.S),
    }


def main():
    basis = canonical_real_basis()
    gram_entries = certify_gram(basis)
    generators = gauge_basis()
    entries = [{"name": e.name, "sector": e.sector,
                "components": sparse_state(e.state)} for e in basis]
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":"))
    payload = {
        "outcome": "CANONICAL_328_REAL_COMPONENT_BASIS_PASS",
        "kinetic_convention": "L_kin=(1/2) G_AB dq_A dq_B",
        "dimensions": {"Phi": 54, "Sigma": 252, "phi": 20, "S": 2,
                       "total": 328},
        "full_basis_sha256": sha256(canonical.encode("utf-8")).hexdigest(),
        "within_sector_gram_entries_tested": gram_entries,
        "cross_sector_gram_entries": "STRUCTURAL_ZERO",
        "gauge_generators": 45,
        "gauge_normalization": "Tr_10(T_a^T T_b)=delta_ab",
        "basis": entries,
        "not_yet_materialized": [
            "physical_290_heavy_scalar_mass_eigenvectors",
            "38_zero_mode_disposition_in_full_component_coordinates",
            "physical_scalar_gauge_goldstone_ghost_vertices",
        ],
    }
    (HERE / "real_field_basis.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("FIELD_BASIS_SHA256", payload["full_basis_sha256"])
    print("GRAM_ENTRIES_TESTED", gram_entries)
    print("GAUGE_GENERATOR_BASIS_PASS", len(generators))


if __name__ == "__main__":
    main()

