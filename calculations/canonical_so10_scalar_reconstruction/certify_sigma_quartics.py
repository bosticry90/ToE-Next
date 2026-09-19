"""Exact rank test for four Sym²(126) x Sym²(bar126) scalar quartics.

P_k[I,J] = sum_K Sigma[K,I] Sigma[K,J] for k contracted indices.
Q_k = sum_(I,J) |P_k[I,J]|² is SO(10)-invariant. The separate D5
character count proves the entire field multiset has multiplicity four.
All coefficients and ranks here are integers/Gaussian integers.
"""

from itertools import combinations
from random import Random
from fractions import Fraction

from sympy import Matrix

from test_eta1_invariant import add, mul, parity, selfdual_form
from verify_eta1_doublet_mixing import doublet_form, vacuum_form


def add_forms(a, b):
    out = dict(a)
    for idx, z in b.items():
        out[idx] = add(out.get(idx, (0, 0)), z)
    return {idx: z for idx, z in out.items() if z != (0, 0)}


def generated_form(seed, terms):
    rng = Random(seed)
    left = tuple(idx for idx in combinations(range(10), 5)
                 if idx < tuple(i for i in range(10) if i not in idx))
    out = {}
    for idx in rng.sample(left, terms):
        z = (rng.choice((-2, -1, 1, 2)), rng.choice((-2, -1, 0, 1, 2)))
        other = tuple(i for i in range(10) if i not in idx)
        sign = parity(idx + other)
        out[idx] = z
        out[other] = (sign*z[1], -sign*z[0])
    return out


def paired_tensor(form, k):
    out = {}
    items = tuple(form.items())
    for (ia, za) in items:
        set_a = set(ia)
        for (ib, zb) in items:
            overlap = tuple(i for i in ia if i in ib)
            for shared in combinations(overlap, k):
                rem_a = tuple(i for i in ia if i not in shared)
                rem_b = tuple(i for i in ib if i not in shared)
                sign = parity(shared + rem_a) * parity(shared + rem_b)
                val = mul(za, zb)
                val = (sign*val[0], sign*val[1])
                key = (rem_a, rem_b)
                out[key] = add(out.get(key, (0, 0)), val)
    return {key: z for key, z in out.items() if z != (0, 0)}


def quartics(form):
    tensors = [paired_tensor(form, k) for k in range(5)]
    norms = tuple(sum(a*a+b*b for a, b in tensor.values()) for tensor in tensors)
    norm = sum(a*a+b*b for a, b in form.values())
    assert norms[0] == norm*norm
    return norms + (cross_contraction(tensors[1], 3, 1),
                    cross_contraction(tensors[1], 2, 2))


def cross_contraction(paired, y, z):
    """Delta graph AB=CD=1, AC=BD=y, AD=BC=z (y+z=4)."""
    assert y + z == 4
    result = (0, 0)
    for (ia, ib), za in paired.items():
        for ac in combinations(ia, y):
            ad = tuple(i for i in ia if i not in ac)
            sign_a = parity(ac + ad)
            for bc in combinations(ib, z):
                bd = tuple(i for i in ib if i not in bc)
                sign_b = parity(bc + bd)
                raw_c = ac + bc
                raw_d = ad + bd
                if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                    continue
                ibar_c, ibar_d = tuple(sorted(raw_c)), tuple(sorted(raw_d))
                zb = paired.get((ibar_c, ibar_d), (0, 0))
                if zb == (0, 0):
                    continue
                sign = sign_a * sign_b * parity(raw_c) * parity(raw_d)
                value = mul(za, (zb[0], -zb[1]))
                result = add(result, (sign*value[0], sign*value[1]))
    assert result[1] == 0
    return result[0]


def permute_form(form):
    # Two axis swaps have determinant +1 and preserve Hodge chirality.
    permutation = (1, 0, 3, 2, 4, 5, 6, 7, 8, 9)
    out = {}
    for idx, z in form.items():
        moved = tuple(permutation[i] for i in idx)
        sign = parity(moved)
        out[tuple(sorted(moved))] = (sign*z[0], sign*z[1])
    return out


def rotate_form(form):
    # Exact nontrivial SO(2) rotation in the 0-1 plane (cos=3/5,sin=4/5).
    out = {}
    c, s = Fraction(3, 5), Fraction(4, 5)
    for idx, z in form.items():
        if 0 in idx and 1 not in idx:
            choices = ((idx, c), (tuple(1 if i == 0 else i for i in idx), s))
        elif 1 in idx and 0 not in idx:
            choices = ((tuple(0 if i == 1 else i for i in idx), -s), (idx, c))
        else:
            choices = ((idx, Fraction(1)),)
        for moved, factor in choices:
            sign = parity(moved)
            key = tuple(sorted(moved))
            scaled = (factor*sign*z[0], factor*sign*z[1])
            out[key] = add(out.get(key, (0, 0)), scaled)
    return {key: z for key, z in out.items() if z != (0, 0)}


def main():
    samples = [vacuum_form(), doublet_form(6),
               add_forms(vacuum_form(), doublet_form(6)), selfdual_form()]
    samples += [generated_form(seed, 8 + seed % 7) for seed in range(1, 9)]
    values = [quartics(f) for f in samples]
    for form, row in zip(samples[:4], values[:4]):
        assert quartics(permute_form(form)) == row
    assert quartics(rotate_form(samples[4])) == values[4]
    matrix = Matrix(values)
    rank = matrix.rank()
    print("Q_k k=0..4 plus crossed delta graphs (1,3,1),(1,2,2); rank=", rank)
    for row in values:
        print(row)
    assert rank <= 4, "representation upper bound violated: implementation error"
    if rank == 4:
        _, pivots = matrix.rref()
        minor = matrix[:4, [0, 1, 2, 5]].det()
        assert minor == -1680479354880
        print("four-by-four exact certificate det=", minor)
        print("FOUR_SIGMA_QUARTICS_CERTIFIED", pivots)
    else:
        print("SIGMA_QUARTIC_RANK_UNRESOLVED", rank)


if __name__ == "__main__":
    main()
