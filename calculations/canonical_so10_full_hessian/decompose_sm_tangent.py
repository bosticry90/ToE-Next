"""Exact SM character decomposition of the 328-real-dimensional tangent.

The table is the decomposition of its complexification, so complex irrep
dimensions sum to 328. Cartan weights are in the parent D5 vector basis;
six times physical hypercharge is 2 sum(color weights)-3 sum(weak weights).
"""

import sys
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from count_d5_singlets import BAR_SIGMA, PHI, SIGMA, VEC, Z, plus


def subtract(a, b):
    return tuple(x-y for x, y in zip(a, b))


def sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i+1, len(p))) % 2 else 1


def sm_weyl_targets():
    rho3 = (1, 0, -1)
    out = []
    for pc in permutations(range(3)):
        tc = subtract(rho3, tuple(rho3[i] for i in pc))
        for pw in permutations(range(2)):
            tw = (0, 0) if pw == (0, 1) else (1, -1)
            out.append((tc+tw, sign(pc)*sign(pw)))
    return out


TARGETS = sm_weyl_targets()


def sm_label(w):
    p, q, n = w[0]-w[1], w[1]-w[2], w[3]-w[4]
    y6 = 2*sum(w[:3])-3*sum(w[3:])
    assert min(p, q, n) >= 0
    return (p, q, n, y6)


def dimension(label):
    p, q, n, _ = label
    return (p+1)*(q+1)*(p+q+2)*(n+1)//2


def decompose(char):
    result = Counter()
    for w in char:
        if not (w[0] >= w[1] >= w[2] and w[3] >= w[4]):
            continue
        multiplicity = sum(s*char.get(plus(w, t), 0) for t, s in TARGETS)
        assert multiplicity >= 0, (w, multiplicity)
        if multiplicity:
            result[sm_label(w)] += multiplicity
    assert sum(dimension(k)*v for k, v in result.items()) == sum(char.values()), result
    return result


def adjoint_char():
    weights = [w for w, m in VEC.items() for _ in range(m)]
    out = Counter()
    for a, b in combinations(range(len(weights)), 2):
        out[plus(weights[a], weights[b])] += 1
    assert sum(out.values()) == 45
    return out


def main():
    sectors = {
        "Phi_54_real": PHI,
        "Sigma_126_complexified": SIGMA,
        "Sigma_bar126_complexified": BAR_SIGMA,
        "phi_10_complexified": VEC,
        "phi_bar10_complexified": VEC,
        "S_realification": Counter({Z: 2}),
    }
    assert sum(sum(c.values()) for c in sectors.values()) == 328
    total = Counter()
    for name, char in sectors.items():
        dec = decompose(char)
        assert sum(dimension(k)*v for k, v in dec.items()) == sum(char.values())
        total.update(dec)
        print(name, "dimension", sum(char.values()), "irreps", sorted(dec.items()))
    assert sum(dimension(k)*v for k, v in total.items()) == 328
    assert total[(0, 0, 0, 0)] == 5
    assert total[(0, 0, 1, -3)] == total[(0, 0, 1, 3)] == 4
    for (p, q, n, y6), mult in total.items():
        assert total[(q, p, n, -y6)] == mult
    print("TOTAL 328-complex-dimensional complexification:")
    for label, mult in sorted(total.items(), key=lambda kv: (dimension(kv[0]), kv[0])):
        print(label, "dim", dimension(label), "multiplicity", mult,
              "contribution", dimension(label)*mult)
    adj = decompose(adjoint_char())
    unbroken = Counter({(1, 1, 0, 0): 1, (0, 0, 2, 0): 1, (0, 0, 0, 0): 1})
    assert sum(dimension(k)*v for k, v in unbroken.items()) == 12
    assert all(adj[k] >= v for k, v in unbroken.items())
    broken = adj-unbroken
    assert sum(dimension(k)*v for k, v in broken.items()) == 33
    assert all(total[k] >= v for k, v in broken.items())
    assert broken[(0, 0, 0, 0)] == 1
    assert broken[(0, 0, 1, -3)] == broken[(0, 0, 1, 3)] == 0
    print("BROKEN_GAUGE_COMPLEXIFICATION 33:", sorted(broken.items()))
    print("Goldstone requirement: 33 gauge directions plus independent PQ neutral singlet = 34 real null directions")
    print("A tuned SM Higgs doublet would add (1,2,+/-1/2) = four real null directions, not part of the 34")
    print("SM_TANGENT_DIMENSION_AND_GOLDSTONE_IRREPS_PASS")


if __name__ == "__main__":
    main()
