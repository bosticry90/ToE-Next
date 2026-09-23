"""Assemble the canonical M08 two-point candidate from derived local kernels.

The output is intentionally non-authoritative.  It exposes the complete
two-point block structure that the missing BRST three-point calculation must
either confirm or amend before UVP_M08 can be retried.
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
    group_replay = verified(
        "uvp_m08_group_contraction_independent_replay.json"
    )
    ghost = verified("uvp_m08_ghost_2point_preflight.json")
    lorentz = verified("uvp_m08_vector_2point_lorentz_preflight.json")
    lorentz_replay = verified(
        "uvp_m08_vector_lorentz_independent_replay.json"
    )
    xi = Symbol("xi", real=True)
    eta = Symbol("eta_H", real=True)
    rho = Symbol("rho", real=True)
    sigma = Symbol("sigma", real=True)
    assert group_replay["primary_group_artifact_sha256"] == (
        group["artifact_sha256"]
    )
    assert float(group_replay["maximum_primary_replay_residual"]) < 2e-12

    coefficients = lorentz["kinematic_pole_coefficients"]
    vector_A = sympify(coefficients["vector_bubble_A_p2_metric"],
                       locals={"rho": rho, "sigma": sigma})
    vector_B = sympify(coefficients["vector_bubble_B_p_mu_p_nu"],
                       locals={"rho": rho, "sigma": sigma})
    ghost_A = sympify(coefficients["ghost_bubble_A_p2_metric"])
    ghost_B = sympify(coefficients["ghost_bubble_B_p_mu_p_nu"])
    replay_coefficients = lorentz_replay["coefficients"]
    for key in (
        "vector_bubble_A_p2_metric", "vector_bubble_B_p_mu_p_nu",
        "ghost_bubble_A_p2_metric", "ghost_bubble_B_p_mu_p_nu",
    ):
        assert simplify(sympify(
            coefficients[key], locals={"rho": rho, "sigma": sigma}
        ) - sympify(
            replay_coefficients[key],
            locals={"rho": rho, "sigma": sigma}
        )) == 0

    # The matter coefficient is derived from the frozen parent content, not
    # from b10: 3 Weyl 16s give sum(T)=6 and the real scalar ledger gives 84.
    fermion_index = Rational(6)
    real_scalar_index = Rational(84)
    matter_loop_A = simplify(
        Rational(2, 3) * fermion_index
        + Rational(1, 6) * real_scalar_index
    )
    matter_loop_B = -matter_loop_A
    assert matter_loop_A == 18

    def gauge_parameter_counterterm(loop_A, loop_B, parameter):
        delta_Z_Q = simplify(-loop_A)
        # For D^{-1}=p^2 g +(1/zeta-1) p p, cancellation of the loop pole
        # gives delta_zeta/zeta = zeta*B +(1-zeta)*delta_Z_Q.
        delta_Z_parameter = simplify(
            parameter * loop_B + (1 - parameter) * delta_Z_Q
        )
        return delta_Z_Q, delta_Z_parameter

    heavy_rows = []
    for row in group["contractions"]["heavy_heavy_heavy"]["spectrum"]:
        k = q(row["eigenvalue"])
        mixed_ordered_pair_sum = 8 - k
        loop_A = simplify(
            vector_A.subs({rho: xi, sigma: xi}) * k
            + vector_A.subs({rho: xi, sigma: eta})
              * mixed_ordered_pair_sum
            + ghost_A * k + matter_loop_A
        )
        loop_B = simplify(
            vector_B.subs({rho: xi, sigma: xi}) * k
            + vector_B.subs({rho: xi, sigma: eta})
              * mixed_ordered_pair_sum
            + ghost_B * k + matter_loop_B
        )
        delta_Z_Q, delta_Z_xi = gauge_parameter_counterterm(
            loop_A, loop_B, xi
        )
        heavy_rows.append({
            "K_HHH_eigenvalue": str(k),
            "multiplicity": row["multiplicity"],
            "ordered_mixed_group_sum": str(mixed_ordered_pair_sum),
            "loop_A": str(loop_A),
            "loop_B": str(loop_B),
            "delta_Z_quantum_heavy_vector": str(delta_Z_Q),
            "multiplicative_delta_Z_xi_candidate": str(delta_Z_xi),
            "equal_gauge_specialization": {
                "delta_Z_quantum_heavy_vector": str(simplify(
                    delta_Z_Q.subs(eta, xi))),
                "multiplicative_delta_Z_xi_candidate": str(simplify(
                    delta_Z_xi.subs(eta, xi))),
            },
        })

    light_rows = []
    for row in group["contractions"]["light_light_light"]["spectrum"]:
        k = q(row["eigenvalue"])
        heavy_pair_sum = 8 - k
        loop_A = simplify(
            vector_A.subs({rho: eta, sigma: eta}) * k
            + vector_A.subs({rho: xi, sigma: xi}) * heavy_pair_sum
            + ghost_A * 8 + matter_loop_A
        )
        loop_B = simplify(
            vector_B.subs({rho: eta, sigma: eta}) * k
            + vector_B.subs({rho: xi, sigma: xi}) * heavy_pair_sum
            + ghost_B * 8 + matter_loop_B
        )
        delta_Z_Q, delta_Z_eta = gauge_parameter_counterterm(
            loop_A, loop_B, eta
        )
        light_rows.append({
            "K_LLL_eigenvalue": str(k),
            "multiplicity": row["multiplicity"],
            "heavy_pair_group_sum": str(heavy_pair_sum),
            "loop_A": str(loop_A),
            "loop_B": str(loop_B),
            "delta_Z_quantum_light_vector": str(delta_Z_Q),
            "multiplicative_delta_Z_eta_H_candidate": str(delta_Z_eta),
            "equal_gauge_specialization": {
                "delta_Z_quantum_light_vector": str(simplify(
                    delta_Z_Q.subs(eta, xi))),
                "multiplicative_delta_Z_eta_H_candidate": str(simplify(
                    delta_Z_eta.subs(eta, xi))),
            },
        })

    heavy_xi_values = {
        row["multiplicative_delta_Z_xi_candidate"] for row in heavy_rows
    }
    light_eta_values = {
        row["multiplicative_delta_Z_eta_H_candidate"] for row in light_rows
    }
    payload = {
        "schema_version": 1,
        "outcome": "M08_CANONICAL_TWO_POINT_ASSEMBLY_PREFLIGHT_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_inputs": {
            "partial_BFM_action_sha256": group["partial_BFM_action_sha256"],
            "group_contraction_sha256": group["artifact_sha256"],
            "independent_group_replay_sha256":
                group_replay["artifact_sha256"],
            "ghost_two_point_sha256": ghost["artifact_sha256"],
            "vector_Lorentz_kernel_sha256": lorentz["artifact_sha256"],
            "independent_vector_Lorentz_replay_sha256":
                lorentz_replay["artifact_sha256"],
        },
        "matter_ledger": {
            "Weyl_index_sum": str(fermion_index),
            "real_scalar_index_sum": str(real_scalar_index),
            "derived_transverse_loop_A": str(matter_loop_A),
            "derived_transverse_loop_B": str(matter_loop_B),
            "b10_imported_as_input": False,
        },
        "heavy_vector_blocks": heavy_rows,
        "light_vector_blocks": light_rows,
        "pre_BRST_diagnostic": {
            "primary_vs_independent_vector_Lorentz_residual": "0",
            "primary_vs_independent_group_maximum_residual":
                group_replay["maximum_primary_replay_residual"],
            "heavy_delta_xi_block_count": len(heavy_xi_values),
            "light_delta_eta_H_block_count": len(light_eta_values),
            "interpretation": (
                "two-point assembly alone produces block-valued gauge-"
                "fixing residues; UVP_M08 cannot adjudicate whether the "
                "single frozen xi/eta_H parameterization closes until the "
                "BRST three-point pole action and independent replay are "
                "complete"
            ),
        },
        "remaining_before_UVP_M08_retry": [
            "heavy/light ghost-vector BRST three-point primary kernels",
            "complete inventory-independent M08 replay",
            "BRST adjudication of block-valued two-point candidates",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_canonical_two_point_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("HEAVY_DELTA_XI_BLOCKS", len(heavy_xi_values))
    print("LIGHT_DELTA_ETA_BLOCKS", len(light_eta_values))
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
