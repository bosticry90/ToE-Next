# Babu-Khan `H_T` threshold attribution and branch audit

## Disposition

```text
AUDIT: BK_HT_THRESHOLD_ATTRIBUTION_AND_BRANCH_AUDIT_V1
RESULT: CORRECTION_APPLIED
HT RUNNING BRANCH: NOT_PHYSICAL_AS_STATED
FUTURE THRESHOLD SEAM: NOT_ADMITTED_NOW
```

The completed Pati-Salam running result had correctly reconstructed the
published beta coefficients but incorrectly named the complex `(6,1,1)` field
responsible for the interval contribution. The source-consistent field is
`Sigma_1` from `126_H`, not `H_T` from `10_H`.

This is a provenance and interpretation correction, not a change to

```text
a_PS = (1, 26/3, 26/3),
A_PS = r4^(-15/4) r2L^(-27/104) r2R^(-27/104),
```

or to the completed `M_I` coefficient projector.

## Exact findings

- A complex `SU(4)` sextet contributes `1/3` to `a_4C`.
- The correct active sextet `Sigma_1` raises `a_4C` from `2/3` to `1`.
- `H_T` is not part of the interval ledger; placing it at `M_U` leaves the
  interval coefficient and exponent unchanged.
- Removing `Sigma_1` produces the altered-spectrum values `a_4C=2/3` and
  exponent `-45/8`. That is not an `H_T`-decoupling branch.
- Under self-consistent one-loop evolution, the published and altered-spectrum
  `SU(4)` factors agree at first leading-log order and differ beginning at
  order `x^2`, with
  `log(A_changed/A_published)=(5/8)x^2+O(x^3)`.
- `H_T` enters high-scale gauge matching through
  `Delta[alpha_4C^(-1)]=-ln(M_HT/M_U)/(6 pi)` and affects the threshold-defined
  unification scale in Babu-Khan Equation (19).

## Verification

The corrected primary Python/SymPy beta reconstruction and independent
Julia/Nemo replay both pass. The calculation-local audit script independently
checks the sextet contribution, both analytic running expressions, their
series comparison, and the high-scale threshold term.

From the repository root:

```powershell
python calculations\bk_ps_bnv_running_mi_matching\verify_running.py

& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" `
  --startup-file=no `
  --project=tools/julia `
  calculations\bk_ps_bnv_running_mi_matching\verify_running.jl

python calculations\bk_ht_threshold_audit\verify_threshold.py
```

SHA-256:

```text
verify_threshold.py
  b10bb931455d44ed4fdd6917e6d135bf163920fdd1059e993f4dd7a4e1dbd60f
```

## Authority ceiling

This audit establishes the correct source-field attribution and rejects one
misstated branch comparison. It does not quantify a Babu-Khan high-scale
threshold benchmark, derive finite one-loop BNV Wilson matching, or establish
proton-decay viability.

The detailed admission criteria and source evidence are in
[`docs/BABU_KHAN_HT_THRESHOLD_AUDIT.md`](../../docs/BABU_KHAN_HT_THRESHOLD_AUDIT.md).
