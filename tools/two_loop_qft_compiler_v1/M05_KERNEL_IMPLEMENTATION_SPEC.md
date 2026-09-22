# UVP_M05 exhaustive quartic kernel implementation contract

This implementation note refines the existing frozen M05 acceptance criterion;
it does not amend it and carries no test authority.

## Required pole operator

Let `I_r(q)`, `r=1,...,26`, be the real Hermitian quartic invariant basis of
`PARENT_ACTION_V1`, and let

```text
V4(q) = sum_r c_r I_r(q),
H2_AB(q) = d_A d_B V4(q).
```

The scalar one-loop local quartic pole is represented without a dense
`328^4` tensor by

```text
Vdiv_scalar(q)|4 = 1/4 Tr[H2(q)^2],
R4_scalar(q,q,q,q) = 3/2 sum_AB V4(q,q,e_A,e_B)^2.
```

The second formula is the primary exhaustive `V4*V4` contraction.  Every
canonical real internal direction appears in the sum.  Symmetric internal
pairs may be enumerated once with multiplicity two off diagonal.

## Projection

Use the 26 deterministic exact parent backgrounds frozen by
`m05_rank26_projector.py`, whose matrix

```text
E_ar = I_r''''(q_a,q_a,q_a,q_a) = 24 I_r(q_a)
```

has exact rank 26.  Project the complete pole only after scalar, vector,
Goldstone, ghost, and M02 field-conversion ledgers have separately been
frozen.  Passing M05 requires a zero exact/certified residual on independent
verification backgrounds, not merely on the 26 projector rows.

## Gauge completion

The gauge contribution must be derived from the frozen partial-BFM action.
It must retain separately:

- quantum-vector diagrams;
- Goldstone diagrams;
- ghost diagrams;
- the M02 external-field conversion exactly once;
- gauge-generated `g10^4` quartics.

The promoted sum must satisfy the frozen `xi`-cancellation requirement.  A
general-RGE formula may be used only as a regression comparator.

## Independent replay

The replay may not import the primary internal-pair inventory or projected
coefficient tables.  It must rebuild the quartic pole by independently
differentiating `1/4 Tr[H2(q)^2]` (or by a complete functional method), freeze
its own inventory, and agree on all 26 residues and the full quadrilinear
operator.

## Current implementation boundary

`m05_parent_scalar_kernel.py` implements and exactly projects the complete
scalar contraction on the closed `Phi+phi+S` subspace (11 real directions,
76 internal real fields). `m05_rank26_projector.py` separately freezes the
complete exact rank-26 invariant projector using 15 additional Sigma-bearing
witnesses. These are implementation checkpoints only. M05 remains blocked
until the Sigma-containing scalar contractions and partial-BFM gauge
completion exist and the full operator has an independent replay.
