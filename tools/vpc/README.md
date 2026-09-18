# Verified Physics Calculator

This directory contains the minimal active VPC exact verifier promoted for ToE-Next. It is a selective secondary verifier for finite, deterministic, typed, hash-bound exact claims that fit the frozen operation vocabulary. It is not a universal calculator, a model of nature, or scientific authority by itself.

## Promotion boundary

Promoted legacy source is limited to seven domain-neutral modules:

- canonical serialization and hashing;
- contracts and bounded resource limits;
- typed exact DAG validation and recomputation;
- exact rational/algebraic scalar and tensor operations;
- dimension checks;
- hash-bound local JSON source resolution;
- fail-closed errors.

The legacy CLI, product shell, plugins, numerical solvers, scientific profiles, C03/RV and CCFT-specific operations, Julia/Lean evidence adapters, release machinery, frozen results, and calibration payloads are not included. ToE-Next adds only a small wrapper, one operation-boundary definition, and minimal pass/fail tests.

The machine-level Python/SymPy installation remains external to the repository and must be revalidated when VPC is used for a consequential claim.

## Applicability

Use VPC only when the decisive subclaim can be encoded as a finite typed DAG whose sources are local, declared, and SHA-256 bound, and whose operations are a claim-specific subset of [`profiles/TRUSTED_EXACT_OPERATIONS.json`](profiles/TRUSTED_EXACT_OPERATIONS.json). Each calculation must define its own narrower `PhysicsProfileV1`, adversarial control, and authority ceiling.

If those conditions do not hold, record VPC as not applicable and use the competent domain tool. Do not expand VPC merely to make it apply.

## Run the minimal tests

From the repository root:

```powershell
& 'C:\Program Files\Python310\python.exe' -m unittest discover -s tools/vpc/tests -p 'test_*.py' -v
```

For a claim-scoped profile and candidate:

```powershell
$env:PYTHONPATH = (Resolve-Path 'tools/vpc/source')
python -m vpc PROFILE.json CANDIDATE.json --source-root SOURCE_DIRECTORY
```

The emitted receipt establishes only exact DAG recomputation within the declared profile. Physical assumptions, source authority, model adequacy, and scientific promotion require separate evidence.

See [`PROVENANCE.json`](PROVENANCE.json) for exact local-custody identities and the bounded historical calibration receipt.
