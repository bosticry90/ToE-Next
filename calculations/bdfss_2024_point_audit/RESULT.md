# Audit of the 2024 Normal-Ordering SO(10) Point

## Decision and authority ceiling

```text
subject = arXiv:2409.03840v1, Appendix A normal-ordering point
outcome = POINT_INTERNALLY_INCONSISTENT_FOR_OUR_PURPOSE
printed_matrix_reconstruction = PASS
GUT_scale_Majorana_Takagi_check = PASS
same_point_PS_threshold_ordering = NOT_FROZEN
real_120_SO10_reality_check = FAIL_FOR_UNCHANGED_POINT
omitted_PS_flavor_running = NOT_QUANTITATIVELY_BOUNDED
source_theory_selected = false
downstream_BNV_running_started = false
```

The printed point is a reproducible numerical solution to the **mass relations
used in the 2024 paper**. It is not a ready, single initial condition for a
controlled `SO(10) -> Pati-Salam -> SM+N` recovery chain. The result is about
this printed point, not a refutation of the `10_R+120_R+126bar` model class.
The later reality-condition result is a 2026 primary preprint; its parent-group
sign derivation has not been reproduced here. The conditional algebraic
consequence for the 2024 point *has* been independently checked.

## Sources and frozen inputs

1. [Babu, Di Bari, Fong and Saad, arXiv:2409.03840v1](https://arxiv.org/html/2409.03840):
   Eqs. (8)-(14), Appendix A Eqs. (132)-(138), GUT-scale fit
   `M_GUT=2 x 10^16 GeV` in section 4.1, right-handed-neutrino values in
   Eq. (59) and Appendix C, and the illustrative gauge-threshold spectrum
   in section 6 with `M_int ~ 10^14 GeV`.
2. [Saad and Susic, arXiv:2604.04021v1](https://arxiv.org/html/2604.04021):
   Eq. (7) and Eqs. (89)-(94) derive opposite reality-conjugation signs for
   the `120_R` `(1,2,2)` and `(15,2,2)` components, rather than the same
   sign used in the 2024 mass relations. This is a later source-level
   correction, not a change silently imposed on the historical fit.
3. [Meloni, Ohlsson and Riad, arXiv:1612.07973v3](https://arxiv.org/html/1612.07973):
   an independently published `10+120+126` Pati-Salam Yukawa-RGE treatment.
   Its abstract reports that SM-like evolution from the same GUT inputs can
   differ substantially. That number is **not** used as a bound for the 2024
   point; the spectrum and fit details differ.

The computation is in [`verify_point.py`](verify_point.py). It uses only the
paper's printed decimal precision and machine-local NumPy. No old repository
file, fit engine, RGE package, or D: payload was used.

## Matrix reconstruction and Takagi test

In the paper's basis, `S` is real positive diagonal, `D` complex symmetric,
and `A` complex antisymmetric. The script transcribes Appendix A and forms

```text
M_U   = D + S + A
M_D   = D + r1*S + exp(i*phi)*A
M_E   = D - 3*r1*S + r2*A
M_nuD = D - 3*S + conj(r2)*exp(i*phi)*A
M_N   = c_R*S
```

It checks symmetry/antisymmetry and finite entries. Because `M_N` is already
positive diagonal in this printed basis, its Takagi rotation is the identity;
singular-value decomposition independently confirms its masses. At the
**printed GUT input scale**:

| State | Reconstructed `M_N` (GeV) | Rounded Eq. (59) (GeV) |
|---|---:|---:|
| `N_1` | `6.57071145e4` | `6.57e4` |
| `N_2` | `2.08096637e12` | `2.08e12` |
| `N_3` | `8.10503509e14` | `8.10e14` |

The largest relative difference from the paper's **rounded** Eq. (59) is
`6.22e-4`, within its displayed precision. Appendix C quotes scale-evolved
values at `M_2` (including `N_3 ~ 7.51e14 GeV`); mixing those with the
GUT-input numbers would be a scale error, not a discrepancy to resolve by
averaging. No low-energy observable, leptogenesis result, or proton lifetime
was replayed.

## Reality-condition falsifier

The 2024 source treats both real-`120_H` Pati-Salam doublets as having the
same up/down conjugation sign. Let their *up-type* coefficients before
absorbing the common antisymmetric Yukawa matrix be `x` for `(1,2,2)` and
`y` for `(15,2,2)`, with the latter normalized so its quark Clebsch is `1`.
Then the up-sector coefficient is `u=x+y`. Under the 2026 parent-`SO(10)`
reality relation, the down and charged-lepton coefficients are

```text
d = x* - y*
e = x* + 3*y*
d + e = 2*(x+y)* = 2*u*
```

After normalizing the up-sector antisymmetric matrix to `A = u times Y_120`, any
unchanged physical point must therefore have `|d/u + e/u|=2`, independent of
the common matrix normalization, family basis, or overall `120_H` sign.
The 2024 point instead sets `d/u=exp(i*phi)` and `e/u=r2`, with

```text
exp(i*phi) = 0.217952778 - 0.975959316*i
r2         = -0.355963000 + 1.252890000*i
|exp(i*phi) + r2| = 0.309414649, not 2
```

An independent SymPy simplification gives exactly zero for
`q+r-2*conj(x+y)/(x+y)`; a separate complex-arithmetic replay reproduces
`0.309414649`. The `1.690585351` modulus gap is not a printed-decimal effect. Thus the
published **unchanged** mass-matrix point fails this necessary corrected
real-`120_H` condition. This is our algebraic inference from the two primary
sources, not a statement that the 2026 authors explicitly tested Appendix A.
One could attempt a fresh corrected fit; substituting a sign into the old
point or keeping its published neutrino masses would not be that fit.

## Scale and field-content check

The paper chooses `M_GUT=2e16 GeV` for the fermion fit. Its separate
gauge-threshold illustration obtains `M_GUT ~ 1e16 GeV` and
`M_int ~ 1e14 GeV`; it does not print one co-frozen gauge/flavor point with
exact `M_int`, full threshold spectrum, and the Appendix A matrices.
Using `1e14 GeV` *only as the paper's illustration*, the reconstructed
GUT-input `M_N3/M_int ~ 8.105`; `N_2` and `N_1` lie below it. Since the
Majorana mass arises when the `126_H` breaks Pati-Salam at `M_int`, an
SM-plus-three-`N` running sequence that integrates `N_3` at its fitted
mass **above** that breaking boundary is not automatically the EFT sequence
of this model. A different, jointly fixed `M_int` or explicit threshold
prescription could change that conclusion. The actual ordering is therefore
**not frozen**, rather than inferred from family labels or from two separate
paper plots.

Section 4.1 explicitly runs SM+type-I from `M_GUT` down, with sequential
singlet-neutrino thresholds; section 6 separately uses Pati-Salam gauge
content and scalar/gauge thresholds. The omitted interval is not merely a
small correction to one universal coefficient: it changes gauge group,
scalar/Yukawa field content, matching, and potentially the relevant `N_3`
boundary.

## Leading-log size and stopping rule

For the paper's `2e16 -> ~1e14 GeV` illustrative span,

```text
ln(M_GUT/M_int)/(16*pi^2) = 0.033551987.
```

This is the loop-log *prefactor*, **not** a bound on the flavor-matrix error.
The model-specific Pati-Salam beta matrices, vevs, thresholds, and a matched
comparison with SM+type-I evolution are required to multiply it. The related
2017 RGE study demonstrates that an SM-like substitution need not be
numerically innocuous, but its reported differences cannot be assigned to
this printed point. Because the unchanged point already fails the later
reality-condition test and lacks a co-frozen `M_int`, deriving a detailed
Pati-Salam evolution for it would be premature. The omission is classified
`NOT_QUANTITATIVELY_BOUNDED` here.

Stop here. Do not select this source model, re-fit the point, import its
neutrino spectrum into Babu-Khan, run BNV SMEFT+`N`, or derive proton
lifetimes from this point. The Babu-Khan gauge-sector recovery maps remain
unchanged. A corrected published model point would require its own basis,
scalar/threshold convention, full flavor inputs, and separate recovery
admission; this historical 2024 point is not it.
