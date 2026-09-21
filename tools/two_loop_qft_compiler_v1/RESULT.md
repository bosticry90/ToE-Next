# TWO_LOOP_QFT_COMPILER_V1: promotion layer 3

## Disposition

The frozen layer-3 closure matrix passes:

\[
\boxed{\texttt{BACKGROUND\_FIELD\_PHYSICAL\_VERTEX\_LAYER\_PASS}}.
\]

All twelve cluster/`xi` cells and all five aggregate checks pass exactly, and an
independent replay reproduces zero symbolic residual. Promotion layer 4,
automatic two-loop diagram enumeration, is now authorized but was not started.

This is an infrastructure promotion. The finite two-loop `C1_GS` remains
uncomputed, so `DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED`,
`DIRECT_GAUGE_MATCHING_UNRESOLVED`, and `BFB_UNRESOLVED` remain unchanged.

## Frozen inputs

The execution used the preregistered matrix without modification:

```text
physical basis
af6354e26e27d47d1de9439b1336361b0a288d68f5e35a21f58ce87010c3b57e

quadratic layer
b983a8d8dae078761d61c8492ddb583f984398e56483cd306e2382e68ea2e692

one-loop xi matrix
46b3bc390967eb256a83f4bb5b20bc46cd7f11f788f59a0ce047e48669294d96
```

The complete action manifest has SHA-256

```text
2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491
```

and the primary 12-cell result has SHA-256

```text
98d1179a02e7dc954aee49467a43e0aa6e8457b6165f04476df6a2629d3405e4
```

## Complete partial-BFM action

[`partial_bfm_action.py`](partial_bfm_action.py) is now the gauge-fixed
authority façade. The earlier [`physical_vertex_api.py`](physical_vertex_api.py)
is retained as its invariant-parent backend; future diagram code must not add a
parallel gauge-fixing convention.

The UV action is represented in complete index form as

\[
S_{\rm UV}^{\rm all}=S_{\rm parent}+S_{\rm fix}^{H}
+S_{\rm fix}^{G/H},
\]

with the ordinary background-field gauge for the unbroken SM group and the
equivariant partial fixing for the 33 heavy directions. The corresponding SM
EFT uses the identical `H`-background gauge action. The heavy condition is

\[
G^i=d^\mu V^i_\mu-\xi M_i\chi^i.
\]

The action contains the heavy-vector fixing, the light and heavy FP sectors,
all background/quantum distinctions used by the one-loop operator, and the
equivariant quartic heavy-ghost term

\[
\frac{\xi}{2}f^i{}_{j\alpha}f^k{}_{\ell\alpha}
\bar u_i u^j\bar u_k u^\ell.
\]

That quartic term is required by partial gauge fixing. It first enters diagrams
at two loops when there are no external ghosts, so it does not alter the
one-loop `F^2` determinant, but its presence is mandatory before layer 4.

The 33 stored physical Goldstones are bridged to the 33 orbit-aligned
vector partners with orthogonality residual `2.80e-15` and reconstruction
residual `4.45e-16`. The heavy mass operator commutes with the unbroken-SM
action to `2.13e-16`. A nonzero quartic-ghost control and all ghost-mass,
Goldstone, light-ghost, background-vector, and invariant-backend façade
regressions pass.

The formal action follows the partially fixed background-field construction
of [Thomsen](https://arxiv.org/abs/2404.11640) and its equivariant partial
gauge-fixing foundation in [Ferrari](https://arxiv.org/abs/1308.6802). Those
papers define the architecture; all benchmark masses, projectors, generators,
and coefficients here are generated from the canonical model.

## Exact general-`xi` one-loop reduction

On the transverse background-`F^2` projection, the BRST/Ward operator identity

\[
\Delta_\xi^{\mu\nu}D_\nu
=\xi^{-1}D^\mu\Delta_0(\xi M^2)
\]

gives the determinant factorization

\[
\det\Delta_\xi
=\det\Delta_1\,
\frac{\det\Delta_0(\xi M^2)}{\det\Delta_0(M^2)}.
\]

This makes the longitudinal-vector contribution an exact scalar-determinant
ratio. In the matching normalization of the project, with
`L=log(M^2/mu^2)`, the separately retained pieces per cluster index `T_i` are

| sector | heat-kernel pole | coefficient of `L` in `lambda_i` | finite at `L=0` |
|---|---:|---:|---:|
| massive vector | `-5 T_i/6` | `-10 T_i` | `T_i[1+log(xi)/2]` |
| Goldstone | `T_i/24` | `T_i/2` | `T_i log(xi)/2` |
| complex ghost | `-T_i/12` | `-T_i` | `-T_i log(xi)` |
| EFT hard subtraction | `0` | `0` | `0` |
| **matched** | **`-7 T_i/8`** | **`-21 T_i/2`** | **`T_i`** |

Thus every `log(xi)` cancels before different mass clusters are summed, and

\[
\lambda_i^{(c)}=T_i^{(c)}
\left[1-21\log\left(\frac{M_c}{\mu}\right)\right],
\qquad
\Delta b_i^{(c)}=-\frac72T_i^{(c)}.
\]

The matching-scale identity

\[
\frac{d\lambda_i^{(c)}}{d\log\mu}+6\Delta b_i^{(c)}=0
\]

holds exactly.

## Twelve primary cells

[`compute_one_loop_xi_cancellation.py`](compute_one_loop_xi_cancellation.py)
executes the immutable Cartesian product:

| cluster | `M_V^2/(g10^2 omega^2)` | real vectors | `(T1,T2,T3)` | tested `xi` |
|---|---:|---:|---:|---:|
| lower charged | `1/200` | 8 | `(14/5,0,1)` | `1/2,1,2` |
| lower neutral | `1/40` | 1 | `(0,0,0)` | `1/2,1,2` |
| upper A | `5/12` | 12 | `(5,3,2)` | `1/2,1,2` |
| upper B | `253/600` | 12 | `(1/5,3,2)` | `1/2,1,2` |

Every cell stores vector, Goldstone, ghost, and EFT terms separately through
pole, logarithmic, and finite order. Each cluster is independently
`xi`-independent. The neutral cluster is exactly zero in all three SM channels.

## Aggregate and independent checks

All five preregistered aggregate tests pass:

1. the exact sum of all cluster thresholds;
2. the degenerate limit with total index `(8,6,5)`;
3. identical light `H`-BFM actions in UV/EFT, giving soft cancellation, no
   unmatched IR pole, and a transverse background `F^2` result;
4. the longitudinal determinant Ward/ST identity above;
5. exact recovery of the independent `xi=1` heat-kernel coefficient
   `-7/8-epsilon/12` and `T_i[1-21 log(M/mu)]`.

[`independent_one_loop_xi_replay.py`](independent_one_loop_xi_replay.py)
imports neither the action compiler nor the primary one-loop assembler. It
reconstructs all component coefficients and all 12 matched cells from the
frozen JSON artifacts. Its maximum symbolic residual is exactly zero.

## Authority boundary

Layer 3 now certifies the field identities, masses, complete partial-BFM action,
Goldstone and ghost disposition, background covariance, clusterwise
gauge-parameter cancellation, vector beta jump, hard subtraction, and
one-loop vector finite coefficient.

This authority is restricted to the preregistered transverse,
dimension-four background `F^2` coefficient. It does not assert that arbitrary
off-shell Wilson coefficients or individual sector contributions are
`xi`-independent.

It does not calculate any two-loop diagram, counterterm, integral reduction,
master integral, or finite `C1_GS`. Authorization of layer 4 is not evidence
that those later layers will pass.

## Reproduction

From the repository root:

```powershell
python tools/two_loop_qft_compiler_v1/physical_vertex_api.py
python tools/two_loop_qft_compiler_v1/partial_bfm_action.py
python tools/two_loop_qft_compiler_v1/check_partial_bfm_action.py
python tools/two_loop_qft_compiler_v1/compute_one_loop_xi_cancellation.py
python tools/two_loop_qft_compiler_v1/independent_one_loop_xi_replay.py
python tools/two_loop_qft_compiler_v1/audit_layer3_gate.py
```

The detailed cells are in
[`one_loop_xi_cancellation_results.json`](one_loop_xi_cancellation_results.json),
and the promoted machine state is in
[`compiler_status.json`](compiler_status.json).
