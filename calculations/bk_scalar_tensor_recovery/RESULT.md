# Babu--Khan scalar tensor recovery: normalization gate and analytic constraints

## Disposition

**`TENSOR_NORMALIZATION_BLOCKED`** for the *complete* parent-potential-to-doublet/triplet Hessian. **No new scalar benchmark was searched for or promoted.** This is a source/convention block, not a proof that the published doublet matrix is wrong or that the model has no viable scalar point. The two earlier BNV recovery passes do not depend on this scalar kernel and are unchanged.

The immediate falsifier is already upstream of the disputed doublet matrix: the [Babu--Khan v2 potential, Eq. (24)](https://arxiv.org/pdf/1507.06712v2) and its printed vacuum evaluation, Eq. (27), cannot be made consistent by *one* normalization of the `126_H` singlet when their identically named coefficients are read literally. Under ordinary all-index Einstein summation, let

```text
N = (1/5!) Sigma_ijklm Sigma*_ijklm = q sigma².

Eq. (24) quadratic 126 term:  -nu² N/2       = -q nu² sigma²/2
Eq. (24) lambda0 term:       +lambda0 N²/4  = +q² lambda0 sigma⁴/4

Eq. (27), as printed:         -nu² sigma²/2 + lambda0 sigma⁴ + ...
```

The quadratic coefficient requires `q=1`; the quartic coefficient requires `q=2`. This contradiction does **not** depend on the detailed embedding of the `126` doublet. It may reflect a printed factorial, a silent coupling redefinition, or a nonstandard contraction convention; the current evidence does not choose among them. Accordingly, neither Eq. (24) nor Eq. (30) was silently repaired or declared authoritative.

## Independent tensor work earned here

The calculation did not stop at reading the source. Starting from the parent ten-dimensional tensors and the [source's vevs, Eq. (26)](https://arxiv.org/html/1507.06712v2), it reconstructed these limited pieces without using the printed mass matrices as input:

- For the traceless real `54_H`, `Phi = omega_s diag(-2/5 I_6, +3/5 I_4)`, so `tr Phi² = 12 omega_s²/5`, `tr Phi³ = 12 omega_s³/25`, and `tr Phi⁴ = 84 omega_s⁴/125`. The first three `10_H` bidoublet Hessian factors follow: `+3 xi3 omega_s/5`, `+6 eta0 omega_s²/5`, and `+9 eta2 omega_s²/25`. The color-vector counterparts are `-2/5`, `6/5`, and `4/25`. These agree with the corresponding *parts* of the printed `A1/B1/A2/B2` expressions.
- For the `126_H` singlet, the self-dual five-form `Sigma_0 = [sigma/(4 sqrt(2))] wedge_{k=1}^5(e_{2k}+i e_{2k-1})` has precisely the printed `246810` component, 32 equal-magnitude independent antisymmetric entries, `N=sigma²`, and Hodge eigenvalue `+i` in the chosen orientation. Its `1/4!` conjugate contraction is a rank-five projector times `sigma²`; the two `gamma` terms therefore give complementary `0` and `gamma sigma²` contributions on the `10_H` bidoublet. This confirms the magnitude of those entries, not yet which named source field is `A2` or `B2` after all phase conventions.
- A canonical `SO(4)` vector-to-bidoublet decomposition gives `sum_{i=7}^{10} phi_i phi_i = 2 h_u^T epsilon h_d`; with `<S>=v_s/sqrt(2)`, the `chi6` mixing magnitude is `sqrt(2) chi6 v_s` (sign depends on the displayed doublet orientation). This independently recovers another magnitude in the printed matrix.

The same exact `126` singlet construction gives `+6 alpha omega_s² sigma²/5` and `-6 beta omega_s² sigma²/5` from the *literal* Eq. (24) contractions, while Eq. (27) prints `+3/5` and `-3/5`. These are secondary normalization warnings. The `nu²`/`lambda0` contradiction above is the cleanest because it needs no `54` embedding or mixed-index contraction.

The source [Aulakh--Girdhar tensor decomposition](https://arxiv.org/html/hep-ph/0204097v4) confirms that `126`/`bar126` orientation and `(15,2,2)` D-parity signs are nontrivial. Its supersymmetric potential is not a replacement for this non-supersymmetric Babu--Khan potential. We have **not** built and normalized the full `(15,2,2)` fluctuation basis nor evaluated the `lambda2`, `lambda4`, `lambda4'`, `chi4`, and `eta1` Hessian contractions. Thus the decisive published factors `8`, `4`, `2 sqrt(2)` for `chi4`, and `4 sqrt(3)` for `eta1` remain **unconfirmed**.

## Exact one-light/positive-heavy condition

Independently of the origin of its entries, any real sparse matrix with the printed doublet pattern can be written

```text
    [ a  b  0  c ]
D = [ b  d  0  0 ]
    [ 0  0  e  f ]
    [ c  0  f  g ].
```

On the generic mixed branch (`b,c,f != 0`), define `A = a-b²/d` and `S = g-f²/e-c²/A`. A congruence/Schur decomposition makes `D` equivalent in inertia to `diag(d,e,A,S)`. Therefore **exactly one zero and three positive eigenvalues** hold iff

```text
d > 0,   e > 0,   A > 0,   S = 0.
```

Equivalently, `ad>b²` and `g=f²/e+c²/A`; in particular `a>0`, `g>0`, and neither mixing term may be hidden in a negative diagonal. With the light-vector last component set to one,

```text
v_light = (-c/A, bc/(dA), -f/e, 1),
r = -f/e,       r s = -d/b,       s = de/(bf).
```

Thus for the source's positive `r,s` convention one needs `b<0` and `f<0`. These are **point-rejection constraints**, not proof that a potential realizing such a matrix exists. If the printed entries are provisionally used, `d>0` and `a>0` impose inequalities on the displayed `lambda2,lambda4,lambda4',beta` combinations, and the previously found negative Table-2 `a=D11` fails immediately. Exceptional zero-mixing branches need separate treatment and are outside this claimed equivalence.

## Verification and authority ceiling

| Gate | Result |
|---|---|
| `54_H` parent tensor and part of `10_H` Hessian | **PASS**, exact |
| `126_H` singlet normalization, duality, and `gamma` projector | **PASS**, exact in stated orientation |
| Eq. (24) to Eq. (27) same-symbol normalization | **FAIL under literal all-index convention**; source convention/redefinition unresolved |
| Generic doublet one-zero/three-positive criterion | **PASS**, exact on mixed branch |
| All `126_H` doublet/triplet tensor Clebsches | **NOT EARNED** |
| Full published doublet matrix | **UNRESOLVED**, neither confirmed nor refuted |
| Fresh scalar benchmark and threshold consistency | **NOT STARTED** after normalization stop |

Python/SymPy reconstructs the self-dual five-form, all 10D contractions used above, the `54` traces, the `chi6` invariant, and the exact Schur identities. Julia/Nemo independently replays the exact normalization contradiction, `54` traces, beta weighting, and a nondegenerate one-light-mode witness. Run from the repository root:

```powershell
python calculations/bk_scalar_tensor_recovery/verify_partial_tensor_and_positivity.py
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no --project=tools/julia calculations/bk_scalar_tensor_recovery/verify_independent.jl
```

The next scientific step is to settle a *single explicit* parent-potential parameter/kinetic convention that reconciles Eqs. (24), (26), and (27), including whether any coefficients were silently redefined. Only then should the normalized `(15,2,2)` and color-triplet tensor Hessians be completed and a new scalar-point search admitted. No flavor RGE, fermion fit, or below-`M_I` running was done here.
