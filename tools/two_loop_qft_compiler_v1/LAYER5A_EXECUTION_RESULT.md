# Layer 5A serial execution result

## Outcome

The frozen contract-v2 execution advanced serially from `UVP_P06` through
`UVP_M03` and stopped at the first non-`PASS` result, as required.

The earned engine result is

```text
ONE_LOOP_UV_POLE_EVALUATOR_PASS
```

with all 27 engine tests passing:

```text
P01-P13: 13/13 PASS
C01-C13: 13/13 PASS
M01:      1/1 PASS
```

The overall Layer-5 result remains

```text
ONE_LOOP_COUNTERTERM_COMPILER_BLOCKED
```

The authoritative ledger stopped at `29/39`: 28 tests passed, `UVP_M03`
blocked, none failed, and `M04-M13` were not run.

The frozen checkpoint artifact SHA-256 is
`8a31bb28df83b7417c5e98d019547ec95966fe3147330b2b05c9a58f7e4b0187`.

## Engine-gate authority

The 27/27 checkpoint independently derives the parent gauge coefficient

```text
b10 = -34/3
```

after the primitive and control-theory suites pass. The engine-gate artifact
is `uv_pole_engine_gate_result.json`; its canonical artifact SHA-256 is
`f40d1653eda2ef8bfc73385a475a17fb4d95a01d95ece312116c862f02f91657`.

This result earns authority for the one-loop UV-pole evaluator only. It does
not promote the canonical counterterm compiler and does not authorize Layer 6.

## Canonical-model progress

`UVP_M02` passes and derives the four parent scalar wave-function residues:

```text
delta_Z_Phi   = -10*g10^2*(3-xi)
delta_Z_Sigma = -(25/2)*g10^2*(3-xi)
delta_Z_phi   = -(9/2)*g10^2*(3-xi)
delta_Z_S     = 0
```

The irrep-identity residual is exactly zero in the certified calculation and
independent replay.

## Fail-fast stop at M03

`UVP_M03` is `BLOCKED`, not `FAIL`. Both the primary capability audit and an
independent API/artifact audit find the same implementation dependency:

```text
M03_EXHAUSTIVE_PARENT_SCALAR_2PT_CONTRACTION_KERNEL_MISSING
```

The absent capabilities are:

- an exhaustive parent-scalar one-loop two-point inventory;
- exact summed `V3*V3` and `M2*V4` contraction backends over the 328-real
  parent field space;
- the quadratic pole projector with gauge/Goldstone/ghost completion.

No M03 residue was fabricated from a later cancellation. The UV/IR
classification remains unevaluated because the required 1PI integrands have
not been materialized. The blocker is an implementation dependency, not an
observed inconsistency of the canonical action.

## Frozen dispositions

- `DIRECT_GAUGE_MATCHING_UNRESOLVED`
- `BFB_UNRESOLVED`
- `finite_C1_GS = null`
- `layer6_authorized = false`

The next admissible implementation target is the exhaustive parent scalar
two-point contraction/projector kernel required by M03. Tests M04-M13 remain
unexecuted until M03 passes in a later attempt.

## Subsequent Layer-5B continuation

M03 was later retried without altering its acceptance criteria. Attempt 2
implements the exhaustive parent-scalar two-point contraction/projector
kernel, independently replays it, and passes with four exact quadratic
residues and zero projection residual. The historical attempt-1 block remains
preserved.

M04 was subsequently retried without changing its criteria. Attempt 2
implements and independently replays the exhaustive sparse `V3*V4`
three-point contraction plus partial-BFM completion and passes with four exact
cubic residues and zero rank-4 projection residual. The serial gate then
stops at M05 because the exhaustive quartic pole kernel is absent. The current
authoritative state is `31/39` (30 pass, one block, zero fail). See
[`LAYER5B_M04_M05_RESULT.md`](LAYER5B_M04_M05_RESULT.md).
