# Parent-SO(10) reality sign of a real 120

```text
question = Do the two Pati-Salam bidoublets of one real 120 have opposite conjugation signs?
outcome = CORRECTED_REALITY_CONDITION_CONFIRMED
method = independent exact Clifford/exterior-power construction
2024_printed_point = NOT_USABLE_UNCHANGED
refit = NOT_STARTED
flavor_RGE = NOT_STARTED
source_switch = NOT_ADMITTED
```

## Scope and sources

This calculation tests a disputed **parent-representation sign**, not the
phenomenological viability of a GUT. It compares the resulting sign with
[Saad and Susič, arXiv:2604.04021v1](https://arxiv.org/html/2604.04021)
and applies its necessary consequence to the unchanged normal-ordering point
of [Babu, Di Bari, Fong and Saad, arXiv:2409.03840v1](https://arxiv.org/html/2409.03840).
The derivation below does not use the 2026 paper's `Σ`-intertwiner proof.
It builds the real parent tensor and its spinorial Yukawa coupling from Pauli
tensor products. The executable exact checks are in [`verify_sign.py`](verify_sign.py).

## Frozen construction and derivation

Work in Euclidean real-vector conventions with
`R^10 = R^6 ⊕ R^4`, where `Spin(6) × Spin(4)` covers the Pati-Salam group.
The real `120` is `Λ³R^10`, so its two electroweak bidoublets lie in
`Λ³R^4` and `Λ²R^6 ⊗ R^4`. Every component of the parent three-form is real.
No independent rephasing of these two pieces is inserted into its one
`SO(10)` Yukawa contraction.

The `Λ³R^4` piece Hodge-dualizes with the **real** four-dimensional epsilon
tensor to a real vector `h_μ`. The quaternionic `Spin(4)` bidoublet map

```text
q(h) = h0 I + i(h1 σ1 + h2 σ2 + h3 σ3),   hμ real
ε q(h)* ε⁻¹ = q(h)
```

therefore has the plus reality sign. For a neutral component,
`q = diag(z,z*)` with `z = h0 + i h3`: the two coefficients are `z,z*`.

For the `Λ²R^6 ⊗ R^4` piece, independently construct Hermitian Euclidean
`Cl(6)` matrices and restrict their rotation generators
`J_ab = [γ_a,γ_b]/4` to a chiral four-spinor. Fifteen independent generators
result, each traceless and anti-Hermitian. Thus a **real** six-dimensional
bivector maps to an anti-Hermitian `SU(4)` adjoint `X`, with
`X* = -Xᵀ`. Tensoring with the same quaternionic bidoublet gives

```text
(I⊗ε) (X⊗q)* (I⊗ε⁻¹) = -Xᵀ⊗q.
```

The extra minus is the opposite reality sign. In the explicit Cartan
direction `J_01+J_23+J_45`, the chiral-four weights are
`(i/2) diag(1,1,1,-3)`. For the neutral `q=diag(z,z*)`, the quark entries
are `iz/2, iz*/2`; the latter is `-(iz/2)*`. The fourth entry is `-3`
times the quark entry, reproducing the usual lepton Clebsch.

To lock this phase to the **same parent coupling**, not merely to a freely
chosen Pati-Salam adjoint convention, the script also builds ten `Cl(10)`
generators and a charge-conjugation intertwiner `C`, then compares the
restricted chiral `CΓ_[ijk]` matrices for real singlet and adjoint three-form
components. For all four real bidoublet modes, the raw adjoint/singlet matrix-entry ratios
are `-i` for the three quark weights and `+3i` for the lepton weight; the
opposite parent chirality conjugates them. The four-dimensional triple-gamma
/ Hodge identities introduce only real orientation signs, not a compensating
imaginary phase. Reversing the global orientation or the overall real-120
sign changes conventions but not the **relative** conjugation parity.

These are exact symbolic matrix equalities (SymPy), not numerical fitting.
The construction is independent of the 2026 paper's explicit `Σ` algebra,
although its final `s_1=+1, s_15=-1` agrees with that paper.

## Consequence for the printed 2024 point

Write the two up-type antisymmetric coefficients as `x` (singlet) and `y`
(adjoint, with its quark Clebsch normalized to one). Then the parent reality
condition and the `1:-3` quark/lepton Clebsch require

```text
u = x+y,       d = x*−y*,       e = x*+3y*,
d+e = 2u*,     hence |d/u + e/u| = 2 (u ≠ 0).
```

The 2024 point instead prints `d/u=e^(iφ)`, `e/u=r₂`, with
`φ=-1.35108` and `r₂=-0.355963+1.25289i`. Direct replay gives
`|e^(iφ)+r₂|=0.309414649`. This is incompatible with the necessary value
`2`; printed rounding cannot bridge the gap. Thus that **unchanged point**
cannot serve as a real-120 parent-`SO(10)` benchmark under the stated
single-coupling construction. This does not refute the
`10_R + 120_R + 126bar` model class or rule out a newly fitted point.

The earlier [printed-point audit](../bdfss_2024_point_audit/RESULT.md)
independently reproduced its Majorana masses. Those numbers remain a valid
replay **of the printed parameterization**, not a validated continuation
benchmark. The lack of one co-frozen `M_I`/flavor point and the unbounded
omitted Pati-Salam flavor evolution remain separate limitations; neither is
promoted here into an additional falsification.

## Verification and stop

Run `python calculations/real_120_sign_audit/verify_sign.py` from the project
root. It checks the Clifford algebra, parent chirality and charge conjugation,
15-dimensional compact adjoint, bidoublet epsilon reality, both signs,
`B-L` weights, and the 2024 modulus. No D: data, new package, fit, RGE,
threshold calculation, or downstream source selection was used.

Stop at this sign result. The two earlier Babu-Khan gauge-sector recovery
steps remain passed; their missing flavor input is not supplied by this audit.
