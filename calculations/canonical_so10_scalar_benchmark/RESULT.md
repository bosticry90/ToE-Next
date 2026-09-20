# Canonical scalar benchmark: bounded result

**Outcome:** `CANONICAL_SCALAR_BENCHMARK_FOUND` for the explicitly new,
source-derived `Spin(10) x U(1)_PQ` parent action, at the **local scalar
quadratic** authority ceiling. This is not a corrected numerical Babu--Khan
point and does not establish a viable fermion fit, proton-decay rate, global
minimum, bounded-from-below potential, or loop-level perturbativity.

The frozen Stage 1 point is [STAGE1_POINT.json](STAGE1_POINT.json). It has
`omega=sqrt(60)`, `sigma/omega=v/omega=0.1`; all 31 free dimensionless
inputs are exact decimal rationals inside the preregistered coefficient
bounds. The remaining three quadratic masses are eliminated by the
action-derived tadpoles. Direct exact-parent replay of all 35 SM-irrep
Hessian blocks gives real rank `294`, nullity `34` (33 gauge plus one PQ),
and strictly positive remaining eigenvalues in the canonical kinetic
metric. The smallest physical mass squared is
`0.08656155779937560698` in the chosen normalization (neutral sector);
the lightest colored mass squared is `1.51771323908775886088`, or
`0.02529522065146265 omega^2`, above the preregistered
`10^-4 omega^2` colored floor; its mass is about `1.59 sigma` for this
point. The 54/126 gauge-orbit kinetic Gram has
12 zero, 9 intermediate, and 24 first-stage gauge directions; the ratio
of lightest first-stage to heaviest intermediate gauge mass is `4.08248`
for a common gauge coupling. The exact vacuum tadpoles vanish.
Both pure-`10_H` quartic coefficients are set to `0.1` in the frozen point.
They vanish through quadratic order at `<10_H>=0`, so they do not alter
the tadpoles or any Hessian block; they remove the immediate pure-`10_H`
runaway that zero quartics would create after Stage 2 tuning. This is not
a global boundedness proof. The Stage 1 point SHA-256 is
`3a1054be3962db4b9055f6c7dbb7a2829f2332ef07dab5997fee693592de5b14`.

Separately, [STAGE2_POINT.json](STAGE2_POINT.json) defines a tuned point
at the same VEVs. It inherits Stage 1 except `z6:re=zK:re=zEta:re=0.3`
and replaces `mphi2/omega^2` by the unique exact root in `(-0.14,-0.13)`
of the frozen quadratic doublet-determinant polynomial. The root is
approximately `-0.1337864654296790720`. Both conjugate Higgs blocks have
exactly one algebraic zero, and the other three eigenvalues are strictly
positive; the next mass squared is `7.04382550799932471`. The light
eigenvector has a nonzero `126_H` fraction `0.00183849641516` in the
canonical kinetic norm. Direct-parent replay of all **four** affected
irrep blocks verifies the colored sectors remain positive (their minimum
is `1.54582347066555928`). The 31 unaffected blocks inherit the exact
Stage 1 certificate because every changed interaction contains `10_H`,
whose VEV is zero. Thus the tuned real Hessian has rank `290`, nullity
`38 = 33 gauge + 1 PQ + 4 light-doublet` with no other zero modes.
The tuned point is marginal in those Higgs directions; stability of its
effective light-Higgs quartic after heavy-field relaxation has not been
established.
The Stage 2 point SHA-256 is
`26bd69eb2f1341bca3576b72da666b0ca4d71a38a3e1c39f362908704dc16b6b`.

The numerical search used affine coefficient matrices compiled from the
frozen parent bilinear, and a fixed-ratio semidefinite feasibility solve;
its solver status was **not** the evidence. The exact witness regression,
rounded-rational point, exact action-tadpole replay, direct parent-action
block recomputation, 60--70-digit generalized eigenvalues, colored floor,
and exact quadratic determinant root provide the reported authority.
Several allowed coefficients are zero at these points, and the tuned Higgs
mixing fraction is small; neither is promoted into a flavor claim. This
is a local high-scale scalar existence result, not proof of global
stability or a phenomenologically complete GUT. The numerical compiler and
direct exact replay share the frozen invariant implementation; they are
independent evaluation paths for coefficient ordering, scaling, and
precision, not wholly separate tensor implementations of every colored
contraction. The prior exact rank/Goldstone and independent doublet checks
remain additional controls.

## Reproduction

From the repository root, with Python, SymPy, NumPy, SciPy, mpmath, and
CVXPY/Clarabel available (used here: SymPy 1.14.0, NumPy 2.2.6,
SciPy 1.15.3, mpmath 1.3.0, CVXPY 1.7.5, Clarabel 0.11.1):

```text
python calculations/canonical_so10_scalar_benchmark/compile_numeric_blocks.py
python calculations/canonical_so10_scalar_benchmark/verify_compiled_blocks.py
python calculations/canonical_so10_scalar_benchmark/search.py
python calculations/canonical_so10_scalar_benchmark/validate_candidate.py
python calculations/canonical_so10_scalar_benchmark/check_gauge_hierarchy.py
python calculations/canonical_so10_scalar_benchmark/replay_candidate_exact.py
python calculations/canonical_so10_scalar_benchmark/stage2_tune.py
python calculations/canonical_so10_scalar_benchmark/derive_stage2_tuning.py
python calculations/canonical_so10_scalar_benchmark/replay_stage2_exact.py
```

`generated_*.npz` files are disposable local caches, not scientific
authority. The frozen action hash is in [RECORD.md](RECORD.md). The exact
Stage 1 and Stage 2 points are the two small JSON files above.
