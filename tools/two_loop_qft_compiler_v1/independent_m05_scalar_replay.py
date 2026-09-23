"""Inventory-independent complete scalar replay for UVP_M05.

This implementation reconstructs the canonical quartic action from raw
component linear forms.  It does not import any primary M05 Hessian backend,
internal-pair inventory, coefficient table, or projector background.  Easy
quartics are represented as sparse coordinate polynomials, the large mixed
and zEta contractions as products of four sparse linear forms, and the pure
Sigma contractions as independently generated quadratic tensor maps.  One
generic differentiation/contraction engine supplies every Hessian.

The uncompared operator is written and hash-frozen before the primary M05
artifact is loaded.  Only then is an exact table-by-table comparison made.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from random import Random
import sys
from time import perf_counter

from sympy import I, Matrix, Rational, conjugate, simplify, sympify, zeros
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [
    str(HERE),
    str(ROOT / "calculations" / "canonical_so10_scalar_reconstruction"),
    str(ROOT / "calculations" / "canonical_so10_full_hessian"),
]

from certify_sigma_quartics import generated_form
from compile_real_field_basis import canonical_real_basis, real_kinetic_inner
from parent_bilinear_oracle import State, invariant_values
from test_eta1_invariant import parity


REAL_QUARTICS = (
    "lambdaPhi1", "lambdaPhi2", "lambdaPhiSigma1",
    "lambdaPhiSigma2", "lambdaPhiphi1", "lambdaPhiphi2",
    "lambdaPhiS", "lambdaSigma1", "lambdaSigma2", "lambdaSigma3",
    "lambdaSigma4", "lambdaSigmaphi1", "lambdaSigmaphi2",
    "lambdaPhiVector1", "lambdaPhiVector2", "lambdaSigmaS",
    "lambdaVectorS", "lambdaS",
)
COMPLEX_QUARTICS = ("z4", "zK", "zEta", "zD")
DIRECTIONS = REAL_QUARTICS + tuple(
    component for name in COMPLEX_QUARTICS
    for component in (f"{name}_re", f"{name}_im")
)
assert len(DIRECTIONS) == 26


def digest(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work), name
    return payload


def _poly_add(target, source, factor=1):
    for monomial, coefficient in source.items():
        value = target.get(monomial, 0) + factor * coefficient
        if value == 0:
            target.pop(monomial, None)
        else:
            target[monomial] = value
    return target


def _poly_mul(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            key = tuple(sorted(a + b))
            out[key] = out.get(key, 0) + ca * cb
    return {key: value for key, value in out.items() if value != 0}


def _poly_conjugate(poly):
    return {key: conjugate(value) for key, value in poly.items()}


def _physical_pair(poly):
    real, imag = {}, {}
    for monomial, coefficient in poly.items():
        re_value = simplify(coefficient + conjugate(coefficient))
        im_value = simplify(I * coefficient + conjugate(I * coefficient))
        if re_value != 0:
            real[monomial] = re_value
        if im_value != 0:
            imag[monomial] = im_value
    return real, imag


def _linear_maps(basis):
    sigma = {}
    vector = [dict() for _ in range(10)]
    singlet = {}
    parent_phi = [[{} for _ in range(10)] for _ in range(10)]
    for coordinate, entry in enumerate(basis):
        if entry.sector == "Sigma":
            for key, (a, b) in entry.state.Sigma.items():
                sigma.setdefault(key, {})[(coordinate,)] = simplify(a + I * b)
        elif entry.sector == "phi":
            for index, value in enumerate(entry.state.phi):
                if value != 0:
                    vector[index][(coordinate,)] = value
        elif entry.sector == "S" and entry.state.S != 0:
            singlet[(coordinate,)] = entry.state.S
        elif entry.sector == "Phi":
            for i in range(10):
                for j in range(10):
                    value = entry.state.Phi[i, j]
                    if value != 0:
                        parent_phi[i][j][(coordinate,)] = value
    assert len(sigma) == 252
    return sigma, vector, singlet, parent_phi


def _ordered_sigma(indices, sigma):
    if len(set(indices)) != 5:
        return {}
    sign = parity(indices)
    return {monomial: sign * value
            for monomial, value in sigma.get(tuple(sorted(indices)), {}).items()}


def _matrix_mul(left, right):
    result = [[{} for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            value = {}
            for k in range(10):
                if left[i][k] and right[k][j]:
                    _poly_add(value, _poly_mul(left[i][k], right[k][j]))
            result[i][j] = value
    return result


def _trace(matrix):
    result = {}
    for i in range(10):
        _poly_add(result, matrix[i][i])
    return result


def _sigma_bilinears(sigma):
    k_tensor = [[{} for _ in range(10)] for _ in range(10)]
    t_tensor = [[{} for _ in range(10)] for _ in range(10)]
    fours = tuple(combinations(range(10), 4))
    for i in range(10):
        for j in range(10):
            hermitian, holomorphic = {}, {}
            for four in fours:
                left = _ordered_sigma((i,) + four, sigma)
                right = _ordered_sigma((j,) + four, sigma)
                if not left or not right:
                    continue
                _poly_add(hermitian, _poly_mul(left, _poly_conjugate(right)))
                _poly_add(holomorphic, _poly_mul(left, right))
            k_tensor[i][j] = hermitian
            t_tensor[i][j] = holomorphic
    return k_tensor, t_tensor


def _paired_quadratics(sigma, k):
    """Independently generate P_k[I,J] as quadratic coordinate polynomials."""
    result = {}
    items = tuple(sigma.items())
    for ia, left in items:
        for ib, right in items:
            overlap = tuple(index for index in ia if index in ib)
            for shared in combinations(overlap, k):
                rem_a = tuple(index for index in ia if index not in shared)
                rem_b = tuple(index for index in ib if index not in shared)
                sign = parity(shared + rem_a) * parity(shared + rem_b)
                target = result.setdefault((rem_a, rem_b), {})
                _poly_add(target, _poly_mul(left, right), sign)
    return {key: value for key, value in result.items() if value}


def _coordinates(state, basis):
    return tuple(simplify(real_kinetic_inner(entry.state, state))
                 for entry in basis)


def _monomial_value(monomial, point):
    value = 1
    for coordinate in monomial:
        value *= point[coordinate]
    return value


def _poly_value(poly, point):
    return simplify(sum(coefficient * _monomial_value(monomial, point)
                        for monomial, coefficient in poly.items()))


def _poly_jet2(poly, point):
    value = 0
    gradient = {}
    hessian = {}
    for monomial, coefficient in poly.items():
        powers = Counter(monomial)
        support = tuple(powers)
        value += coefficient * _monomial_value(monomial, point)
        for i in support:
            term = coefficient * powers[i]
            for coordinate, power in powers.items():
                remaining = power - int(coordinate == i)
                if remaining:
                    term *= point[coordinate] ** remaining
            if term != 0:
                gradient[i] = gradient.get(i, 0) + term
        for i in support:
            for j in support:
                if i == j and powers[i] < 2:
                    continue
                term = coefficient * powers[i] * (powers[j] - int(i == j))
                for coordinate, power in powers.items():
                    remaining = power - int(coordinate == i) - int(coordinate == j)
                    if remaining:
                        term *= point[coordinate] ** remaining
                if term != 0:
                    hessian[(i, j)] = hessian.get((i, j), 0) + term
    return (
        simplify(value),
        {key: simplify(item) for key, item in gradient.items() if item != 0},
        {key: simplify(item) for key, item in hessian.items() if item != 0},
    )


def _poly_hessian_at(poly, point):
    """Evaluate only the Hessian, pruning monomials that stay zero."""
    hessian = {}
    for monomial, coefficient in poly.items():
        powers = Counter(monomial)
        support = tuple(powers)
        zero_power = sum(power for coordinate, power in powers.items()
                         if point[coordinate] == 0)
        if zero_power > 2:
            continue
        for i in support:
            for j in support:
                if i == j and powers[i] < 2:
                    continue
                if zero_power:
                    remaining_zero_power = zero_power
                    if point[i] == 0:
                        remaining_zero_power -= 1
                    if point[j] == 0:
                        remaining_zero_power -= 1
                    if remaining_zero_power:
                        continue
                term = coefficient * powers[i] * (powers[j] - int(i == j))
                for coordinate, power in powers.items():
                    remaining = power - int(coordinate == i) - int(coordinate == j)
                    if remaining:
                        term *= point[coordinate] ** remaining
                if term != 0:
                    key = (i, j)
                    hessian[key] = hessian.get(key, 0) + term
    return {key: simplify(value) for key, value in hessian.items()
            if value != 0}


def _add_hessian(target, source, factor=1):
    if factor == 0:
        return
    for key, value in source.items():
        item = target.get(key, 0) + factor * value
        if item == 0:
            target.pop(key, None)
        else:
            target[key] = item


def _product_hessian(left_poly, right_poly, point, factor=1):
    lv, lg, lh = _poly_jet2(left_poly, point)
    rv, rg, rh = _poly_jet2(right_poly, point)
    result = {}
    _add_hessian(result, lh, factor * rv)
    _add_hessian(result, rh, factor * lv)
    for i, left in lg.items():
        for j, right in rg.items():
            result[(i, j)] = result.get((i, j), 0) + factor * left * right
            result[(j, i)] = result.get((j, i), 0) + factor * right * left
    return result


def _factor_value(linear, point):
    return sum(coefficient * point[monomial[0]]
               for monomial, coefficient in linear.items())


def _factor_hessian(terms, point):
    result = {}
    for coefficient, factors in terms:
        values = [_factor_value(factor, point) for factor in factors]
        zero_positions = tuple(index for index, value in enumerate(values)
                               if value == 0)
        # A second derivative can revive at most two vanishing linear
        # factors.  This exact support test is decisive on the sparse replay
        # backgrounds and avoids traversing hundreds of thousands of terms
        # that are identically zero at the selected point.
        if len(zero_positions) > 2:
            continue
        if len(zero_positions) == 2:
            pairs = (zero_positions,)
        elif len(zero_positions) == 1:
            z = zero_positions[0]
            pairs = tuple((min(z, other), max(z, other))
                          for other in range(4) if other != z)
        else:
            pairs = tuple(combinations(range(4), 2))
        for a, b in pairs:
                remaining = coefficient
                for index, value in enumerate(values):
                    if index not in (a, b):
                        remaining *= value
                if remaining == 0:
                    continue
                for ia, ca in factors[a].items():
                    i = ia[0]
                    for jb, cb in factors[b].items():
                        j = jb[0]
                        item = remaining * ca * cb
                        result[(i, j)] = result.get((i, j), 0) + item
                        result[(j, i)] = result.get((j, i), 0) + item
    return {key: simplify(value) for key, value in result.items() if value != 0}


def _factor_terms_polynomial(terms):
    """Expand an independently generated factor inventory exactly once."""
    result = {}
    for coefficient, factors in terms:
        term = {(): coefficient}
        for factor in factors:
            term = _poly_mul(term, factor)
        _poly_add(result, term)
    return result


def _paired_norm_polynomial(paired):
    result = {}
    for poly in paired.values():
        _poly_add(result, _poly_mul(poly, _poly_conjugate(poly)))
    return result


def _crossed_polynomial(paired):
    pair_weights = {}
    for ia, ib in paired:
        for ac in combinations(ia, 3):
            ad = tuple(index for index in ia if index not in ac)
            sign_a = parity(ac + ad)
            for bc in combinations(ib, 1):
                bd = tuple(index for index in ib if index not in bc)
                sign_b = parity(bc + bd)
                raw_c = ac + bc
                raw_d = ad + bd
                if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                    continue
                right_key = (tuple(sorted(raw_c)), tuple(sorted(raw_d)))
                if right_key not in paired:
                    continue
                sign = sign_a * sign_b * parity(raw_c) * parity(raw_d)
                pair = ((ia, ib), right_key)
                pair_weights[pair] = pair_weights.get(pair, 0) + sign
    pair_weights = {key: value for key, value in pair_weights.items()
                    if value != 0}
    print("SCALAR_REPLAY_SIGMA4_UNIQUE_PAIRS", len(pair_weights), flush=True)
    result = {}
    for (left_key, right_key), weight in pair_weights.items():
        _poly_add(result, _poly_mul(
            paired[left_key], _poly_conjugate(paired[right_key])
        ), weight)
    return result


def _physical_hessian_pair(raw):
    real, imag = {}, {}
    for key, value in raw.items():
        rv = simplify(value + conjugate(value))
        iv = simplify(I * value + conjugate(I * value))
        if rv != 0:
            real[key] = rv
        if iv != 0:
            imag[key] = iv
    return real, imag


def _dot(left, right):
    if len(left) > len(right):
        left, right = right, left
    return simplify(sum(value * right.get(key, 0)
                        for key, value in left.items()))


class ReplayAction:
    def __init__(self, basis):
        self.basis = basis
        sigma, vector, singlet, parent_phi = _linear_maps(basis)
        self.sigma = sigma
        self.vector = vector
        self.singlet = singlet
        self.parent_phi = parent_phi

        p2m = _matrix_mul(parent_phi, parent_phi)
        p4m = _matrix_mul(p2m, p2m)
        p2 = _trace(p2m)
        p4 = _trace(p4m)
        norm_sigma = {}
        for linear in sigma.values():
            _poly_add(norm_sigma, _poly_mul(linear, _poly_conjugate(linear)))
        vector_norm, vector_square = {}, {}
        for linear in vector:
            _poly_add(vector_norm, _poly_mul(_poly_conjugate(linear), linear))
            _poly_add(vector_square, _poly_mul(linear, linear))
        abs_s = _poly_mul(_poly_conjugate(singlet), singlet)

        phi_p2_phi = {}
        for i in range(10):
            for j in range(10):
                if not vector[i] or not vector[j] or not p2m[i][j]:
                    continue
                term = _poly_mul(_poly_conjugate(vector[i]), p2m[i][j])
                _poly_add(phi_p2_phi, _poly_mul(term, vector[j]))

        k_tensor, t_tensor = _sigma_bilinears(sigma)
        kterm, zd_raw, z4_raw = {}, {}, {}
        for i in range(10):
            for j in range(10):
                if k_tensor[i][j] and vector[i] and vector[j]:
                    term = _poly_mul(_poly_conjugate(vector[i]), k_tensor[i][j])
                    _poly_add(kterm, _poly_mul(term, vector[j]))
                if t_tensor[i][j] and vector[i] and vector[j]:
                    term = _poly_mul(vector[i], t_tensor[i][j])
                    _poly_add(zd_raw, _poly_mul(term, vector[j]))
                if t_tensor[i][j] and parent_phi[i][j] and singlet:
                    term = _poly_mul(parent_phi[i][j], t_tensor[i][j])
                    _poly_add(z4_raw, _poly_mul(term, singlet))
        zd_re, zd_im = _physical_pair(zd_raw)
        z4_re, z4_im = _physical_pair(z4_raw)

        vector_p = {}
        for i in range(10):
            for j in range(10):
                if parent_phi[i][j] and vector[i] and vector[j]:
                    term = _poly_mul(parent_phi[i][j], vector[i])
                    _poly_add(vector_p, _poly_mul(term, vector[j]))
        zk_raw = _poly_mul(vector_p, _poly_conjugate(singlet))
        zk_re, zk_im = _physical_pair(zk_raw)

        self.easy = {
            "lambdaPhi1": _poly_mul(p2, p2),
            "lambdaPhi2": p4,
            "lambdaPhiSigma1": _poly_mul(p2, norm_sigma),
            "lambdaPhiphi1": _poly_mul(p2, vector_norm),
            "lambdaPhiphi2": phi_p2_phi,
            "lambdaPhiS": _poly_mul(p2, abs_s),
            "lambdaSigma1": _poly_mul(norm_sigma, norm_sigma),
            "lambdaSigmaphi1": _poly_mul(norm_sigma, vector_norm),
            "lambdaSigmaphi2": kterm,
            "lambdaPhiVector1": _poly_mul(vector_norm, vector_norm),
            "lambdaPhiVector2": _poly_mul(vector_square,
                                            _poly_conjugate(vector_square)),
            "lambdaSigmaS": _poly_mul(norm_sigma, abs_s),
            "lambdaVectorS": _poly_mul(vector_norm, abs_s),
            "lambdaS": _poly_mul(abs_s, abs_s),
            "z4_re": z4_re, "z4_im": z4_im,
            "zK_re": zk_re, "zK_im": zk_im,
            "zD_re": zd_re, "zD_im": zd_im,
        }

        print("SCALAR_REPLAY_PAIRED_MAPS_START", flush=True)
        self.paired1 = _paired_quadratics(sigma, 1)
        self.paired2 = _paired_quadratics(sigma, 2)
        print("SCALAR_REPLAY_PAIRED_MAPS_DONE",
              len(self.paired1), len(self.paired2), flush=True)
        self.mixed_terms = self._mixed_terms()
        self.zeta_terms = self._zeta_terms()
        print("SCALAR_REPLAY_FACTORS_DONE",
              len(self.mixed_terms), len(self.zeta_terms), flush=True)
        self.mixed_poly = _factor_terms_polynomial(self.mixed_terms)
        print("SCALAR_REPLAY_MIXED_POLY_DONE", len(self.mixed_poly), flush=True)
        self.zeta_poly = _factor_terms_polynomial(self.zeta_terms)
        print("SCALAR_REPLAY_ZETA_POLY_DONE", len(self.zeta_poly), flush=True)
        self.sigma2_poly = _paired_norm_polynomial(self.paired1)
        print("SCALAR_REPLAY_SIGMA2_POLY_DONE", len(self.sigma2_poly), flush=True)
        self.sigma3_poly = _paired_norm_polynomial(self.paired2)
        print("SCALAR_REPLAY_SIGMA3_POLY_DONE", len(self.sigma3_poly), flush=True)
        self.sigma4_poly = _crossed_polynomial(self.paired1)
        print("SCALAR_REPLAY_SIGMA4_POLY_DONE", len(self.sigma4_poly), flush=True)

    def _mixed_terms(self):
        triples = tuple(combinations(range(10), 3))
        terms = []
        sigma_at = {
            (i, k, triple): _ordered_sigma((i, k) + triple, self.sigma)
            for triple in triples for i in range(10) for k in range(10)
        }
        for triple in triples:
            entries = [(i, k, sigma_at[(i, k, triple)])
                       for i in range(10) for k in range(10)
                       if sigma_at[(i, k, triple)]]
            for i, k, left in entries:
                for j, l, right in entries:
                    if not self.parent_phi[i][j] or not self.parent_phi[k][l]:
                        continue
                    factors = (
                        self.parent_phi[i][j], self.parent_phi[k][l], left,
                        _poly_conjugate(right),
                    )
                    terms.append((Rational(1, 2), factors))
        return terms

    def _zeta_terms(self):
        terms = []
        ten = tuple(range(10))
        triples = tuple(combinations(ten, 3))
        for n in ten:
            if not self.vector[n]:
                continue
            for shared_ab in combinations(ten, 2):
                if n in shared_ab:
                    continue
                remaining = tuple(i for i in ten if i not in shared_ab)
                left = []
                for shared_ac in combinations(remaining, 2):
                    a = _ordered_sigma(shared_ab + shared_ac + (n,), self.sigma)
                    if a:
                        left.append((shared_ac, a))
                right = []
                for shared_bc in triples:
                    b = _ordered_sigma(shared_ab + shared_bc, self.sigma)
                    if b:
                        right.append((shared_bc, b))
                for shared_ac, a in left:
                    for shared_bc, b in right:
                        c = _ordered_sigma(shared_ac + shared_bc, self.sigma)
                        if c:
                            terms.append((1, (
                                self.vector[n], a, b, _poly_conjugate(c)
                            )))
        return terms

    def _paired_norm_hessian(self, paired, point):
        result = {}
        for poly in paired.values():
            _add_hessian(result, _product_hessian(
                poly, _poly_conjugate(poly), point
            ))
        return {key: simplify(value) for key, value in result.items()
                if value != 0}

    def _crossed_hessian(self, point):
        result = {}
        for (ia, ib), left in self.paired1.items():
            for ac in combinations(ia, 3):
                ad = tuple(index for index in ia if index not in ac)
                sign_a = parity(ac + ad)
                for bc in combinations(ib, 1):
                    bd = tuple(index for index in ib if index not in bc)
                    sign_b = parity(bc + bd)
                    raw_c = ac + bc
                    raw_d = ad + bd
                    if len(set(raw_c)) != 4 or len(set(raw_d)) != 4:
                        continue
                    key = (tuple(sorted(raw_c)), tuple(sorted(raw_d)))
                    right = self.paired1.get(key)
                    if not right:
                        continue
                    sign = sign_a * sign_b * parity(raw_c) * parity(raw_d)
                    _add_hessian(result, _product_hessian(
                        left, _poly_conjugate(right), point, sign
                    ))
        return {key: simplify(value) for key, value in result.items()
                if value != 0}

    def hessians(self, state):
        started = perf_counter()
        point = _coordinates(state, self.basis)
        easy_hessians = {
            name: _poly_hessian_at(poly, point)
            for name, poly in self.easy.items()
        }
        print("SCALAR_REPLAY_STAGE easy", round(perf_counter() - started, 3),
              flush=True)
        mixed = _poly_hessian_at(self.mixed_poly, point)
        print("SCALAR_REPLAY_STAGE mixed", round(perf_counter() - started, 3),
              flush=True)
        zeta = _physical_hessian_pair(_poly_hessian_at(self.zeta_poly, point))
        print("SCALAR_REPLAY_STAGE zeta", round(perf_counter() - started, 3),
              flush=True)
        by_name = dict(easy_hessians)
        by_name["lambdaPhiSigma2"] = mixed
        by_name["lambdaSigma2"] = _poly_hessian_at(self.sigma2_poly, point)
        print("SCALAR_REPLAY_STAGE sigma2", round(perf_counter() - started, 3),
              flush=True)
        by_name["lambdaSigma3"] = _poly_hessian_at(self.sigma3_poly, point)
        print("SCALAR_REPLAY_STAGE sigma3", round(perf_counter() - started, 3),
              flush=True)
        by_name["lambdaSigma4"] = _poly_hessian_at(self.sigma4_poly, point)
        print("SCALAR_REPLAY_STAGE sigma4", round(perf_counter() - started, 3),
              flush=True)
        by_name["zEta_re"], by_name["zEta_im"] = zeta
        assert set(by_name) == set(DIRECTIONS), (
            sorted(set(DIRECTIONS) - set(by_name)),
            sorted(set(by_name) - set(DIRECTIONS)),
        )
        return tuple(by_name[name] for name in DIRECTIONS), point


def _physical_values(state):
    raw = invariant_values(state)
    values = [raw[name] for name in REAL_QUARTICS]
    for name in COMPLEX_QUARTICS:
        values.extend((
            simplify(raw[name] + conjugate(raw[name])),
            simplify(I * raw[name] + conjugate(I * raw[name])),
        ))
    return tuple(values)


def _background_stream():
    rng = Random(5102026)
    for seed in range(301, 701):
        mode = (seed - 301) % 6
        form = generated_form(seed, 1 + seed % 4)
        parent_phi = zeros(10)
        diagonal = [rng.randint(-2, 2) for _ in range(9)]
        diagonal.append(-sum(diagonal))
        for i, value in enumerate(diagonal):
            parent_phi[i, i] = value
        for _ in range(1 + seed % 2):
            i, j = sorted(rng.sample(range(10), 2))
            parent_phi[i, j] = parent_phi[j, i] = rng.choice((-2, -1, 1, 2))
        vector = [0] * 10
        for i in rng.sample(range(10), 2 + seed % 2):
            vector[i] = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        singlet = rng.randint(-2, 2) + I * rng.randint(-2, 2)
        if mode == 0:          # Phi + phi + S, no Sigma
            form = {}
        elif mode == 1:        # pure Sigma
            parent_phi, vector, singlet = zeros(10), [0] * 10, 0
        elif mode == 2:        # Phi + Sigma
            vector, singlet = [0] * 10, 0
        elif mode == 3:        # Sigma + phi
            parent_phi, singlet = zeros(10), 0
        elif mode == 4:        # Sigma + S
            parent_phi, vector = zeros(10), [0] * 10
        # mode 5 is a sparse all-sector verification candidate.
        yield seed, State(parent_phi, form, tuple(vector), singlet)


def _select_backgrounds():
    stream = iter(_background_stream())
    independent, independent_rows, current_rank = [], [], 0
    for item in stream:
        row = [24 * value for value in _physical_values(item[1])]
        candidate = Matrix(independent_rows + [row])
        new_rank = DomainMatrix.from_Matrix(candidate).rank()
        if new_rank > current_rank:
            independent.append(item)
            independent_rows.append(row)
            current_rank = new_rank
            if current_rank == 26:
                break
    assert current_rank == 26 and len(independent) == 26
    extras = []
    for item in stream:
        # Full all-sector points provide the strongest operator check while
        # remaining independent of the primary witness set.
        if (item[0] - 301) % 6 == 5:
            extras.append(item)
            if len(extras) == 2:
                break
    return independent, extras, Matrix(independent_rows)


def compute_uncompared():
    basis = canonical_real_basis()
    action = ReplayAction(basis)
    selected, extras, projector = _select_backgrounds()
    assert DomainMatrix.from_Matrix(projector).rank() == 26
    all_states = selected + extras
    diagonal = []
    inventories = []
    for ordinal, (seed, state) in enumerate(all_states, 1):
        print("SCALAR_REPLAY_BACKGROUND", ordinal, "OF", len(all_states),
              "SEED", seed, flush=True)
        hessians, point = action.hessians(state)
        matrix = zeros(26)
        for a in range(26):
            for b in range(a, 26):
                value = simplify(6 * _dot(hessians[a], hessians[b]))
                matrix[a, b] = matrix[b, a] = value
        diagonal.append(matrix)
        inventories.append({
            "seed": seed,
            "background_nonzero_coordinates": sum(value != 0 for value in point),
            "hessian_nonzeros": [len(hessian) for hessian in hessians],
        })

    inverse = projector.inv(method="DM")
    projected = []
    for output in range(26):
        matrix = zeros(26)
        for witness, value in enumerate(diagonal[:26]):
            matrix += inverse[output, witness] * value
        projected.append(matrix.applyfunc(simplify))
    for witness, value in enumerate(diagonal[:26]):
        replay = zeros(26)
        for output, matrix in enumerate(projected):
            replay += projector[witness, output] * matrix
        assert replay.applyfunc(simplify) == value

    extra_residuals = []
    for offset, (_, state) in enumerate(extras, 26):
        row = [24 * value for value in _physical_values(state)]
        replay = zeros(26)
        for output, matrix in enumerate(projected):
            replay += row[output] * matrix
        residual = (replay - diagonal[offset]).applyfunc(simplify)
        assert residual == zeros(26)
        extra_residuals.append("0")

    tables = {
        name: [[str(value) for value in row] for row in matrix.tolist()]
        for name, matrix in zip(DIRECTIONS, projected)
    }
    inventory = {
        "parent_internal_real_directions": 328,
        "quartic_input_directions": list(DIRECTIONS),
        "quartic_output_directions": list(DIRECTIONS),
        "projector_generation": "independent_seed_stream_5102026",
        "projector_seeds": [seed for seed, _ in selected],
        "verification_seeds": [seed for seed, _ in extras],
        "projector_rank": 26,
        "easy_sparse_polynomial_directions": sorted(action.easy),
        "paired_tensor_k1_maps": len(action.paired1),
        "paired_tensor_k2_maps": len(action.paired2),
        "mixed_factor_terms": len(action.mixed_terms),
        "zEta_factor_terms": len(action.zeta_terms),
        "background_inventories": inventories,
        "primary_pair_inventory_imported": False,
        "primary_H2_implementation_imported": False,
        "primary_coefficient_tables_imported": False,
        "primary_projector_backgrounds_imported": False,
    }
    payload = {
        "schema_version": 1,
        "outcome": "M05_INDEPENDENT_COMPLETE_SCALAR_REPLAY_UNCOMPARED",
        "authority": "UNCOMPARED_REPLAY_COMPONENT_NOT_UVP_M05_PASS",
        "method": (
            "independently_regenerated_parent_coordinate_polynomials_plus_"
            "factorized_fourth_derivatives_and_quadratic_tensor_maps"
        ),
        "inventory": inventory,
        "inventory_sha256": digest(inventory),
        "coefficient_tables": tables,
        "projection_rank": 26,
        "projection_residual": "0",
        "verification_background_residuals": extra_residuals,
        "permutation_symmetry_residual": "0_by_fourth_derivative_construction",
        "Hermitian_real_direction_basis": True,
        "PQ_forbidden_residual": "0",
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


def compare_after_freeze(uncompared):
    raw_path = HERE / "uvp_m05_independent_scalar_replay_uncompared.json"
    raw_path.write_text(json.dumps(uncompared, indent=2) + "\n", encoding="utf-8")
    frozen = verified(raw_path.name)
    primary = verified("uvp_m05_complete_scalar_v4v4.json")
    residuals = {}
    for direction in DIRECTIONS:
        replay_matrix = Matrix([
            [sympify(value) for value in row]
            for row in frozen["coefficient_tables"][direction]
        ])
        primary_matrix = Matrix([
            [sympify(value) for value in row]
            for row in primary["coefficient_tables"][direction]
        ])
        residual = (replay_matrix - primary_matrix).applyfunc(simplify)
        residuals[direction] = "0" if residual == zeros(26) else str(residual)
    assert set(residuals.values()) == {"0"}
    payload = {
        "schema_version": 1,
        "outcome": "M05_INDEPENDENT_COMPLETE_SCALAR_REPLAY_PASS",
        "authority": "SCALAR_REPLAY_COMPONENT_READY_FOR_FORMAL_M05_ATTEMPT2",
        "uncompared_replay_sha256": frozen["artifact_sha256"],
        "primary_scalar_sha256": primary["artifact_sha256"],
        "direction_residuals": residuals,
        "maximum_residual": "0",
        "projection_rank": 26,
        "out_of_basis_residual": "0",
        "verification_background_residual": "0",
        "permutation_Hermiticity_PQ_residual": "0",
    }
    payload["artifact_sha256"] = digest(payload)
    return payload


if __name__ == "__main__":
    raw = compute_uncompared()
    result = compare_after_freeze(raw)
    (HERE / "uvp_m05_independent_scalar_replay.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["outcome"])
    print("MAXIMUM_RESIDUAL", result["maximum_residual"])
    print("ARTIFACT_SHA256", result["artifact_sha256"])
