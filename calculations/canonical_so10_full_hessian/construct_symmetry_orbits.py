"""Explicit real gauge/PQ tangent vectors on the frozen vacuum ansatz.

Uses unnormalized nonzero VEV amplitudes (Phi=diag(-2x6,+3x4), Sigma=V,
S=1), which is sufficient to certify orbit independence. The normalized
factors in RECORD.md must be restored before Hessian multiplication.
"""

import sys
from itertools import combinations
from pathlib import Path

from sympy import Matrix, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_vacuum_kernel"))
from derive_stabilizers import form_action, generators

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from verify_eta1_doublet_mixing import vacuum_form


INDEX5 = tuple(combinations(range(10), 5))


def column(phi_change, sigma_change, s_imag=0):
    # Ambient 100+252+252+2 real coordinates retain redundant Phi and
    # Sigma entries, but injectively represent every physical tangent.
    return Matrix(list(phi_change) +
                  [sigma_change.get(idx, (0, 0))[0] for idx in INDEX5] +
                  [sigma_change.get(idx, (0, 0))[1] for idx in INDEX5] +
                  [0, s_imag])


def main():
    phi = Matrix.diag(*([-2]*6 + [3]*4))
    v = vacuum_form()
    gauge = [column(g*phi-phi*g, form_action(g, v))
             for _, g in generators()]
    gmat = Matrix.hstack(*gauge)
    _, pivots = gmat.rref()
    assert len(pivots) == 33
    pq_sigma = {idx: (-2*z[1], 2*z[0]) for idx, z in v.items()}
    pq = column(zeros(10), pq_sigma, -4)
    assert Matrix.hstack(gmat, pq).rank() == 34
    # The singlet coordinate makes PQ independent of every gauge orbit.
    assert all(col[-1] == 0 for col in gauge) and pq[-1] == -4
    print("EXPLICIT_REAL_ORBITS_PASS gauge rank=33, gauge+PQ rank=34")
    print("independent broken-generator indices:", pivots)
    print("ambient coordinate length:", gmat.rows,
          "(injective redundant tensor coordinates; physical tangent=328)")


if __name__ == "__main__":
    main()
