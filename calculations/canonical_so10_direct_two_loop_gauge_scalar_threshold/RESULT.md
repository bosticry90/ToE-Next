# Direct two-loop gauge/scalar finite threshold: execution result

## Disposition

The requested finite coefficient was **not** computed:

\[
\boxed{\texttt{DIRECT\_TWO\_LOOP\_GAUGE\_SCALAR\_THRESHOLD\_BLOCKED}}.
\]

The benchmark therefore remains

\[
\boxed{\texttt{DIRECT\_GAUGE\_MATCHING\_UNRESOLVED}}.
\]

The earlier `DIRECT_ONE_LOOP_KERNEL_PASS`,
`DIRECT_SM_TWO_LOOP_RUNNING_PASS`, exact two-loop RG logarithmic kernel, and
`YUKAWA_CONVENTION_V1` are preserved.  `BFB_UNRESOLVED` is carried unchanged.
No flavor fit, proton-decay calculation, PS resummation, benchmark replacement,
or gauge refit with an invented threshold was performed.

## What this execution added

The parent action previously supplied invariant values and exact Hessian
bilinears, but not cubic and quartic fluctuation vertices in a reusable API.
[`compile_scalar_vertices.py`](compile_scalar_vertices.py) now differentiates
every one of the 29 parent monomials exactly along arbitrary supplied tensor
directions through fourth order.

The exact regression suite earns

\[
\boxed{\texttt{SCALAR\_VERTEX\_ORACLE\_PASS}}.
\]

It reproduces four independent second-derivative controls from the certified
Hessian oracle, is permutation symmetric at third and fourth order, and gives

\[
I_{\eta}^{(4)}=384,\qquad
I_{z_6}^{(3)}=2,\qquad
I_{z_K}^{(3)}=6,\qquad
I_{\lambda_S}^{(4)}=24
\]

for the selected exact directions.  The `z_K` cubic is the expected expansion
of `Phi phi phi S*` about the nonzero `54_H` VEV.  The fifth derivative vanishes
exactly.  These numbers validate the derivative front end; they are not loop
amplitudes or threshold coefficients.

The comparison with the required centered finite vector was also frozen
*before* any result exists.  Its target has norm `420.0036982` and unit vector

\[
(0.2814581,-0.8044956,0.5230375).
\]

A future result must report magnitude ratio, cosine alignment, beneficial
projection, and—most importantly—the full convention-consistent gauge refit.
The preregistration is in [`comparison_gate.json`](comparison_gate.json).

## Why the finite result remains blocked

An exact scalar-potential derivative oracle is only one input to the requested
calculation.  The audit found no model-specific implementation of:

- the complete 328-real-component physical vertex/eigenstate lift;
- the background/quantum gauge-fixed vector, Goldstone and ghost rules;
- two-loop diagram generation and symmetry factors;
- the required one-loop field, mass, gauge, VEV and tadpole counterterms;
- two-loop tensor/IBP reduction;
- a validated arbitrary-mass vacuum-master evaluator;
- the renormalized UV-minus-SM-EFT hard-region subtraction.

Consequently gauge-parameter cancellation, the finite degenerate-mass limits,
and the exact finite constant cannot yet be tested.  RG consistency fixes the
`L^2` and `L` terms but cannot fix the finite nonuniversal vector.

There is a further scope distinction worth preserving.  A complete
**Yukawa-vertex-independent** two-loop boundary can contain gauge interactions
with light fermions as well as purely vector/scalar diagrams.  The label
`C1_GS` denotes the requested gauge/scalar subset; it must not silently be
promoted to the entire Yukawa-independent boundary unless those mixed
gauge--fermion graphs are dispositioned in the common UV/EFT subtraction.

## Master-integral authority

The required zero-momentum amplitudes can ultimately be organized with
one-loop tadpoles/products and general two-loop massive vacuum sunsets plus
mass derivatives.  Davydychev and Tausk give general tensor-reduction methods
for massive two-loop vacuum diagrams
([arXiv:hep-ph/9504432](https://arxiv.org/abs/hep-ph/9504432)); TSIL provides a
well-documented numerical basis for dimensionally regulated two-loop
self-energy integrals with arbitrary masses
([arXiv:hep-ph/0501132](https://arxiv.org/abs/hep-ph/0501132)).  Neither is a
drop-in calculation of this threshold, and neither is currently integrated.
The exact requirements are frozen in
[`MASTER_BASIS_CONTRACT.md`](MASTER_BASIS_CONTRACT.md).

This reproduces the methodological boundary already visible in Martens's
primary two-loop GUT matching calculation
([arXiv:1011.2927](https://arxiv.org/abs/1011.2927)): finite matching requires
the full renormalized diagram/counterterm construction, including tadpoles and
gauge fixing.  Its restricted finite formula is still inapplicable to this
multi-VEV, trilinear, mixed and nondegenerate benchmark.

## Authority gained and not gained

Earned in this gate:

1. exact on-demand scalar potential vertices through fourth order;
2. exact regressions against the parent Hessian and known mixing structures;
3. a preregistered `C1_GS` direction/magnitude comparison;
4. a machine-readable, fail-fast compiler-layer audit.

Not earned:

1. any two-loop diagram amplitude;
2. any finite `C1_i^{GS}` value;
3. any comparison or alignment with the required vector;
4. a gauge-coupling refit;
5. a benchmark gauge pass or failure.

The requested target remains scientifically well-defined, but completing it
requires a dedicated two-loop QFT compiler rather than another algebraic
extension of the scalar Hessian machinery.

## Reproduction

```powershell
python calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/compile_scalar_vertices.py
python calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/preregister_comparison.py
python calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/audit_compiler_readiness.py
python calculations/canonical_so10_direct_two_loop_heavy_threshold/analyze_boundary.py
python calculations/canonical_so10_direct_two_loop_heavy_threshold/independent_replay.py
```

Machine-readable outputs are
[`scalar_vertex_oracle.json`](scalar_vertex_oracle.json),
[`comparison_gate.json`](comparison_gate.json), and
[`compiler_readiness.json`](compiler_readiness.json).

