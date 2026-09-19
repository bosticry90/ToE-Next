# Babu-Khan high-scale `H_T` threshold audit

## Decision

```text
AUDIT: BK_HT_THRESHOLD_ATTRIBUTION_AND_BRANCH_AUDIT_V1
OUTCOME: CORRECTION_APPLIED
PROPOSED SEAM: BK_HT_MU_THRESHOLD_SYSTEMATICS
ADMISSION: NOT_ADMITTED_NOW
ACTIVE CALCULATION: NONE
```

The proposed comparison between a published branch with `H_T=(6,1,1)` active
throughout the Pati-Salam interval and a branch with `H_T` decoupled near
`M_U` is not a physical two-branch comparison of the Babu-Khan spectrum. The
premise came from a field-attribution error in the completed running result.

The source-consistent identification is:

- `Sigma_1=(6,1,1)` from the complex `126_H` supplies the complex-sextet
  contribution to the Pati-Salam beta ledger between `M_I` and `M_U`;
- `H_T=(6,1,1)` from the complex `10_H` is a high-scale field whose mass
  enters the finite `M_U` gauge-threshold matching condition.

The numerical beta coefficients and completed Wilson-running factor do not
change. Their prior field attribution and threshold qualification do.

## Controlling source evidence

The audit used K. S. Babu and S. Khan,
[arXiv:1507.06712v2](https://arxiv.org/abs/1507.06712v2):

1. Section 2.2 states that `Sigma_1=(6,1,1)` cannot remain at `M_U` and that
   the whole `126_H` is brought to `M_I`.
2. Equation (13) includes the `Sigma_11` and `Sigma_12` components in the
   intermediate-scale threshold ledger.
3. Table 1 places `H_T` at `M_U`, and Equation (17) includes it in the
   high-scale threshold term
   `lambda_4C^(uS)=2 eta_HT+8 eta_zeta3`.
4. Equation (7) labels `(1,26/3,26/3)` as the beta coefficients for the
   intermediate scalar spectrum.

Table 1 displays `Sigma_1` at `M_U`, in tension with the explicit prose and
the intermediate threshold ledger. That internal presentation inconsistency
must remain visible. Because `Sigma_1` and `H_T` are both complex `(6,1,1)`
multiplets, the one- and two-loop beta numbers alone cannot distinguish which
one supplied the sextet term. The explicit placement statements and separate
threshold equations control the attribution used here.

## Corrected field ledger

The Pati-Salam interval ledger is

| Field | Representation | Role |
|---|---|---|
| three `F_L` families | `(4,2,1)` | active Weyl fermions |
| three `F_R` families | `(4bar,1,2)` | active Weyl fermions |
| `H_D` | `(1,2,2)` | active complex scalar |
| `Sigma_1` | `(6,1,1)` | active complex scalar from `126_H` |
| `Sigma_2` | `(10,3,1)` | active complex scalar |
| `Sigma_3` | `(10bar,1,3)` | active complex scalar |
| `Sigma_4` | `(15,2,2)` | active complex scalar |

It reproduces

```text
a_PS = (1, 26/3, 26/3)
b_PS = [[1209/2, 249/2, 249/2],
        [1245/2, 779/3,    48],
        [1245/2,    48, 779/3]].
```

`H_T` is absent from this interval ledger. It remains in the high-scale
matching ledger.

## Branch comparison

Let

```text
x = alpha_U ln(M_U/M_I)/(2 pi).
```

The branches are:

| Branch | Interval sextet | `a_4C` | `SU(4)` factor | Scientific status |
|---|---|---:|---|---|
| Correct Babu-Khan interval | `Sigma_1` active; `H_T` treated at `M_U` | `1` | `(1+x)^(15/4)` | controlling published-spectrum branch |
| `H_T` decoupled at `M_U` | same active `Sigma_1` | `1` | unchanged interval factor | not a distinct running branch |
| Altered spectrum | `Sigma_1` removed | `2/3` | `(1+(2/3)x)^(45/8)` | adversarial comparator, not `H_T` decoupling |

At a fixed endpoint coupling ratio, the changed-spectrum exponent is `-45/8`
rather than `-15/4`. When each branch's gauge coupling is evolved consistently,
both have the same first leading logarithm:

```text
log(A_changed/A_published) = (5/8) x^2 + O(x^3).
```

This comparison is useful as a bookkeeping check, but it does not define a
second Babu-Khan `H_T` branch.

## What `H_T` actually changes

With `rho=M_HT/M_U`, Equations (16)-(17) give the `H_T` contribution

```text
Delta[alpha_4C^(-1)] = -ln(rho)/(6 pi).
```

Equation (19) also puts one power of `M_HT` under the `1/23` root defining the
threshold-shifted unification scale. Thus `H_T` can change the fitted
`M_U`, `alpha_U`, and endpoint ratios through high-scale gauge matching. The
source does not thereby supply a finite one-loop matching correction for the
BNV Wilson coefficient itself.

No numerical effect is quoted. A threshold number would require a frozen,
self-consistent mass benchmark and a coupled gauge-matching solution; inserting
an arbitrary `M_HT/M_U` range into the already completed symbolic running
factor would mix schemes and risk double counting.

## Admission gate for a future threshold calculation

`BK_HT_MU_THRESHOLD_SYSTEMATICS` may be admitted only when a downstream
quantitative observable requires it and all of the following are frozen:

1. a Babu-Khan scalar-spectrum benchmark that identifies the relevant
   `H_T` mass eigenstate or eigenstates and mixing conventions;
2. the matching scale, renormalization scheme, and perturbative order;
3. a coupled solution for `M_I`, `M_U`, `alpha_U`, and the endpoint couplings;
4. a no-double-counting prescription separating interval running from finite
   high-scale gauge matching;
5. a derivation or sourced justification for any finite BNV Wilson-coefficient
   threshold term at the admitted order;
6. a bounded threshold window, perturbativity checks, and propagation of the
   resulting scale/coupling uncertainty;
7. an explicit authority ceiling limited to the `H_T` threshold sensitivity of
   the frozen benchmark.

It must fail or block if the mass eigenstate cannot be mapped to the source
field, the gauge matching is inconsistent, the result depends on an arbitrary
unfrozen spectrum choice, or interval running and threshold matching are
double counted.

## Outcome and stopping boundary

The correction removes the claimed unresolved `H_T` placement from the
completed Pati-Salam running result. The proposed separate running seam is not
admitted. A future numerical high-scale threshold-systematics calculation is
well defined in principle but is not yet scientifically required or adequately
frozen.

No running below `M_I`, right-handed-neutrino threshold, hadronic matching, or
proton-lifetime calculation was performed.
