"""Index-summed vertex-signature catalog derived from the frozen layer-3 action.

The catalog is deliberately tensor level: ``H[a]`` denotes a physical heavy
mass eigenstate with ``a=0..289`` and carries its own mass-table lookup.  This
is the standard compact representation of an exact sum over component fields;
it avoids materializing dense cubic and quartic tensors while preserving every
ordered internal propagator and mass identifier in generated diagrams.
"""

from hashlib import sha256
from itertools import combinations_with_replacement
import json
from pathlib import Path


ACTION_HASH = "2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491"
HERE = Path(__file__).resolve().parent


FIELD_DOMAINS = {
    "q": {"role": "unbroken_SM_quantum_vector", "range": 12,
          "statistics": "boson", "propagator": "q", "mass": "0"},
    "V": {"role": "heavy_quantum_vector", "range": 33,
          "statistics": "boson", "propagator": "V", "mass": "M_V[i]^2"},
    "G": {"role": "orbit_Goldstone", "range": 33,
          "statistics": "boson", "propagator": "G",
          "mass": "xi*M_V[i]^2"},
    "H": {"role": "heavy_physical_scalar", "range": 290,
          "statistics": "boson", "propagator": "H", "mass": "m_H[a]^2"},
    "h": {"role": "retained_light_Higgs_real", "range": 4,
          "statistics": "boson", "propagator": "h", "mass": "0"},
    "p": {"role": "PQ_Goldstone_real", "range": 1,
          "statistics": "boson", "propagator": "p", "mass": "0"},
    "u": {"role": "heavy_ghost", "range": 33,
          "statistics": "fermionic_ghost", "propagator": "U",
          "mass": "xi*M_V[i]^2"},
    "ubar": {"role": "heavy_antighost", "range": 33,
             "statistics": "fermionic_ghost", "propagator": "U",
             "mass": "xi*M_V[i]^2"},
    "c": {"role": "light_SM_ghost", "range": 12,
          "statistics": "fermionic_ghost", "propagator": "C", "mass": "0"},
    "cbar": {"role": "light_SM_antighost", "range": 12,
             "statistics": "fermionic_ghost", "propagator": "C", "mass": "0"},
}

SCALARS = ("G", "H", "h", "p")
GAUGES = ("q", "V")


def canonical_signature(fields):
    return tuple(sorted(fields))


def build_catalog():
    rows = {}

    def add(name, external, internal, source):
        ordered = tuple(internal)
        internal = canonical_signature(ordered)
        key = (external, internal)
        assert key not in rows, (key, rows.get(key), name)
        rows[key] = {
            "vertex_id": name,
            "valence": external + len(internal),
            "external_background_legs": external,
            "internal_fields": list(internal),
            "ordered_internal_fields": list(ordered),
            "source": source,
            "coefficient_policy": "on_demand_tensor_from_PartialBFMAction",
        }

    # Cubic invariant and gauge-fixing vertices without external backgrounds.
    add("YM_q_q_q", 0, ("q", "q", "q"), "Yang_Mills")
    add("YM_q_V_V", 0, ("q", "V", "V"), "Yang_Mills")
    add("YM_V_V_V", 0, ("V", "V", "V"), "Yang_Mills")
    for scalar in ("G", "H", "h"):
        add(f"KIN_q_{scalar}_{scalar}", 0, ("q", scalar, scalar),
            "scalar_kinetic_VSS")
    for left, right in combinations_with_replacement(SCALARS, 2):
        add(f"KIN_V_{left}_{right}", 0, ("V", left, right),
            "scalar_kinetic_VSS")
    for ga, gb in (("q", "V"), ("V", "V")):
        for scalar in SCALARS:
            add(f"VEV_{ga}_{gb}_{scalar}", 0, (ga, gb, scalar),
                "scalar_kinetic_VVS")
    for triple in combinations_with_replacement(SCALARS, 3):
        add("POT3_" + "_".join(triple), 0, triple,
            "PARENT_ACTION_V1_third_derivative")
    for mediator in ("V",) + SCALARS:
        add(f"HGH_ubar_u_{mediator}", 0, ("ubar", "u", mediator),
            "equivariant_heavy_FP")
    add("HGF_cbar_c_q", 0, ("cbar", "c", "q"), "ordinary_H_FP")

    # Cubic vertices with one or two external unbroken background fields.
    add("BFM_A_q_q", 1, ("q", "q"), "background_Yang_Mills")
    add("BFM_A_V_V", 1, ("V", "V"), "background_Yang_Mills")
    for scalar in ("G", "H", "h"):
        add(f"BFM_A_{scalar}_{scalar}", 1, (scalar, scalar),
            "background_scalar_kinetic")
    for scalar in SCALARS:
        add(f"BFM_A_V_{scalar}", 1, ("V", scalar),
            "background_VVS")
    add("BFM_A_ubar_u", 1, ("ubar", "u"), "equivariant_heavy_FP")
    add("BFM_A_cbar_c", 1, ("cbar", "c"), "ordinary_H_FP")

    # Quartic vertices without external backgrounds.
    for four in combinations_with_replacement(GAUGES, 4):
        if four.count("V") == 1:
            continue
        add("YM4_" + "_".join(four), 0, four, "Yang_Mills")
    for ga, gb in combinations_with_replacement(GAUGES, 2):
        for left, right in combinations_with_replacement(SCALARS, 2):
            fields = (ga, gb, left, right)
            add("KIN4_" + "_".join(fields), 0, fields,
                "scalar_kinetic_VVSS")
    for four in combinations_with_replacement(SCALARS, 4):
        add("POT4_" + "_".join(four), 0, four,
            "PARENT_ACTION_V1_fourth_derivative")
    add("HGH4_ubar_u_V_V", 0, ("ubar", "u", "V", "V"),
        "equivariant_heavy_FP")
    add("HGH4_ubar_u_ubar_u", 0, ("ubar", "u", "ubar", "u"),
        "equivariant_quartic_heavy_ghost")

    # Quartic vertices with background legs.
    for triple in combinations_with_replacement(GAUGES, 3):
        if triple.count("V") == 1:
            continue
        add("BFM4_A_" + "_".join(triple), 1, triple,
            "background_Yang_Mills")
    for quantum in GAUGES:
        for left, right in combinations_with_replacement(SCALARS, 2):
            add(f"BFM4_A_{quantum}_{left}_{right}", 1,
                (quantum, left, right), "background_scalar_kinetic")
    add("BFM4_A_ubar_u_V", 1, ("ubar", "u", "V"),
        "equivariant_heavy_FP")
    add("BFM4_A_cbar_c_q", 1, ("cbar", "c", "q"),
        "ordinary_H_FP")
    for ga, gb in combinations_with_replacement(GAUGES, 2):
        add(f"BFM4_A_A_{ga}_{gb}", 2, (ga, gb),
            "background_Yang_Mills")
    for left, right in combinations_with_replacement(("G", "H", "h"), 2):
        add(f"BFM4_A_A_{left}_{right}", 2, (left, right),
            "background_scalar_kinetic")
    add("BFM4_A_A_ubar_u", 2, ("ubar", "u"),
        "equivariant_heavy_FP")
    add("BFM4_A_A_cbar_c", 2, ("cbar", "c"), "ordinary_H_FP")

    result = sorted(rows.values(), key=lambda row: row["vertex_id"])
    assert all(row["valence"] in (3, 4) for row in result)
    return result


def manifest():
    catalog = build_catalog()
    payload = {
        "outcome": "LAYER4_INDEX_SUMMED_VERTEX_CATALOG_PASS",
        "immutable_partial_bfm_action_sha256": ACTION_HASH,
        "field_domains": FIELD_DOMAINS,
        "vertex_signatures": catalog,
        "scope": "gauge_scalar_C1_GS_no_Yukawa_vertices",
        "representation": (
            "exact_index_summed_physical_mass_basis; each propagator dummy "
            "index has an explicit finite domain and mass-table identifier"
        ),
        "not_claimed": [
            "complete_nonYukawa_boundary_including_fermion_gauge_loops",
            "counterterm_coefficients", "tensor_reduction", "integral_values",
        ],
    }
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["vertex_catalog_sha256"] = sha256(packed.encode()).hexdigest()
    return payload


def main():
    payload = manifest()
    (HERE / "layer4_vertex_catalog.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["outcome"])
    print("VERTEX_SIGNATURES", len(payload["vertex_signatures"]))
    print("VERTEX_CATALOG_SHA256", payload["vertex_catalog_sha256"])


if __name__ == "__main__":
    main()
