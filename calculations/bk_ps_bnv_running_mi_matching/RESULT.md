# Babu-Khan Pati-Salam running and intermediate matching result

## Disposition

```text
CALCULATION: BK_PS_BNV_GAUGE_LL_RUNNING_AND_MI_TREE_MATCHING_V1
RESULT: PASS
AUTHORITY: ONE_LOOP_GAUGE_LEADING_LOG_PS_RUNNING_AND_TREE_LEVEL_MI_MATCHING_ONLY
DOWNSTREAM: AUTHORIZED_FOR_SEPARATE_ADMISSION
```

The unique Pati-Salam-covariant BNV coefficient can be evolved from `M_U` to
`M_I` with the published one-loop gauge leading-log factor and then projected
at tree level onto the previously established SMEFT and SMEFT-plus-`N`
boundary. The full flavor tensor is multiplied by one universal factor. The
unequal broken-phase pole coefficients are introduced only after that running.

This result does not include Yukawa or scalar operator mixing, finite one-loop
matching, a numerical threshold benchmark, evolution below `M_I`, a
right-handed-neutrino threshold, hadronic matching, or proton lifetimes. It is
not evidence that the Babu-Khan model, SO(10), or any Theory of Everything is
phenomenologically viable.

## Frozen sources and prior boundary

- K. S. Babu and S. Khan,
  [arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2), especially Eqs.
  (1)-(7), (21), and the spectrum in Table 1;
- Y. Mambrini et al.,
  [arXiv:1502.06929v2](https://arxiv.org/abs/1502.06929v2), Appendix D, Eqs.
  (72)-(78), and the gauge beta convention in Eq. (42);
- the completed ToE-Next
  [tree-level operator boundary](../bk_so10_bnv_matching/RESULT.md).

Alonso et al. [arXiv:1405.0486v2](https://arxiv.org/abs/1405.0486v2) and
Datta et al. [arXiv:2010.12109v3](https://arxiv.org/abs/2010.12109v3) remain
downstream SMEFT/SMNEFT comparators. Their anomalous-dimension systems were not
used above `M_I`.

## Execution protocol and acceptance tests

The calculation ran in this order and stopped before any disallowed stage:

1. reconstruct the Pati-Salam one- and two-loop gauge beta ledger directly
   from the Babu-Khan representations;
2. reconstruct the gauge anomalous factors from the current-current Casimir
   factors and compare them with both primary sources;
3. derive the gauge and Wilson-coefficient differential equations and reconcile
   the apparent exponent-sign difference;
4. solve the coefficient RGE exactly at one-loop leading-log order;
5. verify D parity, the unit-running limit, the first logarithmic term, and
   flavor universality;
6. apply the broken-phase pole projector at `M_I` only after the common
   Pati-Salam running;
7. reproduce the complete prior tree-level boundary when the running factor is
   one, retaining `Q_qqdN` in SMEFT plus singlet neutrinos;
8. replay the exact ledger and coefficient map independently in Julia/Nemo.

All admission falsifiers passed. No numerical benchmark or downstream
calculation was started.

## Model-specific beta ledger

For group order `(4C, 2L, 2R)`, the independently reconstructed one-loop
coefficients are

```text
a_PS = (1, 26/3, 26/3).
```

The field ledger is:

| Field | Type | Pati-Salam representation | Multiplicity/convention |
|---|---|---|---|
| `F_L` | Weyl fermion | `(4,2,1)` | three families |
| `F_R` | Weyl fermion | `(4bar,1,2)` | three families |
| `H_D` | complex scalar | `(1,2,2)` | one |
| `Sigma_1` | complex scalar | `(6,1,1)` | active `126_H` multiplet at `M_I` |
| `Sigma_2` | complex scalar | `(10,3,1)` | one |
| `Sigma_3` | complex scalar | `(10bar,1,3)` | one |
| `Sigma_4` | complex scalar | `(15,2,2)` | one |

As a stronger cross-check, the same ledger reproduces Babu-Khan's full
two-loop matrix exactly:

```text
b_PS = [[1209/2, 249/2, 249/2],
        [1245/2, 779/3,    48],
        [1245/2,    48, 779/3]].
```

### Sextet attribution correction

The published `a_4C=1` and `b_4C,4C=1209/2` require one active complex
`(6,1,1)` multiplet. The exact beta ledger alone cannot identify it because
`Sigma_1` from `126_H` and `H_T` from `10_H` have the same Pati-Salam quantum
numbers. Babu-Khan Section 2.2 states that the whole `126_H`, including
`Sigma_1`, is brought to `M_I`; Equation (13) includes its components in the
intermediate threshold ledger. Table 1 and Equation (17) instead place `H_T`
in the `M_U` threshold ledger. The source-consistent interval field is therefore
`Sigma_1`, and `H_T` is not part of this beta ledger.

Removing `Sigma_1` while leaving all other interval fields fixed gives

```text
a_4C = 2/3
b_4C,4C = 3551/6,
```

with every other entry unchanged. That is a changed spectrum with the active
intermediate sextet removed; it is not an `H_T`-decoupling branch.

Table 1 displays `Sigma_1` at `M_U`, in tension with the explicit placement
prose and the intermediate threshold equation. This source presentation
inconsistency is preserved in the dedicated
[`H_T` threshold audit](../bk_ht_threshold_audit/RESULT.md). It does not change
the published coefficients or the Wilson-running factor. The earlier
high-scale-`H_T` attribution has been corrected.

## Anomalous factors and sign reconciliation

For the unique mixed-chirality Pati-Salam current invariant, the fundamental
Casimirs give

```text
gamma_4C = 2 C2(4) = 2(15/8) = 15/4
gamma_2L = 3 C2(2) = 3(3/4) = 9/4
gamma_2R = 3 C2(2) = 3(3/4) = 9/4.
```

Both papers use the gauge-coupling convention

```text
d(alpha_i^-1)/d ln(mu) = -a_i/(2 pi),
```

equivalently

```text
d alpha_i/d ln(mu) = a_i alpha_i^2/(2 pi).
```

The admitted Wilson-coefficient RGE is

```text
d ln(C_PS)/d ln(mu)
    = -[gamma_4C alpha_4 + gamma_2L alpha_2L
       + gamma_2R alpha_2R]/(2 pi).
```

It follows directly that

```text
d ln(C_PS)/d ln(alpha_i) = -gamma_i/a_i.
```

Mambrini et al. write the low/high coupling ratio to a negative power.
Babu-Khan write the inverse, high/low ratio to the corresponding positive
power. The forms are algebraically identical; there is no sign disagreement.

## Exact Pati-Salam running factor

Define

```text
r4  = alpha_4(M_I)  / alpha_U
r2L = alpha_2L(M_I) / alpha_U
r2R = alpha_2R(M_I) / alpha_U.
```

Then

```text
C_PS(M_I) = A_PS C_PS(M_U),
```

with

```text
A_PS = r4^(-15/4) r2L^(-27/104) r2R^(-27/104).
```

D parity gives `r2L=r2R=r2`, so the reduced form is

```text
A_PS = r4^(-15/4) r2^(-27/52).
```

For `ell=ln(M_U/M_I)>0`, one-loop gauge running gives

```text
alpha_i(M_I)/alpha_i(M_U)
    = 1/[1 + a_i alpha_i(M_U) ell/(2 pi)].
```

The exact checks establish:

- `ell -> 0` gives `A_PS -> 1`;
- the derivative at `ell=0` is
  `sum_i gamma_i alpha_i(M_U)/(2 pi)`;
- differentiating the closed form reproduces the Wilson RGE;
- setting any gauge coupling to zero removes only its own contribution;
- the gauge-only factor is flavor blind and does not mix the frozen tensor.

No numerical value is quoted because this calculation did not admit a model
benchmark or a finite-threshold prescription.

## Tree-level projection at `M_I`

Only `C_PS` is evolved above `M_I`. The broken-phase pole projector is then
applied once:

```text
O_I   -> +2 A_PS k1^2 Q_qque
O_II  -> +2 A_PS k1^2 Q_duql
O_III -> +2 A_PS k2^2 Q_duql
O_IV  -> -2 A_PS k2^2 Q_qqdN.
```

For weak-basis flavor indices `p,r,s,t`, the nonredundant coefficient tensors
at the boundary are

```text
C_qque[p,r,s,t](M_I)
  = A_PS k1^2 (delta[p,s] delta[r,t] + delta[r,s] delta[p,t])

C_duql[p,r,s,t](M_I)
  = 2 A_PS [k1^2 delta[r,s] delta[p,t]
            + k2^2 delta[p,s] delta[r,t]]

C_qqdN[p,r,s,t](M_I)
  = -A_PS k2^2 (delta[p,s] delta[r,t] + delta[r,s] delta[p,t]).
```

The zero entries remain

```text
C_qqql = C_duue = C_uddN = 0.
```

Here

```text
k1^2 = 1/(2 omega_s^2)
k2^2 = 1/[2(omega_s^2 + sigma^2)].
```

They are not independent Wilson coefficients above `M_I`. They enter only in
the Pati-Salam-breaking projection. Setting `A_PS=1` reproduces every nonzero
and zero entry of the completed tree-level boundary.

`Q_qqdN` remains in SMEFT plus singlet neutrinos. No right-handed-neutrino mass
ordering is presumed, and no `N` threshold is crossed.

## Verification record

| Check | Result |
|---|---|
| Babu-Khan one-loop beta coefficients reconstructed | `PASS` |
| Babu-Khan two-loop beta matrix cross-check | `PASS` |
| Intermediate `Sigma_1` sextet contribution isolated | `PASS` |
| `H_T` separated into the `M_U` threshold ledger | `PASS_AFTER_CORRECTION` |
| Casimir reconstruction of anomalous factors | `PASS` |
| Mambrini/Babu-Khan exponent orientation reconciled | `PASS` |
| Analytic RGE and first-log expansion | `PASS` |
| D-parity reduction | `PASS` |
| Full three-generation flavor tensor | `PASS` |
| Running-before-projector ordering | `PASS` |
| Unit-running recovery of prior boundary | `PASS` |
| Right-handed-neutrino retention | `PASS` |
| Independent Julia/Nemo replay | `PASS` |

Cadabra was not needed: the unique indexed Pati-Salam invariant and its
tree-level component signs were resolved by the prior calculation, while the
new claims are exact rational group ledgers and scalar evolution factors.
VPC was not used because its finite exact profile does not cover fractional
power RG evolution.

## Reproduction

From the repository root:

```powershell
python calculations\bk_ps_bnv_running_mi_matching\verify_running.py

& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" `
  --startup-file=no `
  --project=tools/julia `
  calculations\bk_ps_bnv_running_mi_matching\verify_running.jl
```

Verified environment:

```text
Python 3.10.11
SymPy 1.14.0
Julia 1.12.6
Nemo 0.56.1
```

SHA-256:

```text
verify_running.py
  ea163c2c35d1e78bcc411b050b7a1c4f28988cc1d301eda9f7868a07c5770083
verify_running.jl
  429f7a886d0e9ee563efd24e625c611fe704edb54d38792235e9e514036db543
```

The compact machine-readable result is [`result.json`](result.json).

## Stopping boundary

The calculation stops at `M_I` with `PASS`.

No SMEFT or SMNEFT running below `M_I`, right-handed-neutrino threshold,
LEFT/chiral matching, hadronic matrix element, lifetime, or experimental
comparison was performed. Each requires a separate admission decision.
