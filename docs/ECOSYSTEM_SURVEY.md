# Ecosystem Survey

## Purpose

This is a preliminary capability map whose primary rule is: know what exists so ToE-Next does not rebuild it casually. Listing a tool or framework does not adopt it, install it, or make it a project dependency.

The empty `external_frameworks_installed_for_project` array in [`project_state.json`](../project_state.json) means that ToE-Next has adopted no external framework as a project dependency. It does not mean this machine lacks scientific software.

## Existing computational capabilities

The following capabilities were detected on the machine. They must still be revalidated in the calculation-local environment when used.

| Capability | Verified status | Potential role | ToE-Next dependency |
|---|---|---|---|
| Python 3.10 | Installed at an explicit machine path | Orchestration and calculation-local environments | No |
| SymPy 1.14.0 | Importable | General symbolic mathematics | No |
| Python-FLINT 0.9.0 | Importable | Exact integers, rationals, polynomials, and matrices | No |
| NumPy 2.2.6 / SciPy 1.15.3 / mpmath 1.3.0 | Importable | Numerical algebra, integration, optimization, roots, and precision replay | No |
| Z3 Python bindings | Importable | Logical consistency and constraint systems | No |
| cvc5 Python bindings 1.3.4 | Importable | Independent satisfiability and constraint checks | No |
| Hypothesis 6.165.1 | Importable | Property-based and adversarial testing | No |
| Cadabra 2.5.14 | Installed and callable by explicit path; not assumed on PATH | Tensor, covariant, spinor, gamma, GR, and QFT algebra | No |
| Julia 1.12.6 | Installed and callable by explicit path; not on PATH | High-performance numerical and exact calculation host | No |
| Lean / Lake | Launchers detected on PATH; toolchain readiness requires revalidation before use | Narrow exact theorems and decisive formal claims | No |

Detection is not adoption. Versions are recorded here as an initial capability observation; authoritative reproduction versions belong in the calculation that uses them.

## Preserved/recoverable capabilities

| Capability | Status | Potential role | Required action before use |
|---|---|---|---|
| Julia Nemo | Recorded in a legacy-scoped Julia environment, not configured for ToE-Next | Independent exact-algebra replay | Build or select a calculation-local environment and verify the package |
| Julia OrdinaryDiffEq | Recorded in a legacy-scoped Julia environment, not configured for ToE-Next | ODE/PDE dynamics, flow, evolution, and stability | Build or select a calculation-local environment and verify the package |
| VPC | Preserved external capability with a bounded historical calibration | Selective independent verification for claims fitting trusted operations | Recover deliberately, define a claim-specific profile, and revalidate scope |

Preserved capability does not authorize a live dependency on the legacy custody tree. Any recovered tool or environment must be established independently for the active calculation.

## External ecosystem candidates

These established resources may fill scaffold roles if a concrete scientific need justifies adoption:

| Capability | Existing resource | Default ToE-Next action |
|---|---|---|
| Particle-property and phenomenology baseline | PDG | Reference; do not rebuild |
| Experimental high-energy datasets | HEPData | Interface only when a claim needs the data |
| Particle-model encoding | FeynRules / UFO | Reuse a maintained representation when suitable |
| EFT coefficient interchange | WCxf | Adopt the format if an active calculation needs exchange |
| EFT running and matching | `wilson` | Evaluate before implementing equivalent machinery |
| Flavor observables | `flavio` | Reuse when its domain matches the claim |
| SMEFT reference models | SMEFTsim | Compare or reuse rather than duplicate |
| Collider matrix elements and events | MadGraph | Invoke externally for a defined collider claim |
| Broad BSM inference | GAMBIT | Defer until an inference problem justifies its scale |
| Tensor and gravity algebra | xAct | Compare with Cadabra and use the smallest competent route |

## Adoption test

Before adopting an external framework, a calculation must identify:

1. the exact missing capability;
2. why current tools or a standard interface are insufficient;
3. the smallest required integration surface;
4. provenance, license, version, and reproducibility requirements;
5. expected storage and maintenance cost;
6. how the framework will be removed or replaced if it fails the claim.

No framework is installed, vendored, copied, or configured merely to populate the scientific scaffold.
