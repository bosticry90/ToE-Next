# Canonical PS interval EFT: background and quadratic execution

**Disposition: `PS_INTERVAL_EFT_BLOCKED`.** The background and quadratic gate produced a same-coefficient stationary PS configuration and a complete *provisional* 328-real-direction PS mass census. It did not produce a certified heavy/retained split, a uniform Schur expansion, the covariantly matched PS interactions, or a lower-`F²` operator error bound. This is **not** `PS_INTERVAL_EFT_POWER_COUNTING_FAIL`: a controlled multi-spurion counting has not been disproved. Nor is it `PS_INTERVAL_EFT_DEFINED`. The lower, upper, and combined one-loop matching remain blocked; `BFB_UNRESOLVED` is carried unchanged.

## The PS background need not be invented

The prior [`sigma -> 0` recombination](../canonical_so10_ps_threshold_kernel/RESULT.md) held the physical `omega` fixed and was nonstationary. With the *same* frozen parent coefficients, set `sigma=0`, keep the PQ-singlet VEV `v=0.1 sqrt(60)`, and solve the action-derived `Phi` tadpole for `omega_PS` instead. Because the benchmark has `lambdaPhiS=lambdaSigmaS=0`, the `S` tadpole remains solved. Gauge covariance makes the `Sigma=0` first derivative vanish. The nearby positive root is

```text
omega_PS / omega_benchmark = 0.999565346637987,
L_mix=lambdaPhiSigma1-lambdaPhiSigma2/4 = -0.0000313325.
```

This is a stationary **saddle**, not a second stable physical vacuum. The normalized self-dual-`126` triplet-sector curvature is `m²/omega_benchmark² = -0.0249635399367`, across 120 real directions. That can signal the intended lower breaking; it is not by itself a failure of an interval EFT. The stationary PS Hessian has 25 near-zero real directions: 24 first-stage gauge orbits and one PQ orbit. The exact PS projector ranks and the 21/24 adjoint split were replayed. The clustering below is numerical double precision; it is not an exact threshold calculation.

| PS-origin sector | Real dimensions | Stationary-PS `m²/omega_benchmark²` | EFT disposition |
| --- | ---: | ---: | --- |
| `126_C` `(10,3,1) + (10bar,1,3)` | 120 | `-0.02496354` | Requires soft-mass power counting; not yet assigned. |
| `54_R` `(6,2,2)` gauge orbit + PQ singlet | 24 + 1 | `0` | Gauge/PQ directions, not physical scalar thresholds. |
| `10_C` `(1,2,2)`, two real copies | 4 + 4 | `0.000802115`, `0.012572303` | Numerically small, but parametric order unproved. |
| `10_C` `(6,1,1)`, two real copies | 6 + 6 | `0.004478902`, `0.010774246` | Numerically near the lower scale; assignment unproved. |
| `54_R + S_C` remaining PS singlets | 1 + 1 | `0.001440125`, `0.020000000` | Mixed-sector assignment unproved. |
| `54_R` `(20',1,1)`, `(1,3,3)` | 20 + 9 | `0.025279821`, `0.025372751` | Not safely assigned by an `m/omega` cutoff. |
| `126_C` `(15,2,2)`, two real copies | 60 + 60 | `0.254204615`, `0.269366776` | Upper-heavy candidate, not integrated out here. |
| `126_C` `(6,1,1)`, two real copies | 6 + 6 | `1.106871240`, `1.137195562` | Upper-heavy candidate, not integrated out here. |

The table accounts for all **328 real scalar directions**. The upper gauge orbit has 24 massive coset vectors in the formal PS phase; the physical benchmark's lower gauge orbit has 9 broken directions. These vector counts are inherited/replayed structural checks, not an EFT field assignment. The scalar table is explicitly **not** a pole-mass or one-loop decoupling ledger.

## Why epsilon alone does not yet close the field split

At the frozen physical point `epsilon=sigma/omega=0.1`. With coefficients held fixed, the `126` triplet-sector mass at the stationary `sigma=0` background is nonzero and negative; several `10` and `54` masses are numerically `0.0008`–`0.025` in units of `omega²` yet also have nonzero zero-spurion intercepts. A small *number* is not an `O(epsilon²)` statement.

The action-derived physical `Sigma` tadpole gives, for this benchmark (`lambdaSigmaS=0`),

```text
mSigma² = -L_mix omega² - 2 lambdaSigma1 sigma².
```

Thus a **different-theory**, tadpole-tracked family that varies the three quadratic masses with `x=sigma/omega` while keeping the other couplings fixed reaches a critical `sigma=0` endpoint with the full 120-real-dimensional triplet sector at zero curvature. It passes through the exact frozen point at `x=0.1`. This explicitly shows how a soft triplet mass can be counted as `O(x² omega²)`; it is a possible power-counting deformation, **not** a statement that the frozen coefficients change in nature or that the critical endpoint supplies physical threshold masses. At `x=0`, that family still has nonzero `10` bidoublet intercepts `0.000801529` and `0.012573146`, and `54` `(20',1,1)` and `(1,3,3)` intercepts around `0.0253`. Their interval disposition requires further declared spurions or integration with a quantified remainder. The family also has a critical 145-dimensional zero space (`120` soft triplet + `24` gauge + `1` PQ), so it cannot be substituted silently for the frozen same-coefficient theory.

No projected heavy/light off-diagonal matrix has yet been assembled across all PS sectors at finite `sigma`, no uniform inverse bound for candidate upper-heavy blocks has been demonstrated, and no Schur-complement truncation error at `epsilon=0.1` has been quantified. In particular, some candidate scalar mass scales lie close to the lower scale, so a binary upper/lower cutoff would be a prescription rather than a derived expansion. It remains possible to retain additional PS multiplets or use multiple interval thresholds, but those choices require their own covariant field/operator ledger.

There is also an independent definition boundary: [`PARENT_ACTION_V1`](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md) freezes the **complete scalar potential**, while the canonical [`RECORD.md`](../canonical_so10_scalar_reconstruction/RECORD.md) freezes fermion/PQ selection rules but explicitly leaves parent Yukawa normalization and spinor contraction for later work. A *complete* renormalizable PS action including matched Yukawa coefficients cannot be claimed from the frozen scalar action alone. This does not prevent the scalar/gauge quadratic gate, and it does not alter the zero projected complete-family gauge-index jump already earned at the lower one-loop boundary.

## Stopping consequence

The first unresolved gate is a **declared multi-spurion field split** with full projected mass/mixing matrices and an error bound. Only after that can one integrate the upper fields through covariant EOM, produce a once-only PS interval ledger, and determine whether induced operators affect the lower `F²` match. No tree-level current–current coefficient, scalar-exchange operator, lower scalar hard-region subtraction, gauge scale, or flavor quantity is claimed here. The delayed-all-scalars-to-`M_I` logarithmic checksum remains a comparator, not an adopted EFT.

Reproduce from the repository root:

```text
python calculations/canonical_so10_ps_interval_eft/probe_quadratic.py
python calculations/canonical_so10_ps_threshold_kernel/certify_ps_projectors.py
python calculations/canonical_so10_ps_threshold_kernel/check_vector_limits.py
python calculations/canonical_so10_lower_bfm/check_quadratic_orbits.py
```

The first script reuses the previously certified affine full-Hessian blocks, solves the same-coefficient PS `Phi` tadpole, verifies the benchmark `Sigma` and `S` tadpoles, and prints both the stationary-PS census and the explicitly labeled different-theory scaling comparator. Its numeric spectrum needs exact/projected replay before serving as any matching coefficient. The action and point hashes are in [`RECORD.md`](RECORD.md). No published Babu--Khan scalar formula was used.
