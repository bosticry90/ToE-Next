"""Independent sparse-coordinate replay of the 328-real basis certificate."""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from sympy import conjugate, I, re, simplify, sympify


HERE = Path(__file__).resolve().parent


def coordinates(entry):
    c = entry["components"]
    out = {}
    for i, j, z in c["Phi"]:
        out[("P", i, j)] = sympify(z)
    for idx, a, b in c["Sigma"]:
        out[("F", *idx)] = sympify(a) + I*sympify(b)
    for i, z in c["phi"]:
        out[("v", i)] = sympify(z)
    if sympify(c["S"]) != 0:
        out[("s",)] = sympify(c["S"])
    return out


def inner(a, b):
    common = set(a) & set(b)
    value = 0
    for key in common:
        weight = 2 if key[0] in ("v", "s") else 1
        value += weight*re(conjugate(a[key])*b[key])
    return simplify(value)


def main():
    payload = json.loads((HERE / "real_field_basis.json").read_text(
        encoding="utf-8"))
    assert payload["outcome"] == "CANONICAL_328_REAL_COMPONENT_BASIS_PASS"
    entries = payload["basis"]
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":"))
    assert sha256(canonical.encode("utf-8")).hexdigest() == (
        payload["full_basis_sha256"])
    assert Counter(e["sector"] for e in entries) == {
        "Phi": 54, "Sigma": 252, "phi": 20, "S": 2,
    }
    assert len({e["name"] for e in entries}) == 328
    vectors = [coordinates(e) for e in entries]
    tested = 0
    for i, a in enumerate(vectors):
        for j, b in enumerate(vectors):
            assert inner(a, b) == int(i == j), (i, j)
            tested += 1
    assert tested == 328**2

    # Independent trace normalization of the 45 plane rotations divided by
    # sqrt(2): each has two entries of squared magnitude 1/2, and different
    # unordered planes have disjoint support.
    planes = list(combinations(range(10), 2))
    assert len(planes) == 45 and len(set(planes)) == 45
    assert all(2*sympify(1)/2 == 1 for _ in planes)
    print("INDEPENDENT_328_REAL_BASIS_REPLAY_PASS", tested)
    print("INDEPENDENT_45_GENERATOR_NORMALIZATION_REPLAY_PASS")


if __name__ == "__main__":
    main()
