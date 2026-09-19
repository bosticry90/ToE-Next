# Babu-Khan Pati-Salam flavor and one-light-Higgs kernel: fail-fast attempt

## Calculation record

1. **Scientific question:** Can the frozen `54_H + 126_H + complex 10_H + PQ` Babu-Khan model supply checked one-loop Pati-Salam flavor running and tree-level one-light-Higgs matching before any fermion fit?
2. **Claim under test:** The parent Pati-Salam Yukawa vertices, their one-loop beta functions, and the published light-doublet zero-mode relations can be made mutually consistent in one convention.
3. **Scope and authority ceiling:** One-loop flavor RG and tree-level `M_I` matching only; no fit, below-`M_I` running, BNV evolution, lifetime, or model viability verdict. This attempt stopped **before** a complete beta-function system or matching kernel was earned.
4. **Frozen inputs and assumptions:** [Babu--Khan v2](https://arxiv.org/pdf/1507.06712v2) Sections 2, 6 and 7; the corrected interval field attribution in the [threshold audit](../../docs/BABU_KHAN_HT_THRESHOLD_AUDIT.md); a real symmetric doublet mass-squared matrix and the paper's real-VEV branch. One-loop gauge terms use the standard `SU(4)`/`SU(2)` fundamental generator normalization `Tr(T_a T_b)=delta_ab/2`.
5. **Provenance and comparators:** [Aulakh--Girdhar v4](https://arxiv.org/html/hep-ph/0204097v4) Eqs. (112), (115)--(116) for the parent SO(10) Pati-Salam contractions; [Luo--Wang--Xiao v3](https://arxiv.org/html/hep-ph/0211440) Eq. (33) for a generic one-loop Weyl-fermion Yukawa beta function; [Meloni--Ohlsson--Riad](https://arxiv.org/html/1612.07973) Appendix A Eqs. (86)--(88) as a **reduced-spectrum comparator**, not the Babu-Khan answer.
6. **Primary method and tool:** Exact algebra of the four doublet zero-mode equations, with SymPy and rational Casimir bookkeeping; no fitted parameters.
7. **Independent replay decision and reason:** Required because a source-level projector discrepancy could change fit constraints. Julia/Nemo independently sums fundamental generator squares and replays an exact positive-semidefinite doublet counterexample without reading Python outputs.
8. **Adversarial checks and falsifiers:** Gauge-Casimir coefficients, D-parity interchange of left/right gauge terms, published reduced-spectrum gauge-term limit, the `4 x 4` zero mode, positive heavy sector, printed Eq. (36), and source/PQ field inventory. The **printed scalar-projector relation failed**.
9. **Known-limit and physical-assumption checks:** Aulakh--Girdhar's parent invariant contains the `10_H` bidoublet and the `126_H` sextet, left triplet, right triplet and adjoint bidoublet vertices. The 10-Higgs conjugate Yukawa remains forbidden by the frozen PQ assignment. Their `126` versus `126bar` component orientation and exact relative normalizations have **not** been transferred to the Babu-Khan non-SUSY convention here.
10. **Stopping rule:** Stop at the first unresolved normalization or failed source matching/projector identity. The published light-doublet identity failed an exact zero-mode counterexample, so no full Yukawa beta expansion, neutrino threshold disposition, or fit was attempted.
11. **Failure interpretation:** A published algebraic relation is inconsistent with the paper's own `r,s` definitions and zero-mode equations. This does **not** refute the model; the corrected relation is explicit, but its effect on the paper's scalar examples and a canonical `M_I` projector has not been adjudicated.
12. **Result and reproducibility:** `STOPPED_AT_SOURCE_PROJECTOR_INCONSISTENCY`. Run `python calculations/bk_ps_flavor_kernel/verify_boundary.py` and `julia --startup-file=no --project=tools/julia calculations/bk_ps_flavor_kernel/verify_boundary.jl`. Both passed their exact checks and independently flagged the same printed-equation mismatch.

## Admitted task specification and acceptance rule

The admitted relation was `BK_PS_FLAVOR_RGE_AND_MI_MATCHING_KERNEL`: derive the
one-loop Dirac and Majorana Yukawa RGEs for the **actual** Babu--Khan
Pati--Salam interval, then derive the tree-level one-light-Higgs `M_I`
projection to `Y_u,Y_d,Y_e,Y_N,M_N`, including the type-II channel's
disposition. Preserve the parent PQ and D-parity conditions, symmetric family
Yukawas, explicit component normalization, and the active `Sigma_1`--`Sigma_4`
scalar spectrum. Use Meloni--Ohlsson--Riad only as a decoupling comparator.
No fit, proton-decay prediction, or evolution below `M_I` was admitted.

Acceptance required the matrix below to pass, with independent reconstruction
of group factors and matching identities in a second exact environment. The
first unresolved vertex normalization, forbidden Yukawa generation, failed
reduced-spectrum limit, scalar-projector contradiction, or underdefined
threshold convention was a mandatory stop. These are **conjunctive** gates;
the partial passes below do not constitute a completed kernel.

## Verification matrix at stop

| Gate | Outcome | Evidence / ceiling |
|---|---|---|
| Actual interval field and allowed-vertex inventory | PASS, representation channels only | `F_L=(4,2,1)`, `F_R=(4bar,1,2)`; `10_H` bidoublet, `126_H` sextet, left/right triplets and `(15,2,2)` all appear in the parent contractions. Exact `126`/`126bar` conjugation must be frozen before a component vertex is used. The high-scale `H_T` sextet is not substituted for interval `Sigma_1`. |
| One-loop gauge-Casimir part of Yukawa beta functions | PASS | Exact Python formula and independent Julia generator-square sum; agrees with the Dirac/right-Majorana gauge terms in the reduced-spectrum literature. |
| Parent-relative scalar/Yukawa normalization | NOT COMPLETED | Aulakh--Girdhar prints relative factors, but `126`/`126bar` orientation, canonical complex-field, and Babu-Khan mass-matrix normalization transfer were not independently replayed before stop. |
| Complete one-loop Yukawa self/mixed terms | NOT STARTED | No explicit model-specific beta matrices are claimed. |
| Reduced-spectrum full beta-function limit | NOT STARTED | Gauge terms only were checked; cubic Yukawa terms were not. |
| PQ forbidden-coupling closure | STRUCTURAL ONLY | The parent PQ charge forbids a conjugate-`10_H` Yukawa; beta-function closure was not explicitly evaluated. |
| Doublet determinant and zero mode | PASS | The printed determinant equation follows from its `4 x 4` matrix, and an exact rank-three positive-semidefinite example has the declared light eigenvector. |
| Printed `D11` projector equation | **FAIL** | PDF p. 28 Eq. (36) is missing a factor `1/r` relative to Eqs. (33)--(35) in the same paper. |
| Canonical `M_I` map to `Yu,Yd,Ye,YN,MN` and type-II disposition | NOT STARTED | Stopped at projector inconsistency. |

## Earned partial result: universal one-loop gauge terms

For a Yukawa vertex joining Weyl fermions in representations `R_1,R_2`, the
one-loop gauge contribution is `-3 g_i^2 [C2_i(R_1)+C2_i(R_2)]Y` in the
Luo--Wang--Xiao convention. With `C2_4(4)=15/8` and `C2_2(2)=3/4`, the
coefficients of `-(g_4^2,g_L^2,g_R^2)Y` are:

| Fermion channel | Scalar vertices in this interval | Coefficients |
|---|---|---|
| `F_L F_R` | `10_H (1,2,2)` and `126_H (15,2,2)` | `(45/4, 9/4, 9/4)` |
| `F_L F_L` | sextet and left-triplet channel, with scalar conjugation still to be frozen | `(45/4, 9/2, 0)` |
| `F_R F_R` | sextet and right-triplet channel, with scalar conjugation still to be frozen | `(45/4, 0, 9/2)` |

Under unbroken D parity, `g_L=g_R` and the last two channels interchange.
The `F_L F_R` and `F_R F_R` entries reproduce the gauge pieces of the
published reduced-spectrum Eqs. (86)--(88). The **Yukawa-cubic** pieces are
not inferred from this agreement.

## Decisive scalar-projector inconsistency

The paper defines, in its real-VEV branch, `r=v_u/v_d=alpha_h/beta_h` and
`s=kappa_u/(r kappa_d)=alpha_H/(r beta_H)`. Its four zero-mode equations
correspond to

```text
             [ D11 D12   0 D14 ]
   D         [ D12 D22   0   0 ]
             [   0   0 D33 D34 ]
             [ D14   0 D34 D44 ]

   D * (alpha_H, beta_H, alpha_h, beta_h)^T = 0.
```

For nonzero denominators, row 3 gives `D34=-r D33`; row 4 gives
`D14 alpha_H=(r^2 D33-D44) beta_h`; and row 1 then requires

```text
D11 = D14^2/(D44-r^2 D33) - D12/(r s).       [zero-mode identity]
```

The [published PDF](https://arxiv.org/pdf/1507.06712v2), p. 28 Eq. (36),
prints the second term as `-D12/s` instead. The discrepancy is confirmed in
the PDF, not only in the experimental HTML conversion. The adjacent first
zero-mode equation also labels its final beta coefficient `beta_d`, whereas
the declared eigenvector uses `beta_h`; this appears to be a notation slip,
but is not needed for the factor-of-`r` finding.

An exact counterexample, with `r=2`, `s=3`, is

```text
D = [[1/3, -1,  0, -1],
     [ -1,  6,  0,  0],
     [  0,  0,  1, -2],
     [ -1,  0, -2, 10]],
v = (6,1,2,1)^T.
```

Here `D v=0`, `det(D)=0`, `rank(D)=3`; the leading principal minors are
`1/3, 1, 1, 0`, so the three heavy modes are positive. The printed formula
predicts `D11=1/2`, while the exact zero mode requires and the matrix has
`D11=1/3`. Both Python/SymPy and Julia/Nemo reproduce this exactly. This is
an algebraic counterexample to the **printed relation**, not a scalar-potential
point claimed to satisfy every Babu-Khan coupling and threshold condition.

## Carry-forward boundary

The full admitted kernel is **not** a PASS. A future resumed calculation must
first reconcile Eq. (36) with the actual scalar-potential matrix and check
whether any published sample point used the misprinted relation. Only then
may it normalize all active Pati-Salam Yukawa component tensors and evaluate
the complete one-loop beta functions, their reduced-spectrum limit, the
one-light-Higgs `M_I` map, and type-I/type-II neutrino channels. No global fit
or running below `M_I` was begun. The two prior BNV recovery passes remain
unchanged and do not inherit this projector issue automatically.
