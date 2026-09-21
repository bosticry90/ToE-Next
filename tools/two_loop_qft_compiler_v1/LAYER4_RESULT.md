# TWO_LOOP_QFT_COMPILER_V1: promotion layer 4

## Disposition

Layer 4 passes:

\[
\boxed{\texttt{TWO\_LOOP\_DIAGRAM\_GENERATOR\_PASS}}.
\]

The model-independent topology engine, its independent half-edge replay, the
index-summed vertex catalog, the layer-3 one-loop inventory regression, the
ordered quartic-heavy-ghost rule, all 1,900 canonical records, and a second
complete species enumeration pass. Every statistics sign and symmetry
denominator is resolved.

The passed layer-3 result remains
`BACKGROUND_FIELD_PHYSICAL_VERTEX_LAYER_PASS`. Layer 5 counterterm derivation
is now authorized but was not started. Tensor reduction, integral evaluation,
and finite `C1_GS` assembly remain locked. The gauge and BFB physics statuses
do not change.

## Model-independent topology subpass

[`diagram_topology.py`](diagram_topology.py) enumerates connected, 1PI,
amputated two-point multigraphs with labelled external background legs,
parallel propagators, and self-loops. Renormalizability gives

\[
n_3+2n_4=2L.
\]

The result contains two one-loop and nine two-loop topologies. The two-loop
classes contain four cubic vertices, two cubic plus one quartic vertex, or two
quartic vertices. Automorphism factors include vertex relabellings, identical
parallel edges, and bosonic self-loop flips.

An independent implementation starts from labelled half-edge pairings rather
than adjacency multisets. It reproduces exactly the same two and nine
canonical graphs. The topology inventory SHA-256 is

```text
778fe1a80234f7f5fc3c9cbdd02d465bf351f2958d509ef16fc9d2a6c0806021
```

Manual scalar controls reproduce the real-`phi^4` one-loop tadpole factor
`1/2`, two-loop sunset factor `1/6`, and two-loop double-scoop factor `1/4`.
The cubic and mixed cubic/quartic topology counts also replay. Independent
field-colored inventories agree for real `phi^4` (2 diagrams), cubic scalar
theory (2), scalar QED (8), Yang--Mills/ghost (24), and Abelian Higgs in
`R_xi` (46).

## Counterterm placeholders

The generator records 21 future one-loop-with-counterterm slots covering
field, mass, gauge-parameter, gauge-coupling, VEV, tadpole, and generic vertex
insertions. Every coefficient remains `null`; layer 5 has not started.

## Canonical tensor-index inventory

The derived layer-4 catalog contains 168 renormalizable, no-Yukawa,
gauge/scalar vertex signatures tied to the immutable partial-BFM action hash

```text
2ea3aef2e227557db52ec31d9acb48d348dc07fe039001800240e4691ad58491
```

Field assignment is stored in exact index-summed physical-mass-basis form.
For example, `H[a]`, `a=0,...,289`, carries mass identifier `m_H[a]^2`; this
represents the complete finite component sum without materializing dense
`328^3` or `328^4` tensors.

Across the nine topologies the generator produces 1,896 base colored/species
graphs after automorphism quotienting. Four contain the quartic heavy-ghost
vertex and each resolves into direct and exchange ordered-flow terms, yielding
1,900 final records. Every record contains
its topology ID, vertex IDs, ordered line assignment, finite dummy-index
domain, propagator and mass IDs, background channels, resolved statistics
sign, symmetry factor, deterministic loop-momentum routing, unreduced
numerator/denominator skeletons, coupling/group tensor IDs, and immutable
action hash. The inventory SHA-256 is

```text
46f35ed04bff58cd9afd3673da724c376209cac0cd3cd4a15ff252d6ad1ae837
```

The same engine at one loop recovers the six required heavy
vector/Goldstone/ghost inventory classes: bubble and seagull/tadpole graphs for
each sector. Evaluation remains under the passed layer-3 determinant
authority.

## Ordered quartic-ghost closure

The equivariant action contains

\[
\frac{\xi}{2}f^i{}_{j\alpha}f^k{}_{\ell\alpha}
\bar u_i u^j\bar u_k u^\ell.
\]

Left Grassmann differentiation in the ordered slots
`ubar[a],u[b],ubar[c],u[d]` gives

\[
\xi\left(f_{ab\alpha}f_{cd\alpha}
-f_{cb\alpha}f_{ad\alpha}\right).
\]

The two terms define direct and exchange ghost-flow channels. Each channel
stores its local flow pairing, number of closed ghost loops, loop sign,
coefficient sign, and combined Grassmann sign. Four base graphs therefore
produce eight ordered channel records. The derivative regression and all eight
statistics signs pass.

A second enumerator uses recursive edge assignment and an independently coded
canonicalization rather than the primary Cartesian edge-coloring algorithm.
It reproduces all 1,896 base graphs, all 1,900 final records, and every symmetry
denominator with zero set difference and zero residual.

## Authority boundary

No two-loop amplitude, numerator reduction, counterterm coefficient, master
integral, or finite threshold is reported. The 1,900 records are a completed
diagram inventory, not a value of `C1_GS`.

## Reproduction

```powershell
python tools/two_loop_qft_compiler_v1/compile_layer4_topologies.py
python tools/two_loop_qft_compiler_v1/independent_topology_replay.py
python tools/two_loop_qft_compiler_v1/check_topology_controls.py
python tools/two_loop_qft_compiler_v1/layer4_vertex_catalog.py
python tools/two_loop_qft_compiler_v1/enumerate_layer4_species_diagrams.py
python tools/two_loop_qft_compiler_v1/check_quartic_ghost_vertex.py
python tools/two_loop_qft_compiler_v1/independent_species_diagram_replay.py
python tools/two_loop_qft_compiler_v1/check_field_colored_controls.py
python tools/two_loop_qft_compiler_v1/check_layer4_one_loop_regression.py
python tools/two_loop_qft_compiler_v1/audit_layer4_gate.py
```
