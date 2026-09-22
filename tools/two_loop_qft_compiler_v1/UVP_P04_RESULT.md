# UVP_P04 result: rank-two d-dimensional tensor reduction

## Disposition

```text
UVP_P04 = PASS
Layer-5A progress = 4/27
Total contract progress = 4/39
Next authorized test = UVP_P05
```

P01--P03 evidence remains unchanged. The engine gate is unearned, the
counterterm compiler remains blocked, and Layer 6 remains locked.

## Frozen tensor primitive

The tested Euclidean integral is

```text
T_mu_nu = mu^(2 epsilon) Integral_E[d^d k/(2*pi)^d
            * k_mu*k_nu/(k^2+m2)^2],
d = 4 - 2 epsilon,
m2 > 0.
```

Rotational invariance requires

```text
T_mu_nu = delta_mu_nu/d * S,
S = Integral_E[k^2/(k^2+m2)^2].
```

The scalar contraction has normalized pole residue `-2*m2`. Retaining the
exact `1/d` factor through the Laurent algebra gives

```text
T_mu_nu|pole
 = delta_mu_nu*(-m2/2)/(16*pi^2*epsilon_bar).
```

## Primary route

After radialization, the scalar contraction contains

```text
(1+m2/t)^(-2) = 1 - 2*m2/t + 3*m2^2/t^2 - ... .
```

The `-2*m2/t` term is the local logarithmic UV coefficient. The primary
reducer then applies `delta_mu_nu/(4-2*epsilon)` before expanding in epsilon.
Contracting the reduced tensor with `delta^mu_nu` returns the scalar
contraction with exact residual zero.

## Independent replay

The replay does not import the primary tensor reducer. A Schwinger parameter
and differentiated Gaussian source give

```text
Integral[k_mu*k_nu*exp(-s*k^2)]
 = delta_mu_nu*(4*pi*s)^(-d/2)/(2*s),
```

and therefore tensor coefficient

```text
mu2^epsilon*(m2)^(d/2-1)*Gamma(1-d/2)
/(2*(4*pi)^(d/2)).
```

Its pole coefficient is independently `-m2/2`, and its contraction residual
is also exactly zero.

## Premature-d=4 adversarial branch

The promoted route never substitutes `1/d -> 1/4` before Laurent expansion.
For this primitive the shortcut happens to leave the simple-pole residue
unchanged, but it loses the pole-times-epsilon finite contribution

```text
exact minus premature-d4 = -m2/4
```

in units of `1/(16*pi^2)`. The primary and replay derivations agree on this
missed term exactly.

## Evidence

- evidence-schema canonical SHA-256:
  `2f1030fabd314968997f86ce0bf461c488944eb5bf5cbbeaea28a1df7155fbe1`;
- primary artifact SHA-256:
  `097b96f20361d393b166b7a51c96167d999d8d798dcce508f497eaadbcedf441`;
- replay artifact SHA-256:
  `c8890ce8597309156871823239b7dc89e6366d9d8e042a4cfce7b55357d3a7a9`;
- UV/IR provenance SHA-256:
  `a0cc08644785913c282bb23120d1fabb9cb0809b3e5848f289d9da1bb5a9de9e`;
- combined evidence SHA-256:
  `8c848af052e922838a0329c717d89c24a38fc97e740b39151689e3eec8df4326`;
- current execution-ledger SHA-256:
  `d5b1e61b09431fdfb4a0429bbd4f7f0b4b4bdb6b731cd69239e665fd0359dd9f`.

No later test was executed.
