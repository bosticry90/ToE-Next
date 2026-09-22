# TWO_LOOP_QFT_COMPILER_V1: promotion layer 5

## Disposition

Layer 5 is blocked:

\[
\boxed{\texttt{ONE\_LOOP\_COUNTERTERM\_COMPILER\_BLOCKED}}.
\]

This is an implementation block, not a physics failure.  The passed layer-4
diagram inventory remains `TWO_LOOP_DIAGRAM_GENERATOR_PASS`.  No tensor/IBP
reduction, master-integral work, two-loop amplitude assembly, or finite
`C1_GS` extraction began.

## Earned counterterm structure

[`layer5_counterterm_contract.py`](layer5_counterterm_contract.py) expands the
unshifted bare parent action in the same dimensional-regularization,
`MSbar`, partial-BFM convention.  It records all 29 parent coefficient
families (24 real plus five complex) and their exact field-renormalization
multiplicities.  These are the 34 real Hermitian coupling directions of
`PARENT_ACTION_V1`.

For a degree-`n` parent monomial with coefficient `c_n`, the frozen bare
definition is

\[
c_{n,0}=\mu^{(n-2)\epsilon}(c_n+\delta c_n),
\]

and the first-order operator coefficient is

\[
\delta c_n+
c_n\sum_r\frac{N_r}{2}\delta Z_r.
\]

The bare expansion closes on the same 29 monomial families.  This is
algebraic closure of the counterterm *ansatz*; it is not yet proof that the
calculated one-loop poles close on that basis.

All 21 preregistered layer-4 insertion slots now have non-null structural
dispatch expressions for field, mass, gauge-parameter, gauge-coupling, VEV,
tadpole, and generic vertex insertions.  Their one-loop pole residues are not
invented.  The counterterm-contract SHA-256 is

```text
87cf0b4966451c62168552284cb1c709c5e3247d8e1b8241e34d4b78116c48f1
```

## Gauge counterterm subpass

The already-earned parent coefficient

\[
b_{10}=-\frac{34}{3}
\]

fixes, with
`P10=g10^2/(16*pi^2*epsilon_bar)`,

\[
\delta Z_{g_{10}}=-\frac{17}{3}P_{10},\qquad
\delta Z_{\bar A}=\frac{34}{3}P_{10}.
\]

The background-field Ward identity therefore closes exactly:

\[
\delta Z_{g_{10}}+\frac12\delta Z_{\bar A}=0.
\]

This is the standard background-field relation
`Z_g sqrt(Z_background)=1`; the convention was checked against
[Abbott's background-field formulation](https://cds.cern.ch/record/134260/files/198012137.pdf).

This fixes the parent gauge/background-field residue only.  It does not fix
the quantum-vector, gauge-parameter, ghost, scalar, VEV, or tadpole residues.

## Tadpole and VEV convention

The contract freezes one FJ-like explicit-tadpole-shift prescription.  Parent
parameters remain `MSbar`; the same background-field/VEV shift and one-point
conditions must be used in the scalar, Goldstone, ghost, and vector sectors.
Mixing tadpole prescriptions between those sectors is forbidden.  The
Goldstone insertion identity is recorded as

\[
\delta(\xi M_V^2)=M_V^2\delta\xi+\xi\,\delta M_V^2.
\]

The numerical/symbolic residues of the VEV and tadpole shifts remain part of
the block.

## Independent round trip

[`independent_counterterm_roundtrip.py`](independent_counterterm_roundtrip.py)
imports neither the primary compiler nor its monomial table.  A separately
entered field-multiplicity ledger reconstructs all 29 bare-action
coefficients, all 21 slot dispatch classes, and the background Ward identity.
It agrees exactly:

```text
LAYER5_BARE_ACTION_ROUNDTRIP_PASS
PARENT_MONOMIAL_FAMILIES_REPLAYED 29
COUNTERTERM_SLOTS_REPLAYED 21
BACKGROUND_WARD_IDENTITY_RESIDUAL 0
```

## Exact blocker

At the original structural Layer-5 gate, the frozen artifacts did not contain
the one-loop 1PI UV poles needed to determine:

- the quantum-Spin(10), scalar, heavy/light ghost, and gauge-parameter field
  residues;
- the four quadratic, four real cubic, and 26 real quartic parent-potential
  residues;
- the three VEV and three tadpole residues; or
- the required scalar two- and three-point pole-cancellation controls.

Those quantities cannot be obtained from the two-loop graph count or fitted
from cancellation of future subdivergences.  They require a genuine one-loop
UV-pole evaluator for parent scalar one- through four-point functions and the
partial-BFM quantum-vector/ghost system. The later Layer-5A execution has now
validated that evaluator through the 27/27 engine gate and derived the M02
field residues, but it has not supplied the M03 quadratic residues or any
complete slot coefficient. Thus zero of the 21 slots has a *complete* derived
pole coefficient even though all 21 structural expressions are populated.

The next admissible compiler task is therefore the M03 exhaustive parent
scalar two-point contraction/projector kernel. Layer 6 remains unauthorized.

## Layer-5A execution update

The frozen Layer-5A contract has now executed through the first canonical
blocker. All 27 engine tests pass, earning
`ONE_LOOP_UV_POLE_EVALUATOR_PASS`; `UVP_M02` also passes and derives the four
parent scalar wave-function residues. The serial run then stops correctly at
`UVP_M03`, because the exhaustive parent-scalar one-loop two-point inventory,
the summed `V3*V3`/`M2*V4` contraction backend, and the completed quadratic
pole projector are not implemented.

The authoritative state is therefore `29/39` (28 pass, one blocked, zero
fail). This is an implementation block, not a physics failure. The
counterterm compiler remains blocked, Layer 6 remains unauthorized, and all
downstream physics dispositions remain unchanged. See
[`LAYER5A_EXECUTION_RESULT.md`](LAYER5A_EXECUTION_RESULT.md).

## Preserved physics boundary

The following remain unchanged:

- `DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED`;
- `DIRECT_GAUGE_MATCHING_UNRESOLVED`;
- `BFB_UNRESOLVED`;
- `finite_C1_GS = null`.

## Reproduction

```powershell
python tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.py
python tools/two_loop_qft_compiler_v1/independent_counterterm_roundtrip.py
python tools/two_loop_qft_compiler_v1/audit_layer5_gate.py
```
