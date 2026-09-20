# Separate one-light-doublet tuning attempt

This Stage 2 calculation begins **only after** the Stage 1 point in
`STAGE1_POINT.json` passed direct-parent exact 35-block replay. Its smallest
claim is existence of a point in the same preregistered coefficient domain,
at the same `x=y=0.1` VEV ratios, with exactly one massless complex SM Higgs
doublet and all other physical scalar directions positive. It does not
establish a fermion fit, acceptable Yukawa mixture, radiative naturalness,
scalar-mediated baryon-number-violation safety, or global boundedness of the
potential.

Charter fields: (1) question—one light doublet with positive other modes;
(2) claim—one exact tuned point; (3) authority—scalar quadratic only;
(4) frozen inputs—the v1 action, Stage 1 point, and unchanged domain;
(5) provenance—the Stage 1 exact certificate; (6) method—bounded coupling
triples plus a one-variable root; (7) independent replay—direct parent
contractions at the algebraic root; (8) falsifiers—extra zeros, tachyons,
or bound violations; (9) limits—conjugate-doublet and gauge/PQ checks;
(10) stop—one verified point or exhausted targeted trials; (11) failure—no
general no-go follows from an unsuccessful trial; (12) result—the last
paragraph and linked point/result files.

The primary method is a bounded small-block search over selected allowed
`z6,zK,zEta` values, with a one-dimensional root solve in `mphi2/omega^2`
for the lowest Higgs-doublet eigenvalue, followed by deterministic
canonical-kinetic eigenvalue checks. This targeted grid is a discovery
device, not a model constraint or exhaustive parameter search. A
verified point requires the action-derived tadpoles, 33 gauge and one PQ
zero modes, one further zero eigenvalue in each conjugate four-dimensional
doublet multiplicity block (four real directions total), real rank 290,
strictly positive remaining physical directions, and the Stage 1 colored
floor `m_color^2 >= 10^-4 omega^2`. A distinct exact-parent replay is
required before the tuned point can be called established.

Adversarial checks include doublet-conjugate agreement, no second doublet
zero, no extra colored/neutral zero, coefficient-domain bounds, and replacement
of the floating-point root by an exact algebraic determinant root. The stopping
rule is one verified point or a bounded set of targeted coupling triples;
failure of a target choice is only
`STAGE2_NUMERICALLY_UNRESOLVED`, not a scalar no-go. The Stage 1 result is
retained regardless of Stage 2 disposition.

**Result:** Exact parent-action determinant tuning and four affected-block
replay pass. The [algebraic point](STAGE2_POINT.json) has exactly one zero
eigenvalue in each conjugate Higgs block, no extra zero, and positive colored
blocks; the other 31 blocks inherit the exact Stage 1 replay. The Stage 2
real rank is `290`, nullity `38`. See [RESULT.md](RESULT.md) for numerical
margins and authority limits.
