# Exact UVP_P04 execution command

## Frozen Codex instruction

> Execute only `UVP_P04` under the unchanged Layer-5A contract-v2 and
> first-execution plan. Preserve P01--P03 evidence unchanged. Reduce the frozen
> rank-two tensor vacuum primitive in `d=4-2*epsilon` before Laurent expansion,
> replay it with an independent rotational/Gamma or Gaussian-source method,
> contract both results back to the scalar integral, and quarantine an explicit
> premature-`d=4` branch. Advance only to P05 on exact agreement.

## Reproduction command

Run from the repository root while P04 is the authorized cursor:

```powershell
python tools/two_loop_qft_compiler_v1/execute_uvp_p04_primary.py
python tools/two_loop_qft_compiler_v1/independent_uvp_p04_replay.py
python tools/two_loop_qft_compiler_v1/adjudicate_uvp_p04.py
python tools/two_loop_qft_compiler_v1/audit_uvp_p04.py
python tools/two_loop_qft_compiler_v1/audit_uv_pole_execution_plan.py
```

The primary route uses the exact `delta_mu_nu/d` reducer. The replay derives
the tensor directly from a Schwinger-parameter Gaussian source and does not
import that reducer. The adjudicator freezes both artifacts, validates
[`uvp_p04_evidence_schema.json`](uvp_p04_evidence_schema.json), preserves the
P01--P03 ledger rows, and advances only to P05 after exact residue,
contraction, and adversarial checks.

The command does not execute P05, populate canonical counterterms, alter any
physics disposition, or authorize Layer 6.
