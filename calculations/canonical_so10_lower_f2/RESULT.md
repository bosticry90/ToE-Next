# Lower PS-to-SM one-loop F² continuation

**Disposition: `LOWER_BOUNDARY_MATCHING_BLOCKED`, with the lower massive-vector `F²` sector now derived in the frozen partial-background-field Feynman gauge.** The complete physical lower-boundary formula is still unavailable because the PS-side scalar EFT and its heavy/light subtraction have not been frozen. This is not a gauge-unification failure. `PS_THRESHOLD_KERNEL_BLOCKED`, `GAUGE_MATCHING_BLOCKED`, and `BFB_UNRESOLVED` remain. No upper-boundary kernel or scale solve was attempted.

## Lower-boundary pass checklist

| Required item | Status | Evidence/limit |
| --- | --- | --- |
| Frozen gauge and operator convention | **PASS** | Partial background-field `zeta=1`, common unbroken-SM background gauge, `MSbar`, `-F_a²/4` normalization. |
| Physical 12+9 vector orbit and masses | **PASS, inherited** | [Lower quadratic check](../canonical_so10_lower_bfm/RESULT.md). |
| Hypercharge projector and broken-vector index | **PASS, inherited/replayed** | `alpha_1^-1=(2/5)alpha_4^-1+(3/5)alpha_R^-1`; `T=(14/5,0,1)`. |
| Vector + Goldstone + ghost finite and log `F²` term | **PASS in `zeta=1` slice** | Exact dimensional heat-kernel derivation below and [script](check_vector_f2.py); agrees with the published one-loop comparator. |
| Heavy SM-charged fermion threshold | **ZERO at this order and vacuum** | Complete `16_F` projected indices coincide; the `126_H`-generated `nu_R` mass is SM-neutral. No light-Higgs VEV or vectorlike fermion is introduced. |
| PS-side physical scalar content and heavy/light subtraction | **OPEN** | A delayed-decoupling candidate scheme passes an exact log checksum, but its PS-covariant EFT operator construction is not certified. |
| Complete lower beta jump and matching-scale cancellation | **OPEN** | Only the vector and complete-family fermion pieces are checked; scalar interval content is absent. |
| Full matched lower coupling, including all finite pieces | **OPEN** | No complete UV/EFT hard-region supertrace or PS-side scalar action has been evaluated. |

`LOWER_BOUNDARY_MATCHING_PASS` requires **all** rows to pass, not just the vector loop.

## Massive-vector hard `F²` term

For external unbroken SM background gauge fields at the frozen stationary vacuum, the nine PS/SM massive vectors form SM representations and their physical mass operator commutes with SM generators. We use the [partially fixed background-field construction](https://arxiv.org/pdf/2404.11640), with its heavy-vector gauge parameter frozen to `zeta=1` and the same unbroken-SM background gauge on the UV and EFT sides. In this slice, the quadratic vector operator is of Laplace type,

```text
Delta_1^{mu nu}=(-D²+M_V²) delta^{mu nu}-2 Omega^{mu nu},
Delta_0=-D²+M_V²,
Gamma_V^(1)=(1/2) Tr log Delta_1-(1/2) Tr log Delta_0.
```

The last term is the combined one-real-Goldstone plus one-complex-ghost contribution per real broken generator. In `d=4-2 epsilon`, the standard flat-space Laplace heat-kernel `F²` coefficient is `tr[(1/12)Omega_{mu nu}Omega^{mu nu}+(1/2)E²]`. The spin-one endomorphism `E_{mu nu}=-2 Omega_{mu nu}` gives `tr_L(E²)/(2 Omega²)=-2`; the Lorentz identity contributes `d/12`. Thus the combined coefficient per real broken direction is

```text
A(d) = (1/2)(d/12-2) +(1/2)(1/12) -(1/12)
     = -7/8 - epsilon/12.
```

The first term is the vector, the second the Goldstone, and the third the complex Faddeev--Popov ghost. A single real scalar has coefficient `+1/24`, so the vector-system logarithmic weight is `-21` times the real-scalar weight, reproducing the independently checked `-7T/2` beta jump. In `MSbar`, multiplying `A(d)` by the subtracted dimensional pole leaves `-A(0) log(M²/mu²)+A'(0)`, hence a finite-to-`log(M²/mu²)` ratio of `-2/21`. With the beta-slope normalization fixed, this is the conventional finite vector term:

```text
lambda_a^V(mu) = T_a [1 - 21 log(M_charged/mu)],
T=(14/5,0,1),
M_charged²/(g_10² omega²)=0.005.
```

The ninth broken vector has `M²/(g_10² omega²)=0.025` but is an SM singlet, so it contributes no SM `F²` term. Both the finite coefficient and the log agree with [Schwichtenberg, Eq. (8)](https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1), used here as an independent conventional comparator, not as a substitute for the benchmark-specific scalar subtraction. The exact ratio, Lorentz trace sign, group projector and beta-slope checks are in [`check_vector_f2.py`](check_vector_f2.py).

In the convention `alpha_low^-1=M[alpha_PS^-1]-lambda/(12 pi)`, `d lambda^V/d log(mu)=21T` cancels the vector contribution `b_high-b_low=-7T/2` to the one-loop matching-scale derivative. This is a **vector-sector cancellation only**, not the complete lower-boundary checksum. Freezing `zeta=1` is sufficient for this bounded derivation; it does not establish independence under arbitrary gauge-fixing choices or assert that individual off-shell terms are independent.

## Fermion and scalar disposition

For each complete `16_F`, the Weyl-fermion Dynkin-index sums above the lower boundary are `(2,2,2)` for `(SU4,SU2L,SU2R)`. Projecting to `(U1,SU2L,SU3)` gives `(2,2,2)`, exactly the sum of `Q,u^c,d^c,L,e^c,nu^c` below. The `nu^c` entry has zero SM index, and the frozen high-scale vacuum has no electroweak Higgs VEV to mix it with SM-charged fermions. Its unfitted Majorana mass therefore does not prevent this **one-loop gauge-index** cancellation. This does not solve the flavor or right-handed-neutrino threshold problem for other observables.

The scalar calculation does not close. The existing physical SM-side trace includes all 290 heavy real scalar modes after removing 33 gauge Goldstones, the PQ Goldstone and four tuned Higgs directions. It is basis invariant, but it is a direct broken-phase trace, not an `M_I` versus `M_U` field split. A lower scalar formula would require the renormalized PS EFT's retained field/operator content and quadratic operator, then subtraction of its light loops from the parent hard region. Merely selecting broken-phase eigenstates by mass or assigning mixed eigenstates to named PS multiplets would define a new prescription without authority. The previously checked `sigma -> 0` spectrum is nonstationary and cannot supply physical threshold masses. Hence the scalar term and full lower beta jump are not yet **admitted** for the actual two-boundary model.

For an admitted lower heavy-scalar projector `P_I`, the minimal scalar determinant would contribute the familiar `MSbar` dimension-four term `lambda_a^S=(1/2)Tr[P_I T_a² log(M_S²/mu²)]`, with no analogous standalone vector finite-Casimir constant. The physical 290-mode trace is already implemented in the [prior matrix-log check](../canonical_so10_matrix_threshold/RESULT.md); what is missing is authority for `P_I` as a PS-EFT heavy/light subtraction, not another diagonalization.

There is, however, a concrete possible resolution that we tested rather than assuming impossible. One could define a deliberately non-minimal *delayed-scalar-decoupling* PS scheme: integrate the 24 upper heavy vectors at the upper boundary but retain all physical scalar degrees of freedom in the PS EFT until `M_I`, even if some masses are of order `M_U`. Such a mass-independent scheme would contain large compensating logs but could be legitimate if its PS-covariant tree-level action, nonlinear Goldstone treatment, and induced-operator power counting are derived. Algebraically, it would put the existing 290-heavy-scalar SM matrix-log trace entirely at the lower boundary.

The exact [candidate-scheme checksum](check_delayed_scalar_candidate.py) passes. The projected upper-coset Goldstone index is `(26/5,6,4)`; subtracting it from the original scalar `b=(14,14,14)` and then subtracting the light Higgs `(1/10,1/6,0)` gives the candidate PS/SM scalar beta jump. Combined with the lower vector pure-gauge jump and its eaten Goldstones, the total is

```text
b_PS,projected - b_SM = (83/30, 77/6, 29/3),
d lambda_candidate/d log(mu) = (-83/5, -77, -58),
d lambda_candidate/d log(mu) + 6(b_PS,projected-b_SM) = 0.
```

This is a **conditional log checksum**, not a completed EFT match. In particular, retaining heavy scalars below their masses and removing upper gauge Goldstones while the lower `126_H` VEV is nonzero requires an explicit PS-covariant field/operator map; possible higher-dimensional gauge-kinetic operators must be power counted. Tree-level elimination of upper vectors can generate current-current operators schematically `J_A^mu J_{A mu}/M_U²`. If a retained scalar has mass of order `M_U`, its loop can make such operators relevant to the finite `F²` term without a small mass ratio. No map or suppression bound has been derived or accepted, and a matching-scale identity by itself cannot certify one. The candidate therefore does not change `LOWER_BOUNDARY_MATCHING_BLOCKED`.

This exposes a sequencing dependency in the requested lower-first strategy: **the lower vector loop can be completed first, but the actual-spectrum lower scalar match requires at least a tree-level/power-counted definition of the high-side PS EFT.** That definition may be established before the *upper one-loop* calculation, but it cannot be skipped. The separate upper one-loop kernel was not started here.

## Reproduction and authority

From the repository root:

```text
python calculations/canonical_so10_lower_f2/check_vector_f2.py
python calculations/canonical_so10_lower_f2/check_delayed_scalar_candidate.py
python calculations/canonical_so10_lower_bfm/check_quadratic_orbits.py
python calculations/canonical_so10_ps_threshold_kernel/check_vector_matching_indices.py
python calculations/canonical_so10_matrix_threshold/check_vector_matrix_log.py
```

The scripts use exact SymPy rationals for the dimensional coefficient, finite/log ratio, group Casimirs, complete-family index cancellation, candidate all-scalar beta jump, and matching-scale derivatives. The vector script also has an explicit Lorentz-matrix replay of the spin-endomorphism sign. The first unearned step is a frozen PS-side EFT scalar field/operator prescription and its full UV/EFT hard-region `F²` subtraction. Do not infer `M_I`, `M_U`, `alpha_U`, or benchmark viability from this partial result. The Babu--Khan BNV results and the canonical scalar benchmark remain at their previous authority ceilings.
