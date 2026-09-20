"""Exact gauge-vector recombination in PS and Spin(10) restoration limits."""

from itertools import combinations
from pathlib import Path
import sys

from sympy import Matrix, zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_vacuum_kernel"))
from derive_stabilizers import generators


def main():
    phi = Matrix.diag(*([-2]*6+[3]*4))
    columns = []
    for (i, j), g in generators():
        dp = g*phi-phi*g
        if (i < 6) == (j < 6):
            assert dp == zeros(10)
        else:
            assert sum(z*z for z in dp) == 50
        columns.append(Matrix(list(dp)))
    gram = Matrix.hstack(*columns).T*Matrix.hstack(*columns)
    assert gram.rank() == 24
    assert gram*gram == 50*gram
    assert gram.trace() == 24*50
    # With both gauge-breaking VEVs zero, every gauge orbit column is zero.
    assert all(g*zeros(10)-zeros(10)*g == zeros(10)
               for _, g in generators())
    print("VECTOR_RECOMBINATION_PASS", "sigma0: 21 zero +24 at Gram50;",
          "Phi0Sigma0: 45 zero")


if __name__ == "__main__":
    main()
