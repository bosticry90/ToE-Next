# Canonical SO(10) scalar action-definition gate v2

## Disposition and authority

**`ETA1_DOUBLET_MIXING_CONFIRMED`** and **`INVARIANT_BASIS_CLOSED`** for the
explicit exploratory `54_H+126_H+10_H+S_H` scalar theory defined by
[PARENT_ACTION_V1.md](PARENT_ACTION_V1.md) and [RECORD.md](RECORD.md).
The SHA-256 of `PARENT_ACTION_V1.md` is
`01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed`.
This establishes a complete renormalizable `Spin(10) x U(1)_PQ` invariant
scalar polynomial in the frozen tensor/kinetic conventions. It does **not**
establish a vacuum, one-light-Higgs spectrum, viable scalar benchmark,
Pati–Salam flavor RGE, fermion fit, or proton-decay prediction. The model is a
new source-derived variant, not a repair of the printed [Babu–Khan scalar
potential](https://arxiv.org/html/1507.06712v2).

## Fail-fast component calculation

Use zero-based indices `0..5` for `SO(6)~SU(4)` and `6..9` for
`SO(4)~SU(2)_L x SU(2)_R`, orientation `epsilon_0..9=+1` and
`*Sigma=+i Sigma`. Let

```text
V = wedge_{k=0}^4 (e_{2k+1}+i e_{2k}),
Sigma_0 = sigma V/(4 sqrt(2)),
J4 = *6 (e01+e23+e45),
E_a = J4 wedge e_a - i *10(J4 wedge e_a),   a=6..9.
```

`V` has 32 unit-modulus components, is exactly `+i` self-dual, and obeys
`(1/5!) Sigma_0 Sigma_0* = sigma²`. `J4` is the color-`SU(3)` singlet
direction in the `SU(4)` adjoint; `E_a` is its self-dual `126` doublet
fluctuation, with 4-color/1-weak and 2-color/3-weak parts. Each `E_a` has
six unit-modulus independent components, so the canonical complex-doublet
normalization for the kinetic term in [RECORD.md](RECORD.md) is
`E_a/sqrt(3)`; `phi_a` has unit normalization.

Insert `Sigma=Sigma_0+x_a E_a/sqrt(3)` and weak-vector `phi=y_n e_n`
into the unique `eta` invariant of [PARENT_ACTION_V1.md](PARENT_ACTION_V1.md).
Before the common normalization factor `sigma²/(32 sqrt(3))`, its exact
`delta Sigma`–`delta phi` bilinear is

```text
B = 192 * [ [1,-i,0,0], [i,1,0,0],
            [0,0,1,-i], [0,0,i,1] ]
  = 192 (1+iJ),       rank(B)=2,
J = diag( [[0,-1],[1,0]], [[0,-1],[1,0]] ).
```

The `delta Sigma*`–`delta phi` block vanishes in this convention.
Equivalently, with normalized complex weak components
`x_+=(x_6+i x_7)/sqrt(2)`, `y_-=(y_6-i y_7)/sqrt(2)` and the analogous
`(8,9)` pair, the bilinear is

```text
zEta * 4 sqrt(3) sigma² * (x_+ y_- + x'_+ y'_- ) + h.c.
```

The two pairs are the color-singlet electroweak-doublet components of
`(15,2,2)` and `(1,2,2)`, with opposite right-isospin/hypercharge
assignments; overall `T3R` sign is a convention. This proves that the
neutral `eta` invariant supplies the **required type of doublet mixing**
when its coupling and singlet VEV are nonzero. It does not prove one light
eigenvalue, positive heavy modes, or that other allowed interactions do not
change the projector. Exact Python tensor expansion and an independently
written Julia ordered-index replay agree on `B_66=192`, `B_67=-192i`, and
the zero conjugate entry.

## Complete explicit basis and coefficient ledger

The independent `D5` weight-character calculation gives 44 PQ-neutral
field multisets, 26 with singlets, and **34 singlet slots**: 4 quadratic,
4 cubic, 26 quartic. This supplies an exact upper bound. The explicitly
defined contractions in [PARENT_ACTION_V1.md](PARENT_ACTION_V1.md) achieve
that bound, so no additional independent renormalizable scalar invariant
exists for the frozen field and PQ assignment.
The action inventory is checked against **all 44** neutral multisets,
including the 18 with zero `Spin(10)` multiplicity.

| Group of multisets | Counted slots | Explicit certificate |
|---|---:|---|
| All quadratic and cubic; 12 single-multiplicity quartic slots | 20 | Exact nonzero tensor witness for each |
| `Phi⁴`, `Phi² Sigma Sigma*`, `Phi² phi phi*`, `Sigma Sigma* phi phi*`, `phi² phi*²` | 10 | Exact rank 2 for each pair |
| `Sigma² Sigma*²` | 4 | Exact rank 4 for `Q0,Q1,Q2,X131` |
| **Total** | **34** | Matches character upper bound |

For the four-five-form sector, exact Gaussian-integer evaluations on
explicit `+i` self-dual tensors give rank four, with `Q0,Q1,Q2,X131` as a
pivot basis; one displayed four-row minor has determinant
`-1680479354880`. The exact matrices also obey the representation-theory rank
ceiling, `Q0=N²`, invariance under an even coordinate permutation, and invariance
under a nontrivial rational `SO(2)` rotation. The deterministic witness
generation uses fixed seeds only to *find* witnesses; because all entries
and rank calculations are exact and the group count bounds the dimension,
the resulting independence certificate is not floating-point sampling.

The Hermitian action has 24 real self-adjoint coefficients and five complex
coefficients (`z6,z4,zK,zEta,zD`), yielding 34 real coefficient directions
before quotient by field rephasings. All required complex conjugates are
included. The five phase vectors have rank two in the three scalar field
phase variables, leaving PQ as the generic continuous commuting symmetry
and **three** invariant relative scalar-coupling phases. The invariant
combinations may be taken as `arg(zK)-arg(z6)`,
`2arg(zEta)-arg(z4)-arg(z6)`, and
`arg(zD)-arg(z4)-arg(z6)`. This is a statement about generic nonzero
couplings, not a vacuum Goldstone count or claim about tuned zero-coupling
slices.

## Reproduction and stopping boundary

From the repository root run:

```powershell
python calculations/canonical_so10_scalar_reconstruction/verify_pq.py
python calculations/canonical_so10_scalar_reconstruction/test_eta1_invariant.py
python calculations/canonical_so10_scalar_reconstruction/count_d5_singlets.py
python calculations/canonical_so10_scalar_reconstruction/verify_action_inventory.py
python calculations/canonical_so10_scalar_reconstruction/verify_eta1_doublet_mixing.py
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no calculations/canonical_so10_scalar_reconstruction/verify_eta1_doublet_mixing.jl
python calculations/canonical_so10_scalar_reconstruction/certify_simple_invariant_slots.py
python calculations/canonical_so10_scalar_reconstruction/certify_sigma_quartics.py
python calculations/canonical_so10_scalar_reconstruction/verify_scalar_phases.py
```

The next bounded calculation may derive the vacuum polynomial, tadpoles,
gauge/Goldstone spectrum, and scalar Hessian **from this action alone**.
No scalar benchmark scan begins before those analytic outputs and their
independent checks exist. The old sparse Babu–Khan doublet matrix, real-`r,s`
restriction, and scalar thresholds are not inherited. The two earlier
published-model heavy-vector BNV passes remain separate, unchanged results.
