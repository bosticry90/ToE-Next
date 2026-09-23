# UVP_M05 unblock progress: complete primary operator

## Authority boundary

This is an implementation checkpoint, not a retry or promotion of `UVP_M05`.
The authoritative result remains:

```text
31/39 = 30 PASS, 1 BLOCKED, 0 FAIL
UVP_M05 = BLOCKED (attempt 1)
ONE_LOOP_COUNTERTERM_COMPILER = BLOCKED
Layer 6 authorized = false
```

No complete canonical M05 residue is promoted here.

## Complete primary scalar contraction

The primary scalar implementation now covers every one of the 328 real
internal scalar directions and all 26 real Hermitian quartic directions.  It
uses the exact functional identity

```text
V_div^(scalar)|_4 = (1/4) Tr[H2(q)^2]
R4(q,q,q,q)      = 6 Tr[H2(q)^2]
```

without materializing a dense `328^4` tensor.  The implementation includes:

- the previously certified `Phi+phi+S` rank-11 subtheory;
- all Sigma radial and mixed radial quartics;
- `lambdaSigmaphi2`, `z4`, and `zD` in a real Hermitian basis;
- the exact `lambdaPhiSigma2` factorized contraction;
- all four independent pure-Sigma quartics;
- the complete `zEta` real/imaginary structure;
- every cross-coupling among the 26 quartic input directions.

The complete scalar result is evaluated on the frozen exact rank-26
projector plus two independent exact backgrounds.  It has rank 26, zero
projection residual, and zero independent-background residual.  Its artifact
is `uvp_m05_complete_scalar_v4v4.json`.

Calculation-local subtheory artifacts retain separately auditable ledgers for
the Sigma radial, Sigma bilinear, `Phi-Sigma`, pure-Sigma, and `zEta`
contractions.  These are regression components, not separate scientific
gates.

## Complete primary partial-BFM gauge contribution

`m05_partial_bfm_gauge_completion.py` derives the gauge completion from the
frozen partial-BFM determinant and the exact gauge-orbit polynomial.  It keeps
separate vector, Goldstone, ghost, Goldstone-mixed, and M02 external-field
conversion entries.  The determinant weights are

```text
vector transverse   3/4
vector longitudinal xi^2/4
Goldstone pure      xi^2/4
ghost              -xi^2/2
```

so the pure gauge-orbit coefficient is `3/4`.  The Goldstone-mixed and M02
field terms combine as

```text
xi/2 + (3-xi)/2 = 3/2,
```

giving exact `xi` cancellation in every promoted primary quartic residue.
M02 field conversion is included exactly once.  The complete primary scalar
plus gauge candidate is frozen in
`uvp_m05_primary_complete_candidate.json`; its authority explicitly remains
below a formal M05 pass.

## Independent gauge replay

`independent_m05_gauge_replay.py` uses a new deterministic rank-26 background
set, the independently normalized 45-generator basis, its own coefficient-
preserving five-form action, direct construction of the 328-real orbit Gram
matrix, and a separate determinant degree-of-freedom ledger.  It imports
neither the primary background set nor its orbit coefficients or gauge
residue table before freezing its uncompared artifact.

The replay reproduces every gauge-orbit coefficient and all 26 partial-BFM
gauge residues with exact maximum residual zero and exact `xi` cancellation.
The final component artifact is `uvp_m05_independent_gauge_replay.json`.

During development this replay caught a real convention bug in its own first
run: the legacy form-action helper casts generator coefficients to integers,
which erased the Sigma orbit when supplied normalized generators.  That run
never produced a promoted artifact.  The final replay implements the
normalized five-form action independently and passes exactly.

## Remaining M05 blocker

The frozen M05 contract requires a complete inventory-independent replay of
the scalar as well as gauge operator.  The complete scalar replay has not yet
been implemented.  The primary component kernels cannot replay themselves,
and the successful independent gauge replay cannot substitute for this
missing scalar authority.

The only remaining implementation blocker is therefore:

```text
M05_INVENTORY_INDEPENDENT_COMPLETE_SCALAR_OPERATOR_REPLAY_MISSING
```

Until that replay exists and agrees with the frozen primary operator, M05
attempt 2 must not be adjudicated, M06--M13 remain locked, the counterterm
compiler remains blocked, and Layer 6 remains unauthorized.

The machine-readable checkpoint is `m05_unblock_progress.json`.  The separate
`layer5b_m05_m13_preflight.json` records later implementation dependencies
without granting any downstream scientific authority.
