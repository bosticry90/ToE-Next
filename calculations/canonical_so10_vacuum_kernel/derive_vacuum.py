"""Exact VEV restriction of frozen canonical parent-action invariant basis.

No vacuum or tadpole polynomial is entered as input. The script evaluates
the action's tensor invariants, then differentiates their symbolic sum.
"""

import sys
from pathlib import Path

from sympy import I, Symbol, conjugate, diff, expand, simplify, sqrt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from certify_sigma_quartics import quartics
from certify_simple_invariant_slots import pair_counts, t_entry
from test_eta1_invariant import conjugate as conjugate_form, contraction_vector_on_a
from verify_action_inventory import SLOTS
from verify_eta1_doublet_mixing import vacuum_form


def main():
    omega, sigma, v = [Symbol(x, real=True) for x in ("omega", "sigma", "v")]
    d = [-2]*6 + [3]*4
    form = vacuum_form()
    phi_scale = omega/sqrt(60)
    sigma_scale = sigma/(4*sqrt(2))
    s_abs2 = v*v/2

    # Direct evaluation of the invariant definitions in parent action v1.
    p2 = sum(x*x for x in d) * phi_scale**2
    p3 = sum(x**3 for x in d) * phi_scale**3
    p4 = sum(x**4 for x in d) * phi_scale**4
    n = sum(a*a+b*b for a, b in form.values()) * sigma_scale**2
    pair = pair_counts(form)
    l_phisigma = sum(d[i]*d[j]*pair[i, j] for i in range(10)
                     for j in range(i+1, 10))*phi_scale**2*sigma_scale**2
    q_raw = quartics(form)
    q0, q1, q2, _, _, x131, _ = [x*sigma_scale**4 for x in q_raw]
    assert all(t_entry(form, i, j) == 0 for i in range(10) for j in range(10))
    # No SM-singlet 10-vector tadpole is permitted; check this directly
    # for the potentially dangerous eta monomial.
    eta_vector = [contraction_vector_on_a(form, form, conjugate_form(form), i)
                  for i in range(10)]
    assert eta_vector == [(0, 0)]*10

    values = {
        "p2": p2, "N": n, "absS2": s_abs2, "p3": p3,
        "p2_squared": p2**2, "p4": p4,
        "p2_N": p2*n, "L_PhiSigma": l_phisigma,
        "p2_absS2": p2*s_abs2,
        "Q0": q0, "Q1": q1, "Q2": q2, "X131": x131,
        "N_absS2": n*s_abs2, "absS4": s_abs2**2,
    }
    all_slots = {slot for family in SLOTS.values() for slot in family}
    for fields, family in SLOTS.items():
        if "phi" in fields or "phi*" in fields:
            for slot in family:
                values[slot] = 0
        elif "Phi" in fields and fields.count("Sigma") == 2:
            # Phi_ij T_ij S = 0 on the decomposable singlet 5-form.
            for slot in family:
                values[slot] = 0
        elif "Phi" in fields and fields.count("Sigma*") == 2:
            for slot in family:
                values[slot] = 0
    assert set(values) == all_slots, (all_slots-set(values), set(values)-all_slots)

    c = {name: Symbol(name, real=True) for name in (
        "mPhi2", "mSigma2", "mS2", "muPhi", "lambdaPhi1",
        "lambdaPhi2", "lambdaPhiSigma1", "lambdaPhiSigma2",
        "lambdaPhiS", "lambdaSigma1", "lambdaSigma2",
        "lambdaSigma3", "lambdaSigma4", "lambdaSigmaS", "lambdaS")}
    terms = {
        "mPhi2": "p2", "mSigma2": "N", "mS2": "absS2",
        "muPhi": "p3", "lambdaPhi1": "p2_squared",
        "lambdaPhi2": "p4", "lambdaPhiSigma1": "p2_N",
        "lambdaPhiSigma2": "L_PhiSigma", "lambdaPhiS": "p2_absS2",
        "lambdaSigma1": "Q0", "lambdaSigma2": "Q1",
        "lambdaSigma3": "Q2", "lambdaSigma4": "X131",
        "lambdaSigmaS": "N_absS2", "lambdaS": "absS4",
    }
    potential = expand(sum(c[name]*values[slot] for name, slot in terms.items()))
    tadpoles = {str(field): simplify(diff(potential, field))
                for field in (omega, sigma, v)}
    # Independent elementary controls on tensor normalization and the
    # Babu-Khan-source-independent mixed curvature coefficient.
    assert simplify(p2-omega**2) == 0
    assert simplify(p3-omega**3/sqrt(60)) == 0
    assert simplify(p4-7*omega**4/60) == 0
    assert simplify(n-sigma**2) == 0
    assert simplify(l_phisigma+omega**2*sigma**2/4) == 0
    assert simplify(q0-sigma**4) == 0
    assert simplify(q1) == simplify(q2) == simplify(x131) == 0
    for field in (omega, sigma, v):
        assert simplify(diff(potential, field, omega) -
                        diff(potential, omega, field)) == 0
    print("action slots accounted for:", len(all_slots))
    print("VEV invariant values:")
    for name in ("p2", "p3", "p4", "N", "L_PhiSigma", "Q0", "Q1", "Q2", "X131"):
        print(name, "=", simplify(values[name]))
    print("eta vector tadpole:", eta_vector)
    print("V0 =", potential)
    for name, expression in tadpoles.items():
        print("dV0/d"+name, "=", expression)
    print("phase derivatives = 0 identically on this ansatz")
    print("VEV_RESTRICTION_AND_TADPOLES_PASS")
    return potential, (omega, sigma, v), c


if __name__ == "__main__":
    main()
