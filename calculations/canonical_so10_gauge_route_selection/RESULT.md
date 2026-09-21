# Canonical gauge-route selection

## Disposition

\[
\boxed{\texttt{ADMIT\_DIRECT\_MATCHING\_FEASIBILITY}}
\]

The next bounded calculation should be a one-step physical-vacuum
`Spin(10) -> SM` background-field match. This is an admission to calculate,
not a gauge-matching result and not an abandonment of the Pati--Salam route.

The exact/nonlocal two-boundary PS route could ultimately provide the higher
authority because it would resum the two bands through an intermediate EFT.
For the frozen benchmark, however, it now requires a complete nonlocal scalar
and vector functional calculation plus an interval subtraction whose finite
local surrogate has failed several control gates. The direct route reuses the
already-certified physical SM mass operators, for which

\[
[M^2,T_{\rm SM}]=0,
\]

and its physical logarithms are material but not parametrically fatal.

`BFB_UNRESOLVED` remains explicit.

## Direct physical-spectrum logarithms

The frozen physical spectrum contains 290 positive scalar real directions,
organized into 53 mass eigenvalues in the SM multiplicity ledger, and 33
massive vectors. The comparison uses the coarse \(g_U=0.5768665\) only to
turn the exact vector Gram ratios into diagnostic masses. It does not fit
\(g_U\), \(\omega\), or a GeV scale.

Choosing the lightest integrated state as a diagnostic matching scale gives

\[
\frac{\mu_{\rm ref}}{\omega}=0.0379828,
\qquad
\frac{m_{\rm max}}{\omega}=1.13404.
\]

Thus

\[
\frac{m_{\rm max}}{m_{\rm min}}=29.8567,
\qquad
\ln\frac{m_{\rm max}}{m_{\rm min}}=3.39641,
\]

or \(6.79282\) when written as a mass-squared logarithm. This is large enough
that the logs cannot be ignored, but it is not by itself a parametrically
large fixed-order expansion parameter.

Using the coarse coupling only as a diagnostic,

\[
\frac{\alpha_U}{4\pi}\ln\frac{m_{\rm max}}{m_{\rm min}}
=0.00716.
\]

Multiplying this by the largest total scalar and vector index sums gives

\[
0.0942\quad\text{and}\quad0.0573,
\]

respectively. These are not precision error bars: two-loop mixed gauge,
scalar, and Yukawa terms have not been computed. They do show that the direct
one-loop calculation has a credible perturbative feasibility window rather
than an automatically order-one logarithmic expansion.

## Representation-weighted one-loop comparator

At the same reference scale, the already-certified physical scalar ledger
gives

\[
\Delta\alpha^{-1}_{S}=(-4.80417,-4.87358,-4.99054),
\]

whose nonuniversal spread is

\[
0.18637.
\]

Applying the previously derived universal massive-vector finite/log form as a
**comparator**, not yet as direct-matching authority, gives

\[
\Delta\alpha^{-1}_{V}=(6.51194,7.48032,5.00008),
\]

with spread \(2.48024\). Their comparator sum is

\[
(1.70776,2.60674,0.00954),
\]

with maximum pairwise spread

\[
\boxed{2.59720}.
\]

This is comparable to the earlier coarse required displacement

\[
2.0270\text{--}2.9662.
\]

Therefore the direct calculation is not merely feasible; it is potentially
decisive for this benchmark. These numbers are matching-scale- and
scheme-incomplete comparators. They must not be read as a unification pass,
a fitted threshold, or a prediction.

## Route comparison

| Criterion | A: exact/nonlocal PS match | B: direct physical-vacuum match | C: replacement benchmark |
|---|---|---|---|
| Physical mass authority | Requires reconstructing a PS interval subtraction despite borderline modes | Uses the certified stationary broken-phase masses directly | Would require a new scalar/Higgs search |
| Generator/mass commutation | Fails for the physical upper PS generator and needs divided-difference kernels | Passes for unbroken SM generators | Unknown until a new point is found |
| Remaining functional work | Complete 132-real scalar source, nonlocal determinant, nondegenerate vector/Goldstone/ghost determinant, PS hard subtraction, two matching-scale checks | One common-scheme UV/EFT BFM subtraction, all-33 vector replay, direct beta-jump/scale cancellation, coupled scale solve, two-loop uncertainty | Full benchmark optimization and replay before matching |
| Log treatment | Best eventual resummation if completed | Fixed order; largest physical mass log `3.396` | Potentially better, but not demonstrated |
| Additional assumptions | Needs an interval-field definition not yet controlled locally | Needs no artificial PS assignment of mixed physical states | Adds benchmark-selection criteria and new tuning choices |
| Implementation cost | High | Medium | High and scientifically premature |
| Authority achievable next | Full two-boundary matching only after substantial unresolved work | Bounded one-step one-loop verdict with explicit truncation uncertainty | Existence of another point, not a verdict for this point |
| Selection | Deferred, not rejected | **Admit feasibility calculation** | Not admitted |

Route B is selected because it can confront the benchmark with measured gauge
couplings using less unearned structure, while its largest logarithms remain
within a credible one-loop feasibility regime. Route A remains scientifically
valid but is no longer the cheapest next discriminator. Route C is premature
because neither matching language has failed for the current point.

## Minimal admitted direct calculation

The next calculation may do only the following:

1. Freeze one `MSbar` background-field gauge and a low-energy SM field
   content containing the tuned Higgs and PQ mode as appropriate.
2. Construct the full UV and EFT quadratic fluctuation operators at the
   physical stationary vacuum.
3. Integrate all 33 massive vectors with their Goldstones and ghosts once,
   and all 290 positive physical scalar directions once, using basis-invariant
   SM spectral functions.
4. Re-derive the finite and logarithmic massive-vector coefficient for all
   vector mass bands in the same direct UV/EFT subtraction scheme; the lower
   coefficient is a comparator, not transferable authority.
5. Verify the direct `Spin(10)/SM` beta jump, matching-scale cancellation,
   degenerate limits, and basis invariance.
6. Solve the one-loop measured-coupling equations jointly for
   \(g_{10}\) and \(\omega\) only after the kernel passes.
7. Quantify two-loop/log truncation uncertainty before returning any gauge
   verdict.

Right-handed neutrino masses remain unfitted, but they are SM gauge singlets
and do not contribute to this one-loop gauge-kinetic threshold. No broader
fermion/flavor authority is inherited from that fact.

## Explicit nonclaims

This result does not establish:

- gauge unification;
- a physical value of \(M_I\), \(M_U\), \(g_U\), or \(\omega\);
- that direct matching is more accurate than a completed exact PS match;
- global boundedness, flavor, neutrino phenomenology, proton stability, or
  assumption compression;
- rejection of the PS subgroup, the frozen benchmark, or the canonical
  action.

The prior `PS_EFT_ERROR_UNRESOLVED` result remains valid for the attempted
finite local PS split. This calculation changes only the project admission
rule: a direct feasibility calculation is now allowed in parallel scientific
logic, although no full direct match has begun here.

## Reproduction

Run:

```powershell
python calculations/canonical_so10_gauge_route_selection/select_route.py
```

The machine-readable output is `route_selection.json`.
