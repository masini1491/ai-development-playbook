# gastownhall/beads

- Source: `gastownhall/beads`
- Reviewed revision: `a690b0a8c4d1ddc4f0bd9bf767499625dd71bc96`
- Source tree: `8ac01dff6ea07e56d6bbbeee094681d08ed04d17`
- License: MIT
- Source role: external durable agent-memory / dependency-aware task-graph / multi-agent coordination reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps materially with existing Playbook concerns around durable project memory, semantic task identity, dependency-aware execution, agent ownership, handoff, cross-repository coordination, session recovery, context-budget management, capability-vs-authority separation, and preserving provenance when work is discovered during another task.

The architectural difference is substantial: Beads productizes these concerns as a versioned Dolt-backed graph database and CLI. This Playbook instead defines cross-project governance contracts and allows adopter repositories to choose their own Hot/Cold/evidence/task storage.

## 2. Same failure mode, different architecture

### Durable task state

Beads replaces Markdown task plans with structured issues, typed relationships, status/priority metadata, and a dependency graph. `bd ready` computes work with no open blockers, and `bd update --claim` atomically assigns one ready item to an agent.

This Playbook intentionally separates persistence from execution authority. A Hot/Cold/task record does not become executable merely because it exists or appears unblocked; Task/Stage authorization, actor choice, permission, and repository write scope remain independent gates. If a Beads-style ready queue were ever integrated, `ready` would need to remain a derived coordination view over already-admitted work rather than a new admission authority.

### Discovery provenance without blocking execution

Beads distinguishes blocking relationships from non-blocking graph annotations such as `discovered-from`, `caused-by`, `validates`, `related`, and `supersedes`. In particular, `discovered-from` records where a newly noticed item came from without affecting the ready queue.

This maps closely to the Playbook's `Observation ≠ Recommendation ≠ Admitted Work` boundary and maintainer-zone purpose. The useful pattern is not “turn every observation into an issue”; it is the explicit separation between provenance linkage and execution/dependency semantics.

### External conditions as gates

Beads models PR merge, CI success, timers, cross-project bead completion, and human approval as gate issues that can block dependent work. An unavailable or unconfigured external project remains blocking rather than being guessed as satisfied.

This resembles the Playbook's completion evidence, external-service staging, permission gates, and condition-sensitive work, but Beads unifies them into one graph primitive. The Playbook currently keeps these semantics in their domain owners rather than prescribing a universal executable gate object.

### Multi-agent ownership and conflict control

Beads provides atomic claims, assignee-based queues, fan-out/fan-in dependencies, and an exclusive merge-slot primitive for conflict-prone work. This supports autonomous worker pools with low race risk.

The Playbook is more conservative: child delegation requires an explicit delegation gate, parallelism requires independence/benefit, and repository mutation remains constrained by the current write target and project governance. A claim primitive could coordinate already-authorized workers, but must not become permission to self-create or self-admit work.

### Persistent agent memories

`bd remember` stores workspace memories that survive sessions/account rotations. `bd prime` injects them into future agent context; the runtime supports memory-only/no-memory modes and count/character caps so large memories do not automatically dominate the context budget.

The Playbook's durable-fact and context architecture is stricter about canonical ownership and default-load authority. A convenient memory plane can reduce repeated rediscovery, but unqualified memories can also become stale, duplicate canonical truth, or silently act as high-priority instructions. Any analogous mechanism would need owner/provenance/freshness semantics and selective loading rather than treating persistence as authority.

### Compaction

Beads advertises semantic “memory decay” for old closed tasks and supports restoration of pre-compaction issue content. This is repository/task-memory compaction, not the same thing as the Playbook's conversation-level Session Compaction / Rehydration contract.

The scopes should remain distinct: compacting historical task detail can reduce retrieval cost, but must not erase evidence or canonical facts that remain independently authoritative.

### Distributed storage and identity

Beads uses Dolt as the canonical database, hash-based issue IDs for merge-friendly distributed creation, and cell-level merge semantics for concurrent updates. JSONL is explicitly interchange/view material rather than the primary source of truth.

The Playbook already has semantic identity, canonical-evidence, and source-vs-derived guards, but does not prescribe a database or distributed task-state engine.

### Contributor vs maintainer planning separation

Beads can route contributor planning into a separate planning repository so experimental work stays out of project PRs, while maintainer workflows can use the project's own task store.

This is adjacent to the Playbook's maintainer zone but not equivalent. `maintainer/` is deliberately excluded from normal capability/task routing and has no execution authority; Beads contributor planning still represents actionable issue-tracker state in its own workflow.

## 3. External capabilities / implementation maturity worth further evidence

These are external implementation patterns, not whole-Playbook absence claims.

### A. Typed dependency / provenance graph

Beads gives blocking and non-blocking relationships first-class machine semantics. The combination of `blocks`, `discovered-from`, `caused-by`, `validates`, and `supersedes` is especially useful for preserving why an item exists without conflating that provenance with readiness or authority.

### B. Computed ready queue + atomic claim

For already-admitted work, a machine-computed unblocked queue plus atomic claim is a mature solution to multi-agent race conditions and ownership ambiguity.

### C. First-class external-condition gates

PR/CI/timer/human/cross-project conditions become queryable graph objects rather than prose embedded in task descriptions. This is a strong implementation example for projects with many asynchronous prerequisites.

### D. Persistent memory plane with context-budget controls

Beads has explicit remember/list/recall/forget operations, automatic session injection, and bounded injection controls. This is materially more productized than the Playbook's pointer-first durable-context model, while carrying different stale-authority risks.

### E. Concurrency primitives for worker pools

Atomic claims and merge slots give agent swarms a deterministic coordination layer that is stronger than prose-only assignment for high-concurrency repositories.

### F. Distributed task-state storage

Hash IDs, Dolt history, cell-level merges, server/embedded modes, backup/restore, schema guards, and remote synchronization form a complete task-state infrastructure rather than a documentation convention.

## 4. Useful expression / UX patterns

- `bd ready` provides one clear answer to “what is unblocked?” instead of making an agent reconstruct dependencies manually.
- `bd ready --claim` combines selection and atomic ownership, avoiding read-then-write races.
- `discovered-from` is a concise provenance relation that does not itself block or schedule work.
- Gate objects make “waiting for PR/CI/human/time” visible and queryable instead of hiding the condition in prose.
- `bd prime` separates agent-facing workflow/context delivery from underlying database storage.
- `bd remember / recall / forget` makes persistent memory lifecycle explicit and reversible.
- Contributor planning can be isolated from upstream project state instead of leaking experimental coordination artifacts into PRs.

## 5. Runtime/product-specific patterns not suitable for direct generalization

- Beads' `ready` status must not be treated as universal Playbook execution authority. In this Playbook, admission, execution permission, actor authority, and write scope remain separate.
- Automatically injected memories must not become canonical project truth or hidden governance merely because they persist across sessions.
- Dolt, `refs/dolt/data`, hash-ID formats, embedded/server modes, merge slots, and CLI command semantics are Beads implementation choices.
- A shared worker-pool claim model is unnecessary ceremony for projects that do not actually run concurrent self-selecting agents.
- Semantic compaction of closed tasks must not be applied to canonical evidence/facts without preserving restoration, provenance, and surviving owners.
- Contributor-mode planning isolation is not evidence that this Playbook's public `maintainer/` namespace provides access control; it remains a routing/governance boundary only.
- Beads' own agent profiles and Git authority semantics belong to Beads projects and must not be imported as Playbook repository-write authority.

## 6. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Non-blocking provenance-edge experiment** — compare current prose/pointer provenance for maintainer candidates against a machine-readable `discovered-from` relation that cannot promote, block, or authorize work. Measure retrieval clarity and accidental obligation inflation.
2. **Derived ready-queue pilot** — on one adopter with several already-admitted Hot tasks, compute readiness from explicit dependencies while keeping admission/authorization external to the queue. Measure task-selection errors and coordination cost.
3. **External gate-object pilot** — model one PR/CI/human prerequisite as a typed gate object and compare it with prose STOP conditions for freshness, observability, and false-unblock risk.
4. **Persistent-memory loading experiment** — compare small auto-injected project memories against canonical-owner pointers + on-demand retrieval. Measure repeated rediscovery, stale-fact errors, context footprint, and authority confusion.
5. **Atomic claim / merge-slot coordination pilot** — only in a project with genuinely concurrent agents, compare prose assignment against atomic task claim and exclusive conflict-zone ownership.
6. **Historical task-compaction experiment** — compact completed task detail while retaining stable identity, canonical outcomes, evidence pointers, and reversible history; measure retrieval savings versus archaeology/reconstruction cost.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

Beads does not currently demonstrate that this Playbook should replace its lightweight project-owned coordination model with a universal database-backed issue graph. The implementation cost and operational surface would be disproportionate for many adopters.

Its strongest transferable idea is narrower and directly relevant to the new maintainer zone: **provenance edges and execution edges should be different data types**. A candidate can record `discovered-from` / `caused-by` / `validates` relationships without gaining readiness, priority, or execution authority. That is a concrete machine-readable expression of the Playbook's existing observation/admission boundary.

The second-highest-value idea is an explicit **external-condition gate object** for projects whose Hot work repeatedly waits on PRs, CI, timers, hardware/user evidence, or human approval. This should be evaluated only where prose STOP conditions have become a real coordination problem.

Persistent auto-injected memories are worth testing, but the Playbook should remain more conservative unless evidence shows that automatic memory materially outperforms canonical-pointer/on-demand retrieval without introducing stale authority or context inflation.

Do not install Beads, add a universal task database, or convert maintainer candidates into task-like objects solely from this reference.

## Revisit trigger

Revisit if:

- maintainer candidates repeatedly lose discovery provenance or are accidentally treated as admitted obligations;
- an adopter accumulates enough admitted parallel work that agents repeatedly race, duplicate effort, or claim the same task;
- asynchronous PR/CI/human/hardware prerequisites repeatedly go stale in prose coordination;
- repeated sessions spend material context rediscovering stable project facts despite clean canonical ownership;
- Markdown Hot/Cold coordination becomes a measured retrieval/merge bottleneck rather than a theoretical scalability concern.