"""Inventory-independent replay of the canonical M08 two-point assembly.

Only independent group and auxiliary-mass Lorentz artifacts are consumed.
The primary canonical assembly and its residue table are not imported.
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
    group = verified("uvp_m08_group_contraction_independent_replay.json")
    lorentz = verified("uvp_m08_vector_lorentz_independent_replay.json")
    xi = Symbol("xi", real=True)
    eta = Symbol("eta_H", real=True)
    rho = Symbol("rho", real=True)
    sigma = Symbol("sigma", real=True)
    coefficients = lorentz["coefficients"]
    vector_A = sympify(coefficients["vector_bubble_A_p2_metric"],
                       locals={"rho": rho, "sigma": sigma})
    vector_B = sympify(coefficients["vector_bubble_B_p_mu_p_nu"],
                       locals={"rho": rho, "sigma": sigma})
    ghost_A = sympify(coefficients["ghost_bubble_A_p2_metric"])
    ghost_B = sympify(coefficients["ghost_bubble_B_p_mu_p_nu"])

    # Re-derive the matter trace from the immutable parent representation
    # dimensions/indices used by M01, without reading primary M08 outputs.
    matter_A = Rational(2, 3) * 6 + Rational(1, 6) * 84
    matter_B = -matter_A

    def counterterms(loop_A, loop_B, parameter):
        field = simplify(-loop_A)
        gauge = simplify(parameter * loop_B + (1 - parameter) * field)
        return field, gauge

    heavy = []
    for row in group["comparisons"]["heavy_heavy_heavy"]["spectrum"]:
        k = q(row["eigenvalue"])
        loop_A = simplify(
            vector_A.subs({rho: xi, sigma: xi}) * k
            + vector_A.subs({rho: xi, sigma: eta}) * (8 - k)
            + ghost_A * k + matter_A
        )
        loop_B = simplify(
            vector_B.subs({rho: xi, sigma: xi}) * k
            + vector_B.subs({rho: xi, sigma: eta}) * (8 - k)
            + ghost_B * k + matter_B
        )
        field, gauge = counterterms(loop_A, loop_B, xi)
        heavy.append({
            "K_HHH_eigenvalue": str(k),
            "multiplicity": row["multiplicity"],
            "loop_A": str(loop_A),
            "loop_B": str(loop_B),
            "delta_Z_quantum_heavy_vector": str(field),
            "multiplicative_delta_Z_xi_candidate": str(gauge),
        })

    light = []
    for row in group["comparisons"]["light_light_light"]["spectrum"]:
        k = q(row["eigenvalue"])
        loop_A = simplify(
            vector_A.subs({rho: eta, sigma: eta}) * k
            + vector_A.subs({rho: xi, sigma: xi}) * (8 - k)
            + ghost_A * 8 + matter_A
        )
        loop_B = simplify(
            vector_B.subs({rho: eta, sigma: eta}) * k
            + vector_B.subs({rho: xi, sigma: xi}) * (8 - k)
            + ghost_B * 8 + matter_B
        )
        field, gauge = counterterms(loop_A, loop_B, eta)
        light.append({
            "K_LLL_eigenvalue": str(k),
            "multiplicity": row["multiplicity"],
            "loop_A": str(loop_A),
            "loop_B": str(loop_B),
            "delta_Z_quantum_light_vector": str(field),
            "multiplicative_delta_Z_eta_H_candidate": str(gauge),
        })

    payload = {
        "schema_version": 1,
        "outcome": "M08_CANONICAL_TWO_POINT_INDEPENDENT_REPLAY_COMPLETE",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "method": (
            "independent_raw_SO10_group_contractions_plus_auxiliary_mass_"
            "Taylor_Lorentz_poles"
        ),
        "primary_canonical_assembly_imported": False,
        "inputs": {
            "independent_group_sha256": group["artifact_sha256"],
            "independent_Lorentz_sha256": lorentz["artifact_sha256"],
        },
        "heavy_vector_blocks": heavy,
        "light_vector_blocks": light,
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_canonical_two_point_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["outcome"])
    print("HEAVY_BLOCKS", len(heavy))
    print("LIGHT_BLOCKS", len(light))
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
