# Physical-vacuum matrix-threshold continuation

**Disposition: `PS_THRESHOLD_KERNEL_BLOCKED`, with new matrix-trace controls.**
The physical-benchmark *unbroken-SM-side* scalar and vector logarithmic
traces now have basis-invariant implementations. The requested two-boundary
one-loop kernel is still **not** derived: finite vector/Goldstone/ghost
matching, gauge-parameter cancellation, and an exact `PS`-interval
active-field prescription remain outstanding. No coupled gauge-scale solve
was performed. `GAUGE_MATCHING_BLOCKED` and `BFB_UNRESOLVED` remain.

## Physical broken-phase traces that pass

[`check_scalar_matrix_log.py`](check_scalar_matrix_log.py) diagonalizes each
of the 35 physical stationary SM-irrep Hessian blocks in the canonical
kinetic metric. It excludes exactly 38 zero real directions (33 gauge, one
PQ, four deliberately tuned Higgs), leaving 290 positive heavy real
directions. With `b_a=T_a/6` per real scalar and the published convention
`alpha_low^-1=alpha_high^-1-lambda/(12 pi)`, its matrix prescription is

```text
lambda_a^S(mu) = (1/2) Tr_heavy[T_a^2 log(M_S^2/mu^2)]
               = 3 sum_heavy b_a log(m_i^2/mu^2).
```

The trace is unchanged under simultaneous unitary rotation of the mass
matrix and generator insertion within each mixed multiplicity space. It
reproduces the independently stored eigenvalue/index ledger and the
scale derivative `d lambda^S/d log(mu) = -6 b_heavy^S`. At `mu=omega`, the
SM-order `(1,2,3)` values are
`(-65.49183411,-68.10818386,-70.24021592)`; the derivative is
`(-75.4,-77,-79)`. The compact output is
[`scalar_matrix_log.json`](scalar_matrix_log.json). The numeric values are
**direct broken-phase log checks**, not a decomposition into the `M_I` and
`M_U` thresholds. No physical `omega` or GeV scale was fixed.

[`check_vector_matrix_log.py`](check_vector_matrix_log.py) reconstructs
the physical 45-dimensional adjoint vector mass Gram operator and inserts
normalized SM generators directly in its spectral projectors. The mass
windows at the stationary point have index vectors

| `M_V²/(g_10² omega²)` | Real vectors | `(T_1,T_2,T_3)` |
| ---: | ---: | ---: |
| `0.005` | 8 | `(14/5,0,1)` |
| `0.025` | 1 | `(0,0,0)` |
| `50/120` | 12 | `(5,3,2)` |
| `50.6/120` | 12 | `(1/5,3,2)` |

The sum is exactly the prior `(8,6,5)` index checksum within numerical
precision. Simultaneous orthogonal rotations of mass and generators leave
every trace unchanged; the scale derivative of the comparator logarithm
is `+21(8,6,5)`. This certifies the mass-index bookkeeping, **not** the
finite vector contribution or a gauge-independent `R_xi` calculation.

## The upper-boundary matrix-log caveat is realized at this point

For the unbroken SM generators, the vector mass operator commutes with
their adjoint actions, as verified in the script. For a PS generator
broken by the `126_H` VEV, the same commutator has norm
`0.0158113883` in the frozen dimensionless vector Gram convention; it
vanishes in the formal `sigma=0` restoration limit. Therefore an
SM-generator trace may be evaluated blockwise at the *physical* vacuum,
but replacing an upper-boundary PS background-field calculation by the
same simple trace is not justified.

The reason is structural, not a matter of naming eigenstates. A quadratic
one-loop determinant with `M²=diag(a,b)` and an off-diagonal generator
insertion has the mixed-propagator building block

```text
Tr[(p²+M²)^-1 T (p²+M²)^-1 T]
    = 1/[2(p²+a)(p²+b)]     for T=sigma_x/2.
```

Its Feynman-parameter mass dependence involves
`K(a,b)=(a log a-b log b)/(a-b)-1`, not merely the average of two
single-mass logarithms when `a != b`. The exact algebra and degenerate
limit are tested in
[`check_noncommuting_mass_warning.py`](check_noncommuting_mass_warning.py).
This is a determinant-level warning, **not** a claim that this toy `K`
alone is the complete gauge kinetic coefficient. The general need for
non-degenerate matrix matching is also treated in the primary
[universal one-loop effective-action paper](https://arxiv.org/abs/1512.03003).

## What remains unearned

The usual compact one-loop matching formula, including a finite Casimir
piece, vector logarithms, and Goldstone-projected scalar logarithms, is a
useful comparator in a specified scheme
([Schwichtenberg, Eqs. 7--8](https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1)).
Its direct use for the canonical *two-boundary, non-degenerate* stationary
point has not been established here. In particular:

- No background-field determinant including massive vectors, eaten
  Goldstones, and ghosts was derived for both boundaries in one `MSbar`
  `R_xi` prescription; hence `xi` cancellation and finite constants are
  untested.
- The 290 heavy scalar directions have a complete SM-side trace, but no
  proven allocation to PS running, the `M_I` threshold, and the `M_U`
  threshold. A mass-only cutoff can split a PS representation and need not
  define the intended renormalizable interval EFT.
- The noncommuting PS-side mass/generator problem requires the appropriate
  two-mass functional traces or a controlled expansion in the lower VEV
  relative to the upper scale. The formal `sigma=0` nonstationary masses
  remain representation checks, not threshold inputs.
- Per-boundary beta-jump and matching-scale derivative cancellation,
  hypercharge plus D-parity finite matching, and exact once-only state
  accounting cannot yet be checked. A whole-spectrum checksum is not a
  substitute for these boundary tests.

The next calculation must freeze a PS-interval EFT/power-counting
prescription and compute the *full* one-loop background-field two-point
functions with non-degenerate mass matrices, including vector, Goldstone,
ghost, and heavy/light mixing terms. Compare both boundaries in one scheme;
independently replay their `xi` independence, degenerate limits, beta
jumps, and matching-scale derivatives. Only then is a solve for
`M_I`, `M_U`, and `alpha_U` authorized. This outcome does not reject the
scalar benchmark or alter the earlier Babu--Khan BNV results.

## Reproduction

From the repository root:

```text
python calculations/canonical_so10_matrix_threshold/check_scalar_matrix_log.py
python calculations/canonical_so10_matrix_threshold/check_vector_matrix_log.py
python calculations/canonical_so10_matrix_threshold/check_noncommuting_mass_warning.py
```

The frozen action/point hashes are in [`RECORD.md`](RECORD.md). These tests
depend on the already-validated parent-action Hessian/point and the
preceding SM threshold ledger; they do not introduce Babu--Khan scalar
thresholds or physical GeV assignments.
