# ToE-Next

ToE-Next is a research project seeking the most coherent and complete unification obtainable from established physics, serious existing unification frameworks, surviving project results, and new physics only where evidence or mathematical consistency requires it.

The project has an initial dependency scaffold and one model-specific recovery chain with two completed bounded steps. Its first calculation passed: the Babu–Khan non-supersymmetric SO(10) heavy-vector boundary maps through the model's Pati–Salam intermediate symmetry into `Q_qque` and `Q_duql` in standard dimension-six BNV SMEFT, while the right-handed-neutrino term remains separately identified as `Q_qqdN`.

A focused primary-literature audit admitted the next calculation, which also passed. The single Pati-Salam BNV coefficient now has a verified one-loop gauge-leading-log evolution factor and is projected only afterward at `M_I` into the full-flavor SMEFT and SMEFT-plus-`N` boundary. The result is explicitly qualified by Babu-Khan's published high-scale-sextet beta convention. Running below `M_I`, right-handed-neutrino threshold matching, hadronic work, and proton-lifetime calculation remain inactive.

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
13. [`docs/OPEN_SEAMS.md`](docs/OPEN_SEAMS.md)
14. [`docs/PROVENANCE_AND_AUTHORITY.md`](docs/PROVENANCE_AND_AUTHORITY.md)
15. [`docs/LEGACY_HANDOFF.md`](docs/LEGACY_HANDOFF.md)

Repository structure is created only when concrete scientific work requires it. The first earned implementation surface is deliberately narrow:

- [`tools/vpc/`](tools/vpc/) contains a promoted exact-DAG secondary verifier with a frozen applicability boundary and minimal tests;
- [`tools/julia/`](tools/julia/) contains a small locked environment for Nemo and OrdinaryDiffEq plus one readiness smoke test;
- [`tools/readiness/check-c-only.ps1`](tools/readiness/check-c-only.ps1) checks that the active project and its computational stack operate from C: without the legacy custody drive.
- [`calculations/bk_so10_bnv_matching/`](calculations/bk_so10_bnv_matching/) contains the first calculation's compact derivation, coefficient map, and independent exact replays.
- [`calculations/bk_ps_bnv_running_mi_matching/`](calculations/bk_ps_bnv_running_mi_matching/) contains the exact Pati-Salam beta ledger, gauge-running derivation, `M_I` projector, and independent replay.

No model hierarchy, broad calculation framework, dataset, historical scientific tree, environment payload, or bulk generated result is stored here. The machine-level runtimes and package caches remain external to Git.
