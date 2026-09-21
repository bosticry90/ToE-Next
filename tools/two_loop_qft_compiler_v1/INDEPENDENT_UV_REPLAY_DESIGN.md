# Independent replay design for the Layer-5A UV-pole evaluator

This document freezes how `UVP_M13` tests diagram completeness in addition to
UV algebra.  It is specification authority only.  It does not execute a test
or supply a residue.

## Shared independence boundary

The replay may read the immutable parent/partial-BFM action and convention
hashes.  It may not import:

- the primary one-loop graph list or its canonical labels;
- primary graph automorphisms, symmetry factors, or Grassmann signs;
- the primary large-loop-momentum/auxiliary-mass expansion;
- the primary tensor reducer or UV-pole tables;
- expected beta functions as calculated outputs.

Comparisons occur only after each route has frozen its own graph/operator
inventory and residues.  Agreement on an incomplete imported list is not
independence.

## Design A: independent diagrammatic replay

Design A is the preferred process-level replay.

1. Reconstruct the needed vertices by functional differentiation of the
   frozen action, rather than importing the primary vertex-dispatch output.
2. For each required external process, generate connected one-loop 1PI graphs
   with an independent half-edge pairing algorithm.
3. Assign fields using independently implemented Lorentz, SM-charge, ghost
   number, background/quantum-role, and statistics constraints.
4. Canonicalize graphs with an implementation that does not share the primary
   canonical-label routine.  Compute automorphism orders, symmetry factors,
   closed-ghost signs, and ordered quartic-ghost signs independently.
5. Freeze the inventory before evaluating poles.
6. Extract poles with a second method, preferably nonexceptional-momentum
   Feynman parameters/Gamma functions for the replay set, so it does not share
   the primary auxiliary-mass UV projector.

For every external process, Design A must emit:

- an independent canonical graph-set hash;
- `primary_minus_replay` and `replay_minus_primary` set differences;
- per-graph symmetry-factor and statistics-sign residuals;
- the independently derived local UV residue table;
- a process-level pass/block/fail disposition.

Promotion requires empty directed set differences, zero symmetry/sign
residuals, and exact or certified agreement of the local pole action.

## Design B: functional/effective-action replay

Design B is acceptable only if it is genuinely inventory-independent.  It may
use a background-field functional determinant, covariant derivative
expansion, or heat-kernel calculation built directly from the frozen
quadratic fluctuation operators.

It must emit:

- a completeness certificate for every field block, interaction insertion,
  and perturbative order contributing to the requested one-loop functions;
- an explicit map from functional traces to every required local scalar,
  vector, ghost, BRST, tadpole, and VEV operator;
- an independent UV residue table with UV and IR labels kept separate;
- a comparison against the primary diagrammatic pole action.

A functional result that checks only the aggregate background `F^2` operator
does not cover `M02--M13`; the full canonical operator map is mandatory.

## Coverage matrix

Whichever design is chosen must cover:

- all primitive residues used by promotion;
- every promoted control-theory residue;
- parent scalar one-, two-, three-, and four-point functions;
- quantum-vector and heavy/light-ghost two-point functions;
- the gauge-parameter and selected BRST/Slavnov--Taylor vertices;
- tadpole/VEV and all 33 Goldstone consistency relations;
- the parent background-gauge two-point function used to derive `b10`.

Design A and Design B may be combined, but partial coverage from each does not
constitute a complete replay unless their union is accompanied by a frozen,
gap-free coverage map.

## Authority rule

An independently reproduced wrong or out-of-basis local pole is scientific
evidence and triggers the established fail/adjudication path.  Missing replay
coverage, unmatched graph sets, or an incomplete functional completeness
certificate is `BLOCKED`.  Primary/replay disagreements are localized; they
are never averaged.
