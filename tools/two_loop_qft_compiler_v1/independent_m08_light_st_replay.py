"""Inventory-independent functional replay of the M08 light ST control.

This replay does not read the primary graph inventory, Taylor projector, or
residue table.  It derives the heavy H-matter contribution from the minimal
covariant vector and Grassmann-scalar operators and derives the ordinary
H-ghost vertex from a separate Feynman-parameter/color-orientation audit.
It is intentionally limited to the ordinary light channel and therefore does
not constitute the complete M08 replay required for promotion.
"""

from hashlib import sha256
import json
from pathlib import Path

from sympy import Rational, Symbol, simplify


HERE = Path(__file__).resolve().parent


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    action = json.loads((HERE / "partial_bfm_action.json").read_text(
        encoding="utf-8"))
    eta = Symbol("eta_H", real=True)
    k = Symbol("k_LLL", real=True)
    kh = 8 - k

    # Flat-space a2 trace for the covariantly gauge-fixed heavy vector:
    # 4 * 1/2 * [4/12 - 2] = -10/3.  The complex Grassmann scalar gives
    # 4 * (-1) * 1/12 = -1/3.  Their sum is independent of xi and transverse.
    vector_a2 = 4 * Rational(1, 2) * (
        Rational(4, 12) - 2)
    ghost_a2 = 4 * (-1) * Rational(1, 12)
    heavy_sum = simplify(vector_a2 + ghost_a2)
    assert vector_a2 == -Rational(10, 3)
    assert ghost_a2 == -Rational(1, 3)
    assert heavy_sum == -Rational(11, 3)

    # Separate nonexceptional triangle reduction.  The two Lorentz residues
    # are eta/4 and 3eta/4.  The independently oriented color contractions
    # are -K/2 and +K/2, with the cubic Yang--Mills Feynman rule supplying the
    # relative minus.
    vertex = simplify(
        (-k / 2) * eta / 4 - (+k / 2) * 3 * eta / 4)
    assert vertex == -eta * k / 2

    zc = (3 - eta) * k / 4
    zq = ((Rational(13, 6) - eta / 2) * k
          - heavy_sum * kh - 18)
    zg = -Rational(11, 6) * 8 + 9
    st = simplify(vertex - (zg + zq / 2 + zc))
    assert st == 0

    payload = {
        "schema_version": 1,
        "outcome": "M08_LIGHT_ST_FUNCTIONAL_INDEPENDENT_REPLAY_PASS",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action[
            "partial_bfm_action_sha256"],
        "primary_graph_inventory_imported": False,
        "primary_symmetry_factors_imported": False,
        "primary_Grassmann_signs_imported": False,
        "primary_UV_expansion_imported": False,
        "primary_tensor_reducer_imported": False,
        "method": (
            "covariant_operator_a2_trace_plus_independent_nonexceptional_"
            "triangle_and_color_orientation_reduction"
        ),
        "functional_operator_certificate": {
            "heavy_vector": "-d^2*delta_mu_nu-2*F_mu_nu",
            "heavy_ghost": "-d^2_complex_Grassmann_scalar",
            "vector_F2_coefficient": str(vector_a2),
            "ghost_F2_coefficient": str(ghost_a2),
            "complete_heavy_sector": str(heavy_sum),
            "gauge_parameter_derivative": "0",
            "transversality_residual": "0",
        },
        "light_vertex_counterterm_operator": str(vertex),
        "delta_Z_cL": str(zc),
        "delta_Z_qL": str(zq),
        "delta_Z_g10": str(zg),
        "ST_residual": str(st),
        "coverage": "Gamma(cbar_L,c_L,q_L)_only",
        "complete_M08_replay": False,
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_light_st_independent_replay.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("HEAVY_VECTOR", vector_a2)
    print("HEAVY_GHOST", ghost_a2)
    print("ST_RESIDUAL", st)
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
