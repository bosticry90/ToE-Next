# Ecosystem Survey

## Purpose and verdict

This no-install survey maps mature scientific infrastructure so ToE-Next builds only the missing integration layer. Listing a resource does not adopt it, install it, or make it scientific authority.

The initial verdict is:

- evaluated measurements, machine-readable experimental records, theory-model encodings, EFT exchange formats, domain evolution, observable prediction, likelihood evaluation, tensor algebra, event generation, and global fitting already have mature implementations;
- ToE-Next should reference or interface with those implementations when a concrete claim requires them;
- ToE-Next should not build a particle-data catalogue, event generator, EFT runner, observable library, Boltzmann solver, tensor algebra system, or general global-fit framework;
- the project-specific contribution is the explicit connection of assumptions to recovery maps, observables, evidence, verification, and assumption compression.

[project_state.json](../project_state.json) records only adopted project tooling. VPC is a promoted active tool; Nemo and OrdinaryDiffEq are calculation-capable project environments. Other machine-level software and every surveyed framework below remain capabilities or candidates, not ToE-Next dependencies.

Status labels mean:

- `READY_ON_C` — launched or imported from C: during the disconnected-drive readiness audit;
- `PROMOTED_ACTIVE_TOOL` — bounded source and tests are tracked by ToE-Next;
- `AVAILABLE_BUT_REVALIDATE_WHEN_USED` — callable now, but claim-specific readiness must be checked again;
- `SURVEYED_NOT_ADOPTED` — an external capability was reviewed from its authoritative documentation without installation or configuration.

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

Readiness is not scientific authority. Versions here are capability observations; a result's calculation record controls its reproducibility claim.

## Preserved/recoverable capabilities

| Capability | Status | Potential role | Required action before use |
|---|---|---|---|
| Legacy VPC product shell, numerical extensions, and historical profiles | Historical custody only; intentionally not promoted | Provenance or implementation reference | Reconnect custody deliberately, audit the exact need, and promote no more than the claim requires |
| Historical Lean proof corpora and scientific calculation trees | Historical custody only | Comparator or prior-result evidence | Consult by exact receipt; never make them hidden runtime dependencies |

Historical custody is not an active environment. No promoted tool may import, execute, or silently retrieve material from it.

## Surveyed external ecosystem

### Empirical authority and preserved analyses

| Resource | Mature role | Reuse decision | Boundary |
|---|---|---|---|
| [Particle Data Group](https://pdg.lbl.gov/) | Evaluated particle properties, constants, reviews, and machine-readable data | Reference as the default particle-physics baseline; do not rebuild | PDG evaluation is not a substitute for the primary experimental record or a candidate theory |
| [HEPData](https://www.hepdata.net/about) | Open repository for publication-linked collider tables, uncertainties, covariance information, and selected likelihood resources | Retrieve claim-specific records by persistent identifier and preserve exact provenance | Availability and statistical completeness vary by analysis |
| [Rivet](https://heprivet.org/) | Preserved collider analyses and comparison of Monte Carlo events with published observables | Reuse analysis routines when event-level predictions must reach unfolded measurements | An analysis implementation does not supply the candidate model or event generator |
| [pyhf](https://pyhf.readthedocs.io/en/stable/) | Pure-Python HistFactory-style likelihoods, fits, and limits from serialized workspaces | Reuse when a published compatible likelihood exists | A workspace's assumptions and asymptotic or non-asymptotic method must be audited |

HEPData's [analysis-resource guidance](https://hepdata-submission.readthedocs.io/en/latest/analyses.html) explicitly connects preserved records with Rivet analyses and HistFactory JSON resources. That is an interface to adopt when applicable, not a format to recreate.

### Particle models, EFTs, and collider predictions

| Resource | Mature role | Reuse decision | Boundary |
|---|---|---|---|
| [FeynRules](https://cp3.irmp.ucl.ac.be/projects/feynrules) | Derive Feynman rules from a specified Lagrangian and export maintained model formats | Use for a frozen Lagrangian when its supported domain matches the claim | Generated rules still require convention checks and independent physics validation |
| [UFO](https://arxiv.org/abs/1108.2040) | Generator-independent Python representation of model content and interactions | Prefer as a model-to-generator interface when supported | It represents a model; it does not establish that the model is correct |
| [SMEFTsim](https://github.com/SMEFTsim/SMEFTsim) | Maintained SMEFT FeynRules/UFO models with declared flavor and input-scheme choices | Compare with or reuse rather than creating a generic SMEFT encoding | Scheme, flavor assumptions, perturbative order, and documented limitations remain controlling |
| [WCxf](https://wcxf.github.io/) | Unambiguous JSON/YAML exchange of Wilson coefficients, EFTs, bases, and metadata | Adopt for coefficient interchange when an active calculation crosses compatible tools | A shared format does not remove matching, scale, or convention assumptions |
| [`wilson`](https://wilson-eft.github.io/wilson/) | SMEFT/WET running, matching, and basis translation | Reuse before implementing equivalent evolution machinery | Its implemented orders, sectors, and conventions define the supported claim boundary |
| [`flavio`](https://flav-io.github.io/docs/) | Flavor predictions, measurements, likelihoods, and Wilson-coefficient interfaces | Reuse for supported flavor observables | It is a domain engine, not a universal observable layer |
| [MadGraph5_aMC@NLO](https://cp3.irmp.ucl.ac.be/projects/madgraph/) | Matrix elements, cross sections, hard events, and matching for SM/BSM phenomenology | Invoke externally for a frozen collider claim; do not rebuild | Generator settings, perturbative accuracy, showering, cuts, and validation must be recorded |
| [LHAPDF](https://www.lhapdf.org/) | Standard PDF-set format and evaluation library | Reuse named sets with version/member and uncertainty treatment recorded | PDFs are fitted external inputs and can be material storage payloads |
| [Contur](https://hepcedar.gitlab.io/contur-webpage) | Constraints on BSM models using Rivet-preserved measurements | Consider for broad collider consistency attacks after a model can generate events | Complementary constraints are not a proof of completeness or discovery exclusion |

The natural reusable collider/EFT pathways are therefore interfaces, not a new local framework:

```text
frozen Lagrangian -> FeynRules/UFO -> MadGraph -> Rivet/HEPData -> likelihood
candidate coefficients -> WCxf -> wilson -> flavio -> observable/likelihood
```

Each arrow remains a scientific relation whose conventions, approximations, and uncertainty budget must be checked.

### Gravity, cosmology, and broad inference

| Resource | Mature role | Reuse decision | Boundary |
|---|---|---|---|
| [xAct](https://www.xact.es/) | Abstract/component tensor algebra and GR-focused extensions in the Wolfram Language | Use as a possible independent comparator to Cadabra when the claim merits it | Requires a Wolfram environment and claim-specific convention reconciliation |
| [CLASS](https://github.com/lesgourg/class_public) / [CAMB](https://camb.info/) | Background and perturbation evolution into CMB, lensing, and matter observables | Reuse for supported effective cosmologies; do not write a Boltzmann solver | Successful observable computation does not settle dark-sector, inflationary, or initial-condition mechanisms |
| [Cobaya](https://cobaya.readthedocs.io/en/latest/) | Bayesian sampling and interfaces among cosmological theory codes and likelihoods | Consider only when a defined inference problem warrants it | Priors, likelihood selection, convergence, and dataset compatibility remain scientific choices |
| [GAMBIT](https://gambitbsm.org/documentation/installation/introduction/) | Modular global BSM inference across collider, flavor, dark matter, cosmology, neutrino, and precision domains | Defer until a specific multi-domain inference task justifies its large integration surface | It is not directly native to Windows and would be a substantial project dependency |

## Do-not-rebuild map

| Needed capability | Default external authority | ToE-Next contribution |
|---|---|---|
| Evaluated particle facts | PDG | Cite the exact edition/value and propagate uncertainty |
| Experimental collider records | HEPData | Bind the exact record to the claim and preserve provenance |
| Generic model-to-vertex translation | FeynRules | Supply a frozen, attributed Lagrangian and validate conventions |
| Generator model interchange | UFO | Record identity, hash, supported order, and modifications |
| EFT coefficient exchange | WCxf | Define the physical matching claim and its authority ceiling |
| SMEFT/WET evolution and translation | `wilson` | Audit domain, scales, orders, and independent limits |
| Flavor observables | `flavio` | Connect a specific coefficient claim to data |
| Collider matrix elements/events | MadGraph5_aMC@NLO | Freeze inputs and control perturbative/numerical assumptions |
| Parton distributions | LHAPDF | Select, version, and propagate PDF uncertainty |
| Preserved collider analyses | Rivet | Validate the prediction-to-analysis interface |
| HistFactory inference | pyhf | Audit the likelihood and statistical interpretation |
| Broad collider reinterpretation | Contur | Interpret only within its measurement and model coverage |
| Tensor algebra | Cadabra/xAct | State geometry, conventions, checks, and physical meaning |
| Cosmological perturbation observables | CLASS/CAMB | Define the model-to-effective-parameter recovery map |
| Cosmological or multi-domain inference | Cobaya/GAMBIT | Supply the bounded model, priors, interfaces, and interpretation |

## What ToE-Next may need to build

The survey does not reveal a missing general-purpose physics engine. It reveals a project-specific integration problem. Only concrete work may earn implementation of:

1. explicit recovery maps between a candidate theory and an established lower-energy description;
2. small convention and basis adapters where no maintained standard already connects the selected tools;
3. claim-to-assumption-to-evidence lineage records;
4. cross-domain verification that checks the same claim through genuinely independent representations;
5. an assumption ledger that exposes which independent postulates a candidate actually removes, relocates, or adds.

These are scientific interfaces. They must not become a universal orchestration platform or a speculative directory hierarchy.

## Adoption test

Before adopting an external framework, a calculation must identify:

1. the exact missing capability;
2. why current tools or a standard interface are insufficient;
3. the smallest required integration surface;
4. provenance, license, version, and reproducibility requirements;
5. expected storage and maintenance cost;
6. how the framework will be removed or replaced if it fails the claim.

No resource surveyed in this document was installed, vendored, copied, or configured by this audit.
