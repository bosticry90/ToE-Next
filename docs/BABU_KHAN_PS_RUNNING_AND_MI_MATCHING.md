# Babu-Khan Pati-Salam Running and Intermediate Matching

## Admission decision

```text
SEAM: BK_PS_BNV_GAUGE_LL_TO_MI_TREE_MATCH
ADMISSION: ADMITTED_AND_RESOLVED
CALCULATION: BK_PS_BNV_GAUGE_LL_RUNNING_AND_MI_TREE_MATCHING_V1
CALCULATION STATUS: PASS
SOURCE AUTHORITY: WORKING_CANDIDATE_NOT_ACCEPTED
```

The admitted relation is deliberately narrower than a complete Pati-Salam
effective theory:

```text
single Pati-Salam-covariant dimension-six BNV coefficient at M_U
    -> one-loop gauge-only leading-log evolution through the Babu-Khan
       Pati-Salam-plus-D-parity spectrum
    -> tree-level projection at M_I
    -> the already established BNV SMEFT and SMEFT-plus-N boundary
```

The literature supplies enough of this bounded calculation to justify reuse.
It does not supply a turnkey, full-flavor, complete-one-loop implementation for
the exact Babu-Khan `54_H + 126_H + 10_H` model. The missing model-specific
checks are small enough and decisive enough to admit one calculation.

## Focused literature audit

The audit was performed against primary sources current through 2026-09-18.
No package was installed and no calculation was executed.

| Source | Reusable result | Limitation for this seam | Disposition |
|---|---|---|---|
| K. S. Babu and S. Khan, [arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2) | Exact breaking chain, Pati-Salam-plus-D-parity field spectrum, one- and two-loop gauge beta coefficients, threshold conventions, and short-distance anomalous-dimension entries `15/4`, `9/4`, `9/4` | Its proton-lifetime treatment packages rather than derives the full-flavor intermediate EFT map; scalar thresholds make benchmark numerics model-point dependent | Controlling source for this model's spectrum, scales, and gauge-coupling evolution |
| Y. Mambrini et al., [arXiv:1502.06929v2](https://arxiv.org/abs/1502.06929v2), Appendix D | A unique mixed-left/right Pati-Salam BNV invariant, its tree coefficient, the analytic one-loop gauge leading-log factor, and tree-level matching to four Standard Model BNV operators | It neglects fermion flavor mixing, uses a different SO(10) spectrum, and does not preserve the right-handed-neutrino term needed here | Reuse the operator structure and anomalous exponents; do not copy its beta coefficients or complete threshold map |
| R. Alonso et al., [arXiv:1405.0486v2](https://arxiv.org/abs/1405.0486v2) | Complete one-loop dimension-six BNV running in SMEFT, including operators with right-handed neutrinos | Applies after Pati-Salam breaking, not in the Pati-Salam regime | Downstream comparator only; no SMEFT evolution is admitted here |
| A. Datta et al., [arXiv:2010.12109v3](https://arxiv.org/abs/2010.12109v3) | Gauge anomalous dimensions in SMEFT with right-handed neutrinos | Standard-Model gauge symmetry and a broader operator set; not the Pati-Salam stage | Downstream right-handed-neutrino comparator only |
| T. P. Dutka and J. Gargalionis, [arXiv:2211.02054v2](https://arxiv.org/abs/2211.02054v2) | Demonstrates a separate dimension-five source of baryon violation in low-scale Pati-Salam theories | Different operator dimension and source mechanism from the gauge-generated dimension-six boundary here | Excluded from this seam; prevents a false claim of a complete Pati-Salam BNV theory |

The audit found no maintained external tool or primary source that directly
implements all of the following together:

- the exact Babu-Khan intermediate spectrum;
- the full three-generation coefficient tensor from the completed boundary;
- a complete Pati-Salam anomalous-dimension matrix including gauge, Yukawa,
  and scalar effects;
- the split heavy-vector threshold projector at `M_I`;
- the right-handed-neutrino operator disposition.

That absence does not require a new general-purpose framework. It bounds this
calculation to the established gauge-only leading-log result and tree-level
threshold match. A claim of complete one-loop running or complete one-loop
threshold matching remains not admitted.

## What is established and what remains to derive

Mambrini et al. give the Pati-Salam invariant

```text
epsilon_ij epsilon_rs epsilon_ABCD
(Psi^Cbar)^(A i) P_L Psi^(B j)
(Psi^Cbar)^(C r) P_R Psi^(D s),
```

show that the all-left and all-right contractions vanish, and therefore obtain
one mixed-chirality operator. In their sign and beta-function conventions its
coefficient evolves as

```text
C(M_I) = [alpha_4(M_I)/alpha_U]^[-15/(4 b_4)]
         [alpha_2L(M_I)/alpha_U]^[-9/(4 b_2L)]
         [alpha_2R(M_I)/alpha_U]^[-9/(4 b_2R)] C(M_U).
```

Babu and Khan independently use the Pati-Salam anomalous-dimension entries

```text
gamma_4C = 15/4
gamma_2L = 9/4
gamma_2R = 9/4
```

and, for group order `(4C, 2L, 2R)`, publish the model-specific one-loop gauge
coefficients

```text
a_PS = (1, 26/3, 26/3).
```

Their sign convention for `a_i` is not presumed identical to the `b_i`
convention in Mambrini et al. The admitted calculation must derive the
differential equation and reconcile the exponent sign rather than copy a
displayed power.

The completed [tree-level boundary](../calculations/bk_so10_bnv_matching/RESULT.md)
adds information absent from the simplified literature projection: full flavor
wiring, a retained `Q_qqdN` term, and the qualification that `k1^2` and `k2^2`
are symmetry-breaking projections of one coefficient rather than independent
Pati-Salam Wilson coefficients. Those are controlling inputs.

## Calculation record

### 1. Scientific question

Can the single Pati-Salam-covariant BNV coefficient already established at the
high-scale boundary be evolved to `M_I` at one-loop gauge leading-log accuracy
and projected at tree level into the completed SMEFT and SMEFT-plus-`N`
boundary without introducing a second Pati-Salam coefficient, losing flavor
information, or silently integrating out the right-handed neutrino?

### 2. Claim under test

For the Babu-Khan Pati-Salam-plus-D-parity spectrum, the unique mixed-chirality
dimension-six BNV operator is multiplicatively closed under one-loop gauge-only
running. Its full weak-basis flavor tensor receives one universal short-distance
factor from `M_U` to `M_I`. A tree-level symmetry-breaking projector at `M_I`
then reproduces the established `Q_qque`, `Q_duql`, and `Q_qqdN` coefficient map,
including distinct pole-mass dependence only after the projection.

### 3. Scope and authority ceiling

In scope:

- one-loop gauge-only leading-log evolution of one Pati-Salam operator;
- exact symbolic dependence on endpoint gauge couplings and scales;
- independent reconstruction of the Babu-Khan one-loop gauge coefficients from
  its declared active fields;
- full three-generation flavor tensors, with no numerical Yukawa fit;
- tree-level Pati-Salam-to-SM projection at `M_I`;
- explicit retention of the right-handed-neutrino sector.

Out of scope:

- Yukawa- or scalar-induced operator mixing;
- finite one-loop matching corrections at `M_U` or `M_I`;
- numerical selection of a Babu-Khan benchmark or threshold spectrum;
- integrating out any right-handed neutrino;
- SMEFT, SMNEFT, LEFT, or chiral running below `M_I`;
- hadronic matrix elements, partial widths, lifetimes, or exclusions.

A pass establishes only a gauge-leading-log Pati-Salam evolution factor and a
tree-level `M_I` operator boundary for this frozen model. It does not establish
a complete Pati-Salam EFT, proton-decay viability, SO(10), or a Theory of
Everything.

### 4. Frozen inputs and assumptions

Source boundary:

- the `PASS` result in
  [`calculations/bk_so10_bnv_matching/RESULT.md`](../calculations/bk_so10_bnv_matching/RESULT.md);
- one Pati-Salam-covariant Wilson coefficient above `M_I`;
- the completed weak-basis flavor tensors and convention ledger;
- symbolic positive scales `M_U > M_I` and perturbative endpoint couplings;
- no numerical fermion rotation or flavor fit.

Running:

- intermediate group `SU(4)_C x SU(2)_L x SU(2)_R x D`;
- Babu-Khan's extended-survival field content between `M_I` and `M_U`;
- one-loop gauge beta coefficients `(1, 26/3, 26/3)` in group order
  `(4C, 2L, 2R)`, subject to independent reconstruction;
- gauge anomalous-dimension entries `(15/4, 9/4, 9/4)`, subject to an
  independent sign and group-factor check;
- D parity requires equal left and right gauge evolution in the frozen
  spectrum, but the two factors remain explicit until that equality is checked;
- dimensional regularization and an MS-like mass-independent subtraction
  convention for the one-loop leading-log calculation.

Threshold:

- tree-level matching only at `M_I`;
- `k1^2` and `k2^2` enter only through the broken-phase threshold projector;
- the zero-running limit must exactly reproduce the completed coefficient map;
- `Q_qqdN` remains in SMEFT plus singlet neutrinos; no `N` mass hierarchy is
  invented and no `N` threshold is crossed.

### 5. Provenance and comparators

The two controlling primary sources are Babu-Khan for the model and Mambrini et
al. for the Pati-Salam operator-running formula. The completed ToE-Next boundary
is the controlling coefficient and flavor source. Alonso et al. and Datta et al.
are held only as downstream comparators. No legacy implementation or coefficient
is imported.

### 6. Primary method and tool

Primary method: derive the one-loop analytic solution from the Wilson-coefficient
and gauge-coupling differential equations, reconstruct the Babu-Khan beta
coefficients from representation indices, then apply an explicit symbolic
threshold projector to the frozen coefficient tensor.

Primary tools: a small calculation-local SymPy implementation for rational group
factors and symbolic evolution, with Cadabra used only if indexed group/operator
closure needs an executable check. No new package is required.

### 7. Independent replay decision and reason

Independent replay is required because beta-function sign conventions,
representation multiplicities, D-parity duplication, and threshold projection
can each produce plausible but wrong powers or factors.

Julia/Nemo will independently reconstruct the rational beta coefficients and
the analytic evolution exponents without consuming the SymPy result. A manual
group-theory ledger must accompany both implementations. VPC may check a final
finite rational map only if that map lies within its trusted operations.

### 8. Adversarial checks and falsifiers

Stop with `FAIL` or `BLOCKED` if any of these conditions is met:

1. the declared Babu-Khan active fields do not reproduce `(1, 26/3, 26/3)`;
2. the unique operator is not multiplicatively closed under the admitted
   gauge-only approximation;
3. independent derivation does not reproduce `(15/4, 9/4, 9/4)` or cannot
   reconcile the source sign conventions;
4. D parity fails to give consistent left/right running under the frozen
   spectrum;
5. flavor tensors acquire unsupported flavor mixing under gauge-only running;
6. `k1^2` and `k2^2` are treated as independent coefficients above `M_I`;
7. the zero-running threshold map differs from the completed tree-level result;
8. `Q_qqdN` is discarded, forced into standard SMEFT, or integrated out without
   a separately admitted threshold;
9. finite threshold, Yukawa, scalar, or numerical benchmark assumptions are
   inserted to repair a failed leading-log result.

### 9. Known-limit and physical-assumption checks

Required checks are:

- `M_I -> M_U` gives a unit evolution factor;
- turning off any gauge coupling removes only its own logarithmic contribution;
- the analytic solution satisfies the admitted one-loop differential equation;
- expanding the closed-form factor to first order reproduces the direct
  leading-log expression;
- D parity reduces the two `SU(2)` factors consistently without erasing their
  separate group provenance;
- gauge-only running preserves the full flavor tensor;
- applying the threshold projector with unit running reproduces every nonzero
  and zero entry in the completed map;
- the common-mass limit gives one Pati-Salam coefficient, while unequal pole
  dependence appears only after symmetry breaking.

### 10. Stopping rule

Stop at the first of:

- **PASS:** the model-specific beta coefficients, anomalous exponents, analytic
  gauge-leading-log factor, full-flavor evolution, and tree-level `M_I`
  projector agree in primary and independent replays and satisfy all limits;
- **FAIL:** a frozen relation is inconsistent and cannot be corrected without
  changing the admitted source or approximation;
- **BLOCKED:** a required field multiplicity, convention, or threshold projector
  is underdetermined by the frozen sources.

Do not proceed below `M_I` in the same calculation.

### 11. Failure interpretation

Failure rejects or qualifies this gauge-leading-log recovery step for the frozen
Babu-Khan route. It does not refute the completed tree-level operator map, other
orders or threshold prescriptions, the whole Babu-Khan model, or SO(10).

Blocked means the current literature and frozen boundary do not specify enough
to earn the next arrow. It is not evidence for or against proton decay.

### 12. Result and reproducibility record

The calculation resolved `PASS`. The complete derivation, exact coefficient
factor, corrected interval-sextet ledger, threshold map, tool
versions, independent replay, and test matrix are preserved in the
[calculation result](../calculations/bk_ps_bnv_running_mi_matching/RESULT.md).

```text
STATUS = PASS
AUTHORITY = ONE_LOOP_GAUGE_LEADING_LOG_PS_RUNNING_AND_TREE_LEVEL_MI_MATCHING_ONLY
DOWNSTREAM = AUTHORIZED_FOR_SEPARATE_ADMISSION
```

## Admission outcome

The seam was admitted because both endpoints and the established middle
machinery were precise, the missing model-specific work was bounded, and
several cheap falsifiers preceded any phenomenology. It has now resolved
`PASS`, including independent Python/SymPy and Julia/Nemo replays. The result
applies to Babu-Khan's published intermediate spectrum. A later
[`H_T` threshold audit](BABU_KHAN_HT_THRESHOLD_AUDIT.md) corrected the active
complex sextet's identity to `Sigma_1=(6,1,1)` from `126_H`; `H_T` from `10_H`
belongs to the `M_U` threshold ledger. The numerical beta coefficients,
running factor, and `M_I` projection are unchanged.

The pass does not authorize work below `M_I`, selection of a numerical
benchmark, or calculation of a proton lifetime without a separate admission.
