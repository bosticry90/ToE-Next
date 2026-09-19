"""Check every action-v1 invariant family against exact D5 singlet counts.

This is an inventory cross-check, not a replacement for explicit tensor rank.
"""

from itertools import combinations_with_replacement

from count_d5_singlets import NAMES, PQ, multiset_character, singlet_multiplicity


SLOTS = {
    ("Phi", "Phi"): ("p2",),
    ("Sigma", "Sigma*"): ("N",),
    ("phi", "phi*"): ("u",),
    ("S", "S*"): ("absS2",),
    ("Phi", "Phi", "Phi"): ("p3",),
    ("Phi", "phi", "phi*"): ("Phi_phi_phi*",),
    ("phi", "phi", "S*"): ("t_S*",),
    ("phi*", "phi*", "S"): ("conj_t_S",),
    ("Phi", "Phi", "Phi", "Phi"): ("p2_squared", "p4"),
    ("Phi", "Phi", "Sigma", "Sigma*"): ("p2_N", "L_PhiSigma"),
    ("Phi", "Phi", "phi", "phi*"): ("p2_u", "phi*_Phi2_phi"),
    ("Phi", "Phi", "S", "S*"): ("p2_absS2",),
    ("Phi", "Sigma", "Sigma", "S"): ("Phi_T_S",),
    ("Phi", "Sigma*", "Sigma*", "S*"): ("conj_Phi_T_S",),
    ("Phi", "phi", "phi", "S*"): ("Phi_phi_phi_S*",),
    ("Phi", "phi*", "phi*", "S"): ("conj_Phi_phi_phi_S*",),
    ("Sigma", "Sigma", "Sigma*", "Sigma*"): ("Q0", "Q1", "Q2", "X131"),
    ("Sigma", "Sigma", "Sigma*", "phi"): ("E",),
    ("Sigma", "Sigma", "phi", "phi"): ("T_phi_phi",),
    ("Sigma", "Sigma*", "Sigma*", "phi*"): ("conj_E",),
    ("Sigma", "Sigma*", "phi", "phi*"): ("N_u", "phi*_K_phi"),
    ("Sigma", "Sigma*", "S", "S*"): ("N_absS2",),
    ("Sigma*", "Sigma*", "phi*", "phi*"): ("conj_T_phi_phi",),
    ("phi", "phi", "phi*", "phi*"): ("u_squared", "abs_t_squared"),
    ("phi", "phi*", "S", "S*"): ("u_absS2",),
    ("S", "S", "S*", "S*"): ("absS4",),
}


def main():
    assert len(SLOTS) == 26
    for degree in (2, 3, 4):
        for fields in combinations_with_replacement(NAMES, degree):
            if sum(PQ[name] for name in fields) != 0:
                continue
            expected = singlet_multiplicity(multiset_character(fields))
            actual = len(SLOTS.get(fields, ()))
            assert actual == expected, (fields, actual, expected)
    assert sum(map(len, SLOTS.values())) == 34
    print("ACTION_INVENTORY_MATCHES_ALL_44_NEUTRAL_MULTISETS: 26 nonzero families; 34 singlet slots")


if __name__ == "__main__":
    main()
