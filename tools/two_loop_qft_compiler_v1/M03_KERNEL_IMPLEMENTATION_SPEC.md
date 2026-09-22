# UVP_M03 parent-scalar two-point kernel specification

## Scope

This bounded implementation resolves only the attempt-1 blocker
`M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING`. It consumes
the frozen parent action, 328-real canonical basis, passed UV-pole primitives,
and M02 field residues. It does not alter the Layer-5A contract or any earlier
evidence.

## Canonical tensor convention

Write the unshifted scalar potential in canonically normalized real
coordinates as

```text
V = (1/2) M2_AB q_A q_B
  + (1/3!) V3_ABC q_A q_B q_C
  + (1/4!) V4_ABCD q_A q_B q_C q_D.
```

In the normalization already fixed by the primitive/control suite, the
scalar-loop quadratic counterterm matrix is

```text
deltaM2_scalar_AB
  = (1/2) V4_ABCD M2_CD + (1/2) V3_ACD V3_BCD.
```

The gauge contribution is assembled from the partial-BFM scalar two-point
graphs and the M02 field counterterm exactly once. The result must be
independent of `xi` after conversion from the 1PI mass pole to the parent
quadratic parameter counterterm.

## Primary kernel

The primary route shall:

1. generate the canonical 328-real basis and its sector ledger
   `54 + 252 + 20 + 2`;
2. construct the diagonal unshifted parent mass operator from the four frozen
   quadratic invariants;
3. enumerate the two scalar one-loop two-point topologies: the two-cubic
   bubble and the quartic tadpole;
4. evaluate the complete internal-index traces for every external parent
   sector, using exact sparse cubic tensors and exact homogeneous-quartic
   polarization rather than sampled physical-state queries;
5. retain scalar, quantum-vector, Goldstone, ghost, and M02 field-counterterm
   ledgers separately;
6. form the full pole operator in factorized sector-projector form and project
   it onto `mPhi2`, `mSigma2`, `mphi2`, and `mS2`.

Spin(10) covariance and PQ invariance imply that the complete symmetric pole
operator is a scalar multiple of the identity on each of the four inequivalent
realified parent irreps. The implementation must certify the representation
ledger, external-representative equality, and forbidden inter-sector blocks;
it may store the 328-square operator in exact factorized form rather than as a
dense array.

## Independent replay

The replay shall not import the primary contraction table. It shall assemble
the same quadratic pole from the one-loop functional expression

```text
Pole[V1_scalar] = (1/4) Tr[H(q)^2],
```

expanded to second order in independent parent backgrounds, together with an
independent background-covariant gauge/field-renormalization derivation. It
must regenerate its own sector traces and compare every coefficient of every
promoted quadratic residue with the frozen primary artifact.

## Acceptance

Attempt 2 may pass only if:

- all four quadratic residues are explicit local polynomials;
- the full factorized pole operator is symmetric;
- external representatives in each parent irrep agree exactly;
- the four quadratic projectors have full rank and zero projection residual;
- no PQ-forbidden or inter-sector quadratic structure is generated;
- `xi` cancels after the M02 field term is included exactly once;
- primary and replay coefficient dictionaries agree exactly;
- UV poles are present, IR poles are absent under the frozen regulated
  extraction, and no residue is inferred from a future two-loop cancellation.

Attempt 1 remains immutable historical evidence. A passing attempt 2 advances
the existing ledger cursor only to `UVP_M04`; otherwise execution stops.
