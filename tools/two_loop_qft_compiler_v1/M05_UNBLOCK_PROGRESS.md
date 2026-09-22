# UVP_M05 unblock progress: exact non-Sigma scalar subtheory

## Authority boundary

This is an implementation checkpoint, not a retry or promotion of `UVP_M05`.
The authoritative result remains:

```text
31/39 = 30 PASS, 1 BLOCKED, 0 FAIL
UVP_M05 = BLOCKED (attempt 1)
ONE_LOOP_COUNTERTERM_COMPILER = BLOCKED
Layer 6 authorized = false
```

No M05 residue for the complete canonical theory is claimed here.

## Implemented contraction

`m05_parent_scalar_kernel.py` implements the exact scalar one-loop quartic
functional on the restricted `Phi+phi+S` scalar subtheory.  It uses

```text
R4(q,q,q,q) = (3/2) sum_AB V4(q,q,e_A,e_B)^2
             = 6 Tr[H2(q)^2],
```

where `H2=d^2 V4` and the second equality accounts for
`H2=V4(q,q,.,.)/2`.  All 76 real internal directions in the restricted
subtheory are included.  The calculation is performed with sparse exact
degree-four monomials and never materializes a dense rank-four field tensor.

The exact projector covers these 11 real directions:

- `lambdaPhi1`, `lambdaPhi2`;
- `lambdaPhiphi1`, `lambdaPhiphi2`, `lambdaPhiS`;
- `lambdaPhiVector1`, `lambdaPhiVector2`;
- `lambdaVectorS`, `lambdaS`;
- `Re(zK)`, `Im(zK)`.

Its deterministic witness matrix has rank 11 and nonzero exact determinant.
Every projected coefficient table round-trips to all eleven diagonal pole
evaluations with zero exact residual.

The independent bounded audit rebuilds the projector from the complete parent
invariant oracle rather than the primary sparse monomial lists.  It also
reproduces the independent radial `O(N)` controls

```text
delta_lambdaPhi1     = 248 lambdaPhi1^2       (N=54 normalization),
delta_lambdaPhiVector1 = 28 lambdaPhiVector1^2 (N=20),
delta_lambdaS|_(only lambdaS nonzero) = 10 lambdaS^2
```

in the frozen simple-pole convention.

Artifacts:

- primary subspace artifact: `uvp_m05_active_scalar_subspace.json`;
- bounded independent audit: `uvp_m05_active_scalar_subspace_audit.json`.

The complete invariant projector is also now implemented independently of the
pole calculation. `m05_rank26_projector.py` adds 15 deterministic exact
Sigma-bearing witnesses (fixed Gaussian-integer form seeds) to the eleven
subtheory witnesses. The resulting 26-by-26 matrix has exact rank 26 and a
nonzero exact determinant. Its frozen artifact is
`uvp_m05_rank26_projector.json`.

The exact gauge-orbit quartic has also been projected.  With
`K_ab(q)=<T_a q,T_b q>` in the canonical kinetic and generator conventions,
`m05_gauge_orbit_quartic.py` finds

```text
Tr K^2 =
  3 lambdaPhi1 + 10 lambdaPhi2
  + 6 lambdaPhiSigma1 + 4 lambdaPhiSigma2
  + 2 lambdaPhiphi1 + 20 lambdaPhiphi2
  + 45/4 lambdaSigma1 - 4 lambdaSigma2
  + 2 lambdaSigma3 - 1/2 lambdaSigma4
  + 5 lambdaSigmaphi1
  + 5 lambdaPhiVector1 + 4 lambdaPhiVector2,
```

where the symbols on the right denote the corresponding frozen invariant
polynomials, not couplings.  A twenty-seventh exact background gives zero
projection residual.  This fixes the group-theory polynomial needed by the
gauge-generated `g10^4` term, but deliberately does not assign its loop
prefactor or claim partial-BFM `xi` cancellation.

## Remaining M05 blocker

The restricted result is not the complete residue even for its eleven output
directions, because the full canonical theory also contains Sigma-bearing
vertices whose internal Sigma lines contribute.  The missing implementation
is now localized to:

1. the 252-real-direction Sigma contraction backend, including the four
   independent `Sigma^2 Sigma*^2` tensors and the `zEta` structure;
2. all mixed Sigma quartic contractions and the remaining 15 real invariant
   directions;
3. the partial-BFM vector/Goldstone/ghost four-point pole, including the
   coefficient and sector decomposition of the now-projected gauge-orbit
   quartic and exact `xi` cancellation;
4. a complete inventory-independent replay of the 26-direction operator.

Until all four exist, M05 attempt 2 must not be adjudicated and M06 remains
locked.

The machine-readable checkpoint is `m05_unblock_progress.json`. It records no
new test authority and narrows the implementation blocker to
`M05_SIGMA_V4V4_AND_PARTIAL_BFM_4PT_ASSEMBLY_MISSING`.
