# Canonical scalar full-Hessian gate: bounded result

## Disposition

**`FULL_HESSIAN_BLOCKED`.** Exact Standard-Model-irrep decomposition now
accounts for every one of the **328 real tangent directions** after
complexification, and locates all 33 broken-gauge directions by irrep. The
action-derived `10_H` quadratic self-block, including its colored entries,
is explicit. The complete neutral-singlet `5x5` block is also derived and
annihilates its two independent symmetry-phase vectors. The mixed
`126_H`--`10_H` colored blocks, remaining `54_H` and `126_H` scalar blocks,
direct **full-Hessian** Goldstone multiplication, and full generic-witness
rank are **not** complete. Thus no complete physical scalar
spectrum, one-light-Higgs condition, or scalar benchmark is claimed.

## Exact bilinear oracle and stronger row probes

[`parent_bilinear_oracle.py`](parent_bilinear_oracle.py) evaluates every one
of the 24 Hermitian and five complex frozen parent monomials on exact raw
tensor states. For a real tangent direction `u`, it extracts the exact
quadratic coefficient `Q(u)` using five-point interpolation (valid because
the parent potential is quartic). Polarization gives

```text
B(u,v) = Q(u+v) - Q(u) - Q(v).
```

The module checks the frozen parent-action SHA-256 before evaluation. Its
[`regression controls`](verify_oracle_controls.py) reproduce the known
`10_H` color/weak self terms, `z6`, `z4`, the new `zK` contribution, and
the independently derived `eta` doublet mixing. The raw `126` doublet
representative is `sqrt(3)` times the previously normalized one, so the
raw `z4` bilinear is `-60` rather than `-20`; the `eta` mixed bilinear is
`192` in the same raw convention.

[`verify_oracle_goldstone_rows.py`](verify_oracle_goldstone_rows.py) then
computes **off-diagonal** `B(e,g)` values for four probes spanning `54`,
`126`, and `10` sectors against two broken generators. All four vanish
exactly after the three action-derived tadpole masses are substituted;
the complex monomial coefficients separately vanish in these probes.
These are stronger than `B(g,g)=0`, but four rows are **not** a basis of the
Goldstone-containing SM blocks and therefore do not certify all 34
full-Hessian null vectors.

[`define_generic_nullity_test.py`](define_generic_nullity_test.py) freezes a
nonzero rational/Gaussian-rational coefficient assignment at the raw VEV
`omega=sqrt(60), sigma=4sqrt(2), v=sqrt(2)`, solves only the three radial
tadpoles for `mPhi2,mSigma2,mS2`, and verifies them against the generated
vacuum polynomial. Its neutral radial block has rank three. The script
prints the required nullity and target rank for every exact SM irrep. Their
dimension-weighted totals are **34 null directions and rank 294**. This is
an *acceptance specification*, not an attained full-Hessian result. Once
every block is calculated, attaining rank 294 at this exact witness would
prove maximal generic rank on the stationary parameter branch, because
the 34 symmetry directions provide the opposite rank bound.

This calculation uses only [parent action v1](../canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md)
and the previously derived [normalized vacuum](../canonical_so10_vacuum_kernel/RESULT.md).
The published Babu--Khan scalar matrix was not imported.

## Exact SM-irrep census

The [character calculation](decompose_sm_tangent.py) restricts the D5
characters of `54`, `126`, `bar126`, two complexified vector `10` copies,
and the two real singlet directions to the exact unbroken SM embedding.
For a dominant weight `w=(w0,...,w4)`, the labels are

```text
SU(3) Dynkin labels: (p,q)=(w0-w1,w1-w2)
SU(2)L Dynkin label:  n=w3-w4
six times hypercharge: 6Y=2(w0+w1+w2)-3(w3+w4).
```

The complexified dimensions are `54+126+126+10+10+2=328`; the full
irrep table, multiplicities, and exact dimension sum print from the script.
The largest multiplicity is **five**, so an SM-equivariant Hessian can be
specified on multiplicity spaces no larger than `5x5` (with appropriate
real/conjugate pairing). The neutral-singlet multiplicity is five, and the
`(1,2,+/-1/2)` multiplicities are four on each conjugate side. All
conjugate-irrep counts agree. These checks also match the prior independent
SM fixed-subspace and stabilizer calculations.

Subtracting the unbroken SM adjoint (`8+3+1`) from the exact `45` adjoint
character gives the **33** broken-gauge complexified directions:

```text
(1,1)_{-1,0,+1}:          3 dimensions total
(3,1)_{-2/3} + c.c.:      6 dimensions total
(3,2)_{-1/6} + c.c.:     12 dimensions total
(3,2)_{+5/6} + c.c.:     12 dimensions total
```

Here `c.c.` denotes the conjugate SM irrep. Every broken-gauge irrep occurs
in the scalar tangent. The [explicit orbit calculation](construct_symmetry_orbits.py)
builds all 45 gauge tangent vectors on the VEV in an injective real tensor
coordinate representation: rank **33**. Adding the PQ tangent vector raises
the rank to **34**, because the PQ-charged singlet has a nonzero VEV. Therefore the
stationary full Hessian must have **at least 34 real symmetry zeros**: 33
gauge plus one PQ. A deliberately massless SM Higgs doublet would add four
different real zero directions; none was tuned here. The number **exactly**
34 at a generic stationary witness is not yet verified.

An [exact parent-invariant directional evaluator](check_gauge_orbit_quadratics.py)
also computes the `t²` coefficient along each of the 45 standard Lie-basis
generator orbit tangents. All vanish after the action-derived tadpoles;
the 45 tangents span the 33-dimensional gauge orbit, because the 12
stabilizer generators are nontrivial linear combinations of this basis.
The evaluator includes the surviving `Phi`, `Sigma`, and singlet-VEV
invariants, including all four independent `Sigma² Sigma*²` contractions.
It finds three exact raw quadratic patterns (multiplicities 5, 16, 24).
A [focused charged-singlet replay](check_charged_singlet_goldstone.py) and
four [mixed `Phi+Sigma` polarization probes](probe_mixed_orbit_bilinear.py)
pass as adversarial checks. These verify `g^T H g=0` for the Lie basis and
`g^T H h=0` for the four chosen mixed probes. The new bilinear oracle
adds four more `B(e,g)=0` checks, including a `10_H` probe. These still do
**not** establish `H g=0` against a basis of all 328 real fields; complete
irrep blocks remain absent.

## Complete neutral-singlet block

The [five-real-direction derivation](derive_neutral_singlet_block.py) extends
the *generated* VEV polynomial to the unique real `54` singlet and Cartesian
real/imaginary parts of the unique complex `126` and `S` singlets. In the
canonical coordinate order `(omega,sigmaR,sigmaI,vR,vI)`, after substituting
only the action-derived tadpoles, its exact Hessian is the previously
derived `3x3` radial block on indices `(0,1,3)` and **zero rows/columns**
at phase indices `(2,4)`. The script verifies multiplication by the
neutral gauge vector `(0,0,sigma,0,0)` and independent PQ vector
`(0,0,2sigma,0,-4v)`. An exact rational parameter witness gives rank three
for this block; hence a third neutral-singlet zero is not structurally
forced by the action. This is not a full-spectrum generic-witness test and
does not imply a stable vacuum.

## `10_H` vector self-block, including colored components

The [exact tensor derivation](derive_vector10_self_block.py) obtains, on
the frozen VEV, `K_ij=16(I_10-iJ_5)_ij` for the unnormalized singlet
five-form, and `T_ij=0`. An [independent Julia index-loop replay](verify_vector10_self_block.jl)
confirms both tensors. Write

```text
b_c=-2 omega/sqrt(60),       b_w=+3 omega/sqrt(60),
S0=v exp(i thetaS)/sqrt(2), J_5=diag(J_2,J_2,J_2,J_2,J_2),
J_2=[[0,-1],[1,0]].
```

On either color (`r=c`, six vector coordinates) or weak (`r=w`, four
coordinates) subspace, the `10_H` self-quadratic form is

```text
phi_r^dagger B_r phi_r + [phi_r^T D_r phi_r + h.c.],
B_r = [mphi² + muPhiPhi b_r + lambdaPhiphi1 omega²
       + lambdaPhiphi2 b_r² + lambdaSigmaphi1 sigma²
       + (lambdaVectorS/2) v²] I_r
       + (lambdaSigmaphi2/2) sigma² (I_r-iJ_r),
D_r = (z6+zK b_r) conjugate(S0) I_r.
```

The weak restriction agrees with the previously derived doublet `B,D`
subblock. The `zK` term splits the *self-block* color and weak holomorphic
coefficients through `b_c != b_w`; the full physical triplet and doublet
masses also require their `126_H` mixings. Since `T(Sigma0,Sigma0)=0`,
`zD` contributes no `10_H` self-quadratic term at this vacuum. No positivity
or triplet safety is inferred from an isolated self-block.

## Exact stopping boundary

The representation decomposition makes the rest of the job finite and
small-block, but it does not itself produce Hessian coefficients. The next
calculation must construct representatives of every SM multiplicity space,
evaluate every block as second directional derivatives of all 34 parent
invariants, and independently replay the doublet block. After substituting
the three action-derived tadpoles, multiply the resulting blocks by the
**explicit** 33 gauge and one PQ orbit vectors, then test a generic exact
stationary witness for additional nullity. Only a passing full calculation
can turn this gate into `CANONICAL_VACUUM_KERNEL_PASS`.

Reproduce the earned portion from repository root:

```powershell
python calculations/canonical_so10_full_hessian/decompose_sm_tangent.py
python calculations/canonical_so10_full_hessian/construct_symmetry_orbits.py
python calculations/canonical_so10_full_hessian/derive_neutral_singlet_block.py
python calculations/canonical_so10_full_hessian/derive_vector10_self_block.py
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no calculations/canonical_so10_full_hessian/verify_vector10_self_block.jl
python calculations/canonical_so10_full_hessian/check_charged_singlet_goldstone.py
python calculations/canonical_so10_full_hessian/check_gauge_orbit_quadratics.py
python calculations/canonical_so10_full_hessian/probe_mixed_orbit_bilinear.py
python calculations/canonical_so10_full_hessian/parent_bilinear_oracle.py
python calculations/canonical_so10_full_hessian/verify_oracle_controls.py
python calculations/canonical_so10_full_hessian/verify_oracle_goldstone_rows.py
python calculations/canonical_so10_full_hessian/define_generic_nullity_test.py
```
