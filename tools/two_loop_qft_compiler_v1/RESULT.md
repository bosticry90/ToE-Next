# TWO_LOOP_QFT_COMPILER_V1: first execution checkpoint

## Disposition

The infrastructure program is admitted with the already frozen scientific
target `C1_GS`.  Its first component-basis layer passes:

\[
\boxed{\texttt{CANONICAL\_328\_REAL\_COMPONENT\_BASIS\_PASS}}.
\]

The complete physical vertex layer does not yet pass:

\[
\boxed{\texttt{PHYSICAL\_VERTEX\_MATERIALIZATION\_BLOCKED}}.
\]

Accordingly the physics status remains
`DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED` and
`DIRECT_GAUGE_MATCHING_UNRESOLVED`.  The passed scalar vertex oracle and all
lower-order gauge results are preserved; `BFB_UNRESOLVED` is unchanged.

## Exact field-space layer now earned

[`compile_real_field_basis.py`](compile_real_field_basis.py) constructs the
parent scalar tangent space directly from the frozen kinetic convention:

| Parent sector | Real directions |
|---|---:|
| real traceless symmetric `54_H` | 54 |
| complex self-dual `126_H` | 252 |
| complex vector `10_H` | 20 |
| complex singlet | 2 |
| **Total** | **328** |

The basis is canonical for

\[
\mathcal L_{\rm kin}=\frac12G_{AB}\,\partial q_A\partial q_B.
\]

All `66,824` within-parent-sector Gram entries were checked exactly; all
cross-sector entries vanish structurally.  The complete 328-vector sparse
serialization has SHA-256

```text
c66398b6321988b643af5c12fdbea86c3a2589b7b139450770c6ef72c31a3b5e
```

The same layer constructs all 45 plane-rotation generators in the previously
used normalization

\[
\operatorname{Tr}_{10}(T_a^T T_b)=\delta_{ab}.
\]

An independently written sparse-coordinate replay checks the full
`328 x 328` real Gram matrix (`107,584` entries) and the 45-generator
normalization without importing the parent kinetic-inner implementation.  A
separate gate audit confirms that the existing 65 highest-weight
multiplicity representatives in 35 SM-irrep classes reconstruct dimension
328, while also demonstrating why those representatives are not yet a full
interaction basis.

## First unearned object

This component basis is not yet the requested **physical** basis.  The current
Hessian infrastructure contains 65 normalized highest-weight representatives
and complete small multiplicity blocks, which is sufficient for spectra and
rank.  It does not yet provide one complete 328-component transformation that
simultaneously:

1. expands every state of every SM multiplet, not only one highest weight;
2. rotates every multiplicity space into the physical mass basis;
3. isolates the 33 gauge Goldstones, one PQ mode and four light-Higgs real
   directions exactly once;
4. returns the 290 positive heavy scalar columns with a certified inverse;
5. exposes gauge-generator matrices and parent vertices in that basis.

Without that transformation, generating a subset of mass-basis cubic or
quartic rules would be incomplete and could not support diagram enumeration.
The program therefore stops at this fail-fast boundary rather than advancing
to background-field gauge fixing prematurely.

## Next compiler-only target

The next layer is a complete SM-irrep state compiler: generate all weights from
each certified highest-weight copy, assemble the exact parent-to-irrep map,
diagonalize only the small multiplicity matrices at the frozen point, and
materialize the resulting real 328-component parent-to-physical matrix.  Its
acceptance tests are exact kinetic unitarity, Hessian reconstruction, the
`290+38` disposition, conjugate-irrep consistency, and recovery of every
passed block eigenvalue.

No background-field vertices, diagrams, counterterms, master integrals, or
finite `C1_GS` are promoted before this layer passes.

## Reproduction

```powershell
python tools/two_loop_qft_compiler_v1/compile_real_field_basis.py
python tools/two_loop_qft_compiler_v1/independent_basis_replay.py
python tools/two_loop_qft_compiler_v1/audit_physical_basis_gate.py
```

The complete basis is stored in
[`real_field_basis.json`](real_field_basis.json); the current promotion status
is in [`compiler_status.json`](compiler_status.json).
