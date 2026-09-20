"""Fail-fast exact block-rank test at the frozen stationary witness.

Each H_R is B_C(conj(e_R,a),e_R,b). The real tangent complexifies as
the direct sum of these irrep spaces; a non-self-conjugate pair R,Rbar
contributes both complex ranks to the dimension-weighted real rank.
No positivity or physical vacuum claim follows from rank.
"""

from sympy import Matrix, simplify, zeros

from define_generic_nullity_test import expected_block_ranks
from evaluate_sm_hessian_blocks import block, orbit_coefficients, pq_coefficients


def conjugate_label(label):
    p, q, n, y6 = label
    return q, p, n, -y6


def ordered_labels(expected):
    # Fail first on gauge nullity, then Higgs doublets, then the rest.
    goldstone = [r for r, (_, k, _) in expected.items()
                 if k and r != (0, 0, 0, 0)]
    doublets = [(0, 0, 1, -3), (0, 0, 1, 3)]
    neutral = [(0, 0, 0, 0)]
    initial = goldstone+neutral+doublets
    return initial+[r for r in sorted(expected) if r not in initial]


def main():
    expected = expected_block_ranks()
    ranks = {}
    for label in ordered_labels(expected):
        m, required_nullity, target_rank = expected[label]
        h = block(label)
        assert h.shape == (m, m)
        if label == (0, 0, 0, 0):
            gauge_orbits = orbit_coefficients(label)
            assert gauge_orbits
            assert Matrix.hstack(*gauge_orbits).rank() == 1
            pq = pq_coefficients()
            assert all((h*g).applyfunc(simplify) == zeros(m, 1)
                       for g in gauge_orbits)
            assert (h*pq).applyfunc(simplify) == zeros(m, 1)
            assert Matrix.hstack(*gauge_orbits, pq).rank() == 2
        if required_nullity and label != (0, 0, 0, 0):
            orbits = orbit_coefficients(label)
            assert len(orbits) == required_nullity, (label, len(orbits))
            for g in orbits:
                assert (h*g).applyfunc(simplify) == zeros(m, 1), (
                    label, "H*g", h*g)
        rank = h.rank()
        assert rank == target_rank, (label, "rank", rank, target_rank, h)
        ranks[label] = rank
        print("BLOCK_PASS", label, "multiplicity", m,
              "rank", rank, "nullity", m-rank, flush=True)
    assert all(ranks[r] == ranks[conjugate_label(r)] for r in ranks)
    from decompose_sm_tangent import dimension
    real_rank = sum(dimension(r)*rank for r, rank in ranks.items())
    assert real_rank == 294
    print("FULL_EXACT_STATIONARY_WITNESS_RANK_PASS real_rank=294 nullity=34")


if __name__ == "__main__":
    main()
