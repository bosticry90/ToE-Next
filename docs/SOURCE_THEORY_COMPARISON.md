# Source-Theory Comparison

## Decision

```text
SOURCE CANDIDATE SELECTED FOR SEAM EVALUATION:
    Babu-Khan 2015 non-supersymmetric SO(10)
    Higgs content: 54_H + 126_H + 10_H
    Breaking route: Pati-Salam with discrete parity as the intermediate stage

AUTHORITY: WORKING_CANDIDATE_NOT_ACCEPTED
ACTIVE SEAM: NONE
ACTIVE PHYSICS CALCULATION: NONE

CANDIDATE RELATION:
    heavy-vector SO(10) sector
        -> dimension-six baryon-number-violating SMEFT coefficients
        -> LEFT/chiral matching and running
        -> nucleon-decay observables
```

This selects at most one source theory for evaluating whether a precise seam can be activated. It does not accept SO(10), this model, its symmetry-breaking history, or any predicted lifetime as established physics. It authorizes no calculation or tool installation.

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

Destination endpoint:

- a named dimension-six baryon-number-violating SMEFT basis at a specified matching scale;
- subsequent running and matching into a named low-energy/chiral basis;
- a defined set of nucleon-decay partial widths with stated hadronic matrix elements and experimental comparators.

The proposed scientific arrow is:

```text
frozen SO(10) heavy-vector interactions
    -> tree-level baryon-number-violating SMEFT coefficients
    -> controlled running and low-energy/chiral matching
    -> selected proton or neutron decay widths
    -> comparison with identified experimental limits
```

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

Until these are frozen in a calculation record, the relation remains a candidate and is not added to `active_seams`.

## Cheap falsifier and stopping rule

The cheapest decisive attack is ordered to fail early:

1. re-evaluate threshold-aware gauge-coupling and intermediate-scale consistency using current inputs and the paper's stated model assumptions;
2. derive the heavy-vector baryon-number-violating coefficient pattern in a declared SMEFT basis and test symmetry, normalization, and flavor consistency;
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

If activated, the relation should use claim-scaled verification:

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

## Legacy independence

The preserved strict SU(5)/Route-C result remains an unfinished benchmark checkpoint, not a default source theory. It informed the comparison by exposing representation and exact-equivalence burdens; it did not determine the winner and is not reactivated. No legacy source, environment, model tree, or result has been copied into this decision.

## Canonical sources

- H. Georgi and S. L. Glashow, *Unity of All Elementary-Particle Forces*, [Phys. Rev. Lett. 32, 438](https://doi.org/10.1103/PhysRevLett.32.438).
- J. C. Pati and A. Salam, *Lepton Number as the Fourth Color*, [Phys. Rev. D 10, 275](https://doi.org/10.1103/PhysRevD.10.275).
- H. Fritzsch and P. Minkowski, *Unified Interactions of Leptons and Hadrons*, [Annals of Physics 93, 193](https://doi.org/10.1016/0003-4916(75)90211-0).
- F. Gürsey, P. Ramond, and P. Sikivie, *A Universal Gauge Theory Model Based on E6*, [Physics Letters B 60, 177](https://doi.org/10.1016/0370-2693(76)90417-2).

## State consequence

The comparison selects one working source candidate and one candidate relation for seam evaluation. It deliberately leaves:

```text
active_physics_calculation = null
active_seams = []
active_focus = null
```

The next scientific decision is whether the inputs above can be frozen into a bounded calculation record with a meaningful cheap falsifier. Only that review may activate a seam.
