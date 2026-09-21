# UVP_P01 result: massive rank-zero tadpole

## Disposition

```text
UVP_P01 = PASS
Layer-5A progress = 1/27
Total contract progress = 1/39
Next authorized test = UVP_P02
```

The counterterm compiler remains blocked and Layer 6 remains locked.

## Frozen integral and result

With

```text
d = 4 - 2 epsilon
1/epsilon_bar = 1/epsilon - gamma_E + log(4*pi)
```

the tested Minkowski integral, including the scalar propagator numerator, is

```text
mu^(2 epsilon) Integral[d^d k/(2*pi)^d * i/(k^2-m2+i0)].
```

Wick rotation maps it to

```text
mu^(2 epsilon) Integral_E[d^d k_E/(2*pi)^d * 1/(k_E^2+m2)].
```

For `m2>0`, the derived pole is

```text
-m2/(16*pi^2*epsilon_bar).
```

Thus the normalized residue in units of
`1/(16*pi^2*epsilon_bar)` is exactly `-m2`.

## Primary route

The primary calculation uses an auxiliary squared mass `aux2` and the exact
large-loop-momentum rearrangement

```text
1/(t+m2)
 = 1/(t+aux2)
 + (aux2-m2)/(t+aux2)^2
 + (aux2-m2)^2/((t+m2)*(t+aux2)^2).
```

The final term is UV finite after radialization.  The two logarithmic master
coefficients are `-aux2` and `+1`, so their sum is

```text
-aux2 + (aux2-m2) = -m2.
```

The auxiliary mass cancels exactly.

## Independent replay

The replay does not import the primary expansion.  It evaluates

```text
mu2^epsilon * (m2)^(d/2-1) * Gamma(1-d/2) / (4*pi)^(d/2)
```

and independently extracts

```text
limit[epsilon * 16*pi^2 * integral, epsilon -> 0] = -m2.
```

The primary-minus-replay residual is exactly zero.

## UV/IR classification

- UV pole: yes;
- IR pole: no for `m2>0`;
- scaleless: no;
- auxiliary mass: cancelled;
- `R*` subtraction: not required for this primitive.

## Evidence

- evidence-schema canonical SHA-256:
  `8240e1b8594c21a952cfd22c599ea0116d7e664f7782227a7487337cf4d93f7b`;
- primary artifact SHA-256:
  `3a7ca69ddc77b722f2bf4f38d71ffde20498061a8c4b181b4e88a269d19c33f8`;
- replay artifact SHA-256:
  `3405590993437058d2c377b505babb99ea303ce3069c5e8ce0de326dfacae237`;
- UV/IR provenance SHA-256:
  `ad6646b107c543a2439d73be2522a0db6ab38a2774ca3c43213a44c639a749fa`;
- combined evidence SHA-256:
  `7d9a646003c1a46a1bc693289c91ea1d7bea844f05dabe3e8a5b06d2bce1f071`;
- current execution-ledger SHA-256:
  `13a0bc6f202eaa5de3b71c74aab1acbbfe697ef597d66b1901bcfd1b2ca58f12`.

No later test was executed.
