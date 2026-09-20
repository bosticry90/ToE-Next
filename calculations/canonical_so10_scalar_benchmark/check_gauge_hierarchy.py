"""Gauge-orbit kinetic Gram spectrum at a declared VEV ratio.

The common gauge coupling and common generator normalization cancel in the
heavy/intermediate mass ratio. This is a breaking-hierarchy control, not a
threshold or gauge-running calculation.
"""

from itertools import combinations
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_vacuum_kernel"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_reconstruction"))
from derive_stabilizers import generators, form_action
from verify_eta1_doublet_mixing import vacuum_form


def spectrum(x):
    b = x*np.sqrt(15/8)
    phi = np.diag([-2.0]*6+[3.0]*4)
    form = vacuum_form()
    indices = list(combinations(range(10), 5))
    columns = []
    for _, gen in generators():
        g = np.asarray(gen, dtype=float)
        dp = (g@phi-phi@g).reshape(-1)
        ds = form_action(gen, form)
        sig = np.asarray([complex(*(ds.get(k, (0, 0)))) for k in indices])
        columns.append(np.r_[dp, b*sig.real, b*sig.imag])
    c = np.column_stack(columns)
    gram = c.T@c
    vals = np.linalg.eigvalsh(gram)
    assert np.sum(abs(vals) < 1e-8) == 12, vals
    positive = vals[12:]
    return positive[:9], positive[9:], vals


def main():
    low, high, _ = spectrum(0.1)
    print("GAUGE_HIERARCHY x=0.1", "intermediate_count", len(low),
          "heavy_count", len(high),
          "max_intermediate_over_min_heavy_m2", max(low)/min(high),
          "min_heavy_over_max_intermediate_mass", np.sqrt(min(high)/max(low)))
    assert max(low) < min(high)


if __name__ == "__main__":
    main()
