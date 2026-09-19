# Babu–Khan heavy-vector BNV matching result

## Disposition

```text
CALCULATION: BK_SO10_HEAVY_VECTOR_PS_TO_D6_BNV_SMEFT_TREE_MATCHING_V1
RESULT: PASS
AUTHORITY: TREE_LEVEL_WEAK_BASIS_OPERATOR_MAP_ONLY
DOWNSTREAM: AUTHORIZED_FOR_SEPARATE_ADMISSION
```

The four gauge-mediated current-current operators in Babu and Khan Eq. (61) have a complete tree-level map into the standard dimension-six BNV SMEFT basis plus the required right-handed-neutrino extension. The calculation did not perform Pati–Salam running, matching at the right-handed-neutrino threshold, SMEFT or LEFT running, hadronic matching, or a proton-lifetime calculation.

The result is a controlled operator boundary for this frozen source model. It is not evidence that the Babu–Khan model, SO(10), grand unification, or any Theory of Everything is viable.

## Frozen sources

- K. S. Babu and S. Khan, [arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2), Eqs. (61)–(64), with the gauge-vector masses in Sec. 6.2.
- S. Banik, A. Crivellin, L. Naterop, and P. Stoffer, [arXiv:2510.08682v2](https://arxiv.org/abs/2510.08682v2), Table 1.
- R. Alonso et al., [arXiv:1405.0486v2](https://arxiv.org/abs/1405.0486v2), Eqs. (1), (2), and (9), for the right-handed-neutrino extension and flavor symmetries.
- P. Nath and P. Fileviez Pérez, [arXiv:hep-ph/0601023v3](https://arxiv.org/abs/hep-ph/0601023v3), Eqs. (12)–(27), as the source cited by Babu and Khan for the current-current and physical-basis forms.

No legacy source, code, environment, or runtime path was used. D: was absent throughout execution.

## Legacy-method disposition

The verified SU(5) relevance audit contributed only methods that transfer across gauge-mediated BNV calculations: freeze the operator basis before algebra, preserve mediator-resolved coefficients, make epsilon and charge-conjugation signs executable, separate threshold assumptions from exact identities, and require an independent exact replay. Those controls were reimplemented here from primary sources. No SU(5) coefficient, model conclusion, code, packet, or generated output was imported.

## Conventions

The calculation fixes:

```text
metric                 eta = diag(+1,-1,-1,-1)
charge conjugation     C = i gamma^2 gamma^0
color epsilon          epsilon_123 = +1
weak epsilon           epsilon_12 = +1
Q_L                    (u_L,d_L)
L_L                    (nu_L,e_L)
```

Babu–Khan Eq. (61) is taken with the displayed Lagrangian sign. In the chiral representation the required two-component identity is

```text
(xi† barsigma^mu chi)(eta† barsigma_mu rho)
    = -2 (xi† eta†)(chi rho).
```

The explicit-component replay constructs the charge-conjugation matrix and both sides from the stated gamma convention; the factor and sign are not inserted as an expected output.

## Heavy-vector and Pati–Salam boundary

One fermion family decomposes as

```text
16_F = (4,2,1) + (4bar,1,2),
```

and the SO(10)/Pati–Salam broken-vector sector is `(6,2,2)`. Write `A,B` for SU(4) indices, `a,b` for SU(2)L indices, and `alpha,beta` for SU(2)R indices. The relevant antisymmetric current and interaction can be represented as

```text
J_mu^[AB]a alpha
  = (F_R dagger)^[A alpha] barsigma_mu F_L^[B]a
    - (F_R dagger)^[B alpha] barsigma_mu F_L^[A]a

L_int = (g_U/sqrt(2)) V_mu,[AB]a alpha J^mu,[AB]a alpha + h.c.
```

with the component-vertex normalization fixed by Babu–Khan Eq. (61). Contracting two currents gives the Pati–Salam singlet boundary

```text
O_PS = k_PS^2 epsilon_ABCD epsilon_ab epsilon_alpha_beta
       J_mu^[AB]a alpha J^mu,[CD]b beta + h.c.
```

In the component-vertex normalization fixed above, its Standard-Model expansion is the four-term source boundary in Babu–Khan Eq. (61); the executable replay below verifies the relative signs and Fierz factors rather than presuming them.

The exact mass information requires a two-stage interpretation. With the Pati–Salam-breaking vev turned off,

```text
M_XY^2 = M_XpYp^2 = g_U^2 omega_s^2
k_PS^2 = 1/(2 omega_s^2).
```

This is the unique Pati–Salam-covariant dimension-six coefficient above `M_I`. After the `126_H` vev `sigma` breaks Pati–Salam, the vector inverse-mass operator becomes

```text
M_V^-2 = [1/(g_U^2 omega_s^2)] P_XY
       + [1/(g_U^2 (omega_s^2+sigma^2))] P_XpYp,
```

so the broken-phase pole coefficients are

```text
k1^2 = g_U^2/(2 M_XY^2)     = 1/(2 omega_s^2),
k2^2 = g_U^2/(2 M_XpYp^2)   = 1/[2(omega_s^2+sigma^2)].
```

This is the controlling threshold qualification: `k1^2` and `k2^2` must not be treated as two independent Pati–Salam-covariant Wilson coefficients above `M_I`. Their difference is a Pati–Salam-breaking threshold projection. In the `sigma -> 0` limit both reduce to `k_PS^2`. This calculation applies the projection algebraically but does not run either coefficient.

## Operator map

Using the destination definitions

```text
Q_duql = epsilon_color epsilon_weak (d^T C u)(q^T C l)
Q_qque = epsilon_color epsilon_weak (q^T C q)(u^T C e)
Q_qqql = epsilon_color epsilon_weak epsilon_weak (q^T C q)(q^T C l)
Q_duue = epsilon_color (d^T C u)(u^T C e),
```

and the neutrino-extended operator

```text
Q_qqdN = epsilon_color epsilon_weak (q^T C q)(d^T C N),
```

the source terms map as

| Babu–Khan term | Mediator | Exact map |
|---|---|---|
| `O_I` | `(X,Y)` | `+2 k1^2 Q_qque` with source flavor wiring |
| `O_II` | `(X,Y)` | `+2 k1^2 Q_duql` with source flavor wiring |
| `O_III` | `(X',Y')` | `+2 k2^2 Q_duql` with the alternate source wiring |
| `O_IV` | `(X',Y')` | `-2 k2^2 Q_qqdN` with source flavor wiring |

For weak-basis flavor indices `p,r,s,t`, the nonredundant coefficient tensors are

```text
C_qque[p,r,s,t]
  = k1^2 (delta[p,s] delta[r,t] + delta[r,s] delta[p,t])

C_duql[p,r,s,t]
  = 2 k1^2 delta[r,s] delta[p,t]
  + 2 k2^2 delta[p,s] delta[r,t]

C_qqdN[p,r,s,t]
  = -k2^2 (delta[p,s] delta[r,t] + delta[r,s] delta[p,t]).
```

At this tree-level gauge boundary,

```text
C_qqql = C_duue = C_uddN = 0.
```

The symmetrized `qque` and `qqdN` tensors implement the published identities `Q_qque[p,r,s,t] = Q_qque[r,p,s,t]` and `Q_qqdN[p,r,s,t] = Q_qqdN[r,p,s,t]`. The unsymmetrized source sums and these nonredundant tensors give the same Lagrangian.

The `Q_qqdN` term is not forced into the four-operator standard SMEFT. It remains in SMEFT plus singlet neutrinos until a separately specified `N`-threshold match. No `N` term was discarded.

## Physical-basis comparator

The weak-to-mass-basis rotations reproduce the matrix products in Babu–Khan Eqs. (62)–(64). The exact identities used are

```text
Uc† D = V1 VUD
Ec† U = V2 VUD†
Dc† U = V4 VUD†
Uc† E = V1 VUD V4† V3
Dc† N = V3 VEN
Uc† N = V1 VUD V4† V3 VEN
Nc† D = UEN† V2
Nc† U = UEN† V2 VUD†.
```

Substitution into the four weak-basis source terms yields the two `k1^2` structures in `c(e^C,d)`, the `k1^2+k2^2` structures in `c(e,d^C)` and `c(nu,d,d^C)`, and the two `k2^2` structures in `c(nu^C,d,d^C)`. The replay verifies these identities for independently generated unitary matrices without importing a numerical Yukawa fit.

## Adversarial checks

| Check | Result |
|---|---|
| SM gauge invariance and hypercharge sum for every destination operator | `PASS` |
| Operator mass dimension and coefficient dimension | `PASS` |
| Color and weak epsilon signs | `PASS` |
| Charge-conjugation/Fierz factor and relative signs | `PASS` |
| `qque` and `qqdN` flavor symmetry | `PASS` |
| Independent mediator decoupling | `PASS` |
| Equal-mass limit derived rather than assumed | `PASS` |
| Right-handed-neutrino sector retained separately | `PASS` |
| Physical-basis rotation identities | `PASS` |
| Primary/independent coefficient-map agreement | `PASS` |

The source paper describes Eq. (61) directly in Standard-Model components rather than printing the compact Pati–Salam current invariant. The bridge above is therefore bounded to the representation, common-coefficient limit, published mass operator, and component expansion needed for this calculation. It does not claim a complete Pati–Salam EFT basis or anomalous-dimension calculation.

## Reproduction

Observed runtimes:

```text
Python 3.10.11
SymPy 1.14.0
NumPy 2.2.6
Cadabra 2.5.14
Julia 1.12.6
Nemo 0.56.1
```

Run from the repository root:

```powershell
& 'C:\Program Files\Python310\python.exe' calculations\bk_so10_bnv_matching\verify_map.py

$cadabraRoot = Join-Path $env:LOCALAPPDATA 'Programs\Cadabra'
$env:PYTHONPATH = $cadabraRoot
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $cadabraRoot
& .\cadabra2-cli.exe 'C:\Users\psboy\Documents\ToE-Next\calculations\bk_so10_bnv_matching\primary_map.cdb'
Pop-Location

$env:JULIA_PKG_OFFLINE = 'true'
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" `
  --startup-file=no `
  --project=tools\julia `
  calculations\bk_so10_bnv_matching\verify_map.jl
```

Expected terminal lines are:

```text
PASS: explicit Grassmann, flavor, gauge, dimension, and rotation checks
PASS: Cadabra color/weak epsilon sign checks
PASS: Nemo coefficient symmetry, decoupling, and PS-limit checks
```

SHA-256:

```text
verify_map.py    b9d4d16415fbe505d2b13a4e150b57ca147861ff4f340e989f553fd360bcca83
primary_map.cdb  d5e293281a39db514a0655f84826aaa469210ee1ac4cfd73030b9ca59c41a376
verify_map.jl    9428e6d8f2810b018cf8fb41a245edf2a7beccbde1f5355c6888257ab19d3a09
coefficient_map.json  7f17bef72aa3a02691e5091123dad21ebcd4d3680aeefc77c87cb8cea1be8775
```

## Carry-forward decision

A separate Pati–Salam-running and `M_I` threshold-matching calculation may now be considered for admission. It must start from the single Pati–Salam-covariant coefficient, define the required Pati–Salam operator basis and anomalous dimensions, and introduce the unequal pole coefficients only through the symmetry-breaking threshold projector.

No downstream calculation is activated by this result.
