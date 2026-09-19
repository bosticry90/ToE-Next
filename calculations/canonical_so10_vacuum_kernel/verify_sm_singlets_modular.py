"""Exact finite-field lower bound for SM-invariant 126 directions.

At p=101, i maps to 10 because 10²=-1 mod 101. Rank mod p is a lower
bound on the Q(i) rank. The known singlet V gives one exact kernel vector,
so rank 125 proves it is the unique complex SM-singlet direction.
"""

from itertools import combinations
from math import lcm

from sympy import Matrix, zeros

from derive_stabilizers import form_action, form_column, generators
from test_eta1_invariant import parity
from verify_eta1_doublet_mixing import vacuum_form

P = 101
IMOD = 10


def rank_rows(rows):
    pivots = {}
    for row in rows:
        row = [x % P for x in row]
        for pivot, basis in pivots.items():
            factor = row[pivot]
            if factor:
                row = [(x-factor*y) % P for x, y in zip(row, basis)]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            inv = pow(row[pivot], -1, P)
            pivots[pivot] = [(x*inv) % P for x in row]
    return len(pivots)


def main():
    phi = Matrix.diag(*([-2]*6 + [3]*4))
    h0 = [g for _, g in generators() if all(x == 0 for x in g*phi-phi*g)]
    v = vacuum_form()
    orbit = Matrix.hstack(*[Matrix(form_column(form_action(g, v))) for g in h0])
    kernel = orbit.nullspace()
    assert len(kernel) == 12
    sm = []
    for vector in kernel:
        g = sum((vector[i]*h0[i] for i in range(21)), zeros(10))
        denominator = lcm(*(int(x.q) for x in g))
        sm.append(g*denominator)

    half = [idx for idx in combinations(range(10), 5)
            if idx < tuple(i for i in range(10) if i not in idx)]
    assert len(half) == 126
    basis = []
    for idx in half:
        other = tuple(i for i in range(10) if i not in idx)
        basis.append({idx: (1, 0), other: (0, -parity(idx+other))})
    idxs = tuple(combinations(range(10), 5))
    rows = []
    for g in sm:
        columns = [form_action(g, form) for form in basis]
        for idx in idxs:
            rows.append([(z[0]+IMOD*z[1]) % P
                         for col in columns for z in [col.get(idx, (0, 0))]])
    rank = rank_rows(rows)
    assert rank == 125, rank
    print("EXACT_MODULAR_126_SINGLET_CHECK: rank=125 over F101; V is exact kernel; unique complex SM singlet")


if __name__ == "__main__":
    main()
