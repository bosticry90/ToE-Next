"""Fixed-coupling sigma->0 mass recombination, from the parent affine blocks.

The affine block cache was compiled with Sigma=b*Sigma_raw and S=s*S_raw.
For each Hessian entry divide by the corresponding tangent scale factors
before taking b->0. This avoids the false vanishing of the entire 126
quadratic operator that a naive b=0 cache substitution would produce.
The point's tadpole-eliminated coefficients are fixed at the *original*
stationary point; this path is not a family of newly fitted theories.
"""

from collections import defaultdict
from pathlib import Path
import sys
import json

import numpy as np
from sympy import Rational

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent / "canonical_so10_scalar_benchmark"
FULL = HERE.parent / "canonical_so10_full_hessian"
sys.path.insert(0, str(BENCH))
sys.path.insert(0, str(FULL))

from search import FREE, DEGREES, load_blocks, parent_coefficients
from compile_numeric_blocks import SLOTS
from evaluate_sm_hessian_blocks import rational_representatives
from replay_candidate_exact import kinetic_diag
from decompose_sm_tangent import dimension

PHI_DEGREES = {
    "mPhi2": 2, "muPhi": 3, "muPhiPhi": 1,
    "lambdaPhi1": 4, "lambdaPhi2": 4,
    "lambdaPhiSigma1": 2, "lambdaPhiSigma2": 2,
    "lambdaPhiphi1": 2, "lambdaPhiphi2": 2,
    "lambdaPhiS": 2,
    "z4": 1, "zK": 1,
}


def fixed_couplings():
    import json
    base = json.loads((BENCH / "STAGE1_POINT.json").read_text())["free_coefficients"]
    tuned = json.loads((HERE.parent / "canonical_so10_positive_higgs" /
                        "POINT.json").read_text())
    base.update(tuned["changed_free_coefficients"])
    base["mphi2"] = tuned["approximate_mphi2_over_omega2"]
    return parent_coefficients([float(base[n]) for n in FREE], .1, .1)


def endpoint_block(label, coeff, fixed, a, b, s):
    reps = rational_representatives()[label]
    kphi = [int(sector == "Phi") for sector, _, _ in reps]
    ksig = [int(sector in ("Sigma", "SigmaBar")) for sector, _, _ in reps]
    ks = [int(sector in ("S", "SBar")) for sector, _, _ in reps]
    g0 = np.asarray([float(g) for g in kinetic_diag(label, 1, 1)])
    m = len(reps)
    h = np.zeros((m, m), dtype=complex)
    for z, slot in enumerate(SLOTS):
        name, _, part = slot.partition(":")
        nphi = PHI_DEGREES.get(name, 0)
        nsig, n_s = DEGREES.get(name, (0, 0))
        value = fixed[name]
        v = value.imag if part == "im" else value.real
        if abs(v) < 1e-15:
            continue
        for i in range(m):
            for j in range(m):
                if abs(coeff[z, i, j]) < 1e-15:
                    continue
                power_a = nphi-kphi[i]-kphi[j]
                power_b = nsig-ksig[i]-ksig[j]
                power_s = n_s-ks[i]-ks[j]
                assert power_a >= 0 and power_b >= 0 and power_s >= 0, (
                    label, slot, i, j, power_a, power_b, power_s)
                if (a or power_a == 0) and (b or power_b == 0):
                    h[i, j] += (v*(a**power_a)*(b**power_b)
                                *(s**power_s)*coeff[z, i, j])
    h /= np.sqrt(np.outer(g0, g0))
    assert np.max(abs(h-h.conj().T)) < 1e-8, label
    return h


def clusters_at(blocks, fixed, a, b, s):
    eigen = []
    for label, coeff in sorted(blocks.items()):
        h = endpoint_block(label, coeff, fixed, a, b, s)
        for q in np.linalg.eigvalsh(h).real/60:
            eigen.append((float(q), dimension(label), label))
    assert sum(d for _, d, _ in eigen) == 328
    clusters = []
    for mass, dim, label in sorted(eigen):
        if not clusters or abs(clusters[-1][0]-mass) > 1e-8:
            clusters.append([mass, dim, [label]])
        else:
            clusters[-1][1] += dim
            clusters[-1][2].append(label)
    assert sum(row[1] for row in clusters) == 328
    return clusters


def main():
    blocks = load_blocks()
    fixed = fixed_couplings()
    s = .1*np.sqrt(30)
    b_physical = .1*np.sqrt(15/8)
    recorded = json.loads((HERE.parent / "canonical_so10_gauge_matching" /
                           "scalar_sm_ledger.json").read_text())
    for row in recorded["blocks"]:
        ir = row["sm_irrep"]
        label = tuple(ir["su3_dynkin"]+[ir["su2_dim"]-1,
                                          int(ir["hypercharge"].split("/")[0])])
        h = endpoint_block(label, blocks[label], fixed, 1, b_physical, s)
        calc = sorted(np.linalg.eigvalsh(h).real/60, key=abs)
        assert np.allclose(calc, row["mass_squared_over_omega_squared"],
                           rtol=1e-9, atol=1e-9), label
    clusters = clusters_at(blocks, fixed, 1, 0, s)
    assert sorted(row[1] for row in clusters) == sorted(
        [120, 60, 60, 24, 20, 9, 6, 6, 6, 6, 4, 4, 1, 1, 1])
    print("PS_LIMIT_NUMERIC_RECOMBINATION", "clusters", len(clusters))
    for mass, dim, labels in clusters:
        print(f"m2/omega2={mass:.12g} real_dim={dim} SM_irreps={labels}")
    unified = clusters_at(blocks, fixed, 0, 0, s)
    assert sorted(row[1] for row in unified) == sorted([252, 54, 10, 10, 1, 1])
    print("SPIN10_LIMIT_NUMERIC_RECOMBINATION", "clusters", len(unified))
    for mass, dim, _ in unified:
        print(f"m2/omega2={mass:.12g} real_dim={dim}")
    ps_labels = [
        "126_C triplet sectors (10,3,1)+(10bar,1,3), realified",
        "54/S PS-singlet mixing eigenstate", "54_R (6,2,2) first-stage orbit",
        "10_C (1,2,2), real copy A", "54/S PS-singlet mixing eigenstate",
        "10_C (6,1,1), real copy A", "10_C (6,1,1), real copy B",
        "10_C (1,2,2), real copy B", "54/S PS-singlet mixing eigenstate",
        "54_R (20prime,1,1)", "54_R (1,3,3)",
        "126_C (15,2,2), real copy A", "126_C (15,2,2), real copy B",
        "126_C (6,1,1), real copy A", "126_C (6,1,1), real copy B",
    ]
    spin_labels = ["126_C realification", "S real direction A", "54_R",
                   "10_C real copy A", "10_C real copy B",
                   "S real direction B"]
    assert len(ps_labels) == len(clusters) and len(spin_labels) == len(unified)
    result = {
        "authority": "fixed_coupling_nonstationary_symmetry_limit_numeric_spectrum_not_physical_threshold_masses",
        "path": "Phi=a*Phi_frozen, Sigma=b*Sigma_frozen, S=S_frozen; original parent couplings held fixed",
        "ps_limit": [
            {"m2_over_omega2": mass, "real_dimension": dim,
             "parent_ps_sector": tag,
             "threshold_mass_eligible_without_further_matching": False}
            for (mass, dim, _), tag in zip(clusters, ps_labels)],
        "spin10_limit": [
            {"m2_over_omega2": mass, "real_dimension": dim,
             "parent_sector": tag,
             "threshold_mass_eligible_without_further_matching": False}
            for (mass, dim, _), tag in zip(unified, spin_labels)],
    }
    (HERE / "restoration_limit_spectrum.json").write_text(
        json.dumps(result, indent=2)+"\n")


if __name__ == "__main__":
    main()
