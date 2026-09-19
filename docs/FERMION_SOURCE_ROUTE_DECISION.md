# Fermion-Source Continuation Decision

## Decision

```text
question = BABU_KHAN_SPECIFIC_REFIT_OR_PUBLISHED_FIT_SOURCE
outcome = NONE_FOR_EXECUTION
babu_khan_refit = NOT_ADMITTED
source_switch = NOT_ADMITTED
active_seam = NONE
active_calculation = NONE
```

Two Babu-Khan gauge-sector recovery boundaries remain passed. This decision does
not qualify or undo them. It asks only whether the missing model-specific
fermion/neutrino input has earned a new fit, or whether a different published
source model offers a cleaner complete benchmark for the next threshold arrow.
The answer is **neither yet**. A printed numerical fit is not automatically a
fit through its model's full intermediate theory; conversely, missing Babu-Khan
fit data do not automatically justify launching a new optimization program.

## Comparison

| Criterion | A: refit frozen Babu-Khan 54/126/complex-10 plus PQ model | B: use a published-fit source model |
|---|---|---|
| Assumption compression | Two symmetric Yukawa matrices are economical, but the PQ restriction, Higgs-doublet mixing, scalar-potential parameters, threshold spectrum, and boundary conditions must all be counted. A successful fit could test whether that economy is real. | A model with an extra Yukawa structure may fit more easily but can relocate rather than remove independent assumptions. A lower fitting cost is not itself greater unification. |
| Earned recovery work | The heavy-vector/Pati-Salam operator map and one-loop gauge-leading-log plus `M_I` projection already apply. | Group-theory and verification methods transfer, but coefficients, spectrum, flavor rotations, and matching must be rederived for the changed model. The Babu-Khan results cannot be relabeled. |
| Numerical input and parameter burden | The quoted Joshipura-Patel point is numerically informative but has a different breaking chain and complex `s`; the frozen model has no validated `H,F,r,s,r_R` point. A new coupled fit is a substantial nonlinear task, not a matrix substitution. | The 2024 Babu et al. `10+120+126bar` model prints GUT-scale matrices and fit parameters for normal/inverted ordering. Its Yukawa sector has two symmetric and one antisymmetric matrices; the paper counts 3 real plus 9 complex Yukawa parameters in its chosen basis, before all scale and threshold choices. The Haba-Shimizu-Yamada `54+126+10` analysis fits through a Pati-Salam boundary but presents a scan rather than one printed full benchmark, and allows both `10` and `10*` Yukawa couplings. |
| Same breaking chain and flavor treatment | Babu-Khan specifies the `54 -> Pati-Salam with D parity -> 126 -> SM` chain, but a flavor fit through that chain is not published in the audited lineage. | Babu et al. (2024) specifies a `54 -> Pati-Salam with D parity -> 126 -> SM` chain and fits sequential singlet-neutrino thresholds, but explicitly approximates the entire sub-GUT flavor evolution with SM plus type-I RGEs. Its gauge-scale analysis separately uses threshold corrections. That does not yet furnish one demonstrated coupled Pati-Salam-flavor benchmark. Haba et al. handles the Pati-Salam-scale fit but does not publish the free phases, unitary matrix, and Higgs-mixing coefficients of one reconstructible point. |
| Proton-decay discriminator | Babu-Khan has the already-verified BNV operator boundary, but no validated flavor matrices to predict channels or lifetimes. | Babu et al. provides proton-decay and gauge-threshold analysis, but its fit and scale studies are not a single fully coupled flavor/threshold point. Haba et al. discusses gauge-boson masses and nucleon-decay bounds, not a complete printed BNV flavor benchmark. |
| Cost and first possible falsifier | High cost: low-energy inputs, matching and PS Yukawa running, scalar-vev restrictions, fit objective, uncertainty treatment, and independent replay must be fixed first. The real-`s`/PQ condition and fit quality are sharp tests, but no cheap decisive *no-go* is established; optimizer nonconvergence alone would not falsify the model. | Lower cost to inspect and reconstruct a printed 2024 matrix point, but correcting its omitted Pati-Salam flavor interval may itself require refitting. A first admission check is whether one published point's `M_U`, `M_I`, `M_{N_i}`, basis, and threshold convention form a single consistent initial condition. Failure would block *that point*, not its entire model. |
| Broader lesson | A controlled fit would test whether a relatively economical gauge-plus-flavor construction truly coexists at one parameter point, beyond the gauge recovery maps. | A controlled alternate would test whether published numerical completeness buys a cheaper UV-to-IR chain or only hides intermediate matching assumptions. |

The parameter counts above are **not** an apples-to-apples model-complexity score.
Scalar, threshold, symmetry and boundary-condition assumptions remain to be
accounted for in either route.

## Evidence and qualifications

- [Babu and Khan, arXiv:1507.06712v2](https://arxiv.org/html/1507.06712v2)
  specifies the scalar/breaking construction and cites a related flavor point,
  but notes that the small complex phase in the quoted `s` is not an independent
  phase of its scalar realization and that a mass/mixing fit may need to be
  redone. The [fit-provenance audit](BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md)
  tests direct adoption rather than assuming it.
- [Haba, Shimizu and Yamada, arXiv:2304.06263v2](https://arxiv.org/html/2304.06263v2)
  uses the closer `54/126/10` two-step chain and constrains Yukawas at the
  Pati-Salam scale, but explicitly includes both `10` and conjugate-`10`
  couplings. Its published fit outputs are distributions over free phases,
  charged-lepton rotation and Higgs-mixing coefficients, not one fully printed
  matrix point ready for a Takagi replay.
- [Babu et al., arXiv:2409.03840](https://arxiv.org/html/2409.03840)
  provides explicit normal/inverted GUT-scale fit parameters and singlet-neutrino
  spectra in its appendices. It uses `10+120+126bar`, not Babu-Khan's two-matrix
  Yukawa structure. Section 4.1 explicitly substitutes SM+type-I running from
  `M_GUT` for the Pati-Salam flavor interval, whereas section 6 uses the
  intermediate chain and gauge-threshold variations. The published numerical
  points therefore deserve independent *model-internal* consistency checks
  before being treated as frozen downstream EFT input. In particular, the
  printed heavy-neutrino masses and the selected `M_I` must be compared in one
  convention; their family labels alone do not set threshold order.
- [Djouadi et al., arXiv:2212.11315](https://arxiv.org/abs/2212.11315)
  develops gauge and Pati-Salam Yukawa matching with a PQ/two-Higgs-doublet
  setup, but the published fit exercise is third-generation Yukawa unification,
  not the full flavor/neutrino matrices required here. It is useful machinery,
  not a replacement benchmark.

This is a bounded primary-source comparison, not a proof that no better
published fit exists. The leading *low-cost comparator* is the printed 2024
`10+120+126bar` point, but it is **not selected as the new source theory**.
The closer Haba construction is **not selected as a numerical benchmark**.

## Reopening conditions and authority ceiling

Route A may be admitted only after a costed, model-specific fit protocol fixes
the input dataset and scheme, PS and scalar-threshold treatment, Higgs-doublet
mixing and the PQ/phase restriction, fit objective, uncertainty acceptance,
and an independent validation plan. One accepted point would show only that
one frozen parameter set accommodates the targeted fermion data.

Route B may be admitted only when one **same-model** numerical point is
reconstructible with a stated flavor basis, all relevant Yukawa/Majorana
matrices, breaking scales, intermediate EFT, and threshold ordering. An
approximate treatment may be retained if its effect is bounded and the
resulting authority ceiling is explicit. A source switch requires new
matching/recovery admission; Babu-Khan coefficients are not inherited.

Until one route passes those tests, no fit, Takagi-spectrum validation,
SMEFT+`N` evolution, `N_i` threshold, or proton-lifetime calculation is active.
`NONE_FOR_EXECUTION` is a choice against premature expenditure, not a verdict
against either SO(10) realization or the already-earned gauge-sector work.
