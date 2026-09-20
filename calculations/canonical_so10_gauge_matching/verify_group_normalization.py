"""Independent exact normalization checks for the tree-level matching gate."""

from sympy import I, Matrix, Rational, diag, simplify, sqrt


def main():
    t15 = diag(1, 1, 1, -3)/(2*sqrt(6))
    bl_half = diag(Rational(1, 6), Rational(1, 6),
                   Rational(1, 6), -Rational(1, 2))
    assert simplify((t15*t15).trace()) == Rational(1, 2)
    assert bl_half == simplify(sqrt(Rational(2, 3))*t15)
    # The standard SO(10) vector-index-one plane generator.
    raw = Matrix.zeros(10)
    raw[0, 1], raw[1, 0] = 1, -1
    hermitian = I*raw/sqrt(2)
    assert simplify((hermitian*hermitian).trace()) == 1
    print("GROUP_NORMALIZATION_PASS",
          "1/gY^2=1/gR^2+(2/3)/g4^2;",
          "alpha1^-1=(3/5)alphaR^-1+(2/5)alpha4^-1")


if __name__ == "__main__":
    main()
