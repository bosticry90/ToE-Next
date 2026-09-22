# Layer 5B: M04 retry and M05 fail-fast result

## Disposition

`UVP_M04` passes on attempt 2. Serial execution then reaches M05 and stops at
the first new non-pass:

```text
UVP_M04 = PASS
UVP_M05 = BLOCKED
M05_EXHAUSTIVE_PARENT_SCALAR_4PT_CONTRACTION_PROJECTOR_MISSING
```

The authoritative ledger is `31/39`: 30 pass, one block, and zero failures.
`ONE_LOOP_UV_POLE_EVALUATOR_PASS` remains earned. The complete counterterm
compiler remains blocked and Layer 6 remains unauthorized.

## M04 implementation

The primary route evaluates the complete one-loop scalar cubic pole from

\[
\frac12\sum_{D,E}\left(
V_{3,ADE}V_{4,BCDE}+V_{3,BDE}V_{4,CADE}
+V_{3,CDE}V_{4,ABDE}\right).
\]

All 328 parent real directions are audited. Because none of the frozen cubic
operators contains `Sigma`, its 252 directions are structural zeros in this
contraction. The remaining 76 `Phi+phi+S` directions are summed exhaustively
as ordered pairs. The partial-BFM 1PI gauge completion and M02 field
conversion are retained separately and cancel `xi` exactly.

The independent replay imports neither the primary field-pair inventory nor
its derivative tensors. It rebuilds the inventory and obtains cubic and
quartic derivatives through independent eight- and sixteen-corner parent
polynomial polarizations. Both coefficient matrices agree exactly.

## Earned cubic residues

The following coefficients multiply `1/(16*pi^2*epsilon_bar)`:

```text
delta_muPhi =
  45*g10^2*muPhi + 24*lambdaPhi1*muPhi
  + (354/5)*lambdaPhi2*muPhi + lambdaPhiphi2*muPhiPhi

delta_muPhiPhi =
  (57/2)*g10^2*muPhiPhi
  + 2*lambdaPhiVector1*muPhiPhi + 4*lambdaPhiVector2*muPhiPhi
  + 4*lambdaPhiphi1*muPhiPhi + (84/5)*lambdaPhiphi2*muPhi
  + (58/5)*lambdaPhiphi2*muPhiPhi
  + 8*z6_im*zK_im + 8*z6_re*zK_re

delta_z6_re =
  (27/2)*g10^2*z6_re + 2*lambdaPhiVector1*z6_re
  + 20*lambdaPhiVector2*z6_re + 2*lambdaVectorS*z6_re
  + (54/5)*muPhiPhi*zK_re

delta_z6_im =
  (27/2)*g10^2*z6_im + 2*lambdaPhiVector1*z6_im
  + 20*lambdaPhiVector2*z6_im + 2*lambdaVectorS*z6_im
  + (54/5)*muPhiPhi*zK_im
```

The four-real-direction projector has exact rank four and zero residual. The
trilinear form is permutation symmetric, no Sigma-containing or PQ-forbidden
cubic is generated, and attempt 1 remains preserved as historical evidence.

## M05 fail-fast stop

M05 targets 18 real plus four complex quartic families, or 26 real
directions. The primary and independent capability audits agree that the
following required implementation is absent:

- exhaustive symmetrized `V4*V4` contractions over the parent field space;
- the full partial-BFM scalar four-point pole, including gauge-generated
  quartic structures;
- the rank-26 real invariant projector; and
- an inventory-independent fourth-derivative replay.

No M05 residue has been calculated or inferred. This is an implementation
block, not evidence of a radiative-closure or physics failure. M06-M13 remain
unexecuted.

## Frozen artifacts

- M04 attempt-2 evidence:
  `2e199c35a4f48e210a4de42178d45b1df9d622676956f968462b9ebb12b7018c`
- M05 blocked evidence:
  `29998c0e5df9562ed5fa6e5bd109a2ea03c0a0730a8490ff8691be74e1d57859`
- 31/39 checkpoint:
  `83c9a6340b175d15affa3baa5fec1f7cac19ec9cafba0a8b8fdae34e5d789ec4`

## Preserved boundaries

- `ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED`
- `DIRECT_GAUGE_MATCHING_UNRESOLVED`
- `BFB_UNRESOLVED`
- `finite_C1_GS = null`
- `layer6_authorized = false`

The only next admissible implementation target is the exhaustive M05 parent
scalar four-point contraction/gauge-completion/projector kernel.
