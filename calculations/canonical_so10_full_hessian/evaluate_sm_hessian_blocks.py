"""Exact kinetic-normalized complexified Hessian pairings at the witness.

For an SM irrep R, the invariant Hessian pairs a highest-weight vector in R
with the conjugate (lowest-weight) vector in Rbar. A complex highest-weight
representative is represented as A+iB with A,B physical real tangents.
The parent oracle then yields B_C(u,conj(v)) by real bilinear extension.
This file supports focused block checks; an all-irrep pass is not claimed.
"""

from dataclasses import dataclass
from functools import lru_cache

from sympy import Float, I, Matrix, Rational, conjugate, simplify, sympify, zeros

from compile_sm_multiplicity_representatives import (
    compile_representatives, scale_obj,
)
from compile_sm_multiplicity_representatives import (
    adjoint_highest_weights, form_action, kinetic_inner,
)
from define_generic_nullity_test import exact_stationary_witness
from parent_bilinear_oracle import State, parent_bilinear, vacuum_state


def split(z):
    real, imag = z.as_real_imag()
    return simplify(real), simplify(imag)


def form_state(form):
    return {idx: split(z) for idx, z in form.items()}


def empty_state(phi=None, sigma=None, vec=None, singlet=0):
    return State(phi if phi is not None else zeros(10),
                 sigma if sigma is not None else {},
                 tuple(vec) if vec is not None else (0,)*10, singlet)


@dataclass(frozen=True)
class ComplexTangent:
    real: State
    imag: State


def realified_representative(sector, obj):
    """Map one complexified tensor representative into A+iB real tangents."""
    if sector == "Phi":
        ar = zeros(10)
        ai = zeros(10)
        for j in range(10):
            for k in range(10):
                ar[j, k], ai[j, k] = split(obj[j, k])
        return ComplexTangent(empty_state(phi=ar), empty_state(phi=ai))
    if sector in ("Sigma", "SigmaBar"):
        # For a complex field Z, Z and Z* are independent in the
        # complexified real tangent. The factor 1/2 gives delta Z=F,
        # delta Z*=0 (or vice versa). A rational rescaling of each already
        # normalized parent rep avoids unnecessary radicals in contractions.
        f = obj if sector == "Sigma" else {
            idx: conjugate(z) for idx, z in obj.items()}
        sign = -1 if sector == "Sigma" else 1
        real_form = {idx: simplify(Rational(1, 2)*z) for idx, z in f.items()}
        imag_form = {idx: simplify(sign*I*Rational(1, 2)*z) for idx, z in f.items()}
        return ComplexTangent(empty_state(sigma=form_state(real_form)),
                              empty_state(sigma=form_state(imag_form)))
    if sector in ("phi", "phiBar"):
        v = obj if sector == "phi" else obj.applyfunc(conjugate)
        sign = -1 if sector == "phi" else 1
        return ComplexTangent(
            empty_state(vec=[simplify(Rational(1, 2)*z) for z in v]),
            empty_state(vec=[simplify(sign*I*Rational(1, 2)*z) for z in v]),
        )
    assert sector in ("S", "SBar")
    sign = -1 if sector == "S" else 1
    return ComplexTangent(empty_state(singlet=Rational(1, 2)),
                          empty_state(singlet=sign*I/2))


@lru_cache(maxsize=None)
def representatives():
    return compile_representatives()


def rationalized_object(sector, obj):
    if sector in ("Sigma", "SigmaBar"):
        entries = list(obj.values())
    else:
        entries = list(obj)
    pivot = next(z for z in entries if z != 0)
    result = scale_obj(obj, 1/sympify(pivot))
    flattened = list(result.values()) if isinstance(result, dict) else list(result)
    assert all(simplify(z).as_real_imag()[0].is_rational
               and simplify(z).as_real_imag()[1].is_rational
               for z in flattened), (sector, pivot)
    return result


@lru_cache(maxsize=None)
def rational_representatives():
    return {label: [(sector, weight, rationalized_object(sector, obj))
                    for sector, weight, obj in entries]
            for label, entries in representatives().items()}


@lru_cache(maxsize=None)
def witness():
    return exact_stationary_witness()


def hermitian_entry(u, v, coefficients=None):
    """Return B_C(conj(u),v), so H times orbit coordinates is meaningful."""
    c = witness() if coefficients is None else coefficients
    a, b = u.real, u.imag
    x, y = v.real, v.imag
    return simplify(parent_bilinear(a, x, c)+parent_bilinear(b, y, c)
                    +I*(parent_bilinear(a, y, c)-parent_bilinear(b, x, c)))


def block(label, coefficients=None):
    """Exact multiplicity block at the raw VEV for any frozen-action coefficients.

    The default is the declared stationary rank witness. Passing a complete
    coefficient mapping produces the same block at another parameter point;
    no tadpoles or positivity are silently imposed by this function.
    """
    reps = rational_representatives()[label]
    tangents = [realified_representative(sector, obj)
                for sector, _, obj in reps]
    m = len(tangents)
    h = Matrix(m, m, lambda i, j: hermitian_entry(
        tangents[i], tangents[j], coefficients))
    assert not h.atoms(Float), (label, "non-exact Hessian entry")
    assert h == h.H, (label, h-h.H)
    return h


def orbit_coefficients(label):
    """Project each broken adjoint highest weight orbit into the scalar basis."""
    base = vacuum_state()
    p0 = base.Phi
    f0 = {idx: a+I*b for idx, (a, b) in base.Sigma.items()}
    fbar0 = {idx: conjugate(z) for idx, z in f0.items()}
    reps = rational_representatives()[label]
    results = []
    for _, generator in adjoint_highest_weights()[label]:
        dp = generator*p0-p0*generator
        df = form_action(generator, f0)
        dfbar = form_action(generator, fbar0)
        coefficients = []
        for sector, _, obj in reps:
            if sector == "Phi":
                z = kinetic_inner(obj, dp, "matrix")/kinetic_inner(obj, obj, "matrix")
            elif sector == "Sigma":
                z = kinetic_inner(obj, df, "form")/kinetic_inner(obj, obj, "form")
            elif sector == "SigmaBar":
                z = kinetic_inner(obj, dfbar, "form")/kinetic_inner(obj, obj, "form")
            else:
                z = 0
            coefficients.append(simplify(z))
        column = Matrix(coefficients)
        if column == zeros(len(reps), 1):
            continue
        # The representative basis is complete within this highest-weight
        # space, not merely a source of plausible orbit coefficients.
        rp = zeros(10)
        rf = {}
        rfbar = {}
        for coefficient, (sector, _, obj) in zip(coefficients, reps):
            if sector == "Phi":
                rp += coefficient*obj
            elif sector in ("Sigma", "SigmaBar"):
                dest = rf if sector == "Sigma" else rfbar
                for idx, value in obj.items():
                    dest[idx] = simplify(dest.get(idx, 0)+coefficient*value)
        assert rp == dp, (label, "Phi orbit projection")
        assert all(simplify(rf.get(idx, 0)-df.get(idx, 0)) == 0
                   for idx in set(rf) | set(df)), (label, "Sigma orbit projection")
        assert all(simplify(rfbar.get(idx, 0)-dfbar.get(idx, 0)) == 0
                   for idx in set(rfbar) | set(dfbar)), (label, "SigmaBar orbit projection")
        results.append(column)
    return results


def pq_coefficients():
    """Project the physical PQ tangent (2i Sigma, -4i S) into neutral copies."""
    label = (0, 0, 0, 0)
    base = vacuum_state()
    f0 = {idx: a+I*b for idx, (a, b) in base.Sigma.items()}
    df = {idx: 2*I*z for idx, z in f0.items()}
    dfbar = {idx: -2*I*conjugate(z) for idx, z in f0.items()}
    out = []
    for sector, _, obj in rational_representatives()[label]:
        if sector == "Sigma":
            z = kinetic_inner(obj, df, "form")/kinetic_inner(obj, obj, "form")
        elif sector == "SigmaBar":
            z = kinetic_inner(obj, dfbar, "form")/kinetic_inner(obj, obj, "form")
        elif sector == "S":
            z = -4*I
        elif sector == "SBar":
            z = 4*I
        else:
            z = 0
        out.append(simplify(z))
    return Matrix(out)


def main():
    # These six broken-gauge irreps have multiplicity one in the scalar
    # tangent, so their complete multiplicity block must vanish.
    one_copy_goldstones = (
        (0, 0, 0, 6), (0, 0, 0, -6),
        (0, 1, 0, 4), (1, 0, 0, -4),
        (1, 0, 1, 5), (0, 1, 1, -5),
    )
    for label in one_copy_goldstones:
        h = block(label)
        assert h == zeros(1), (label, h)
        orbits = orbit_coefficients(label)
        assert len(orbits) == 1 and h*orbits[0] == zeros(1, 1)
        print(label, "1x1 broken-gauge block EXACT_ZERO")
    print("SIX_ONE_COPY_GOLDSTONE_BLOCKS_PASS; remaining blocks not evaluated")


if __name__ == "__main__":
    main()
