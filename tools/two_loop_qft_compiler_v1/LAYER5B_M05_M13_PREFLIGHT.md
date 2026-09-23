# Layer-5B M05--M13 implementation preflight

## Authority boundary

This is a non-authoritative implementation inventory.  It does not execute,
retry, or promote any canonical test.  The authoritative ledger remains

```text
31/39 = 30 PASS, 1 BLOCKED, 0 FAIL
UVP_M05 = BLOCKED (attempt 1)
ONE_LOOP_COUNTERTERM_COMPILER = BLOCKED
Layer 6 authorized = false
```

The preflight exists only to distinguish implementation that is ready from
scientific tests that remain locked behind the serial M05 gate.

## Capability inventory

| Gate | Implementation state | Scientific authority |
|---|---|---|
| M05 | Complete primary 26-direction scalar `V4*V4` pole and complete primary partial-BFM gauge completion. The independent gauge replay passes exactly; the complete inventory-independent scalar-operator replay remains required. | `BLOCKED_ATTEMPT1` |
| M06 | The 4 quadratic, 4 cubic, and primary 26 quartic directions can be assembled after M05 passes. A distinct aggregate rank-34 projector/audit has not been executed. | `LOCKED` |
| M07 | Degree-local Hermiticity/PQ checks exist, but the aggregate calculated counterterm-action check has not been executed. | `LOCKED` |
| M08 | Background-field gauge residue is known, but the required quantum-vector, heavy/light-ghost, gauge-parameter, and BRST-associated residue calculation is incomplete. | `LOCKED` |
| M09 | The FJ-like prescription is frozen structurally. The three VEV and three tadpole residues have not been calculated. | `LOCKED` |
| M10 | Goldstone identities and the 33 broken directions are structurally available. The identities cannot be evaluated before M08--M09 residues exist. | `LOCKED` |
| M11 | Selected cancellation targets exist, but complete derived counterterms are unavailable before M08--M10. | `LOCKED` |
| M12 | All 21 slot structures and dispatch classes exist. Complete derived coefficients cannot be populated before the remaining residue groups pass. | `LOCKED` |
| M13 | Earlier gates have bounded independent replays. A complete inventory-independent replay covering every M01--M12 residue group does not exist. | `LOCKED` |

## M05 implementation boundary

The primary implementation now contains all of the following:

- every one of the 328 real scalar internal directions;
- all 26 real Hermitian quartic input and output directions;
- all Sigma radial, bilinear, mixed, pure-Sigma, and `zEta` structures;
- exact rank-26 projection and independent primary verification backgrounds;
- the vector, Goldstone, and ghost functional-determinant pieces;
- M02 external-field conversion exactly once;
- exact cancellation of the partial-BFM gauge parameter;
- the complete primary 26-direction quartic residue table.

The independent gauge replay also passes with exact zero residual.  It uses a
new rank-26 background set and a separate normalized five-form action.  It is
still only one component of the complete M05 replay requirement.

These implementation components do not constitute an M05 pass.  The frozen
contract also requires a complete inventory-independent replay.  A gauge-only
replay, even if successful, cannot substitute for the missing independent
scalar full-operator reconstruction.

## Fail-fast consequence

M06--M13 remain scientifically locked.  Shared utilities may be prepared,
but no later test may be calculated or promoted until M05 attempt 2 satisfies
the complete frozen acceptance criterion.  If the independent scalar replay
is absent, the correct stopping state is the existing M05 implementation
block rather than an inferred pass.
