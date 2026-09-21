# TWO_LOOP_QFT_COMPILER_V1 layer-3 closure task

This document freezes the next Codex task and the one-loop gauge-parameter
cancellation test matrix. It is a specification, not a completed background-
field action or loop calculation. The current outcome remains
`BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_BLOCKED`; two-loop diagram enumeration
is not authorized.

## Exact Codex task

> **Continue `TWO_LOOP_QFT_COMPILER_V1` only to close promotion layer 3. Treat the physical-basis SHA-256 `af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e`, quadratic-layer SHA-256 `b983a8d8dae078761d61c8492ddb583f984398e56483cd306e2382e68ea2e692`, `PARENT_ACTION_V1`, and the frozen positive-Higgs benchmark as immutable inputs. Derive one complete partially fixed background-field `R_xi` UV action and the corresponding SM EFT background-field action in the same dimensional-regularization/MSbar convention. Start from the canonical Yang--Mills and scalar kinetic terms, split every gauge field into background and quantum parts, define the BRST transformations and one gauge-fixing fermion, and derive—rather than manually append—the gauge-fixing, Goldstone, heavy/light ghost, background, quantum-vector, and scalar interaction vertices. Make this complete action the authority source beneath the existing sparse physical-vertex façade.**
>
> **Using only that action, calculate the renormalized one-loop UV-minus-EFT coefficient of the three unbroken-SM background `F_i^2` operators at `xi=1/2,1,2`. Preserve massive-vector, Goldstone, ghost, and EFT-subtraction terms separately through the pole, logarithmic, and finite parts. Execute every cell and aggregate check in `one_loop_xi_cancellation_matrix.json`. Require clusterwise—not merely total—cancellation of `xi`, recovery of `lambda_i^V=T_i[1-21 log(M_V/mu)]`, the vector beta jump `-7T_i/2`, matching-scale cancellation, the SM-neutral cluster zero, the degenerate-mass and Feynman-gauge heat-kernel limits, absence of an unmatched IR pole, background transversality, and selected one-loop Slavnov--Taylor identities derived from the same BRST action. Independently replay the action-to-vertex derivation and final matched coefficient.**
>
> **Return `BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS` only if all twelve cluster/xi cells and all aggregate tests pass. Return `BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_FAIL` only after a complete independent replay demonstrates persistent gauge-parameter dependence, a wrong beta jump, or a wrong finite coefficient. Otherwise retain `BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_BLOCKED` and name the first unimplemented or ambiguous action, subtraction, infrared, or identity layer. Do not enumerate any two-loop diagrams, construct two-loop counterterms, calculate `C1_GS`, refit gauge couplings, or begin flavor, proton-decay, PS-resummation, benchmark-replacement, or BFB work during this task.**

## Authority ceiling and frozen conventions

The task may earn only the complete layer-3 background-field/physical-vertex
authority. It may not infer a two-loop finite threshold or change any physics
status. The conventions are:

- dimensional regularization with `d=4-2 epsilon` and `MSbar` subtraction;
- GUT-normalized `U(1)_Y`, plus `SU(2)_L` and `SU(3)_c` backgrounds;
- `-F_i^{mu nu}F_{i,mu nu}/4` gauge-operator normalization;
- the existing direct-matching convention
  `alpha_low^-1=alpha_parent^-1-lambda_i/(12 pi)`;
- one partially fixed background-field `R_xi` action shared by UV, EFT
  subtraction, regressions, and future diagram generation;
- immutable field IDs and transformations from the passed physical basis.

The partially fixed construction in [Thomsen, *A Partially Fixed Background
Field Gauge*](https://arxiv.org/abs/2404.11640) is a formal comparator for the
action architecture, not authority for this benchmark's coefficients.

## Required action derivation

The implementation must materialize or generate on demand, from one action:

1. background and quantum SM gauge fields;
2. the 33 heavy quantum vectors in their four mass eigenspaces;
3. the 33 orbit-defined Goldstones;
4. heavy and unbroken/light ghosts with their background covariant operators;
5. all 290 heavy physical scalars, the PQ direction, and the retained Higgs;
6. gauge-fixing and FP interactions, including all background/quantum
   distinctions needed by the one-loop two-point function;
7. the SM EFT action and its subtraction in precisely the same convention.

The existing `physical_vertex_api.py` becomes a façade over this source. It
must not remain a second independently maintained gauge-interaction authority.
The passed scalar parent oracle remains the scalar-potential backend.

The action compiler must expose its BRST/gauge-fixing source, field ledger,
normalizations, and a stable content hash. It must replay the already-earned
quadratic and tree-level vertex checks before any loop result is evaluated.

## Preregistered one-loop test matrix

The machine-readable authority is
[`one_loop_xi_cancellation_matrix.json`](one_loop_xi_cancellation_matrix.json).
Its twelve primary cells are the Cartesian product of three gauge parameters
and four vector mass clusters:

| Cluster | `M_V^2/(g10^2 omega^2)` | real vectors | `(T1,T2,T3)` | `xi` |
|---|---:|---:|---:|---:|
| lower charged | `1/200` | 8 | `(14/5,0,1)` | `1/2,1,2` |
| lower neutral | `1/40` | 1 | `(0,0,0)` | `1/2,1,2` |
| upper A | `5/12` | 12 | `(5,3,2)` | `1/2,1,2` |
| upper B | `253/600` | 12 | `(1/5,3,2)` | `1/2,1,2` |

For every cell and every nonzero SM channel, store separately:

- vector, Goldstone, ghost, and EFT-subtraction contributions;
- UV-pole, logarithmic, and finite coefficients;
- their complete matched sum;
- the corresponding beta-jump and matching-scale-derivative replay;
- the selected BRST/Slavnov--Taylor residuals.

Individual pieces may depend on `xi`; the complete matched sum may not. The
primary criterion is exact symbolic cancellation. A minimum 50-decimal replay
with relative tolerance `1e-10` is the secondary certificate. A cancellation
visible only after summing different mass clusters is a failure of the
clusterwise gate.

## Expected results and aggregate checks

For each cluster `c`,

\[
\lambda_i^{(c)}=T_i^{(c)}
\left[1-21\log\left(\frac{M_c}{\mu}\right)\right],
\qquad
\Delta b_i^{(c)}=-\frac72 T_i^{(c)}.
\]

Thus

\[
\frac{d\lambda_i^{(c)}}{d\log\mu}
+6\Delta b_i^{(c)}=0.
\]

At `mu=M_c`, the finite cluster coefficient is `T_i^(c)`. The neutral cluster
must vanish in all SM channels. If all vector masses are made degenerate, the
result must reduce to the total index `(8,6,5)` multiplying the same universal
coefficient.

The aggregate calculation must also establish:

- cancellation of UV/EFT soft contributions and absence of an unmatched IR
  pole in the hard coefficient;
- transversality of each renormalized background two-point function;
- selected one-loop Slavnov--Taylor identities derived from the frozen BRST
  functional, with signs and tadpole terms taken from that functional rather
  than hard-coded;
- exact recovery of the independent `xi=1` heat-kernel result.

## Outcomes and stopping rule

`BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS` requires the complete action,
all twelve matrix cells, all aggregate tests, and an independent replay.

`BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_FAIL` requires a complete calculation
and replay that still produces a wrong pole/log/finite coefficient or
gauge-parameter dependence. An implementation error is a block, not a physics
failure.

`BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_BLOCKED` applies whenever a required
vertex class, EFT subtraction, UV/IR separation, counterterm needed already at
one loop, or loop-level identity remains absent or ambiguous. At any block or
failure, stop without authorizing layer 4.

## Required deliverables

1. the generated UV and SM-EFT gauge-fixed action manifests and hashes;
2. a once-only field/ghost/Goldstone ledger;
3. sparse derived vertex manifests tied to the action hash;
4. all twelve cell records with separate component contributions;
5. aggregate, beta-jump, scale, transversality, and ST reports;
6. an independent replay that does not import the primary assembler;
7. a gate audit updating `compiler_status.json` without altering downstream
   physics verdicts unless layer 3 actually passes.
