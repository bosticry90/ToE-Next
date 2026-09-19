"""Exact quadratic doublet block from the frozen canonical action.

Coordinates x_a multiply E_a/sqrt(3) in Sigma; y_a multiply e_a in phi,
a=6..9. These are canonically normalized complex coordinates. The output
is the complete quadratic form on the color-singlet SO(4)-vector doublet
sector, not a light-eigenvalue or positivity claim.
"""

import sys
from itertools import combinations
from pathlib import Path

from sympy import I, Matrix, Symbol, conjugate, eye, simplify, sqrt, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from certify_sigma_quartics import add_forms, paired_tensor
from certify_simple_invariant_slots import k_entry
from test_eta1_invariant import add, mul, parity
from verify_eta1_doublet_mixing import bilinear_matrices, doublet_form, vacuum_form


def c(z):
    return z[0] + I*z[1]


def gram(forms, weight):
    return Matrix(4, 4, lambda a, b: sum(
        weight(idx)*c(forms[a].get(idx, (0, 0)))*conjugate(c(forms[b].get(idx, (0, 0))))
        for idx in set(forms[a]) | set(forms[b])))


def holomorphic_gram(forms, weight):
    return Matrix(4, 4, lambda a, b: sum(
        weight(idx)*c(forms[a].get(idx, (0, 0)))*c(forms[b].get(idx, (0, 0)))
        for idx in set(forms[a]) | set(forms[b])))


def tensor_difference(a, b, cform):
    out = dict(a)
    for source in (b, cform):
        for key, z in source.items():
            old = out.get(key, (0, 0))
            out[key] = (old[0]-z[0], old[1]-z[1])
    return {key: z for key, z in out.items() if z != (0, 0)}


def mixed_pair(v, e, k):
    return tensor_difference(paired_tensor(add_forms(v, e), k),
                             paired_tensor(v, k), paired_tensor(e, k))


def pair_norm(a, b):
    return sum(c(z)*conjugate(c(b.get(key, (0, 0)))) for key, z in a.items())


def crossed_pair(a, b):
    # Delta graph (AB,AC,AD,BC,BD,CD)=(1,3,1,1,3,1).
    result = (0, 0)
    for (ia, ib), za in a.items():
        for ac in combinations(ia, 3):
            ad = tuple(i for i in ia if i not in ac)
            sign_a = parity(ac+ad)
            for bc in combinations(ib, 1):
                bd = tuple(i for i in ib if i not in bc)
                raw_c, raw_d = ac+bc, ad+bd
                if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                    continue
                zb = b.get((tuple(sorted(raw_c)), tuple(sorted(raw_d))), (0, 0))
                if zb == (0, 0):
                    continue
                sign = sign_a*parity(bc+bd)*parity(raw_c)*parity(raw_d)
                z = mul(za, (zb[0], -zb[1]))
                result = add(result, (sign*z[0], sign*z[1]))
    return c(result)


def main():
    v = vacuum_form()
    e = [doublet_form(a) for a in range(6, 10)]
    d = [-2]*6 + [3]*4
    ngram = gram(e, lambda idx: 1)/3
    lgram = gram(e, lambda idx: sum(d[i]*d[j] for i, j in combinations(idx, 2)))/3
    tgram = holomorphic_gram(e, lambda idx: sum(d[i] for i in idx))/3
    p1 = [mixed_pair(v, f, 1) for f in e]
    p2 = [mixed_pair(v, f, 2) for f in e]
    q1gram = Matrix(4, 4, lambda a, b: pair_norm(p1[a], p1[b]))
    q2gram = Matrix(4, 4, lambda a, b: pair_norm(p2[a], p2[b]))
    xgram = Matrix(4, 4, lambda a, b: crossed_pair(p1[a], p1[b]))
    kweak = Matrix(4, 4, lambda a, b: k_entry(v, int(a)+6, int(b)+6))
    eta_raw, eta_conj_raw = bilinear_matrices()
    eta = Matrix(4, 4, lambda a, b: c(eta_raw[int(a)][int(b)]))
    assert all(z == (0, 0) for row in eta_conj_raw for z in row)
    for matrix in (ngram, lgram, q1gram, q2gram, xgram, kweak):
        assert matrix == matrix.conjugate().T
    assert tgram == tgram.T
    assert ngram == 2*eye(4)

    omega, sigma, vS = [Symbol(x, real=True) for x in ("omega", "sigma", "vS")]
    s, sbar = Symbol("s"), Symbol("sbar")  # s=vS*exp(i thetaS)/sqrt(2)
    z4, z6, zK, zEta = [Symbol(x) for x in ("z4", "z6", "zK", "zEta")]
    names = ("mSigma2", "mphi2", "muPhiPhi", "lambdaPhiSigma1",
             "lambdaPhiSigma2", "lambdaSigma1", "lambdaSigma2",
             "lambdaSigma3", "lambdaSigma4", "lambdaSigmaS",
             "lambdaPhiphi1", "lambdaPhiphi2", "lambdaSigmaphi1",
             "lambdaSigmaphi2", "lambdaVectorS")
    z = {name: Symbol(name, real=True) for name in names}
    b = 3*omega/sqrt(60)  # weak 10-vector Phi eigenvalue
    # Quadratic potential in x,y is x_a conjugate(x_b) A_ab +
    # y_a conjugate(y_b) B_ab + [x_a x_b C_ab + y_a y_b D_ab
    # + x_a y_b E_ab + h.c.].
    a = ngram*(z["mSigma2"] + z["lambdaPhiSigma1"]*omega**2
               + z["lambdaSigmaS"]*vS**2/2
               + 2*z["lambdaSigma1"]*sigma**2)
    a += z["lambdaPhiSigma2"]*omega**2*lgram/60
    a += sigma**2*(z["lambdaSigma2"]*q1gram
                   + z["lambdaSigma3"]*q2gram
                   + z["lambdaSigma4"]*xgram)/96
    bmat = eye(4)*(z["mphi2"] + z["muPhiPhi"]*b
                   + z["lambdaPhiphi1"]*omega**2
                   + z["lambdaPhiphi2"]*b**2
                   + z["lambdaSigmaphi1"]*sigma**2
                   + z["lambdaVectorS"]*vS**2/2)
    bmat += z["lambdaSigmaphi2"]*sigma**2*kweak/32
    cmat = z4*s*omega*tgram/sqrt(60)
    dmat = (z6+zK*b)*sbar*eye(4)
    emat = zEta*sigma**2*eta/(32*sqrt(3))
    assert a.applyfunc(simplify) == a.conjugate().T.applyfunc(simplify)
    assert bmat.applyfunc(simplify) == bmat.conjugate().T.applyfunc(simplify)
    assert cmat == cmat.T and dmat == dmat.T

    print("N gram=", ngram)
    print("L(weak) gram=", lgram)
    print("T holomorphic gram=", tgram)
    print("Q1 gram=", q1gram)
    print("Q2 gram=", q2gram)
    print("X131 gram=", xgram)
    print("K weak raw=", kweak)
    print("A (Sigma hermitian)=", a.applyfunc(simplify))
    print("B (10 hermitian)=", bmat.applyfunc(simplify))
    print("C (Sigma holomorphic)=", cmat.applyfunc(simplify))
    print("D (10 holomorphic)=", dmat.applyfunc(simplify))
    print("E (eta mixed holomorphic)=", emat.applyfunc(simplify))
    print("DOUBLEt_QUADRATIC_BLOCK_DERIVED; no inertia/nullity claim")


if __name__ == "__main__":
    main()
