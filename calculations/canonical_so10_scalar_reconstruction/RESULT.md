# Canonical SO(10) scalar invariant gate: representation count and eta1 witness

## Disposition

**`ETA1_NEUTRAL_INVARIANT_EXISTS`**, with multiplicity **one** in `Sym²(126) x bar126 x 10`. The broader outcome is **`INVARIANT_BASIS_UNRESOLVED`**: all renormalizable PQ-neutral scalar *singlet multiplicities* have been counted, but an explicit, exact-rank `delta/epsilon` contraction basis has not been certified for every multiset. Consequently there is still no frozen parent scalar action, vacuum calculation, benchmark search, or fermion fit. The [canonical variant definition](RECORD.md) remains distinct from the [printed Babu–Khan scalar model](https://arxiv.org/html/1507.06712v2).

## Fail-fast representation result

For either choice of `126` chirality, the [published SO(10) product decomposition](https://doi.org/10.1103/PhysRevD.106.025013) gives

```text
Sym²(126) = 54 + 1050 + 2772 + 4125         (dimension 8001),
126 x 10  = 210 + 1050                        (dimension 1260).
```

The common `1050` occurs once; the conjugation label suppressed in dimension-only notation is fixed here by the explicit tensor witness. Independently, `count_d5_singlets.py` constructs the exact `D5` weight characters of the vector, symmetric-traceless `54`, and both Hodge chiralities of the middle five-form. It takes bosonic symmetric powers, multiplies characters, and extracts singlet multiplicities via the Weyl antisymmetrizer with `rho=(4,3,2,1,0)`. It also extracts all dominant highest weights in `Sym²(126)` and `126 x 10`, computes their dimensions with the Weyl formula, and reproduces the two displayed decompositions independently. It returns exactly **one** singlet for `Sigma Sigma Sigma* phi`. Dimension and known-singlet controls pass.

An explicit invariant is represented by the delta contraction

```text
I_eta = (1/(2! 2! 3!))
        Sigma_{ij l m n} Sigma_{ij p q r}
        Sigma*_{l m p q r} phi_n .
```

The two `Sigma` fields are identical commuting scalars, so this polynomial belongs to their symmetric square. `test_eta1_invariant.py` builds a 48-component `*Sigma=+i Sigma` Gaussian-integer five-form from 24 displayed seed components, checks self-duality on all 252 ordered-independent five-index choices, sets `phi=e_0`, and evaluates `I_eta=-48` **exactly**. A nonzero value proves the invariant exists. It is not the [source Eq. (24)](https://arxiv.org/html/1507.06712v2) `Sigma Sigma* Sigma* phi` monomial, which carries nonzero PQ charge under the stated scalar charges. This gate establishes an allowed quartic interaction, **not yet** that its singlet-VEV insertion produces the desired light-doublet mixing coefficient.

## Complete representation-count ledger, not yet a tensor basis

The exact charge filter gives 44 PQ-neutral scalar field multisets: 6 quadratic, 12 cubic, 26 quartic. The `D5` character calculation finds singlets in 26 of them (4, 4, and 18 respectively) and **34 complex invariant slots** (4 quadratic, 4 cubic, 26 quartic). Conjugate pairing implies 34 real Hermitian coefficient directions before quotienting valid field rephasings, but explicit Hermitian basis elements and their contraction normalizations are still unfrozen. The nonzero slots are:

| Degree | Field multiset | Singlet multiplicity |
|---:|---|---:|
| 2 | `Phi²`, `Sigma Sigma*`, `phi phi*`, `S S*` | 1 each |
| 3 | `Phi³`, `Phi phi phi*`, `phi² S*`, `phi*² S` | 1 each |
| 4 | `Phi⁴`, `Phi² Sigma Sigma*`, `Phi² phi phi*` | 2 each |
| 4 | `Phi² S S*`, `Phi Sigma² S`, `Phi Sigma*² S*` | 1 each |
| 4 | `Phi phi² S*`, `Phi phi*² S` | 1 each |
| 4 | `Sigma² Sigma*²` | 4 |
| 4 | `Sigma² Sigma* phi`, `Sigma Sigma*² phi*`, `Sigma² phi²`, `Sigma*² phi*²` | 1 each |
| 4 | `Sigma Sigma* phi phi*`, `phi² phi*²` | 2 each |
| 4 | `Sigma Sigma* S S*`, `phi phi* S S*`, `S² S*²` | 1 each |

The other 18 PQ-neutral multisets have zero SO(10) singlet multiplicity and must not be inserted as potential terms. Controls include `Sym²(54)` having one singlet, `126 x bar126` having one, and `Sigma² Sigma*²` having four, consistent with the [published `126 x 126` decomposition](https://doi.org/10.1103/PhysRevD.106.025013) and the four source quartic labels. The weight-character implementation itself is exact integer arithmetic; the publication is a separate product-decomposition comparator, not the source of the computed 44-row ledger.

One noteworthy **candidate missing from the printed claim of a general potential** is

```text
kappa Phi_ij phi_i phi_j S* + h.c.
```

It is SO(10)-invariant by direct index contraction, PQ-neutral, and has one singlet per conjugate multiset in the independent character count. It is distinct from the printed cubic `chi6 phi_i phi_i S*` and quartic `Phi² phi phi*` terms. This is a statement about the [potential as printed](https://arxiv.org/html/1507.06712v2), not a claim that its numerical examples would have used a nonzero `kappa`.

## Phase and accidental-symmetry preview

The allowed terms `chi4 Sigma² Phi S`, `chi6 phi² S*`, and `eta1 Sigma² Sigma* phi` have scalar-field phase vectors, in `(theta_Sigma,theta_phi,theta_S)`,

```text
chi4 : (2,0, 1)
chi6 : (0,2,-1)
eta1: (1,1, 0) = (chi4+chi6)/2.
```

With generic nonzero `chi4` and `chi6`, these constraints have rank two and leave just the intended fieldwise PQ rephasing `(1,-1,-2)`. Because each nontrivial scalar gauge irrep occurs once, Schur's lemma bounds connected internal symmetries commuting with `Spin(10)` to the three initial scalar phase rotations; thus **no extra connected internal symmetry commuting with the gauge group** survives for generic nonzero `chi4` and `chi6`. If either coefficient is set to zero in a benchmark, the pointwise symmetry must be rechecked. This does not settle discrete/global-quotient symmetries or vacuum Goldstone counting.

The same rank-two result means there are **not** three independent rephasings to make `chi4`, `chi6`, and `eta1` all real: `2 arg(eta1)-arg(chi4)-arg(chi6)` is invariant. The new `kappa` term has the same phase vector as `chi6`, yielding another relative phase if both coefficients are present. Thus the published real-`r,s` scalar restriction cannot simply be inherited by the variant; any such restriction would need its own CP or parameter-slice premise and validation. `verify_scalar_phases.py` replays these exact linear relations. Whether a physical CP phase survives after all vacuum/fermion conventions is not determined here.

## Verification, stopping boundary, and next gate

Run from repository root:

```powershell
python calculations/canonical_so10_scalar_reconstruction/verify_pq.py
python calculations/canonical_so10_scalar_reconstruction/test_eta1_invariant.py
python calculations/canonical_so10_scalar_reconstruction/count_d5_singlets.py
python calculations/canonical_so10_scalar_reconstruction/verify_scalar_phases.py
```

The immediate next gate is to realize **all 34 singlet slots** as normalized `delta/epsilon` contractions and demonstrate exact rank equals each representation multiplicity. For each multiset, exact evaluations on explicit canonical tensors can certify linear independence once the representation count gives the upper bound; mere random numerical rank cannot certify completeness. Then freeze Hermitian combinations, coefficient phases and allowable rephasings, retain the generic connected-symmetry result above while checking any tuned coefficient slice separately, and hash one parent action. Only that result could earn `INVARIANT_BASIS_CLOSED`. No vacuum, scalar point, flavor running, or proton phenomenology was performed here.
