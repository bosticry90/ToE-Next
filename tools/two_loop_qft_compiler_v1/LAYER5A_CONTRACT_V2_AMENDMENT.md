# Layer-5A contract v2 amendment

This amendment was made before evaluator execution.  It supersedes contract
v1 hash
`f4cf741afed95657b8c8c80ff178147189f35c7db42a8fdcea95e8ed3ae3f588`
with contract v2 hash
`6e256b9f8b2ed0e7243acc96d96daa854410673f59334b126446666d488ffe92`.
No scientific result, residue, or downstream disposition changes.

## Amendment 1: explicit rank-eight primitive

The declared maximum tensor rank remains eight, and the primitive suite now
tests that rank directly as `UVP_P13`.  For a rotationally invariant scalar
integrand `f(k^2)`, the evaluator must reproduce

```text
Integral[k_mu1 ... k_mu8 f(k^2)]
  = Sym_105[g_mu1mu2 g_mu3mu4 g_mu5mu6 g_mu7mu8]
    / (d (d+2) (d+4) (d+6))
    * Integral[(k^2)^4 f(k^2)].
```

`Sym_105` is the sum over all 105 perfect pairings of eight indices.  Passing
requires:

- exactly 105 unique pairings with equal coefficient;
- correct contraction back to the scalar integral;
- retention of `d=4-2 epsilon` through tensor reduction and Laurent
  expansion;
- consistency with the frozen routing and one-loop IBP controls;
- explicit UV/IR labels whenever the selected scalar integral is scaleless or
  infrared rearranged.

Prematurely setting `d=4`, omitting a pairing, using an incorrect denominator,
or validating only ranks two through six fails `UVP_P13`.  Removing the test
would require a new versioned contract and a formal proof that rank eight is
unreachable; v2 does not make that reduction.

## Amendment 2: inventory-independent replay

`UVP_M13` now tests graph completeness as well as UV algebra.  The replay may
not import the primary diagram inventory.  It must use either the independent
diagrammatic route or the inventory-independent functional route frozen in
[`INDEPENDENT_UV_REPLAY_DESIGN.md`](INDEPENDENT_UV_REPLAY_DESIGN.md).

The replay must expose enough artifacts to distinguish:

- a missing or duplicated graph;
- an incorrect field assignment;
- a wrong automorphism/symmetry factor;
- a Grassmann-loop or ordered-ghost sign error;
- a tensor-reduction/UV-extraction error.

Two evaluators applied to the same imported graph list do not satisfy the
amended independence requirement.

## Count and promotion change

The frozen matrix is now

```text
13 primitive + 13 control + 13 canonical = 39 tests.
```

The fail-fast partition is:

- 27 tests (`P01--P13`, `C01--C13`, `M01`) for
  `ONE_LOOP_UV_POLE_EVALUATOR_PASS`;
- 12 tests (`M02--M13`) for possible
  `ONE_LOOP_COUNTERTERM_COMPILER_PASS`.

At preregistration, zero of 39 tests have executed.  Layer 6 remains locked.
