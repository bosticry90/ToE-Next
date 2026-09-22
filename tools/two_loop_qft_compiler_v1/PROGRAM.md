# TWO_LOOP_QFT_COMPILER_V1

## Frozen scientific target

The sole target is the finite, centered, benchmark-specific two-loop
gauge/scalar matching vector `C1_GS` already preregistered in
`calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold`.

The program may not change the canonical action, benchmark, matching scheme,
target vector, or lower-order results.  It may not begin flavor, proton decay,
PS resummation, benchmark replacement, or gravity work.

## Promotion ladder

1. exact 328-real component basis and normalized 45-generator basis;
2. complete physical scalar/Goldstone basis and parent-to-mass rotation;
3. background-field `R_xi` gauge, ghost action and complete vertices;
4. independently replayable two-loop diagram/symmetry-factor generator;
5. one-loop field, mass, gauge, VEV, gauge-parameter and tadpole counterterms;
6. tensor/IBP reduction to the frozen massive-vacuum master contract;
7. two independently validated arbitrary-mass master evaluators;
8. renormalized UV-minus-SM-EFT hard-region assembly;
9. exact reproduction of the known `L^2` and `L` coefficients;
10. exposure of finite `C1_GS`, preregistered comparison, and gauge refit.

Every layer must reproduce a lower-complexity result before promotion.  No
finite threshold may be inferred from RG logarithms, scale variation, diagram
counts, or incomplete topology subsets.

## Current phase

Promotion layers 1, 2 and 3 pass. Layer 3 now supplies one authoritative
partially fixed background-field action, including the equivariant heavy-ghost
sector, and a sparse physical-vertex facade derived from it. Its exact
UV-minus-SM-EFT one-loop `F^2` assembly passes all 12 preregistered
cluster/`xi` cells and all five aggregate checks. An implementation-independent
replay has zero symbolic residual.

The partial-BFM action SHA-256 is
`2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491` and
the one-loop result SHA-256 is
`98d1179a02e7dc954aee49467a43e0aa6e8457b6165f04476df6a2629d3405e4`.
Promotion layer 4 was authorized and has now completed. Its model-independent
topology subgate passes: two one-loop and nine two-loop 1PI background
two-point topologies are independently reproduced, with 21 future counterterm
slots. A 168-signature index-summed vertex catalog generates 1,896 canonical
gauge/scalar species records and reproduces the complete layer-3 one-loop
inventory.

The full layer now passes as `TWO_LOOP_DIAGRAM_GENERATOR_PASS`. The four base
graphs containing the equivariant quartic heavy-ghost vertex are differentiated
into direct/exchange ordered Grassmann channels, giving 1,900 final records.
An independent recursive enumerator reproduces the complete set and every
symmetry denominator, while five field-colored control theories pass. Layer 5
was therefore authorized. See [`LAYER4_RESULT.md`](LAYER4_RESULT.md).

The first layer-5 execution derives the complete bare-action counterterm
structure for all 29 parent monomial families, populates the structural
dispatch expression for every one of the 21 preregistered insertion slots,
fixes a single FJ-like tadpole/VEV convention, and independently replays the
bare-action expansion. The earned parent `b10=-34/3` coefficient also fixes
the gauge/background-field counterterm and its Ward identity. Promotion is
nevertheless blocked because the one-loop scalar, quantum-vector, ghost,
gauge-parameter, VEV, and tadpole UV-pole residues have not been calculated.
The disposition is `ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED`; layer 6 remains
locked. See [`LAYER5_RESULT.md`](LAYER5_RESULT.md). No amplitude, finite
`C1_GS`, gauge refit, or new physics verdict is inferred.

The missing layer-5A kernel is now preregistered in
[`LAYER5A_UV_POLE_EVALUATOR_TASK.md`](LAYER5A_UV_POLE_EVALUATOR_TASK.md) and
[`one_loop_uv_pole_evaluator_contract.json`](one_loop_uv_pole_evaluator_contract.json).
Contract v2 freezes 13 primitive UV-algebra tests, 13 control-theory tests,
and 13 canonical-model tests, together with explicit UV/IR-separation,
independent-replay, operator-projection, and fail-closed rules. It adds a
direct rank-eight primitive and requires the replay to reconstruct the
one-loop diagram inventory independently or supply an inventory-independent
functional completeness proof. Its SHA-256 is
`6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92`,
superseding v1 hash
`f4cf741afed95657b8c8c80ff178147189f35c7db42a8fdcea95e8ed3ae3f588`.
This is specification authority only: zero of the 39 tests has run and the
counterterm/compiler outcome remains blocked. The fail-fast partition is 27
tests for the evaluator engine and 12 for canonical counterterm completion.

The first execution order and result ledger are now frozen without amending
contract v2. The exact engine order is `P01--P13`, `C01--C13`, then `M01`,
with advancement only on `PASS`. The execution-plan SHA-256 is
`54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101` and
the result-schema SHA-256 is
`5999c0a7ff7d2458b0c204a7f8313c0d39a6473aaeff7282ac1f1f1034f699b8`.
The ledger was initialized at `0/39` (`0/27` in the engine gate), while a
synthetic schema-only replay proves that the format can represent the exact
`27/27` checkpoint without promoting the counterterm compiler or Layer 6.
See [`LAYER5A_EXECUTION_ORDER.md`](LAYER5A_EXECUTION_ORDER.md).

The first authorized test has now executed. `UVP_P01` passes with the exact
massive tadpole residue `-m2` in units of
`1/(16*pi^2*epsilon_bar)`. The primary auxiliary-mass UV projection and the
independent Wick-rotated Gamma-function replay agree with zero symbolic
residual, and the positive-mass primitive has no IR pole. Progress is `1/39`
(`1/27` in the engine gate); `UVP_P02` is next. The counterterm compiler and
Layer 6 remain blocked. See [`UVP_P01_RESULT.md`](UVP_P01_RESULT.md).

The second primitive has also executed. `UVP_P02` passes with the exact
mass-independent logarithmic-bubble residue `+1` in units of
`1/(16*pi^2*epsilon_bar)`. The primary radial large-loop-momentum projector
and an independent Wick-rotated Gamma-function replay agree exactly, and both
give a zero derivative with respect to `m2`; no finite mass dependence enters
the UV pole. Progress is `2/39` (`2/27` in the engine gate), and `UVP_P03` is
the sole next authorized test. See [`UVP_P02_RESULT.md`](UVP_P02_RESULT.md).

The third primitive closes the first internal consistency triangle. `UVP_P03`
passes: a direct doubled-line auxiliary-mass projection, an independent
general-`alpha` Gamma-function replay, and minus the mass derivative of the
verified frozen P01 pole all give normalized residue `+1`. The three pairwise
residuals and the integrand sign-identity residual are exactly zero. Progress
is `3/39` (`3/27` in the engine gate); `UVP_P04` alone is next. See
[`UVP_P03_RESULT.md`](UVP_P03_RESULT.md).

The fourth primitive is the first tensor-algebra gate. `UVP_P04` passes for
`Integral_E[k_mu*k_nu/(k^2+m2)^2]`: exact reduction with
`delta_mu_nu/d`, followed by Laurent expansion, gives normalized tensor
coefficient `-m2/2`. An independent Schwinger-parameter Gaussian-source replay
agrees exactly and both contractions return the scalar integral with zero
residual. A quarantined `d=4` shortcut leaves the pole unchanged but misses a
finite `-m2/4` term in `1/(16*pi^2)` units, proving why the promoted route
retains `d=4-2*epsilon`. Progress is `4/39` (`4/27`); `UVP_P05` alone is next.
See [`UVP_P04_RESULT.md`](UVP_P04_RESULT.md).

The exact closure task and its 12-cell/5-aggregate-test preregistration are
frozen in [`LAYER3_CLOSURE_TASK.md`](LAYER3_CLOSURE_TASK.md) and
[`one_loop_xi_cancellation_matrix.json`](one_loop_xi_cancellation_matrix.json).
The matrix canonical SHA-256 is
`46b3bc390967eb256a83f4bb5b20bc46cd7f11f788f59a0ce047e48669294d96`.
The criteria were executed without alteration. The authoritative outcome and
reproduction commands are recorded in [`RESULT.md`](RESULT.md).
