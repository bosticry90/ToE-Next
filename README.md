# ToE-Next

ToE-Next is a research project seeking the most coherent and complete unification obtainable from established physics, serious existing unification frameworks, surviving project results, and new physics only where evidence or mathematical consistency requires it.

The project has an initial dependency scaffold and one model-specific recovery chain with two completed bounded steps. Its first calculation passed: the Babu–Khan non-supersymmetric SO(10) heavy-vector boundary maps through the model's Pati–Salam intermediate symmetry into `Q_qque` and `Q_duql` in standard dimension-six BNV SMEFT, while the right-handed-neutrino term remains separately identified as `Q_qqdN`.

A focused primary-literature audit admitted the next calculation, which also passed. The single Pati-Salam BNV coefficient now has a verified one-loop gauge-leading-log evolution factor and is projected only afterward at `M_I` into the full-flavor SMEFT and SMEFT-plus-`N` boundary. A subsequent source audit corrected the interval sextet's identity from high-scale `H_T` to intermediate-scale `Sigma_1` without changing the beta coefficients or recovery map.

The [downstream admission audit](docs/BABU_KHAN_SMEFT_N_THRESHOLD_AUDIT.md) found complete one-loop BNV SMEFT-plus-`N` running machinery, but the Babu-Khan source does not freeze the numerical fermion fit, singlet-neutrino masses, ordering, or flavor rotations required to use it. The physical `Q_qqdN` threshold carry-forward also requires an explicit dimension-seven disposition. The proposed running-and-threshold seam is therefore not admitted, and no calculation below `M_I` has begun.

A [published-fit provenance audit](docs/BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md) located the numerical point Babu-Khan quoted and a later full-RGE fit. Both are informative comparators but cannot be adopted unchanged under the frozen intermediate-spectrum and scalar-vev assumptions. No fermion benchmark has been selected or reconstructed.

A [fermion-source continuation decision](docs/FERMION_SOURCE_ROUTE_DECISION.md) compared a Babu-Khan-specific refit with switching to a published-fit SO(10) source model. Neither route is admitted for execution yet: the former requires a costed coupled-fit protocol, while the most explicit alternate prints matrices but approximates its Pati-Salam flavor interval. The two passed Babu-Khan gauge-sector boundaries remain intact.

A bounded [audit of the explicit 2024 normal-ordering point](calculations/bdfss_2024_point_audit/RESULT.md) independently reconstructs its printed mass matrices and heavy-neutrino spectrum. An [independent parent-`SO(10)` sign derivation](calculations/real_120_sign_audit/RESULT.md) confirms that its unchanged real-`120_H` point violates the required opposite bidoublet conjugation signs. Its Pati-Salam flavor-running approximation and co-frozen threshold ordering remain uncontrolled. This specific point is not admitted as a replacement source; no refit or downstream BNV running began.

The particle-unification route is paused at its model-specific flavor boundary, preserving both passed gauge-sector recovery steps. A separate [gravity source-framework comparison](docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md) retains low-energy GR EFT as the baseline/control but admits no gravity source or active seam; no gravity calculation has begun.

A bounded [joint Standard-Model-plus-gravity EFT reference audit](docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md) now records a finite-order common low-energy control surface, its coefficient and assumption ledgers, and the limits of its observable authority. It admits no active cross-domain seam or new calculation.

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
18. [`calculations/bdfss_2024_point_audit/RESULT.md`](calculations/bdfss_2024_point_audit/RESULT.md)
19. [`docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md`](docs/GRAVITY_SOURCE_FRAMEWORK_COMPARISON.md)
20. [`docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md`](docs/JOINT_SM_GR_EFT_REFERENCE_AUDIT.md)
21. [`docs/OPEN_SEAMS.md`](docs/OPEN_SEAMS.md)
22. [`docs/PROVENANCE_AND_AUTHORITY.md`](docs/PROVENANCE_AND_AUTHORITY.md)
23. [`docs/LEGACY_HANDOFF.md`](docs/LEGACY_HANDOFF.md)

Repository structure is created only when concrete scientific work requires it. The first earned implementation surface is deliberately narrow:

- [`tools/vpc/`](tools/vpc/) contains a promoted exact-DAG secondary verifier with a frozen applicability boundary and minimal tests;
- [`tools/julia/`](tools/julia/) contains a small locked environment for Nemo and OrdinaryDiffEq plus one readiness smoke test;
- [`tools/readiness/check-c-only.ps1`](tools/readiness/check-c-only.ps1) checks that the active project and its computational stack operate from C: without the legacy custody drive.
- [`calculations/bk_so10_bnv_matching/`](calculations/bk_so10_bnv_matching/) contains the first calculation's compact derivation, coefficient map, and independent exact replays.
- [`calculations/bk_ps_bnv_running_mi_matching/`](calculations/bk_ps_bnv_running_mi_matching/) contains the exact Pati-Salam beta ledger, gauge-running derivation, `M_I` projector, and independent replay.
- [`calculations/bk_ht_threshold_audit/`](calculations/bk_ht_threshold_audit/) contains the exact sextet-attribution correction and symbolic branch comparison.

No model hierarchy, broad calculation framework, dataset, historical scientific tree, environment payload, or bulk generated result is stored here. The machine-level runtimes and package caches remain external to Git.
