"""Exact self-dual-126 wedge identity and pure-sector quartic bound."""

from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_reconstruction"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_benchmark"))
from certify_sigma_quartics import (
    cross_contraction, generated_form, paired_tensor, parity,
)
from replay_candidate_exact import exact_coefficients


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def mul(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def selfdual_basis():
    universe = tuple(range(10))
    result = []
    for indices in combinations(universe, 5):
        complement = tuple(i for i in universe if i not in indices)
        if indices < complement:
            # *Sigma = +i Sigma in the frozen convention.
            result.append({indices: (1, 0),
                           complement: (0, -parity(indices+complement))})
    assert len(result) == 126
    return result


def contracted_wedge(a, b):
    """The 8-form sum_i (interior_i a) wedge (interior_i b)."""
    out = {}
    for ia, za in a.items():
        for ib, zb in b.items():
            shared = set(ia) & set(ib)
            if len(shared) != 1:
                continue
            i = next(iter(shared))
            ra = tuple(j for j in ia if j != i)
            rb = tuple(j for j in ib if j != i)
            ordered = ra + rb
            key = tuple(sorted(ordered))
            sign = (-1)**(ia.index(i)+ib.index(i))*parity(ordered)
            z = mul(za, zb)
            out[key] = add(out.get(key, (0, 0)), (sign*z[0], sign*z[1]))
    return {k: v for k, v in out.items() if v != (0, 0)}


def casimir(partition, n=10):
    return sum(length*(length+n+1-2*i)
               for i, length in enumerate(partition, start=1))


def gl_dimension(partition, n=10):
    dimension = Fraction(1)
    for i, row in enumerate(partition):
        for j in range(row):
            hook = row-j+sum(1 for lower in partition[i+1:] if lower > j)
            dimension *= Fraction(n+j-i, hook)
    assert dimension.denominator == 1
    return int(dimension)


def exchange_casimir(p):
    """Independent E_ji (x) E_ij action on Lambda^4 (x) Lambda^4."""
    out = {}
    for (a, b), z in p.items():
        for pos_i, i in enumerate(a):
            for pos_j, j in enumerate(b):
                ra = a[:pos_i]+a[pos_i+1:]
                rb = b[:pos_j]+b[pos_j+1:]
                if j in ra or i in rb:
                    continue
                ca, cb = (j,)+ra, (i,)+rb
                sign = (-1)**(pos_i+pos_j)*parity(ca)*parity(cb)
                key = tuple(sorted(ca)), tuple(sorted(cb))
                out[key] = add(out.get(key, (0, 0)),
                               (sign*z[0], sign*z[1]))
    return out


def inner(p, q):
    return sum(z[0]*q.get(key, (0, 0))[0]
               +z[1]*q.get(key, (0, 0))[1]
               for key, z in p.items())


def main():
    basis = selfdual_basis()
    pairs = 0
    for i, a in enumerate(basis):
        for b in basis[i:]:
            # W is symmetric in a,b since the contracted forms are 4-forms.
            assert not contracted_wedge(a, b), (i, pairs)
            pairs += 1
    assert pairs == 126*127//2
    # Sym^2(Lambda^4 C^10) has LR partitions (1^8), (2^2,1^4),
    # (2^4). The exchange-Casimir operator on these acts as below.
    c4 = casimir([1]*4)
    eigenvalues = []
    dimensions = []
    for k in (0, 2, 4):
        shape = [2]*k+[1]*(8-2*k)
        eigenvalues.append((casimir(shape)-2*c4)//2)
        dimensions.append(gl_dimension(shape))
    assert eigenvalues == [-16, -2, 4]
    assert dimensions == [45, 8250, 13860]
    assert sum(dimensions) == comb(10, 4)*(comb(10, 4)+1)//2
    a = (0, 1, 2, 3)
    p_high = {(a, a): (1, 0)}
    assert exchange_casimir(p_high) == {(a, a): (4, 0)}
    u = tuple(range(8))
    p_wedge = {}
    for left in combinations(u, 4):
        right = tuple(i for i in u if i not in left)
        p_wedge[left, right] = (parity(left+right), 0)
    assert {key: z for key, z in exchange_casimir(p_wedge).items()
            if z != (0, 0)} == {
                key: (-16*z[0], -16*z[1]) for key, z in p_wedge.items()}
    for seed in (1, 2, 3):
        p = paired_tensor(generated_form(seed, 5+seed), 1)
        assert inner(p, exchange_casimir(p)) == cross_contraction(p, 3, 1)
    # The exact contracted-wedge identity removes the (1^8) component.
    # Hence crossed X131 >= -2 Q1 for every self-dual Sigma.
    c, _, _ = exact_coefficients()
    residual = c["lambdaSigma2"]-2*c["lambdaSigma4"]
    assert c["lambdaSigma1"] > 0 and residual > 0 and c["lambdaSigma3"] > 0
    # The positive-Higgs point changes this mixed coefficient from Stage 1.
    from sympy import Rational
    a = c["lambdaPhi1"]+c["lambdaPhi2"]/10
    b = c["lambdaPhiVector1"]
    cross = -Rational(1, 500)
    assert c["lambdaPhiVector2"] >= 0 and c["lambdaPhiphi2"] >= 0
    assert a > 0 and b > 0 and 4*a*b > cross**2
    print("SELFDUAL_WEDGE_ZERO", pairs, "polarized_basis_pairs", flush=True)
    print("SYMMETRIC_EXCHANGE_EIGENVALUES", eigenvalues, flush=True)
    print("PURE_SIGMA_CERTIFIED", "X131>=-2*Q1",
          "lambdaSigma1", c["lambdaSigma1"],
          "lambdaSigma2_minus_2lambdaSigma4", residual,
          "lambdaSigma3", c["lambdaSigma3"], flush=True)
    print("PHI_PLUS_PHI_VECTOR_CERTIFIED", "quartic_lower_matrix_det",
          a*b-cross**2/4, flush=True)


if __name__ == "__main__":
    main()
