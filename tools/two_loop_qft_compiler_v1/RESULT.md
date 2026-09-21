# TWO_LOOP_QFT_COMPILER_V1: promotion layer 2

## Disposition

The complete parent-to-physical scalar basis now passes:

\[
\boxed{\texttt{CANONICAL\_328\_PHYSICAL\_BASIS\_PASS}}.
\]

This is an infrastructure result, not a finite two-loop threshold. The physics
status remains `DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED`,
`DIRECT_GAUGE_MATCHING_UNRESOLVED`, and `BFB_UNRESOLVED`. Background-field
gauge fixing, bulk vertex generation, diagrams, counterterms, reduction, and
master-integral evaluation were not started.

## Exact all-weight layer

[`compile_all_weight_basis.py`](compile_all_weight_basis.py) expands the 65
certified highest-weight copies in 35 SM-irrep classes into every weight state.
The lowering order and phase convention are deterministic. Equivalent copies
of each irrep have exactly identical raising/lowering representation matrices,
so one small multiplicity rotation can be replicated across the whole irrep.

The resulting real map has 328 exactly orthonormal columns and full exact rank.
Its sparse serialization has SHA-256

```text
5c37fb29bcbc9418b44c2d87e42416c58a6612b08b039bd52aa1a3407c0d00e1
```

## Physical mass and special-zero layer

[`materialize_physical_basis.py`](materialize_physical_basis.py) applies only
the already-certified small multiplicity Hessian blocks. It explicitly bridges
the phase convention of the rational block representatives to the all-weight
convention; the first attempted replay exposed this required bridge by failing
the Goldstone-nullspace test, and no result was promoted until it was inserted.

The special directions are not assigned by a generic eigensolver:

- 33 gauge Goldstones are constructed from the broken-generator vacuum orbit;
- the PQ mode is constructed from the PQ charge orbit;
- the remaining four null directions, after projection away from those 34
  symmetry directions, form the tuned complex Higgs doublet.

The final disposition is exactly

| Direction class | Real dimension |
|---|---:|
| positive heavy physical scalars | 290 |
| gauge Goldstones | 33 |
| PQ mode | 1 |
| light Higgs | 4 |
| **total** | **328** |

The principal residual certificates are

```text
max kinetic orthogonality residual   1.1102230246251565e-15
max Hessian round-trip residual      5.329070518200751e-15
max independent zero-subspace error  8.881784197001252e-16
```

The reproducible factorized physical-basis authority hash is

```text
af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e
```

It covers the exact all-weight hash, the small multiplicity rotations, the
explicit special-zero columns, and the heavy spectrum. A dense float17 hash is
retained only as a same-run diagnostic because reapplying serialized rotations
can change last-bit rounding without changing the certified basis.

## Gauge-generator regression

The unbroken color, weak, and hypercharge Cartan generators were transformed
through the physical map. Restricting them to the 290 heavy directions
reproduces the previously independent scalar one-loop beta-index ledger:

\[
(T_1,T_2,T_3)=\left(\frac{377}{30},\frac{77}{6},\frac{79}{6}\right).
\]

This tests the physical basis as a gauge-interaction basis, rather than only a
mass diagonalization.

## Independent replay

[`independent_physical_basis_replay.py`](independent_physical_basis_replay.py)
does not import the materializer. It reconstructs the 328 columns from the
saved factorization, checks the authority hash, full rank, orthogonality,
special-zero subspace, Hessian round trip, disposition, and heavy-scalar index
target. [`audit_physical_basis_gate.py`](audit_physical_basis_gate.py) then
freezes the promotion status in [`compiler_status.json`](compiler_status.json).

## Authority boundary

The compiler now knows which physical scalar, Goldstone, PQ, or light-Higgs
direction every future scalar line denotes. It does **not** yet possess the
background-field gauge/ghost action or a promoted physical vertex database.
Those belong to promotion layer 3 and require a separate gate. No finite
`C1_GS` or gauge refit is inferred here.

## Reproduction

```powershell
python tools/two_loop_qft_compiler_v1/compile_all_weight_basis.py
python tools/two_loop_qft_compiler_v1/materialize_physical_basis.py
python tools/two_loop_qft_compiler_v1/independent_physical_basis_replay.py
python tools/two_loop_qft_compiler_v1/audit_physical_basis_gate.py
```

The stored maps are [`sm_weight_basis.json`](sm_weight_basis.json) and
[`physical_basis.json`](physical_basis.json).
