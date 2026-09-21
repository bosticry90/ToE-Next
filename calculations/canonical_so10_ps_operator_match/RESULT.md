# Canonical `Spin(10) -> PS` tree-operator gate

## Disposition

\[
\boxed{\texttt{PS\_EFT\_ERROR\_UNRESOLVED}}
\]

The requested operator-level calculation earns an exact upper-vector
current--current operator and a once-only local gauge-slice disposition. It
does **not** close the preregistered `0.2027005` inverse-coupling error gate.
The first missing authority is the complete candidate-heavy-scalar source
functional, followed by its background-field one-loop insertions. More
importantly, the frozen split does not admit a controlled finite local inverse
expansion for all of the borderline retained modes, so those missing
coefficients cannot be replaced by a dimension-six or dimension-eight tail
estimate.

This result is neither `PS_EFT_ACCURATE_FOR_GAUGE_MATCHING` nor
`PS_EFT_INACCURATE_FOR_GAUGE_MATCHING`.

## Exact upper-vector elimination

Use the canonical convention

\[
\operatorname{Tr}_{10}(T_A T_B)=\delta_{AB},\qquad
\mathcal L\supset \frac12 A^A_\mu (M_V^2)_{AB}A^{B\mu}
   +g_{10}A^A_\mu J_A^\mu,
\]

with \(M_V^2=g_{10}^2K_V\). At the physical point, the 24 first-stage
vectors split into two twelve-dimensional eigenspaces with raw kinetic-orbit
Gram eigenvalues

\[
50,\qquad 50.6=\frac{253}{5},
\]

and

\[
K_V/\omega^2=\frac{\text{raw Gram}}{120}.
\]

Their algebraic equations of motion therefore give

\[
\Delta\mathcal L_V^{\rm tree}
=-\frac12J_A^\mu(K_V^{-1})_{AB}J^B_\mu.
\]

In a mass eigenbasis, the exact coefficients in units of \(\omega^{-2}\)
are

| multiplicity | raw Gram | coefficient multiplying \(J_A^2/\omega^2\) |
|---:|---:|---:|
| 12 | \(50\) | \(-6/5\) |
| 12 | \(253/5\) | \(-300/253\) |

The \(\sigma/\omega\to0\) limit correctly recombines all 24 coefficients to
\(-6/5\). The gauge coupling cancels between the two vertices and the inverse
vector mass, as it must at this tree order.

## Goldstone and candidate-scalar overlap

The exact generator-orbit calculation gives

\[
\operatorname{rank}\delta\Phi=24,
\qquad
\operatorname{rank}\delta\Sigma=12,
\qquad
\operatorname{rank}(\delta\Phi,\delta\Sigma)=24.
\]

All 24 upper generators have a nonzero \(126_H\) projection, but those
projections span 12 real directions, entirely inside the projected
\(126_H(15,2,2)\) sector. Thus a valid local unitary slice can set the 24
\(54_H(6,2,2)\) orbit coordinates to zero. The 24 vector Goldstones are then
removed once, and the corresponding 24 complex ghosts occur only in the loop
gauge-fixing determinant. This is a complete counting disposition, but it
also proves that removal of the vector orbit and elimination of the candidate
heavy scalar block are coupled coordinate operations; treating them as two
independent physical state sums would double count part of the same orbit.

## Candidate-heavy-scalar operator

For the frozen 132-real
\(126_H[(6,1,1)+(15,2,2)]\) block, exact tree elimination has the nonlocal
form

\[
\Delta\mathcal L_H
=-\frac12J_H[L]^T(M_{HH}^2-D^2)^{-1}J_H[L].
\]

Its leading local term would be

\[
-\frac12J_H[L]^T(M_{HH}^2)^{-1}J_H[L],
\]

but the complete cubic source tensors \(J_H[L]\) were not compiled into a
closed PS operator basis in this calculation. Consequently no claim is made
for their one-loop gauge-kinetic insertions.

This is not merely a missing-software issue. For the frozen split the
retained-to-heavy mass-squared ratio is

\[
r=0.7039927683.
\]

The norm diagnostics for the inverse series are therefore

\[
\frac{r}{1-r}=2.37830
\]

after retaining only the leading local inverse, and

\[
\frac{r^2}{1-r}=1.67430
\]

after also retaining the next derivative term. These are not small
remainders. The earlier matrix-log bound also remains open through the
smallest positive scalar gap.

For the upper vectors, the coarse-coupling diagnostic gives

\[
\frac{m^2_{\rm retained,max}}{M^2_{V,\rm upper,min}}
=1.45572>1.
\]

It is not a physical matched value because \(g_U\) has not been solved, but
it is sufficient to reject using a convergent local current--current
derivative series as the present error certificate.

## Preregistered error-gate rerun

| Required item | Status |
|---|---|
| target in inverse-coupling differences | `0.20270050124930578` frozen |
| upper-vector tree coefficient | exact |
| once-only vector/Goldstone/ghost disposition | exact at tree/counting level |
| 132-real heavy-scalar cubic source basis | not complete |
| induced scalar-operator one-loop \(F^2\) insertions | not computed |
| upper-vector-operator one-loop \(F^2\) insertions | not computed |
| uniformly controlled finite local remainder | fails current norm diagnostics |
| closed sum/bound comparable with target | unavailable |

The numerical gate therefore cannot be rerun as a closed error sum. Calling
the EFT accurate would omit required terms. Calling it inaccurate would
mistake failure of this finite local truncation for a demonstrated excessive
physical correction; an exact nonlocal treatment or a revised field
allocation could still close the observable.

## Authority and downstream state

Earned here:

- the exact tree upper-vector current--current coefficients;
- exact upper Goldstone overlap ranks and a once-only local gauge slice;
- a demonstrated nonclosure of dimension-six/dimension-eight inverse-series
  error estimates for the frozen split.

Not earned:

- a complete local renormalizable PS EFT plus controlled higher operators;
- either boundary's complete one-loop matching;
- the gauge-scale solution;
- admission of direct broken-phase matching;
- flavor, baryon-number violation, or a replacement benchmark search.

`BFB_UNRESOLVED`, `PS_INTERVAL_EFT_BLOCKED`,
`LOWER_BOUNDARY_MATCHING_BLOCKED`, `PS_THRESHOLD_KERNEL_BLOCKED`, and
`GAUGE_MATCHING_BLOCKED` remain in force.

## Reproduction

Run:

```powershell
python calculations/canonical_so10_ps_operator_match/derive_tree_gate.py
```

The machine-readable output is `tree_operator_gate.json`.
