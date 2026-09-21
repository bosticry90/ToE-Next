# TWO_LOOP_QFT_COMPILER_V1: promotion layer 3 attempt

## Disposition

The requested background-field/physical-vertex gate is not yet complete:

\[
\boxed{\texttt{BACKGROUND\_FIELD\_PHYSICAL\_VERTEX\_LAYER\_BLOCKED}}.
\]

Two bounded prerequisites pass:

\[
\boxed{\texttt{BACKGROUND\_FIELD\_QUADRATIC\_LAYER\_PASS}},\qquad
\boxed{\texttt{PHYSICAL\_VERTEX\_API\_CORE\_PASS}}.
\]

The blocker is no longer field identity, vector masses, Goldstone selection, or
tree-level interaction generation. It is the missing complete
background/quantum partially fixed background-field action and its explicit
general-`xi` one-loop UV-minus-EFT `F^2` cancellation. Two-loop diagram
enumeration remains unauthorized.

The physics status is unchanged:
`DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED`,
`DIRECT_GAUGE_MATCHING_UNRESOLVED`, and `BFB_UNRESOLVED`.

## Immutable inputs

The implementation rejects a mismatched physical basis. Its immutable scalar
basis hash is

```text
af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e
```

Every new artifact records that hash. The quadratic sublayer has hash

```text
b983a8d8dae078761d61c8492ddb583f984398e56483cd306e2382e68ea2e692
```

## Background-field quadratic subpass

[`compile_background_field_quadratic.py`](compile_background_field_quadratic.py)
constructs the complete vacuum-orbit map `Q` in the canonical 328-real basis.
In dimensionless units,

```text
M_V^2/(g10^2 omega^2) = Q^T Q,
M_G^2/(g10^2 omega^2) = xi Q Q^T on image(Q),
M_ghost^2/(g10^2 omega^2) = xi Q^T Q.
```

It finds 12 unbroken SM vectors and 33 massive vectors with nonzero mass
clusters

| `M_V^2/(g10^2 omega^2)` | multiplicity |
|---:|---:|
| `0.005` | 8 |
| `0.025` | 1 |
| `50/120` | 12 |
| `50.6/120` | 12 |

The orbit Goldstone projector agrees with the independently frozen physical
basis to `1.45e-15`. For `xi=1/2,1,2`, all 33 nonzero Goldstone and complex
ghost masses equal `xi M_V^2`; the largest residual is `7.78e-16`.

The independently known vector-index ledgers are recovered:

\[
(T_1,T_2,T_3)_\text{all massive}=(8,6,5),
\]

\[
(T_1,T_2,T_3)_{PS/SM}=(14/5,0,1).
\]

This is a quadratic/operator pass. It is not a loop-level gauge-parameter
cancellation proof.

## Sparse physical-vertex core

[`physical_vertex_api.py`](physical_vertex_api.py) supplies deterministic field
IDs and on-demand kernels for `SSS`, `SSSS`, `VSS`, `VVS`, `VVSS`, pure-gauge
`VVV` structure constants and `VVVV` color channels, plus ghost masses and the
tree FP ghost--ghost--scalar kernel. It uses the factorized physical basis and
never materializes dense `328^3` or `328^4` tensors.

The scalar API evaluates the same parent invariant contractions as the exact
oracle. Because the physical mixing columns are residual-certified floating
algebraic numbers, a narrow serial numeric wrapper relaxes only the oracle's
exact-equality guards. This API is calculation-local and is not advertised as
a thread-safe symbolic database.

[`check_physical_vertex_api.py`](check_physical_vertex_api.py) passes:

- `VSS` antisymmetry and `VVSS` exchange symmetry;
- pure-gauge antisymmetry, Jacobi, and four-vector color-pair symmetry;
- all 33 ghost/vector mass pairings for `xi=1/2,1,2`;
- the tree FP/VVS relation in the frozen normalization;
- physical scalar cubic and quartic permutation symmetry;
- inherited exact scalar controls `zEta=384`, `z6=2`, VEV-induced `zK=6`,
  and `lambdaS^(4)=24`.

All reported core residuals are zero except the numerical Jacobi replay,
`2.35e-31`, and the mass-pairing replay, `4.45e-16`.

## Why the full layer does not pass

The existing one-loop vector authority is the Feynman-gauge result

\[
\lambda_i^V=T_i\left[1-21\log(M_V/\mu)\right].
\]

It is a valid regression in its frozen slice, but it does not show that the
complete matched coefficient is unchanged for `xi=1/2,1,2`. That stronger
claim requires all background/quantum gauge-fixing and ghost vertices and an
explicit UV-minus-EFT hard-region calculation. Equal vector, Goldstone, and
ghost masses and a tree Ward identity are necessary checks, not substitutes.

This caution is structural: the partially fixed background-field construction
was introduced precisely to make loop matching with heavy vectors well-defined
when the ordinary broken-theory BFM does not transparently provide the needed
UV/EFT cancellation; see [Thomsen, *A Partially Fixed Background Field
Gauge*](https://arxiv.org/abs/2404.11640).

The remaining layer-3 requirements are therefore:

1. complete partial-BFM background/quantum gauge-fixed vertices;
2. general-`xi` one-loop UV-minus-EFT `F^2` assembly;
3. explicit vector/Goldstone/ghost cancellation at `xi=1/2,1,2`;
4. selected loop-level Slavnov--Taylor replays in the same prescription.

No diagram count, counterterm layer, master reduction, finite `C1_GS`, or gauge
refit is inferred.

## Frozen closure task

The next calculation is now preregistered in
[`LAYER3_CLOSURE_TASK.md`](LAYER3_CLOSURE_TASK.md). Its machine-readable
[`one_loop_xi_cancellation_matrix.json`](one_loop_xi_cancellation_matrix.json)
contains 12 primary cells: four independently tested vector mass clusters at
`xi=1/2,1,2`. Five aggregate tests cover the degenerate limit, full hard
subtraction and transversality, loop-level ST replay, and the independent
Feynman-gauge comparator. The canonical matrix hash is

```text
46b3bc390967eb256a83f4bb5b20bc46cd7f11f788f59a0ce047e48669294d96
```

The matrix requires clusterwise cancellation; agreement only after summing
different masses cannot pass. This preregistration changes no compiler or
physics disposition.

## Reproduction

From the repository root:

```powershell
python tools/two_loop_qft_compiler_v1/compile_background_field_quadratic.py
python tools/two_loop_qft_compiler_v1/physical_vertex_api.py
python tools/two_loop_qft_compiler_v1/check_physical_vertex_api.py
python calculations/canonical_so10_lower_f2/check_vector_f2.py
python tools/two_loop_qft_compiler_v1/audit_layer3_gate.py
```

The machine-readable outputs are
[`background_field_quadratic.json`](background_field_quadratic.json),
[`physical_vertex_api.json`](physical_vertex_api.json),
[`physical_vertex_api_regression.json`](physical_vertex_api_regression.json),
and [`compiler_status.json`](compiler_status.json).
