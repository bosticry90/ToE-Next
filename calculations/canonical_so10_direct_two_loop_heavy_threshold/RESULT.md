# Direct two-loop heavy threshold: bounded execution result

## Disposition

The prior results remain valid:

\[
\boxed{\texttt{DIRECT\_ONE\_LOOP\_KERNEL\_PASS}},\qquad
\boxed{\texttt{DIRECT\_SM\_TWO\_LOOP\_RUNNING\_PASS}}.
\]

The newly requested boundary does **not** pass:

\[
\boxed{\texttt{DIRECT\_TWO\_LOOP\_HEAVY\_THRESHOLD\_BLOCKED}}.
\]

Therefore the benchmark verdict remains

\[
\boxed{\texttt{DIRECT\_GAUGE\_MATCHING\_UNRESOLVED}}.
\]

`BFB_UNRESOLVED` is carried unchanged.  No flavor fit, proton-decay
calculation, PS resummation, or replacement-benchmark search was started.

## Part A: what is fixed exactly

For Weyl fermions and real scalars, the frozen field content gives

\[
S_2(F)=6,\qquad \sum_F C_2(F)T(F)=\frac{135}{4},
\]

\[
S_2(S)=84,\qquad \sum_S C_2(S)T(S)=1004.
\]

The exact parent coefficients, including gauge interactions of all matter but
excluding Yukawa vertices at two loops, are

\[
\boxed{b_{10}=-\frac{34}{3}},\qquad
\boxed{B_{10}^{\text{Yukawa-independent}}=\frac{10405}{6}}.
\]

The first number independently replays the passed one-loop kernel.  At the
diagnostic `g10=0.523126`, the absolute ratio of the parent two-loop
gauge/scalar term to the one-loop term is `0.265`.  This is not a breakdown
proof, but it is too large to replace by the earlier heuristic `0.245`
inverse-coupling uncertainty.

At a common coupling, the three SM two-loop gauge row sums are

\[
\left(\frac{387}{25},\frac{281}{15},-\frac{102}{5}\right).
\]

Consequently the Yukawa-independent two-loop beta discontinuities are

\[
\Delta B_i=\left(-\frac{257803}{150},
                  -\frac{51463}{30},
                  -\frac{52637}{30}\right).
\]

Together with

\[
\Delta b_i=\left(\frac{463}{30},\frac{49}{6},\frac{13}{3}\right),
\]

these fix the complete two-loop matching-scale logarithms.  In the notation
of the primary two-loop GUT matching calculation,

\[
\zeta_i=1+\frac{\alpha}{\pi}
\left[\frac{\Delta b_i}{2}L-C_{0i}\right]
+\left(\frac{\alpha}{\pi}\right)^2
\left[\frac{\Delta b_i^2}{4}L^2
+\left(\frac{\Delta B_i}{8}-C_{0i}\Delta b_i\right)L
+C_{1i}\right].
\]

The calculation-local script materializes all exact coefficients and the
known one-loop `C0_i` values at `mu=omega`.  It therefore advances the
matching-scale check from a numerical envelope to an exact RG template.
It does not determine the finite constants `C1_i`.

## Why the finite gauge/scalar threshold was not imported

The available primary two-loop GUT calculation explicitly assumes one
GUT-scale VEV, no scalar trilinear, no heavy fermions, common masses for the
heavy vectors and most other scalars, and at most three SM irreps in the
GUT-breaking Higgs.  The canonical benchmark instead has three nonzero VEVs,
dimensionful cubic scalar interactions, four split vector mass/index sets,
and 290 mixed nondegenerate heavy scalar directions.  The source also reports
thousands of two-loop diagrams and requires one-loop gauge-parameter, mass,
field, and tadpole counterterms.

Accordingly, applying that finite formula here would not evaluate
`PARENT_ACTION_V1`; it would replace it by a different restricted theory.
Only its general background-field definition and RG logarithmic identity are
used.  A genuine Part A result requires a new model-specific two-loop
hard-region compiler.  Gauge-parameter cancellation and the finite
degenerate-mass limits cannot be claimed before those diagrams exist.

## Numerical burden carried by the missing constant

The known residual is

\[
r=(0.260915,-0.745476,0.484795).
\]

Thus the minimum channelwise inverse-coupling correction needed to cancel it
is `-r`.  Expressed as a centered `C1`-equivalent coefficient with natural
conversion `alpha_U/pi^2`, it is approximately

\[
(118.21,-337.89,219.68),
\]

up to a common component absorbed into the unified coupling.  This is a
normalization diagnostic, not a plausibility bound.  It shows precisely why
matching-scale stability cannot adjudicate the benchmark: the missing
information is a finite nonuniversal two-loop vector.

## Part B: symbolic Yukawa structure frozen

The canonical Yukawa operator convention is now fixed in
[`YUKAWA_CONVENTION_V1.md`](YUKAWA_CONVENTION_V1.md).  With isometrically
normalized symmetric `Spin(10)` intertwiners,

\[
\mathcal L_Y=-\frac12\left[
Y_{10}\,(16_F16_F)_{10}\,10_H
+Y_{126}\,(16_F16_F)_{126}\,\overline{126}_H
\right]+\text{h.c.},
\]

where both three-by-three family matrices are complex symmetric.  At two
loops the vertex-polynomial family dependence is exactly the Hermitian Gram
matrix

\[
K_{rs}=\operatorname{Tr}(Y_r^\dagger Y_s),
\qquad r,s\in\{10,126\}.
\]

Its four real coordinates are

\[
\operatorname{Tr}Y_{10}^\dagger Y_{10},\quad
\operatorname{Tr}Y_{126}^\dagger Y_{126},\quad
\Re\operatorname{Tr}Y_{10}^\dagger Y_{126},\quad
\Im\operatorname{Tr}Y_{10}^\dagger Y_{126}.
\]

The cross term must be retained because the physical scalar mass operator
mixes the two Yukawa channels.

This does not make the physical Yukawa threshold numerical.  The singlet VEV
generates `M_N=c_N sigma Y126`; exact massive integrals depend on its singular
values and mixing projectors.  Those are absent until a canonical flavor
point exists.  No flavor fit was started in this gate.

## Consequence for the requested refit

There is no derived finite two-loop heavy correction to insert.  Reusing the
old fit, setting `C1=0`, or scanning arbitrary `C1_i` would not be a model
prediction.  The refit is therefore **not authorized** and the previous
diagnostic values of `g10` and `omega` remain unphysical.

The first unearned object is now exact and narrow: a benchmark-specific
two-loop hard-region calculation with the full cubic/quartic scalar tensors,
split vector sector, one-loop counterterms, tadpoles, and (for the complete
answer) numerical Yukawa/right-handed-neutrino data.

## Reproduction

```powershell
python calculations/canonical_so10_direct_two_loop_heavy_threshold/analyze_boundary.py
python calculations/canonical_so10_direct_two_loop_heavy_threshold/independent_replay.py
```

Machine-readable output is in [`two_loop_boundary.json`](two_loop_boundary.json).
