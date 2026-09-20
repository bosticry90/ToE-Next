"""Exact PS projectors in frozen vector, symmetric-54, self-dual-126 spaces.

The 126 projector separates number of SO(6) indices (1/5, 2/4, 3), then
uses the SO(6) 3-form Hodge eigenspaces on the 3+2 sector. It acts directly
on the same sorted-index self-dual basis as the parent-action oracle.
"""

from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

from sympy import I, Matrix, Rational, eye, simplify, zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_full_hessian"))
from compile_sm_multiplicity_representatives import HALF5, projected, hodge
from test_eta1_invariant import parity


def project_vector(v):
    assert len(v) == 10
    return Matrix(list(v[:6])+[0]*4), Matrix([0]*6+list(v[6:]))


def project_adjoint(g):
    assert g.shape == (10, 10) and g+g.T == zeros(10)
    so6, so4, cross = zeros(10), zeros(10), zeros(10)
    so6[:6, :6] = g[:6, :6]
    so4[6:, 6:] = g[6:, 6:]
    cross[:6, 6:] = g[:6, 6:]
    cross[6:, :6] = g[6:, :6]
    assert g == so6+so4+cross
    return so6, so4, cross


def project_54(x):
    assert x.shape == (10, 10) and x == x.T and x.trace() == 0
    a, b = x[:6, :6], x[6:, 6:]
    ta, tb = a.trace()/6, b.trace()/4
    sing = zeros(10)
    p20 = zeros(10)
    p9 = zeros(10)
    p24 = zeros(10)
    sing[:6, :6] = ta*eye(6)
    sing[6:, 6:] = tb*eye(4)
    p20[:6, :6] = a-ta*eye(6)
    p9[6:, 6:] = b-tb*eye(4)
    p24[:6, 6:] = x[:6, 6:]
    p24[6:, :6] = x[6:, :6]
    assert x == sing+p20+p9+p24
    return sing, p20, p9, p24


def basis_54():
    out = []
    for i in range(9):
        m = zeros(10)
        m[i, i], m[9, 9] = 1, -1
        out.append(m)
    for i, j in combinations(range(10), 2):
        m = zeros(10)
        m[i, j] = m[j, i] = 1
        out.append(m)
    assert len(out) == 54
    return out


def count_color(idx):
    return sum(j < 6 for j in idx)


def basis_126(eigen):
    assert eigen in (I, -I)
    return [(idx, projected({idx: 2}, eigen)) for idx in HALF5]


def star6_middle(form):
    """SO(6) Hodge star on (3 color indices)+(2 weak indices)."""
    out = {}
    for idx, z in form.items():
        assert count_color(idx) == 3
        col = tuple(j for j in idx if j < 6)
        weak = tuple(j for j in idx if j >= 6)
        comp = tuple(j for j in range(6) if j not in col)
        new = comp+weak
        out[new] = parity(comp+col)*z
    return out


def project_126_coeffs(coeffs, eigen):
    """Project 126 coordinates onto 6, 15x2x2, and the two 30s."""
    assert len(coeffs) == 126 and eigen in (I, -I)
    basis = basis_126(eigen)
    groups = {k: [j for j, (idx, _) in enumerate(basis)
                  if min(count_color(idx), 6-count_color(idx)) == k]
              for k in (1, 2, 3)}
    assert tuple(map(len, groups.values())) == (6, 60, 60)
    p6 = zeros(126, 1)
    p60 = zeros(126, 1)
    for j in groups[1]:
        p6[j, 0] = coeffs[j]
    for j in groups[2]:
        p60[j, 0] = coeffs[j]
    keys = [basis[j][0] for j in groups[3]]
    middle = Matrix([coeffs[j] for j in groups[3]])
    s6 = zeros(60)
    for col, j in enumerate(groups[3]):
        transformed = star6_middle(basis[j][1])
        for row, key in enumerate(keys):
            s6[row, col] = transformed.get(key, 0)
    assert s6*s6 == -eye(60)
    middle_plus = (eye(60)+s6/I)*middle/2
    middle_minus = (eye(60)-s6/I)*middle/2
    pplus = zeros(126, 1)
    pminus = zeros(126, 1)
    for row, j in enumerate(groups[3]):
        pplus[j, 0] = middle_plus[row]
        pminus[j, 0] = middle_minus[row]
    return p6, p60, pplus, pminus


def certify_126(eigen):
    basis = basis_126(eigen)
    by_k = Counter(min(count_color(idx), 6-count_color(idx)) for idx, _ in basis)
    assert by_k == {1: 6, 2: 60, 3: 60}, by_k
    mid = [(idx, form) for idx, form in basis if count_color(idx) == 3]
    keys = [idx for idx, _ in mid]
    s6 = zeros(60)
    for j, (_, form) in enumerate(mid):
        transformed = star6_middle(form)
        assert {k: simplify(v) for k, v in hodge(transformed).items()} == {
            k: simplify(eigen*v) for k, v in transformed.items()}
        for i, key in enumerate(keys):
            s6[i, j] = transformed.get(key, 0)
    assert s6*s6 == -eye(60)
    plus = (eye(60)+s6/I)/2
    minus = eye(60)-plus
    assert plus*plus == plus and minus*minus == minus
    assert plus*minus == zeros(60)
    assert plus.trace() == minus.trace() == 30
    probe = Matrix([j+I*(j % 7) for j in range(126)])
    parts = project_126_coeffs(probe, eigen)
    assert sum(parts, zeros(126, 1)) == probe
    for k, part in enumerate(parts):
        projected_parts = project_126_coeffs(part, eigen)
        assert projected_parts[k] == part
        assert all(projected_parts[l] == zeros(126, 1)
                   for l in range(4) if l != k)
    return {"(6,1,1)": 6, "(15,2,2)": 60,
            "(10,3,1)_orientation_A": 30,
            "(10bar,1,3)_orientation_B": 30}


def certify_54():
    source = basis_54()
    ranks = []
    for part in range(4):
        cols = [Matrix(list(project_54(x)[part])) for x in source]
        ranks.append(Matrix.hstack(*cols).rank())
    assert ranks == [1, 20, 9, 24], ranks
    return ranks


def main():
    e = eye(10)[:, 0]
    c, w = project_vector(e)
    assert c == e and w == zeros(10, 1)
    r54 = certify_54()
    r126 = certify_126(I)
    rbar = certify_126(-I)
    assert sum(r54) == 54 and sum(r126.values()) == 126
    assert r126 == rbar
    adjoint_basis = []
    for i, j in combinations(range(10), 2):
        g = zeros(10)
        g[i, j], g[j, i] = 1, -1
        adjoint_basis.append(g)
    adjoint_ranks = [Matrix.hstack(*[
        Matrix(list(project_adjoint(g)[k])) for g in adjoint_basis]).rank()
        for k in range(3)]
    assert adjoint_ranks == [15, 6, 24]
    print("PS_PROJECTORS_PASS", "10:6+4", "54:", r54,
          "126 and bar126:", r126,
          "adjoint:", adjoint_ranks)


if __name__ == "__main__":
    main()
