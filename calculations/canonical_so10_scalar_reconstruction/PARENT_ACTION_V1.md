# Canonical exploratory scalar parent action v1

This is a **new source-derived variant**, not the printed Babu–Khan scalar
potential or its numerical benchmark. Its fields, PQ charges, kinetic terms,
orientation, and `*Sigma=+i Sigma` convention are fixed in [RECORD.md](RECORD.md).
The scalar potential below is the most general local, renormalizable,
`Spin(10) x U(1)_PQ`-invariant polynomial for those fields, with one coefficient
per exact invariant-basis direction. No coefficient is set to zero here.
`Phi` is real symmetric traceless; `Sigma` is a complex self-dual 5-form;
`phi` is a complex 10-vector; `S` is a complex singlet. Tensor indices run
from 0 to 9 and repeated indices are summed. `h.c.` conjugates the entire
preceding complex monomial and coefficient.

Define `N = (1/5!) Sigma_{abcde} Sigma*_{abcde}`,
`u = phi*_i phi_i`, `t = phi_i phi_i`,
`p2 = Phi_{ij} Phi_{ji}`, `p3 = Phi_{ij} Phi_{jk} Phi_{ki}`,
`p4 = Phi_{ij} Phi_{jk} Phi_{kl} Phi_{li}`,
`K_{ij} = (1/4!) Sigma_{i abcd} Sigma*_{j abcd}`,
and `T_{ij} = (1/4!) Sigma_{i abcd} Sigma_{j abcd}`.
The self-dual 5-form makes `T` symmetric traceless. For the quartic with two
`Phi` fields, define

```text
L_PhiSigma = (1/(2*3!)) Phi_ij Phi_kl Sigma_{ikabc} Sigma*_{jlabc}.
```

For the unique `eta` monomial define

```text
E = (1/(2!*2!*3!)) Sigma_{ijlmn} Sigma_{ijpqr}
                       Sigma*_{lmpqr} phi_n.
```

The four independent `Sigma² Sigma*²` invariants are `Q0,Q1,Q2,X131`.
For sorted increasing index tuples `I,J,K`, use the antisymmetric components
`Sigma_{K I}` and set

```text
P_k[I,J] = sum_{K in C(10,k)} Sigma_{K I} Sigma_{K J},
Q_k = sum_{I,J in C(10,5-k)} |P_k[I,J]|²,       k=0,1,2.
```

Terms with repeated indices inside either 5-form are zero. For disjoint
tuples `A,B`, write `eps(A,B)` for the parity of their concatenation relative
to sorted order, and `eps=0` when the concatenation repeats an index. The
fourth invariant is the crossed delta contraction

```text
X131 = sum_{I,J in C(10,4)} sum_{A subset I, |A|=3}
       sum_{B subset J, |B|=1}
       eps(A,I\A) eps(B,J\B) eps(A,B) eps(I\A,J\B)
       P_1[I,J] conjugate(P_1[sort(A union B),
                              sort((I\A) union (J\B))]).
```

The graph has edge multiplicities `AB=CD=1`, `AC=BD=3`, `AD=BC=1` for
the two `Sigma` and two `Sigma*` tensors. Complex conjugation exchanges
the two identical tensor pairs, so `X131` is real. These definitions use
independent sorted-index sums; rescaling an invariant would only redefine
its coefficient, but **these** are the frozen v1 normalizations.

The potential `V = V2 + V3 + V4` is:

```text
V2 = mPhi² p2 + mSigma² N + mphi² u + mS² |S|².

V3 = muPhi p3 + muPhiPhi (Phi_ij phi*_i phi_j)
   + [ z6 t S* + h.c. ].

V4 = lambdaPhi1 p2² + lambdaPhi2 p4
   + lambdaPhiSigma1 p2 N + lambdaPhiSigma2 L_PhiSigma
   + lambdaPhiphi1 p2 u + lambdaPhiphi2 (phi*_i Phi_ij Phi_jk phi_k)
   + lambdaPhiS p2 |S|²
   + lambdaSigma1 Q0 + lambdaSigma2 Q1
   + lambdaSigma3 Q2 + lambdaSigma4 X131
   + lambdaSigmaphi1 N u + lambdaSigmaphi2 (phi*_i K_ij phi_j)
   + lambdaPhiVector1 u² + lambdaPhiVector2 |t|²
   + lambdaSigmaS N |S|² + lambdaVectorS u |S|²
   + lambdaS |S|⁴
   + [ z4 (Phi_ij T_ij S)
       + zK (Phi_ij phi_i phi_j S*)
       + zEta E
       + zD (T_ij phi_i phi_j)
       + h.c. ].
```

All `m²` coefficients are real mass dimension 2; `muPhi` and `muPhiPhi`
are real mass dimension 1; `z6` is complex mass dimension 1. All `lambda`
coefficients are real and all `z4,zK,zEta,zD` are complex, dimensionless.
There are 24 real self-adjoint coefficient directions and five complex
directions, i.e. 34 real coefficient directions before allowed rephasings.
With generic nonzero complex interactions, two independent field rephasings
are available (the third is PQ), leaving three relative scalar-coupling
phases. This parameter count does **not** imply that all directions influence
the eventual chosen vacuum or observables independently.

Exact `D5` character multiplicities give the upper bound of 34. The explicit
contractions above reach the required ranks: nonzero witnesses for every
multiplicity-one multiset, exact rank two for each of five multiplicity-two
multisets, and exact rank four for `Sigma² Sigma*²`. See
`certify_simple_invariant_slots.py` and `certify_sigma_quartics.py`.
Conjugate monomials are included by Hermitian completion, not duplicated
as independent complex coefficients. No vacuum, Hessian, threshold, or
fermion fit has been inferred from this action.
