# Open Seams

## Current state

There are no active seams and no active physics calculation.

```text
active_seams = []
active_physics_calculation = null
```

The first admitted seam, `BK_SO10_HEAVY_VECTOR_PS_TO_D6_BNV_SMEFT`, resolved `PASS` at its tree-level authority ceiling. The [admission record](BABU_KHAN_SO10_BNV_MATCHING.md) and [calculation result](../calculations/bk_so10_bnv_matching/RESULT.md) preserve the derivation and qualification.

The focused [Pati-Salam literature audit and admission record](BABU_KHAN_PS_RUNNING_AND_MI_MATCHING.md) found reusable gauge-leading-log and tree-level matching machinery and admitted the next bounded seam. Its [calculation result](../calculations/bk_ps_bnv_running_mi_matching/RESULT.md) resolved `PASS` at the one-loop gauge-leading-log and tree-level `M_I` matching ceiling. The result is qualified by the published high-scale-sextet beta convention.

No SMEFT/SMNEFT evolution below `M_I`, right-handed-neutrino threshold, LEFT/chiral matching, lifetime calculation, other source theory, or other relation class is active.

## Definition

A seam is a specific missing derivation, compatibility relation, recovery map, or explanatory connection between already identified parts of the scientific scaffold.

A seam is not:

- a famous unsolved problem named without a project-specific relation;
- a broad subject area;
- a desired theory or mechanism;
- an invitation to speculative calculation;
- a software feature or directory proposal.

## Admission requirements

An active seam must state:

1. the two or more scientific domains or objects being connected;
2. the exact missing relation;
3. the empirical or theoretical obligation motivating it;
4. the assumptions already fixed;
5. a falsifiable acceptance condition or stopping boundary;
6. the maximum authority its resolution could earn.

For example, “quantum gravity is unsolved” is not a seam. A controlled threshold-matching relation between a frozen unified matter sector and a specified low-energy effective theory could become one once its inputs and acceptance conditions are defined.

## Lifecycle

Potential seams are first compared with established literature and external frameworks. A seam is added to `project_state.json` only when it is precise enough to drive a calculation. It is removed or reclassified when resolved, refuted, absorbed into known physics, or shown to be underdefined.
