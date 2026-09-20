"""Finite, preregistered positive-quartic discovery grid (not a no-go scan)."""

import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq
from sympy import Rational, sqrt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "canonical_so10_scalar_benchmark"))
sys.path.insert(0, str(ROOT / "canonical_so10_light_higgs_quartic"))
sys.path.insert(0, str(ROOT / "canonical_so10_full_hessian"))

from evaluate_sm_hessian_blocks import rational_representatives, realified_representative
from replay_candidate_exact import exact_coefficients
from search import FREE, DEGREES, affine_matrices, load_blocks
from stage2_tune import DOUBLETS, replay
from validate_candidate import kinetic_diag
from compute import (
    Evaluator, add, build_hessian, canonical_norm2, heavy_basis, mp,
    mpval, rat, relaxed, scale,
)

TRIPLES = (
    (0, 0, .3), (0, 0, .1), (0, 0, .03),
    (0, .03, .3), (.03, 0, .3), (.03, .03, .3),
    (.1, 0, .3), (0, .1, .3), (.1, .1, .3),
    (.3, .3, .3),
)


def starting_data():
    point = json.loads((ROOT / "canonical_so10_scalar_benchmark" /
                        "STAGE1_POINT.json").read_text())
    base = np.array([float(point["free_coefficients"][n]) for n in FREE])
    affine = affine_matrices(load_blocks(), .1, .1)
    metric = {label: kinetic_diag(label, .1, .1) for label in affine}
    return base, affine, metric


def tune(base, affine, metric, triple):
    free = base.copy()
    for name, value in zip(("z6:re", "zK:re", "zEta:re"), triple):
        free[FREE.index(name)] = value
    mass_index = FREE.index("mphi2")
    label = DOUBLETS[0]

    def lowest(u):
        free[mass_index] = u
        h = np.einsum("j,jab->ab", free, affine[label])
        d = metric[label]
        return np.linalg.eigvalsh(h/np.sqrt(np.outer(d, d)))[0]

    if not (lowest(-1) < 0 < lowest(1)):
        return None
    free[mass_index] = brentq(lowest, -1, 1, xtol=1e-14)
    smallest, colored, zero, rank = replay(free, affine, metric)
    h = np.einsum("j,jab->ab", free, affine[label])
    d = metric[label]
    eig, vectors = np.linalg.eigh(h/np.sqrt(np.outer(d, d)))
    mix = float(sum(abs(vectors[j, 0])**2 for j in (0, 1)))
    return free, smallest, colored, zero, rank, mix, eig, vectors


def coefficients(free):
    effective, b, s = exact_coefficients()
    c = dict(effective)
    u = Rational(str(free[FREE.index("mphi2")]))
    c["mphi2"] = 60*u
    c["z6"] = Rational(str(free[FREE.index("z6:re")]))*sqrt(60)*s
    c["zK"] = Rational(str(free[FREE.index("zK:re")]))*s
    c["zEta"] = Rational(str(free[FREE.index("zEta:re")]))*b**3
    c["lambdaPhiphi1"] = Rational(str(free[FREE.index("lambdaPhiphi1")]))
    c["lambdaPhiphi2"] = Rational(str(free[FREE.index("lambdaPhiphi2")]))
    for name in ("lambdaPhiVector1", "lambdaPhiVector2"):
        c[name] = Rational(str(free[FREE.index(name)]))
    return {name: mpval(value) for name, value in c.items()}, mpval(b).real, mpval(s).real


def light_state(eigvec, metric, digits=13):
    reps = rational_representatives()[DOUBLETS[0]]
    states = []
    for z, g, (sector, _, obj) in zip(eigvec, metric, reps):
        tangent = realified_representative(sector, obj)
        c = z/np.sqrt(g)
        states.append(add(scale(tangent.real, rat(c.real, digits)),
                          scale(tangent.imag, -rat(c.imag, digits))))
    return add(*states)


def main():
    base, affine, metric = starting_data()
    heavy = heavy_basis()
    heavy_matrices = None
    evaluated = 0
    for triple in TRIPLES:
        result = tune(base, affine, metric, triple)
        if result is None:
            print("NO_BRACKET", triple, flush=True)
            continue
        free, smallest, colored, zero, rank, mix, eig, vectors = result
        print("QUADRATIC", triple, "u", free[FREE.index("mphi2")],
              "min_other", smallest, "min_colored", colored,
              "zero", zero, "rank", rank, "126_fraction", mix,
              flush=True)
        if not (smallest[0] >= .02 and colored[0] >= .006 and
                zero < 1e-7 and rank == 290 and mix > 1e-6):
            continue
        for pure in (.1, .5, 1.0):
            if evaluated >= 12:
                print("PARENT_EVALUATION_BUDGET_EXHAUSTED", flush=True)
                return
            trial = free.copy()
            for name in ("lambdaPhiVector1", "lambdaPhiVector2"):
                trial[FREE.index(name)] = pure
            c, b, s = coefficients(trial)
            evaluator = Evaluator(c)
            if heavy_matrices is None:
                heavy_matrices = build_hessian(evaluator, heavy)
            h = light_state(vectors[:, 0], metric[DOUBLETS[0]])
            direct, correction, eff, _, _ = relaxed(
                evaluator, h, heavy, heavy_matrices)
            norm = canonical_norm2(h, b, s)
            lam_direct = 4*direct/norm**2
            lam_singlet = 4*correction/norm**2
            lam = 4*eff/norm**2
            evaluated += 1
            print("QUARTIC_TRIAL", triple, "pure", pure,
                  "direct", mp.nstr(lam_direct, 16),
                  "subtraction", mp.nstr(lam_singlet, 16),
                  "effective", mp.nstr(lam, 20),
                  "parent_evaluations", evaluator.calls, flush=True)
            if lam >= mp.mpf("0.05"):
                print("PRELIMINARY_POSITIVE_SURVIVOR", triple, "pure", pure,
                      "u", free[FREE.index("mphi2")], flush=True)
                return
            # The direct quartic varies monotonically with the positive
            # pure-10_H coefficients; keep the same determinant tuning.
    print("GRID_ENDED_WITHOUT_POSITIVE_SURVIVOR", flush=True)


if __name__ == "__main__":
    main()
