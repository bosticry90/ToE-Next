# First BFB/runaway probe of the positive-Higgs point

**Disposition: `BFB_UNRESOLVED`.** No negative quartic was found in the preregistered set of 200 low-support rational tensor rays. This does **not** prove that the full 34-direction renormalizable potential is bounded below. The [positive relaxed-Higgs result](../canonical_so10_positive_higgs/RESULT.md) therefore remains a local tree-level benchmark only.

The probe used the exact homogeneous degree-four part of `PARENT_ACTION_V1` at the frozen [POINT.json](../canonical_so10_positive_higgs/POINT.json). The tested directions included pure real-`54_H`, self-dual-complex-`126_H`, complex-`10_H`, and PQ-singlet components; sign and scale variations of their pairwise mixtures; and selected three-field mixtures. The smallest **unnormalized** value among these rays was

```text
V4(Sigma_doublet_re) = 7169699367/640000000000
                       = 0.0112026552609375 > 0.
```

That is merely the minimum among the particular coordinate rays tested; their norms differ, and it is not a lower bound on the field sphere.

Three simpler analytic checks also pass. For a real traceless symmetric `Phi`, `tr(Phi^4) >= [tr(Phi^2)]^2/10`, so the frozen pure-`Phi` quartic obeys

```text
V4(Phi) >= [lambdaPhi1 + lambdaPhi2/10] [tr(Phi^2)]^2
        = 0.000052268 [tr(Phi^2)]^2 > 0.
```

The pure-`10_H` quartic is `0.1(phi†phi)^2 + 0.1|phi·phi|^2`, and the pure-singlet quartic is positive. These necessary single-field checks do not constrain every mixed field direction; in particular, they do not certify the self-dual `126_H` sector or the complete multi-field orbit space.

A negative quartic direction, if later found, would dominate lower-order terms under uniform scaling and would reject **this point's** global tree-level stability. The absence of one in 200 structured directions cannot support the opposite inference. No global optimizer, sum-of-squares certificate, gauge-unification calculation, flavor fit, or proton-decay calculation was performed.

Reproduce the exact structured screen from the repository root with:

```text
python calculations/canonical_so10_bfb_probe/probe.py
```
