# Julia calculation environment

This is a small, calculation-local Julia environment created fresh on C: from the machine's existing package cache. It was not copied from the legacy repository or its Julia environment.

It currently pins:

- Nemo 0.56.1 for independent exact algebra;
- OrdinaryDiffEq 7.2.1 for ODE evolution and numerical-method capability.

`Project.toml`, `Manifest.toml`, and `smoke.jl` are the only repository payloads. Julia itself, the depot, packages, artifacts, precompiled state, and caches remain outside Git on C:. Revalidate the relevant package and numerical controls for every consequential calculation.

Run from the repository root:

```powershell
& "$env:LOCALAPPDATA\Programs\Julia-1.12.6\bin\julia.exe" --startup-file=no --project=tools/julia tools/julia/smoke.jl
```

The smoke test establishes only that exact matrix arithmetic and a controlled elementary ODE solve are callable. It is not scientific evidence for a ToE claim.
