"""Connected fieldwise-rephasing check for claimed smallness protection.

This check is confined to symmetries commuting with Spin(10) on one copy of
each scalar irrep. It does not classify discrete/nonlinear symmetries and
does not complete the unfrozen parent Yukawa sector.
"""

from pathlib import Path
import sys

import numpy as np
from sympy import Matrix

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_ps_threshold_kernel"))
from check_ps_mass_limit import fixed_couplings

CHI4 = (2, 0, 1)       # Sigma Sigma Phi S
CHI6 = (0, 2, -1)      # phi phi S*
ETA = (1, 1, 0)        # Sigma Sigma Sigma* phi
KAPPA = CHI6            # Phi phi phi S*
PQ = (1, -1, -2)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def main():
    c = fixed_couplings()
    assert abs(c["z4"]) > 0 and abs(c["zEta"]) > 0
    assert Matrix([CHI4, ETA]).rank() == 2
    assert dot(CHI4, PQ) == 0 and dot(ETA, PQ) == 0
    null = Matrix([CHI4, ETA]).nullspace()
    assert len(null) == 1
    assert Matrix.hstack(*null).columnspace()[0].cross(Matrix(PQ)) == Matrix.zeros(3, 1)
    # The physical point is even more constrained: z6 and zK are nonzero.
    assert abs(c["z6"]) > 0 and abs(c["zK"]) > 0
    assert Matrix([CHI4, CHI6, ETA, KAPPA]).rank() == 2
    # Nonzero self-interactions exclude a field-independent scalar shift.
    for name in ("lambdaPhi1", "lambdaPhi2", "lambdaSigma1",
                 "lambdaPhiphi1", "lambdaPhiphi2"):
        assert abs(c[name]) > 0, name
    print("SCALAR_CONNECTED_REPHASING_ONLY_PQ_PASS")
    print("NO_SEPARATE_CONTINUOUS_REPHASING_PROTECTS_10_OR_54_LIGHT_COMBINATIONS")
    print("DISCRETE_NONLINEAR_AND_FULL_YUKAWA_PROTECTION_UNRESOLVED")


if __name__ == "__main__":
    main()
