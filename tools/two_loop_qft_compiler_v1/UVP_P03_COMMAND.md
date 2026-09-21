# Exact UVP_P03 execution command

## Frozen Codex instruction

> Execute only `UVP_P03` under the unchanged Layer-5A contract-v2 and
> first-execution plan. Preserve P01 and P02 evidence unchanged. Evaluate the
> doubled propagator directly with the primary UV projector, replay it with a
> separately implemented Gamma-function route, and separately compute minus
> the mass derivative of the verified frozen P01 pole. Do not use the P01
> derivative as primary evaluator input. Require exact three-way agreement and
> explicit Minkowski numerator/sign consistency. Advance only to P04 on pass.

## Reproduction command

Run from the repository root while P03 is the authorized cursor:

```powershell
python tools/two_loop_qft_compiler_v1/execute_uvp_p03_primary.py
python tools/two_loop_qft_compiler_v1/independent_uvp_p03_replay.py
python tools/two_loop_qft_compiler_v1/derive_uvp_p03_p01_relation.py
python tools/two_loop_qft_compiler_v1/adjudicate_uvp_p03.py
python tools/two_loop_qft_compiler_v1/audit_uvp_p03.py
python tools/two_loop_qft_compiler_v1/audit_uv_pole_execution_plan.py
```

The adjudicator freezes all three artifacts before comparison, validates
[`uvp_p03_evidence_schema.json`](uvp_p03_evidence_schema.json), preserves the
P01 and P02 ledger records as unchanged JSON values, and advances only to P04
when every pairwise residue difference and the integrand-sign residual vanish.

The command does not execute P04, populate canonical counterterms, alter any
physics disposition, or authorize Layer 6.
