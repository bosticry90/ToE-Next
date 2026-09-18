# Source-Theory Comparison

## Decision

```text
SOURCE CANDIDATE SELECTED FOR SEAM EVALUATION:
    Babu-Khan 2015 non-supersymmetric SO(10)
    Higgs content: 54_H + 126_H + 10_H
    Breaking route: Pati-Salam with discrete parity as the intermediate stage

AUTHORITY: WORKING_CANDIDATE_NOT_ACCEPTED
SEAM AT COMPLETION OF THIS COMPARISON: NONE
SUBSEQUENT ADMISSION: docs/BABU_KHAN_SO10_BNV_MATCHING.md

CANDIDATE RELATION:
    heavy-vector SO(10) sector
        -> Pati-Salam baryon-number-violating EFT boundary
        -> dimension-six baryon-number-violating SMEFT coefficients
        -> LEFT/chiral matching and running
        -> nucleon-decay observables
```

This comparison selected at most one source theory for evaluating whether a precise seam could be activated. It did not accept SO(10), this model, its symmetry-breaking history, or any predicted lifetime as established physics. The later [model-specific admission decision](BABU_KHAN_SO10_BNV_MATCHING.md) authorizes only a tree-level operator-matching calculation and no tool installation.

## Question and method

The [first seam-selection brief](SEAM_SELECTION.md) identified unified or ultraviolet particle theory to SMEFT/WET as the leading relation class, but no source endpoint. This comparison asks which mature source framework, if any, offers the most consequential and tractable recovery relation into established low-energy physics.

Candidates are compared on:

1. what is unified and what remains independent;
2. recovery of Standard Model gauge structure and representations;
3. treatment of neutrino masses, flavor, symmetry breaking, and proton-decay constraints;
4. parameter and assumption burden;
5. clarity of the path into SMEFT/WET and observables;
6. maturity of supporting literature and external infrastructure;
7. availability of a cheap decisive falsifier;
8. legacy leverage without inherited preference;
9. the maximum authority a successful bounded calculation could earn.

Canonical frameworks are the comparison level; a source is selectable only if a sufficiently explicit published construction also defines the fields, breaking route, and observable path needed to assess a seam.

## Framework comparison

| Framework | Unification gained | Principal unresolved burden | EFT and observable route | Cheap discriminator | Disposition |
|---|---|---|---|---|---|
| Strict Georgi-Glashow SU(5) | One simple gauge group; Standard Model matter fits into `10 + 5bar`; charge quantization | No right-handed neutrino in the minimal matter assignment; incorrect minimal charged-fermion relations; doublet-triplet, threshold, and proton-decay problems require extensions | Direct heavy-vector and colored-scalar routes to baryon-number-violating operators and nucleon decay | Proton-decay channels and gauge-unification consistency | Not selected: exceptionally simple, but the strict model is too deficient and repaired variants move substantial assumptions into added representations and thresholds |
| Pati-Salam | Unifies quarks with leptons through `SU(4)_C` and provides left-right structure with a right-handed neutrino | Product-group couplings remain independent unless embedded; Higgs, flavor, breaking, and baryon-number structure are model dependent | Leptoquark, right-handed-current, neutrino, and flavor operators can map into SMEFT/WET | Flavor/lepton-number constraints and model-specific mediator patterns | Retained as a valuable intermediate symmetry, not selected as the standalone source theory |
| SO(10) | A complete family, including a right-handed neutrino, fits into one `16`; a simple group contains both SU(5) and Pati-Salam routes | The framework alone does not choose Higgs representations, breaking chain, thresholds, Yukawa textures, or vacuum; proton lifetime is highly threshold sensitive | Heavy vectors and scalars can generate baryon-number-violating SMEFT; seesaw/flavor sectors can feed lepton-number and flavor EFTs | Threshold-aware unification plus nucleon decay for a frozen model | **Selected only through one explicit published construction** |
| E6 | A family can occupy a `27`, decomposing under SO(10) into `16 + 10 + 1`; offers a larger unified structure | Extra matter, its decoupling, additional breaking stages, Higgs structure, and flavor assumptions increase the initial burden | Rich EFT signatures are possible but depend on the exotic spectrum and breaking route | No equally cheap model-independent discriminator for the broader framework | Not selected: additional structure is not justified for the first bounded relation |

The original SU(5), Pati-Salam, SO(10), and E6 proposals establish the canonical structures used in this comparison. They do not by themselves fix a modern calculational benchmark.

## Candidate constructions within SO(10)

### Selected working candidate

K. S. Babu and S. Khan specify a renormalizable, non-supersymmetric SO(10) construction with `54_H`, `126_H`, and `10_H`, one Pati-Salam intermediate stage with discrete parity, a two-matrix Yukawa sector, an explicit scalar potential, and threshold corrections. The paper also states a Peccei-Quinn completion and derives proton-decay expectations. This combination supplies a version-frozen source with substantially more of the recovery chain exposed than the SO(10) label alone.

The selected source authority is the final arXiv version and published article:

- K. S. Babu and S. Khan, *Minimal nonsupersymmetric SO(10) model: Gauge coupling unification, proton decay, and fermion masses*, [arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2), [Phys. Rev. D 92, 075018](https://doi.org/10.1103/PhysRevD.92.075018).

Selection is driven by the model's explicit breaking and threshold structure and its calculable proton-decay interface. It is not an endorsement of its naturalness, scalar hierarchy, cosmology, flavor fit, or completeness as a unification.

### Sensitivity control, not the selected source

S. M. Boucenna, T. Ohlsson, and M. Pernow study a different minimal non-supersymmetric SO(10) construction breaking directly to the Standard Model and report a testable proton lifetime and potentially accessible scalar octets. Their analysis explicitly uses one-loop running and neglects threshold corrections and higher-dimensional operators. It is therefore useful as a control showing how strongly conclusions can depend on the breaking and threshold assumptions, but it is less suitable for the first threshold-aware recovery claim.

- S. M. Boucenna, T. Ohlsson, and M. Pernow, *A minimal non-supersymmetric SO(10) model with Peccei-Quinn symmetry*, [arXiv:1812.10548](https://arxiv.org/abs/1812.10548).

## Assumption ledger for the selected candidate

Selection does not presume net assumption compression.

Potentially compressed or related within the candidate:

- one simple gauge group replaces the independent Standard Model gauge factors above the breaking scale;
- each matter family, including a right-handed neutrino, is organized in a single spinor representation;
- quark and lepton quantum numbers and charge relations share a group-theoretic origin;
- the renormalizable fermion sector is organized around two Yukawa matrices rather than unrelated sector-by-sector interactions.

Still independent, added, or relocated:

- the existence of three generations;
- the choice of `54_H`, `126_H`, and `10_H` and the stated Peccei-Quinn structure;
- the Pati-Salam breaking route, discrete parity history, vacuum, and boundary conditions;
- scalar-potential parameters, hierarchy assumptions, doublet-triplet separation, and threshold spectrum;
- Yukawa textures, phases, flavor rotations, and their fitted values;
- the selection of a phenomenologically viable region from the model's parameter space;
- quantum gravity, cosmological initial conditions, and the other sectors outside this particle-unification claim.

A later calculation must determine whether the relation removes assumptions, correlates them, or merely transfers them to the heavy spectrum and boundary data.

## Candidate relation for seam evaluation

### Proposed endpoints

Source endpoint:

- the heavy gauge-boson sector of the Babu-Khan model at a frozen symmetry-breaking and threshold benchmark;
- its couplings, masses, flavor rotations, and convention choices sufficient to integrate out the baryon-number-violating mediators.

Intermediate endpoint:

- a Pati-Salam-covariant dimension-six BNV operator boundary below the GUT-scale heavy-vector poles;
- an explicit disposition for operators containing the right-handed neutrino and a branching map at the Pati-Salam-to-Standard-Model threshold.

Destination endpoint:

- a named dimension-six baryon-number-violating SMEFT basis on the Standard-Model side of the intermediate threshold;
- subsequent running and matching into a named low-energy/chiral basis;
- a defined set of nucleon-decay partial widths with stated hadronic matrix elements and experimental comparators.

The proposed scientific arrow is:

```text
frozen SO(10) heavy-vector interactions
    -> tree-level Pati-Salam-covariant baryon-number-violating operators
    -> Pati-Salam running and matching at the intermediate scale
    -> dimension-six baryon-number-violating SMEFT coefficients
    -> controlled running and low-energy/chiral matching
    -> selected proton or neutron decay widths
    -> comparison with identified experimental limits
```

The intermediate EFT is not optional bookkeeping. The selected source breaks through `SU(4)_C x SU(2)_L x SU(2)_R x D`, so a direct SMEFT evolution from the unification scale would erase active fields and symmetries. The first admitted calculation therefore tests the tree-level operator map and its intermediate-symmetry bridge; it does not run SMEFT above the Pati-Salam breaking scale.

A recent systematic treatment of baryon-number-violating UV-to-SMEFT-to-LEFT-to-chiral matching provides a candidate modern endpoint convention and cross-check, but no implementation is adopted by this decision:

- C.-Q. Song and J.-H. Yu, *Comprehensive Effective Field Theory Analysis for Baryon Number Violating Processes*, [arXiv:2603.11158](https://arxiv.org/abs/2603.11158).

### Inputs that must be frozen before activation

1. the exact source version and the subset of its benchmark parameter space under test;
2. gauge conventions, generator normalization, heavy-vector masses, and interaction vertices;
3. scalar thresholds used to establish the unification and intermediate scales;
4. fermion-basis conventions, Yukawa solution, flavor rotations, and treatment of neutrino states;
5. SMEFT and low-energy operator bases, signs, normalizations, matching scale, and perturbative order;
6. renormalization-group and threshold treatment with declared uncertainties;
7. lattice or other hadronic matrix elements and their covariance or uncertainty model;
8. exact decay channels, experimental datasets, and statistical comparison rule;
9. the independent-replay route and a failure interpretation for each stage.

These inputs are now narrowed for the first link in [BABU_KHAN_SO10_BNV_MATCHING.md](BABU_KHAN_SO10_BNV_MATCHING.md). Later running and observable stages remain inactive and require their own calculation-local freezes.

## Cheap falsifier and stopping rule

The cheapest decisive attack is ordered to fail early:

1. derive the heavy-vector baryon-number-violating operator pattern, preserve the Pati-Salam intermediate symmetry, and test its projection into a declared SMEFT basis for gauge, normalization, flavor, and convention consistency;
2. only if that map passes, re-evaluate threshold-aware gauge-coupling and intermediate-scale consistency using current inputs and the paper's stated model assumptions;
3. run and match only the surviving pattern to the selected nucleon-decay channels;
4. compare the uncertainty-bounded predictions with the frozen experimental limits.

Stop without enlarging the model if:

- the source benchmark cannot reproduce its required scale relation within the declared threshold treatment;
- the derived operator pattern is inconsistent with the source symmetries or cannot be mapped unambiguously into the chosen basis;
- no tested parameter region survives a frozen nucleon-decay limit once declared uncertainties are propagated; or
- sensitivity to uncontrolled thresholds, flavor choices, or hadronic inputs prevents the planned authority ceiling from being reached.

Current primary experimental comparators include Super-Kamiokande limits for `p -> e+ pi0` and `p -> mu+ pi0`, and its newer searches for `p -> nu-bar pi+` and `n -> nu-bar pi0`. Exact channels and versions must be frozen before computation:

- Super-Kamiokande Collaboration, [arXiv:2010.16098](https://arxiv.org/abs/2010.16098), [Phys. Rev. D 102, 112011](https://doi.org/10.1103/PhysRevD.102.112011);
- Super-Kamiokande Collaboration, [arXiv:2510.26232v2](https://arxiv.org/abs/2510.26232v2).

## Verification and authority ceiling

The admitted first link and any later downstream link must use claim-scaled verification:

- symbolic derivation with dimensional, group-theoretic, basis, and limiting-case checks;
- an independent exact or symbolic replay of the coefficient pattern when practical;
- numerical running with convergence, truncation, conditioning, precision, and uncertainty controls;
- comparison against the source paper, the modern EFT pipeline, and the current experimental records;
- an adversarial audit of threshold and flavor sensitivity.

A failure may exclude or qualify only the frozen model region and recovery assumptions actually tested. It cannot exclude SO(10), grand unification, or all possible ultraviolet sources.

A success can establish only that one specified SO(10) benchmark admits a controlled baryon-number-violating recovery chain consistent with the selected data at the declared accuracy. It cannot establish SO(10) as true, prove a Theory of Everything, or demonstrate net assumption compression outside the audited ledger.

## Software and storage disposition

No new tool or framework is required or adopted by this comparison. The existing C:-resident symbolic, exact-algebra, constraint, numerical, and verification capabilities are sufficient to begin a bounded derivation once the calculation record is frozen. No audited turnkey source-model-to-baryon-violating-EFT implementation has been identified as a project dependency.

If a later calculation needs an external package, model encoding, or data payload, it must earn adoption through the calculation's claim and provenance requirements. Large outputs remain external under the repository's storage policy.

## D:-connected legacy SU(5) relevance audit

```text
SOURCE-COMPARISON OUTCOME: NO_MATERIAL_CHANGE
REUSE OUTCOME: REUSABLE_SU5_METHODS_AND_BOUNDED_RESULTS_IDENTIFIED
SU(5) REACTIVATION: NO
```

The complete local custody repository was reconnected and audited at freeze commit `a7ac8ddb2457ed4f44dca8ddab6aa6874dd610e3`. The audit inspected the C02 pause, accepted operator-interface controls, threshold qualifications, source-review boundary, matching/RG status, and proton-decay artifacts. It did not rerun or extend SU(5).

| Audit question | Finding | Consequence for the SO(10) decision |
|---|---|---|
| Was a complete strict-SU(5) UV-to-observable chain already executed? | No. Matching, RG evolution, numerical widths, lifetimes, and model viability remained unauthorized or unevaluated; C02 later remained paused and unadjudicated. | No basis to replace the selected source with strict SU(5) |
| Is there an accepted reusable operator interface? | Yes. Independent review reproduced the four dimension-six BNV weak-basis SMEFT tensor rows, flavor/sign controls, a dimension-seven endpoint-sign map, and fail-closed threshold guards within a restricted control contract. | Reuse as an adversarial comparator; independently derive the SO(10) map |
| Did the common-heavy-threshold shortcut survive? | No. The exact common-threshold restricted domain was independently found empty in the strict Model-1 scope; unequal thresholds and global execution remained open. | Never assume equal heavy masses merely to simplify the SO(10) matching |
| Is the legacy low-energy interface useful? | Yes, as a method: direct lattice `W0/W1` row custody, scheme/unit/sign checks, exact massive-lepton treatment, coherent channel addition, and a prohibition on invented covariance were defined and reviewed. | Revalidate against current primary sources when the downstream stage is activated |
| Was the missing intermediate BNV one-loop kernel solved? | No. The last controlling review left kernel provenance undecided, the kernel open, and all matching/RG and physics results absent. | Do not import a legacy kernel or claim that the downstream chain already exists |

Controlling local-custody evidence includes:

- C02 pause: commit `dafe88872724f016f388f20f72c7f934243857a3`, `formal/tooling/scientific_compute/model1_installation_preparation/route_c02_background_baa_repair_20260910_v2/PAUSE_CHECKPOINT.md`;
- independently accepted weak-basis/operator-lift and sign control: freeze commit `a7ac8ddb2457ed4f44dca8ddab6aa6874dd610e3`, `formal/docs/release/STRICT_NONSUPERSYMMETRIC_SU5_MODEL_1_LOW_ENERGY_MATCHING_AND_HADRONIC_INPUT_CONTROLLED_EXECUTION_OPERATOR_LIFT_SIGN_AND_THRESHOLD_DOMAIN_AMENDMENT_INDEPENDENT_REVIEW_RESULT_20260809_v1.json`;
- empty exact-common-threshold control domain: freeze commit `a7ac8ddb2457ed4f44dca8ddab6aa6874dd610e3`, `formal/docs/release/STRICT_NONSUPERSYMMETRIC_SU5_MODEL_1_EXACT_COMMON_HEAVY_THRESHOLD_RESTRICTED_LOW_ENERGY_PIPELINE_QUALIFICATION_PACKET_INDEPENDENT_REVIEW_RESULT_20260809_v0.json`;
- final source-review boundary: freeze commit `a7ac8ddb2457ed4f44dca8ddab6aa6874dd610e3`, `formal/docs/release/STRICT_MODEL1_KERNEL_SOURCE_COMPREHENSIVE_SCIENTIFIC_REVIEW_SOURCE_SPECIFIC_DISPOSITION_TOTALITY_AND_FULL_SCOPE_LIMITATION_MATERIALITY_AMENDMENT_INDEPENDENT_REVIEW_RESULT_20260816_v4.json`.

All paths are documentary provenance into local custody. They are not runtime dependencies.

## Legacy independence

The preserved strict SU(5)/Route-C result remains an unfinished benchmark checkpoint, not a default source theory. Its relevance audit identifies methods and bounded controls worth reproducing independently, but it does not supply an SO(10) premise, executable kernel, or accepted lifetime pipeline. It did not determine the winner and is not reactivated. No legacy source, environment, model tree, or result has been copied into this decision.

## Canonical sources

- H. Georgi and S. L. Glashow, *Unity of All Elementary-Particle Forces*, [Phys. Rev. Lett. 32, 438](https://doi.org/10.1103/PhysRevLett.32.438).
- J. C. Pati and A. Salam, *Lepton Number as the Fourth Color*, [Phys. Rev. D 10, 275](https://doi.org/10.1103/PhysRevD.10.275).
- H. Fritzsch and P. Minkowski, *Unified Interactions of Leptons and Hadrons*, [Annals of Physics 93, 193](https://doi.org/10.1016/0003-4916(75)90211-0).
- F. Gürsey, P. Ramond, and P. Sikivie, *A Universal Gauge Theory Model Based on E6*, [Physics Letters B 60, 177](https://doi.org/10.1016/0370-2693(76)90417-2).

## State consequence

The comparison selected one working source candidate and initially left the seam inactive. The subsequent admission decision in [BABU_KHAN_SO10_BNV_MATCHING.md](BABU_KHAN_SO10_BNV_MATCHING.md) activates one corrected, model-specific relation that retains the Pati-Salam intermediate stage. It does not broaden the source theory's authority.
