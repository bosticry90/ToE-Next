# Canonical direct physical-vacuum gauge matching

## Disposition

The one-loop kernel passes:

\[
\boxed{\texttt{DIRECT\_ONE\_LOOP\_KERNEL\_PASS}}
\]

The gauge-unification verdict is:

\[
\boxed{\texttt{DIRECT\_GAUGE\_MATCHING\_UNRESOLVED}}
\]

The frozen benchmark has no exact common one-loop solution for the three
measured gauge couplings. Its best perturbative one-loop fit has a maximum
inverse-coupling residual of \(1.060\). That is not yet a point-level
falsification because known gauge-only SM two-loop running shifts the
nonuniversal result by \(0.706\), while a separate next-threshold-order
diagnostic is \(0.245\). The admitted-order uncertainty and residual are
therefore comparable.

`BFB_UNRESOLVED` remains in force. No flavor, proton-decay, PS-resummation, or
replacement-benchmark calculation was begun.

## Frozen direct scheme and field disposition

The calculation uses one `MSbar` background-field Feynman gauge at the actual
positive-Higgs stationary vacuum. The low operator basis contains the three
GUT-normalized SM gauge kinetic terms. Light fields are common to the UV and
EFT hard subtraction and cancel there.

The heavy field ledger contains exactly once:

- 290 positive physical scalar real directions;
- 33 massive gauge vectors;
- one eaten Goldstone and one complex ghost pair for each massive vector.

The 38 excluded scalar zero directions are

\[
33\text{ gauge Goldstones}+1\text{ PQ mode}+4\text{ tuned-Higgs directions}.
\]

The tuned Higgs remains in the low theory. The PQ Goldstone and the unfitted
right-handed neutrinos are SM gauge singlets, so they contribute no one-loop
SM gauge-kinetic threshold. This statement gives them no broader
phenomenological authority.

## Direct vector derivation

The vector coefficient was rederived in this calculation rather than copied
from the earlier lower boundary. In background-field Feynman gauge, the
combined massive-vector, real-Goldstone, and complex-ghost heat-kernel
coefficient is

\[
a_2\big|_{F^2}=-\frac78-\frac{\epsilon}{12}.
\]

Relative to one real scalar, the logarithmic coefficient is \(-21\), and the
dimension-dependent pole leaves the finite/logarithmic ratio

\[
-\frac{2}{21}.
\]

Thus every massive-vector SM index block contributes in the frozen scheme

\[
\boxed{\lambda_i^V=T_i\left[1-21\ln\frac{M_V}{\mu}\right]}.
\]

This formula was applied to all 33 physical massive vectors using the exact
mass/index sets

\[
\begin{array}{c|c|c}
M_V^2/(g_{10}^2\omega^2)&\text{real vectors}&(T_1,T_2,T_3)\\ \hline
0.005&8&(14/5,0,1)\\
0.025&1&(0,0,0)\\
50/120&12&(5,3,2)\\
50.6/120&12&(1/5,3,2).
\end{array}
\]

The scalar contribution is the independently verified basis-invariant
physical matrix log. No PS interval beta coefficient or state assignment is
used.

## Exact beta-jump and scale checks

The parent `Spin(10)` coefficient follows independently from

\[
-\frac{11}{3}C_2(45)
+\frac23\,3T(16)
+\frac16T(54)
+\frac13\left[T(126)+T(10)\right],
\]

with

\[
C_2(45)=8,\qquad
T(16,54,126,10)=(2,12,35,1),
\]

giving

\[
b_{10}=-\frac{34}{3}.
\]

Starting from

\[
b_{\rm SM}=\left(\frac{41}{10},-\frac{19}{6},-7\right),
\]

the complete heavy-scalar jump is

\[
b_S=\left(\frac{377}{30},\frac{77}{6},\frac{79}{6}\right),
\]

and the vector jump is

\[
-\frac72(8,6,5).
\]

Channel by channel,

\[
b_{\rm SM}+b_S-\frac72T_V
=\left(-\frac{34}{3},-\frac{34}{3},-\frac{34}{3}\right).
\]

The threshold derivative obeys

\[
\frac{d\lambda_i}{d\ln\mu}
=-6b_{S,i}+21T_{V,i}
=6(b_{{\rm SM},i}-b_{10}),
\]

so

\[
\alpha_i^{-1}=\alpha_{10}^{-1}-\frac{\lambda_i}{12\pi}
\]

has exactly the required one-loop matching-scale derivative. The degenerate
limit, basis rotations, physical scalar trace, and vector index trace also
pass their independent replays.

## Measured-coupling solve

At \(\mu=\omega\), the three one-loop equations are

\[
\alpha_i^{-1}(M_Z)
=\frac{4\pi}{g_{10}^2}
-\frac{\lambda_i^S+\lambda_i^V(g_{10})}{12\pi}
+\frac{b_i^{\rm SM}}{2\pi}\ln\frac{\omega}{M_Z}.
\]

The frozen inputs are

\[
(\alpha_1^{-1},\alpha_2^{-1},\alpha_3^{-1})_{M_Z}
=(59.0100,29.5800,8.47458).
\]

There is no exact common solution. Matching pairs of channels separately
leaves the third-channel residuals

\[
2.506,\qquad -1.641,\qquad 4.749,
\]

respectively. Solving the two independent relative-coupling equations has a
unique formal point only at

\[
g_{10}\sim1.7\times10^{-36},qquad
\omega\sim10^{49}\ {\rm GeV},
\]

where the common normalization fails by \(O(10^{72})\). Thus there is no
hidden perturbative exact root.

The least-squares diagnostic point is

\[
g_{10}=0.52250,qquad
\omega=2.22\times10^{15}\ {\rm GeV},
\]

with residual vector

\[
\boxed{(0.366,-1.060,0.694)}
\]

and Euclidean norm \(1.319\). Because it is not a common solution, these
parameter values are not promoted to physical benchmark scales.

## Perturbative uncertainty

The route-selection loop-log diagnostics give

\[
\left(0.007157\right)^2=5.12\times10^{-5}
\]

for the raw squared loop-log factor and

\[
\left(0.09424\right)^2=8.88\times10^{-3}
\]

after the conservative total-index weighting. These show perturbative
feasibility but do not directly bound inverse-coupling residuals.

As a more physical comparator, standard gauge-only two-loop SM running to the
one-loop best-fit scale changes the three inverse couplings by

\[
(-0.222,-0.288,+0.417),
\]

whose nonuniversal spread is

\[
0.706.
\]

Refitting after that known correction gives

\[
g_{10}=0.52326,qquad
\omega=1.64\times10^{15}\ {\rm GeV},
\]

and residual

\[
(0.262,-0.749,0.487).
\]

This is a comparator, not a two-loop match. It omits two-loop Yukawa terms,
two-loop heavy-threshold matching, and scheme-consistent higher-order finite
terms. Scaling the one-loop nonuniversal threshold by the largest
index-weighted loop-log factor gives a separate next-order diagnostic

\[
0.245.
\]

The deliberately conservative linear combination

\[
0.706+0.245=0.951
\]

is comparable with the one-loop maximum residual \(1.060\). Therefore the
calculation cannot honestly distinguish a point-level failure from a shift
that could be material at the next admitted order.

## Authority and next state

Earned:

- a common-scheme direct one-loop scalar/vector matching kernel;
- complete one-loop state accounting;
- exact direct beta-jump and matching-scale cancellation;
- proof that the frozen inputs have no exact common one-loop solution;
- a quantified reason that this is not yet a robust failure.

Not earned:

- gauge unification or its exclusion;
- physical \(g_{10}\), \(\omega\), \(M_I\), or \(M_U\);
- a complete two-loop uncertainty;
- global BFB, flavor, neutrino, or proton-decay viability.

The exact PS route remains deferred rather than rejected. Benchmark
replacement remains closed during this gate.

## Reproduction

Run:

```powershell
python calculations/canonical_so10_direct_gauge_matching/derive_and_solve.py
```

The machine-readable output is `direct_matching.json`.
