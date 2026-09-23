"""Primary partial-BFM M08 ghost--vector three-point pole assembly.

This is a calculation preflight, not an M08 adjudicator.  It combines the
action-derived graph inventory, exact Spin(10) structure tensors, and the
local Lorentz kernels.  Results are retained by topology and compared with
the counterterm tensors implied by the already frozen two-point operators.
"""

from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from sympy import Rational, Symbol, lambdify, simplify

from m08_brst_lorentz_kernel import (
    P, Q, gauge_triangle, ghost_triangle, quartic_ghost_bubble,
    swordfish_external_antighost_on_seagull,
    swordfish_external_ghost_on_seagull, vector_swordfish,
)
from partial_bfm_action import PartialBFMAction


HERE = Path(__file__).resolve().parent
xi = Symbol("xi")
eta = Symbol("eta_H")


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def tensor_norm(tensor):
    return float(np.max(np.abs(tensor))) if tensor.size else 0.0


def pq_coefficients(vector):
    return simplify(vector[0]), simplify(vector[1])


def evaluate(expression, xv, ev):
    return float(lambdify((xi, eta), expression, "numpy")(xv, ev))


def vertex_counterterm(tree, zleft, zright, zvector, zg):
    return (
        zg * tree
        + Rational(1, 2) * np.einsum("ia,aje->ije", zleft, tree)
        + Rational(1, 2) * np.einsum("ja,iae->ije", zright, tree)
        + Rational(1, 2) * np.einsum("ef,ijf->ije", zvector, tree)
    )


def projected_operator(tree, tensor):
    gram = np.einsum("ije,ijf->ef", tree, tree)
    rhs = np.einsum("ije,ijf->ef", tree, tensor)
    operator = np.linalg.pinv(gram, rcond=1e-11) @ rhs
    reconstructed = np.einsum("ijf,fe->ije", tree, operator)
    return operator, tensor_norm(tensor - reconstructed)


def main():
    action = PartialBFMAction()
    ids = [action.invariant.vector_id(index) for index in range(45)]
    structure = np.asarray([[[action.structure(a, b, c) for c in ids]
                             for b in ids] for a in ids])
    light = np.arange(12)
    heavy = np.arange(12, 45)

    # Ghost generators, with axes (antighost, ghost, vector).
    th = structure[np.ix_(heavy, heavy, heavy)]
    tq = structure[np.ix_(heavy, light, heavy)].transpose(0, 2, 1)
    tl = structure[np.ix_(light, light, light)].transpose(0, 2, 1)

    def gtri(tx, te):
        return np.einsum("iax,bjx,abe->ije", tx, tx, te,
                         optimize=True)

    def vtri(tx, ty, vector_x, vector_y, external):
        fxy = structure[np.ix_(vector_x, vector_y, external)]
        return np.einsum("imx,mjy,xye->ije", tx, ty, fxy,
                         optimize=True)

    # Differentiated seagull tensors (antighost,ghost,external,internal).
    f_hhl = structure[np.ix_(heavy, heavy, light)]
    f_lhh = structure[np.ix_(light, heavy, heavy)]
    shh = (
        np.einsum("iea,axj->ijex", f_hhl, f_lhh, optimize=True)
        + np.einsum("ixa,aej->ijex", f_hhl, f_lhh, optimize=True)
    )
    f_hhh = structure[np.ix_(heavy, heavy, heavy)]
    f_hlh = structure[np.ix_(heavy, light, heavy)]
    shq = np.einsum("ime,maj->ijea", f_hhh, f_hlh,
                    optimize=True)
    sqq = (
        np.einsum("iam,mbj->ijab", f_hlh, f_hlh, optimize=True)
        + np.einsum("ibm,maj->ijab", f_hlh, f_hlh, optimize=True)
    )

    def sghost_left(seagull, tx):
        return np.einsum("imex,mjx->ije", seagull, tx,
                         optimize=True)

    def sghost_right(tx, seagull):
        return np.einsum("imx,mjex->ije", tx, seagull,
                         optimize=True)

    def svector(seagull, vx, vy, external):
        fxy = structure[np.ix_(vx, vy, external)]
        return np.einsum("ijxy,xye->ije", seagull, fxy,
                         optimize=True)

    # Ordered direct/exchange quartic-heavy-ghost tensors contracted with the
    # cubic vertex.  The common xi and the closed-loop sign are attached in
    # the topology ledger below.
    f_hhl_for_q4 = structure[np.ix_(heavy, heavy, light)]

    # The exchange contraction above is clearer and less error-prone with
    # explicit labels in einsum's integer-list interface.
    def quartic_exchange(te):
        return -np.einsum(
            structure[np.ix_(heavy, heavy, light)], [0, 3, 4],
            structure[np.ix_(heavy, heavy, light)], [1, 2, 4],
            te, [2, 3, 5], [0, 1, 5], optimize=True)

    def quartic_direct(te):
        return np.einsum(
            structure[np.ix_(heavy, heavy, light)], [0, 1, 4],
            structure[np.ix_(heavy, heavy, light)], [2, 3, 4],
            te, [2, 3, 5], [0, 1, 5], optimize=True)

    rules = {
        "H": (Rational(0), Rational(1)),
        "L_on_H": (Rational(1), Rational(-1)),
        "L": (Rational(1), Rational(0)),
    }

    khhh = np.einsum("abc,dbc->ad", th, th)
    khhl = np.einsum("iax,jax->ij", tq, tq)
    klll = np.einsum("abc,dbc->ad", tl, tl)
    klhh = np.einsum("aij,bij->ab",
                     structure[np.ix_(light, heavy, heavy)],
                     structure[np.ix_(light, heavy, heavy)])
    identity_h = np.eye(33)
    identity_l = np.eye(12)

    def z_u_h(xv, ev):
        return (float((3 - xv) / 4) * khhh
                + float((3 - ev) / 4) * khhl)

    def z_c_l(xv, ev):
        del xv
        return float((3 - ev) / 4) * klll

    def z_q_h(xv, ev):
        return (-float(xv / 4) * khhh - float(ev / 2) * khhl
                - 2 * float(xv) * identity_h + khhh / 12
                - 4 * identity_h / 3)

    def z_q_l(xv, ev):
        return (-float(ev / 2) * klll - float(xv / 2) * klhh
                - 2 * identity_l / 3)

    processes = {}

    def assemble(name, tree, ext_rule, pieces, ghost_z, vector_z):
        ledger = []
        for row in pieces:
            cp, cq = pq_coefficients(row["lorentz"])
            sign = row.get("sign", 1)
            ledger.append({
                "topology": row["topology"],
                "assignment": row["assignment"],
                "p_coefficient": str(simplify(sign * cp)),
                "q_coefficient": str(simplify(sign * cq)),
                "color_tensor_sha256": digest(np.round(
                    row["color"], 14).tolist()),
                "maximum_color_entry": format(tensor_norm(row["color"]),
                                                ".12g"),
            })
        samples = []
        for xv, ev in ((Rational(1, 2), Rational(1, 2)),
                       (Rational(1), Rational(1)),
                       (Rational(2), Rational(2)),
                       (Rational(1), Rational(2))):
            pn = np.zeros_like(tree)
            qn = np.zeros_like(tree)
            for row in pieces:
                cp, cq = pq_coefficients(row["lorentz"])
                sign = row.get("sign", 1)
                pn += evaluate(sign * cp, xv, ev) * row["color"]
                qn += evaluate(sign * cq, xv, ev) * row["color"]
            op_p, residual_p = projected_operator(tree, pn)
            op_q, residual_q = projected_operator(tree, qn)
            predicted = vertex_counterterm(
                tree, ghost_z(xv, ev), ghost_z(xv, ev),
                vector_z(xv, ev), -Rational(17, 3))
            predicted = np.asarray(predicted, dtype=float)
            ap, bp = map(float, ext_rule)
            predicted_p = ap * predicted
            predicted_q = bp * predicted
            samples.append({
                "xi": str(xv), "eta_H": str(ev),
                "p_tree_operator_spectrum": [
                    format(float(value), ".12g")
                    for value in np.linalg.eigvalsh((op_p + op_p.T) / 2)],
                "q_tree_operator_spectrum": [
                    format(float(value), ".12g")
                    for value in np.linalg.eigvalsh((op_q + op_q.T) / 2)],
                "p_out_of_tree_operator_residual": format(residual_p, ".12g"),
                "q_out_of_tree_operator_residual": format(residual_q, ".12g"),
                "ST_actual_minus_counterterm_p_maximum_residual": format(
                    tensor_norm(pn - predicted_p), ".12g"),
                "ST_actual_minus_counterterm_q_maximum_residual": format(
                    tensor_norm(qn - predicted_q), ".12g"),
                "ST_actual_plus_counterterm_p_maximum_residual": format(
                    tensor_norm(pn + predicted_p), ".12g"),
                "ST_actual_plus_counterterm_q_maximum_residual": format(
                    tensor_norm(qn + predicted_q), ".12g"),
            })
        processes[name] = {
            "tree_rule": [str(value) for value in ext_rule],
            "topology_ledger": ledger,
            "factorized_pole_operator_sha256": digest(ledger),
            "sample_tree_operator_projections": samples,
        }

    # Heavy external vector.
    pieces_v = [
        {"topology": "ghost_vector_triangle", "assignment": "internal_V",
         "color": gtri(th, th),
         "lorentz": ghost_triangle(rules["H"], rules["H"], xi)},
        {"topology": "ghost_vector_triangle", "assignment": "internal_q",
         "color": gtri(tq, th),
         "lorentz": ghost_triangle(rules["H"], rules["L_on_H"], eta)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_V_V", "color": vtri(th, th, heavy, heavy, heavy),
         "lorentz": gauge_triangle(rules["H"], rules["H"], rules["H"],
                                    xi, xi)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_V_q", "color": vtri(th, tq, heavy, light, heavy),
         "lorentz": gauge_triangle(rules["H"], rules["H"],
                                    rules["L_on_H"], xi, eta)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_q_V", "color": vtri(tq, th, light, heavy, heavy),
         "lorentz": gauge_triangle(rules["H"], rules["L_on_H"],
                                    rules["H"], eta, xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "VV_ext_antighost_on_seagull",
         "color": sghost_left(shh, th),
         "lorentz": swordfish_external_antighost_on_seagull(rules["H"], xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "VV_ext_ghost_on_seagull",
         "color": sghost_right(th, shh),
         "lorentz": swordfish_external_ghost_on_seagull(rules["H"], xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "Vq_ext_antighost_on_seagull",
         "color": sghost_left(shq, tq),
         "lorentz": swordfish_external_antighost_on_seagull(
             rules["L_on_H"], eta)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "Vq_ext_ghost_on_seagull",
         "color": sghost_right(tq, shq),
         "lorentz": swordfish_external_ghost_on_seagull(
             rules["L_on_H"], eta)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "VV_three_vector", "color": svector(shh, heavy, heavy, heavy),
         "lorentz": vector_swordfish(xi, xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "Vq_three_vector", "color": svector(shq, heavy, light, heavy),
         "lorentz": vector_swordfish(xi, eta)},
        {"topology": "equivariant_quartic_ghost_bubble",
         "assignment": "direct", "color": quartic_direct(th),
         "lorentz": quartic_ghost_bubble(rules["H"]), "sign": -xi},
        {"topology": "equivariant_quartic_ghost_bubble",
         "assignment": "exchange", "color": quartic_exchange(th),
         "lorentz": quartic_ghost_bubble(rules["H"]), "sign": -xi},
    ]
    assemble("Gamma_ubarH_uH_VH", th, rules["H"], pieces_v, z_u_h, z_q_h)

    # Heavy ghosts with a light quantum vector.
    pieces_q = [
        {"topology": "ghost_vector_triangle", "assignment": "internal_V",
         "color": gtri(th, tq),
         "lorentz": ghost_triangle(rules["L_on_H"], rules["H"], xi)},
        {"topology": "ghost_vector_triangle", "assignment": "internal_q",
         "color": gtri(tq, tq),
         "lorentz": ghost_triangle(rules["L_on_H"], rules["L_on_H"], eta)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_V_V", "color": vtri(th, th, heavy, heavy, light),
         "lorentz": gauge_triangle(rules["L_on_H"], rules["H"], rules["H"],
                                    xi, xi)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_q_q", "color": vtri(tq, tq, light, light, light),
         "lorentz": gauge_triangle(rules["L_on_H"], rules["L_on_H"],
                                    rules["L_on_H"], eta, eta)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "Vq_ext_antighost_on_seagull",
         "color": np.einsum("imxe,mjx->ije", shq, th,
                             optimize=True),
         "lorentz": swordfish_external_antighost_on_seagull(rules["H"], xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "Vq_ext_ghost_on_seagull",
         "color": np.einsum("imx,mjxe->ije", th,
                             shq, optimize=True),
         "lorentz": swordfish_external_ghost_on_seagull(rules["H"], xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "qq_ext_antighost_on_seagull",
         "color": sghost_left(sqq, tq),
         "lorentz": swordfish_external_antighost_on_seagull(
             rules["L_on_H"], eta)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "qq_ext_ghost_on_seagull",
         "color": sghost_right(tq, sqq),
         "lorentz": swordfish_external_ghost_on_seagull(
             rules["L_on_H"], eta)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "VV_three_vector", "color": svector(shh, heavy, heavy, light),
         "lorentz": vector_swordfish(xi, xi)},
        {"topology": "seagull_cubic_swordfish",
         "assignment": "qq_three_vector", "color": svector(sqq, light, light, light),
         "lorentz": vector_swordfish(eta, eta)},
        {"topology": "equivariant_quartic_ghost_bubble",
         "assignment": "direct", "color": quartic_direct(tq),
         "lorentz": quartic_ghost_bubble(rules["L_on_H"]), "sign": -xi},
        {"topology": "equivariant_quartic_ghost_bubble",
         "assignment": "exchange", "color": quartic_exchange(tq),
         "lorentz": quartic_ghost_bubble(rules["L_on_H"]), "sign": -xi},
    ]
    assemble("Gamma_ubarH_uH_qL", tq, rules["L_on_H"], pieces_q,
             z_u_h, z_q_l)

    # Ordinary light H ghost vertex: the two derived diagrams are a useful
    # exact calibration of group orientation and graph signs.
    pieces_l = [
        {"topology": "ghost_vector_triangle", "assignment": "internal_q",
         "color": gtri(tl, tl),
         "lorentz": ghost_triangle(rules["L"], rules["L"], eta)},
        {"topology": "one_ghost_two_vector_triangle",
         "assignment": "internal_q_q", "color": vtri(tl, tl, light, light, light),
         "lorentz": gauge_triangle(rules["L"], rules["L"], rules["L"],
                                    eta, eta)},
    ]
    assemble("Gamma_cbarL_cL_qL", tl, rules["L"], pieces_l, z_c_l, z_q_l)

    # Store known two-point operators symbolically for the later ST solver.
    two_point_formulas = {
        "Z_uH": "(3-xi)/4*K_HHH+(3-eta_H)/4*K_HHL",
        "Z_cL": "(3-eta_H)/4*K_LLL",
        "Z_QH": "-xi/4*K_HHH-eta_H/2*K_HHL-2*xi*I+K_HHH/12-4*I/3",
        "Z_QL": "-eta_H/2*K_LLL-xi/2*K_LHH-2*I/3",
        "Z_g10": "-17/3*I",
    }
    matrix_hashes = {
        "K_HHH": digest(np.round(khhh, 14).tolist()),
        "K_HHL": digest(np.round(khhl, 14).tolist()),
        "K_LLL": digest(np.round(klll, 14).tolist()),
        "K_LHH": digest(np.round(klhh, 14).tolist()),
        "I_H": digest(identity_h.tolist()),
        "I_L": digest(identity_l.tolist()),
    }

    payload = {
        "schema_version": 1,
        "outcome": "M08_PRIMARY_BRST_THREE_POINT_POLE_ASSEMBLY_PREFLIGHT",
        "authority": "IMPLEMENTATION_PREFLIGHT_NO_UVP_M08_AUTHORITY",
        "immutable_partial_BFM_action_sha256": action.manifest()[
            "partial_bfm_action_sha256"],
        "method": (
            "action_derived_complete_1PI_inventory_plus_local_Taylor_"
            "Lorentz_projector_plus_explicit_Spin10_einsum_contractions"
        ),
        "normalization": "g10^3/(16*pi^2*epsilon_bar)",
        "processes": processes,
        "two_point_operator_formulas_for_ST_stage": two_point_formulas,
        "two_point_operator_matrix_hashes": matrix_hashes,
        "scalar_Goldstone_triangles": {
            "inventory_included": True,
            "UV_disposition": (
                "ZERO_BY_LOCAL_DIMENSION_POWER_COUNTING_TWO_DIMENSIONFUL_"
                "GHOST_SCALAR_COUPLINGS"
            ),
        },
        "formal_M08_retry_authorized": False,
        "remaining_before_retry": [
            "independent graph inventory and residue replay",
            "certified ST solution including all seagull normalization signs",
            "direct gauge-parameter-basis closure adjudication",
        ],
    }
    payload["artifact_sha256"] = digest(payload)
    (HERE / "uvp_m08_brst_three_point_primary_preflight.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    for name, row in processes.items():
        print(name, "TOPOLOGIES", len(row["topology_ledger"]))
        for sample in row["sample_tree_operator_projections"]:
            print(" ", sample["xi"], sample["eta_H"],
                  sample["p_out_of_tree_operator_residual"],
                  sample["q_out_of_tree_operator_residual"])
    print("ARTIFACT_SHA256", payload["artifact_sha256"])


if __name__ == "__main__":
    main()
