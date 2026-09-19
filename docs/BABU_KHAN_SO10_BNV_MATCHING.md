# Babu-Khan SO(10) Baryon-Violation Matching

## Seam-admission decision

```text
SEAM: BK_SO10_HEAVY_VECTOR_PS_TO_D6_BNV_SMEFT
ADMISSION: ADMITTED_AND_RESOLVED
SOURCE AUTHORITY: WORKING_CANDIDATE_NOT_ACCEPTED
CALCULATION: BK_SO10_HEAVY_VECTOR_PS_TO_D6_BNV_SMEFT_TREE_MATCHING_V1
CALCULATION STATUS: PASS
```

The resolved seam is model-specific:

```text
Babu-Khan 2015 non-supersymmetric SO(10)
    -> GUT-scale heavy-vector exchange
    -> Pati-Salam-covariant dimension-six BNV operator boundary
    -> operator projection at the Pati-Salam-to-SM boundary
    -> standard dimension-six BNV SMEFT basis
```

The Pati-Salam stage is explicit because the source model breaks as
`SO(10) -> SU(4)_C x SU(2)_L x SU(2)_R x D -> SM`. A direct SO(10)-to-SMEFT running calculation above the intermediate scale is not admitted. The first calculation is the tree-level matching and operator-map layer only; it does not perform RG evolution, hadronic matching, or a lifetime calculation.

## Admission findings

The seam passes admission because:

- the source is version-frozen and specifies the heavy-vector operators, masses, couplings, family indices, breaking route, and physical-basis rotation conventions;
- the intermediate symmetry and its scale are named rather than hidden in a direct-SMEFT shorthand;
- the destination is a version-frozen four-operator dimension-six BNV SMEFT basis with explicit gauge and flavor indices;
- the first claim is algebraic and has cheap failures before numerical evolution;
- legacy SU(5) work supplies adversarial controls without supplying SO(10) premises;
- the result has a narrow authority ceiling and requires no new dependency or large payload.

The seam would not have been admitted as a direct `SO(10) -> SMEFT at M_U` calculation. That form would incorrectly evolve through a regime where Pati-Salam fields and symmetries remain active.

## Calculation record

### 1. Scientific question

Can the GUT-scale heavy-vector interactions stated in the Babu-Khan model be converted into a complete, convention-explicit, gauge-covariant dimension-six BNV operator boundary that passes through the model's Pati-Salam intermediate symmetry and projects consistently onto the standard SMEFT BNV basis?

### 2. Claim under test

After integrating out the two source heavy-vector classes at tree level while retaining their distinct masses, the four source current-current operators in Eq. (61) of Babu-Khan, with the physical-basis structures and rotations of Eqs. (62)-(64), admit a unique coefficient-tensor map into:

```text
Q_duql
Q_qque
Q_qqql
Q_duue
```

for the Standard-Model field sector, plus an explicitly separated right-handed-neutrino/intermediate-EFT sector wherever the standard SMEFT field content is insufficient. The map must preserve color and weak contractions, mass dimension, full flavor indices, mediator provenance, relative normalization, and signs.

The calculation must not force a source term containing an active right-handed neutrino into the four-operator standard SMEFT basis. Such a term must remain in the Pati-Salam or neutrino-extended EFT until a later threshold match is defined.

### 3. Scope and authority ceiling

In scope:

- gauge-boson-mediated dimension-six BNV interactions only;
- both Babu-Khan heavy-vector classes, denoted `(X,Y)` and `(X',Y')`;
- tree-level low-momentum expansion through order `1/M_X^2`;
- full three-generation weak-basis coefficient tensors;
- Pati-Salam covariance and branching into Standard Model fields;
- the four standard dimension-six BNV SMEFT operators and any separately identified right-handed-neutrino sector.

Out of scope:

- scalar-mediated proton decay;
- loop matching, RG evolution, electroweak or LEFT matching;
- numerical Yukawa fitting or selection of a Babu-Khan benchmark point;
- hadronic matrix elements, partial widths, lifetimes, or experimental exclusion;
- viability of the complete Babu-Khan model, SO(10) generally, or any ToE claim.

A pass establishes only a controlled tree-level operator boundary for this source model. It does not establish phenomenological viability or net assumption compression.

### 4. Frozen inputs and assumptions

Source theory:

- K. S. Babu and S. Khan, arXiv [`1507.06712v2`](https://arxiv.org/abs/1507.06712v2), especially the breaking chain and Eqs. (61)-(64);
- Higgs and breaking specification `54_H + 126_H + 10_H` with the Pati-Salam-plus-discrete-parity intermediate stage;
- source definitions `k_1 = g_U/(sqrt(2) M_(X,Y))` and `k_2 = g_U/(sqrt(2) M_(X',Y'))`;
- source mass relations `M_(X,Y)^2 = g_U^2 omega_s^2` and `M_(X',Y')^2 = g_U^2 (omega_s^2 + sigma^2)`;
- the heavy-vector masses remain distinct symbolic positive parameters; neither equality nor near-degeneracy is assumed;
- source family indices remain general and no numerical fermion fit is imported.

Destination convention:

- S. Banik, A. Crivellin, L. Naterop, and P. Stoffer, arXiv [`2510.08682v2`](https://arxiv.org/abs/2510.08682v2), Table 1 definitions of `Q_duql`, `Q_qque`, `Q_qqql`, and `Q_duue`;
- weak-eigenstate flavor indices and the source's explicit color and `SU(2)_L` epsilon conventions;
- Wilson coefficients have mass dimension `-2` and mediator-separated contributions remain identifiable;
- any four-component to two-component conversion, charge-conjugation convention, Fierz identity, or epsilon-index permutation must be written explicitly in the result.

Scale treatment:

- the tree-level effective action is defined below both GUT-scale heavy-vector poles with exact `1/M_(X,Y)^2` and `1/M_(X',Y')^2` dependence;
- `M_U` labels the high-scale boundary but is not substituted for either pole mass;
- no SMEFT RGE is applied above the Pati-Salam breaking scale `M_I`;
- Pati-Salam running and the numerical `M_U -> M_I` evolution are reserved for a later calculation.

The calculation is exact and symbolic at this stage. Numerical convergence and propagated parameter uncertainty are not applicable. Any unresolved convention or source ambiguity produces `BLOCKED`, not an invented numerical error bar.

### 5. Provenance and comparators

Primary sources and comparators:

- the Babu-Khan source model and operator equations above;
- the four-operator SMEFT definitions in arXiv `2510.08682v2`;
- R. Alonso et al., arXiv [`1405.0486v2`](https://arxiv.org/abs/1405.0486v2), as a one-loop BNV-SMEFT flavor/RG comparator only;
- C.-Q. Song and J.-H. Yu, arXiv [`2603.11158v1`](https://arxiv.org/abs/2603.11158v1), as a modern UV-to-SMEFT-to-LEFT-to-chiral pipeline comparator, not an adopted implementation.

The D:-connected SU(5) relevance audit returned `NO_MATERIAL_CHANGE` to source selection and `REUSABLE_SU5_METHODS_AND_BOUNDED_RESULTS_IDENTIFIED`. The legacy operator lift, sign controls, threshold guards, lattice interface, and uncertainty discipline are adversarial comparators only. All SO(10) coefficients must be freshly derived from the cited source.

### 6. Primary method and tool

Primary method: an analytic tree-level integration of each heavy-vector class followed by explicit spinor, color, weak-index, and flavor-tensor conversion into the frozen destination basis.

Primary tool: Cadabra for indexed tensor and spinor algebra, with a small calculation-local symbolic representation of the operator tensors. SymPy may orchestrate exact coefficient bookkeeping. No numerical engine is required at this stage.

Tool output is subordinate to the written derivation. No external framework is installed, and no legacy code is imported.

### 7. Independent replay decision and reason

Independent replay is required because charge conjugation, Fierz rearrangement, epsilon ordering, and identical-field flavor symmetries can change signs or factors while leaving expressions superficially plausible.

The replay will use an independently encoded exact tensor map in Python/SymPy or Julia/Nemo that does not consume the primary transformation output. VPC may check the final finite linear map only if its trusted operations cover the representation. Running the same formulas through two front ends does not count as independence.

### 8. Adversarial checks and falsifiers

The calculation fails immediately if any of these occurs:

1. a claimed SMEFT term is not invariant under `SU(3)_C x SU(2)_L x U(1)_Y`;
2. a source term cannot be embedded in a Pati-Salam-covariant intermediate operator or is silently evolved as SMEFT above `M_I`;
3. an active right-handed-neutrino term is discarded or forced into the four-operator standard SMEFT basis;
4. mass dimension, color antisymmetry, weak contraction, or required flavor symmetry is violated;
5. mediator-separated coefficients cannot reproduce the source's `k_1^2` and `k_2^2` dependence;
6. the map depends on an unstated charge-conjugation, Fierz, phase, or epsilon convention;
7. primary and independent coefficient maps disagree after an explicit convention transformation;
8. the source's physical-basis operator structures in Eqs. (62)-(64) cannot be recovered symbolically from the weak-basis map.

Zero coefficients are results only when their absence follows from the source couplings and basis identities; they are not filled by assumption.

### 9. Known-limit and physical-assumption checks

Required checks:

- both heavy-vector contributions vanish independently as their corresponding mass tends to infinity;
- setting one mediator class absent leaves the other class's coefficient pattern unchanged;
- the equal-mass expression, if evaluated, is a derived limit rather than an input domain;
- generation-diagonal gauge interactions remain so before fermion-basis rotations;
- full unitary flavor rotations reproduce the source physical-basis structures without inserting a numerical Yukawa fit;
- the Standard Model field projection respects the published four-operator flavor identities;
- all assumptions excluded from this calculation—scalar exchange, intermediate running, threshold corrections, and hadronic inputs—remain visibly excluded from the result.

### 10. Stopping rule

Stop at the first of:

- **PASS:** a complete mediator-separated coefficient map, explicit Pati-Salam bridge, right-handed-neutrino disposition, convention ledger, and independent replay all agree;
- **FAIL:** any adversarial falsifier is triggered and cannot be resolved without changing the frozen source or destination;
- **BLOCKED:** the cited source does not specify enough interaction or convention data to derive a unique map, in which case the exact missing information is recorded and no downstream work begins.

Do not proceed to running, hadronic matching, or lifetimes in the same calculation.

### 11. Failure interpretation

Failure rejects the proposed recovery map under the frozen source equations and conventions. It may reveal an error, ambiguity, or missing intermediate-EFT definition in this implementation or in the use of the source. It does not refute all Babu-Khan parameter choices, SO(10), grand unification, or baryon-number-violating EFT.

A blocked result means the first arrow is underdefined; it is not evidence for or against the model.

### 12. Result and reproducibility record

Result:

```text
PASS
AUTHORITY = TREE_LEVEL_WEAK_BASIS_OPERATOR_MAP_ONLY
DOWNSTREAM = AUTHORIZED_FOR_SEPARATE_ADMISSION
```

The complete derivation, coefficient tensors, convention ledger, executable replays, hashes, and adversarial-test matrix are in [`calculations/bk_so10_bnv_matching/RESULT.md`](../calculations/bk_so10_bnv_matching/RESULT.md). The result establishes:

- `O_I -> +2 k1^2 Q_qque`;
- `O_II + O_III -> Q_duql` with distinct, explicit flavor wirings and `k1^2`, `k2^2` provenance;
- `O_IV -> -2 k2^2 Q_qqdN`, kept outside the four-operator standard SMEFT sector;
- `Q_qqql`, `Q_duue`, and `Q_uddN` are zero at this tree-level gauge boundary;
- the unequal pole coefficients are Pati–Salam-breaking threshold projections, not independent Pati–Salam-covariant coefficients above `M_I`.

No downstream work was executed in this calculation. The subsequent [focused literature audit and admission decision](BABU_KHAN_PS_RUNNING_AND_MI_MATCHING.md) admitted one gauge-leading-log Pati-Salam-running and tree-level intermediate-threshold calculation, which later resolved [`PASS`](../calculations/bk_ps_bnv_running_mi_matching/RESULT.md) at its bounded authority ceiling.

## Downstream anchors, not active inputs

Later records may evaluate the chain through Pati-Salam running, SMEFT/LEFT evolution, and hadronic observables. Candidate frozen anchors for that later review are:

- lattice matrix elements: J.-S. Yoo et al., arXiv [`2111.01608v1`](https://arxiv.org/abs/2111.01608v1), with scheme, scale, sign, units, momentum transfer, and uncertainties revalidated;
- charged-lepton channel: Super-Kamiokande, arXiv [`2010.16098v2`](https://arxiv.org/abs/2010.16098v2), `p -> e+ pi0` and `p -> mu+ pi0`;
- neutrino channel: Super-Kamiokande, arXiv [`2510.26232v2`](https://arxiv.org/abs/2510.26232v2), `p -> nu pi+` and `n -> nu pi0`.

These sources do not authorize downstream computation now. Their values and uncertainty models must be frozen again when a surviving coefficient map makes them relevant.
