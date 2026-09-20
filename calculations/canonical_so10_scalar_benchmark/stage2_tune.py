"""Targeted one-light-doublet tuning from the verified Stage 1 point."""

from pathlib import Path
import json
import sys

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from define_generic_nullity_test import expected_block_ranks
from decompose_sm_tangent import dimension
from search import FREE, OMEGA, affine_matrices, load_blocks
from validate_candidate import kinetic_diag

DOUBLETS = ((0, 0, 1, -3), (0, 0, 1, 3))


def load_stage1():
    point = json.loads((HERE / "STAGE1_POINT.json").read_text())
    return np.asarray([float(point["free_coefficients"][n]) for n in FREE])


def physical_eigenvalues(label, free, affine, metric):
    h = np.einsum("j,jab->ab", free, affine[label])
    d = metric[label]
    h = h / np.sqrt(d[:, None]*d[None, :])
    return np.linalg.eigvalsh(h)


def replay(free, affine, metric):
    expected = expected_block_ranks()
    smallest = (float("inf"), None)
    colored = (float("inf"), None)
    max_zero = 0.0
    rank = 0
    for label in expected:
        eigenvalues = physical_eigenvalues(label, free, affine, metric)
        zeros = expected[label][1] + int(label in DOUBLETS)
        order = np.argsort(abs(eigenvalues))
        if zeros:
            max_zero = max(max_zero, float(max(abs(eigenvalues[order[:zeros]]))))
        remaining = eigenvalues[order[zeros:]]
        if len(remaining):
            low = float(min(remaining))
            if low < smallest[0]:
                smallest = low, label
            if (label[0] or label[1]) and low < colored[0]:
                colored = low, label
        rank += dimension(label)*int(np.sum(abs(remaining) > 1e-7))
    return smallest, colored, max_zero, rank


def main():
    x = y = 0.1
    affine = affine_matrices(load_blocks(), x, y)
    metric = {label: kinetic_diag(label, x, y) for label in affine}
    base = load_stage1()
    trials = (
        (0.05, 0.00, 0.00),
        (0.00, 0.05, 0.00),
        (0.05, 0.05, 0.00),
        (0.10, 0.10, 0.00),
        (0.20, 0.20, 0.00),
        (0.30, 0.30, 0.00),
        (0.30, 0.30, 0.01),
        (0.30, 0.30, 0.03),
        (0.30, 0.30, 0.05),
        (0.30, 0.30, 0.10),
        (0.30, 0.30, 0.30),
        (0.30, 0.30, 0.50),
        (0.10, 0.10, 0.01),
        (0.20, 0.20, 0.02),
        (0.05, -0.05, 0.00),
        (0.05, -0.05, 0.01),
        (0.10, -0.10, 0.02),
        (-0.10, 0.10, 0.02),
        (0.20, -0.20, 0.02),
        (-0.20, 0.20, 0.02),
        (0.30, -0.30, 0.03),
        (-0.30, 0.30, 0.03),
    )
    best = None
    for z6, zk, zeta in trials:
        free = base.copy()
        free[FREE.index("z6:re")] = z6
        free[FREE.index("zK:re")] = zk
        free[FREE.index("zEta:re")] = zeta
        mass_index = FREE.index("mphi2")

        def min_doublet(mass):
            free[mass_index] = mass
            return float(min(physical_eigenvalues(DOUBLETS[1], free, affine, metric)))

        lo, hi = min_doublet(-1), min_doublet(1)
        if not (lo < 0 < hi):
            print("NO_ROOT_BRACKET", z6, zk, zeta, lo, hi, flush=True)
            continue
        root = brentq(min_doublet, -1, 1, xtol=1e-14)
        free[mass_index] = root
        smallest, colored, zero, rank = replay(free, affine, metric)
        print("STAGE2_TRIAL", z6, zk, zeta, "mphi2", root,
              "min_other", smallest, "min_color", colored,
              "max_zero", zero, "rank", rank, flush=True)
        if (smallest[0] > 1e-6 and colored[0]/OMEGA**2 > 1e-4
                and zero < 1e-6 and rank == 290):
            if (best is None or colored[0] > best[0]+1e-8
                    or (abs(colored[0]-best[0]) <= 1e-8
                        and zeta > best[2][2])):
                best = (colored[0], free.copy(), (z6, zk, zeta))
            print("PRELIMINARY_STAGE2_SURVIVOR", z6, zk, zeta,
                  "colored_margin", colored[0], flush=True)
    if best is not None:
        np.savez_compressed(HERE / "generated_stage2_candidate.npz",
                            free=best[1], x=x, y=y)
        print("BEST_PRELIMINARY_STAGE2", best[2],
              "colored_margin", best[0], flush=True)


if __name__ == "__main__":
    main()
