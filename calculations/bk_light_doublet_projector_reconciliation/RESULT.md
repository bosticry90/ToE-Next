# Babu--Khan light-doublet projector and printed-sample reconciliation

## Calculation record

1. **Scientific question:** Is the missing `1/r` in the published light-doublet identity harmless typography, or do the published scalar samples supply a reproducible full-matrix boundary for the proposed flavor calculation?
2. **Claim under test:** The real-VEV `54_H + 126_H + complex 10_H + PQ` scalar sector, the full `4 x 4` doublet matrix, light zero mode, and both printed samples agree without using the disputed reduced identity as an input.
3. **Scope and authority ceiling:** Published scalar matrices and printed sample parameters only. This does not test the viability of the SO(10) model, calculate a complete fermion fit, or revise the two prior BNV recovery results.
4. **Frozen inputs and assumptions:** [Babu--Khan v2](https://arxiv.org/pdf/1507.06712v2), PDF Eqs. (24), (26), (30), (32)--(36), Tables 2--5; real couplings/VEVs and the canonical doublet order `(H_u,H_d*,h_u,h_d*)`. Source tables are **rounded**, and their common `10_H` quadratic mass `m^2` is not printed.
5. **Provenance and comparators:** The [author's October 2015 talk](https://indico.bnl.gov/event/1282/contributions/1373/attachments/1079/1229/Saki_Khan_UD2_2015_.pdf) repeats the Table 2 exponent. The [APS journal record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.92.075018) and [arXiv record](https://arxiv.org/abs/1507.06712) were checked for a visible correction; no explicit correction to Eq. (36) or Table 2 was found in this limited source/author-lineage check.
6. **Primary method and tool:** Direct analysis of the source's *full* doublet mass matrix, independently of reduced Eq. (36); exact sign/mass-ratio checks with Nemo and a rounded-sample spectral sensitivity replay in Python/NumPy. A complete independent SO(10)-tensor Hessian expansion of potential Eq. (24) was **not** obtained.
7. **Independent replay decision and reason:** The printed-sample inconsistency is consequential, so Julia/Nemo independently checked its decisive rational sign and mass-squared ratio without using Python's output.
8. **Adversarial checks and falsifiers:** Re-derive the zero-mode identity; require one null eigenvector with three positive heavy modes; compare a non-doublet mass that does not depend on `m^2`; test nearest-last-digit rounding and the single-exponent repair hypothesis; keep actual use of Eq. (36) in unpublished author code unresolved.
9. **Known limits and assumptions:** At nonzero component ratios, `r=alpha_h/beta_h`, `s=alpha_H/(r beta_H)` imply `alpha_H/beta_H=r s`. The entries' *coupling provenance* follows the printed potential and matrix, but the exact `SO(10)` tensor Clebsches and canonical normalizations of every second derivative have not been independently reconstructed here.
10. **Stopping rule:** Do not resume the flavor RGE or fit until a source sample's full matrix and light projector are reproducible from a corrected, sufficiently precise scalar benchmark, and the potential-to-matrix normalization check is complete.
11. **Failure interpretation:** At least the **printed Table 2 point** needs repair before use. This does not prove the authors used the erroneous Eq. (36), does not refute a possible unrounded original point, and does not show Table 4 is inconsistent.
12. **Disposition and reproduction:** `PUBLISHED_SAMPLE_POINTS_REQUIRE_REPAIR`, with the qualifier `EQ36_NUMERICAL_USE_UNRESOLVED`. Run `python calculations/bk_light_doublet_projector_reconciliation/replay_samples.py` and `julia --startup-file=no --project=tools/julia calculations/bk_light_doublet_projector_reconciliation/verify_printed_sample.jl` (project Julia path is `tools/julia`). No downstream calculation began.

## Verification matrix

| Requested gate | Outcome | Boundary |
|---|---|---|
| Derive all entries by normalized SO(10) tensor-Hessian expansion of potential Eq. (24) | **NOT EARNED** | The source's full Eq. (30) was replayed and its allowed-term structure checked, but its numerical Clebsches were not rederived from ten-dimensional component tensors. |
| Full `D v_light=0` and corrected identity | **PASS, algebraic** | No use of Eq. (36); the four zero-mode rows recover `-D12/(r s)`. |
| Printed Table 2 as a positive-heavy-mode scalar point | **FAIL** | Its `D11<0` survives displayed rounding, independent of unprinted `m^2`. |
| Table 2 vs. an independent non-doublet mass in Table 3 | **FAIL** | Source mass formula gives about ten times the listed mass; exact Julia/Nemo verifies squared ratio `>100`. |
| One-power `sigma`-exponent change | **POSSIBLE REPAIR, NOT ADOPTED** | Removes the two large contradictions but does not establish the original unrounded point. |
| Printed Table 4 as a complete projector | **UNDERDEFINED** | `m^2` and full-precision fine-tuned couplings/eigenvector are not printed; rounded replay cannot decide. |
| Explicit correction or evidence of Eq. (36) use in author follow-up | **NOT FOUND / UNRESOLVED** | Limited primary-source and author-talk search; no inference about private calculation code. |

## Potential, full matrix, and projector boundary

The source potential contains the `126` self-quartics and `54^2 126 126*` terms, the `10` quadratic and `54/126`-dependent terms, the `chi_4` singlet-assisted `126` mixing, `chi_6` singlet-assisted `10` mixing, and `eta_1` mixing between a `126` doublet and a `10` doublet. Those allowed terms explain the sparse pattern of the published full matrix:

```text
                  [ D11  D12    0  D14 ]
  D               [ D12  D22    0    0 ]
                  [   0    0  D33  D34 ]
                  [ D14    0  D34  D44 ]

  D11 = 8(lambda2+lambda4-2lambda4') sigma^2 + beta omega_s^2
  D12 = 2 sqrt(2) chi4 omega_s v_s
  D14 = 4 sqrt(3) eta1 sigma^2
  D22 = 4(3lambda2+3lambda4+4lambda4') sigma^2 + beta omega_s^2
  D33 = A2; D44 = B2; D34 = sqrt(2) chi6 v_s
  B2-A2 = (gamma2-gamma1) sigma^2.
```

Here `A2` and `B2` also contain the same unprinted `m^2` and the source's `xi3,eta0,eta2,chi5` terms. The displayed coefficients are **transcribed from the source's full Eq. (30)** and checked against Eq. (24)'s allowed-coupling structure. We did not derive all numerical factors `8, 4, sqrt(2), sqrt(3)` from normalized ten-dimensional component tensors, so that stronger requested step remains unearned. No inference from Eq. (36) entered this matrix.

Let `v=(alpha_H,beta_H,alpha_h,beta_h)^T`. The full zero-mode equations `D v=0`, combined with `r=alpha_h/beta_h` and `s=alpha_H/(r beta_H)`, imply

```text
  D34 = -r D33,
  D14 alpha_H = (r^2 D33-D44) beta_h,
  D11 = D14^2/(D44-r^2 D33) - D12/(r s).
```

This reconfirms the previous [exact projector check](../bk_ps_flavor_kernel/RESULT.md). The PDF's Eq. (36) instead has `-D12/s`. We found no alternative field or VEV convention in the source that reconciles the two expressions; a full independent tensor-normalization check remains pending.

## Decisive printed Table 2 contradiction

Table 2 prints `sigma=8.65 x 10^14 GeV`, `lambda2=-0.17`, `lambda4=0.48`, `lambda4'=0.17`, `beta=1.25 x 10^-5`, and `omega_s=1.38 x 10^16 GeV`. Inserting these into the full matrix (without Eq. (36)) gives

```text
  D11 = -1.771935 x 10^29 GeV^2.
```

A real symmetric mass-squared matrix with one zero and all remaining modes positive must be positive semidefinite, hence every diagonal entry must be nonnegative. `D11<0` rules that out for the **point as printed**, regardless of the unprinted `m^2`. Taking generous nearest-last-digit intervals for the displayed couplings and scales still gives `D11 < -5.7 x 10^28 GeV^2`; ordinary table rounding cannot reverse the sign.

There is a second independent, `m^2`-free discrepancy. PDF Eq. (30) gives `M^2(3,3,-1/3)=4(3lambda2+3lambda4+4lambda4')sigma^2`. Table 2 as printed predicts `M=2.195 x 10^15 GeV`, while Table 3 lists `2.17 x 10^14 GeV`. Julia/Nemo confirms exactly that the predicted **mass squared** exceeds the listed value by more than `100x`.

If one changes *only* Table 2's `sigma` exponent to `10^13`, these two large contradictions disappear: `D11=+5.848 x 10^26 GeV^2` and the non-doublet mass becomes `2.195 x 10^14 GeV`, close to the printed `2.17 x 10^14 GeV`. This is strong evidence for a **Table 2 exponent transcription error**, not proof of the authors' unprinted original input. The October 2015 author talk repeats `10^14`, so it does not provide a published correction.

## What the rounded tables cannot decide

With the hypothetical `10^13` repair for Table 2, and with Table 4 as printed, the fixed full-matrix entries give `alpha_H/beta_H=-D22/D12` of `25.165` and `25.192`, respectively. These are near the stated `r s=69 x 0.36=24.84`. The small differences cannot reject an underlying point because `r,s` and all couplings are printed with limited precision.

For sensitivity only, we eliminated the unprinted `m^2` by tuning the full matrix to one zero eigenvalue. The positive-heavy branches exist for both those cases, but the **rounded** parameter values give light-mode `r` near `190` and `186`, not the quoted `69`, and their smallest heavy masses differ from the printed `1.13 x 10^12 GeV`. These are not decisive failures: `D11` is a cancellation among terms, and variations of the displayed two-decimal quartics within combined rounding intervals can change the inferred small eigenvalue and `r` substantially. Thus neither Table 4 nor the hypothetically repaired Table 2 yields a validated, exact light-Higgs projector from the data actually published.

The printed Table 2 contradiction alone earns `PUBLISHED_SAMPLE_POINTS_REQUIRE_REPAIR`. It does **not** identify whether the original numerical program used the wrong Eq. (36), used the full matrix correctly, or relied on unprinted high-precision values. No searched author follow-up explicitly settles this. A source correction or complete, full-precision benchmark (including `m^2`, normalized doublet eigenvector, and triplet check) is needed before treating either scalar sample as a flavor-fit boundary.
