"""Bounded adversarial orbit search; exact parent-action replay decides any hit."""

from pathlib import Path
import sys

import numpy as np
from scipy.optimize import differential_evolution
from sympy import N, simplify, zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canonical_so10_bfb_probe"))
sys.path.insert(0, str(HERE.parent / "canonical_so10_scalar_reconstruction"))
from probe import State, coefficients, parts, quartic, state_add, state_scale
from certify_sigma_quartics import generated_form, quartics
from verify_eta1_doublet_mixing import doublet_form, vacuum_form


def combine(states, weights):
    result = state_scale(states[0], 0)
    for state, weight in zip(states, weights):
        if weight:
            result = state_add(result, state_scale(state, weight))
    return result


def sigma_scan(c):
    coeff = [c[f"lambdaSigma{i}"] for i in range(1, 5)]
    best = None
    for seed in range(1, 65):
        form = generated_form(seed, 2 + seed % 9)
        q = quartics(form)
        value = coeff[0]*q[0] + coeff[1]*q[1] + coeff[2]*q[2] + coeff[3]*q[5]
        if seed == 1:
            assert simplify(quartic(State(zeros(10), form, (0,)*10, 0), c)-value) == 0
        ratio = float(N(value/q[0], 30))
        if best is None or ratio < best[0]:
            best = (ratio, seed, value, q)
        if value < 0:
            print("PURE_SIGMA_NEGATIVE", seed, value, q, flush=True)
            return form
    print("PURE_SIGMA_SCREEN", "64_exact_forms", "min_V4_over_Q0", best[0],
          "seed", best[1], "X131_over_Q1", float(best[3][5]/best[3][1]), flush=True)
    return None


def monomials(count):
    def rec(left, n):
        if n == 1:
            yield (left,)
        else:
            for k in range(left + 1):
                for tail in rec(left-k, n-1):
                    yield (k,) + tail
    return list(rec(4, count))


def simplex_nodes(count):
    return monomials(count)


def monomial_values(x, exponents):
    return np.array([np.prod([a**p for a, p in zip(x, powers)])
                     for powers in exponents], dtype=float)


def compiled_stratum(names, states, c):
    exponents = monomials(len(names))
    nodes = simplex_nodes(len(names))
    matrix = np.array([monomial_values(node, exponents) for node in nodes])
    assert np.linalg.matrix_rank(matrix) == len(exponents)
    values = np.array([float(N(quartic(combine(states, node), c), 30))
                       for node in nodes])
    coeff = np.linalg.solve(matrix, values)
    # A signed out-of-grid point checks the interpolated quartic before use.
    check = tuple((1, -2, 3, -1, 2)[:len(names)])
    direct = float(N(quartic(combine(states, check), c), 30))
    predicted = float(monomial_values(check, exponents) @ coeff)
    if abs(direct-predicted) > 1e-8*max(1.0, abs(direct)):
        print("INTERPOLATION_CHECK_FAILURE", names, "direct", direct,
              "predicted", predicted, "condition", np.linalg.cond(matrix),
              flush=True)
        raise AssertionError("quartic interpolation mismatch")
    return exponents, coeff


def optimize_stratum(names, states, c):
    exponents, coeff = compiled_stratum(names, states, c)

    def objective(x):
        norm = np.linalg.norm(x)
        if norm < 1e-12:
            return 1e6
        return float(monomial_values(x/norm, exponents) @ coeff)

    runs = [differential_evolution(objective, [(-1, 1)]*len(names),
                                   seed=seed, maxiter=240, popsize=12,
                                   tol=1e-10, polish=True)
            for seed in (1729, 2718, 3141, 5772)]
    result = min(runs, key=lambda item: item.fun)
    x = result.x/np.linalg.norm(result.x)
    print("STRATUM", "+".join(names), "min_unit_coordinate_V4", result.fun,
          "unit_coordinates", x.tolist(), flush=True)
    if result.fun < -1e-8:
        # Integer coordinates represent the same fixed-denominator rational ray.
        weights = [round(float(a)*10000) for a in x]
        ray = combine(states, weights)
        exact = quartic(ray, c)
        print("RATIONAL_REPLAY", "+".join(names), weights,
              "exact_V4", exact, "numeric_V4", N(exact, 40), flush=True)
        if exact < 0:
            assert simplify(quartic(state_scale(ray, 2), c)-16*exact) == 0
            return weights, exact
    return None


def main():
    c = coefficients()
    if sigma_scan(c) is not None:
        return
    basis = dict(parts())
    zero_vector = (0,)*10
    basis["Sigma_eta_vac"] = State(zeros(10), vacuum_form(), zero_vector, 0)
    basis["Sigma_eta_weak6"] = State(zeros(10), doublet_form(6), zero_vector, 0)
    basis["Sigma_eta_weak7"] = State(zeros(10), doublet_form(7), zero_vector, 0)
    basis["phi_eta_weak6"] = State(zeros(10), {}, (0,)*6+(1,)+(0,)*3, 0)
    basis["phi_eta_weak7"] = State(zeros(10), {}, (0,)*7+(1,)+(0,)*2, 0)
    strata = (
        ("Phi_diag", "phi_doublet_re", "S_re"),
        ("Phi_PS", "Sigma_singlet", "S_re"),
        ("Sigma_singlet", "Sigma_doublet_re", "phi_doublet_re"),
        ("Sigma_singlet", "phi_doublet_re", "S_re"),
        ("Sigma_doublet_re", "Sigma_doublet_im", "phi_doublet_re"),
        ("Phi_PS", "Sigma_singlet", "phi_doublet_re", "S_re"),
        ("Sigma_eta_vac", "Sigma_eta_weak6", "phi_eta_weak6"),
        ("Sigma_eta_vac", "Sigma_eta_weak6", "Sigma_eta_weak7",
         "phi_eta_weak6"),
    )
    if "--extended" in sys.argv:
        basis["Sigma_generated6"] = State(
            zeros(10), generated_form(6, 8), zero_vector, 0)
        strata = (
            ("Phi_PS", "Sigma_eta_vac", "Sigma_eta_weak6",
             "phi_eta_weak6", "S_re"),
            ("Sigma_eta_vac", "Sigma_eta_weak6", "phi_eta_weak6",
             "S_re", "S_im"),
            ("Phi_diag", "Sigma_generated6", "phi_eta_weak6", "S_re"),
        )
    for names in strata:
        hit = optimize_stratum(names, [basis[name] for name in names], c)
        if hit:
            print("BFB_COUNTEREXAMPLE_FOUND", "+".join(names), flush=True)
            return
    print("BFB_UNRESOLVED", "strata", len(strata), flush=True)


if __name__ == "__main__":
    main()
