# Canonical direct two-loop gauge/scalar finite-threshold gate

1. **Question.** Can the finite, nonuniversal, Yukawa-vertex-independent
   two-loop heavy boundary `C1_GS` be calculated for the frozen canonical
   positive-Higgs benchmark?
2. **Frozen authority.** `PARENT_ACTION_V1`, the exact positive-Higgs point,
   `DIRECT_ONE_LOOP_KERNEL_PASS`, `DIRECT_SM_TWO_LOOP_RUNNING_PASS`, the exact
   RG two-loop logarithmic kernel, and `YUKAWA_CONVENTION_V1`.
3. **Authority ceiling.** Model-input/implementation readiness and any finite
   coefficient actually produced by a complete renormalized two-loop
   background-field calculation.  No arbitrary finite constants, no flavor
   fit, no proton decay, no PS resummation, no replacement benchmark, and no
   global-BFB promotion.
4. **Primary method attempted.** Reuse the exact parent invariant evaluator to
   compile scalar-potential derivatives of order two through four on demand;
   inventory every further layer required for a two-loop hard-region match;
   preregister the centered-vector comparison before any `C1_GS` exists.
5. **Exact controls.** The new derivative oracle must reproduce the certified
   Hessian oracle, be permutation symmetric, recover nonzero `zEta`, native
   `z6`, VEV-induced `zK`, and `lambdaS` controls, and vanish above fourth
   order.
6. **Required two-loop layers.** Complete component/eigenstate lift; partial
   background-field gauge fixing; vector/Goldstone/ghost vertices; diagram
   enumeration and symmetry factors; one-loop field, mass, gauge, VEV and
   tadpole counterterms; tensor/IBP reduction; a validated massive-vacuum
   master evaluator; ultraviolet/infrared pole separation; and the common
   UV/EFT subtraction.
7. **Finite-constant checks.** Exact RG `L^2` and `L` reproduction,
   gauge-parameter cancellation, basis invariance, finite degenerate-mass
   limits, and one-loop regressions.  These checks are not claimable before
   the finite amplitude exists.
8. **Preregistered comparison.** Center `C1_GS`, then record its norm ratio,
   cosine alignment and projection against
   `(118.2134,-337.8911,219.6777)`.  A physical gauge refit remains mandatory.
9. **Technical comparators.** Martens
   ([arXiv:1011.2927](https://arxiv.org/abs/1011.2927)) defines the relevant
   two-loop background-field matching architecture but not this benchmark's
   finite result. Davydychev--Tausk
   ([hep-ph/9504432](https://arxiv.org/abs/hep-ph/9504432)) and TSIL
   ([hep-ph/0501132](https://arxiv.org/abs/hep-ph/0501132)) define useful
   reduction/evaluation comparators, not the missing model compiler.
10. **Stopping rule.** If any required finite-amplitude layer is absent, do
    not generate, fit, or compare a `C1_GS`; report the first unearned layers
    and preserve the lower-order passes.
11. **Result.** The scalar vertex input layer and comparison preregistration
    pass.  The diagram, counterterm, reduction, and master-integral layers do
    not exist, so `C1_GS` is uncomputed.  The gate is
    `DIRECT_TWO_LOOP_GAUGE_SCALAR_THRESHOLD_BLOCKED`; the gauge verdict remains
    `DIRECT_GAUGE_MATCHING_UNRESOLVED`, with `BFB_UNRESOLVED` carried forward.

