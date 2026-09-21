# Exact UVP_P02 execution command

## Frozen Codex instruction

> Continue the frozen Layer-5A execution with `UVP_P02` only under contract v2
> hash `6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92`
> and execution-plan hash
> `54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101`.
> Preserve the terminal P01 evidence unchanged. Derive the massive rank-zero
> logarithmic-bubble UV pole with the primary radial large-loop-momentum
> projector and a separately implemented Wick-rotated Gamma-function replay.
> Verify exact mass independence, freeze both artifacts before comparing them,
> and record the UV/IR provenance and content hashes. Advance only to P03 on
> exact agreement. Do not execute P03 or authorize any later layer.

## Reproduction command

Run from the repository root:

```powershell
python tools/two_loop_qft_compiler_v1/execute_uvp_p02_primary.py
python tools/two_loop_qft_compiler_v1/independent_uvp_p02_replay.py
python tools/two_loop_qft_compiler_v1/adjudicate_uvp_p02.py
python tools/two_loop_qft_compiler_v1/audit_uvp_p02.py
python tools/two_loop_qft_compiler_v1/audit_uv_pole_execution_plan.py
```

The first program performs a radial large-momentum UV projection. The second
does not import that expansion and instead evaluates the closed Gamma-function
integral. The adjudicator freezes both artifacts, validates
[`uvp_p02_evidence_schema.json`](uvp_p02_evidence_schema.json), preserves the
P01 record byte-for-byte as a JSON value, and advances the ledger to P03 only
after exact agreement and an exact zero mass derivative.

The command does not execute P03, populate a canonical counterterm, alter a
physics disposition, or authorize Layer 6.
