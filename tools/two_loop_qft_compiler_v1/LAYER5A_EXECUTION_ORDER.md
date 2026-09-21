# Layer-5A first-execution order

> **Post-P02 record (2026-09-21):** `UVP_P01=PASS` and `UVP_P02=PASS`;
> progress is `2/39` (`2/27` in the engine gate), and `UVP_P03` is next. The
> order and plan hash below are unchanged. See
> [`UVP_P01_RESULT.md`](UVP_P01_RESULT.md) and
> [`UVP_P02_RESULT.md`](UVP_P02_RESULT.md).

This file binds the frozen contract v2 hash
`6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92`
to its first fail-fast execution. It does not amend the contract. This file
records the current cursor while the machine ledger remains authoritative.

## Engine gate: exact order

The first 27 tests run serially in this order:

1. `UVP_P01` through `UVP_P13`, in numeric order;
2. `UVP_C01` through `UVP_C13`, in numeric order;
3. `UVP_M01`.

No control theory starts before all 13 primitives pass.  `M01` starts only
after all 13 controls pass.  Each test advances the cursor only on `PASS`.

On `BLOCKED`, the current phase stops as blocked.  On `FAIL`, the current phase
stops as failed.  Subsequent tests remain unexecuted and may not be marked as
implicitly passing.  A retry must increment that test's attempt number and
preserve the prior evidence artifact.

## Exact 27/27 checkpoint

The only engine-pass checkpoint is:

```text
executed = 27
passed = 27
blocked = 0
failed = 0
engine_gate = PASS
overall_status = ONE_LOOP_UV_POLE_EVALUATOR_PASS
authority = ENGINE_GATE_AUTHORITY
counterterm_compiler = BLOCKED
layer6_authorized = false
```

At that checkpoint `M02--M13` remain a distinct 12-test canonical gate.  The
engine result does not populate missing canonical residues or authorize
Layer 6.

## Result transitions

The machine ledger begins at `0/39` with `P01` ready, `P02--M01` waiting on
predecessors, and `M02--M13` locked on the engine gate.  Allowed test states
are:

```text
NOT_RUN -> RUNNING -> PASS | BLOCKED | FAIL
LOCKED  -> NOT_RUN only after the engine 27/27 checkpoint
```

Every terminal test record must contain primary and independent-replay
evidence, the derived result, a verdict reason, and content hashes for the
inventory/residue/UV-IR provenance artifacts where applicable.  Primitive
tests without graphs use an independently implemented second algebraic
method and mark graph inventory as not applicable rather than fabricating a
hash.

The schema is
[`uv_pole_evaluator_result_schema.json`](uv_pole_evaluator_result_schema.json),
the immutable order is
[`uv_pole_evaluator_execution_plan.json`](uv_pole_evaluator_execution_plan.json),
and the initial ledger is
[`uv_pole_evaluator_results.json`](uv_pole_evaluator_results.json).

## Authority ceiling

The initial ledger began at `0/39`.  Actual progress is recorded only in
`uv_pole_evaluator_results.json`; the counterterm compiler and Layer 6 remain
locked until their stated gates pass.  No finite `C1_GS`, gauge, BFB, flavor,
or proton-decay disposition changes merely from primitive progress.
