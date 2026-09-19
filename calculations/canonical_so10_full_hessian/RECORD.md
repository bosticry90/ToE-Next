# Canonical SO(10) full scalar Hessian gate

1. **Question:** Can every quadratic scalar fluctuation of frozen
   `PARENT_ACTION_V1` be derived in exact SM-irrep blocks and certified
   against the broken-gauge and PQ orbit vectors?
2. **Claim under test:** The complete 328-real-dimensional tangent space
   decomposes into known SM irreps; the action-derived Hessian preserves
   those blocks and has exactly the required symmetry-null directions at a
   generic stationary witness, before deliberate light-Higgs tuning.
3. **Authority ceiling:** Analytic scalar kernel only. No positive vacuum,
   physical scalar spectrum, doublet tuning, threshold input, fermion fit,
   or BNV prediction follows from the representation census alone.
4. **Frozen inputs:** [parent action v1](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md),
   SHA-256 `01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`;
   normalized `54`, `126`, and PQ-singlet VEV ansatz in the
   [prior record](../canonical_so10_vacuum_kernel/RECORD.md); the exact
   unbroken SM generators derived there. No parameter scan or CP truncation.
5. **Provenance/comparator:** The prior [partial vacuum kernel](../canonical_so10_vacuum_kernel/RESULT.md)
   supplies earned tadpoles, stabilizer, radial block, and a specified
   color-singlet doublet subspace. Published Babu--Khan scalar matrices are
   not authority for this exploratory variant.
6. **Method:** Restrict the D5 weight characters to the exact SM embedding
   and use the SU(3)xSU(2) Weyl alternating sum to count multiplicity
   spaces. Build quadratic forms by second directional derivatives of the
   same parent invariants on representatives of every irrep. Do not use a
   dense 328x328 symbolic matrix as the primary representation.
7. **Independent replay:** Cross-check the irrep census against the
   previously computed exact generator stabilizers and fixed-subspace
   counts. The vacuum `K,T` tensors in the `10_H` self-block receive an
   independent Julia index-loop replay. Every complete quadratic block,
   especially the inherited
   doublet subspace, requires independent contraction or representation
   replay before physical interpretation. Full Hessian nullity requires
   both Ward identity and explicit block-matrix multiplication.
8. **Adversarial checks:** Complexified tangent dimensions must sum to 328;
   conjugate-irrep multiplicities must agree; the broken adjoint minus SM
   adjoint must sum to 33 and embed in the scalar tangent. At a stationary
   point, each broken gauge vector and an independent PQ vector must be
   annihilated by the exact full Hessian. The generic witness must have no
   additional nullity; a tuned Higgs doublet would add four real zeros
   separately. Blocks must obey real/Hermitian and decoupling identities.
9. **Known limits:** The neutral-singlet multiplicity is five; the
   `(1,2,+/-1/2)` complexified multiplicities are four each; the previously
   derived doublet and radial restrictions must be recovered exactly.
10. **Stop:** No scan or light-Higgs tuning. Pass only after all SM blocks,
    including colored and mixed `126` sectors, and explicit 34-vector
    symmetry-nullity replay are complete. Otherwise return
    `FULL_HESSIAN_BLOCKED` with the exact unfinished blocks.
11. **Failure meaning:** A dimension or Ward-identity contradiction is a
    real inconsistency for this implementation/ansatz. An unmaterialized
    block is incomplete calculation, not evidence that the model lacks a
    physical vacuum or is refuted.
12. **Result:** [`FULL_HESSIAN_BLOCKED`](RESULT.md). The exact irrep census,
    Goldstone-irrep distribution, action-derived `10_H` self-block, explicit
    33+1 orbit-vector rank, and complete neutral-singlet `5x5` Hessian with
    its two checked null vectors are earned. Exact directional parent-action
    quadratics vanish for all 45 Lie-basis directions after tadpoles, and
    four mixed `Phi+Sigma` bilinear probes pass. An exact all-29-monomial
    bilinear oracle now reproduces the known `10_H` self and `eta` doublet
    entries and passes four additional off-diagonal `B(e,g)=0` probes. A
    nonzero-coupling exact stationary witness and per-irrep rank targets are
    frozen; its neutral radial rank is three. Mixed and remaining colored
    blocks, 34-vector *full-Hessian* multiplication, and full witness rank
    remain unearned.
