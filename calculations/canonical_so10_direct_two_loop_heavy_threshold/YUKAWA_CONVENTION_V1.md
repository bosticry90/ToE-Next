# Canonical Yukawa convention v1 (symbolic threshold gate)

This file freezes the theory-level normalization needed to state the Yukawa
dependency of the two-loop direct gauge threshold.  It does **not** choose or
fit numerical flavor matrices.

Let the three left-handed matter multiplets be `psi_p` (`p=1,2,3`) in the
canonically normalized `16` of `Spin(10)`.  Let `C^10_A` and `C^126_I` be the
unique symmetric intertwiners in

```text
Sym^2(16) = 10 + 126,
```

where `A` and `I` label orthonormal scalar bases in the frozen kinetic metrics
of the complex `10_H` and self-dual `126_H`.  Fix their remaining overall
normalizations by the Hilbert--Schmidt isometries

```text
sum_(alpha,beta) conjugate(C^R_X[alpha,beta]) C^R_Y[alpha,beta] = delta_XY
```

for `R=10,126`.  The Yukawa Lagrangian is defined to be

```text
L_Y = -1/2 [
  (Y10)_pq C^10_A[alpha,beta] psi_p^alpha psi_q^beta phi_A
 + (Y126)_pq C^126_I[alpha,beta] psi_p^alpha psi_q^beta Sigma*_I
 ] + h.c.
```

Thus `Y10=Y10^T` and `Y126=Y126^T`.  This is compatible with the frozen PQ
charges: both Yukawa scalar insertions have charge `-2`.  A component gamma
matrix realization must reproduce these isometry conditions; it may not
silently rescale one Yukawa matrix relative to the other.

At two-loop order a gauge two-point diagram has two Yukawa vertices.  Before
putting Yukawa-generated fermion masses into propagators, the complete family
dependency is therefore the Hermitian positive-semidefinite Gram matrix

```text
K_rs = Tr(Y_r^dagger Y_s),       r,s in {10,126}.
```

Equivalently, it has four real coordinates:

```text
Tr(Y10^dagger Y10),
Tr(Y126^dagger Y126),
Re Tr(Y10^dagger Y126),
Im Tr(Y10^dagger Y126).
```

The off-diagonal coordinate can contribute only multiplied by a scalar kernel
that connects the `10` and `bar126` Yukawa channels.  Such mixing exists at the
physical benchmark, so it cannot be discarded by representation labels.

This four-coordinate statement is complete only for the vertex polynomial.
At the physical vacuum the right-handed-neutrino mass matrix is

```text
M_N = c_N sigma Y126,
```

where `c_N` is fixed by the normalized singlet component of the isometric
intertwiner.  Exact massive two-loop integrals consequently depend on spectral
matrix functions of `M_N^dagger M_N` and its projectors, not just on the four
numbers above.  No numerical `Y10`, `Y126`, `c_N`, right-handed-neutrino
spectrum, or flavor point is frozen in this calculation.  Hence the symbolic
operator normalization and quadratic invariant basis are earned, but the
physical Yukawa-dependent threshold is not numerically defined.
