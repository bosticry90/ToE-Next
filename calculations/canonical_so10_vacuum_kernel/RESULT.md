# Canonical scalar vacuum kernel: bounded analytic result

## Disposition

**`VACUUM_KERNEL_BLOCKED` for the full requested authority.** The exact
action-derived vacuum restriction, all singlet tadpoles, intended connected
stabilizers, gauge-orbit counts, singlet-radial Hessian, and the quadratic
block on the specified color-singlet electroweak-doublet subspace have passed the checks
below. The **full colored-scalar Hessian** and an explicit full-matrix
Goldstone-nullity replay have **not** been derived. Thus
`CANONICAL_VACUUM_KERNEL_PASS`, a scalar benchmark, and a one-light-Higgs
claim are not earned. This is a calculation boundary, **not** an inconsistency
or no-go for the canonical theory.

Only [parent action v1](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md)
(SHA-256 `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`)
is scalar authority. No printed Babu–Khan vacuum equation, doublet matrix,
real-`r,s` rule, or scalar threshold was imported.

## Vacuum polynomial and stationarity

Use the normalized ansatz in [RECORD.md](RECORD.md), with nonzero
`omega,sigma,v` and `phi_0=0`. Exact evaluation of all 34 action slots gives

```text
p2=omega², p3=omega³/sqrt(60), p4=7 omega⁴/60,
N=sigma², L_PhiSigma=-omega² sigma²/4,
Q0=sigma⁴, Q1=Q2=X131=0,
Phi_ij T_ij=0, E|_(phi=0)=0.
```

The eta invariant's potential `phi` tadpole is exactly zero in every 10
direction. Define `L_Phi=lambdaPhi1+7lambdaPhi2/60` and
`L_mix=lambdaPhiSigma1-lambdaPhiSigma2/4`. Direct assembly from the frozen
invariants, followed by differentiation, yields

```text
V0 = mPhi2 omega² + mSigma2 sigma² + (mS2/2) v²
   + (muPhi/sqrt(60)) omega³
   + L_Phi omega⁴ + L_mix omega² sigma²
   + (lambdaPhiS/2) omega² v² + lambdaSigma1 sigma⁴
   + (lambdaSigmaS/2) sigma² v² + (lambdaS/4) v⁴.

0 = (1/omega) dV0/domega
  = 2mPhi2 + 3muPhi omega/sqrt(60) + 4L_Phi omega²
    + 2L_mix sigma² + lambdaPhiS v²;
0 = (1/sigma) dV0/dsigma
  = 2mSigma2 + 2L_mix omega² + 4lambdaSigma1 sigma²
    + lambdaSigmaS v²;
0 = (1/v) dV0/dv
  = mS2 + lambdaPhiS omega² + lambdaSigmaS sigma² + lambdaS v².
```

The VEV polynomial is independent of the three invariant scalar-coupling
phases. The two VEV phases of `Sigma` and `S` can be removed by a broken
gauge phase and PQ, respectively, on this ansatz. Therefore no *spontaneous*
CP phase is forced here. **Generic complex couplings still explicitly break
CP**; a CP-invariant scalar submodel requires the three invariant phase
combinations to be real (`0` or `pi` modulo conventions), an additional
symmetry premise rather than a result of stationarity. No CP statement about
the unfrozen Yukawa sector follows. The exact VEV coefficients were also
replayed independently with Julia index-set arithmetic.

## Symmetry and Goldstone obligations

For the `54` VEV, the exact `so(10)` adjoint orbit rank is 24, leaving
`so(6)+so(4)` of dimension 21. The group stabilizer also has the expected
disconnected `S(O(6)xO(4))` component that supplies the Pati–Salam `D`
representative. The `126` VEV moves under that representative and has rank
9 within the 21-dimensional connected Pati–Salam algebra, leaving a
12-dimensional connected stabilizer. An independent centralizer construction
finds `u(3)+u(2)` of dimension 13, with one VEV phase constraint; the
surviving abelian generator is `2J_c-3J_w`. Thus the local connected algebra
is `su(3)+su(2)+u(1)` and the gauge orbit has **33** independent directions.
Exact fixed-subspace checks give one real SM singlet in the `54`, no singlet
in the complex `10`, and one complex singlet in the self-dual `126` (the last
by a rank-125 finite-field lower bound together with the exact known VEV
kernel). Hence the three displayed radial tadpoles, with their removable
phase partners, cover all gauge-invariant first derivatives on this ansatz.

For a gauge generator with field-space vector `R_a`, gauge invariance gives
`R_a^A partial_A V=0`. Differentiating and imposing *all* tadpoles gives
`H_AB R_a^B=0`. Therefore the complete, as-yet-unmaterialized Hessian must
have **at least the 33 independent gauge-Goldstone zero directions** found
above. With `v != 0`, PQ supplies a further independent global Goldstone
direction. This is an exact Ward-identity obligation, **not** a claim that
the explicit full Hessian has been checked or that it has no additional
flat directions.

## Derived Hessian pieces

Differentiating the same `V0` and eliminating the three quadratic masses
with the nonzero-VEV tadpoles gives the exact singlet-radial Hessian in
`(omega,sigma,v)`:

```text
[ 3muPhi omega/sqrt(60)+8L_Phi omega²,  4L_mix omega sigma,    2lambdaPhiS omega v ]
[ 4L_mix omega sigma,                  8lambdaSigma1 sigma²,  2lambdaSigmaS sigma v]
[ 2lambdaPhiS omega v,                 2lambdaSigmaS sigma v, 2lambdaS v²          ].
```

No positivity follows without a parameter point.

The [doublet derivation](derive_doublet_block.py) gives the quadratic form
on the specified color-singlet `(15,2,2)`-`126` and `(1,2,2)`-`10`
subspace, in canonical complex coordinates `x_a,y_a` (`a=6..9`):

```text
V2_doublet = x_a conjugate(x_b) A_ab + y_a conjugate(y_b) B_ab
           + [ x_a x_b C_ab + y_a y_b D_ab + x_a y_b E_ab + h.c. ].
```

For `J=diag([[0,-1],[1,0]],[[0,-1],[1,0]])`, write
`A=A0 I_4+AJ(-iJ)` and `B=B0 I_4+BJ(-iJ)`, where

```text
A0 = 2mSigma2 + 2lambdaPhiSigma1 omega²
   - lambdaPhiSigma2 omega²/12 + 4lambdaSigma1 sigma²
   + 10(lambdaSigma2+lambdaSigma3) sigma² + lambdaSigmaS v²;
AJ = 2(lambdaSigma2+lambdaSigma3+8lambdaSigma4) sigma²;
B0 = mphi2 + (3muPhiPhi omega/sqrt(60))
   + lambdaPhiphi1 omega² + (3lambdaPhiphi2/20) omega²
   + lambdaSigmaphi1 sigma² + (lambdaSigmaphi2/2) sigma²
   + (lambdaVectorS/2) v²;
BJ = (lambdaSigmaphi2/2) sigma².
```

The holomorphic blocks `C,D` are proportional to `I_4`, and

```text
E = 2sqrt(3) zEta sigma² (I_4+iJ),
C = -10 z4 s omega/sqrt(60) I_4,
D = (z6+3zK omega/sqrt(60)) conjugate(s) I_4,
s = v exp(i thetaS)/sqrt(2).
```

The script prints the complete `A,B` coefficient expressions and exact
tensor Gram matrices. It checks Hermiticity of `A,B` and symmetry of `C,D`.
In particular, `zK` contributes directly to the `10` holomorphic bilinear;
the inherited sparse source matrix is not the canonical one. No doublet
eigenvalue, heavy-mode positivity, or light-Higgs projector has been claimed.

## Exact stopping boundary

The remaining work is to derive and independently replay the **full**
real-scalar Hessian, including every colored and other non-singlet block,
and compare its explicit nullspace with the 33 gauge directions plus the
PQ direction. Only then can physical scalar eigenvalues, one-light-doublet
conditions, and a benchmark search be discussed. The present partial
calculation is not a reason to import the source's mass matrix or to tune a
numerical point.

Run from repository root:

```powershell
python calculations/canonical_so10_vacuum_kernel/derive_vacuum.py
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no calculations/canonical_so10_vacuum_kernel/verify_vacuum_replay.jl
python calculations/canonical_so10_vacuum_kernel/derive_stabilizers.py
python calculations/canonical_so10_vacuum_kernel/verify_sm_singlets_modular.py
python calculations/canonical_so10_vacuum_kernel/derive_radial_hessian.py
python calculations/canonical_so10_vacuum_kernel/derive_doublet_block.py
```
