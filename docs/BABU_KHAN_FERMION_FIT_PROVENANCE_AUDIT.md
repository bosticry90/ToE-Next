# Babu-Khan Fermion-Fit Provenance and Reconstructibility

## Decision

```text
audit = BK_FERMION_FIT_PROVENANCE_AND_RECONSTRUCTIBILITY_V1
outcome = FIT_FOUND_BUT_INCOMPATIBLE_WITH_FROZEN_MODEL
qualified_meaning = PUBLISHED_FITS_CANNOT_BE_ADOPTED_AS_IS
fit_selected = null
calculation_started = false
```

Here *incompatible* means incompatible **for direct use as the frozen numerical
boundary of this particular Babu-Khan construction**. It does not mean that its
two-matrix Yukawa structure has been disproved or that a new, model-consistent
fit is impossible. No published fit examined in this focused lineage audit
simultaneously supplies the required matrices, conventions and scales while
retaining the `54_H -> Pati-Salam with D parity -> 126_H -> SM` spectrum and
the frozen Peccei-Quinn/two-Yukawa assumptions. No fit is promoted into
`project_state.json` as a benchmark.

This is a source and reconstructibility audit, not a fit reconstruction. No
matrix was entered into a numerical program, diagonalized or used for running.

## Acceptance test

For an as-published benchmark to pass, it must provide an attributable
renormalizable non-SUSY `10_H + 126bar_H` two-symmetric-matrix fit, with the
same restrictions on the conjugate `10_H` coupling and Higgs-vev phases as the
Babu-Khan source. It must give sufficient numerical data and conventions to
obtain `H`, `F`, `r`, `s`, `r_R`, `Y_u`, `Y_d`, `Y_e`, `Y_N`, and `M_N` at specified
scale(s), including a justified translation through the actual Pati-Salam
interval and `M_I` threshold. The fit quality, input data, evolution and
matching scheme must be identifiable. The numerical Majorana spectrum and
Takagi rotation would then be independently reproduced in a **separately
admitted calculation**, not asserted from a suggestive related model.

An algebraically similar Yukawa Lagrangian is necessary but not sufficient:
moving its fitted matrices across a different breaking chain, threshold
spectrum or scalar vacuum changes the physical initial condition.

## Babu-Khan source and the exact cited fit

[Babu and Khan, arXiv:1507.06712v2, section 7](https://arxiv.org/html/1507.06712v2)
give `M_nu^D = r(H - 3sF)` and `M_N = r_R^-1 F`, with complex symmetric `H`
and `F`. Their `r ~ 69`, `s ~ 0.36 - 0.04i` illustration refers directly to
[Joshipura and Patel, arXiv:1102.5148v1](https://arxiv.org/html/1102.5148),
whose appendix prints `r = 69.1739`, `s = 0.362941 - 0.0463175i`, a diagonal
charged-lepton matrix, and a complex symmetric down-quark matrix. Its type-I
table gives `r_R = 5.62 x 10^-14` in its convention. Thus this is a real,
substantially reconstructible *Joshipura-Patel* fit, not a missing citation or
an invented texture: `H=(M_d+M_l)/4` and `F=(M_d-M_l)/4` can be reconstructed
in the published charged-lepton basis, subject to its stated rounding.

It does **not** thereby become a frozen Babu-Khan fit:

- Joshipura-Patel's non-SUSY realization uses `45_H + 10_H + 126bar_H`,
  whereas Babu-Khan uses `54_H + 126_H + 10_H` and a D-parity-preserving
  Pati-Salam interval. The former discusses an intermediate unification scale
  near `10^11 GeV`; Babu-Khan places `M_I` near `10^13-10^14 GeV`.
- The printed point fits charged-fermion inputs extrapolated to
  `M_GUT = 2 x 10^16 GeV` using a non-SUSY SM extrapolation with a
  `140 GeV` Higgs input. It is not a coupled fit through Babu-Khan's actual
  Pati-Salam spectrum and thresholds to an `M_I` EFT boundary.
- Its `s` has a nonzero imaginary part. Babu-Khan explicitly discusses this
  small phase, states that its scalar realization has no independent phase
  associated with `s`, and says the mass-and-mixing chi-squared fit may have
  to be redone. Replacing complex `s` by its real part is not a validated fit.
- The model-specific Higgs-doublet mixing, scale/scheme translation, and
  consistency of the reconstructed Yukawa matrices with the frozen scalar
  benchmark have not been demonstrated.

The fit is a valuable starting comparator for a future re-fit, not an
authorized `Y_N(M_I)` or `M_N(M_I)` input.

## Other close published fits

| Primary source | Positive evidence | Direct-adoption failure |
|---|---|---|
| [Dueck and Rodejohann, arXiv:1306.4468v3](https://arxiv.org/html/1306.4468v3), model MN | Appendix A prints explicit minimal non-SUSY `H`, `F`, `r`, `s`, `r_R` for both no-RGE and full-RGE fits; the latter integrates heavy neutrinos one by one | It explicitly neglects intermediate breaking chains, treating them as near `M_GUT`; its fitted `s` remains complex. The no-RGE and RGE points are different fits (reported chi-squared values 1.103 and 22.97), not interchangeable Babu-Khan `M_I` data. |
| [Babu and Macesanu, hep-ph/0505200v2](https://arxiv.org/html/hep-ph/0505200v2) | Two-matrix type-I SO(10) fit lineage | Its illustrated fit has `tan beta` and `M_SUSY` inputs; it is supersymmetric, not the frozen non-SUSY spectrum. |
| [Haba, Shimizu and Yamada, arXiv:2304.06263v2](https://arxiv.org/html/2304.06263v2) | `54_H + 126_H + 10_H` and a Pati-Salam intermediate scale closer to Babu-Khan | It deliberately allows Yukawa coupling to both the complex `10_H` and its conjugate, rather than Babu-Khan's PQ-restricted two-matrix Yukawa sector. |
| [Kaladharan and Saad, arXiv:2308.04497v2](https://arxiv.org/abs/2308.04497v2) | Addresses tension from running in a PQ-motivated SO(10) fermion fit | Adds a fundamental fermion and spinorial scalar to the minimal framework, changing the frozen model. |
| [Babu et al., arXiv:2409.03840v1](https://arxiv.org/abs/2409.03840v1) | Explicit modern fermion and singlet-neutrino fits | Uses real `10_H`, real `120_H`, and `126bar_H`; the extra `120_H` changes the Yukawa structure. |

The later literature was checked to avoid overlooking a closer numerical
benchmark; these papers are comparators, not substitute boundary conditions.
This focused search cannot prove that no compatible fit exists anywhere.

## Acceptance matrix

| Requirement | Joshipura-Patel quoted point | Dueck-Rodejohann MN RGE point |
|---|---|---|
| Attributable numerical matrices and `r,s,r_R` | `PASS_WITH_ROUNDING`: matrices/parameters printed across appendix and table | `PASS`: Appendix A explicitly prints the matrices and parameters |
| Two symmetric `10_H + 126bar_H` Yukawa structure, no `120_H` | `PASS` at the Yukawa-Lagrangian level | `PASS` at the Yukawa-Lagrangian level |
| Same frozen scalar breaking and intermediate spectrum | `FAIL`: `45_H` construction and different intermediate assumptions | `FAIL`: intermediate chain neglected |
| Same frozen scalar-vev phase restriction | `FAIL_FOR_AS_IS_USE`: complex `s`; Babu-Khan calls for a re-fit | `FAIL_FOR_AS_IS_USE`: complex `s` |
| Declared and compatible scale/scheme translation to `M_I` | `FAIL`: one-step GUT-scale input extrapolation | `FAIL`: SM RGE with intermediate symmetry omitted |
| Validated Babu-Khan `Y_N(M_I)`, `M_N(M_I)` | `NOT_EARNED` | `NOT_EARNED` |
| Independently checked Takagi masses and rotation | `NOT_RUN` | `NOT_RUN` |

The binary outcome here is **not** `FIT_FOUND_AND_RECONSTRUCTIBLE` for the
frozen model, despite publication of reconstructible *related* points. It is
also not `NONE`: concrete fit points were found. `FIT_FOUND_BUT_UNDERDEFINED`
does not describe the principal obstacle of the two best-documented points;
their numerical input exists, but direct model compatibility fails.

## Consequence and stopping rule

The `M_I -> first N threshold` BNV seam remains unadmitted, with no active
physics calculation. Do not infer an `N_3,N_2,N_1` ordering from family labels,
paste the Joshipura-Patel matrices into Babu-Khan, make `s` real by fiat,
substitute a different model's published heavy-neutrino spectrum, or install
an RGE engine to mask the missing initial condition.

An independently authorized next scientific decision may either admit a
**new Babu-Khan-specific fermion re-fit** with its scalar, Pati-Salam and
threshold assumptions frozen, or compare another source model with a
published compatible fit. This audit chooses neither automatically. Only a
validated model-specific fit could earn the subsequent Takagi-spectrum
calculation; RG evolution remains downstream of that result.
