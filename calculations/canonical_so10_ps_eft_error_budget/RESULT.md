# Canonical PS interval EFT: gauge-matching error budget

**Disposition: `PS_EFT_ERROR_UNRESOLVED`.** The candidate split is not shown accurate enough for the one-loop gauge test, but it is also not shown unavoidably inaccurate. The calculation exposes two numerical contributions near the declared tolerance and four operator-level terms whose coefficients have not been matched. Consequently `PS_INTERVAL_EFT_BLOCKED`, `LOWER_BOUNDARY_MATCHING_BLOCKED`, `PS_THRESHOLD_KERNEL_BLOCKED`, `GAUGE_MATCHING_BLOCKED`, and `BFB_UNRESOLVED` remain. The direct physical-vacuum fallback is **not** admitted by this outcome.

## Frozen observable-specific target

The coarse complete-multiplet diagnostic requires a displacement

```text
delta(alpha_L^-1-alpha_4^-1) = 2.027--2.966
```

to move its crossing into the canonical vector-band hierarchy. This is not a prediction, but it is the scale of the next discrimination. The gate preregisters a maximum nonuniversal EFT uncertainty of ten percent of the lower endpoint,

```text
delta_target = 0.2027005
```

in any pairwise inverse-coupling difference. A common shift of all three inverse couplings is irrelevant to this target. Ten percent is a project accuracy choice, not an experimental error bar or a general EFT standard.

The frozen candidate split integrates the `126_H` `(6,1,1)+(15,2,2)` scalar sectors as an upper block: **132 real directions**. Everything else remains provisionally retained for this error test, including directions whose eventual Goldstone/vector disposition is not yet covariantly matched. This is the same diagnostic split used by the multi-spurion calculation; it is not silently promoted into an EFT.

## What can be quantified

### Candidate upper-scalar placement

SM-block counting gives the upper candidate scalar beta vector

```text
b_H^(1,2,3) = (79/15, 5, 17/3).
```

An independent PS replay obtains `b_4=(1+16)/3=17/3`, `b_L=b_R=15/3=5`, and `b_1=(2/5)b_4+(3/5)b_R=79/15`. Moving this complete candidate block across a scale ratio `r` changes inverse couplings by `b_H log(r)/(2 pi)`. Across the physical vector-band ratio range this gives

| `r` | `|delta(alpha_L^-1-alpha_4^-1)|` |
| ---: | ---: |
| `4.08248` | `0.14926` |
| `9.12871` | `0.23464` |

The upper endpoint exceeds `delta_target`. This is a **scale-placement sensitivity**, not an uncertainty that must remain after correct matching. It proves that the field disposition cannot be chosen casually at the requested accuracy.

### Known physical scalar logarithm

The existing basis-invariant broken-phase trace for all 290 positive heavy scalar directions at `mu=omega` corresponds to

```text
delta alpha^-1_(1,2,3) = (1.73722, 1.80663, 1.86318).
```

Its maximum nonuniversal spread is `0.12595`, and its `L-C` difference is `0.05655`, both below the target. Varying the scale through the vector-band window changes the scalar-log pairwise spread by `0.13433--0.21118`; the upper value is again near or slightly above the target. These are complete **direct broken-phase scalar contributions and scale sensitivities**, not the error of a PS EFT. They show that known scalar logarithms are numerically relevant but do not by themselves invalidate the target.

### Quadratic and derivative-expansion diagnostics

At the physical endpoint the candidate split has

```text
lambda_min(H_HH)/omega^2 = 0.286714
||H_LL||/omega^2         = 0.201845
||H_LH||/omega^2         = 0.031450
||Schur||/omega^2        = 0.003444.
```

Thus `||H_LL||/lambda_min(H_HH)=0.7040` and `||H_LH||/lambda_min(H_HH)=0.1097`. The exact quadratic Schur complement can in principle be retained, so its size is not automatically an EFT error. However, the smallest positive physical scalar gap is only `0.00144269 omega^2`: the direct Schur norm is `2.39` times this gap, and the conservative family bound is `9.30` times it. Therefore the available norm data fail the prerequisite `||delta M^2||<lambda_min` for a uniform matrix-log perturbation bound. No finite scalar-threshold error follows from the current Schur estimate.

The largest retained/heavy mass-squared ratio `0.704` also makes a first-order derivative expansion poorly conditioned for the borderline modes: the formal geometric tail diagnostic `r^2/(1-r)` is `1.67`. This number is **not** a Wilson-coefficient bound; it shows why truncation at the first induced operator is not certified by scale separation alone.

Using the coarse `g_U=0.5769` only as a comparator, the lightest upper vector has `M_V^2/omega^2=g_U^2(50/120)=0.13866`. The largest provisionally retained scalar block then has `m^2/M_V^2=1.46`. Hence upper-vector current-current insertions into loops of all provisionally retained scalars cannot be declared suppressed by `m^2/M_V^2`. This does not compute their contribution, because the covariant operator coefficients and subtraction have not been derived.

## Terms that remain unbounded

The frozen parent action and current field ledger do not yet supply a common, PS-covariant calculation of:

1. upper-vector current-current insertions in retained-field loops;
2. upper-heavy scalar-exchange operators contributing to lower `F^2`;
3. covariant removal of the 24 upper Goldstone directions and their vector/ghost completion;
4. the finite hard-region subtraction for the borderline retained multiplets.

Assigning order-one coefficients to these terms would be dimensional analysis, not a bound. Setting them to zero would assume the conclusion. Their absence prevents adding the known entries into a total uncertainty smaller than `0.2027005`.

## Decision

`PS_EFT_ACCURATE_FOR_GAUGE_MATCHING` is not earned because the complete error cannot be bounded. `PS_EFT_INACCURATE_FOR_GAUGE_MATCHING` is also not earned: the quantities exceeding the target are placement/scale sensitivities that correct matching could cancel or determine, not unavoidable residual errors. The correct result is therefore

```text
PS_EFT_ERROR_UNRESOLVED
```

The first unearned step remains a covariant tree-level PS field/operator match for this specific split, followed by the hard-region insertion calculation. The direct `Spin(10)->SM` fallback was authorized by the decision tree only after an `INACCURATE` finding; it remains scoped but unadmitted. A cleaner benchmark remains a later alternative, not a result of this gate.

Reproduce from the repository root:

```text
python calculations/canonical_so10_ps_eft_error_budget/quantify_error_budget.py
python calculations/canonical_so10_matrix_threshold/check_scalar_matrix_log.py
python calculations/canonical_so10_ps_multispurion/test_joint_family.py
python calculations/canonical_so10_lower_f2/check_delayed_scalar_candidate.py
```

The compact machine-readable budget is [`error_budget.json`](error_budget.json). Exact group indices and ledger counts are replayed in the primary script; norm and scale diagnostics are double precision and carry no interval-certificate authority.
