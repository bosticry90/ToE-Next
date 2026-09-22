# UVP_P05 result: rank-four and rank-six tensor reduction

## Disposition

```text
UVP_P05 = PASS
Layer-5A progress = 5/27
Total contract progress = 5/39
Next authorized test = UVP_P06
```

P01--P04 evidence remains unchanged. The evaluator engine gate is unearned,
the counterterm compiler remains blocked, and Layer 6 remains locked.

## Tensor primitives

The logarithmic Euclidean primitives use

```text
rank 4: Integral_E[k_i1*k_i2*k_i3*k_i4/(k^2+m2)^4]
rank 6: Integral_E[k_i1*...*k_i6/(k^2+m2)^5].
```

The primary reducer obtains

```text
rank 4:  3 pairings, denominator d*(d+2),       residue 1/24 per pairing;
rank 6: 15 pairings, denominator d*(d+2)*(d+4), residue 1/192 per pairing.
```

The scalar radial logarithmic residue is one in each case.

## Independent constructions

The primary implementation recursively pairs the first unpaired index with
each possible partner. The replay uses a distinct algorithm: it enumerates
the full index-permutation orbit, groups adjacent indices, and quotients only
afterward. The two pairing sets agree exactly with empty set differences.

The replay derives each common coefficient from Schwinger-parameter Gaussian
moments rather than importing the primary isotropic-tensor denominator.

## Symmetry and recursive contractions

- all 24 permutations of the rank-four indices preserve its pairing sum;
- all 720 permutations of the rank-six indices preserve its pairing sum;
- contracting rank six produces the corresponding rank-four coefficient;
- contracting rank four produces the rank-two coefficient;
- the final rank-two contraction recovers the scalar moment.

Every primary and replay contraction residual is exactly zero.

## Premature-d=4 adversarial branch

The promoted routes retain `d=4-2*epsilon`. Replacing the dimensional
denominators by their four-dimensional values before Laurent expansion would
miss finite per-pairing terms

```text
rank 4:  5/144
rank 6: 13/2304
```

in normalized `1/(16*pi^2)` units. Both implementations reproduce these
diagnostics exactly; no finite one-loop amplitude authority is claimed.

## Evidence

- evidence-schema canonical SHA-256:
  `22d90a23f7552f5e128b9b78aaab1c19454d6b1195402f80c656cba052de99ff`;
- primary artifact SHA-256:
  `0be759a316e1ed344775a103fcdb78033777e38ebcc1e34cc561b4e49ba9a48f`;
- replay artifact SHA-256:
  `0d2b91a0a4e46f103d8595a60fd77c4b456a0bd373a92322457bf553cbb8beda`;
- UV/IR provenance SHA-256:
  `6ff0aa6a02a9ed779406ffeffb1dd65cbc974b7aec7b8087e1afd342a410c627`;
- combined evidence SHA-256:
  `a2c8154d9d38d8d24fcf85f25b202bc7ea3c0ca7c45f34dd591c17990cda01da`;
- current execution-ledger SHA-256:
  `c8da4ad5bc87cecfb2b594fe17423c2d8a8f21d7239c57b706fcef56177ff004`.

No later test was executed.
