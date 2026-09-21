# UVP_P02 result: massive rank-zero logarithmic bubble

## Disposition

```text
UVP_P02 = PASS
Layer-5A progress = 2/27
Total contract progress = 2/39
Next authorized test = UVP_P03
```

The completed `UVP_P01` evidence is unchanged. The counterterm compiler
remains blocked and Layer 6 remains locked.

## Frozen integral and result

With

```text
d = 4 - 2 epsilon
1/epsilon_bar = 1/epsilon - gamma_E + log(4*pi)
```

the tested Minkowski integral is

```text
mu^(2 epsilon) Integral[d^d k/(2*pi)^d * (-i)/(k^2-m2+i0)^2].
```

Wick rotation maps it to

```text
mu^(2 epsilon) Integral_E[d^d k_E/(2*pi)^d * 1/(k_E^2+m2)^2].
```

For `m2>0`, the derived pole is

```text
1/(16*pi^2*epsilon_bar).
```

The normalized residue is exactly `1`, and

```text
d(residue)/d(m2) = 0.
```

## Primary route

After radialization with `t=k_E^2`, the primary calculation expands

```text
(1+m2/t)^(-2) = 1 - 2*m2/t + 3*m2^2/t^2 - 4*m2^3/t^3 + ... .
```

Only the mass-independent coefficient multiplying `t^(-1-epsilon)` is
logarithmically UV divergent. Every term containing `m2` is UV finite for
this primitive. The radial prefactor at `d=4` is `1/(16*pi^2)`, giving the
normalized pole residue `1`.

## Independent replay

The replay does not import the primary expansion. It evaluates

```text
mu2^epsilon * (m2)^(d/2-2) * Gamma(2-d/2) / (4*pi)^(d/2)
```

and independently extracts

```text
limit[epsilon * 16*pi^2 * integral, epsilon -> 0] = 1.
```

Its mass derivative also vanishes, and the primary-minus-replay residue is
exactly zero.

## UV/IR classification

- UV pole: yes;
- IR pole: no for `m2>0`;
- scaleless: no;
- mass dependence in the pole: none;
- `R*` subtraction: not required for this primitive.

## Evidence

- evidence-schema canonical SHA-256:
  `8a0b96724c7f7414a41f355658e74e8ec6a7b78c3e4e47f54c1cda85b86eaf60`;
- primary artifact SHA-256:
  `66d293fd5bd34a6c405fc3db797354b8f793bcc0e126f05920cfc520ad5ecc79`;
- replay artifact SHA-256:
  `42a39389d4c2ae6b7b5cc133b961d5e33771dd1c981e106640f35fab8f25f6ec`;
- UV/IR provenance SHA-256:
  `79c637dbbdd2e5f4174c806e0a7ad189eb762ba5cbf8c6f97677addc3ecbd75f`;
- combined evidence SHA-256:
  `549ce62f87a6c73bd0fbc60871a50de4d6ec8952fb92ca58adb2f5f45fee1013`;
- current execution-ledger SHA-256:
  `4d06a98051813afba0a9d5b6e2affb3201598931372fed4595ee706a9c2572bf`.

No later test was executed.
