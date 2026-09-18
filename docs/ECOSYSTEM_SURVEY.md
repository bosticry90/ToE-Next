# Ecosystem Survey

## Purpose

This is a preliminary capability map whose primary rule is: know what exists so ToE-Next does not rebuild it casually. Listing a tool or framework does not by itself adopt it or make it scientific authority.

[project_state.json](../project_state.json) now records VPC as a promoted active tool and Nemo plus OrdinaryDiffEq as the two adopted project frameworks. `tooling_vendored: true` refers only to the bounded, provenance-identified VPC source promotion; no runtime, package cache, legacy environment, or third-party framework source was copied into Git. Machine-level scientific software not listed there remains an external capability, not a project dependency.

Status labels mean:

- `READY_ON_C` — launched or imported from C: during the current readiness audit;
- `PROMOTED_ACTIVE_TOOL` — bounded source and tests are tracked by ToE-Next;
- `AVAILABLE_BUT_REVALIDATE_WHEN_USED` — callable now, but claim-specific readiness must be checked again.

## Existing computational capabilities

| Capability | Status | Verified observation | Potential role |
|---|---|---|---|
| Python 3.10 | `READY_ON_C` | Interpreter at `C:\Program Files\Python310\python.exe` | Orchestration and calculation-local execution |
| SymPy 1.14.0 / Python-FLINT 0.9.0 | `READY_ON_C` | Imported successfully | Symbolic and exact algebra |
| NumPy 2.2.6 / SciPy 1.15.3 / mpmath 1.3.0 | `READY_ON_C` | Imported successfully | Numerical algebra, integration, optimization, roots, and precision replay |
| Z3 / cvc5 1.3.4 / Hypothesis 6.165.1 | `READY_ON_C` | Python bindings imported successfully | Constraints, satisfiability, property-based and adversarial testing |
| Cadabra 2.5.14 | `AVAILABLE_BUT_REVALIDATE_WHEN_USED` | Launched by explicit C: path | Tensor, covariant, spinor, gamma, GR, and QFT algebra |
| Julia 1.12.6 | `READY_ON_C` | Launched by explicit C: path; not on PATH | Host for exact and numerical replay |
| Nemo 0.56.1 | `READY_ON_C` | Fresh locked ToE-Next environment resolved offline and exact-matrix smoke passed | Independent exact-algebra replay |
| OrdinaryDiffEq 7.2.1 | `READY_ON_C` | Fresh locked ToE-Next environment resolved offline and elementary ODE smoke passed | ODE dynamics, flow, evolution, and stability |
| Lean 4.34.0 / Lake 5.0.0 | `READY_ON_C` | Launchers executed and a trivial theorem compiled | Narrow exact theorems and decisive formal claims |
| VPC exact core | `PROMOTED_ACTIVE_TOOL` | Minimal pass/fail tests execute from [tools/vpc/](../tools/vpc/) | Selective secondary verification of supported exact DAG claims |

Readiness is not scientific authority. Versions recorded here are capability observations; calculation-specific reproduction records remain controlling for actual results.

## Preserved/recoverable capabilities

| Capability | Status | Potential role | Required action before use |
|---|---|---|---|
| Legacy VPC product shell, numerical extensions, and historical profiles | Historical custody only; intentionally not promoted | Possible provenance or implementation reference | Reconnect custody deliberately, audit the exact need, and promote no more than the claim requires |
| Historical Lean proof corpora and scientific calculation trees | Historical custody only | Comparator or prior-result evidence | Consult by exact receipt; never make them hidden runtime dependencies |

Historical custody is not an active environment. No promoted tool may import, execute, or silently retrieve material from it.

## External ecosystem candidates

These established resources may fill scaffold roles if a concrete scientific need justifies adoption:

| Capability | Existing resource | Default ToE-Next action |
|---|---|---|
| Particle-property and phenomenology baseline | PDG | Reference; do not rebuild |
| Experimental high-energy datasets | HEPData | Interface only when a claim needs the data |
| Particle-model encoding | FeynRules / UFO | Reuse a maintained representation when suitable |
| EFT coefficient interchange | WCxf | Adopt the format if an active calculation needs exchange |
| EFT running and matching | `wilson` | Evaluate before implementing equivalent machinery |
| Flavor observables | `flavio` | Reuse when its domain matches the claim |
| SMEFT reference models | SMEFTsim | Compare or reuse rather than duplicate |
| Collider matrix elements and events | MadGraph | Invoke externally for a defined collider claim |
| Broad BSM inference | GAMBIT | Defer until an inference problem justifies its scale |
| Tensor and gravity algebra | xAct | Compare with Cadabra and use the smallest competent route |

## Adoption test

Before adopting an external framework, a calculation must identify:

1. the exact missing capability;
2. why current tools or a standard interface are insufficient;
3. the smallest required integration surface;
4. provenance, license, version, and reproducibility requirements;
5. expected storage and maintenance cost;
6. how the framework will be removed or replaced if it fails the claim.

No framework is installed, vendored, copied, or configured merely to populate the scientific scaffold.
