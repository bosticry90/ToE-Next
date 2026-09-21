# Exact UVP_P01 execution command

## Frozen Codex instruction

> Execute only `UVP_P01` under contract v2 hash
> `6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92`
> and execution-plan hash
> `54d792571e20239e7b586360fe04557154fc64a5942865896c35d34b89584101`.
> Derive the massive rank-zero tadpole pole with the primary
> large-loop-momentum/auxiliary-mass projector and a separately implemented
> Wick-rotated Gamma-function replay.  Freeze both artifacts before comparing
> them.  Record the integral convention, exact normalized residue, UV/IR
> classification, auxiliary-mass cancellation, artifact hashes, and verdict
> in the P01 evidence and execution ledgers.  Advance to `UVP_P02` only on
> exact agreement.  Do not execute P02, populate canonical counterterms,
> change a physics disposition, or authorize Layer 6.

## Reproduction command

Contract v2 and the execution plan authorize only `UVP_P01` at the start of
this command.  Run from the repository root:

```powershell
python tools/two_loop_qft_compiler_v1/execute_uvp_p01_primary.py
python tools/two_loop_qft_compiler_v1/independent_uvp_p01_replay.py
python tools/two_loop_qft_compiler_v1/adjudicate_uvp_p01.py
python tools/two_loop_qft_compiler_v1/audit_uvp_p01.py
python tools/two_loop_qft_compiler_v1/audit_uv_pole_execution_plan.py
```

The first program uses the large-loop-momentum/auxiliary-mass UV projector.
The second program does not import it and instead evaluates the Wick-rotated
closed Gamma-function integral.  The adjudicator freezes both artifacts before
comparison, validates
[`uvp_p01_evidence_schema.json`](uvp_p01_evidence_schema.json), and advances
the ledger to `UVP_P02` only on exact agreement.

The command does not execute `P02`, populate a canonical counterterm, or
authorize Layer 6.
