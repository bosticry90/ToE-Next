# Canonical positive-Higgs point: gauge-matching boundary

**Disposition: `GAUGE_MATCHING_BLOCKED`.** This is a source-derived canonical
`Spin(10)` point, not the published Babu--Khan scalar benchmark. Its global
quartic status remains **`BFB_UNRESOLVED`**. The calculation has generated a
complete *SM-side* scalar mass/one-loop-index ledger and a heavy-vector mass
ledger, and has derived and tested the normalized tree matching and a coarse
one-loop crossing. It has **not** generated the PS-covariant split-threshold
and heavy-vector matching kernel needed to say this point passes or fails
actual-spectrum gauge unification. No GeV scale is assigned to the point.

## Earned threshold ingredients

[`scalar_sm_ledger.json`](scalar_sm_ledger.json) evaluates all 35 frozen
SM-irrep Hessian blocks at the exact-defined positive-Higgs point. In the
canonical kinetic metric and units of `omega`, it accounts for all 328 real
scalar directions: 38 zero (33 gauge, one PQ, four tuned Higgs) and 290
strictly positive heavy. For each eigenvalue it records the SM irrep,
`m²/omega²`, and its one-loop `(b1,b2,b3)` index if active. The light Higgs
pair reproduces `(1/10,1/6,0)`; conjugate irreps are kept together in the
real-dimension count, rather than counting each as an independent complex
field. The lightest positive state is a neutral singlet at
`m²/omega² = 0.00144269`; a colored `(3,1,+1/3)+c.c.` scalar pair is at
`m²/omega² = 0.00171831`. These masses invalidate a blanket assertion that
every colored scalar decouples at `M_U` or that one-Higgs SM running is exact
up to `M_I`. The generated affine-block cache passed its direct exact-block
regression, and the frozen point already has a separate direct-parent,
high-precision replay. The ledger itself is a derived double-precision
inventory, not a new exact eigenvalue certificate.

[`vector_ledger.json`](vector_ledger.json) uses the frozen kinetic VEVs and
standard vector-index-one generator normalization
`Tr_10(T_a T_b)=delta_ab`. The raw plane generators are divided by
`sqrt(2)`, so `M_V²/(g_10² omega²) = Gram_eigenvalue/120`. There are 12
unbroken SM vectors; the 9 PS-to-SM vectors split into eight at raw Gram
`0.6` and one at `3`; the 24 first-stage vectors split into twelve at `50`
and twelve at `50.6`. An independent adjoint-hypercharge projection
distinguishes the `Y=±2/3,±1,0,±5/6,±1/6` mass sets. Adjoint branching
supplies their SM representation labels; a full independent SU(3)/SU(2)
projector is still desirable before finite vector thresholds. The ratio of
lightest first-stage to intermediate vector masses ranges from `4.08248`
(against the heaviest intermediate mode) to `9.12871` (against the lightest).
The standard gauge kinetic normalization is an **explicit matching
convention**, not a scalar-potential prediction; these mass ratios are
independent of the common coupling and normalization.

The parent PS content, before PS breaking and without assigning a single
mass to a split broken-phase eigenstate, is
`54_R=(1,1,1)+(20',1,1)+(6,2,2)+(1,3,3)`,
`10_C=(6,1,1)+(1,2,2)`, and
`126_C=(6,1,1)+(10,3,1)+(10bar,1,3)+(15,2,2)`.
Those representation identities do **not** alone specify which multiplets
are active at each threshold of this particular point.

## Matching and coarse diagnostic

The normalized SU(4) generator is
`T15=diag(1,1,1,-3)/(2 sqrt(6))`, with
`Tr_4(T15²)=1/2` and `(B-L)/2=sqrt(2/3) T15`. Thus

```text
Y = T3R + (B-L)/2
alpha_Y^-1 = alpha_2R^-1 + (2/3) alpha_4C^-1
alpha_1^-1 = (3/5) alpha_2R^-1 + (2/5) alpha_4C^-1
```

where `alpha_1=(5/3)alpha_Y`. D parity enforces
`alpha_2L=alpha_2R` in the PS interval before its breaking; at tree level
`alpha_3=alpha_4C` and `alpha_2=alpha_2L` at `M_I`.
[`verify_group_normalization.py`](verify_group_normalization.py) checks the
generator trace, B-L factor, and vector generator norm exactly. These are
tree identities, not finite one-loop matching formulas.

As a deliberately **coarse diagnostic only**, put one Higgs below `M_I`,
keep complete complex `10_H+126_H` multiplets between the boundaries,
decouple `54_H` at `M_U`, omit all split thresholds and finite matching, and
use the one-loop convention `d alpha_i^-1/d ln mu=-b_i/(2 pi)`. Three
`16_F` generations yield PS fermion Dynkin sum 6 per factor. The complex
`10_H` contributes index `(1,1,1)` and `126_H` contributes `(35,35,35)`;
therefore `b_(4,L,R)=(4/3,26/3,26/3)`. Complete additional `54_H` or
`10_H` multiplets shift all three factors equally and do not change the
important difference `b_L-b_4=22/3`.

Using the same-scheme illustrative inputs
`alpha_EM,MSbar^-1(M_Z)=127.930`,
`sin²theta_MSbar(M_Z)=0.23122`, `alpha_s(M_Z)=0.1180`, and
`M_Z=91.1876 GeV`, the diagnostic equations give

```text
M_I = 5.05e13 GeV
M_U/M_I = 51.84
M_U = 2.62e15 GeV
alpha_U^-1 = 37.76, g_U = 0.577
```

The electromagnetic and weak-angle input convention follows the
[PDG GUT review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf);
the strong-coupling central value is from the
[PDG QCD review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-qcd.pdf).
[`coarse_one_loop.py`](coarse_one_loop.py) supplies the reproducible
algebra. The **coarse** crossing is perturbative but asks for an interval
ratio much larger than the vector mass-band ratios `4.08--9.13`.
Identifying those bands with the two matching boundaries would require an
effective `alpha_L^-1-alpha_4^-1` threshold displacement of roughly
`2.03--2.97`. This is a target for the actual threshold calculation, not
evidence that the required correction is impossible. Changing the choice of
matching scales and treating the split scalar/vector states can move the
diagnostic result.

## Exact blocking condition and next bounded derivation

Stage B cannot be certified by assigning the broken-phase SM eigenmasses to
degenerate PS irreps. After the `126_H` VEV, mass eigenstates mix and split
across the parent PS multiplets. A full threshold prescription must derive
the PS-covariant active-multiplet/mass map on the high side of `M_I`, the
broken-to-unbroken one-loop matching at both boundaries (including heavy
vectors, Goldstones and the scheme-dependent finite terms), and a consistent
choice of `M_I,M_U` tied to the same canonical VEVs. The current 35-block
SM Hessian and vector Gram do not supply that map by themselves. Importing
published Babu--Khan scalar thresholds would violate this point's
provenance. Stage A cannot be promoted into `GAUGE_MATCHING_FAIL`, and no
Stage C two-loop, flavor, or proton-decay calculation was started.

The next calculation, if admitted, is therefore a **canonical PS split-
threshold matching kernel**: construct PS multiplet projectors and their
mass/mixing evolution from the parent action, derive the one-loop decoupling
constants in a named scheme, and independently replay their group indices.
Only then solve the coupled physical-scale equations. The present outcome
rejects neither the benchmark nor the model class; it records the precise
missing map that stands between a coarse crossing and a falsifiable
actual-spectrum test.

## Reproduction

From the repository root:

```text
python calculations/canonical_so10_scalar_benchmark/verify_compiled_blocks.py
python calculations/canonical_so10_gauge_matching/build_sm_threshold_ledger.py
python calculations/canonical_so10_gauge_matching/build_vector_ledger.py
python calculations/canonical_so10_gauge_matching/verify_group_normalization.py
python calculations/canonical_so10_gauge_matching/coarse_one_loop.py
```

The SM scalar masses and beta indices, vector Gram/hypercharge sets, and
coarse one-loop numbers are preserved as calculation-local JSON files.
