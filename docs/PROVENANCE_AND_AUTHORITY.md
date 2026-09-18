# Provenance and Authority

## State authority

[`project_state.json`](../project_state.json) is the sole machine-readable authority for current project state. Human-readable documents explain scientific posture and evidence but must not create independent status mirrors.

## Claim identity

Every consequential claim must identify:

- the exact statement and scope;
- whether it is observation, established theory, inherited result, current result, hypothesis, or speculation;
- its assumptions, conventions, domain, and authority ceiling;
- its source or derivation;
- the evidence that supports it and the evidence that could defeat it.

AI output, code execution, formal syntax, numerical precision, or agreement among closely related implementations is evidence only within the failure modes it actually tests. None confers scientific authority by itself.

## Source priority

Prefer primary and authoritative sources: original peer-reviewed literature, maintained collaboration references, standards, canonical datasets, and official framework documentation. Reviews and secondary sources may orient the work but should not replace primary provenance for decisive claims.

Established results are cited under their established names. A project-specific representation or implementation does not create ownership of the underlying physics.

## Project results

A current result earns authority only for its recorded claim, inputs, domain, and checks. It must distinguish:

- derivation from assumption;
- exact result from numerical approximation;
- internal verification from independent reproduction;
- local or effective validity from fundamental interpretation;
- absence of evidence from evidence of absence.

Negative, blocked, or inconclusive results retain value when their tested scope and failure boundary are explicit.

## Legacy evidence

The complete local legacy authority and the public historical GitHub repository are different custody domains. A commit present in local custody must not be described as public unless remote reachability is independently verified.

Legacy material is historical evidence, not active authority merely because it exists. It may be consulted to avoid repeating work, recover a precise bounded result, or understand a prior failure boundary. Carry-forward requires a claim-specific receipt satisfying the tests in [`LEGACY_HANDOFF.md`](LEGACY_HANDOFF.md).

Full 40-character commit SHAs are primary identifiers. Tags may be recorded only as optional aliases. Historical content is not copied into ToE-Next merely for convenience.

## Reproducibility

Dependencies and versions are calculation-local. A calculation records only the engines, packages, data, parameters, conventions, and commands it actually requires. ToE-Next does not maintain a universal environment containing every available tool.

Small authoritative evidence may be committed. Large or externally governed payloads remain outside Git with:

- a stable identity and location class;
- a cryptographic hash;
- origin, license, and acquisition provenance where applicable;
- parameters and generation instructions;
- required software and versions;
- explicit behavior when the payload is unavailable.

No calculation may silently obtain inputs from the legacy custody tree. Historical custody can be read deliberately for provenance; it cannot become a live dependency.

## Attribution and correction

Attribution must survive reuse, translation, implementation, and synthesis. If later evidence narrows or overturns a claim, the current project state and affected calculation record are updated without rewriting historical evidence. Corrections state what changed, why, and which downstream claims are affected.
