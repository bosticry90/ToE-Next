"""Independent exact replay of the parent gauge/scalar beta coefficients."""

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    q = Fraction
    c_a = q(8)
    # Entries are (multiplicity in the real-field formula, T, C2).
    fermions = [(3, q(2), q(45, 8))]
    scalars = [
        (1, q(12), q(10)),       # real 54
        (2, q(35), q(25, 2)),    # complex 126
        (2, q(1), q(9, 2)),      # complex 10
        (2, q(0), q(0)),         # complex singlet
    ]
    sf = sum((n*t for n, t, _ in fermions), q(0))
    cf = sum((n*t*c for n, t, c in fermions), q(0))
    ss = sum((n*t for n, t, _ in scalars), q(0))
    cs = sum((n*t*c for n, t, c in scalars), q(0))
    b = -q(11, 3)*c_a + q(2, 3)*sf + q(1, 6)*ss
    B = (-q(34, 3)*c_a*c_a + 2*cf + q(10, 3)*c_a*sf
         + 2*cs + q(1, 3)*c_a*ss)
    data = json.loads((HERE / "two_loop_boundary.json").read_text())
    assert str(b) == data["part_A_gauge_scalar"]["parent_b_one_loop"]
    assert str(B) == data["part_A_gauge_scalar"]["parent_B_two_loop_yukawa_independent"]
    assert b == -q(34, 3)
    assert B == q(10405, 6)
    assert data["part_B_yukawa"]["real_coordinates"] == [
        "Tr(Y10^dagger Y10)",
        "Tr(Y126^dagger Y126)",
        "Re Tr(Y10^dagger Y126)",
        "Im Tr(Y10^dagger Y126)",
    ]
    print("INDEPENDENT_PARENT_BETA_PASS", b, B)
    print("YUKAWA_GRAM_BASIS_REPLAY_PASS")


if __name__ == "__main__":
    main()
