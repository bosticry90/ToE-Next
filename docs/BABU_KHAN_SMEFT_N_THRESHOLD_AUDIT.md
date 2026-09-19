# Babu-Khan SMEFT+N Running and Right-Handed-Neutrino Threshold Audit

## Decision

```text
audit = BK_SMEFT_N_RUNNING_AND_N_THRESHOLD_ADMISSION_AUDIT_V1
outcome = NOT_ADMITTED_SOURCE_MODEL_INPUTS_AND_THRESHOLD_MATCHING_UNFROZEN
proposed_seam = BK_MI_TO_FIRST_N_THRESHOLD_BNV_NUSMEFT_RUNNING_AND_MATCHING
calculation_started = false
```

The boundary at `M_I` is scientifically meaningful, but it is not yet a
complete initial condition for controlled evolution through the singlet-neutrino
thresholds. The source model fixes the form of the Majorana and Dirac-neutrino
mass relations, but the audited construction does not freeze the numerical
family matrices, physical Majorana eigenvalues, mass ordering, or flavor
rotations required by the next calculation.

No running below `M_I`, singlet-neutrino diagonalization, threshold matching,
or proton-decay calculation was performed in this audit.

## Audited question

Can the already-established Babu-Khan boundary

```text
M_I boundary in BNV SMEFT plus singlet neutrinos
    -> one-loop running with all active N_i
    -> first physical N threshold
    -> controlled threshold match
```

be frozen tightly enough to admit one bounded calculation?

Admission requires all of the following before algebra or numerical evolution
begins:

1. a model-specific singlet-neutrino mass matrix and Dirac-neutrino Yukawa
   matrix at a declared scale and in a declared scheme;
2. the physical singlet-neutrino eigenvalues and the unitary rotation that
   defines their mass basis;
3. a justified threshold order, including the possibility of near-degenerate
   thresholds;
4. a closed operator basis and one-loop anomalous-dimension system between the
   two frozen scales;
5. an explicit disposition for `Q_qqdN` when an `N` field is removed;
6. known-limit, basis-covariance, uncertainty, and stopping tests.

The literature supplies item 4 and parts of items 5 and 6. It does not supply
the model-specific information needed for items 1 through 3, and the physical
BNV threshold carry-forward in item 5 is not turnkey.

## Inherited boundary

The previous calculations remain unchanged:

- one Pati-Salam-covariant BNV coefficient runs from `M_U` to `M_I` under the
  frozen published spectrum convention;
- the symmetry-breaking projection is applied only at `M_I`;
- the nonzero destination sectors are `Q_qque`, `Q_duql`, and `Q_qqdN` with
  full flavor tensors;
- `Q_qqdN` remains in the EFT with active singlet neutrinos rather than being
  discarded or forced into ordinary SMEFT;
- no singlet-neutrino mass basis or hierarchy was assumed by those results.

This audit does not modify either passed recovery step.

## Source-model neutrino information

The Babu-Khan construction writes the renormalizable Yukawa sector as

```text
16_F (Y_10 10_H + Y_126bar 126bar_H) 16_F
```

with two complex symmetric family matrices. In its compact mass notation,

```text
M_nu^D = r (H - 3 s F)
M_nu^M = r_R^-1 F = f sigma
```

where `H` and `F` are complex symmetric matrices. The source quotes viable
information for `r` and `s` and refers to earlier fermion-fit literature, but it
does not freeze the numerical `H`, `F`, and `r_R` needed here. Consequently it
does not determine, for this calculation:

- the three physical singular values of `M_nu^M`;
- whether every `N_i` lies materially below `M_I`;
- whether the thresholds are hierarchical or should be grouped;
- a sequence such as `M_I -> M_N3 -> M_N2 -> M_N1`;
- the Takagi rotation of the symmetric Majorana matrix;
- `Y_N` and the BNV coefficient tensor in the same mass/flavor convention.

Family labels do not establish a threshold order. The future threshold order
must be set by the physical masses after diagonalization.

## One-loop BNV running below M_I

Alonso et al. give the complete one-loop anomalous-dimension system for the six
dimension-six BNV operators in SMEFT with singlet neutrinos:

```text
Q_duql, Q_qque, Q_qqql, Q_duue, Q_qqdN, Q_uddN.
```

That result is the controlling running authority for this boundary. It includes
both gauge and Yukawa contributions. The Yukawa terms make the current nonzero
set non-closed by itself. In particular:

- `Q_qqdN` and `Q_duql` communicate through `Y_N` and `Y_u`;
- `Q_qqdN` can feed `Q_qqql` through `Y_N` and `Y_d`;
- the coupled system can populate `Q_uddN` and other initially vanishing
  sectors through the full flavor equations;
- wave-function and self-mixing terms depend on the complete Yukawa matrices.

Therefore a gauge-only continuation would suppress known, potentially
model-dependent mixing precisely where the model's fermion fit matters. It may
be useful later as an explicitly labeled approximation or cross-check, but it
cannot be the admitted controlled continuation of this source-model boundary.

The 2024 `wilson` extension implements numerical running in `nuSMEFT`, including
the two BNV operators with singlet neutrinos and the Alonso BNV running. It
requires the neutrino Yukawa matrix as external input. Its documented flavor
basis assumes no Majorana mass term, so it does not perform the Babu-specific
Majorana diagonalization or sequential threshold matching required here. The
package is not installed in the current ToE-Next Python environment and was not
installed by this audit.

## What happens at an N threshold

The dimension-six treatment in Alonso et al. states that below `M_N` the
singlet field is integrated out and the two operators containing `N` are
dropped from that dimension-six RGE system. That is a consistent statement
about the retained dimension-six truncation; it is not by itself a complete
physical matching prescription for a nonzero `Q_qqdN` coefficient.

Combining `Q_qqdN` with the renormalizable neutrino Yukawa interaction when a
massive `N_i` is integrated out can generate dimension-seven BNV SMEFT
descendants, schematically proportional to

```text
C_qqdN * Y_N / M_N.
```

The exact sign, flavor contractions, basis map, and accompanying seesaw
threshold terms must be derived under frozen conventions; the schematic
relation is not a result of this audit. Complete dimension-seven BNV operator
bases and their one-loop running exist in the literature, and the 2026
comprehensive BNV pipeline extends the ordinary-SMEFT path through higher
dimensions to LEFT and chiral EFT. The focused audit did not find a turnkey,
model-specific sequential threshold implementation that carries this
`Q_qqdN` boundary through the Babu-Khan `N_i` thresholds.

A future calculation must choose explicitly between:

1. a dimension-six-only truncation that drops the `N`-containing coefficient at
   threshold and states the resulting authority ceiling; or
2. a physical carry-forward that derives and retains the induced
   dimension-seven BNV coefficients.

The second route is required before claiming a complete proton-decay recovery
chain unless the first route's omitted contribution is independently bounded.

## Literature and infrastructure audit

| Source or capability | What is reusable | Limitation for this seam | Disposition |
|---|---|---|---|
| K.S. Babu and S. Khan, [arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2) | Model field content and the relations `M_nu^D = r(H-3sF)` and `M_nu^M = r_R^-1 F` | Does not freeze the numerical fermion fit, Majorana eigenvalues, ordering, or rotations needed here | Source-model authority; insufficient initial data |
| R. Alonso et al., [arXiv:1405.0486v2](https://arxiv.org/abs/1405.0486v2) | Complete one-loop dimension-six BNV gauge-plus-Yukawa RGEs including `Q_qqdN` and `Q_uddN` | Uses a generic singlet-neutrino EFT and does not supply Babu-specific thresholds | Controlling RGE authority |
| A. Datta et al., [arXiv:2010.12109v3](https://arxiv.org/abs/2010.12109v3) | Gauge anomalous dimensions for a broad SMNEFT operator set | Not the controlling complete BNV Yukawa system | Comparator only |
| A. Ardu and S. Marcano, [arXiv:2407.16751](https://arxiv.org/abs/2407.16751) | Complementary one-loop Yukawa-dependent `nuSMEFT` results | Does not replace the Alonso BNV system or provide this threshold match | Comparator only |
| S. Das Bakshi et al., [`wilson` `nuSMEFT` extension, arXiv:2411.07220](https://arxiv.org/abs/2411.07220) | Public full-flavor evolution framework; includes the singlet-neutrino BNV operators and Alonso running | Requires `Y_N`; current documented basis assumes no Majorana mass; no Babu-specific sequential threshold solution | Surveyed, not installed or adopted |
| Y. Liao and X.-D. Ma, [arXiv:1607.07309](https://arxiv.org/abs/1607.07309), and subsequent dimension-seven work | Complete dimension-seven SMEFT basis with BNV sector and one-loop running | Does not supply the model-specific `Q_qqdN` threshold coefficient | Reuse after a threshold map is derived |
| C.-Q. Song and J.-H. Yu, [arXiv:2603.11158v1](https://arxiv.org/abs/2603.11158v1) | Modern higher-dimensional SMEFT-to-LEFT-to-chiral BNV pipeline | Uses ordinary SMEFT fields and does not resolve the singlet-neutrino threshold | Downstream infrastructure candidate |
| J. Heeck, D. Sokhashvili, and A. Thapa, [arXiv:2603.17050v1](https://arxiv.org/abs/2603.17050v1) | Exhaustive tree-level UV completions for non-derivative BNV operators, including right-handed neutrinos | Classifies UV completions; it is not the required running and sequential matching calculation | Comparator and future UV cross-check |

No source or tool was copied, installed, or configured.

## Admission matrix

| Requirement | Status | Evidence or missing item |
|---|---|---|
| `M_I` BNV boundary | `PASS` | Previous matching and Pati-Salam running calculations |
| Babu-compatible fermion-fit benchmark | `FAIL_UNFROZEN` | No complete numerical `H`, `F`, `r`, `s`, `r_R` set has been selected and validated |
| `Y_N(M_I)` and `M_N(M_I)` in one scheme and basis | `FAIL_UNFROZEN` | Relations exist, numerical matrices do not |
| Physical `M_Ni` values and threshold ordering | `FAIL_UNFROZEN` | Requires Takagi diagonalization of the selected benchmark |
| Rotation of `C_qqdN` into the `N` mass basis | `FAIL_UNFROZEN` | Requires the same Takagi matrix and convention ledger |
| Complete one-loop BNV running above each threshold | `PASS_IN_LITERATURE` | Alonso gauge-plus-Yukawa system |
| Reusable numerical RGE implementation | `PARTIAL` | `wilson` `nuSMEFT` is available externally but is not installed and does not solve the Majorana thresholds |
| Sequential EFT tower | `BLOCKED` | Number, order, and degeneracy of active `N_i` are unknown |
| `Q_qqdN` threshold disposition | `BLOCKED` | Dimension-six dropping is documented; physical dimension-seven carry-forward remains to be derived or bounded |
| Known-limit and numerical controls | `SPECIFIABLE_NOT_EXECUTED` | Listed below; no admitted calculation exists |

The controlling failures are model inputs and threshold matching, not a lack of
general one-loop RGE machinery.

## Admission gate for the first downstream calculation

The proposed seam may be admitted only after all of these tests pass:

1. **Fit identity:** select one explicit, attributable fermion-fit benchmark
   compatible with the Babu-Khan field content and assumptions. Record its
   scale, scheme, input observables, fit quality, and any adaptation.
2. **Matrix reconstruction:** reconstruct `H`, `F`, `r`, `s`, and `r_R`, then
   derive `Y_u`, `Y_d`, `Y_e`, `Y_N`, and `M_N` in one convention.
3. **Independent mass check:** perform and independently replay the Takagi
   factorization of the complex symmetric `M_N`; verify residuals, positive
   masses, ordering, precision sensitivity, and near-degeneracies.
4. **Flavor rotation:** rotate every affected Yukawa matrix and the final index
   of `C_qqdN` into the same `N` mass basis. Verify unitary basis covariance.
5. **Threshold tower:** define the EFTs by the number of active singlets,
   `n_N = 3, 2, 1, 0`, or justify grouped thresholds. Admit only states whose
   physical masses lie below the current scale.
6. **Running system:** use the complete one-loop gauge-plus-Yukawa BNV equations
   between `M_I` and the highest physical `N` threshold. An intentionally
   gauge-only calculation must be separately scoped as an approximation.
7. **First threshold map:** freeze the operator conventions and derive the
   tree-level removal of the highest-mass state, including the standard seesaw
   terms and the disposition of its `Q_qqdN` component. If dimension-seven BNV
   descendants are retained, map them into a named complete basis.
8. **Fail-fast limits:** require zero-log recovery, `Y_N -> 0` decoupling,
   `C_qqdN -> 0` recovery of ordinary BNV SMEFT, degenerate-threshold
   consistency, and invariance under allowed unitary flavor-basis changes.
9. **Numerical controls:** predeclare ODE tolerances, convergence and precision
   replays, threshold-scale variation, conditioning checks, and uncertainty
   propagation from the fermion fit.
10. **Stopping boundary:** stop immediately after the first `N` threshold has
    been matched and independently checked. Do not continue to the next
    threshold, electroweak matching, LEFT, hadronic EFT, or lifetime prediction
    in the same calculation.

## Failure and authority rules

- If no attributable Babu-compatible benchmark supplies the required matrices,
  the proposed seam remains blocked rather than using an invented texture.
- If a physical `N_i` is not below `M_I`, it must be handled at the `M_I`
  boundary rather than evolved as an active lower-energy field.
- If thresholds are not well separated, sequential decoupling is not presumed;
  a grouped match must be justified.
- If the `Q_qqdN` threshold map is ambiguous, the calculation stops there.
- Passing the future first-threshold calculation would establish only one
  controlled interval and one threshold match. It would not establish the
  full low-energy chain, a proton lifetime, model viability, SO(10), or a
  Theory of Everything.

## Next prerequisite

The next bounded task is not RG evolution. It is:

```text
FREEZE_AND_VALIDATE_ONE_BABU_KHAN_COMPATIBLE_FERMION_FIT
```

That task should first determine whether a published fit can be adopted without
changing the source model. It may find a directly reconstructible compatible
fit, a numerically specified but incompatible fit, an underdefined fit, or no
relevant fit. It must not construct a texture simply to keep the chain moving.
Until a compatible benchmark is validated, the proposed downstream seam is
not active.

The subsequent [fit provenance audit](BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md)
found published, numerically specified *related* fits but no fit directly
adoptable under the frozen source-model assumptions. Its outcome is
`FIT_FOUND_BUT_INCOMPATIBLE_WITH_FROZEN_MODEL` for as-published use; it did
not execute a fit reconstruction or admit the downstream seam.
