# Exact UVP_P05 execution command

## Frozen Codex instruction

> Execute only `UVP_P05` under the unchanged Layer-5A contract-v2 and frozen
> execution plan. Preserve P01--P04 evidence unchanged. Generate rank-four and
> rank-six isotropic tensors with exact d-dimensional denominators, replay the
> pairing sets and coefficients independently through Gaussian moments, test
> every required permutation, and recursively contract rank six through rank
> four and rank two to the scalar moment. Advance only to P06 on exact pass.

## Reproduction command

Run from the repository root while P05 is the authorized cursor:

```powershell
python tools/two_loop_qft_compiler_v1/execute_uvp_p05_primary.py
python tools/two_loop_qft_compiler_v1/independent_uvp_p05_replay.py
python tools/two_loop_qft_compiler_v1/adjudicate_uvp_p05.py
python tools/two_loop_qft_compiler_v1/audit_uvp_p05.py
python tools/two_loop_qft_compiler_v1/audit_uv_pole_execution_plan.py
```

The primary uses recursive perfect matchings. The replay instead forms
pairings from the full permutation orbit and obtains coefficients from
Schwinger/Gaussian moments. The adjudicator compares denominators by exact
symbolic equivalence rather than representation-dependent factor strings,
freezes both artifacts, preserves P01--P04, and advances only to P06 after all
pairing, symmetry, contraction, and adversarial checks pass.

The command does not execute P06, populate canonical counterterms, alter any
physics disposition, or authorize Layer 6.
