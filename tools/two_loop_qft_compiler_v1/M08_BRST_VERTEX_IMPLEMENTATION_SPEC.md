# M08 BRST-vertex completion specification

## Scope and authority

This is an implementation specification beneath the frozen `UVP_M08` gate.
It does not amend the gate, retry M08, or promote any residue.  The existing
attempt-1 `BLOCKED` evidence remains authoritative.

The primary and independent canonical two-point pole operators are complete
and agree.  The only remaining calculation needed before a formal M08 retry is
the ghost-vector BRST three-point pole action and its implication for the
gauge-parameter counterterm basis.

## Required tree vertices from the frozen action

The notation `d_mu` in the partial fixing is the covariant derivative of the
unbroken group.  Its expansion must materialize, from the same frozen action:

- `ubar_H u_H V_H` and `ubar_H u_H V_H V_H`;
- `ubar_H u_H q_L` and `ubar_H u_H q_L q_L`;
- the background counterparts required by the Ward comparison;
- `cbar_L c_L q_L`;
- the equivariant `ubar_H u_H ubar_H u_H` interaction;
- the already-frozen scalar/Goldstone ghost interactions.

No parallel hand-maintained vertex source is permitted.

## Primary one-loop processes

Generate complete connected 1PI inventories for:

1. `Gamma(ubar_H,u_H,V_H)`;
2. `Gamma(ubar_H,u_H,q_L)`;
3. `Gamma(cbar_L,c_L,q_L)`.

The inventory must consider and either evaluate or power-count to zero every
allowed one-loop topology, including:

- ghost/vector triangles;
- one-ghost/two-vector triangles;
- seagull/cubic swordfish graphs from `ubar u A A`;
- the equivariant quartic-heavy-ghost/cubic-ghost-vector graph;
- scalar/Goldstone ghost graphs permitted by the frozen action.

Keep heavy and light internal-vector assignments, ghost-flow order, symmetry
factors, and Grassmann signs separately auditable.

## Local UV projection

Project the vertex poles through the tree derivative order.  The promoted pole
must be local and must retain the complete H-covariant tensor/operator form,
not only selected field components.  Combine it only afterward with the
already-frozen two-point operators.

The BRST/Slavnov--Taylor system must determine whether the two-point block
candidates are expressible with the single frozen heavy parameter `xi` and
the light parameter `eta_H`.  Do not average inequivalent blocks and do not
define a gauge-parameter counterterm by assuming the identity being tested.

If a complete primary and independent replay reproduce block-dependent poles
that cannot be absorbed by the frozen parameterization, adjudicate under the
contract's physics-level failure path.  If graph coverage or a projector is
missing, retain `BLOCKED`.

## Independent replay

The replay may read only immutable action/basis hashes.  It may not import the
primary graph inventory, symmetry factors, Grassmann signs, UV expansion, or
residue table.  Preferred routes are:

- independent half-edge diagram generation plus nonexceptional Feynman-
  parameter integration; or
- a complete equivariant-BRST functional pole construction with an explicit
  map to all three processes above.

Freeze both routes before comparison.  A formal M08 attempt 2 is authorized
only after exact/certified agreement of the complete two- and three-point pole
action and all required Ward/BRST residuals.
