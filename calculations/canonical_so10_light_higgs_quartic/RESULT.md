# Relaxed light-Higgs quartic at the frozen Stage 2 point

**Disposition: `LIGHT_HIGGS_QUARTIC_NEGATIVE`.** The algebraically tuned Stage 2 scalar point is quadratically flat in one complex SM Higgs doublet, but is **not a local scalar minimum** once its heavy fields relax. This rejects that particular tuned point; it does not refute the canonical parent action or the separately positive Stage 1 point.

For a canonically normalized neutral field `h`, with `H†H=h²/2`, write the parent potential near the Stage 2 vacuum as

```text
V = V0 + a_direct h^4 + h^2 j_A X_A + (1/2) X_A H_AB X_B + ... .
```

On the positive physical heavy subspace, elimination gives `X=-H^+ j h²+...` and

```text
lambda_eff = 4 [a_direct - (1/2) j^T H^+ j],
V_eff = lambda_eff (H†H)^2 + higher orders.
```

The direct parent-invariant evaluation at the frozen [Stage 2 point](../canonical_so10_scalar_benchmark/STAGE2_POINT.json) yields:

| Canonically normalized coefficient | Value |
| --- | ---: |
| Direct, heavy fields held fixed | `+0.199095687934763` |
| Heavy-field relaxation subtraction | `56.6889310614242` |
| **Relaxed `lambda_eff`** | **`-56.4898353734894`** |

The unnormalized coefficient of the fourth power of the calculation's real light direction is `-3.53061471084309`. The subtraction is overwhelmingly from the physical neutral-singlet sector: its raw contribution is `3.54217071648408`, versus `0.000333102464898191` from the neutral `Y=0` triplet and `0.000554372390034386` from the neutral `Y=±1` triplet pair. All other scalar irreps are excluded as tree-level sources of two Higgs fields by the unbroken SM tensor-product selection rule. The neutral-source calculation uses five real singlet directions (two symmetry zeros), one real `Y=0` triplet direction, and four real directions in the `Y=±1` triplet pair.

The heavy Hessian is positive on the eight physical source directions. The source is orthogonal to both singlet symmetry null directions to about `1.1e-25` in the 15-digit direction replay. The light direction was obtained from a high-precision direct-parent doublet block, whose untampered mass-squared residual is about `5e-65`; its exact algebraic tuning and full rank-290/nullity-38 Hessian certificate remain in the preceding [benchmark result](../canonical_so10_scalar_benchmark/RESULT.md).

Checks of the new quartic result:

- Rationalizing the light direction at 11 and 15 digits changes `lambda_eff` by less than `1e-12`; the sign margin is about `56`.
- A direct nine-point parent-potential polynomial expansion along the solved heavy-field valley gives the same quartic, `-3.53061471084309` in the raw light coordinate, without using the final Schur-contraction expression.
- An invertible shear of the heavy-coordinate basis leaves the relaxation subtraction unchanged.
- A quarter-turn in the complex Higgs phase gives the same relaxed quartic.
- The fixed-heavy quartic is positive, and the heavy-field correction lowers it, as required by the positive heavy Hessian.

These checks use distinct extraction routes from the same frozen 29-monomial tensor implementation; they are **not** a wholly independent reimplementation of every parent contraction. The earlier action-basis and Hessian validations remain the tensor-level controls. The quoted decimals are evaluation values, not a claim of that many independently verified physical digits.

This result is local and tree level. It makes no claim about the full potential's global boundedness or about whether another doublet tuning or scalar parameter point can give a positive relaxed quartic. No gauge-unification, flavor, or proton-decay calculation was started from this failed Stage 2 point.

## Reproduction

With the same SymPy, mpmath, NumPy, and SciPy environment used for the prior canonical scalar calculations, from the repository root:

```text
python calculations/canonical_so10_light_higgs_quartic/compute.py
```

The run evaluates the frozen parent action, the exact Stage 2 tuning root, the full neutral-source heavy Hessian, the cubic sources, and all checks described above. The parent-action SHA-256 is `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`; the Stage 2 input SHA-256 is `26bd69eb2f1341bca3576b72da666b0ca4d71a38a3e1c39f362908704dc16b6b`.
