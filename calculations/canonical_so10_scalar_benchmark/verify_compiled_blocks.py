"""Regression checks for the generated affine block cache."""

import numpy as np

from compile_numeric_blocks import SLOTS
from search import FREE, effective_slot_vector, load_blocks

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "canonical_so10_full_hessian"))
from define_generic_nullity_test import exact_stationary_witness, expected_block_ranks
from decompose_sm_tangent import dimension
from evaluate_sm_hessian_blocks import block


def main():
    blocks = load_blocks()
    witness = exact_stationary_witness()
    slot_values = np.asarray([float(complex(witness[name]).real)
        if not part else float(complex(witness[name]).real if part == "re"
                               else complex(witness[name]).imag)
        for slot in SLOTS for name, _, part in (slot.partition(":"),)])
    x = (4*np.sqrt(2))/np.sqrt(60)
    y = np.sqrt(2)/np.sqrt(60)
    free = []
    for name in FREE:
        base, _, part = name.partition(":")
        z = complex(witness[base])
        value = z.real if part in ("", "re") else z.imag
        if base == "mphi2":
            value /= 60
        elif base in ("muPhi", "muPhiPhi", "z6"):
            value /= np.sqrt(60)
        free.append(value)
    recovered = effective_slot_vector(free, x, y)
    assert np.allclose(slot_values, recovered, rtol=1e-13, atol=1e-12)
    expected = expected_block_ranks()
    real_rank = 0
    for label, coeff in blocks.items():
        h = np.einsum("s,sab->ab", slot_values, coeff)
        assert np.max(abs(h-h.conj().T)) < 1e-8
        rank = np.linalg.matrix_rank(h, tol=1e-7)
        assert rank == expected[label][2], (label, rank, expected[label])
        real_rank += dimension(label)*rank
    assert real_rank == 294
    for label in ((0, 0, 0, 0), (0, 0, 1, 3), (1, 0, 1, 5)):
        h = np.einsum("s,sab->ab", slot_values, blocks[label])
        exact = np.array(block(label, witness)).astype(np.complex128)
        assert np.allclose(h, exact, rtol=1e-12, atol=1e-8), label
    print("COMPILED_BLOCKS_REPLAY_PASS real_rank=294; direct exact blocks agree")


if __name__ == "__main__":
    main()
