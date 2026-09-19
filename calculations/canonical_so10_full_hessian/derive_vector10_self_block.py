"""Action-derived 10-vector quadratic self-block at the frozen singlet VEV.

This is a subblock: the eta invariant can mix the 10 with the 126, so its
eigenvalues alone are not physical scalar masses.
"""

import sys
from pathlib import Path

from sympy import I, Matrix, Symbol, conjugate, eye, simplify, sqrt, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from certify_simple_invariant_slots import k_entry, t_entry
from verify_eta1_doublet_mixing import vacuum_form


def main():
    vform = vacuum_form()
    j = zeros(10)
    for a in range(0, 10, 2):
        j[a, a+1] = -1
        j[a+1, a] = 1
    kraw = Matrix(10, 10, lambda a, b: k_entry(vform, int(a), int(b)))
    traw = Matrix(10, 10, lambda a, b: t_entry(vform, int(a), int(b)))
    assert kraw == 16*(eye(10)-I*j)
    assert traw == zeros(10)

    omega, sigma, vs = [Symbol(x, real=True) for x in ("omega", "sigma", "vs")]
    sbar = Symbol("sbar")  # conjugate(S0)=vs exp(-i thetaS)/sqrt(2)
    coefficients = {n: Symbol(n, real=True) for n in (
        "mphi2", "muPhiPhi", "lambdaPhiphi1", "lambdaPhiphi2",
        "lambdaSigmaphi1", "lambdaSigmaphi2", "lambdaVectorS")}
    z6, zk = Symbol("z6"), Symbol("zK")
    d = Matrix.diag(*([-2]*6+[3]*4))*omega/sqrt(60)
    common = (coefficients["mphi2"]+coefficients["lambdaPhiphi1"]*omega**2
              +coefficients["lambdaSigmaphi1"]*sigma**2
              +coefficients["lambdaVectorS"]*vs**2/2)
    b = (common*eye(10)+coefficients["muPhiPhi"]*d
         +coefficients["lambdaPhiphi2"]*d*d
         +coefficients["lambdaSigmaphi2"]*sigma**2*kraw/32)
    h = sbar*(z6*eye(10)+zk*d)
    assert b == conjugate(b.T)
    assert h == h.T
    assert b[:6, 6:] == zeros(6, 4)
    assert h[:6, 6:] == zeros(6, 4)
    assert all(simplify(b[a, a]-b[0, 0]) == 0 for a in range(6))
    assert all(simplify(b[a, a]-b[6, 6]) == 0 for a in range(6, 10))
    assert b.subs(coefficients["lambdaSigmaphi2"], 0)[0, 1] == 0
    assert b.subs(coefficients["lambdaSigmaphi2"], 0)[6, 7] == 0
    assert simplify((h[0, 0]-h[6, 6]).subs(zk, 0)) == 0
    print("Kraw=16(I-iJ5); T(Sigma0,Sigma0)=0")
    print("color B diagonal=", simplify(b[0, 0]), "off-pair=", simplify(b[0, 1]))
    print("weak B diagonal=", simplify(b[6, 6]), "off-pair=", simplify(b[6, 7]))
    print("color holomorphic D=", simplify(h[0, 0]))
    print("weak holomorphic D=", simplify(h[6, 6]))
    print("VECTOR10_SELF_BLOCK_PASS; 126 mixing not included")


if __name__ == "__main__":
    main()
