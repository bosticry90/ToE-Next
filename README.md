# ToE-Next

ToE-Next is a research project seeking the most coherent and complete unification obtainable from established physics, serious existing unification frameworks, surviving project results, and new physics only where evidence or mathematical consistency requires it.

The project has an initial dependency scaffold and one model-specific recovery chain with two completed bounded steps. Its first calculation passed: the Babu–Khan non-supersymmetric SO(10) heavy-vector boundary maps through the model's Pati–Salam intermediate symmetry into `Q_qque` and `Q_duql` in standard dimension-six BNV SMEFT, while the right-handed-neutrino term remains separately identified as `Q_qqdN`.

A focused primary-literature audit admitted the next calculation, which also passed. The single Pati-Salam BNV coefficient now has a verified one-loop gauge-leading-log evolution factor and is projected only afterward at `M_I` into the full-flavor SMEFT and SMEFT-plus-`N` boundary. A subsequent source audit corrected the interval sextet's identity from high-scale `H_T` to intermediate-scale `Sigma_1` without changing the beta coefficients or recovery map.

The [downstream admission audit](docs/BABU_KHAN_SMEFT_N_THRESHOLD_AUDIT.md) found complete one-loop BNV SMEFT-plus-`N` running machinery, but the Babu-Khan source does not freeze the numerical fermion fit, singlet-neutrino masses, ordering, or flavor rotations required to use it. The physical `Q_qqdN` threshold carry-forward also requires an explicit dimension-seven disposition. The proposed running-and-threshold seam is therefore not admitted, and no calculation below `M_I` has begun.

A [published-fit provenance audit](docs/BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md) located the numerical point Babu-Khan quoted and a later full-RGE fit. Both are informative comparators but cannot be adopted unchanged under the frozen intermediate-spectrum and scalar-vev assumptions. No fermion benchmark has been selected or reconstructed.

A [fermion-source continuation decision](docs/FERMION_SOURCE_ROUTE_DECISION.md) compared a Babu-Khan-specific refit with switching to a published-fit SO(10) source model. Neither route is admitted for execution yet: the former requires a costed coupled-fit protocol, while the most explicit alternate prints matrices but approximates its Pati-Salam flavor interval. The two passed Babu-Khan gauge-sector boundaries remain intact.

A [proactive Babu-Khan fit-feasibility analysis](docs/BABU_KHAN_FIT_FEASIBILITY.md) derives exact two-matrix and scalar candidate-point checks, then identifies the missing model-specific Pati-Salam flavor-running and one-light-doublet matching kernel. It finds no optimization-free model no-go, but does not admit a fit before that theory kernel is derived and validated; no optimizer was run.

The [admitted flavor-kernel attempt](calculations/bk_ps_flavor_kernel/RESULT.md) checked the actual interval's universal one-loop Yukawa gauge terms and then stopped at a source-level scalar-projector inconsistency: the published `D11` relation lacks a factor `1/r` required by its own zero-mode equations. Independent exact Python and Julia/Nemo checks reproduce the discrepancy. The complete Yukawa RGEs and `M_I` projector are **not** established; this is not a Babu-Khan model rejection, and no fit or below-`M_I` evolution began.

A targeted [light-doublet and scalar-sample reconciliation](calculations/bk_light_doublet_projector_reconciliation/RESULT.md) finds that the first printed scalar point cannot have positive heavy doublet modes with Table 2's stated `sigma` exponent; a separate non-doublet mass is also off by about a factor of ten. A one-power exponent change removes these large contradictions, but the unprinted fine-tuned mass and full-precision inputs prevent validating the original zero mode or deciding whether the authors used the misprinted reduced identity. The printed point requires repair; the flavor kernel remains stopped.

A subsequent [parent-tensor normalization and positivity calculation](calculations/bk_scalar_tensor_recovery/RESULT.md) independently confirms several `54_H`, `10_H`, singlet-`126_H`, and singlet-mixing factors and derives an exact one-light/positive-heavy Schur criterion. It also finds that the source's potential and vacuum potential cannot share one literal `126_H` normalization for their identically named quadratic and quartic coefficients. The full `126_H` doublet/triplet Hessian and published `4 x 4` matrix are therefore neither confirmed nor refuted; no new scalar-point search or fermion fit was started.

The focused [scalar source-convention reconstruction](calculations/bk_scalar_source_convention/RESULT.md) finds a decisive same-symbol obstruction even before the full tensor Hessian: the printed vacuum potential's `lambda0` tadpole coefficient differs by a factor of four from the printed stationarity equation, and its accessible singlet Hessian does not agree with one common convention in the `126_H` diagonal. A single equation-independent translation cannot reconcile the formulas as printed. This is a source-formula conclusion, not a rejection of the field-content model.

A separate [canonical source-derived scalar reconstruction](calculations/canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md) remains **in the exploratory lane**, distinct from the printed Babu--Khan scalar model. Its complete 34-direction renormalizable invariant action, intended gauge stabilizer, exact tadpoles, and [full 35-block scalar Hessian](calculations/canonical_so10_full_hessian/RESULT.md) have passed their bounded gates. The [Stage 1 scalar benchmark](calculations/canonical_so10_scalar_benchmark/RESULT.md) is a locally positive high-scale stationary point with exactly 33 gauge plus one PQ zero modes. Its first light-Higgs tuning failed the [heavy-relaxed quartic test](calculations/canonical_so10_light_higgs_quartic/RESULT.md), but a [new exact tuning](calculations/canonical_so10_positive_higgs/RESULT.md) has one light complex Higgs doublet, positive remaining scalar masses, and a positive heavy-relaxed tree-level quartic. An initial [structured BFB/runaway probe](calculations/canonical_so10_bfb_probe/RESULT.md) found no negative ray, and a subsequent [orbit-space check](calculations/canonical_so10_bfb_orbit/RESULT.md) certified positivity of the pure self-dual `126_H` quartic and the `54_H+10_H` sector. The complete mixed-field quartic remains `BFB_UNRESOLVED`. A [bounded gauge-matching calculation](calculations/canonical_so10_gauge_matching/RESULT.md) generated the canonical SM scalar/vector ledgers and a coarse one-loop crossing. The subsequent [PS threshold-kernel calculation](calculations/canonical_so10_ps_threshold_kernel/RESULT.md) passed exact representation-projector, symmetry-restoration, vector-index, and whole-spectrum logarithmic checks. A [physical-vacuum matrix-threshold continuation](calculations/canonical_so10_matrix_threshold/RESULT.md) now passes basis-invariant SM-side scalar/vector log checks, but demonstrates that an upper-boundary PS generator does not commute with the frozen vector mass operator. The full non-degenerate two-boundary matching, finite vector/Goldstone/ghost terms, and interval ledger remain unearned: `PS_THRESHOLD_KERNEL_BLOCKED` and `GAUGE_MATCHING_BLOCKED`; no GeV scales were fitted. Global stability, loop-level perturbativity, fermion flavor, scalar-mediated baryon-number violation, and phenomenological GUT viability remain unestablished. No published Babu--Khan scalar benchmark or scalar threshold has been inherited.

The [physical lower-boundary background-field continuation](calculations/canonical_so10_lower_bfm/RESULT.md) verifies the nine `PS/SM` broken vector--Goldstone--ghost quadratic mass pairings in a partial `R_zeta` gauge. That checkpoint did not yet compute a one-loop `F²` term.

A [lower one-loop `F²` continuation](calculations/canonical_so10_lower_f2/RESULT.md) has since derived the finite and logarithmic **massive-vector** coefficient in the frozen partial background-field Feynman gauge, and checked the complete-`16_F` zero projected fermion gauge jump. A delayed-scalar-decoupling candidate also passes an exact lower logarithmic beta-jump checksum, but the required PS-covariant EFT field/operator map and UV/EFT hard-region subtraction remain unearned. The lower boundary is still blocked; the upper one-loop calculation and scale fit remain untouched.

The next calculation is specified in the [canonical PS interval EFT task and pass checklist](docs/CANONICAL_PS_INTERVAL_EFT_TASK.md). It first asks whether the frozen benchmark admits a controlled tree-level PS field/operator split; drafting this gate does not change the blocked one-loop matching status.

A bounded [audit of the explicit 2024 normal-ordering point](calculations/bdfss_2024_point_audit/RESULT.md) independently reconstructs its printed mass matrices and heavy-neutrino spectrum. An [independent parent-`SO(10)` sign derivation](calculations/real_120_sign_audit/RESULT.md) confirms that its unchanged real-`120_H` point violates the required opposite bidoublet conjugation signs. Its Pati-Salam flavor-running approximation and co-frozen threshold ordering remain uncontrolled. This specific point is not admitted as a replacement source; no refit or downstream BNV running began.

The particle-unification route is paused at its model-specific flavor boundary, preserving both passed gauge-sector recovery steps. A separate [gravity source-framework comparison](docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md) retains low-energy GR EFT as the baseline/control but admits no gravity source or active seam; no gravity calculation has begun.

A bounded [joint Standard-Model-plus-gravity EFT reference audit](docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md) now records a finite-order common low-energy control surface, its coefficient and assumption ledgers, and the limits of its observable authority. It admits no active cross-domain seam or new calculation.

A [massless-spin-2 assumption-compression audit](docs/MASSLESS_SPIN2_ASSUMPTION_COMPRESSION_AUDIT.md) compares soft-graviton, self-coupling, and geometric-uniqueness derivations against that ledger. It identifies conditional leading-order relations but no demonstrated net ToE assumption compression or new active seam.

A [quasiclassical recovery reference audit](docs/QUASICLASSICAL_RECOVERY_REFERENCE_AUDIT.md) separates decoherence, stable variables, effective classical dynamics, probability calculus, shared records, definite outcomes, and Born weights. Established mechanisms recover several of these conditionally, but no interpretation or active seam is selected.

A [project-wide seam-selection refresh](docs/PROJECT_WIDE_SEAM_REFRESH.md) applies the current admission rubric across particle, gravity, joint-interface, quantum-foundations, cosmological, thermodynamic, and cross-domain relations. No next calculation is currently admissible; the earlier bounded results and reference controls remain intact.

## Scientific posture

- Novelty is not a requirement.
- Provenance and attribution are requirements.
- Established physics is reused under its established identity rather than renamed or rebuilt.
- Hypotheses may be proposed freely, but authority must be earned through claim-scaled evidence.
- AI assists the research process but is never standalone scientific authority.
- Repository size is not a proxy for scientific completeness.

The sole machine-readable project-state authority is [`project_state.json`](project_state.json). Human-readable documents explain that state without creating competing status surfaces.

## Reading order

1. [`README.md`](README.md)
2. [`CHARTER.md`](CHARTER.md)
3. [`project_state.json`](project_state.json)
4. [`docs/SCIENTIFIC_BASELINE.md`](docs/SCIENTIFIC_BASELINE.md)
5. [`docs/ECOSYSTEM_SURVEY.md`](docs/ECOSYSTEM_SURVEY.md)
6. [`docs/DEPENDENCY_SCAFFOLD.md`](docs/DEPENDENCY_SCAFFOLD.md)
7. [`docs/SEAM_SELECTION.md`](docs/SEAM_SELECTION.md)
8. [`docs/SOURCE_THEORY_COMPARISON.md`](docs/SOURCE_THEORY_COMPARISON.md)
9. [`docs/BABU_KHAN_SO10_BNV_MATCHING.md`](docs/BABU_KHAN_SO10_BNV_MATCHING.md)
10. [`calculations/bk_so10_bnv_matching/RESULT.md`](calculations/bk_so10_bnv_matching/RESULT.md)
11. [`docs/BABU_KHAN_PS_RUNNING_AND_MI_MATCHING.md`](docs/BABU_KHAN_PS_RUNNING_AND_MI_MATCHING.md)
12. [`calculations/bk_ps_bnv_running_mi_matching/RESULT.md`](calculations/bk_ps_bnv_running_mi_matching/RESULT.md)
13. [`docs/BABU_KHAN_HT_THRESHOLD_AUDIT.md`](docs/BABU_KHAN_HT_THRESHOLD_AUDIT.md)
14. [`calculations/bk_ht_threshold_audit/RESULT.md`](calculations/bk_ht_threshold_audit/RESULT.md)
15. [`docs/BABU_KHAN_SMEFT_N_THRESHOLD_AUDIT.md`](docs/BABU_KHAN_SMEFT_N_THRESHOLD_AUDIT.md)
16. [`docs/BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md`](docs/BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md)
17. [`docs/FERMION_SOURCE_ROUTE_DECISION.md`](docs/FERMION_SOURCE_ROUTE_DECISION.md)
18. [`docs/BABU_KHAN_FIT_FEASIBILITY.md`](docs/BABU_KHAN_FIT_FEASIBILITY.md)
19. [`calculations/bdfss_2024_point_audit/RESULT.md`](calculations/bdfss_2024_point_audit/RESULT.md)
20. [`docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md`](docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md)
21. [`docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md`](docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md)
22. [`docs/MASSLESS_SPIN2_ASSUMPTION_COMPRESSION_AUDIT.md`](docs/MASSLESS_SPIN2_ASSUMPTION_COMPRESSION_AUDIT.md)
23. [`docs/QUASICLASSICAL_RECOVERY_REFERENCE_AUDIT.md`](docs/QUASICLASSICAL_RECOVERY_REFERENCE_AUDIT.md)
24. [`docs/PROJECT_WIDE_SEAM_REFRESH.md`](docs/PROJECT_WIDE_SEAM_REFRESH.md)
25. [`docs/OPEN_SEAMS.md`](docs/OPEN_SEAMS.md)
26. [`docs/PROVENANCE_AND_AUTHORITY.md`](docs/PROVENANCE_AND_AUTHORITY.md)
27. [`docs/LEGACY_HANDOFF.md`](docs/LEGACY_HANDOFF.md)

Repository structure is created only when concrete scientific work requires it. The first earned implementation surface is deliberately narrow:

- [`tools/vpc/`](tools/vpc/) contains a promoted exact-DAG secondary verifier with a frozen applicability boundary and minimal tests;
- [`tools/julia/`](tools/julia/) contains a small locked environment for Nemo and OrdinaryDiffEq plus one readiness smoke test;
- [`tools/readiness/check-c-only.ps1`](tools/readiness/check-c-only.ps1) checks that the active project and its computational stack operate from C: without the legacy custody drive.
- [`calculations/bk_so10_bnv_matching/`](calculations/bk_so10_bnv_matching/) contains the first calculation's compact derivation, coefficient map, and independent exact replays.
- [`calculations/bk_ps_bnv_running_mi_matching/`](calculations/bk_ps_bnv_running_mi_matching/) contains the exact Pati-Salam beta ledger, gauge-running derivation, `M_I` projector, and independent replay.
- [`calculations/bk_ht_threshold_audit/`](calculations/bk_ht_threshold_audit/) contains the exact sextet-attribution correction and symbolic branch comparison.

No model hierarchy, broad calculation framework, dataset, historical scientific tree, environment payload, or bulk generated result is stored here. The machine-level runtimes and package caches remain external to Git.
