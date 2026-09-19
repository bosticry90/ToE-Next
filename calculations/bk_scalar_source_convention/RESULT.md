# Babu--Khan scalar source-convention reconstruction

## Outcome and authority

**`NO_SINGLE_TRANSLATION_RECONCILES_SOURCE`** for the [Babu--Khan scalar equations as printed](https://arxiv.org/pdf/1507.06712v2), assuming the same printed coupling symbols and vev variables mean the same thing in Eqs. (24), (27), (28), and (30). The decisive obstruction is internal to Eqs. (27)--(28), before any disputed `126_H` Clebsch is used. It rules out a *global, equation-independent dictionary for the printed formulas*, not the existence of a consistent `54_H+126_H+10_H+S_H` theory or a viable parameter point after explicit corrections.

No benchmark search, Pati--Salam flavor RGE, fermion fit, or below-`M_I` evolution was started. The two earlier Babu--Khan BNV passes are independent of these scalar formulas and remain bounded passes. The printed `4 x 4` light-doublet matrix is still **neither confirmed nor refuted** by a full normalized `126_H` Hessian.

## Frozen canonical convention and source comparison

The canonical comparison uses real symmetric traceless `Phi_ij` (`54_H`), a complex self-dual antisymmetric five-form `Sigma_ijklm` (`126_H`), a complex vector `phi_i` (`10_H`), and a complex PQ singlet `S`. Every repeated `SO(10)` index in Eq. (24) is summed over all ten values; a `p!` divides overcounting only where it is explicitly printed. The kinetic normalization chosen for this calculation is

```text
L_kin = (1/2) dPhi_ij dPhi_ij
      + (1/(2*5!)) dSigma*_ijklm dSigma_ijklm
      + dphi*_i dphi_i + dS* dS.
```

The `1/2` for the self-dual `126` prevents double-counting independent components; this convention is explicitly discussed in the directly cited [Aulakh--Girdhar source lineage](https://arxiv.org/html/hep-ph/0405074). That paper also notes that other `126` conventions require field/coupling rescalings, but it studies a different supersymmetric potential and does not supply a Babu--Khan scalar-coupling dictionary.

For the Babu--Khan vevs, `Phi_0=omega_s diag(-2/5 I_6,+3/5 I_4)`, `S_0=v_s/sqrt(2)`, and the self-dual `126` singlet has `Sigma_246810=sigma/(4 sqrt(2))`. The prior [parent-tensor replay](../bk_scalar_tensor_recovery/RESULT.md) establishes `(Sigma Sigma*)/5!=sigma^2`, `tr Phi²=12 omega_s²/5`, and the exact antisymmetric-pair weight in the `beta` invariant. Under the frozen *literal* Eq. (24) contractions, accessible vacuum coefficients compared with Eq. (27) are:

| Coupling monomial | Literal parent coefficient | Eq. (27) coefficient | Formal parent/printed ratio |
|---|---:|---:|---:|
| `-nu² sigma²` | `-1/2` | `-1/2` | `1` |
| `lambda0 sigma⁴` | `1/4` | `1` | `1/4` |
| `alpha omega_s² sigma²` | `6/5` | `3/5` | `2` |
| `beta omega_s² sigma²` | `-6/5` | `-3/5` | `2` |
| `chi2 sigma² v_s²` | `60` | `1/4` | `240` |
| `chi3 omega_s² v_s²` | `6/5` | `3/5` | `2` |

The `chi2` ratio is especially convention-sensitive because Eq. (24) prints *no* `1/5!` on that particular full-index contraction. This table is a **formal vacuum-only candidate dictionary**, not a finding that the authors actually redefined couplings by these factors. `54`-only and `S`-only terms provide controls: their literal contractions agree with Eq. (27). We did not expand the difficult `lambda2,lambda4,lambda4',chi4,eta1` fluctuation invariants here because the decisive no-map condition occurs earlier.

## Global-translation falsifier: vacuum--tadpole integrability

Differentiating the printed Eq. (27) with respect to the printed nonzero `sigma` gives, with *the same* `lambda0` and `sigma`,

```text
nu² = 4 lambda0 sigma²
    + (6/5)(alpha-beta) omega_s²
    + (chi2/2) v_s².
```

The printed Eq. (28) instead has **`lambda0 sigma²`** in this row. The `omega_s` row of Eq. (28) *does* follow exactly from Eq. (27), a useful control showing this is not an across-the-board derivative convention. The printed `mu_s²` row also contains a dimension-one `chi1 v_s` where differentiation of Eq. (27) requires `chi1 v_s²`; its typography is a secondary warning and is not needed for the decision.

This is independent of the choice of normalized parent tensor basis. A constant, invertible coupling redefinition `lambda0_parent = z lambda0_printed` changes the coefficient of `sigma⁴` and its derivative together; it cannot change their fixed derivative ratio of four to one inside the *same printed* Eq. (27). A field rescaling applied globally to both printed equations also cannot change that ratio. The mismatch vanishes only on a special slice such as `lambda0=0` or `sigma=0`, not as an identity of the model; printed scalar tables include nonzero `lambda0` and the breaking requires nonzero `sigma`. Reconciling the printed Eq. (27) and Eq. (28) therefore requires an **equation-specific correction or symbol switch**, which the frozen task explicitly forbids.

As an accessible Hessian check, we derived the **full three-by-three singlet radial Hessian** from Eq. (27), using Eq. (27)'s *own* stationary point and the Eq. (26) singlet coordinates `(-sqrt(12/5) delta_omega_s, delta_sigma, delta_v_s)`. Five of the six independent entries in printed Eq. (30)'s singlet matrix equal **half** that canonical Hessian: its `54` diagonal, PQ-singlet diagonal, and all three off-diagonals. The remaining `126` diagonal does not: Eq. (27) gives `8 lambda0 sigma²` for the canonical radial curvature, so a common half-Hessian convention would give `4 lambda0 sigma²`, whereas Eq. (30) prints `lambda0 sigma²/4`. The exact matrix residual is `diag(0, 15 lambda0 sigma²/4, 0)` after subtracting Eq. (30) from half the canonical Hessian. This is a second same-symbol failure; it does not require the difficult `(15,2,2)` decomposition. The Eq. (27)--(28) integrability failure alone already decides the outcome.

## Lineage, checks, and stopping rule

Both [arXiv v1](https://arxiv.org/html/1507.06712v1) and [v2](https://arxiv.org/html/1507.06712v2) print the same Eq. (27) quartic and Eq. (28) `lambda0` tadpole coefficient. The paper cites [Aulakh--Girdhar's tensor decomposition](https://arxiv.org/html/hep-ph/0204097v4) and [spectrum/convention paper](https://arxiv.org/html/hep-ph/0405074). They establish relevant self-duality and normalizations, but no directly transferable non-supersymmetric `54+126+10+S` potential convention or correction to the Babu--Khan vacuum/tadpole pair was located in this narrow lineage check. The [arXiv record](https://arxiv.org/abs/1507.06712) lists v2 as the latest version; this does not exclude an unpublished author correction.

Exact Python/SymPy replay differentiates the entire printed vacuum polynomial, verifies the `omega_s` positive control, computes the literal accessible parent-to-vacuum ratios, and checks the complete accessible singlet Hessian against Eq. (30). Julia/Nemo independently constructs the decisive one-variable polynomial slice and checks the derivative and the literal-parent alternative. Run:

```powershell
python calculations/bk_scalar_source_convention/verify_translation.py
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no --project=tools/julia calculations/bk_scalar_source_convention/verify_translation.jl
```

The next authorized scientific choice is **not** to silently repair one equation. Either obtain an attributable corrected source dictionary that states every changed symbol and reproduces vacuum, tadpoles, and masses under one convention, or separately admit a *new, explicitly canonical source-derived scalar variant* with no claim of numerical identity to the printed Babu--Khan benchmark. Neither fork was activated in this calculation.
