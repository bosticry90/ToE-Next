"""Exact D5 weight-character singlet counts for PQ-neutral scalar multisets.

This is the representation-count half of basis closure. It is not an explicit
delta/epsilon contraction basis or a phase/accidental-symmetry analysis.
"""

from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from math import comb
from fractions import Fraction

Z = (0, 0, 0, 0, 0)
RHO = (4, 3, 2, 1, 0)
NAMES = ("Phi", "Sigma", "Sigma*", "phi", "phi*", "S", "S*")
PQ = {"Phi": 0, "Sigma": 2, "Sigma*": -2, "phi": -2, "phi*": 2, "S": -4, "S*": 4}


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vector_char():
    out = Counter()
    for i in range(5):
        for s in (-1, 1):
            w = list(Z)
            w[i] = s
            out[tuple(w)] += 1
    return out


def form126_char(chirality):
    """Weights of the two Hodge eigenspaces in Lambda^5(C^10).

    Five nonzero coordinates have one weight vector and split by chirality.
    Three nonzero coordinates have multiplicity one per chirality; one nonzero
    coordinate has multiplicity three per chirality.
    """
    out = Counter()
    for w in product((-1, 0, 1), repeat=5):
        nz = tuple(x for x in w if x)
        if len(nz) == 5 and nz[0] * nz[1] * nz[2] * nz[3] * nz[4] == chirality:
            out[w] = 1
        elif len(nz) == 3:
            out[w] = 1
        elif len(nz) == 1:
            out[w] = 3
    assert sum(out.values()) == 126
    return out


def multiply(a, b):
    out = Counter()
    for wa, ma in a.items():
        for wb, mb in b.items():
            out[plus(wa, wb)] += ma * mb
    return out


def symmetric_power(char, n):
    h = [Counter({Z: 1})]
    for degree in range(1, n + 1):
        value = Counter()
        for k in range(1, degree + 1):
            power_sum = {tuple(k * x for x in w): m for w, m in char.items()}
            value.update(multiply(power_sum, h[degree - k]))
        assert all(m % degree == 0 for m in value.values())
        h.append(Counter({w: m // degree for w, m in value.items() if m}))
    assert sum(h[n].values()) == comb(sum(char.values()) + n - 1, n)
    return h[n]


def permutation_sign(p):
    inv = sum(p[i] > p[j] for i in range(5) for j in range(i + 1, 5))
    return -1 if inv % 2 else 1


def weyl_targets():
    out = Counter()
    for p in permutations(range(5)):
        psign = permutation_sign(p)
        for signs in product((-1, 1), repeat=5):
            if signs[0] * signs[1] * signs[2] * signs[3] * signs[4] != 1:
                continue
            wrho = tuple(signs[i] * RHO[p[i]] for i in range(5))
            target = tuple(RHO[i] - wrho[i] for i in range(5))
            out[target] += psign
    assert sum(abs(v) for v in out.values()) == 1920
    return out


TARGETS = weyl_targets()
VEC = vector_char()
PHI = symmetric_power(VEC, 2)
PHI[Z] -= 1  # symmetric traceless 54
assert sum(PHI.values()) == 54
SIGMA = form126_char(1)
BAR_SIGMA = form126_char(-1)
BASE = {"Phi": PHI, "Sigma": SIGMA, "Sigma*": BAR_SIGMA, "phi": VEC, "phi*": VEC}


@lru_cache(None)
def char_power(name, n):
    return symmetric_power(BASE[name], n)


def singlet_multiplicity(char):
    result = sum(sign * char.get(target, 0) for target, sign in TARGETS.items())
    assert result >= 0
    return result


def irrep_multiplicity(char, highest):
    result = sum(
        sign * char.get(plus(highest, target), 0)
        for target, sign in TARGETS.items()
    )
    assert result >= 0
    return result


def weyl_dimension(highest):
    shifted = plus(highest, RHO)
    result = Fraction(1)
    for i in range(5):
        for j in range(i + 1, 5):
            result *= Fraction(shifted[i] ** 2 - shifted[j] ** 2, RHO[i] ** 2 - RHO[j] ** 2)
    assert result.denominator == 1
    return result.numerator


def decomposition_dimensions(char):
    found = []
    for weight in char:
        if not (weight[0] >= weight[1] >= weight[2] >= weight[3] >= abs(weight[4])):
            continue
        multiplicity = irrep_multiplicity(char, weight)
        if multiplicity:
            found.append((weight, weyl_dimension(weight), multiplicity))
    assert sum(dimension * multiplicity for _, dimension, multiplicity in found) == sum(char.values())
    return sorted(found, key=lambda item: item[1])


def multiset_character(fields):
    powers = Counter(name for name in fields if name not in ("S", "S*"))
    pieces = [char_power(name, n) for name, n in powers.items()]
    pieces.sort(key=len)
    out = Counter({Z: 1})
    for piece in pieces:
        out = multiply(out, piece)
    return out


def main():
    assert singlet_multiplicity(VEC) == 0
    assert singlet_multiplicity(symmetric_power(VEC, 2)) == 1
    assert singlet_multiplicity(symmetric_power(PHI, 2)) == 1
    assert singlet_multiplicity(multiply(SIGMA, BAR_SIGMA)) == 1
    assert singlet_multiplicity(multiset_character(("Sigma", "Sigma", "Sigma*", "phi"))) == 1
    assert [(d, m) for _, d, m in decomposition_dimensions(char_power("Sigma", 2))] == [(54, 1), (1050, 1), (2772, 1), (4125, 1)]
    assert [(d, m) for _, d, m in decomposition_dimensions(multiply(SIGMA, VEC))] == [(210, 1), (1050, 1)]
    print("D5 character controls PASS; eta1-neutral multiplicity = 1")
    print("Independent highest-weight dimensions PASS: Sym^2(126)=54+1050+2772+4125; 126x10=210+1050")
    counts = Counter()
    supported = Counter()
    total = 0
    for degree in (2, 3, 4):
        for fields in combinations_with_replacement(NAMES, degree):
            if sum(PQ[name] for name in fields) != 0:
                continue
            multiplicity = singlet_multiplicity(multiset_character(fields))
            counts[degree] += 1
            if multiplicity:
                supported[degree] += 1
            total += multiplicity
            print(f"{degree}: {' '.join(fields):35s} singlets={multiplicity}")
    assert counts == {2: 6, 3: 12, 4: 26}
    print(f"TOTAL PQ-neutral field multisets={sum(counts.values())}; singlet-bearing multisets={sum(supported.values())}; complex singlet slots={total}")
    print(f"SINGLET_BEARING_BY_DEGREE {dict(supported)}")
    print("This character-count script supplies upper bounds; explicit rank and Hermitian closure are checked separately in the v2 action gate.")


if __name__ == "__main__":
    main()
