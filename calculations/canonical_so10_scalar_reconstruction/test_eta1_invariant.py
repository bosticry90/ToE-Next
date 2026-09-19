"""Exact nonzero-witness test for a candidate Sym²(126) x bar126 x 10 invariant.

This proves existence if a nonzero value is found. It does not determine multiplicity
or prove that every possible delta/epsilon contraction has been enumerated.
"""

from itertools import combinations

TEN = tuple(range(10))
ZERO = (0, 0)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def parity(seq):
    inversions = sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i + 1, len(seq)))
    return -1 if inversions % 2 else 1


def component(form, indices):
    if len(set(indices)) < 5:
        return ZERO
    value = form.get(tuple(sorted(indices)), ZERO)
    sign = parity(indices)
    return sign * value[0], sign * value[1]


WITNESS_F = (
    ((0, 1, 2, 3, 7), 1), ((0, 1, 2, 4, 7), 1),
    ((0, 1, 2, 5, 7), 2), ((0, 1, 2, 6, 7), -2),
    ((0, 1, 2, 6, 9), -2), ((0, 1, 3, 5, 6), 2),
    ((0, 1, 3, 6, 9), -2), ((0, 1, 5, 6, 9), -2),
    ((0, 1, 5, 7, 8), -1), ((0, 1, 7, 8, 9), 2),
    ((0, 2, 3, 4, 6), 2), ((0, 2, 3, 4, 9), -1),
    ((0, 2, 3, 5, 7), -1), ((0, 2, 3, 5, 8), -2),
    ((0, 2, 4, 5, 7), 2), ((0, 2, 4, 6, 9), 1),
    ((0, 2, 5, 6, 9), 2), ((0, 3, 4, 6, 9), -2),
    ((0, 3, 4, 8, 9), -1), ((0, 3, 5, 6, 8), -1),
    ((0, 3, 5, 8, 9), -1), ((0, 3, 6, 7, 9), 1),
    ((0, 4, 5, 8, 9), -2), ((0, 5, 6, 7, 8), -2),
)


def selfdual_form():
    """Exact F - i *F witness, with *Sigma = +i Sigma."""
    form = {}
    for selected, weight in WITNESS_F:
        other = tuple(i for i in TEN if i not in selected)
        form[selected] = add(form.get(selected, ZERO), (weight, 0))
        sign = parity(selected + other)
        form[other] = add(form.get(other, ZERO), (0, -weight * sign))
    return {key: value for key, value in form.items() if value != ZERO}


def conjugate(form):
    return {key: (value[0], -value[1]) for key, value in form.items()}


def contraction(a, b, c, n):
    """1/(3! 2! 2!) sum A_ijklm B_ijkpq C_lmpqn phi_n, phi=e_n."""
    total = ZERO
    for triple in combinations(TEN, 3):
        remaining = tuple(i for i in TEN if i not in triple)
        entries_a = [(pair, component(a, triple + pair)) for pair in combinations(remaining, 2)]
        entries_b = [(pair, component(b, triple + pair)) for pair in combinations(remaining, 2)]
        for pair_a, va in entries_a:
            if va == ZERO:
                continue
            for pair_b, vb in entries_b:
                if vb == ZERO:
                    continue
                vc = component(c, pair_a + pair_b + (n,))
                if vc != ZERO:
                    total = add(total, mul(mul(va, vb), vc))
    return total


def contraction_vector_on_a(a, b, c, n):
    """Other delta graph: A_ijlmn B_ijpqr C_lmpqr phi_n / (2!2!3!)."""
    total = ZERO
    for shared_ab in combinations(TEN, 2):
        remaining = tuple(i for i in TEN if i not in shared_ab)
        for shared_ac in combinations(remaining, 2):
            va = component(a, shared_ab + shared_ac + (n,))
            if va == ZERO:
                continue
            for shared_bc in combinations(TEN, 3):
                vb = component(b, shared_ab + shared_bc)
                if vb == ZERO:
                    continue
                vc = component(c, shared_ac + shared_bc)
                if vc != ZERO:
                    total = add(total, mul(mul(va, vb), vc))
    return total


def main():
    sigma = selfdual_form()
    assert len(sigma) == 48
    for five in combinations(TEN, 5):
        other = tuple(i for i in TEN if i not in five)
        star_component = component(sigma, other)
        sign = parity(other + five)
        star_component = sign * star_component[0], sign * star_component[1]
        value = component(sigma, five)
        assert star_component == (-value[1], value[0]), "self-duality failed"
    bar_sigma = conjugate(sigma)
    value_c = contraction(sigma, sigma, bar_sigma, 0)
    value_a = contraction_vector_on_a(sigma, sigma, bar_sigma, 0)
    assert value_c == ZERO
    assert value_a == (-48, 0), (value_c, value_a)
    print(f"NONZERO_WITNESS n=0 values={value_c},{value_a} components={len(sigma)}")
    print("EXISTS: one explicit delta contraction in Sym^2(126) x bar126 x 10.")


if __name__ == "__main__":
    main()
