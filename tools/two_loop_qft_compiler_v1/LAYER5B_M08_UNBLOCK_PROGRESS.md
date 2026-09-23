# Layer-5B M08 unblock progress

## Authority boundary

This checkpoint is implementation preflight only.  It does not retry or
promote `UVP_M08`.  The authoritative state remains:

```text
34/39 = 33 PASS, 1 BLOCKED, 0 FAIL
UVP_M08 = BLOCKED (attempt 1)
ONE_LOOP_COUNTERTERM_COMPILER = BLOCKED
Layer 6 authorized = false
```

## Newly completed implementation

The frozen partial-BFM action has now been contracted into the group kernels
needed by the ghost and quantum-vector pole calculations.  The full adjoint
contraction independently returns `C_A(Spin(10)) = 8` in all 45 directions.

The partial fixing resolves the ghost sectors into non-universal blocks:

- heavy-ghost `K_HHH` spectrum:
  `3 (x12), 19/5 (x12), 24/5 (x6), 34/5 (x2), 8 (x1)`;
- light-ghost `K_LLL` spectrum:
  `0 (x1), 2 (x3), 3 (x8)`.

The ordered mixed contractions satisfy the completeness identities

```text
K_HHH + 2 K_HHL = 8 I_33
K_LLL + K_LHH   = 8 I_12
```

to the certified floating-point authority of the immutable physical gauge
basis.  Both heavy kernels commute with the frozen heavy-vector mass matrix.

The local ghost two-point UV projector has also been implemented.  Its direct
large-loop-momentum derivation and an independent Feynman-parameter/Gaussian
replay agree exactly on the kinematic coefficient

```text
(3 - gauge_parameter)/4.
```

Here `d_mu` in the frozen partial gauge-fixing action is the unbroken-group
covariant derivative.  Expanding it includes the heavy-ghost/light-quantum-
vector bubble as required by the source partial-BFM construction (Eqs. 3.31
and 3.36 of [Thomsen, arXiv:2404.11640](https://arxiv.org/abs/2404.11640)).
Consequently the derived kinetic-pole operators are

```text
delta Z_uH = (3-xi)/4 K_HHH + (3-eta_H)/4 K_HHL
delta Z_cL = (3-eta_H)/4 K_LLL
```

in units of `g10^2/(16*pi^2*epsilon_bar)`.  These are block-valued operators,
not single universal numbers.  Mass, scalar, Goldstone, and equivariant
quartic-ghost insertions were audited as carrying no external-momentum-squared
pole in these two-point functions.

The quantum-vector Lorentz pole has now also been derived directly from two
three-Yang--Mills vertices and general-gauge propagators.  A second
implementation based on an auxiliary-mass large-momentum Taylor expansion
agrees exactly with the primary Feynman-parameter calculation:

```text
vector bubble: A = (rho+sigma)/4 - 25/12
               B = -(rho+sigma)/4 + 7/3
ghost bubble:  A = -1/12
               B = -1/6
```

For an ordinary unsplit ghost sector this independently reconstructs
`delta Z_Q = 13/6-xi/2` and a zero transverse residual before any canonical
group factor is applied.

Combining these Lorentz kernels with independently regenerated SO(10) group
contractions and the parent matter index ledger produces a complete canonical
two-point candidate.  A separate raw-Kronecker group construction plus the
auxiliary-mass Lorentz replay reproduces every heavy and light block with zero
symbolic residual.

The two-point result is not compatible with treating all broken directions as
one undifferentiated counterterm block: it resolves five heavy irreducible
blocks.  The three light blocks coalesce to the ordinary parent value when
`eta_H=xi`; the heavy gauge-fixing candidates do not.  This is a pre-BRST
diagnostic, not yet a promoted failure: the frozen M08 criterion also requires
the associated ghost-vector three-point pole action and its aggregate BRST
adjudication.

## Remaining M08 blocker

The completed and independently replayed two-point kernels do not satisfy the
full frozen M08 gate.
The following still require direct primary calculations and a complete
inventory-independent replay:

1. the heavy/light ghost-vector BRST three-point pole operators;
2. the aggregate BRST/background-Ward adjudication of the block-valued
   two-point candidates;
3. a decision, based on that complete calculation, whether the single frozen
   `xi` ansatz closes or requires separately invariant coset gauge parameters.

The pure-Yang--Mills control values cannot be promoted into these missing
canonical objects because the partial fixing resolves distinct heavy and
light group kernels.  No BRST vertex residue has been inferred from a
Slavnov--Taylor identity or a later gate.

M09--M13 therefore remain locked by the existing serial fail-fast rule.
