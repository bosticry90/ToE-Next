"""Exact regression controls for the all-parent-invariant bilinear oracle."""

import sys
from pathlib import Path

from sympy import I, zeros

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "canonical_so10_scalar_reconstruction"))
from verify_eta1_doublet_mixing import doublet_form

from parent_bilinear_oracle import (
    State, bilinear_coefficients,
)


def vector_direction(index, value=1):
    x = [0]*10
    x[index] = value
    return State(zeros(10), {}, tuple(x), 0)


def sigma_direction(form):
    return State(zeros(10), form, (0,)*10, 0)


def main():
    weak = vector_direction(6)
    color = vector_direction(0)
    bw = bilinear_coefficients(weak, weak)
    bc = bilinear_coefficients(color, color)
    assert bw["mphi2"] == bc["mphi2"] == 2
    assert (bw["muPhiPhi"], bc["muPhiPhi"]) == (6, -4)
    assert (bw["lambdaPhiphi2"], bc["lambdaPhiphi2"]) == (18, 8)
    assert bw["lambdaSigmaphi2"] == bc["lambdaSigmaphi2"] == 32
    assert (bw["z6"], bw["zK"], bw["zD"]) == (2, 6, 0)
    assert (bc["z6"], bc["zK"], bc["zD"]) == (2, -4, 0)
    bi = bilinear_coefficients(vector_direction(6, I),
                               vector_direction(6, I))
    assert (bi["z6"], bi["zK"]) == (-2, -6)

    e = sigma_direction(doublet_form(6))
    be = bilinear_coefficients(e, e)
    assert be["z4"] == -60  # raw E is sqrt(3) times the normalized doublet basis
    eta = bilinear_coefficients(e, weak)
    assert eta["zEta"] == 192
    assert all(eta[n] == 0 for n in ("z6", "z4", "zK", "zD"))
    print("ORACLE_CONTROLS_PASS: 10 color/weak self-block, z4, z6, zK, eta")


if __name__ == "__main__":
    main()
