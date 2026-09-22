# Layer 5B: M03 retry and M04 fail-fast result

## Disposition

The focused M03 implementation retry passes on attempt 2:

```text
UVP_M03 = PASS
```

The frozen serial execution then advances to M04 and stops at the first new
non-pass:

```text
UVP_M04 = BLOCKED
M04_EXHAUSTIVE_PARENT_SCALAR_3PT_CONTRACTION_PROJECTOR_MISSING
```

The authoritative ledger is `30/39`: 29 pass, one block, and zero failures.
The engine gate remains `ONE_LOOP_UV_POLE_EVALUATOR_PASS`; the complete
counterterm compiler remains blocked and Layer 6 remains unauthorized.

## M03 implementation

The promoted kernel works in the frozen 328-real unshifted parent basis. It
constructs the complete constant scalar two-point pole operator from the
exhaustive scalar contractions

\[
\frac12 V_{3,ACD}V_{3,BCD}
+\frac12 V_{4,ABCD}(M^2)_{CD},
\]

then adds the partial-BFM gauge completion and the already-earned M02 field
counterterm exactly once. The operator is stored in exact factorized form as
the four identity blocks of dimensions `54 + 252 + 20 + 2`, rather than as a
dense 328 by 328 array.

The primary implementation uses exact sparse parent-vertex contractions. The
independent replay regenerates the quartic part through functional Hessian
sector Laplacians and the cubic part through separately implemented
eight-corner finite differences with exact rational recognition. Neither
route imports the other's promoted contraction table.

## Earned quadratic residues

The following coefficients multiply `1/(16*pi^2*epsilon_bar)`:

```text
delta_mPhi2 =
  30*g10^2*mPhi2
  + 224*lambdaPhi1*mPhi2
  + (224/5)*lambdaPhi2*mPhi2
  + lambdaPhiS*mS2
  + 504*lambdaPhiSigma1*mSigma2
  - 56*lambdaPhiSigma2*mSigma2
  + 10*lambdaPhiphi1*mphi2
  + lambdaPhiphi2*mphi2
  + (126/5)*muPhi^2
  + (1/2)*muPhiPhi^2

delta_mSigma2 =
  (75/2)*g10^2*mSigma2
  + 108*lambdaPhiSigma1*mPhi2
  - 12*lambdaPhiSigma2*mPhi2
  + 1016*lambdaSigma1*mSigma2
  + 2440*lambdaSigma2*mSigma2
  + 2680*lambdaSigma3*mSigma2
  + 4960*lambdaSigma4*mSigma2
  + lambdaSigmaS*mS2
  + 10*lambdaSigmaphi1*mphi2
  + 5*lambdaSigmaphi2*mphi2

delta_mphi2 =
  (27/2)*g10^2*mphi2
  + 22*lambdaPhiVector1*mphi2
  + 4*lambdaPhiVector2*mphi2
  + 108*lambdaPhiphi1*mPhi2
  + (54/5)*lambdaPhiphi2*mPhi2
  + 504*lambdaSigmaphi1*mSigma2
  + 252*lambdaSigmaphi2*mSigma2
  + lambdaVectorS*mS2
  + (27/5)*muPhiPhi^2
  + 4*z6_re^2 + 4*z6_im^2

delta_mS2 =
  108*lambdaPhiS*mPhi2
  + 4*lambdaS*mS2
  + 504*lambdaSigmaS*mSigma2
  + 10*lambdaVectorS*mphi2
  + 20*z6_re^2 + 20*z6_im^2
```

The four-direction projection has rank four and exact residual zero. The
primary and replay expressions agree exactly. The original attempt-1 blocker
is preserved as historical evidence rather than overwritten.

## M04 fail-fast stop

M04 targets the four real cubic directions `muPhi`, `muPhiPhi`, `Re(z6)`,
and `Im(z6)`. Both the primary capability audit and the independent
AST/artifact audit find the same missing implementation:

- an exhaustive mixed `V3_ADE * V4_BCDE` three-point contraction backend;
- the complete partial-BFM vector/Goldstone/ghost scalar three-point pole
  kernel; and
- a four-real-direction cubic invariant projector with independent replay.

No M04 residue was evaluated or inferred. This is an implementation block,
not a radiative-closure failure or other physics failure. Tests M05-M13 were
not run.

## Frozen artifacts

- M03 attempt-2 evidence:
  `ddad67dc0278be554c5a4cd401d66e348ed08cfef6f0bd6a4a0df406ca0b5451`
- M04 blocked evidence:
  `683ffc450210b10fd381f45b6942d00fa7ec6fee818335bf5a2aaa9de30b2898`
- 30/39 checkpoint:
  `af50334b6393ecf7a7752b3f6faddbea9212c3ffd0d54748ad6c745a4d2006f4`

## Preserved boundaries

- `ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED`
- `DIRECT_GAUGE_MATCHING_UNRESOLVED`
- `BFB_UNRESOLVED`
- `finite_C1_GS = null`
- `layer6_authorized = false`

The only next admissible implementation target is the exhaustive M04 parent
scalar three-point contraction/projector kernel.
