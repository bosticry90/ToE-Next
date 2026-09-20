"""Exact-source quadratic search along the transparent post-pilot shift path."""

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "canonical_so10_light_higgs_quartic"))

from explore import starting_data, tune, coefficients, light_state
from compute import (
    Evaluator, build_hessian, canonical_norm2, heavy_basis,
    mp, mpval, relaxed,
)
from parent_bilinear_oracle import vacuum_state
from search import FREE

TRIPLE = (.03, .03, .3)
BASE_MIXED = mp.mpf("0.19204517")


def pinverse(H):
    eig, U = mp.eigsy(H)
    inv = mp.matrix(H.rows)
    for k, value in enumerate(eig):
        if abs(value) < mp.mpf("1e-40"):
            continue
        assert value > 0
        for i in range(H.rows):
            for j in range(H.rows):
                inv[i, j] += U[i, k]*U[j, k]/value
    return inv


def scalar(x):
    return x[0] if isinstance(x, mp.matrix) else x


def main():
    base, affine, metric = starting_data()
    result = tune(base, affine, metric, TRIPLE)
    assert result is not None
    free, smallest, colored, zero, rank, mix, eig, vectors = result
    assert smallest[0] > .02 and colored[0] > .006 and rank == 290
    assert zero < 1e-7 and mix > 1e-6
    u_base = mp.mpf(str(free[FREE.index("mphi2")]))
    c, b, s = coefficients(free)
    evaluator = Evaluator(c)
    groups = heavy_basis()
    H = build_hessian(evaluator, groups)
    h = light_state(vectors[:, 0], metric[(0, 0, 1, -3)], 15)
    norm = canonical_norm2(h, b, s)
    j = [mp.matrix([evaluator.source(h, x) for x in group])
         for group in groups]
    inv = [pinverse(m) for m in H]
    # I_mix = tr(Phi^2) phi†phi. At phi0=0, its h^2 X coefficient
    # is 2 tr(Phi0 X_Phi) (phi_h†phi_h), so only the Phi singlet is sourced.
    phi_norm = sum(mpval(z.conjugate()*z).real for z in h.phi)
    phi0 = vacuum_state().Phi
    x0 = groups[0][0].Phi
    first = 2*mpval((phi0*x0).trace()).real*phi_norm
    j1 = mp.matrix([first, 0, 0, 0, 0])
    unit = {name: mp.mpf(0) for name in c}
    unit["lambdaPhiphi1"] = mp.mpf(1)
    direct_source = Evaluator(unit).source(h, groups[0][0])
    assert abs(first-direct_source) < mp.mpf("1e-25"), (first, direct_source)
    a = scalar(j1.T*inv[0]*j1)
    cross = scalar(j1.T*inv[0]*j[0])
    delta_opt = -cross/a
    delta_lo = max(-1-BASE_MIXED, u_base-1)
    delta_hi = min(1-BASE_MIXED, u_base+1)
    delta = min(max(delta_opt, delta_lo), delta_hi)
    print("ANALYTIC_SOURCE", "j1", mp.nstr(first, 25),
          "quadratic_curvature", mp.nstr(a, 25),
          "delta_opt", mp.nstr(delta_opt, 25),
          "allowed_delta", (mp.nstr(delta_lo, 16), mp.nstr(delta_hi, 16)),
          "selected_delta", mp.nstr(delta, 25), flush=True)
    assert delta_lo <= delta <= delta_hi

    def correction_at(d):
        total = mp.mpf(0)
        for k in range(3):
            source = j[k]+(d*j1 if k == 0 else mp.matrix(len(j[k]), 1))
            total += scalar(source.T*inv[k]*source)/2
        return total

    direct01 = evaluator.direct4(h)
    source01 = correction_at(delta)
    for pure in (.1, .5, 1):
        if pure == .1:
            direct = direct01
        else:
            free_pure = free.copy()
            for name in ("lambdaPhiVector1", "lambdaPhiVector2"):
                free_pure[FREE.index(name)] = pure
            c_pure, _, _ = coefficients(free_pure)
            direct = Evaluator(c_pure).direct4(h)
        lam = 4*(direct-source01)/norm**2
        print("ANALYTIC_TUNED_QUARTIC", "pure", pure,
              "direct", mp.nstr(4*direct/norm**2, 25),
              "subtraction", mp.nstr(4*source01/norm**2, 25),
              "effective", mp.nstr(lam, 25), flush=True)
        if lam >= mp.mpf("0.05"):
            print("PRELIMINARY_POSITIVE_SURVIVOR",
                  "mixed", mp.nstr(BASE_MIXED+delta, 30),
                  "u", mp.nstr(u_base-delta, 30),
                  "pure", pure, "z", TRIPLE, flush=True)
            # Re-evaluate every cubic source from the modified parent action,
            # without using the analytic j0+delta*j1 prediction.
            selected = free.copy()
            selected[FREE.index("lambdaPhiphi1")] = float(BASE_MIXED+delta)
            selected[FREE.index("mphi2")] = float(u_base-delta)
            for name in ("lambdaPhiVector1", "lambdaPhiVector2"):
                selected[FREE.index(name)] = pure
            c_replay, _, _ = coefficients(selected)
            replay = Evaluator(c_replay)
            d2, corr2, eff2, _, _ = relaxed(replay, h, groups, H)
            lam2 = 4*eff2/norm**2
            assert abs(lam2-lam) < mp.mpf("1e-8")
            print("DIRECT_PARENT_REPLAY", mp.nstr(lam2, 30),
                  "calls", replay.calls, flush=True)
            return
    print("NO_POSITIVE_ON_MIXED_SHIFT_PATH", flush=True)


if __name__ == "__main__":
    main()
