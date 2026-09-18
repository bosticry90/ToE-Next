# First Seam-Selection Brief

## Decision

```text
ACTIVE SEAM: NONE
OUTCOME: NONE_CURRENTLY_ADMISSIBLE
LEADING RELATION CLASS:
    unified or ultraviolet particle candidate -> SMEFT/WET coefficients
```

No physics calculation is authorized by this decision. The leading relation class is the best place to seek a concrete candidate relation; it is not itself an active seam and it does not select a unified theory.

## Question

Which of the five relation classes in the [scientific dependency scaffold](DEPENDENCY_SCAFFOLD.md) presently contains one relation precise enough, important enough, and economical enough to activate under the [open-seam admission requirements](OPEN_SEAMS.md)?

The admissible answer set includes `NONE`. A broad class cannot pass by importance alone: it needs a named candidate, mature endpoints, an explicit missing arrow, a falsifier or acceptance condition, frozen assumptions, a stopping rule, and a bounded scientific interpretation.

## Comparison method

The comparison uses eight criteria:

1. **ToE leverage** — potential to connect major sectors or reduce major independent assumptions;
2. **endpoint maturity** — whether both sides of the proposed arrow are defined well enough to specify recovery;
3. **discriminating power** — ability to rule out, force, or materially narrow candidate structure;
4. **cheap falsifier** — availability of a decisive attack before large implementation;
5. **existing infrastructure** — fraction of downstream computation already covered by mature tools;
6. **legacy leverage** — usable prior results or failure boundaries without silently reactivating historical programs;
7. **initial cost** — expected dependency, storage, and computational burden of the first decisive test;
8. **authority ceiling** — what a successful first result could actually establish.

Ratings are comparative scientific judgments, not measured scores. A strong rating cannot compensate for a failed seam-admission requirement.

## Relation-class comparison

| Relation class | ToE leverage | Endpoint maturity | Discrimination / cheap falsifier | Infrastructure | Legacy leverage | Initial cost | Authority ceiling | Admissible now? |
|---|---|---|---|---|---|---|---|---|
| Unified or UV particle candidate -> SMEFT/WET | High | Destination high; source absent | Potentially high / medium-high | High | High but bounded by an unfinished SU(5) checkpoint | Low to moderate after a candidate is frozen | A controlled matching result could materially constrain particle unification | **No** — no selected source theory, Lagrangian, matching regime, basis, scale, or observable |
| Particle candidate -> collider likelihood | Medium for unification; high for phenomenology | Likelihood endpoint high; source absent | High / high | Very high | Low | Moderate after a model is frozen | Strong bounded exclusion or support for a parameter region | **No** — no candidate model; this is normally downstream of a broader particle-theory relation |
| Candidate gravity -> GR limit -> tested observable | High | GR endpoint high; source absent | Potentially high / low until a candidate is specified | Medium; symbolic support is strong but observation paths are claim-specific | High but negative or unresolved | Potentially high | A controlled recovery or failure could bear directly on gravitational unification | **No** — no selected action, field content, background, limiting procedure, or measurement target |
| Candidate cosmology -> effective cosmology -> observations | Medium to high | Effective/observational endpoint high; mechanism absent | High / medium | High | Medium; the preserved vacuum-energy result supplies an obstruction, not a candidate | Moderate to high | A bounded mechanism-to-observable map could constrain fundamental cosmology | **No** — no selected mechanism, initial conditions, parameter map, dataset, or likelihood |
| Cross-domain proposal -> shared assumption ledger | Potentially highest | Low; no concrete proposal or two recovery maps | Unknown / low | Fragmented across domains | Mostly cautionary; CCFT is closed in its tested historical corpus | High | Genuine multi-sector recovery could provide the strongest assumption compression | **No** — no concrete cross-domain structure and no pair of independently testable recovery maps |

## Why the leading class is particle unification to EFT

The unified/UV particle to SMEFT/WET class has the best present balance, even though it does not yet pass admission:

- the destination theories, coefficient representations, running/matching interfaces, and many observable routes are mature;
- a first matching calculation can be bounded to a small operator sector, scale interval, or symmetry-breaking assumption;
- exact algebra, symbolic checks, constraint solvers, and independent replay are already available on C:;
- low-energy or collider data can provide relatively cheap falsifiers;
- a controlled map can reveal whether a claimed unification genuinely reduces matter-sector assumptions or merely moves them into heavy spectra, thresholds, flavor choices, and boundary conditions.

The class outranks direct collider work because it can address the physical arrow from a broader structure into the low-energy description. Collider likelihoods remain a downstream test once such an arrow and candidate exist. It outranks the gravity, cosmology, and cross-domain classes at this moment because those classes lack both a selected source theory and a comparably cheap first falsifier.

This priority is conditional. Evidence for a more mature, better-falsifiable candidate in another class may replace it.

## Why the legacy SU(5) checkpoint is not the source endpoint

The local-custody receipt records a strict Model-1 SU(5)/Route-C C02 benchmark that is paused and unadjudicated: Route C is `2/4`, strict exact equivalence is `1/4`, production is `76/1188`, and the receipt explicitly provides no scientific promotion or automatic continuation.

That record is valuable legacy leverage and a warning against recomputation. It is not an accepted Lagrangian-to-SMEFT recovery map, a completed physical model, or authority to resume the historical benchmark. Selecting it automatically would substitute repository continuity for scientific candidate selection.

The gravity, QGT, and vacuum-energy receipts impose similar boundaries: they provide reference controls, known obstructions, or paused results, not ready source theories. CCFT/UEFM remains closed as a ToE in its tested historical corpus.

## Failed admission tests

Every relation class presently fails at least these controlling tests:

1. **Selected source:** no precise candidate theory or mechanism has been admitted under the candidate-unification contract.
2. **Frozen arrow:** no source-to-destination recovery relation has fixed its regime, conventions, approximation order, and error terms.
3. **Bounded decision:** no acceptance threshold and failure interpretation jointly distinguish a scientific outcome from exploratory output.

Activating a seam despite these failures would recreate hypothesis-first work under a new label.

## Conditions for activation in the leading class

The unified/UV particle to SMEFT/WET class may become active only when a candidate proposal supplies all of the following:

1. an attributed, version-frozen action or Lagrangian with field content and symmetries;
2. a specified symmetry-breaking and heavy-field spectrum relevant to the proposed matching;
3. a named SMEFT or WET basis, matching scale, perturbative order, and convention map;
4. one narrow operator sector or coefficient relation whose derivation is missing or disputed;
5. at least one low-energy or collider observable capable of discriminating the result;
6. a cheap pre-computation falsifier, such as an inconsistency, forbidden operator pattern, failed limit, anomaly, or impossible parameter relation;
7. an assumption ledger that exposes thresholds, boundary conditions, flavor choices, and new parameters rather than hiding them as unification;
8. a calculation record with a stopping rule, independent-replay decision, and authority ceiling.

Meeting these conditions authorizes a proposal for seam activation; it does not prejudge the proposal's success.

## Next scientific boundary

The next work is candidate admission within the leading relation class: compare serious, explicitly specified unified or ultraviolet particle constructions for one narrow matching relation that satisfies the activation conditions above. That comparison should prefer a candidate with an accessible cheap falsifier and a maintained path into established EFT or observable infrastructure.

Until such a candidate is identified, [project_state.json](../project_state.json) correctly retains:

```text
active_physics_calculation = null
active_seams = []
```
