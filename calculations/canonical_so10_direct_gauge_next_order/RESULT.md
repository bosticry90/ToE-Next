# Canonical direct gauge matching at the next running order

## Disposition

The coupled Standard Model running gate passes:

\[
\boxed{\texttt{DIRECT\_SM\_TWO\_LOOP\_RUNNING\_PASS}}
\]

The benchmark-level gauge verdict remains:

\[
\boxed{\texttt{DIRECT\_GAUGE\_MATCHING\_UNRESOLVED}}.
\]

The passed `DIRECT_ONE_LOOP_KERNEL` is preserved. Complete two-loop SM gauge
running reduces the best-fit maximum inverse-coupling residual from `1.060` to
`0.745`, but does not produce a common solution. The result cannot be promoted
to `FAIL` because the model-dependent two-loop heavy decoupling constants are
neither calculated nor rigorously bounded. Their Yukawa-dependent part is not
even numerically defined before the canonical Yukawa matrices are frozen.

`BFB_UNRESOLVED` remains explicit. No flavor fit, proton-decay calculation, PS
resummation, or replacement-benchmark search was started.

## Coupled running

The calculation uses GUT-normalized `g1` and

\[
\frac{d g_i}{d\ln\mu}=
\frac{b_i g_i^3}{16\pi^2}
+\frac{g_i^3}{(16\pi^2)^2}
\left(\sum_jB_{ij}g_j^2-c_i^t y_t^2-c_i^b y_b^2-c_i^\tau y_\tau^2\right),
\]

with

\[
b=\left(\frac{41}{10},-\frac{19}{6},-7\right),
\]

\[
B=\begin{pmatrix}
199/50&27/10&44/5\\
9/10&35/6&12\\
11/10&9/2&-26
\end{pmatrix}.
\]

The top, bottom, tau, and Higgs quartic are evolved at one loop. That is the
order needed for their insertion in the two-loop gauge beta function. The
quartic is included as a coupled monitor but does not enter the gauge beta
function at two loops.

The frozen reference boundary is

\[
\mu=m_t=173.34\ {\rm GeV},\qquad
(y_t,y_b,y_\tau,\lambda)=(0.93714,0.0164,0.0102,0.12604).
\]

At the central diagnostic matching scale the flow gives

\[
(g_1,g_2,g_3)=(0.56839,0.53025,0.54112),
\]

\[
(y_t,y_b,y_\tau,\lambda)=(0.46190,0.006613,0.009936,-0.03459).
\]

The last number is only an SM-running monitor. It is not matched here to the
canonical light-Higgs quartic and therefore carries no scalar-benchmark
verdict.

The Yukawa terms shift the three high-scale inverse gauge couplings, relative
to gauge-only two-loop running, by

\[
(0.02190,0.01937,0.02541).
\]

Their nonuniversal effect is consequently small but has now been included
rather than estimated.

## Known next-order direct match

At `mu=omega`, the joint refit gives

\[
g_{10}=0.523126,\qquad
\omega=1.6374\times10^{15}\ {\rm GeV},
\]

with residual

\[
\boxed{(0.260915,-0.745476,0.484795)}
\]

and Euclidean norm `0.926735`. These fitted values remain diagnostics, not
physical benchmark parameters, because the three channels do not meet.

Matching pairs of channels exactly leaves the third off by

\[
1.772,\qquad -1.152,\qquad 3.293,
\]

respectively. Thus the known two-loop-running plus one-loop-threshold system
has no common perturbative root.

## Scale and weak-boundary tests

Refitting at

\[
\mu/\omega=(0.5,0.75,1,1.5,2)
\]

gives maximum residuals between

\[
\boxed{0.74172\ \text{and}\ 0.74931}.
\]

The envelope is only `0.00759`. This is evidence that the known logarithmic
terms are stable; it is not a rigorous bound on unknown finite two-loop heavy
thresholds.

Varying `yt(mt)` by `+-0.006`, `yb` and `ytau` by `+-20%`, and the quartic by
`+-0.002` changes the optimized maximum residual by at most

\[
5.8\times10^{-5}.
\]

The remaining ambiguity is therefore not coming from these weak-boundary
nuisance choices.

## Independent replay

The primary program evolves `g_i`. A separate implementation evolves

\[
A_i=\alpha_i^{-1}
\]

directly with a different adaptive integrator. It reproduces

\[
g_{10}=0.5231256382,
\qquad
\omega=1.6373732\times10^{15}\ {\rm GeV},
\]

and the residual vector to better than `2e-8`. The change from the previous
gauge-only comparator is therefore physical within the frozen equations, not
an integration-coordinate artifact.

## Why the verdict is still unresolved

Two-loop SM running plus the passed one-loop threshold is a legitimate
RG-improved next step, but it is not a closed benchmark-level uncertainty
budget. A full fixed-order boundary at the next threshold order contains
model-dependent two-loop massive diagrams involving:

- heavy vectors, Goldstones, ghosts, and physical scalars;
- scalar self-interactions fixed by `PARENT_ACTION_V1`;
- heavy-light gauge interactions;
- Yukawa-dependent diagrams whose two canonical Yukawa matrices and phases
  have not been frozen.

The small matching-scale envelope constrains omitted logarithmic dependence,
not arbitrary finite matching constants. The earlier `0.245` estimate is
therefore retired as authority and retained only as historical diagnostics;
it has not been converted into a rigorous bound.

The known residual is now localized sharply:

\[
\|r\|_\infty=0.7455,
\]

while weak-input and matching-scale effects inside the completed running are
far smaller. But without the two-loop heavy boundary, the preregistered rule
does not permit either `PASS` or `FAIL`.

## Authority

Earned:

- complete two-loop SM gauge evolution with the required third-family Yukawa
  insertions;
- coupled one-loop top/bottom/tau/Higgs evolution;
- a numerically stable next-order refit and pairwise no-root check;
- matching-scale and weak-boundary sensitivity envelopes;
- independent inverse-coupling replay.

Not earned:

- a complete two-loop direct `Spin(10) -> SM` threshold;
- a rigorous total higher-order uncertainty smaller than the residual;
- gauge-unification success or exclusion;
- physical `g10` or `omega`;
- Higgs-quartic matching, flavor, proton decay, or global BFB.

## Reproduction

Run:

```powershell
python calculations/canonical_so10_direct_gauge_next_order/run_next_order.py
python calculations/canonical_so10_direct_gauge_next_order/independent_replay.py
```

The machine-readable output is `next_order.json`.
