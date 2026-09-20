"""Compile the frozen exact bilinear oracle into 35 linear coefficient blocks.

The output is a generated numeric cache, never a replacement for the exact
parent action. Each matrix entry is computed over Q(i) before float casting.
"""

from pathlib import Path
import sys

import numpy as np
from sympy import I, simplify

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))

from define_generic_nullity_test import expected_block_ranks
from evaluate_sm_hessian_blocks import rational_representatives, realified_representative
from parent_bilinear_oracle import REAL_NAMES, COMPLEX_NAMES, bilinear_coefficients

SLOTS = REAL_NAMES + tuple(n + ":re" for n in COMPLEX_NAMES) + tuple(
    n + ":im" for n in COMPLEX_NAMES)


def real_imag(z):
    return z.as_real_imag()


def entry_components(u, v):
    a, b = u.real, u.imag
    x, y = v.real, v.imag
    q1 = bilinear_coefficients(a, x)
    q2 = bilinear_coefficients(b, y)
    q3 = bilinear_coefficients(a, y)
    q4 = bilinear_coefficients(b, x)
    out = []
    for n in REAL_NAMES:
        out.append(simplify(q1[n] + q2[n] + I * (q3[n] - q4[n])))
    for part in ("re", "im"):
        for n in COMPLEX_NAMES:
            z1, z2, z3, z4 = (real_imag(q[n]) for q in (q1, q2, q3, q4))
            k = 0 if part == "re" else 1
            sign = 2 if k == 0 else -2
            out.append(simplify(sign * (z1[k] + z2[k] + I * (z3[k] - z4[k]))))
    return out


def compile_blocks():
    blocks = {}
    expected = expected_block_ranks()
    for label in sorted(expected):
        reps = rational_representatives()[label]
        tangents = [realified_representative(sector, obj)
                    for sector, _, obj in reps]
        m = len(tangents)
        coeff = np.zeros((len(SLOTS), m, m), dtype=np.complex128)
        for a in range(m):
            for b in range(m):
                values = entry_components(tangents[a], tangents[b])
                coeff[:, a, b] = [complex(v) for v in values]
        residue = float(np.max(np.abs(coeff - coeff.conj().transpose(0, 2, 1))))
        assert residue < 1e-10, (label, residue)
        blocks[label] = coeff
        print("COMPILED", label, "multiplicity", m, flush=True)
    return blocks


def main():
    blocks = compile_blocks()
    output = HERE / "generated_linear_blocks.npz"
    arrays = {"_".join(map(str, label)): value for label, value in blocks.items()}
    np.savez_compressed(output, **arrays)
    print("SAVED", output, "blocks", len(blocks), "slots", len(SLOTS))


if __name__ == "__main__":
    main()
