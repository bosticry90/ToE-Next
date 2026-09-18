# ToE-Next

ToE-Next is a research project seeking the most coherent and complete unification obtainable from established physics, serious existing unification frameworks, surviving project results, and new physics only where evidence or mathematical consistency requires it.

The project begins with no active physics calculation and no active seams. Its first task is to construct a defensible scientific scaffold before selecting a concrete calculation.

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
5. [`docs/OPEN_SEAMS.md`](docs/OPEN_SEAMS.md)
6. [`docs/PROVENANCE_AND_AUTHORITY.md`](docs/PROVENANCE_AND_AUTHORITY.md)
7. [`docs/LEGACY_HANDOFF.md`](docs/LEGACY_HANDOFF.md)
8. [`docs/ECOSYSTEM_SURVEY.md`](docs/ECOSYSTEM_SURVEY.md)

Repository structure is created only when concrete scientific work requires it. The first earned implementation surface is deliberately narrow:

- [`tools/vpc/`](tools/vpc/) contains a promoted exact-DAG secondary verifier with a frozen applicability boundary and minimal tests;
- [`tools/julia/`](tools/julia/) contains a small locked environment for Nemo and OrdinaryDiffEq plus one readiness smoke test;
- [`tools/readiness/check-c-only.ps1`](tools/readiness/check-c-only.ps1) checks that the active project and its computational stack operate from C: without the legacy custody drive.

No model hierarchy, calculation hierarchy, dataset, historical scientific tree, environment payload, or generated result is stored here. The machine-level runtimes and package caches remain external to Git.
