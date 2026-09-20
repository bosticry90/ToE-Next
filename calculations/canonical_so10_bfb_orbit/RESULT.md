# Quartic orbit-space check of the positive-Higgs point

**Disposition: `BFB_UNRESOLVED`.** The frozen benchmark has a certified positive pure self-dual-`126_H` quartic, in addition to positive pure `54_H`, `10_H`, singlet, and the `54_H+10_H` two-field sector. No negative direction appeared in 11 adversarial low-dimensional mixed strata. The full `54_H+126_H+10_H+S_H` quartic orbit space is **not** certified bounded below, so the positive-Higgs point retains only local tree-level stability authority. No gauge-unification, flavor, or proton-decay calculation was performed here.

The calculation uses the unchanged [parent action](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md) (SHA-256 `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`) and [exact positive-Higgs point](../canonical_so10_positive_higgs/POINT.json) (SHA-256 `476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816`). Only the homogeneous quartic matters for a tree-level runaway.

## Exact pure-`126_H` bound

Write the four self-dual-`126_H` invariants in the frozen basis as `Q0`, `Q1`, `Q2`, and the crossed contraction `X131`. The first three are squared norms. Let `P1` be the paired four-form tensor obtained by contracting one index between two copies of `Sigma`. It lies in `Sym²(Lambda⁴ C¹⁰)`, and `X131` is its exchange-Casimir quadratic form.

The fully antisymmetric eight-form projection of `P1` is `sum_i (i_i Sigma) wedge (i_i Sigma)`. It vanishes for every complex self-dual five-form: [the exact checker](certify_pure_sigma.py) verifies the polarized identity on all `126*127/2 = 8,001` pairs of a complete self-dual basis. The three `GL(10)` summands of `Sym²(Lambda⁴)` have dimensions `45`, `8,250`, and `13,860` (summing to its full dimension `22,155`) and exchange eigenvalues `-16`, `-2`, and `4`; the vanishing eight-form removes the `-16` summand. An independently implemented index-exchange operator agrees with `X131` on exact tensor samples and reproduces the extremal `-16` and `4` eigenvectors. Consequently,

```text
X131 >= -2 Q1

V4(Sigma) >= lambdaSigma1 Q0
             + (lambdaSigma2 - 2 lambdaSigma4) Q1
             + lambdaSigma3 Q2.
```

At the frozen point the three coefficients on the last line are, exactly,

```text
lambdaSigma1                  = 280840437/1280000000000 > 0
lambdaSigma2-2*lambdaSigma4  = 289048779/2560000000000 > 0
lambdaSigma3                  = 43964541/320000000000 > 0.
```

Since `Q0 > 0` for any nonzero `Sigma`, the pure-`126_H` quartic is strictly positive. This removes one important unknown from the earlier [200-ray probe](../canonical_so10_bfb_probe/RESULT.md); it says nothing by itself about mixed runaways.

For `Phi+phi` with `Sigma=S=0`, `tr(Phi⁴) >= [tr(Phi²)]²/10`, `phi†Phi²phi >= 0`, and `|phi·phi|² >= 0` give the exact lower quadratic form in `p2=tr(Phi²)` and `u=phi†phi`:

```text
V4(Phi,phi) >= (52268/10^9) p2² - (1/500) p2*u + (1/10) u².
```

Its symmetric coefficient matrix has determinant `10567/2500000000 > 0` and positive leading entry, certifying this two-field sector. The pure-singlet coefficient and remaining single-field limits are also positive.

## Mixed-field attack and its limit

The [search code](attack_orbit.py) evaluated 64 additional exact sparse self-dual forms and compiled the exact parent quartic on 11 targeted three-to-five-component strata, including the *nonvanishing* `Sigma Sigma Sigma* phi` doublet pairing and its singlet/phase mixtures. Every interpolated quartic was checked at a signed point outside its interpolation grid against direct exact parent-invariant evaluation. Four unrelated deterministic differential-evolution seeds searched each normalized coordinate stratum. No optimizer minimum was negative; the smallest reported coordinate-stratum value was about `0.0075358`. These coordinate normalizations differ across strata and are **not** a global or canonical-kinetic lower bound.

This is an adversarial search, not an interval or SOS certificate. It samples only selected subspaces of the full 328-real-dimensional field space. In particular, mixed `126_H` and multi-field orbit directions remain uncontrolled. A future exact negative ray would immediately change the disposition to `BFB_COUNTEREXAMPLE_FOUND`; non-detection here cannot justify `BFB_CERTIFIED`.

## Gauge-unification handoff

**Conditional diagnostic handoff defined, not executed.** The certified pure-`126_H` and `54_H+10_H` sectors, combined with the absence of a mixed counterexample in this bounded attack, justify testing the benchmark's gauge running as an *independent potential falsifier*. `BFB_UNRESOLVED` must be carried visibly; successful gauge matching would not promote this point to a globally viable vacuum.

The separate calculation must first freeze the physical heavy-vector masses, all non-Goldstone scalar eigenmasses and SM/Pati--Salam representations from this canonical action and exact point, and the interpretation of the common overall scale, `M_I`, and `M_U`. It must use the **canonical** spectrum, never published Babu--Khan scalar thresholds. Specify the renormalization scheme, normalized hypercharge embedding `Y=T3R+(B-L)/2`, one-loop decoupling/matching conventions, uncertainty inputs, and treatment of the single light Higgs and PQ singlet. Then ask whether measured low-energy gauge couplings can match through the actual intermediate thresholds to one common perturbative `Spin(10)` coupling and scale. A failed match rejects this point within the declared matching order; a missing threshold, convention, or spectrum entry returns `GAUGE_MATCHING_BLOCKED`. No flavor or BNV inference is allowed from either outcome.

Reproduce from the repository root:

```text
python calculations/canonical_so10_bfb_orbit/certify_pure_sigma.py
python calculations/canonical_so10_bfb_orbit/attack_orbit.py
python calculations/canonical_so10_bfb_orbit/attack_orbit.py --extended
```
