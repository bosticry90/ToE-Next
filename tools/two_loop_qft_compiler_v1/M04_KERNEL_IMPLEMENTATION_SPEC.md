# UVP_M04 parent-scalar three-point kernel specification

## Scope

This bounded implementation resolves only the attempt-1 blocker
`M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING`. It consumes
the frozen parent action, canonical 328-real basis, passed one-loop UV-pole
evaluator, and M02 field residues. It does not alter any earlier evidence.

## Canonical convention

In canonically normalized real coordinates,

```text
V = (1/2) M2_AB q_A q_B
  + (1/3!) V3_ABC q_A q_B q_C
  + (1/4!) V4_ABCD q_A q_B q_C q_D.
```

The scalar-loop cubic counterterm is the third derivative of
`Pole[V1_scalar]=(1/4) Tr[H(q)^2]`:

```text
deltaV3_scalar_ABC = (1/2) sum_DE [
    V3_ADE V4_BCDE + V3_BDE V4_CA DE + V3_CDE V4_ABDE
].
```

Equivalently, on one diagonal background `q`,

```text
deltaV3_scalar(q,q,q) = (3/2) sum_DE V3(q,D,E)V4(q,q,D,E).
```

The complete counterterm adds the partial-BFM gauge 1PI completion and the
M02 field conversion exactly once. For a cubic invariant with external
Casimirs `C_A+C_B+C_C`, these pieces are respectively
`(xi/2) g10^2 sum(C) h` and `((3-xi)/2) g10^2 sum(C) h`, hence the promoted
sum is `(3/2) g10^2 sum(C) h` and is independent of `xi`.

## Primary kernel

The primary route uses the exact analytic parent cubic derivative and an
exact compressed homogeneous-quartic polarization. It enumerates all 328
internal real directions. The 252 Sigma directions are certified structural
zeros because none of the three frozen cubic families contains Sigma; the
remaining 76 directions are summed exhaustively as ordered pairs. It stores
the nonzero field-pair inventory and sector contributions before projection.

Four deterministic parent backgrounds isolate the real cubic invariant
directions `muPhi`, `muPhiPhi`, `Re(z6)`, and `Im(z6)`. The resulting exact
rank-four evaluation matrix is inverted only after the complete scalar and
gauge trilinear form has been assembled.

## Independent replay

The replay must not import the primary promoted contraction table. It
regenerates the one-loop graph inventory from the canonical basis, derives
the cubic derivative by an independent eight-corner polarization of the
frozen parent invariant evaluator, and derives the quartic derivative using
the uncompressed sixteen-corner polarization. It freezes its inventory and
residue artifact before comparison.

## Acceptance

Attempt 2 passes only if:

- all four real cubic residues are explicit local polynomials;
- the cubic evaluation matrix has exact rank four;
- the complete trilinear form is symmetric under external permutations;
- its projection on the four frozen cubic invariant tensors has zero exact
  residual on the projector and independent verification backgrounds;
- no Sigma-containing, PQ-forbidden, or other cubic operator is generated;
- scalar, vector, Goldstone, ghost, and M02 field pieces remain separately
  auditable and `xi` cancels exactly;
- primary and replay graph inventories and all residue coefficients agree;
- UV poles are present and IR poles are absent under the frozen regulated
  local extraction.

Attempt 1 remains immutable historical evidence. A passing attempt 2 advances
the serial cursor only to `UVP_M05`.
