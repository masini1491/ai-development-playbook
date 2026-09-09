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

Current canonical owners already cover much of the underlying model:

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

Therefore the evidence does **not** currently establish that the Playbook lacks routing, reuse, batching, or retrieval-cost governance.

The possible incremental value is narrower:

1. **Session-local verified context reuse**
   - make explicit that verified route / owner / leaf state can remain active within a session until a material freshness / scope trigger invalidates it;
   - when current HEAD changes, prefer bounded change detection and selective invalidation / reload over unconditional global rehydration when correctness permits.

2. **Hot-path regression ratchet / guard pattern**
   - optionally allow repositories with demonstrated retrieval pain to encode routing-only invariants and growth review signals in deterministic checks;
   - preserve the distinction between correctness `FAIL` and architecture-review `WARN`;
   - avoid cargo-cult universal byte / line thresholds.

3. **Deterministic runtime transport efficiency**
   - distinguish runtime-asset identity reuse from process / interpreter / module reuse;
   - when safe and supported, batch compatible independent executions while preserving individual semantic identity;
   - prefer minimum-sufficient machine-result projection for the model, while retaining audit-grade detail only when required.

These are candidate refinements, not yet canonical requirements.

## Why this may matter

The three evidence streams converged from different workloads:

- repeated stochastic runtime execution;
- engineering knowledge retrieval;
- private structured context retrieval.

That convergence suggests the performance problem is not domain-specific. A repository can satisfy ordinary "progressive reading" guidance yet still become slow through repeated freshness ceremony, repeated routing, repeated process startup, oversized machine transport, or unguarded growth of always-on routing surfaces.

The stronger candidate principle is therefore:

> **Optimize end-to-end minimum-sufficient working-set cost, including repeated session retrieval and execution transport—not merely initial file loading.**

## Risks / competing explanations

Do not promote this pattern without accounting for:

- stale-context risk if session reuse outlives a material authority change;
- incorrect selective invalidation if a changed owner has hidden cross-owner effects;
- premature `STOP` when evidence coverage is insufficient for a negative / repository-wide claim;
- over-fragmentation caused by adding specialized routers for every low-frequency intent;
- cargo-cult size limits that optimize bytes rather than authority clarity / retrieval quality;
- batching that accidentally merges semantic identities, state, RNG outcomes, validation boundaries, or failure handling;
- compact transport that removes provenance / diagnostics actually required for the current decision;
- assuming persistent interpreter / module state on execution surfaces that do not guarantee it;
- exposing private adopter provenance or content in a public maintainer artifact.

## Evidence that would change the decision

Evidence favoring canonical promotion could include:

- repeated real projects showing measurable latency / tool-round-trip / loaded-context reduction without correctness regressions;
- behavioral evidence that agents reliably reuse verified session context but revalidate on material triggers;
- a bounded experiment showing selective invalidation avoids unnecessary rereads without stale-authority errors;
- repeated retrieval regressions caught by a lightweight deterministic hot-path checker before they reached normal users;
- runtime evidence that process / module reuse, batching, or compact result projection materially reduces overhead while preserving semantic and validation boundaries.

Evidence favoring `NO CHANGE` could include:

- current `AI_CONTEXT.md`, `CHATGPT_WORKFLOW.md`, and `CODEX_EXECUTION.md` already causing fresh agents to derive these behaviors reliably;
- added canonical text increasing always-on / routing cost more than it improves behavior;
- deterministic hot-path checks producing mostly noisy architecture warnings or project-specific thresholds;
- selective reuse / invalidation causing stale-state regressions that outweigh the saved retrieval cost.

## Candidate evaluation path

If this candidate is later admitted for evidence gathering, prefer a bounded comparison rather than immediate policy mutation:

1. choose one real adopter task with repeated same-session retrieval or runtime execution;
2. establish baseline behavior / overhead;
3. apply the smallest candidate fast-path behavior;
4. verify correctness / identity / freshness boundaries;
5. reduce scaffolding and repeat in a nearby task;
6. decide `NO CHANGE`, `RECOMMENDATION ONLY`, `MORE EVIDENCE NEEDED`, or propose a specific existing canonical owner update.

Do not manufacture a new framework or checker solely to prove this candidate.

## Current conclusion

**Status: `CANDIDATE / MORE EVIDENCE NEEDED`.**

The cross-project convergence is strong enough to preserve as maintainer evidence. It is not yet strong enough to justify a new canonical surface, mandatory validator, universal routing metric, or task admission.

Current obligation remains `NONE`.
