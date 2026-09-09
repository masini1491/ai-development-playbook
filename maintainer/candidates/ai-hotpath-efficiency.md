# AI Hot-Path Efficiency｜Cross-project maintainer candidate

> **Maintainer-only candidate.** This file records pre-canonical cross-project evidence. It is not a Playbook capability claim, policy owner, admitted task, eval result, implementation authority, or execution authorization.
>
> **Current obligation: `NONE`.** Presence here does not create Hot/Cold work. Any canonical change, formal eval, tooling, or adoption requirement must pass normal governance separately.

## Candidate question

Several independently maintained AI-facing repositories converged under real latency / context pressure on a similar pattern:

`route narrowly → reuse verified session state → invalidate selectively on material freshness triggers → execute with minimum transport overhead → stop at minimum-sufficient evidence → guard the hot path against regression`

Maintainer question:

> Should the Playbook eventually make **session-local verified-context reuse, hot-path regression protection, and deterministic runtime transport efficiency** more explicit as a reusable cross-project pattern, or are the existing canonical rules already sufficient when applied correctly?

This is a refinement / operationalization question, **not evidence that a fundamental Playbook capability is missing**.

## Public source evidence

### `masini1491/ai-divination-playbook`

Reviewed revision:

- commit: `dc6402933a1caac485f63bf7eeab596b2b78b118`
- public source: <https://github.com/masini1491/ai-divination-playbook/commit/dc6402933a1caac485f63bf7eeab596b2b78b118>

Recent hot-path work includes:

- ordinary-reading and method-selection fast paths that stop routing after a high-confidence owner / method decision instead of loading every possible contract owner;
- verified runtime-asset reuse without repeated source acquisition or full smoke validation when no material refresh trigger exists;
- reuse of an already imported canonical runtime module within the same interpreter when identity remains sufficient;
- batching compatible independent readings into fewer runtime calls while preserving child identity and fresh stochastic results;
- minimum-sufficient AI transport via compact machine payloads instead of always returning audit-grade full runtime metadata;
- behavioral regression evidence that observes invocation count, argument / result mapping, and identity preservation rather than treating "batching exists" as sufficient proof.

The important abstraction is broader than divination:

> **Fresh task input may require fresh execution without requiring fresh program acquisition, process startup, full provenance transport, or repeated routing.**

### `masini1491/building-envelope-engineering-kb`

Reviewed revision:

- commit: `4868440b381b170cc048e6b3c5b570e3e6df5a46`
- public source: <https://github.com/masini1491/building-envelope-engineering-kb/commit/4868440b381b170cc048e6b3c5b570e3e6df5a46>

Recent hot-path work includes:

- same-session reuse of already confirmed current HEAD / manifest / router / canonical leaf when no material freshness or scope trigger exists;
- `Sufficient then STOP` as an explicit retrieval termination rule;
- a hot-path growth ratchet: new AI-facing mutations should not worsen the minimum-sufficient working set without a concrete retrieval / correctness benefit;
- deterministic `check_ai_fastpath.py` coverage for routing-only boundaries, target integrity, ambiguity, and growth review signals;
- size thresholds treated as architecture-review `WARN` signals rather than universal correctness limits;
- CI integration so routing regressions can become observable rather than relying only on maintainer memory.

The useful abstraction is:

> **AI readability can have regression protection without reducing architecture quality to file-size minimization.**

## Sanitized private-adopter evidence

A private internal adopter was also reviewed during this maintainer session. Its repository identity, revision, domain data, entities, records, and private content are intentionally **not persisted in this public repository**.

Only architecture-level observations are retained here:

- machine routing metadata remained explicitly `routing-only`;
- exact targets could bypass generic routers;
- high-frequency access patterns received thin specialized routing hubs before generic domain fallback;
- already verified session route / leaf state could be reused until a material freshness trigger occurred;
- current-state changes favored bounded diff / selective owner reload rather than full-context reload;
- a deterministic fast-path checker validated routing targets and surfaced always-on / narrow-router growth as review signals;
- new writes followed a retrieval-cost ratchet so persistence did not automatically increase future default-load cost.

This evidence is deliberately sanitized. It may support the architectural pattern but **must not be used to infer or expose private source content**.

## Reconciliation with current canonical Playbook

Current canonical owners already covered much of the underlying model before this candidate was partially promoted:

- `AI_CONTEXT.md`
  - Expected Retrieval Cost;
  - Progressive Routing / Direct-leaf Bypass;
  - Thin Routing Metadata;
  - Context Cohesion Gate;
  - fail-fast context ordering;
  - AI Readability / Retrieval Cost Change Gate;
- `CHATGPT_WORKFLOW.md`
  - Execution Opportunity Scan;
  - Runtime Asset Reuse Fast Path;
  - asset reuse vs fresh-result distinction;
- `CODEX_EXECUTION.md`
  - Progressive Context;
  - tool / skill surface trimming;
  - Independent Tool Scheduling Discipline;
  - long-running output discipline.

Therefore the evidence never established that the Playbook lacked routing, reuse, batching, or retrieval-cost governance. The useful result was a narrower operational refinement.

## Promotion reconciliation

### Promoted to `AI_CONTEXT.md`

The following two cross-project refinements are now canonical in the existing AI Context owner:

1. **Session-local verified context reuse / selective invalidation**
   - verified route / owner / leaf state may be reused within a session until a material freshness / scope trigger occurs;
   - unchanged identity does not require ceremonial reread;
   - changed identity should use bounded change detection and selectively invalidate / reload affected Context when coverage is sufficient;
   - reuse never promotes conversation memory over canonical authority.

2. **Hot-path growth ratchet / optional deterministic regression guard**
   - new AI-facing mutations should not worsen the common minimum-sufficient working set without a concrete retrieval / correctness / scope-isolation benefit;
   - repositories with demonstrated retrieval pain may encode machine-checkable routing invariants in lightweight deterministic guards;
   - broken routing / schema invariants may `FAIL`, while size / growth / hop heuristics normally remain `WARN` / architecture-review signals;
   - no universal byte, line, entry-count, hop-depth, or token threshold is introduced.

This promotion reused the existing canonical owner; it did not create a new canonical surface, mandatory validator, TASKS item, formal eval, or execution authority.

### Still candidate / more evidence needed

The remaining incremental topic is **deterministic runtime transport efficiency**, especially:

- persistent interpreter / imported-module reuse beyond ordinary runtime-asset reuse;
- minimum-sufficient machine-result projection for model consumption while retaining audit-grade data when required;
- broader evidence that compatible execution batching preserves semantic identity across multiple non-divination workloads.

Existing canonical rules already cover runtime-asset reuse and general independent batching. The remaining question is whether process/module lifecycle reuse and compact result transport deserve stronger cross-project semantics.

## Why the remainder may matter

The evidence streams came from different workloads:

- repeated stochastic runtime execution;
- engineering knowledge retrieval;
- private structured context retrieval.

That convergence suggests the performance problem is not domain-specific. A repository can satisfy ordinary "progressive reading" guidance yet still become slow through repeated process startup, oversized machine transport, or execution-surface ceremony even after retrieval reuse is solved.

The remaining candidate principle is therefore narrower than the original:

> **After retrieval hot paths are already efficient, determine whether runtime process/module lifecycle and result transport also need a reusable minimum-sufficient contract.**

## Risks / competing explanations for the remainder

Do not promote the remaining runtime pattern without accounting for:

- batching that accidentally merges semantic identities, state, RNG outcomes, validation boundaries, or failure handling;
- compact transport that removes provenance / diagnostics actually required for the current decision;
- assuming persistent interpreter / module state on execution surfaces that do not guarantee it;
- mistaking a domain-specific micro-optimization for a cross-project contract;
- exposing private adopter provenance or content in a public maintainer artifact.

## Evidence that would change the remaining decision

Evidence favoring further canonical promotion could include:

- a second non-divination deterministic workload showing material process/module reuse benefit while preserving canonical identity and fresh-result semantics;
- repeated evidence that compact machine-result projection materially reduces model/tool overhead without hiding required diagnostics or provenance;
- behavioral evidence that agents correctly fall back when interpreter/module persistence is unavailable;
- nearby-task transfer showing the runtime transport rule is recoverable without domain-specific scaffolding.

Evidence favoring `NO CHANGE` could include:

- existing `CHATGPT_WORKFLOW.md` runtime-asset reuse plus `CODEX_EXECUTION.md` independent scheduling rules already causing agents to derive the needed optimizations reliably;
- execution surfaces varying too much for process/module reuse to support a stable cross-project contract;
- compact transport creating more provenance/debugging ambiguity than the saved Context is worth.

## Candidate evaluation path

If the remaining runtime candidate is later admitted for evidence gathering, prefer a bounded comparison rather than immediate policy mutation:

1. choose one real non-divination deterministic workload with repeated execution;
2. establish baseline execution / transport overhead;
3. apply the smallest process/module reuse or compact-result behavior;
4. verify correctness / identity / freshness / diagnostics boundaries;
5. reduce scaffolding and repeat in a nearby task;
6. decide `NO CHANGE`, `RECOMMENDATION ONLY`, `MORE EVIDENCE NEEDED`, or propose a specific existing canonical owner update.

Do not manufacture a new framework or checker solely to prove this candidate.

## Current conclusion

**Status: `PARTIALLY PROMOTED / RUNTIME REMAINDER MORE EVIDENCE NEEDED`.**

Session-local verified Context reuse and conditional hot-path regression guidance have been promoted into the existing canonical AI Context owner. Runtime process/module reuse and compact machine-result transport remain maintainer-only evidence candidates.

Current obligation remains `NONE`.
