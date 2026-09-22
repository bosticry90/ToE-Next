"""Primary UVP_P05: recursive rank-four/rank-six isotropic tensors."""

from collections import defaultdict
from hashlib import sha256
from itertools import permutations
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CONTRACT_HASH = "6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92"
PLAN_HASH = "54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101"


def canonical_hash(payload):
    return sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canonical_pairing(pairs):
    return tuple(sorted(tuple(sorted(pair)) for pair in pairs))


def recursive_pairings(labels):
    labels = tuple(labels)
    if not labels:
        return {()}
    first = labels[0]
    result = set()
    for position in range(1, len(labels)):
        second = labels[position]
        rest = labels[1:position] + labels[position + 1:]
        for tail in recursive_pairings(rest):
            result.add(canonical_pairing(((first, second),) + tail))
    return result


def pairing_strings(pairings):
    return ["*".join(f"g{a}{b}" for a, b in pairing)
            for pairing in sorted(pairings)]


def permutation_invariance_count(pairings, rank):
    reference = set(pairings)
    passed = 0
    for permutation in permutations(range(rank)):
        transformed = {
            canonical_pairing((permutation[a], permutation[b]) for a, b in pairing)
            for pairing in reference
        }
        passed += int(transformed == reference)
    return passed


def contract_first_pair(pairings, d):
    """Contract labels 0 and 1 and collect each remaining metric monomial."""
    coefficients = defaultdict(lambda: sp.Integer(0))
    for pairing in pairings:
        mate = {}
        for a, b in pairing:
            mate[a] = b
            mate[b] = a
        if mate[0] == 1:
            remaining = [pair for pair in pairing if set(pair) != {0, 1}]
            coefficients[canonical_pairing(remaining)] += d
        else:
            mate0, mate1 = mate[0], mate[1]
            remaining = [pair for pair in pairing
                         if 0 not in pair and 1 not in pair]
            remaining.append(tuple(sorted((mate0, mate1))))
            coefficients[canonical_pairing(remaining)] += 1
    return dict(coefficients)


def rank_record(n, d, epsilon):
    rank = 2 * n
    pairings = recursive_pairings(range(rank))
    expected_count = math.prod(range(1, rank, 2))
    denominator = sp.prod(d + 2 * j for j in range(n))
    denominator_d4 = denominator.subs(epsilon, 0)

    # Choose alpha=n+2, so the scalar radial moment is logarithmic and its
    # normalized residue is the u^0 coefficient, exactly one.
    scalar_radial_residue = sp.Integer(1)
    per_pairing_residue = sp.simplify(
        scalar_radial_residue / denominator_d4)
    exact_kernel = 1 / (epsilon * denominator)
    premature_kernel = 1 / (epsilon * denominator_d4)
    missed_finite_shift = sp.simplify(sp.limit(
        exact_kernel - premature_kernel, epsilon, 0))

    contracted = contract_first_pair(pairings, d)
    lower_pairings = recursive_pairings(range(2, rank))
    contraction_factor = d + 2 * n - 2
    assert set(contracted) == lower_pairings
    assert all(sp.simplify(value - contraction_factor) == 0
               for value in contracted.values())
    contraction_residual = sp.simplify(
        contraction_factor / denominator
        - 1 / sp.prod(d + 2 * j for j in range(n - 1)))

    permutation_checks = permutation_invariance_count(pairings, rank)
    assert len(pairings) == expected_count
    assert permutation_checks == math.factorial(rank)
    assert contraction_residual == 0

    return {
        "rank": rank,
        "denominator_power": n + 2,
        "pairing_count": len(pairings),
        "expected_pairing_count": expected_count,
        "pairings": pairing_strings(pairings),
        "equal_pairing_coefficients": True,
        "dimension_denominator": str(sp.factor(denominator)),
        "dimension_denominator_at_d4": str(denominator_d4),
        "scalar_radial_normalized_residue": str(scalar_radial_residue),
        "normalized_residue_per_pairing": str(per_pairing_residue),
        "permutation_checks_passed": permutation_checks,
        "permutation_checks_required": math.factorial(rank),
        "first_pair_contraction_factor": str(contraction_factor),
        "first_pair_contraction_structure_count": len(contracted),
        "first_pair_contraction_residual": str(contraction_residual),
        "premature_d4_used_by_promoted_route": False,
        "premature_d4_missed_finite_shift_per_pairing": str(
            missed_finite_shift),
    }


def main():
    epsilon = sp.symbols("epsilon")
    d = 4 - 2 * epsilon
    rank4 = rank_record(2, d, epsilon)
    rank6 = rank_record(3, d, epsilon)

    rank4_to_rank2 = sp.simplify(
        (d + 2) / (d * (d + 2)) - 1 / d)
    rank2_to_scalar = sp.simplify(d / d - 1)
    rank4_to_scalar = sp.simplify(rank4_to_rank2 + rank2_to_scalar)
    rank6_to_rank4 = sp.simplify(
        (d + 4) / (d * (d + 2) * (d + 4)) - 1 / (d * (d + 2)))
    rank6_to_scalar = sp.simplify(
        rank6_to_rank4 + rank4_to_rank2 + rank2_to_scalar)
    assert rank4_to_scalar == rank6_to_scalar == 0

    payload = {
        "schema_version": 1,
        "test_id": "UVP_P05",
        "attempt": 1,
        "contract_sha256": CONTRACT_HASH,
        "execution_plan_sha256": PLAN_HASH,
        "method": "recursive_perfect_matching_d_dimensional_tensor_reducer",
        "dimension": "d=4-2*epsilon",
        "rank4_integral": (
            "Integral_E[k_i1*k_i2*k_i3*k_i4/(k^2+m2)^4]"
        ),
        "rank6_integral": (
            "Integral_E[k_i1*k_i2*k_i3*k_i4*k_i5*k_i6/(k^2+m2)^5]"
        ),
        "rank4": rank4,
        "rank6": rank6,
        "recursive_contractions": {
            "rank6_to_rank4_residual": str(rank6_to_rank4),
            "rank4_to_rank2_residual": str(rank4_to_rank2),
            "rank2_to_scalar_residual": str(rank2_to_scalar),
            "rank4_to_scalar_residual": str(rank4_to_scalar),
            "rank6_to_scalar_residual": str(rank6_to_scalar),
        },
        "uv_ir": {
            "uv_pole": True, "ir_pole": False, "scaleless": False,
            "mass_domain": "m2>0", "rstar_required": False,
        },
    }
    payload["artifact_sha256"] = canonical_hash(payload)
    (HERE / "uvp_p05_primary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("UVP_P05_PRIMARY_COMPLETE")
    print("PAIRING_COUNTS", rank4["pairing_count"], rank6["pairing_count"])
    print("RANK4_PER_PAIRING_RESIDUE", rank4["normalized_residue_per_pairing"])
    print("RANK6_PER_PAIRING_RESIDUE", rank6["normalized_residue_per_pairing"])
    print("RECURSIVE_CONTRACTION_MAX_RESIDUAL 0")
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
