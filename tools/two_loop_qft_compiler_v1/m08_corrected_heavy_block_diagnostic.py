"""Corrected, non-authoritative M08 heavy two-point block diagnostic.

This consumes the action-derived partial-gauge-fixing mixed V-q kernel.  It
does not solve the BRST vertex problem and therefore cannot adjudicate M08 or
define a promoted gauge-parameter counterterm.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from sympy import Rational, Symbol, simplify, sympify


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def verified(name):
    payload = json.loads((HERE / name).read_text(encoding="utf-8"))
    work = dict(payload)
    embedded = work.pop("artifact_sha256")
    assert embedded == digest(work), name
    return payload


def q(value):
    value = Fraction(value)
    return Rational(value.numerator, value.denominator)


def main():
    group = verified("uvp_m08_group_contraction_preflight.json")
    partial = verified("uvp_m08_partial_gf_vector_kernel.json")
    mixed_replay = verified(
        "uvp_m08_heavy_mixed_partial_gf_independent_replay.json")
    primary = verified("uvp_m08_brst_three_point_primary_preflight.json")
    xi = Symbol("xi", positive=True)
    eta = Symbol("eta_H", positive=True)
    rho = Symbol("rho", positive=True)

    mixed = partial["external_heavy_mixed_V_q_sector"][
        "yang_mills_plus_partial_gauge_fixing"]
    mixed_a = sympify(mixed["A"], locals={"rho": rho, "eta_H": eta})
    mixed_b = sympify(mixed["B"], locals={"rho": rho, "eta_H": eta})
    mixed_a = simplify(mixed_a.subs(rho, xi))
    mixed_b = simplify(mixed_b.subs(rho, xi))
    replay_a = sympify(mixed_replay["coefficients"]["A"],
                        locals={"xi": xi, "eta_H": eta})
    replay_b = sympify(mixed_replay["coefficients"]["B"],
                        locals={"xi": xi, "eta_H": eta})
    assert simplify(mixed_a - replay_a) == 0
    assert simplify(mixed_b - replay_b) == 0

    # Pure-heavy vector plus heavy ghost use the already validated ordinary
    # covariant-gauge kernels.  Parent matter supplies the transverse +18/-18
    # contribution derived from the frozen representation ledger.
    pure_a = xi / 2 - Rational(13, 6)
    pure_b = Rational(13, 6) - xi / 2
    rows = []
    for block in group["contractions"]["heavy_heavy_heavy"]["spectrum"]:
        k = q(block["eigenvalue"])
        ordered_mixed = 8 - k
        loop_a = simplify(pure_a * k + mixed_a * ordered_mixed + 18)
        loop_b = simplify(pure_b * k + mixed_b * ordered_mixed - 18)
        zq = simplify(-loop_a)
        candidate = simplify(xi * loop_b + (1 - xi) * zq)
        rows.append({
            "K_HHH_eigenvalue": str(k),
            "ordered_2K_HHL_eigenvalue": str(ordered_mixed),
            "multiplicity": block["multiplicity"],
            "loop_A": str(loop_a),
            "loop_B": str(loop_b),
            "delta_Z_QH": str(zq),
            "pre_BRST_multiplicative_delta_Z_xi_candidate": str(candidate),
            "xi_eta_equal_one_candidate": str(candidate.subs({xi: 1, eta: 1})),
        })

    equal_one = sorted({row["xi_eta_equal_one_candidate"] for row in rows})
    process_residuals = {}
    for name in ("Gamma_ubarH_uH_VH", "Gamma_ubarH_uH_qL"):
        process = primary["processes"][name]
        process_residuals[name] = {
            "unit_gauge_p_out_of_tree_residual": process[
                "sample_tree_operator_projections"][1][
                    "p_out_of_tree_operator_residual"],
            "unit_gauge_q_out_of_tree_residual": process[
                "sample_tree_operator_projections"][1][
                    "q_out_of_tree_operator_residual"],
            "arbitrary_topology_weight_best_fit_residual": process[
                "non_authoritative_topology_weight_diagnostic"][
                    "maximum_fit_residual"],
        }

    payload = {
        "schema_version": 1,
        "outcome": "M08_CORRECTED_HEAVY_BLOCK_DIAGNOSTIC_INCOMPLETE_BRST",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": (
            "action_derived_partial_gf_mixed_vector_kernel_plus_frozen_"
            "ordinary_pure_heavy_ghost_and_matter_kernels"
        ),
        "partial_gf_kernel_sha256": partial["artifact_sha256"],
        "partial_gf_independent_replay_sha256": mixed_replay[
            "artifact_sha256"],
        "mixed_kernel_primary_replay_residual": {"A": "0", "B": "0"},
        "three_point_primary_candidate_sha256": primary["artifact_sha256"],
        "mixed_kernel": {"A": str(mixed_a), "B": str(mixed_b)},
        "heavy_blocks": rows,
        "equal_unit_gauge_distinct_candidate_values": equal_one,
        "equal_unit_gauge_block_count": len(equal_one),
        "three_point_operator_closure_diagnostics": process_residuals,
        "single_xi_closure_adjudicated": False,
        "reason": (
            "heavy_three_point_operator_does_not_yet_close_and_complete_"
            "inventory_independent_residue_replay_is_absent"
        ),
        "formal_M08_attempt2_authorized": False,
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_corrected_heavy_block_diagnostic.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("HEAVY_BLOCKS", len(rows))
    print("UNIT_GAUGE_CANDIDATES", equal_one)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
