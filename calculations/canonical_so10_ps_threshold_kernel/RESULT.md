# Canonical Pati--Salam split-threshold kernel: first stopping boundary

**Disposition: `PS_THRESHOLD_KERNEL_BLOCKED`.** The parent-representation
projectors, symmetry-restoration recombination, vector indices, and a
whole-spectrum one-loop logarithmic checksum pass. A two-boundary threshold
kernel for the frozen positive-Higgs point does **not** yet pass: the
PS-interval state/decoupling map and the finite heavy-vector--Goldstone--ghost
matching have not been derived in one specified scheme. Consequently the
previous `GAUGE_MATCHING_BLOCKED` status remains, no physical `M_I`, `M_U`, or
`alpha_U` is assigned, and `BFB_UNRESOLVED` remains explicit. No two-loop,
flavor, or proton-decay calculation was started.

## Earned structural and logarithmic results

[`certify_ps_projectors.py`](certify_ps_projectors.py) constructs exact
idempotent projectors in the frozen tensor coordinates. Their ranks give

```text
10_C  -> (6,1,1)[6] + (1,2,2)[4]
54_R  -> (1,1,1)[1] + (20',1,1)[20] + (1,3,3)[9] + (6,2,2)[24]
126_C -> (6,1,1)[6] + (15,2,2)[60] + (10,3,1)[30]
         + (10bar,1,3)[30]
45    -> PS adjoint[21] + coset (6,2,2)[24]
```

For the self-dual `126`, the 60-dimensional middle sector is separated by
the exact SO(6) Hodge projectors into two rank-30 pieces. The script checks
idempotence, mutual annihilation, decomposition, and the conjugate
orientation. These are representation projectors, **not** an admission of a
threshold assignment for their split broken-phase eigenstates.

[`check_ps_mass_limit.py`](check_ps_mass_limit.py) holds the *same parent
coefficients* fixed while scaling the `54` and `126` VEVs. It first
reproduces the frozen SM scalar mass ledger at the actual point. At
`sigma -> 0`, its 328 real eigen-directions numerically recombine into 15
PS-symmetric mass clusters, including dimensions 120, 60, 60, 24, 20, 9,
four 6s, two 4s, and three singlets. At `Phi = Sigma = 0`, they recombine
into full Spin(10) representations with real dimensions 252, 54, 10, 10,
1, and 1. The limit eigenvalues and labels are preserved in
[`restoration_limit_spectrum.json`](restoration_limit_spectrum.json).
The PS-limit 120-real-dimensional cluster has
`m²/omega² = -0.0249635944`; it is not a stable physical threshold mass.
This limit is generally **nonstationary** because the parent coefficients
were fixed at the original broken vacuum. Re-solving tadpoles along the
path would silently change the theory and is not an allowed repair.
[`replay_limit_direct.py`](replay_limit_direct.py) independently differentiates
the 29 original parent monomials and confirms eight representative limit
curvatures (including a `126` sector); the 15-cluster equality itself is a
double-precision numerical check of the frozen block compiler, not an
all-entry exact polynomial proof.

[`check_vector_limits.py`](check_vector_limits.py) gives 21 zero plus 24
equal massive gauge-orbit directions at `sigma = 0`, and all 45 zero when
both breaking VEVs vanish. [`check_vector_matching_indices.py`](check_vector_matching_indices.py)
finds exact heavy-vector index vectors

```text
Spin(10) -> PS: (T_4,T_L,T_R) = (4,6,6)
PS -> SM:       (T_1,T_2,T_3) = (14/5,0,1)
```

The normalized tree identity is
`alpha_1^-1 = (2/5)alpha_4^-1 + (3/5)alpha_2R^-1`.
The vector indices reproduce the `-7 T/2` one-loop beta discontinuity
after including the eaten real scalar. At the level of the full direct
Spin(10)-to-SM spectrum, [`check_full_log_checksum.py`](check_full_log_checksum.py)
finds scalar beta contributions `(14,14,14)`, symmetry-zero plus tuned
Higgs contributions `(43/30,7/6,5/6)`, and the required high-minus-low
beta difference `(-463/30,-49/6,-13/3)`. This agrees with the derivative
of the universal split-log formula. It is a **sum rule**, not the required
allocation of individual masses to the two breaking boundaries.

## Why the kernel stops

The published one-loop threshold convention
`alpha_low^-1 = alpha_high^-1 - lambda/(12 pi)`, with a finite Casimir term,
split vector logarithms, and a Goldstone-projected scalar logarithm, is a
useful primary-literature comparator: [Schwichtenberg, Eqs. 7--8](https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1).
That article explicitly treats a grand desert rather than this two-boundary
split spectrum. The [Meloni--Ohlsson--Pernow threshold study](https://arxiv.org/abs/1911.11411)
uses a different scalar spectrum and, for its displayed simplified
threshold formula, assumes heavy vectors coincide with the matching scale.
Neither supplies the frozen canonical point's `M_I` and `M_U` interval map
or substitutes for independently checked finite vector matching.

In particular, a broken-phase SM eigenvalue cannot be assigned wholesale
to one PS parent multiplet if its eigenspace mixes parent representations.
Conversely, the PS-restoration eigenvalue is not automatically the pole or
decoupling mass at the physical stationary vacuum. Without a frozen,
gauge-invariant active-field prescription and its mass matrices on both
sides of `M_I`, a split log can be placed in the wrong interval or counted
twice. The present checks fix total coefficients but cannot determine the
needed `2--3` inverse-coupling displacement. The finite vector/Goldstone/
ghost contribution and matching-scale cancellation **at each boundary**
also remain unverified. Thus no actual-spectrum gauge solve is authorized.

## Threshold-ledger schema for continuation

Every future row should carry: parent field/representation and exact PS
projector; SM irrep and real/complex multiplicity; physical mass function
and frozen `m/omega`; proposed EFT interval and activity flag; gauge or
global Goldstone status; `(T_4,T_L,T_R)` and `(T_1,T_2,T_3)` in the same
generator normalization; scalar/vector/fermion log coefficient; finite
constant with scheme and gauge-fixing provenance; and the matching boundary
and scale. A row must not be admitted solely from a symmetry-restoration
cluster. Conjugate and mixed eigenstates require explicit projectors and
index-preserving traces.

The continuation is specifically to derive the two-boundary background-field
decoupling map and independently replay the finite massive-vector,
Goldstone, and ghost terms. Then test degenerate logs, each boundary's beta
jump and matching-scale derivative, D-parity and hypercharge normalization,
and only afterward solve `M_I`, `M_U`, and `alpha_U` together with the
vector relation `M_V ~ g v`. A completed kernel can pass while this one
benchmark subsequently fails gauge unification; those dispositions must
remain separate.

## Reproduction

Run, from the repository root, each of:

```text
python calculations/canonical_so10_ps_threshold_kernel/certify_ps_projectors.py
python calculations/canonical_so10_ps_threshold_kernel/check_ps_mass_limit.py
python calculations/canonical_so10_ps_threshold_kernel/replay_limit_direct.py
python calculations/canonical_so10_ps_threshold_kernel/check_vector_limits.py
python calculations/canonical_so10_ps_threshold_kernel/check_vector_matching_indices.py
python calculations/canonical_so10_ps_threshold_kernel/check_full_log_checksum.py
```

The action and point hashes are frozen in [`RECORD.md`](RECORD.md). Scripts
read the preceding canonical action/Hessian and positive-Higgs point, not
the published Babu--Khan scalar tables. This result does not change the
two independently passed Babu--Khan BNV boundaries.
