# UVP_P03 result: doubled-propagator mass-derivative consistency

## Disposition

```text
UVP_P03 = PASS
Layer-5A progress = 3/27
Total contract progress = 3/39
Next authorized test = UVP_P04
```

The completed P01 and P02 evidence records are unchanged. The counterterm
compiler remains blocked and Layer 6 remains locked.

## Frozen convention and result

The P01 and P03 Minkowski integrands are

```text
P01: +i/(k^2-m2+i0)
P03: -i/(k^2-m2+i0)^2.
```

Direct differentiation gives

```text
P03_integrand = -d(P01_integrand)/d(m2).
```

For `d=4-2*epsilon` and `m2>0`, the directly derived P03 pole is

```text
1/(16*pi^2*epsilon_bar),
```

with normalized residue `+1`.

## Route 1: direct doubled-line projection

The primary route does not read P01. It uses the exact auxiliary-mass
rearrangement

```text
1/(t+m2)^2
 = 1/(t+aux2)^2
 + (aux2-m2)*(2*t+aux2+m2)/((t+m2)^2*(t+aux2)^2).
```

The first term has unit logarithmic residue. The exact remainder begins as
`2*(aux2-m2)/t^3`, so after the radial `t` factor it is `O(t^-2-epsilon)`
and UV finite. Both physical- and auxiliary-mass derivatives of the promoted
residue vanish.

## Route 2: independent replay

The replay constructs the general Euclidean one-denominator formula

```text
mu2^epsilon*(m2)^(d/2-alpha)*Gamma(alpha-d/2)
/((4*pi)^(d/2)*Gamma(alpha))
```

and only then specializes to `alpha=2`. Its independently extracted normalized
residue is `+1`.

## Route 3: frozen-P01 derivative relation

The third route verifies the content hash of the terminal P01 evidence before
reading its normalized residue `-m2`. It then obtains

```text
-d(-m2)/d(m2) = 1.
```

It separately verifies the Minkowski numerator identity at integrand level.
The three pairwise residue differences and the integrand residual are all
exactly zero.

## UV/IR classification

- UV pole: yes;
- IR pole: no for `m2>0`;
- scaleless: no;
- auxiliary-mass dependence in the pole: none;
- `R*` subtraction: not required for this primitive.

## Evidence

- evidence-schema canonical SHA-256:
  `29499399ca6cc8317278869dd30e798f9e24819406ad6716380700407491006d`;
- primary artifact SHA-256:
  `f01b82a7925f20aa7854b40412af3c3a84140e8a2d5835d9a2e13194205ae132`;
- replay artifact SHA-256:
  `e93f071293a2047d950edb98c5a17f733795bb0d624439458384e93aad05190a`;
- P01-derivative artifact SHA-256:
  `834d23375b7a6126dab4141c8f1bb9d331a22b14b1115de04278a3da102ddf9c`;
- UV/IR provenance SHA-256:
  `e7650fcdb9ff758bcd1ffd852697ef45b364ddc6fa3a127c0022b5895f3d21da`;
- combined evidence SHA-256:
  `be4585b1188f61116490d810c9d66ad2f391963d05a01d69ca7233ccd849b4d2`;
- current execution-ledger SHA-256:
  `7f89b29775731b8d24eed996a2f2fdd1dba2a000169d232cfd013ec33ae903ab`.

No later test was executed.
