# Physical lower-boundary background-field matching attempt

**Disposition: `LOWER_BOUNDARY_MATCHING_BLOCKED`.** The physical
`PS -> SM` quadratic broken-gauge sector passes a new mass-pairing check,
but the complete one-loop `F^2` matching coefficient has not been derived.
The upper `Spin(10) -> PS` kernel and the coupled gauge-scale solve were
therefore **not started**. Carry `BFB_UNRESOLVED`.

## Gauge-fixing convention and what it permits

The calculation is organized in a mass-independent `MSbar` scheme with a
partially fixed background-field gauge for the heavy `PS/SM` coset and a
separate background-field gauge for the unbroken SM. For a diagonal heavy
vector mass basis, the partial gauge condition is

```text
G_i = d_mu V_i^mu - zeta M_i chi_i,
L_gf = -(1/(2 zeta)) G_i G_i.
```

It cancels vector--Goldstone kinetic mixing and gives both Goldstone and
heavy-ghost quadratic masses `zeta M_i^2`. This prescription and its
hard-region matching construction are given by [Thomsen, Eqs. (3.31)--
(3.36) and (4.33)](https://arxiv.org/pdf/2404.11640). That paper says the
corresponding soft-region cancellation was not demonstrated for the
*ordinary* background-field gauge in this setting; it does **not** prove
ordinary gauge impossible. The source also makes clear that a hard-region
formula is a statement about a consistently gauge-fixed full UV/EFT
functional, not about vector masses alone.

## New physical-vacuum check

[`check_quadratic_orbits.py`](check_quadratic_orbits.py) builds the orbit map
`Q` directly from the frozen `54_H` and `126_H` VEVs and the 21 exact
Pati--Salam generators. With the vector-index-one convention and
`omega^2=60`, `M_V^2/(g_10^2 omega^2)=Q^T Q`. The result is:

| Subspace | Real generators | `M_V^2/(g_10^2 omega^2)` |
| --- | ---: | ---: |
| unbroken SM | 12 | 0 |
| broken charged PS/SM | 8 | 0.005 |
| broken neutral PS/SM | 1 | 0.025 |

The whole PS Gram agrees with the PS principal submatrix of the
independently built physical 45-adjoint vector operator to `1e-12`.
Singular-value duality then gives the same nine **nonzero** eigenvalues
for `Q^T Q` and `Q Q^T`; at `zeta=1/2, 1, 5/2`, the gauge-fixed heavy
ghost and Goldstone masses pair as `zeta M_V^2` to `1e-12`. The 12 zero
eigenvalues in PS generator space are unbroken SM directions, not heavy
ghosts or Goldstones. This confirms the *quadratic* partial-gauge setup
under the already-frozen kinetic/orbit normalization. It does not test
the gauge-background vertices or cancellation of `zeta` in an `F^2`
coefficient.

The independent exact group check
[`check_vector_matching_indices.py`](../canonical_so10_ps_threshold_kernel/check_vector_matching_indices.py)
gives lower broken-vector index `(T_1,T_2,T_3)=(14/5,0,1)` and the
universal vector-sector logarithmic beta-jump relation
`b_high-b_low=-(7/2)T`. The physical adjoint matrix-log replay
[`check_vector_matrix_log.py`](../canonical_so10_matrix_threshold/check_vector_matrix_log.py)
locates that index in the eight `0.005` vectors and confirms that the
neutral `0.025` vector has zero SM index. These are log and group
checks, **not** a boundary-wide beta jump including all active scalars,
fermions, finite constants, and subtraction terms.

As a comparator only, the conventional one-loop threshold expression
([Schwichtenberg, Eq. (8)](https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1))
would assign the lower vector sector a finite Casimir/index term
`(14/5,0,1)` and a log term
`-21(14/5,0,1) log(M_charged/mu)`, with
`M_charged^2/(g_10^2 omega^2)=0.005`. The neutral broken vector has no
SM gauge index. This is **not** substituted for the unperformed
background-field derivation or the full lower matching coefficient.

## First unearned step

The actual hard-region supertrace must be formed from the full
background-dependent fluctuation operator, including heavy vectors,
eaten Goldstones, heavy and light ghosts, physical scalar fields,
heavy/light mixing, and the consistently gauge-fixed EFT comparison.
It must then be expanded to the SM gauge-kinetic `F^2` terms. We have
not evaluated the resulting two-point integrals or their finite parts.
Consequently, none of the following has been certified here:

- cancellation of gauge-fixing dependence in the **matched** gauge
  coupling (as distinct from intermediate off-shell terms);
- finite massive-vector constants in the declared scheme;
- a complete PS-side active-field prescription and the lower-boundary
  scalar/fermion contribution;
- a separate lower-boundary matching-scale derivative cancellation.

The [primary matching construction](https://arxiv.org/pdf/2404.11640)
states that the one-loop matching formula depends on the gauge-fixing
choices. A raw off-shell term should therefore not be required to be
individually gauge-parameter independent; the comparison must first
specify matched fields, operators and scheme. Treating equality of the
Goldstone and ghost masses as an `F^2` cancellation would be precisely
the false promotion this gate is designed to prevent.

At the upper boundary there is an additional, separate issue: the
physical lower `126_H` VEV breaks PS, so a broken-phase extraction of
one *renormalizable* PS gauge coupling needs a declared EFT expansion
and treatment of PS-invariant higher-dimensional gauge-kinetic
operators. A spectral two-mass kernel is required for noncommuting mass
and PS-generator matrices, but such a kernel by itself does not define
the retained PS operator basis. That issue was **not** calculated here.

## Reproduction and carry-forward

From the repository root:

```text
python calculations/canonical_so10_lower_bfm/check_quadratic_orbits.py
python calculations/canonical_so10_ps_threshold_kernel/check_vector_matching_indices.py
python calculations/canonical_so10_matrix_threshold/check_vector_matrix_log.py
```

The script prints `LOWER_BFM_QUADRATIC_ORBIT_PASS`; this must not be
confused with `PS_THRESHOLD_KERNEL_PASS`. The point and parent-action
hashes are in [`RECORD.md`](RECORD.md). No benchmark parameter, physical
GeV scale, GUT coupling, flavor input, or Babu--Khan threshold was changed.
Next authority would require a complete lower hard-region `F^2` match
and independent check, then the nondegenerate upper match in a frozen PS
EFT operator basis. Until both pass, retain `GAUGE_MATCHING_BLOCKED`.
