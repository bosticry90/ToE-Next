"""Direct-parent independent Hessian spot checks at the PS-symmetric limit.

This deliberately calls the 29 invariant definitions, not the affine SM
Hessian cache. A fixed-coupling Sigma=0 background need not be stationary;
negative common PS multiplet masses are allowed in this limit check.
"""

from pathlib import Path
import sys

from sympy import I, Matrix, zeros, sqrt

HERE = Path(__file__).resolve().parent
FULL = HERE.parent / "canonical_so10_full_hessian"
sys.path.insert(0, str(FULL))

from parent_bilinear_oracle import (
    REAL_NAMES, COMPLEX_NAMES, State, invariant_values, state_add,
)
from compile_sm_multiplicity_representatives import projected
from check_ps_mass_limit import fixed_couplings


def scale_state(a, k):
    return State(k*a.Phi,
                 {key: (k*z[0], k*z[1]) for key, z in a.Sigma.items()},
                 tuple(k*z for z in a.phi), k*a.S)


def potential(a, c):
    iv = invariant_values(a)
    value = sum(c[n]*iv[n] for n in REAL_NAMES)
    value += sum(2*(c[n]*iv[n]).as_real_imag()[0]
                 if hasattr(c[n]*iv[n], "as_real_imag") else
                 2*(c[n]*complex(iv[n])).real for n in COMPLEX_NAMES)
    return complex(value).real


def curvature(base, direction, c, metric):
    v0 = potential(base, c)
    pair1 = (potential(state_add(base, direction), c)
             +potential(state_add(base, scale_state(direction, -1)), c)
             -2*v0)
    pair2 = (potential(state_add(base, scale_state(direction, 2)), c)
             +potential(state_add(base, scale_state(direction, -2)), c)
             -2*v0)
    # The parent potential is quartic: eliminate the finite-step t^4 term.
    hessian = (16*pair1-pair2)/12
    return hessian/metric/60


def base_state():
    return State(Matrix.diag(*([-2]*6+[3]*4)), {}, (0,)*10, sqrt(30)/10)


def phi_vector(index, imag=False):
    x = [0]*10
    x[index] = I if imag else 1
    return State(zeros(10), {}, tuple(x), 0)


def phi_54(i, j, offdiag=False):
    x = zeros(10)
    if offdiag:
        x[i, j] = x[j, i] = 1
    else:
        x[i, i], x[j, j] = 1, -1
    return State(x, {}, (0,)*10, 0)


def sigma_middle():
    # One normalized self-dual five-form direction in the k=3 sector.
    f = projected({(0, 1, 2, 6, 7): 2}, I)
    form = {key: tuple(z.as_real_imag()) for key, z in f.items()}
    assert len(form) == 2
    return State(zeros(10), form, (0,)*10, 0), 2


def main():
    c = fixed_couplings()
    base = base_state()
    tests = [
        ("54_20prime", phi_54(0, 1), 2, 0.0252958473015),
        ("54_9", phi_54(6, 7), 2, 0.0254020393319),
        ("54_24", phi_54(0, 6, True), 2, 0.00000062665),
        ("10_6_real", phi_vector(0), 2, 0.0107736024439),
        ("10_6_imag", phi_vector(0, True), 2, 0.00447921129969),
        ("10_4_real", phi_vector(6), 2, 0.0125731459545),
        ("10_4_imag", phi_vector(6, True), 2, 0.000801529235218),
    ]
    sig, gsig = sigma_middle()
    tests.append(("126_middle", sig, gsig, -0.0249635944))
    for name, direction, metric, expected in tests:
        actual = curvature(base, direction, c, metric)
        assert abs(actual-expected) < 2e-9, (name, actual, expected)
        print(name, actual)
    print("DIRECT_PARENT_PS_LIMIT_SPOT_REPLAY_PASS", len(tests))


if __name__ == "__main__":
    main()
