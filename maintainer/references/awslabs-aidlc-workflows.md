# awslabs/aidlc-workflows

- Source: `awslabs/aidlc-workflows`
- Reviewed revision: `227745d03bdd1879f51409eeba051e4c6c585b5f`
- Source tree: `346dc838c445cf0dd8d6d55bc6d95611ef781b8a`
- License: MIT No Attribution (MIT-0)
- Source role: external full-lifecycle AI software-delivery / harness-engineering reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps materially with existing Playbook concerns around Task/Stage boundaries, explicit user authority, staged execution, progressive context loading, session recovery, validation gates, subagent/delegation boundaries, capability-vs-authority separation, and thin multi-runtime activation.

The important difference is maturity and packaging: AI-DLC implements these concerns as a productized deterministic lifecycle engine, whereas this Playbook primarily defines cross-project governance contracts and lets adopter repositories own their actual task/state artifacts.

## 2. Same failure mode, different architecture

### Workflow and stage lifecycle

AI-DLC uses nested workflow / phase / stage state machines. Stage state is explicit (`Pending`, `Active`, `AwaitingApproval`, `Revising`, `Completed`, `Skipped`), and transitions are owned by deterministic tools rather than LLM prose. This Playbook instead defines Task/Stage authorization, Hot/Cold coordination, actor revalidation, and completion-evidence rules without requiring a universal lifecycle state machine in every adopter.

### Human approval

AI-DLC places an explicit approval gate after almost every non-initialization stage and records exact gate choices in state/audit machinery. This Playbook requires user/project authorization where authority changes or execution/mutation requires it, but intentionally does not force a universal approval ceremony after every engineering stage.

### State and history

AI-DLC separates current state (`aidlc-state.md`) from an append-only per-clone audit trail and makes state transitions/audit emissions tool-owned. This Playbook separates current canonical / Hot / Cold / Evidence / Historical surfaces semantically and requires canonical read-back, but does not prescribe a universal per-project append-only event taxonomy.

### Context and recovery

AI-DLC persists workflow state/artifacts to disk and reconstructs sessions from that state, with a recovery breadcrumb around compaction. This Playbook has a conversation-level Session Compaction / Rehydration contract and canonical-pointer-first recovery, but does not currently implement an equivalent runtime-owned session/state recovery engine across supported assistants.

### Multi-runtime architecture

AI-DLC has a harness-neutral `core/` plus thin `harness/<name>/` projections and a package determinism guard. This Playbook has thin activation-adapter semantics and machine-readable routing, but currently stops short of generated native harness packages/installers/hooks for each runtime.

## 3. External capabilities / implementation maturity worth further evidence

These are not whole-Playbook absence claims; they are external implementation patterns not evidenced at equivalent maturity in the checked current Playbook surfaces.

### A. Deterministic lifecycle state machine + atomic audit emitters

AI-DLC assigns each state transition exactly one tool-owned emitter and couples transition/audit behavior so workflow history can be reconstructed from deterministic evidence. A drift test checks documentation against emitter behavior.

The Playbook has strong authority, completion, validation, and status-scope contracts, but the checked discovery/owner surfaces do not show a generic executable project-lifecycle state machine or universal append-only transition ledger.

### B. Human-affirmed durable learning promotion

AI-DLC keeps per-stage `memory.md` observations, surfaces candidates at approval gates, defaults promoted learnings to narrow project scope, allows explicit widening to team scope, checks proposed rules against org guidance, and applies the new rule only from the next workflow compile. Practices Discovery separately uses `scan → draft → affirm → publish` before writing standing team/project memory.

This is especially relevant to the Playbook's new maintainer zone: both systems distinguish observation from durable policy, but AI-DLC has an executable promotion pipeline with scope selection and audit receipts.

### C. Framework/team × continuous/per-workflow information-placement matrix

AI-DLC explicitly classifies information along two axes: who authors it (framework vs team) and when it is consumed (continuously vs per-workflow). It also treats one quadrant as intentionally empty. This is a concrete placement heuristic that complements this Playbook's Always-on / Hot / Cold / Evidence / Current canonical / Historical model.

### D. Workflow profiles as explicit ceremony budgets

AI-DLC maps work types such as Feature, Bugfix, Refactor, Security Patch, Enterprise, and Express to explicit stage routes, depth, test strategy, and review ceiling. This Playbook calibrates actor/model/context/validation and task scope, but does not prescribe a fixed cross-project profile matrix.

### E. Harness packaging parity and productized runtime hooks

AI-DLC projects one harness-neutral core into multiple runtime integrations and checks package determinism/parity. This is a stronger distribution implementation layer than the Playbook's current manual thin adapters.

## 4. Useful expression / UX patterns

- A visible stage state that distinguishes `AwaitingApproval` from `Revising` is operationally clearer than a generic "in progress" status.
- Separating current state from append-only audit history makes resume/debug/reconstruction easier to reason about.
- The two-axis configuration placement model gives maintainers a fast answer to "where should this information live?".
- Workflow profiles communicate ceremony/cost explicitly instead of hiding it in a generic lifecycle.
- `scan → draft → affirm → publish` is a concise promotion pattern for persistent team truth.
- "Applies next workflow, not mid-run" gives durable learning a clean stability boundary.

## 5. Runtime/product-specific patterns not suitable for direct generalization

- A mandatory approval gate after nearly every stage would add excessive ceremony to many adopter projects and should not become a universal Playbook rule without evidence.
- The fixed 5-phase / 33-stage lifecycle and named workflow profiles are AI-DLC product design choices, not universal project semantics.
- Claude/Kiro/Codex/Cursor/opencode/Copilot hook schemas, native picker behavior, worktree/Bolt/swarm machinery, and specific package layout are runtime implementation details.
- A 91-event audit taxonomy is useful evidence of product maturity but should not be copied wholesale into a general governance Playbook.
- AI-DLC's learning conflict check includes an LLM judgment step; it is an audit/coherence aid, not a deterministic policy-enforcement boundary.
- Project/team memory automatically loaded into future workflows has non-trivial context and stale-rule costs; this Playbook should preserve its own retrieval-cost and authority gates before adopting an analogous mechanism.

## 6. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Maintainer-zone promotion experiment** — compare the current manual `observation → maintainer evidence → conclusion → canonical promotion` flow against an AI-DLC-style `surface → explicit keep/reject → scope → conflict check → persist` flow. Measure accidental promotion, user friction, provenance quality, and stale-rule risk.
2. **State/audit split pilot** — on one complex adopter workflow, compare current Hot/current-state reconstruction against a minimal current-state + append-only event ledger. Measure resume reliability, reconciliation cost, and search noise before considering generic tooling.
3. **Stage status semantic fixture** — test whether explicitly distinguishing `AwaitingApproval` and `Revising` improves agent continuation behavior versus generic pending/in-progress labels.
4. **Harness packaging comparison** — compare pointer-based Playbook activation with generated harness projections on bootstrap reliability, drift, update cost, immutable-version clarity, and context footprint.
5. **Ceremony-budget comparison** — map a small bugfix, medium feature, and high-assurance change through Playbook's existing gates versus AI-DLC profile routes; identify whether explicit profile presets reduce decision cost without over-prescribing project workflow.
6. **Durable learning compile-boundary test** — compare immediate mid-session rule mutation against "next workflow/session only" activation for reproducibility and surprising behavior.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

AI-DLC does not currently demonstrate that this Playbook needs a new universal lifecycle engine. Its strongest transferable ideas are narrower:

- human-affirmed promotion before tentative observations become standing rules;
- an explicit current-state / append-only-history separation when workflow complexity justifies it;
- deterministic ownership of state transitions and audit emitters when a project chooses an executable lifecycle;
- a stable boundary where newly learned rules apply only to the next workflow/session;
- generated harness parity as a future distribution-maturity benchmark.

The highest-value immediate research candidate is the **maintainer-zone promotion experiment**, because it directly tests the self-correction area just introduced in this Playbook without requiring a new global runtime or task engine.

Do not mutate canonical policy, create a universal state machine, install AI-DLC, or admit implementation work solely from this reference.

## Revisit trigger

Revisit if:

- maintainer observations/candidates begin being promoted inconsistently or without enough explicit evidence;
- adopter projects repeatedly lose current workflow state across sessions despite the existing compaction/rehydration contract;
- native adapter/distribution friction becomes material across multiple runtimes;
- repeated projects independently reinvent state/audit machinery;
- behavioral evidence shows an explicit approval/revision status materially improves agent continuation correctness.
