# TWO_LOOP_QFT_COMPILER_V1 layer 5A: one-loop UV-pole evaluator (contract v2)

This document freezes the next compiler task and its minimum control suite.
It is a specification, not an evaluator result.  The machine-readable
authority is
[`one_loop_uv_pole_evaluator_contract.json`](one_loop_uv_pole_evaluator_contract.json),
whose canonical SHA-256 is

```text
6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92
```

Contract v2 transparently supersedes v1 hash
`f4cf741afed95657b8c8c80ff178147189f35c7db42a8fdcea95e8ed3ae3f588`.
It changes no earned result.  It adds one explicit rank-eight tensor primitive,
requires replay-level diagram completeness rather than only independent
algebra, and freezes a 27-test evaluator gate followed by a 12-test canonical
counterterm gate.  The exact delta is recorded in
[`LAYER5A_CONTRACT_V2_AMENDMENT.md`](LAYER5A_CONTRACT_V2_AMENDMENT.md).

No test in the contract has been executed.  The compiler remains
`ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED`; layer 6 remains unauthorized.

## Exact task

> **Continue `TWO_LOOP_QFT_COMPILER_V1` within layer 5 only by implementing
> `ONE_LOOP_UV_POLE_EVALUATOR`.  Treat the hashes in
> `one_loop_uv_pole_evaluator_contract.json` as immutable.  Do not change the
> 21 counterterm slot structures, infer residues from future two-loop
> cancellations, or use the already-known beta coefficients as evaluator
> outputs.**
>
> **Implement a dimensional-regularization/`MSbar` projector for the local
> `1/epsilon_bar` part of renormalizable one-loop 1PI amplitudes.  Support
> scalar one- through four-point functions, scalar/vector/ghost two-point
> functions through the required external-momentum order, BRST-required
> three-point controls, arbitrary nondegenerate masses, massless limits, and
> tensor ranks through eight.  Perform tensor reduction in `d=4-2 epsilon`
> before expanding in epsilon.  Reject nonlocal pole outputs.**
>
> **Use an explicit UV/IR-separation protocol.  The primary path may use
> auxiliary-mass infrared rearrangement, but must include every induced local
> IR counterterm.  A scaleless integral may not be accepted as evidence of a
> zero UV pole: store UV and IR labels separately.  Cancel the auxiliary mass
> from promoted physical counterterms and replay massless cases at
> nonexceptional off-shell momenta or with an independently implemented
> Feynman-parameter/Gamma-function residue calculation.  Apply an `R*`
> subtraction whenever the rearrangement creates spurious IR
> subdivergences.**
>
> **Execute all 13 primitive algebra tests and all 13 control-theory tests in
> the frozen contract before applying the evaluator to the canonical model.
> Controls include real `phi4`, superrenormalizable real `phi3`, scalar QED,
> pure Yang--Mills/ghosts, Abelian Higgs, and a non-Abelian
> `SU(2)->U(1)` adjoint-Higgs partial-BFM system.  The evaluator must derive,
> rather than import, the expected gauge coefficients and must leave zero UV
> residual in the selected renormalized amplitudes.**
>
> **Only after those controls pass, execute the 13 canonical-model tests.
> Derive all four scalar wave-function residues, four quadratic directions,
> four real cubic directions, 26 real quartic directions, quantum-vector and
> heavy/light-ghost residues, `delta_xi`, three VEV shifts, and three tadpole
> residues.  Project the complete parent pole action onto all 34 real
> Hermitian directions represented by the 29 frozen monomial families.  A
> nonzero out-of-basis residual is a fail/block requiring adjudication, never
> permission to extend `PARENT_ACTION_V1` silently.  Derive `b10=-34/3`
> independently and check it only after evaluation.**
>
> **Perform an independent replay that imports neither the primary UV
> expansion/tensor reducer nor the primary one-loop diagram inventory.  It
> must either independently generate and canonicalize every relevant
> one-loop 1PI diagram, including field assignments, statistics signs and
> symmetry factors, or use a functional/effective-action method whose
> completeness is independent of the primary graph list.  It must cover all
> primitive residues, every promoted control-theory residue, and every
> canonical residue group.  Reuse of expected beta functions, or evaluating
> the same potentially incomplete graph list twice, is not an independent
> replay.**
>
> **Return `ONE_LOOP_UV_POLE_EVALUATOR_PASS` only when all primitive and
> control-theory tests pass and the evaluator independently reproduces the
> parent gauge pole.  Return `ONE_LOOP_COUNTERTERM_COMPILER_PASS` only after
> all canonical tests pass, the 18 missing residue groups are explicit, all
> 21 slots contain complete coefficients, radiative operator closure and
> independent replay pass, and selected renormalized amplitudes have zero
> UV pole.  Otherwise return the scoped `...BLOCKED` or `...FAIL`.  Do not
> begin layer 6, finite one-loop amplitudes, two-loop reduction, master
> integrals, `C1_GS`, gauge refitting, BFB, flavor, or proton-decay work.**

## Authority ceiling

The task may earn only the one-loop UV-pole evaluator and, if all model tests
also pass, completion of layer 5.  It may not evaluate any two-loop integral
or change a physics disposition.

The frozen conventions are:

- `d=4-2 epsilon`;
- `MSbar` and the `1/epsilon_bar` pole;
- the promoted partial-BFM/BRST action and physical basis;
- the layer-5 FJ-like explicit tadpole-shift prescription;
- `beta_g=b*g^3/(16*pi^2)`;
- `-F^2/4` for background gauge operators;
- exact or certified algebra for every promoted residue.

The partial-BFM architecture follows the already frozen comparison to
[Thomsen, *A Partially Fixed Background Field Gauge*](https://arxiv.org/abs/2404.11640).
The background Ward check uses the standard formulation in
[Abbott, *The Background Field Method Beyond One Loop*](https://cds.cern.ch/record/134260/files/198012137.pdf).
The UV/IR contract follows the logic of infrared rearrangement and `R*`, for
which [Chetyrkin et al., *The method of global R* and its applications*](https://arxiv.org/abs/1801.03024)
is a comparator.  These sources define methodology; they do not provide the
canonical model's residues.

## Fail-fast partition

The 39 frozen tests are split into two promotion decisions:

- **Layer 5A engine gate (27 tests):** `P01--P13`, `C01--C13`, and `M01`.
  A complete pass earns `ONE_LOOP_UV_POLE_EVALUATOR_PASS` while preserving
  `ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED`.
- **Layer 5B canonical counterterm gate (12 tests):** `M02--M13`.  A complete
  pass may earn `ONE_LOOP_COUNTERTERM_COMPILER_PASS`; layer 6 remains subject
  to its separate audit.

The second gate may not compensate for a failure in the first.

## Minimum primitive suite

The 13 primitive tests cover:

1. massive rank-zero tadpoles;
2. logarithmic bubbles;
3. doubled propagators/mass derivatives;
4. rank-two tensor reduction;
5. rank-four and rank-six tensor reduction;
6. local external-momentum expansion through the required orders;
7. unequal-mass bubble poles;
8. loop-routing invariance;
9. a `d`-dimensional total-derivative/IBP identity;
10. auxiliary-mass cancellation;
11. separately labelled UV and IR poles of a scaleless integral;
12. agreement of massless off-shell and auxiliary-mass UV residues.
13. an explicit rank-eight tensor vacuum integral, with all 105 metric
    pairings and denominator `d(d+2)(d+4)(d+6)` retained before the epsilon
    expansion.

The evaluator must preserve `d` until pole-times-epsilon contributions are
resolved.  A four-dimensional tensor average used before that point is a
failure.

## Minimum theory-control suite

The 13 theory tests are deliberately redundant:

- real `phi4`: two-point mass/field residues, four-point crossing residue,
  and renormalized pole cancellation;
- real `phi3`: one-point tadpole, two-point bubble, and UV-finite triangle;
- scalar QED: background `b=1/3`, transversality, scalar two-point/vertex Ward
  identity, and renormalized cancellation;
- pure Yang--Mills: background `b=-11 C_A/3`, separately retained ghost and
  vector pieces, plus quantum-vector/ghost/gauge-parameter ST controls;
- Abelian Higgs: broken-phase Goldstone/ghost mass and tadpole/VEV controls;
- `SU(2)` with one real adjoint scalar broken to `U(1)`: parent `b=-7`,
  equivariant partial-BFM vector/Goldstone/ghost/quartic-ghost controls, and an
  independent UV/IR extraction replay.

The scalar normalizations are frozen in the JSON contract.  In particular,
for `L=-lambda*phi^4/4!` and `d=4-2 epsilon`, the counterterm-pole coefficients
are half the familiar `d=4-epsilon` presentation: `delta_m2=lambda*m2/2` and
`delta_lambda=3*lambda^2/2` in units of
`1/(16*pi^2*epsilon_bar)`.

## Canonical-model acceptance matrix

The 13 model tests require:

1. independent recovery of `b10=-34/3`;
2. all four parent scalar wave-function residues;
3. four quadratic residues;
4. four real cubic residues;
5. 26 real quartic residues;
6. rank-34 projection with zero out-of-basis residual;
7. Hermiticity and PQ closure;
8. quantum-vector, heavy/light-ghost, and gauge-parameter residues;
9. three VEV and three tadpole residues in the frozen scheme;
10. all 33 Goldstone mass-counterterm identities;
11. zero residual poles in selected renormalized amplitudes;
12. complete coefficients for all 21 layer-5 slots;
13. an implementation-independent canonical replay.

The projection must distinguish the 29 monomial families from their 34 real
Hermitian coefficient directions.  Numerical least squares without an exact
or interval-certified rank and residual is not sufficient.

## Independent replay design

The replay must satisfy one of the two complete designs frozen in
[`INDEPENDENT_UV_REPLAY_DESIGN.md`](INDEPENDENT_UV_REPLAY_DESIGN.md):

- **Design A (diagrammatic):** reconstruct vertices from the frozen action,
  independently enumerate/canonicalize the one-loop 1PI graph sets per
  external process, and independently compute symmetry factors, Grassmann
  signs, and UV residues;
- **Design B (functional):** derive the pole action from a background-field
  effective-action or heat-kernel construction with an explicit completeness
  certificate mapping its operator traces to every required local operator.

A diagrammatic replay must publish per-process set hashes, both directed set
differences, symmetry/sign residuals, and an independent residue table.  A
functional replay must publish its completeness certificate, full operator
map, residue table, and comparison with the primary diagrammatic result.
Either design must cover all control and canonical scalar one- through
four-point, quantum-vector, ghost, and BRST-vertex processes.

## UV/IR fail-closed rules

- A scaleless integral is `UV+IR=0`, not `UV=0`.
- A massless limit is taken only after UV classification.
- An auxiliary mass must cancel from promoted counterterms.
- Any required local IR counterterm must be generated and provenance-linked.
- Nonlocal dependence in a UV counterterm is a failure.
- A residue inferred from a known beta function is a regression input, not an
  evaluator output.
- A disagreement between primary and independent UV extraction is a block
  until localized; it is not averaged away.

## Outcomes

`ONE_LOOP_UV_POLE_EVALUATOR_PASS` requires the 27-test engine gate: every
primitive and control-theory test plus independent derivation of the parent
gauge pole.

`ONE_LOOP_COUNTERTERM_COMPILER_PASS` additionally requires every canonical
test and complete population of the existing layer-5 contract.

A persistent wrong/nonlocal pole, BRST violation, or out-of-basis divergence
confirmed by complete independent replay is a `FAIL`.  Missing vertices,
IR subtractions, projectors, or replay coverage are `BLOCKED`.

## Required deliverables

1. immutable evaluator convention and version hash;
2. all primitive pole records with UV/IR labels;
3. all control-theory diagrams, residues, and cancellation reports;
4. independent replay artifacts;
5. complete canonical residue tables and projection certificate;
6. 33 Goldstone and BRST/background-Ward reports;
7. layer-5 slot file with complete derived coefficients;
8. a gate audit that preserves all downstream physics dispositions unless the
   full layer actually passes.
