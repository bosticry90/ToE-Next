"""Diagnostic 132-real 126-heavy PS-projector split, not an EFT match.

Upper-heavy candidate: 126 PS (6,1,1) and (15,2,2) copies. Every other
scalar tangent, including gauge/PQ directions, is provisionally retained.
Finite-x points except 0 and .1 are off shell in the Sigma direction.
"""

from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
CALC = HERE.parent
for name in ("canonical_so10_ps_threshold_kernel", "canonical_so10_ps_interval_eft",
             "canonical_so10_full_hessian", "canonical_so10_scalar_benchmark"):
    sys.path.insert(0, str(CALC / name))

from check_ps_mass_limit import fixed_couplings, load_blocks, endpoint_block
from check_ps_mass_limit import PHI_DEGREES
from probe_quadratic import stationary_omega
from evaluate_sm_hessian_blocks import rational_representatives
from replay_candidate_exact import kinetic_diag
from search import DEGREES
from compile_numeric_blocks import SLOTS
from decompose_sm_tangent import dimension


def ps_origin(sector, obj):
    if sector in ("Sigma", "SigmaBar"):
        ks = {min(sum(i < 6 for i in idx), 6-sum(i < 6 for i in idx))
              for idx, z in obj.items() if z != 0}
        assert len(ks) == 1, (sector, ks)
        return f"126_k{next(iter(ks))}"
    if sector in ("phi", "phiBar"):
        color = any(obj[i] != 0 for i in range(6))
        weak = any(obj[i] != 0 for i in range(6, 10))
        assert color != weak
        return "10_6" if color else "10_4"
    if sector == "Phi":
        color = obj[:6, :6]
        weak = obj[6:, 6:]
        cross = obj[:6, 6:]
        if any(z != 0 for z in cross):
            assert not any(z != 0 for z in color) and not any(z != 0 for z in weak)
            return "54_24"
        if any(z != 0 for z in color) and not any(z != 0 for z in weak):
            return "54_20"
        if any(z != 0 for z in weak) and not any(z != 0 for z in color):
            return "54_9"
        return "54_1"
    assert sector in ("S", "SBar")
    return "S_1"


def main():
    c = fixed_couplings()
    blocks = load_blocks()
    reps = rational_representatives()
    origins = {label: [ps_origin(sector, obj) for sector, _, obj in entries]
               for label, entries in reps.items()}
    counts = {}
    for label, names in origins.items():
        for name in names:
            counts[name] = counts.get(name, 0)+dimension(label)
    assert sum(counts.values()) == 328, counts
    assert counts["126_k1"] == 12 and counts["126_k2"] == 120
    assert counts["126_k3"] == 120
    assert counts["54_20"] == 20 and counts["54_9"] == 9
    assert counts["54_24"] == 24 and counts["54_1"] == 1
    assert counts["10_6"] == 12 and counts["10_4"] == 8 and counts["S_1"] == 2
    print("PS_ORIGIN_REAL_DIMENSION_LEDGER", dict(sorted(counts.items())))
    a0 = stationary_omega(c, 0)/np.sqrt(60)
    amin, amax = a0, 1.0
    bmax = .1*np.sqrt(15/8)
    s = .1*np.sqrt(30)
    # The nearby positive Phi-tadpole root is monotone on [0,.1]:
    # da/dx has numerator -4 L_mix x omega and a positive denominator.
    lphi = c["lambdaPhi1"]+7*c["lambdaPhi2"]/60
    lmix = c["lambdaPhiSigma1"]-c["lambdaPhiSigma2"]/4
    assert lmix < 0
    assert 8*lphi*stationary_omega(c, 0)+3*c["muPhi"]/np.sqrt(60) > 0
    min0 = float("inf")
    worst_hh_delta = 0.0
    worst_hl_bound = 0.0
    uniform_lower = float("inf")
    uniform_schur = 0.0
    sharp_lower = float("inf")
    sharp_schur = 0.0
    for label, coeff in blocks.items():
        names = origins[label]
        hi = [i for i, name in enumerate(names) if name in ("126_k1", "126_k2")]
        lo = [i for i in range(len(names)) if i not in hi]
        if not hi:
            continue
        h0 = endpoint_block(label, coeff, c, a0, 0.0, s)/60
        local_min0 = float(np.linalg.eigvalsh(h0[np.ix_(hi, hi)])[0])
        min0 = min(min0, local_min0)
        assert not lo or np.linalg.norm(h0[np.ix_(lo, hi)]) < 1e-10
        g0 = np.asarray([float(g) for g in kinetic_diag(label, 1, 1)])
        kphi = [int(sector == "Phi") for sector, _, _ in reps[label]]
        ksig = [int(sector in ("Sigma", "SigmaBar")) for sector, _, _ in reps[label]]
        ks = [int(sector in ("S", "SBar")) for sector, _, _ in reps[label]]
        grouped = {"hh": {}, "lh": {}}
        for z, slot in enumerate(SLOTS):
            name, _, part = slot.partition(":")
            value = c[name]
            v = value.imag if part == "im" else value.real
            if abs(v) < 1e-15:
                continue
            nphi = PHI_DEGREES.get(name, 0)
            nsig, ns = DEGREES.get(name, (0, 0))
            for rowset, colset, target in ((hi, hi, "hh"), (lo, hi, "lh")):
                if not rowset:
                    continue
                terms = grouped[target]
                for i in rowset:
                    for j in colset:
                        if abs(coeff[z, i, j]) < 1e-15:
                            continue
                        powers = (nphi-kphi[i]-kphi[j],
                                  nsig-ksig[i]-ksig[j], ns-ks[i]-ks[j])
                        assert min(powers) >= 0, (label, slot, i, j, powers)
                        mat = terms.setdefault(powers, np.zeros(
                            (len(rowset), len(colset)), dtype=complex))
                        mat[rowset.index(i), colset.index(j)] += (
                            v*coeff[z, i, j]/np.sqrt(g0[i]*g0[j])/60)
        bounded = {}
        for target, terms in grouped.items():
            amount = 0.0
            for (pa, pb, ps), mat in terms.items():
                if pb == 0:
                    factor = (amax**pa-amin**pa)*s**ps
                else:
                    factor = amax**pa*bmax**pb*s**ps
                amount += float(np.linalg.norm(mat, 2)*factor)
            bounded[target] = amount
        delta_hh, bound_hl = bounded["hh"], bounded["lh"]
        worst_hh_delta = max(worst_hh_delta, delta_hh)
        worst_hl_bound = max(worst_hl_bound, bound_hl)
        local_lower = local_min0-delta_hh
        uniform_lower = min(uniform_lower, local_lower)
        if lo and local_lower > 0:
            uniform_schur = max(uniform_schur, bound_hl**2/local_lower)
        # Preserve the sign of the x^2 heavy-heavy coefficient instead of
        # bounding its whole norm as a potentially negative perturbation.
        hh0_drift = 0.0
        hh1_bound = 0.0
        hh2_drift = 0.0
        hh2_at_amin = np.zeros((len(hi), len(hi)), dtype=complex)
        for (pa, pb, ps), mat in grouped["hh"].items():
            norm2 = float(np.linalg.norm(mat, 2))
            if pb == 0:
                hh0_drift += norm2*(amax**pa-amin**pa)*s**ps
            elif pb == 1:
                hh1_bound += norm2*amax**pa*bmax*s**ps
            elif pb == 2:
                hh2_at_amin += mat*amin**pa*s**ps*(15/8)
                hh2_drift += norm2*(amax**pa-amin**pa)*s**ps*(15/8)
            else:
                raise AssertionError((label, pa, pb, ps))
        assert np.linalg.norm(hh2_at_amin-hh2_at_amin.conj().T) < 1e-9
        negative_hh2 = max(0.0, -float(np.linalg.eigvalsh(hh2_at_amin)[0]))
        local_sharp = (local_min0-hh0_drift-hh1_bound
                       -.1**2*(negative_hh2+hh2_drift))
        sharp_lower = min(sharp_lower, local_sharp)
        if lo and local_sharp > 0:
            sharp_schur = max(sharp_schur, bound_hl**2/local_sharp)
    print("TRIANGLE_OPERATOR_INTERVAL_BOUND", "min_heavy_at_x0", min0,
          "max_heavy_delta", worst_hh_delta, "uniform_lower", uniform_lower,
          "max_mixing_bound", worst_hl_bound,
          "max_schur_bound", uniform_schur if uniform_lower > 0 else None)
    print("SIGN_AWARE_INTERVAL_BOUND", "uniform_lower", sharp_lower,
          "max_schur_bound", sharp_schur if sharp_lower > 0 else None)
    for x in (0.0, .025, .05, .075, .1):
        a = stationary_omega(c, x*np.sqrt(60))/np.sqrt(60)
        b = x*np.sqrt(15/8)
        s = .1*np.sqrt(30)
        minimum = float("inf")
        largest_mixing = 0.0
        largest_schur = 0.0
        for label, coeff in blocks.items():
            h = endpoint_block(label, coeff, c, a, b, s)/60
            names = origins[label]
            hi = [i for i, name in enumerate(names) if name in ("126_k1", "126_k2")]
            lo = [i for i in range(len(names)) if i not in hi]
            if not hi:
                continue
            hhh = h[np.ix_(hi, hi)]
            eig = np.linalg.eigvalsh(hhh)
            minimum = min(minimum, float(eig[0]))
            if lo:
                hlh = h[np.ix_(lo, hi)]
                largest_mixing = max(largest_mixing, float(np.linalg.norm(hlh, 2)))
                schur = hlh@np.linalg.solve(hhh, hlh.conj().T)
                largest_schur = max(largest_schur, float(np.linalg.norm(schur, 2)))
        print("FIXED_COEFFICIENT_OFFSHELL_PATH", "x", x,
              "min_heavy_m2_over_omega2", minimum,
              "max_mixing_m2_over_omega2", largest_mixing,
              "max_schur_m2_over_omega2", largest_schur)
    print("CANDIDATE_SPLIT_DIAGNOSTIC_ONLY")


if __name__ == "__main__":
    main()
