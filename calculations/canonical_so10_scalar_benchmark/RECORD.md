# Canonical SO(10) positive scalar benchmark search

## Preregistered question and authority

Does the frozen `PARENT_ACTION_V1` admit a stationary point in the finite domain below for which all 294 non-Goldstone scalar directions are strictly positive, before any electroweak-doublet tuning? A successful Stage 1 point is a local scalar minimum modulo 33 gauge and one PQ orbit. It is not a viable GUT, a fermion fit, a proton-decay result, or a physical threshold prescription. Stage 2 (one light complex SM doublet) is permitted only after an independently replayed Stage 1 point.

The parent action is `../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md` (SHA-256 `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`). The exact 35-block Hessian and rank-294 stationary witness are from `../canonical_so10_full_hessian/`. Published Babu--Khan scalar points are not inputs.

This record satisfies the charter's twelve fields as follows: (1) the question is scalar-local-minimum existence; (2) the claim is one verified positive point in the declared domain; (3) the authority ceiling is scalar-only local stability; (4) frozen inputs are the action, VEV ansatz, and bounds below; (5) provenance is the passed exact Hessian, with published Babu--Khan scalar points excluded; (6) primary method is exact-oracle compilation followed by small-block numerical semidefinite feasibility; (7) any survivor requires higher-precision and independent parent-action replay; (8) falsifiers are violated tadpoles, extra null modes, a negative physical eigenvalue, wrong hierarchy, or a light colored state; (9) known-limit controls are the exact rank-294 witness, block Hermiticity, gauge/PQ Ward zeros, and kinetic-metric conversion; (10) stop after a verified Stage 1 point or the stated finite numerical budget, and run Stage 2 only after Stage 1 success; (11) search failure is inconclusive without an exhaustive certificate; (12) result and reproducibility evidence are to be appended after execution, never inferred from solver status.

## Finite Stage 1 domain (frozen before candidate evaluation)

Choose the positive reference scale `omega = sqrt(60)` in the normalized VEV convention. Search dimensionless `x = sigma/omega` in `[0.001, 0.5]` and `y = v/omega` in `[0.001, 0.5]`, both logarithmically sampled. This imposes the intended hierarchy `omega > sigma` but does not assert that the VEV ratio equals a physical gauge-boson mass ratio. All 18 independent real quartic coefficients lie in `[-1,1]`. The four complex quartics `z4,zK,zEta,zD` have magnitude at most one; their phases span `[0,2 pi)`. Real cubic coefficients satisfy `|muPhi|/omega <= 1` and `|muPhiPhi|/omega <= 1`; the complex cubic `z6` is likewise bounded by `|z6|/omega <= 1`, with unrestricted phase. The free `10_H` quadratic coefficient obeys `mphi2/omega^2 in [-1,1]`. The three other quadratic masses are eliminated exactly by the action-derived tadpoles, not sampled.

These are coefficient bounds in the frozen action convention, not proof of perturbative loop control. A later benchmark must assess representation multiplicities and loop expansion separately. All three invariant scalar phases remain available; any real-coupling/CP slice is explicitly a restricted preliminary search and cannot establish absence in the full domain.

## Evaluation and stopping rules

Use the exact parent bilinear oracle to compile the 35 small SM multiplicity blocks. A candidate must satisfy the action-derived tadpoles, block Hermiticity/conjugate consistency, exactly 34 symmetry zeros and rank 294 before Higgs tuning. Project out the known gauge/PQ null vectors, then require a strictly positive margin in every physical block. Colored physical states must be non-tachyonic and not accidentally light: preregister `m_color^2 >= 10^-4 omega^2` for this first scalar-only gate, using the canonical kinetic metric rather than raw representative coordinates. This is **not** a proton-decay bound. A point reported as found requires higher-precision deterministic reevaluation and an independent calculation replay; optimizer flags are not evidence.

Exploration budget: at most 20,000 quasi-random/random Stage 1 candidates, then at most 10,000 global/local objective evaluations in promising restricted or full-domain searches. This is a heuristic finite-domain search, not exhaustive certification. If no verified point is found, return `BENCHMARK_SEARCH_NUMERICALLY_UNRESOLVED` unless a separate rigorous argument excludes the entire declared domain. `NO_BENCHMARK_IN_DECLARED_DOMAIN` is reserved for such an exhaustive certificate, not optimizer failure. Do not start Stage 2 without a Stage 1 pass. If Stage 2 occurs, require exactly four additional real doublet zeros (rank 290/nullity 38), no other zeros, and separate verification.

The fixed-ratio semidefinite-feasibility calculation is an additional deterministic search method within this domain, not an exhaustion of its continuous `(x,y)` range. Its small-block solver output is a lead only; deterministic eigenvalue and action-level checks govern disposition.

## Result and carry-forward

`CANONICAL_SCALAR_BENCHMARK_FOUND` at the local scalar-quadratic ceiling. The
exact-decimal [Stage 1 point](STAGE1_POINT.json) passed action-tadpole,
all-35-block direct-parent exact rank/nullity, positive generalized-eigenvalue,
colored-floor, and gauge-hierarchy checks. The separately recorded
[Stage 2 calculation](STAGE2_RECORD.md) also found an exactly defined
one-light-doublet tuning. Full evidence and exclusions are in
[RESULT.md](RESULT.md). No fermion fit, below-`M_I` evolution, or proton-decay
calculation began.
