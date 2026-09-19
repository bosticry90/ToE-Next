# Canonical scalar vacuum-kernel analytic gate

1. **Question:** Does the frozen canonical scalar action admit the intended
   `Spin(10) -> PS x D -> SM` vacuum ansatz, and can its stationarity,
   Goldstone, and scalar-block kernels be derived without source equations?
2. **Smallest claims:** The VEV-restricted polynomial and tadpoles follow
   from [parent action v1](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md);
   the proposed VEV stabilizers are computed on exact generators.
3. **Ceiling:** Analytic action consequences only. No numerical point, local
   minimum, global stability, light Higgs, fermion fit, flavor evolution, or
   proton-decay prediction is implied by a passing intermediate check.
4. **Frozen inputs:** Parent-action SHA-256
   `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`;
   `Phi_0=(omega/sqrt(60)) diag(-2 I6,+3 I4)`,
   `Sigma_0=(sigma exp(i thetaSigma)/(4 sqrt(2))) V`, where
   `V=wedge_(k=0..4)(e_(2k+1)+i e_(2k))`, `phi_0=0`, and
   `S_0=v exp(i thetaS)/sqrt(2)` in the parent's orientation and kinetic
   normalization. Initially take nonzero `omega,sigma,v`, but solve no
   stationarity equations by assigning numeric values.
5. **Provenance:** The earlier `54+126+10` breaking intent is a comparator,
   not authority for scalar coefficients, stationarity equations, or masses.
6. **Method:** Exact tensor evaluation of each v1 invariant at the VEV;
   symbolic differentiation of the generated polynomial; independent
   generator-orbit rank and centralizer analysis; then Hessian from the same
   action if those stages pass.
7. **Replay:** Exact contraction values and tadpoles require algebraic
   identities and independent checks. Stabilizers require both orbit rank
   and constructive subgroup identification. Goldstone nullity requires
   Ward-identity and explicit Hessian checks before physical eigenvalues.
8. **Fail-fast:** A nonzero omitted singlet or `phi` tadpole, phase dependence
   inconsistent with the exact invariants, wrong connected stabilizer or
   discrete remnant, broken-generator count mismatch, non-Hermitian Hessian,
   or unresolved contraction normalization stops downstream work.
   A full pass also requires every physical scalar block, including colored
   sectors, to be extracted from the same action; the explicit full Hessian
   must annihilate every independently computed broken-gauge orbit vector,
   with any additional null directions separately classified. The doublet
   quadratic form must be replayed independently before an inertia or
   one-light-Higgs claim.
9. **Known limits:** `omega` alone leaves `S(O6 x O4)`; nonzero `sigma` is
   expected to reduce the connected stabilizer to SM; setting mixed
   couplings to zero must remove the corresponding mixed Hessian pieces.
10. **Stop:** Complete only the analytic kernel; no parameter scan. If a
    required stage cannot be fully derived or independently checked, report
    `VACUUM_KERNEL_BLOCKED` with earned partial results rather than a pass.
11. **Negative meaning:** An ansatz or implementation failure does not refute
    all vacua of the action. `INTENDED_BREAKING_FAILS` requires an exact
    stabilizer contradiction for the frozen ansatz; `GOLDSTONE_OR_HESSIAN_INCONSISTENCY`
    requires an actual failure of a derived Hessian, not missing work.
12. **Result:** [`VACUUM_KERNEL_BLOCKED`](RESULT.md) at full colored-Hessian
    extraction. The action-derived vacuum, tadpoles, stabilizers, Ward-identity
    Goldstone obligation, radial Hessian, and quadratic form on the specified
    color-singlet doublet subspace are earned; no scan or physical mass
    interpretation follows.
