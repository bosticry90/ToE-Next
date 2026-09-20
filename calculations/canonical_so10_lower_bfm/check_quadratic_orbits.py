"""Check the physical PS/SM orbit and partial-BFM R_zeta mass pairing.

This is a quadratic-operator check, not a one-loop F^2 matching calculation.
The normalized orbit map Q obeys M_V^2 = g_10^2 omega^2 Q^T Q.
The nonzero spectra of Q^T Q and Q Q^T coincide by singular-value
duality, giving the heavy-ghost and Goldstone gauge-fixing masses.
"""

from itertools import combinations
from pathlib import Path
import math
import sys

import numpy as np

CALC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CALC / "canonical_so10_vacuum_kernel"))
sys.path.insert(0, str(CALC / "canonical_so10_scalar_reconstruction"))
sys.path.insert(0, str(CALC / "canonical_so10_matrix_threshold"))

from derive_stabilizers import form_action, generators
from verify_eta1_doublet_mixing import vacuum_form
from check_vector_matrix_log import physical_vector_gram


def ps_orbit():
    """Return the dimensionless 604-by-21 orbit map for PS generators."""
    gens = generators()
    ps = [(pair, gen) for pair, gen in gens if (pair[0] < 6) == (pair[1] < 6)]
    assert len(gens) == 45 and len(ps) == 21
    phi = np.diag([-2.0] * 6 + [3.0] * 4)
    sigma = 0.1 * math.sqrt(15 / 8)
    form = vacuum_form()
    tuples = list(combinations(range(10), 5))
    columns = []
    for _, generator in ps:
        g = np.asarray(generator, dtype=float)
        ds = form_action(generator, form)
        sig = np.asarray([complex(*ds.get(k, (0, 0))) for k in tuples])
        columns.append(np.r_[((g @ phi) - (phi @ g)).reshape(-1),
                               sigma * sig.real, sigma * sig.imag])
    # Raw plane generators are normalized by sqrt(2); omega^2=60.
    return np.column_stack(columns) / math.sqrt(120), [pair for pair, _ in ps]


def main():
    q, pairs = ps_orbit()
    assert q.shape == (100 + 2 * 252, 21)
    gram = q.T @ q
    eigenvalues = np.linalg.eigvalsh(gram)
    assert np.count_nonzero(abs(eigenvalues) < 1e-12) == 12
    assert np.count_nonzero(abs(eigenvalues - 0.005) < 1e-12) == 8
    assert np.count_nonzero(abs(eigenvalues - 0.025) < 1e-12) == 1
    # Independently compare the PS principal submatrix of the separately
    # built full physical 45-adjoint vector Gram.
    all_pairs = [pair for pair, _ in generators()]
    positions = [all_pairs.index(pair) for pair in pairs]
    other_gram = physical_vector_gram(generators())
    assert np.max(abs(gram - other_gram[np.ix_(positions, positions)])) < 1e-12

    # In partial BFM R_zeta, heavy ghosts have zeta Q^TQ; Goldstones have
    # zeta QQ^T on the image of Q. Test their nonzero spectra independently
    # by SVD. The remaining zero modes are not heavy Goldstones/ghosts.
    singular = np.linalg.svd(q, compute_uv=False)
    singular_positive = np.sort((singular[singular > 1e-8]) ** 2)
    vector_positive = np.sort(eigenvalues[eigenvalues > 1e-8])
    assert len(singular_positive) == len(vector_positive) == 9
    assert np.max(abs(singular_positive - vector_positive)) < 1e-12
    for zeta in (0.5, 1.0, 2.5):
        ghost = np.sort(np.linalg.eigvalsh(zeta * gram)[-9:])
        goldstone = zeta * singular_positive
        assert np.max(abs(ghost - goldstone)) < 1e-12
    print("LOWER_BFM_QUADRATIC_ORBIT_PASS",
          "PS_generators=21", "SM_null=12", "broken=9",
          "vector_mass2_over_g2omega2={0.005:8,0.025:1}",
          "Goldstone_ghost_Rzeta_mass_pairing=PASS",
          "F2_matching_and_zeta_cancellation=NOT_DERIVED")


if __name__ == "__main__":
    main()
