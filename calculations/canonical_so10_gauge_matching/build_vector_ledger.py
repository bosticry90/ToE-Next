"""Canonical VEV heavy-vector mass ratios in the vector-index-one convention.

For T(vector)=1, the plane-rotation matrices used by the existing Gram
calculator are divided by sqrt(2). With L_kin(Phi)=|D Phi|²/2 and
L_kin(Sigma)=|D Sigma|²/(2*5!), the resulting vector mass matrix is
g_10² times the raw orbit Gram divided by two. omega²=60 at this point.
The below-SO10 split labels are spectrum *sets*; no PS-threshold matching
prescription is inferred from the broken-phase eigenvalues.
"""

import json
import math
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_vacuum_kernel"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_reconstruction"))
from check_gauge_hierarchy import spectrum
from derive_stabilizers import generators, phase_complex_structure, form_action
from verify_eta1_doublet_mixing import vacuum_form
from itertools import combinations


def mass_and_hypercharge_sets():
    """Independently project each mass eigenspace against minus ad(Y6)^2."""
    gens = generators()
    phi = np.diag([-2.0]*6+[3.0]*4)
    b = .1*math.sqrt(15/8)
    form = vacuum_form()
    idx = list(combinations(range(10), 5))
    columns = []
    for _, gen in gens:
        g = np.asarray(gen, dtype=float)
        ds = form_action(gen, form)
        sig = np.asarray([complex(*ds.get(k, (0, 0))) for k in idx])
        columns.append(np.r_[((g@phi)-(phi@g)).reshape(-1),
                               b*sig.real, b*sig.imag])
    c = np.column_stack(columns)
    gram = c.T@c
    y6 = 2*phase_complex_structure(((0, 1), (2, 3), (4, 5))) - (
        3*phase_complex_structure(((6, 7), (8, 9))))
    yy = np.asarray(y6, dtype=float)
    adjoint = np.column_stack([
        np.asarray(yy @ np.asarray(gen, dtype=float)
                   - np.asarray(gen, dtype=float) @ yy)[
                       tuple(zip(*[(i, j) for (i, j), _ in gens]))]
        for _, gen in gens
    ])
    assert np.max(abs(adjoint+adjoint.T)) < 1e-12
    assert np.max(abs(gram@adjoint-adjoint@gram)) < 1e-9
    ev, vec = np.linalg.eigh(gram)
    result = []
    for value, count in [(0.6, 8), (3, 1), (50, 12), (50.6, 12)]:
        q = vec[:, abs(ev-value) < 1e-9]
        assert q.shape[1] == count
        y2 = np.linalg.eigvalsh(q.T @ (-adjoint@adjoint) @ q)
        result.append((value, [round(float(z)) for z in y2]))
    return result


def main():
    low, high, all_eigen = spectrum(0.1)
    expected = [(0.6, 8), (3.0, 1), (50.0, 12), (50.6, 12)]
    for value, count in expected:
        assert sum(abs(z-value) < 1e-10 for z in all_eigen) == count, (value, all_eigen)
    assert len(low) == 9 and len(high) == 24
    charge_sets = mass_and_hypercharge_sets()
    assert charge_sets[0][1] == [16]*6+[36]*2, charge_sets[0]
    assert charge_sets[1][1] == [0], charge_sets[1]
    assert {tuple(charges) for _, charges in charge_sets[2:]} == {
        tuple([1]*12), tuple([25]*12)
    }, charge_sets
    result = {
        "normalization": "Tr_10(T_a T_b)=delta_ab; raw generators divided by sqrt(2)",
        "formula": "M_vector^2/(g10^2 omega^2)=raw_kinetic_orbit_Gram_eigenvalue/120",
        "omega_squared": 60,
        "unbroken_SM_vectors": 12,
        "mass_sets": [
            {"raw_gram_eigenvalue": z, "real_vectors": n,
             "mass_squared_over_g10_squared_omega_squared": z/120,
             "mass_over_g10_omega": math.sqrt(z/120),
             "hypercharge_y6_squared_multiplicities": {
                 str(k): charges.count(k) for k in sorted(set(charges))},
             "sm_representations_inferred_from_adjoint_branching": {
                 0.6: "(3,1,+2/3)+c.c. and (1,1,+1)+c.c.",
                 3.0: "(1,1,0)",
                 50.0: "(3,2,+5/6)+c.c.",
                 50.6: "(3,2,+1/6)+c.c.",
             }[z]}
            for (z, n), (_, charges) in zip(expected, charge_sets)
        ],
        "PS_to_SM_broken": 9,
        "Spin10_to_PS_broken": 24,
        "min_high_over_max_intermediate_mass": math.sqrt(50/3),
        "min_high_over_min_intermediate_mass": math.sqrt(50/0.6),
        "assignment_caveat": "SM labels use adjoint branching plus exact hypercharge-eigenspace counts; a full SU3/SU2 projector and one-loop massive-vector threshold matching have not been independently frozen.",
    }
    (HERE / "vector_ledger.json").write_text(json.dumps(result, indent=2)+"\n")
    print("VECTOR_SPECTRUM_PASS", "unbroken", 12, "intermediate", 9,
          "first_stage", 24, "ratios",
          result["min_high_over_max_intermediate_mass"],
          result["min_high_over_min_intermediate_mass"])


if __name__ == "__main__":
    main()
