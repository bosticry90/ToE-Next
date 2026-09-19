# Scientific Dependency Scaffold

## Purpose

This document is the first dependency map for ToE-Next. It organizes what a candidate unification must connect without choosing a candidate, inventing a mechanism, or beginning a calculation.

The scaffold is:

```text
empirical obligations
    -> established descriptions
    -> candidate unifications
    -> recovery maps
    -> operational observables
    -> verification
    -> assumption compression
```

The arrows are claims, not repository directories. A named theory or tool occupies only the role for which evidence supports it.

## Authority layers

| Layer | Question | Required content | Authority limit |
|---|---|---|---|
| Empirical obligation | What must a viable account reproduce? | Named observation, dataset or evaluated result; uncertainty; domain | Establishes a target, not an explanation |
| Established description | What currently predicts the target? | Theory, regime, approximations, parameters and known limits | Valid only in its tested or justified domain |
| Candidate unification | What broader structure is proposed? | Fields or objects, symmetries, dynamics, parameters and assumptions | A working hypothesis until recovery and comparison succeed |
| Recovery map | How does the candidate yield the established description? | Explicit limit, reduction, matching, emergence relation or theorem | Establishes only the mapped relation and its conditions |
| Operational observable | How does the description reach a measurement? | Quantity, computation, instrument/likelihood model and uncertainties | Does not outrun the measurement or statistical model |
| Verification | Why trust the derivation and computation? | Known limits, independent replay, adversarial tests and numerical controls | Raises confidence; does not create physical evidence |
| Assumption compression | What explanatory burden changed? | Before/after assumption ledger, degeneracies and new commitments | Compression is valuable only if recovery and evidence survive |

## Initial domain map

This map is deliberately coarse. It identifies interfaces that mature infrastructure can service and the assumptions that remain independent; it does not declare active seams.

| Empirical obligation class | Established description to recover | Mature route to observables/evidence | Examples of remaining independent assumptions |
|---|---|---|---|
| Particle spectrum, charges, lifetimes, couplings, and precision observables | Standard Model quantum field theory in its tested domain | PDG/HEPData; FeynRules/UFO; WCxf, `wilson`, `flavio`; claim-specific likelihoods | Gauge group, representations, three generations, parameter values, flavor/Yukawa structure, Higgs-sector choices |
| Collider rates, distributions, and exclusions | Perturbative QFT with factorization and controlled effective descriptions | MadGraph5_aMC@NLO, LHAPDF, Rivet, HEPData, pyhf, Contur | Candidate Lagrangian, truncation/order, PDFs, shower/hadronization and detector/statistical assumptions |
| Macroscopic and radiative gravitation in tested regimes | General relativity and its controlled low-energy/effective limits | Cadabra or xAct for derivations; observation-specific pipelines for comparison | Spacetime/dynamical assumptions, matter coupling, boundary conditions, quantum/UV completion |
| Expansion history, CMB, large-scale structure, lensing, and abundance constraints | Relativistic cosmology plus specified matter content and perturbation theory | CLASS or CAMB for supported observables; Cobaya or claim-specific likelihoods for inference | Dark-sector identity, inflationary or alternative early-universe mechanism, initial conditions, priors and systematics |
| Thermodynamic consistency, equilibrium limits, entropy and statistical behavior | Thermodynamics, statistical mechanics and quantum statistical mechanics in their domains | Analytic derivation plus calculation-specific numerical tools and empirical comparators | Microstate ontology, coarse graining, initial/boundary data and emergence assumptions |
| Quantum coherence, probabilities and measurement statistics | Quantum theory/QFT operational predictions | Domain-specific experiment records and statistical models | Interpretation is not promoted into an empirical fact; any proposed deeper dynamics must reproduce observed statistics |

Observed phenomena and successful effective descriptions are obligations. Unsettled mechanisms in the final column are not silently promoted into the baseline.

## Candidate-unification admission contract

Before a candidate may occupy the scaffold, it must declare:

1. its scientific source and relationship to prior work;
2. mathematical objects, symmetries, action or dynamics, and domains of definition;
3. independent assumptions and free parameters;
4. the established descriptions it claims to recover;
5. the explicit form expected of each recovery map;
6. the observables by which it can be compared or falsified;
7. known pathologies, unresolved consistency conditions, and authority ceiling;
8. which parts are established physics, reused framework, inference, or new hypothesis.

A candidate is not admitted merely because it is mathematically interesting, broad in scope, or generated by AI.

## Recovery-map contract

Every proposed arrow from a candidate to established physics must freeze:

- source theory and destination theory;
- parameter regime, scales, state/background, boundary conditions, and approximation order;
- field, variable, basis, unit, and convention map;
- derivation or computational transformation;
- error terms and a declared domain of validity;
- recovery targets and acceptance tolerances;
- failure interpretation and authority ceiling;
- provenance for every inherited formula, implementation, dataset, and comparator.

Where a maintained interface such as UFO or WCxf covers part of the arrow, ToE-Next should use it and document the remaining scientific relation. Data serialization is not itself a recovery proof.

## Observable and evidence contract

An observable path must remain traceable:

```text
candidate assumptions
    -> recovery or matching relation
    -> prediction engine
    -> operational observable
    -> likelihood or comparison rule
    -> identified empirical record
```

Each step must state approximations and uncertainties. Numerical work must address convergence, discretization or truncation error, conditioning, precision sensitivity, and uncertainty propagation when applicable. Tool output without this chain is exploratory evidence at most.

## Verification contract

Verification is claim-scaled:

- exploratory claims use one competent engine plus dimensional, symmetry, limiting-case, and numerical sanity checks;
- consequential mathematical results add a genuinely independent replay and an adversarial attempt to find counterexamples or hidden assumptions;
- major scientific claims add independent reproduction, known-limit recovery, literature comparison, physical-assumption audit, and a calculation-appropriate uncertainty analysis;
- formal proof is reserved for bounded decisive statements whose exact formalization improves the claim.

Multiple tools sharing the same formula, code path, data, or convention do not constitute independent verification.

## Assumption-compression test

The central comparison is not novelty or file count. For each candidate, compare:

```text
independent assumptions required by recovered baseline descriptions
    versus
independent assumptions required by the candidate plus its recovery maps
```

Record whether an apparent reduction is genuine, merely relocates assumptions into boundary conditions or parameters, or trades them for unverified dynamics. A candidate that compresses assumptions but fails an empirical obligation does not advance the scaffold.

## Candidate seam families

The initial map exposes relation classes that may later yield a precise seam:

| Relation class | Why it may matter | What is missing before activation |
|---|---|---|
| Unified or ultraviolet candidate -> SMEFT/WET coefficients | Connects broader particle structure to tested low-energy observables | A selected candidate, frozen matching regime, bases, scales and discriminating observable |
| Candidate particle model -> collider likelihood | Tests new states/interactions against preserved measurements | A frozen Lagrangian and parameter slice, perturbative order, event/analysis chain and stopping rule |
| Candidate gravitational dynamics -> GR limit -> tested observable | Requires any broader gravity proposal to recover successful GR predictions | A selected candidate, background/regime, explicit reduction and measurement target |
| Candidate cosmology -> effective parameters -> CMB/LSS/expansion observables | Separates mechanism claims from successful effective phenomenology | A selected mechanism, initial conditions, parameter map, dataset and likelihood |
| Cross-domain proposal -> shared assumption ledger | Tests whether one principle genuinely explains multiple sectors | A specific proposal and at least two independently recoverable domain maps |

The unified/ultraviolet-particle relation class has now produced one resolved seam and one bounded active successor. The other relation classes remain inactive. The [open-seam criteria](OPEN_SEAMS.md) remain controlling.

## Calculation-selection rule

A physics calculation is admitted only after a candidate relation can satisfy all of the following:

1. both endpoints and their authority are explicit;
2. the missing relation is narrower than a field-wide open problem;
3. a result can discriminate, constrain, recover, or falsify something consequential;
4. mature infrastructure can supply the domain calculation without needless reimplementation;
5. assumptions, known limits, numerical controls, stopping rule, and authority ceiling can be frozen in advance;
6. the dependency and storage surface is proportionate to the claim.

Until a relation passes these requirements, it does not enter the active state in [project_state.json](../project_state.json).

## Current boundary

The initial ecosystem audit and documentary scaffold are complete enough to evaluate candidate relations. [SEAM_SELECTION.md](SEAM_SELECTION.md) identifies the unified/UV particle candidate to SMEFT/WET class as the leading class. [SOURCE_THEORY_COMPARISON.md](SOURCE_THEORY_COMPARISON.md) selects one published SO(10) construction as a working candidate. [BABU_KHAN_SO10_BNV_MATCHING.md](BABU_KHAN_SO10_BNV_MATCHING.md) admitted one model-specific seam, and its [first calculation](../calculations/bk_so10_bnv_matching/RESULT.md) resolved `PASS` at the tree-level operator-map ceiling. The direct SO(10)-to-SMEFT shorthand is corrected there: the model's Pati-Salam intermediate symmetry remains explicit, and unequal heavy-vector pole coefficients enter only as a symmetry-breaking threshold projection.

The [next admission record](BABU_KHAN_PS_RUNNING_AND_MI_MATCHING.md) finds that published work already supplies the unique Pati-Salam operator, gauge-leading-log anomalous exponents, and a simplified tree-level Standard Model projection. Its [calculation](../calculations/bk_ps_bnv_running_mi_matching/RESULT.md) resolved `PASS`: the Babu-Khan beta ledger, analytic gauge-running factor, full flavor structure, right-handed-neutrino retention, and post-running `M_I` projector agree in independent exact replays. The later [`H_T` threshold audit](BABU_KHAN_HT_THRESHOLD_AUDIT.md) corrected the beta-ledger sextet's identity to intermediate `Sigma_1`; `H_T` remains a high-scale gauge-threshold field. No running below `M_I` or phenomenology has been performed.
