"""Stage-A *diagnostic* one-loop crossing, with complete coarse PS multiplets.

This is not a benchmark-matched result: split scalar and gauge thresholds,
finite matching, and physical MI/MU definitions are deliberately omitted.
"""

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ps_coefficients():
    # b = -11 C2(G)/3 + 2 sum_Weyl T/3 + sum_complex T/3.
    # Three 16_F generations give sum_Weyl T=6 for each PS factor.
    fermion = 2 * 6 / 3
    # Complex 10_H: (6,1,1)+(1,2,2), indices (1,1,1).
    ten = (1, 1, 1)
    # Complex 126_H: (6,1,1)+(10,3,1)+(10bar,1,3)+(15,2,2).
    # SU4 indices: 1+3*3+3*3+4*4 = 35.
    # SU2L/R indices: 10*2+15*2*(1/2) = 35 each.
    sigma = (35, 35, 35)
    assert ten == (1, 1, 1) and sigma == (35, 35, 35)
    return tuple(-11*c2/3 + fermion + (a+b)/3
                 for c2, a, b in zip((4, 2, 2), ten, sigma))


def crossing():
    # MSbar inputs used by the PDG 2025 GUT review; this is a diagnostic
    # frozen-input set, not a precision 2026 electroweak fit.
    mz = 91.1876
    alpha_em_inv = 127.930
    sin2 = 0.23122
    alpha_s = 0.1180
    a1 = 3*(1-sin2)*alpha_em_inv/5
    a2 = sin2*alpha_em_inv
    a3 = 1/alpha_s
    b1, b2, b3 = 41/10, -19/6, -7
    b4, bl, br = ps_coefficients()
    assert bl == br and abs((bl-b4)-22/3) < 1e-12
    # D parity plus Y=T3R+(B-L)/2 gives
    # a1(MI)=(3/5)a2(MI)+(2/5)a3(MI).
    den_i = b1-3*b2/5-2*b3/5
    ti = 2*math.pi*(a1-3*a2/5-2*a3/5)/den_i
    ai4 = a3-b3*ti/(2*math.pi)
    ail = a2-b2*ti/(2*math.pi)
    den_u = bl-b4
    tu = 2*math.pi*(ail-ai4)/den_u
    au4 = ai4-b4*tu/(2*math.pi)
    aul = ail-bl*tu/(2*math.pi)
    assert abs(au4-aul) < 1e-12
    out = {
        "authority": "coarse_complete_multiplets_only_not_canonical_threshold_matching",
        "inputs": {"MZ_GeV": mz, "alpha_em_MSbar_inverse_MZ": alpha_em_inv,
                   "sin2theta_MSbar_MZ": sin2, "alpha_s_MSbar_MZ": alpha_s},
        "SM_one_loop_b": [b1, b2, b3],
        "PS_one_loop_b_4_L_R": [b4, bl, br],
        "log_MI_over_MZ": ti,
        "MI_GeV": mz*math.exp(ti),
        "log_MU_over_MI": tu,
        "MU_over_MI": math.exp(tu),
        "MU_GeV": mz*math.exp(ti+tu),
        "alpha_U_inverse": au4,
        "g_U": math.sqrt(4*math.pi/au4),
        "vector_hierarchy_mass_ratio_range": [math.sqrt(50/3), math.sqrt(50/0.6)],
        "inverse_coupling_difference_shift_needed_for_vector_ratio_range": [
            den_u*math.log(math.exp(tu)/math.sqrt(50/0.6))/(2*math.pi),
            den_u*math.log(math.exp(tu)/math.sqrt(50/3))/(2*math.pi),
        ],
        "comparison_only": "The canonical vector Gram hierarchy is much shorter than the coarse crossing ratio; split thresholds and matching are essential before judging the point."
    }
    assert ti > 0 and tu > 0 and au4 > 1
    return out


def main():
    result = crossing()
    (HERE / "coarse_one_loop.json").write_text(json.dumps(result, indent=2)+"\n")
    print("COARSE_CROSSING", "MI_GeV", result["MI_GeV"],
          "MU_over_MI", result["MU_over_MI"],
          "alpha_U_inverse", result["alpha_U_inverse"])


if __name__ == "__main__":
    main()
