# ToE-Next Charter

## Objective

Construct the most coherent and complete unification obtainable from established physics, existing serious unification frameworks, surviving project results, and promote new physics only where evidence or mathematical consistency requires it.

The central question is:

> How much accepted physics can be recovered from progressively fewer independent assumptions?

Originality is not an acceptance criterion. Provenance, physical adequacy, mathematical consistency, and explanatory compression are.

## Scientific scaffold

Research is organized as a dependency structure:

```text
empirical obligations
→ established theories
→ candidate unifications
→ recovery maps and seams
→ operational observables
→ verification
→ assumption compression
```

The layers mean:

1. **Empirical obligations** — observations and tested regularities that a viable construction must reproduce.
2. **Established theories** — the accepted descriptions that work in specified domains, including their known limits.
3. **Candidate unifications** — serious broader frameworks assessed without presuming adoption.
4. **Recovery maps and seams** — explicit derivations or compatibility relations connecting broader and lower-level descriptions.
5. **Operational observables** — the route from formal structure to quantities that can be measured or constrained.
6. **Verification** — checks scaled to the strength, consequence, and failure modes of a claim.
7. **Assumption compression** — determining whether several independent assumptions can be replaced by fewer justified principles.

This scaffold begins as an intellectual and dependency structure. It does not justify pre-creating software or document hierarchies. A new directory, abstraction, dependency, or data surface must be earned by active scientific work.

## Scientific commitments

- Established physics is preferred to reinvention when it already supplies the needed result.
- Established physics is cited and used under its conventional identity.
- A successful effective theory in its tested domain need not be a final fundamental theory.
- Scientifically motivated new-physics hypotheses may be generated, explored, and falsified when useful. They become accepted components only after evidence, consistency, recovery, and comparator tests justify promotion.
- No mechanism is promoted merely because it is mathematically attractive or computationally tractable.
- A failed, blocked, or underdetermined calculation is a scientific result when its scope and assumptions are explicit.
- Open questions are not automatically active research seams.

## AI and computational science operating model

ToE-Next is AI-assisted and computationally capable. AI may act in distinct roles:

- **Proposer:** generate hypotheses, mathematical structures, and discriminating questions.
- **Implementer:** translate a frozen claim into symbolic, numerical, logical, or formal work.
- **Comparator:** determine whether a result is already known and identify its provenance and nearest established analogues.
- **Adversary:** search for hidden assumptions, counterexamples, sign or convention errors, failed limits, and alternative explanations.
- **Integrator:** interpret what a result changes in the larger scaffold.

These roles may inform one another, but an AI-generated statement is not scientific authority merely because it is fluent, reproducible by the same model, or supported by many generated artifacts.

The normal workflow is:

```text
scientific question
→ minimal claim
→ frozen assumptions
→ smallest competent toolset
→ independent attack when warranted
→ physical interpretation
→ bounded authority
```

Tools are selected by the claim. Running more engines does not automatically increase confidence, and the complete available stack is never run merely for procedural completeness.

## Calculation record

Every calculation begins with one compact record containing these twelve fields:

1. **Scientific question** — the decision the work is intended to inform.
2. **Claim under test** — the smallest exact statement being evaluated.
3. **Scope and authority ceiling** — what the result can and cannot establish.
4. **Frozen inputs and assumptions** — physical, mathematical, numerical, and conventional choices.
5. **Provenance and comparators** — relevant established results and prior project evidence.
6. **Primary method and tool** — the chosen method, engine, and reason for the choice.
7. **Independent replay decision and reason** — whether a genuinely independent check is needed and why.
8. **Adversarial checks and falsifiers** — tests that could expose an error or defeat the claim.
9. **Known-limit and physical-assumption checks** — required recovery behavior and assumption audit.
10. **Stopping rule** — the outcome or boundary that ends the calculation.
11. **Failure interpretation** — what a negative, blocked, unstable, or inconclusive outcome means.
12. **Result and reproducibility record** — disposition, evidence, calculation-local versions, outputs, and carry-forward consequence.

This record is the unit of computational work. Separate planning packets, mirrored status files, and schemas are not created unless a concrete need later justifies them.

Numerical work must address convergence, discretization or truncation error, conditioning, precision sensitivity, and uncertainty propagation when applicable. A precise-looking numerical value without the controls relevant to its method does not earn additional authority.

## Risk-scaled verification

Verification effort follows claim risk:

- **Exploratory work:** one competent engine plus dimensional, sign, scale, and limiting sanity checks.
- **Consequential mathematical result:** a primary derivation, a genuinely independent replay when practical, and an adversarial attack.
- **Major scientific claim:** independent computational reproduction, known-limit recovery, literature comparison, a physical-assumptions audit, and formalization only where a small decisive statement benefits from it.

Independent replay means independence in method, implementation, representation, or engine sufficient to expose the relevant failure modes. Repeating the same derivation through a cosmetic wrapper does not qualify.

## Provenance and authority

Claims must distinguish observation, established theory, inherited result, current project result, hypothesis, and speculation. Authority is claim-specific and bounded by assumptions, evidence, and reproducibility. Detailed rules are in [`docs/PROVENANCE_AND_AUTHORITY.md`](docs/PROVENANCE_AND_AUTHORITY.md).

Historical material is not current authority merely because it exists. Legacy evidence is consulted deliberately through the immutable references in [`docs/LEGACY_HANDOFF.md`](docs/LEGACY_HANDOFF.md).

## Repository operation

All ordinary work occurs on `main`. No branch, worktree, or alternate development ref may be created unless the owner explicitly authorizes it for the task. Any authorized temporary branch or worktree must be reconciled or rejected and removed before task completion. Force pushes, history rewrites, and destructive ref updates are prohibited. Remote `main` receives only reviewed, validated, fast-forward checkpoints. At normal task completion, local and remote `main` should agree.

Scientific questions and calculations drive architecture. The repository does not accumulate empty structures, speculative abstractions, duplicated external frameworks, or universal environments in anticipation of possible work.

## Storage and external payloads

Git stores the science needed to understand and reproduce claims, not every byte produced while obtaining them.

Store in Git:

- source and compact derivations;
- concise calculation records;
- small exact or machine-readable evidence;
- scientifically useful small figures;
- hashes and manifests for external payloads;
- reproduction instructions.

Keep outside Git by default:

- environments, package depots, caches, and compiled artifacts;
- downloaded frameworks and external databases;
- large datasets, sweeps, grids, simulations, frames, and symbolic intermediates;
- raw outputs that can be regenerated from preserved inputs and instructions.

Storage thresholds are:

- initial foundation below 1 MiB;
- preferred active Git repository below 250 MiB;
- architecture and storage review before exceeding 1 GiB;
- individual files above 10 MiB external by default;
- generated tranches above 100 MiB external by default;
- expected additions above 500 MiB require explicit owner approval before execution.

Large authoritative payloads may use a separately designated active-data location, including D:, when a calculation requires it. Each payload must be separated from historical custody, provenance-bound, hash-identified, manifest-described, and accompanied by reproduction and retrieval information. A missing declared payload must fail explicitly or be reported unavailable; silent fallback is prohibited.

The active project must never depend on the legacy custody tree through a junction, symlink, worktree, import, required execution path, or hidden runtime lookup. Historical custody is evidence storage, not an active dependency surface.

Repository size is not a measure of scientific capability or completeness. Scientific authority depends on the quality and custody of evidence.
