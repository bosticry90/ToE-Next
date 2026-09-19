# Babu-Khan-specific fermion-fit feasibility, before optimization

## Disposition

```text
question = CAN_ONE_REPRODUCIBLY_FIT_THE_FROZEN_BABU_KHAN_MODEL
outcome = BLOCKED_BY_MISSING_THEORY_INPUT
cheap_model_no_go = NOT_ESTABLISHED
global_optimization = NOT_STARTED
active_seam = NONE
active_calculation = NONE
```

This is a **protocol-admission** result, not a failure of the model. The parent
Yukawa and scalar theory is specified well enough that the missing work can in
principle be derived by ToE-Next. It is **not** yet an executable, model-specific
fit: the full Pati-Salam flavor RG system for the actual Babu-Khan interval
spectrum, its threshold matching into one light Standard-Model Higgs, and a
single coupled scalar/gauge/flavor benchmark have not been frozen and checked.
Importing a published two-Higgs-doublet or reduced-spectrum fit would silently
change the model. No optimizer was run; optimization failure would not by
itself be a no-go theorem.

## Source boundary and nearest calculational comparator

[Babu and Khan, arXiv:1507.06712v2](https://arxiv.org/html/1507.06712v2)
specify the `54_H -> PS x D -> 126_H -> SM` breaking chain, a complex `10_H`,
complex `126_H`, and a PQ singlet. Their PQ charge assignment forbids the
conjugate-`10_H` fermion coupling. Equations (55)-(57) give two symmetric
generation Yukawa matrices and the tree-level mass relations below. Their
chosen scalar vacuum requires real `r,s`; they explicitly note that the
related fit they quote has a nonzero imaginary part of `s` and would have to
be redone. Equations (58)-(60) define one light Higgs-doublet combination and
its scalar-mass constraints, but they do not constitute a co-frozen numerical
flavor/scalar point.

[Meloni, Ohlsson and Riad, arXiv:1612.07973, Appendix A](https://arxiv.org/html/1612.07973)
give explicit one-loop Pati-Salam Yukawa equations and matching for a related
minimal `10_H + 126_H` model. They state that these equations correct earlier
published formulae. They are a useful **limit and sign comparator**, not a
Babu-Khan implementation: their active Pati-Salam scalar content differs from
the Babu-Khan `126_H` interval spectrum, and their low-energy theory has two
Higgs doublets whereas Babu-Khan retains one. The Babu-Khan interval includes
`Sigma_1=(6,1,1)`, the D-parity partner `Sigma_2=(10,3,1)`,
`Sigma_3=(10bar,1,3)`, and `Sigma_4=(15,2,2)`; see the prior
[sextet-attribution audit](BABU_KHAN_HT_THRESHOLD_AUDIT.md). Whether and how
each extra scalar Yukawa vertex changes the flavor anomalous dimensions must
be derived, not assumed away. The source's Table 1 placement of `Sigma_1`
conflicts with its prose/threshold ledger, as recorded in that audit.

[Ohlsson and Pernow, arXiv:1804.04560](https://arxiv.org/html/1804.04560)
report a poor minimal-model fit with a different intermediate spectrum,
scale, and two-Higgs-doublet treatment. That is an adversarial warning, not a
cheap no-go for this frozen model. The prior
[fit-provenance audit](BABU_KHAN_FERMION_FIT_PROVENANCE_AUDIT.md) explains why
no published point can be transplanted unchanged.

## Exact necessary conditions available now

At a **single common tree-level matching convention and scale** in which
Babu-Khan Eq. (57) applies, let `H,F` be complex symmetric and `r,s` real:

```text
Md = H + F                 Me = H - 3F
Mu = r(H + sF)             MnuD = r(H - 3sF)
MN = rR^(-1) F
```

Elimination gives exact candidate-point checks:

```text
F = (Md - Me)/4
H = (3Md + Me)/4
Mu = (r/4)[(3+s)Md + (1-s)Me]
MnuD = Mu - r s (Md - Me)
```

Thus `Mu` must lie in the **real** linear span of `Md,Me` in the common
SO(10) flavor basis. For the three full complex matrices `M_i`, form the real
Hilbert-Schmidt Gram matrix
`G_ij = Re Tr(M_i^dagger M_j)`, `i,j in {u,d,e}`. A necessary condition is
`det(G)=0`; this statement is invariant under the common family rotation
`M_i -> U^T M_i U`. The two-matrix identity was independently expanded with
SymPy during this audit. This is a strong **candidate-matrix rejection test**,
not an observational no-go: measured masses and CKM data do not determine
the common quark-lepton flavor orientation or all phases, and the simple
identity must not be applied to low-energy matrices after different RG flows.
In a full running fit, the Pati-Salam Yukawa components, including the
right-handed Majorana coupling, evolve separately; Eq. (57) cannot be used as
an unmodified low-energy equality.

The scalar light-doublet gate is independent: the frozen real `4 x 4`
doublet mass-squared matrix must have **exactly one** light eigenvector with
the declared mixing coefficients, positive remaining physical eigenvalues,
and acceptable color-triplet masses. Babu-Khan Eq. (59)'s determinant identity
was re-expanded independently with SymPy. Equation (60) imposes additional
sign/positivity conditions on a candidate scalar point. The paper exhibits
allowed scalar examples; these conditions have not failed for the model as a
whole. The quoted complex-`s` literature point fails the Babu-Khan vacuum
restriction **as-is**, not every possible refit.

**Later calculation qualification:** the admitted [flavor-kernel fail-fast
attempt](../calculations/bk_ps_flavor_kernel/RESULT.md) found that the
published `D11` identity (PDF Eq. (36), numbered differently in the HTML
rendering) omits `1/r` in its `D12` term relative to the paper's own zero-mode
equations and definitions of `r,s`. The determinant identity remains valid;
the printed positivity restriction relying on the `D11` expression must not
be applied unchanged. This is not a model no-go or a verdict on its scalar
sample points.

A naive charged-sector parameter count is not a no-go: after a common Takagi
choice for one symmetric matrix, `h` has 3 real diagonal entries, `f` has 12
real entries, and real `r,s` add 2 (17 continuous parameters before scalar
relations), while charged masses and CKM supply 13 observables. This count
neither proves fit feasibility nor accounts for all scalar/threshold
constraints. It explains why optimization-free exclusion is not obtained by
counting alone.

## Reproducible protocol that still needs its theory kernel

| Stage | Required freeze or derivation | Cheapest acceptance/rejection test |
|---|---|---|
| 0. Parent model | Fix field normalization, PQ charges, D parity, complex versus real scalar multiplets, the `Sigma_1` placement qualification, and one scalar-potential branch. | Reject a point violating PQ, real `s`, perturbativity, one-light-doublet positivity, or triplet safety. |
| 1. `M_U -> M_I` | Derive and independently check **Babu-Khan-spectrum** one-loop RGEs for all Pati-Salam Dirac and Majorana Yukawa vertices, with gauge running and any split scalar thresholds in one scheme. Use the 2017 reduced-spectrum equations as a limiting comparator only. | Recover the parent Yukawa equalities at `M_U`, D-parity checks while unbroken, known gauge terms, and the reduced-spectrum limit. |
| 2. `M_I` boundary | Diagonalize the actual doublet mass matrix; project to **one** light SM Higgs; match `Yu,Yd,Ye,YN,MN` with explicit normalizations, phases, finite-threshold order, and a disposition for the left-triplet/type-II channel if present. | Reject nonunitary/inconsistent projectors, unfrozen phases, or a matching formula that requires an extra light Higgs or conjugate-`10_H` Yukawa. |
| 3. Below `M_I` | Use SM-plus-active-`N` running with sequential thresholds in the order obtained from the evolving Takagi masses, then SM running to chosen input scales. Do not assume every `N_i < M_I`. | Verify decoupling, scheme consistency, and that threshold order follows calculated masses rather than family labels. |
| 4. Fit inputs | Freeze a dated primary charged-fermion/CKM and neutrino dataset, renormalization scheme, matching scales, input covariance, theory errors, scalar/gauge threshold nuisance parameters, and fit objective. | Reproduce the input observables and uncertainty transformation before attempting a fit. |
| 5. Fit stages | First test charged masses plus CKM, **while still evolving the neutrino Yukawa/Majorana couplings that enter their RGEs**; then add neutrino mass splittings and PMNS data. Independently replay a surviving point and Takagi spectrum. | A validated point is one compatible benchmark, not global viability; nonconvergence is not model falsification. |

Primary running/threshold comparators include
[Antusch et al., hep-ph/0501272](https://arxiv.org/abs/hep-ph/0501272) for
sequential singlet-neutrino thresholds. Its Standard-Model-side machinery
does not supply the Babu-Khan Pati-Salam-side matching. Current candidate
input releases include [PDG 2026](https://pdg.lbl.gov/2026/) and
[NuFIT 6.1](https://www.nu-fit.org/?q=node%2F309); **no values, covariance,
mass scheme, or release are frozen for a fit by this audit**.

## Exact block and next proactive calculation

`FIT_PROTOCOL_ADMISSIBLE` would overstate the present result. Before global
optimization, ToE-Next must produce one checked **Pati-Salam flavor-theory
kernel** for the actual interval spectrum: its Yukawa/Majorana beta equations,
the one-light-doublet `M_I` projector, the induced neutrino-mass channels and
threshold order, and the perturbative matching/error convention. This is a
bounded derivation task that can be done **by the project**; it does not
require waiting for a new published fit. Its first fail-fast test is whether
the reduced-spectrum/decoupling limits and the scalar eigenvector reproduce
their known source expressions. Only a passing kernel would justify freezing
data and admitting a charged-sector fit. No downstream BNV evolution,
proton-decay lifetime, or source-model switch follows from this audit.
