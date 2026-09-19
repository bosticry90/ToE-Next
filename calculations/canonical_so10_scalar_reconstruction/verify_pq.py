"""Exact additive PQ-charge gate for the canonical SO(10) reconstruction."""

from itertools import combinations_with_replacement

SOURCE = {"16": -1, "Phi": 0, "Sigma": 2, "phi": -2, "S": -4}
VARIANT = {**SOURCE, "16": 1}


def charge(table, *factors):
    return sum((-1 if name.endswith("*") else 1) * table[name.rstrip("*")] for name in factors)


def main():
    terms = {
        "Y10": ("16", "16", "phi"),
        "Ybar126": ("16", "16", "Sigma*"),
        "forbidden_conjugate_Y10": ("16", "16", "phi*"),
        "printed_eta1": ("Sigma", "Sigma*", "Sigma*", "phi"),
        "neutral_eta1_multiset": ("Sigma", "Sigma", "Sigma*", "phi"),
        "chi4": ("Sigma", "Sigma", "Phi", "S"),
        "chi6": ("phi", "phi", "S*"),
        "eta3": ("Sigma", "Sigma", "phi", "phi"),
    }
    expected_source = (-4, -4, 0, -4, 0, 0, 0, 0)
    expected_variant = (0, 0, 4, -4, 0, 0, 0, 0)
    assert tuple(charge(SOURCE, *t) for t in terms.values()) == expected_source
    assert tuple(charge(VARIANT, *t) for t in terms.values()) == expected_variant
    for name, term in terms.items():
        print(f"{name}: source={charge(SOURCE, *term):+d}, variant={charge(VARIANT, *term):+d}")
    scalar_types = ("Phi", "Sigma", "Sigma*", "phi", "phi*", "S", "S*")
    for degree in (2, 3, 4):
        neutral = tuple(
            fields
            for fields in combinations_with_replacement(scalar_types, degree)
            if charge(VARIANT, *fields) == 0
        )
        print(f"degree {degree}: {len(neutral)} PQ-neutral scalar field multisets (SO(10) screening pending)")
    print("PQ arithmetic PASS; SO(10) multiplicities are checked separately in count_d5_singlets.py")


if __name__ == "__main__":
    main()
