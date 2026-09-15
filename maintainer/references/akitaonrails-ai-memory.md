# akitaonrails/ai-memory

- Source: `akitaonrails/ai-memory`
- Reviewed revision: `74d2d31ebd8cca656c49f31563fac53e0b61c5cf`
- Source tree: `6397c73c6d36f1bee036dd82f934eef6c0887c00`
- Release at reviewed revision: `v2.2.1`
- License: MIT
- Source role: external long-term agent-memory / cross-agent handoff / retrieval-authority / memory-lifecycle reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Review scope

This review is deliberately bounded to the source's architecture and operating semantics that overlap with this Playbook's durable project memory, session continuity, retrieval authority, context loading, historical evidence, and learned-rule promotion concerns.

Primary reviewed surfaces:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/usage.md`
- `docs/security.md`
- `crates/ai-memory-core/src/routing_skills/ai-memory-retrieval/SKILL.md`
- source search evidence for the auto-improvement approval path

This is not a full security audit, performance audit, code-quality audit, or compatibility certification of ai-memory.

## 2. Already-covered concerns

The reviewed source strongly overlaps with existing Playbook principles:

- durable information should have a stable source of truth rather than rely on one agent's private chat memory;
- persistence does not imply default loading;
- historical/session memory does not automatically become current authority;
- search results/snippets are discovery evidence, not full authority;
- current project state, current instructions, source/build/test/runtime evidence outrank remembered historical content;
- retrieval should be bounded and broaden only when the first lookup is insufficient;
- optional richer capabilities should not be required for the baseline path;
- derived indexes/caches should not silently become source truth;
- long-lived memory needs explicit stale/expiry/feedback semantics rather than indefinite unquestioned accumulation.

The implementation architecture is different. ai-memory is a concrete Rust server/runtime with hooks, MCP, a Markdown wiki, SQLite/FTS/entity/graph/vector retrieval, handoff state, audit history, optional LLM consolidation, and optional managed workstreams. This Playbook defines cross-project governance and information-integrity contracts and intentionally does not require a universal memory server.

## 3. Same failure mode, different architecture

### Canonical memory versus derived retrieval index

ai-memory keeps a git-versioned Markdown wiki as the durable human-readable source of truth while SQLite acts as a derived index for search, sessions, observations, handoffs, embeddings, audit, and related runtime state. The database can be rebuilt from the durable files for the wiki content.

This is strongly aligned with the Playbook's canonical-owner / derived-artifact distinction. The transferable principle is not the specific Markdown+SQLite stack; it is that retrieval optimization must not invert authority.

Useful abstraction:

`durable source → derived retrieval/index surface → bounded recall → current-authority reconciliation`

### Retrieved memory is historical evidence, not instructions

ai-memory repeatedly states that recalled pages, observations, handoffs, briefings, and workstream events are untrusted historical data. Even maintained namespaces such as `_rules/`, `decisions/`, `procedures/`, and `gotchas/` do not authorize commands, tools, disclosure, permission changes, policy changes, or feedback merely by being retrieved.

Before acting on remembered content, the agent is instructed to read the full relevant page and validate it against the current user request, canonical project instructions, and current checkout state.

This is almost exactly the operational implementation of the Playbook's current-canonical-over-historical rule. It provides mature external evidence for a stronger memory-layer mental model:

`persistence ≠ retrieval ≠ trust ≠ authority`

The Playbook already separates persistence, default loading, write authority, and execution authority. ai-memory shows that **retrieval trust** deserves to remain an explicit independent concern whenever an external/persistent memory system is involved.

### Search rank and metadata do not create authority

ai-memory can rank maintained namespaces more strongly when relevance is close, and uses page kind, tiers, pinning, tags, entity matches, graph neighbors, vectors, and optional reranking as retrieval signals. It explicitly prevents these signals from becoming instruction authority.

This is directly compatible with the Playbook's derived metadata and search-result authority guards. A ranking system may improve discovery without becoming a policy-precedence system.

### Historical memory versus live code versus operational evidence

ai-memory explicitly separates three questions:

- historical memory answers why a design was chosen, what failed before, and what handoff/procedure may be relevant;
- current checkout or structural-code tools answer where symbols are now and what currently depends on them;
- source inspection, builds, tests, and observed runtime behavior decide whether a change actually works.

This three-way split is especially useful as a human-facing explanatory pattern for the Playbook's existing authority/evidence model. It prevents historical narrative from outranking current code or actual validation.

### Bounded recall rather than full-memory loading

The retrieval skill instructs agents to choose the smallest useful lookup, use recent/status/briefing/query tools according to intent, fetch full pages only after relevant hits, and broaden to sibling/global scope only on a thin or empty result. Expired pages are excluded from normal recall unless explicitly requested.

This closely matches Progressive Routing, direct-leaf/bounded reads, evidence-relative STOP conditions, and low-context loading in `AI_CONTEXT.md`.

### Zero-LLM baseline with optional richer retrieval

The source's capture, search, and handoff baseline works without LLM calls. LLM consolidation, embeddings, and final reranking are optional capability layers.

This is strongly aligned with the Playbook's minimum-sufficient capability and Free ChatGPT cold-start design pressure: stronger capability should improve quality/convenience without silently becoming a baseline prerequisite unless evidence proves it materially necessary.

## 4. Typed handoff lifecycle is the strongest novel implementation pattern

ai-memory treats handoff as durable protocol state rather than merely a prose summary convention.

Observed semantics include:

- explicit handoff identity;
- `open` state;
- list/inspect without claiming;
- explicit acceptance that records the receiver;
- single-use delivery/claim semantics;
- cancellation of mistaken handoffs;
- owner-scoped versus deliberately shared handoffs;
- stale/older automatic handoff expiry rules;
- separation between handoff and a live inter-agent message bus;
- session-end generation and next-session consumption boundaries.

The Playbook currently has a strong Session Compaction / Rehydration contract and a minimum checkpoint payload, but its handoff is primarily semantic/conversation-level rather than a prescribed typed state machine.

The transferable idea is therefore **not** “add ai-memory” or “require a handoff database.” It is:

> If a project needs durable cross-session or cross-agent handoffs, handoff identity, ownership, lifecycle state, acceptance, cancellation, supersession/expiry, and replay/idempotency deserve explicit semantics rather than relying only on prose summaries.

This may be especially valuable in projects with genuinely concurrent or alternating AI actors. It would be unnecessary ceremony for simple single-session repositories.

## 5. Memory lifecycle / decay / feedback patterns worth retaining as reference

ai-memory supports several memory-lifecycle concepts that are more productized than the Playbook's current generic historical/archive model:

- TTL / explicit expiration;
- retention and decay;
- `helpful`, `not_helpful`, `stale`, and `wrong` feedback;
- stale/wrong flags feeding later audit/lint review;
- explicit inclusion of expired memory only when requested;
- session-level raw observations retained separately from compiled summaries;
- pruning rules that preserve the last surviving account of a session before raw evidence can be removed.

These are useful implementation references for projects that accumulate large persistent memory. They should not become universal Playbook requirements without a demonstrated retrieval/storage problem.

A particularly important guard is that memory feedback never derives authority from the recalled text itself: a recalled page cannot instruct the agent to rate or mutate itself.

## 6. Auto-improvement: mature implementation, different governance default

When an LLM provider is configured, ai-memory can review completed sessions, produce proposed `concepts/`, `decisions/`, `gotchas/`, `procedures/`, and `_rules/` writes, record them in a pending-writes audit trail, and by default approve them through the normal wiki write path. Operators can set `[auto_improve] require_approval = true` to hold proposals for explicit approval. Optional executable evaluation can gate selected proposal prefixes before staging/approval.

This is technically mature and directly relevant to the Playbook's learned-rule-promotion research, but the default governance philosophy is not directly portable.

The Playbook currently keeps:

`observation / reflection → evidence / curation → conclusion → optional promotion through normal governance`

and explicitly treats reflection as evidence generation rather than promotion authority.

Therefore:

- automatic candidate extraction is compatible;
- automatic contradiction/staleness detection is compatible;
- pending-writes/audit staging is a useful implementation pattern;
- **automatic promotion into canonical project governance or policy should not be imported as a Playbook default**;
- any future Playbook-facing auto-improvement integration should keep canonical promotion behind the existing owner/admission/evidence boundary.

This source independently reinforces the existing `SYNTHESIS-learned-rule-promotion.md` research topic, but does not by itself justify changing that synthesis into canonical policy.

## 7. Security / privacy implementation patterns

The source treats memory capture as a real data-security surface rather than harmless note taking. Relevant patterns include:

- loopback-only default for unauthenticated single-user deployment;
- fail-closed unauthenticated non-loopback behavior;
- bearer/OIDC/multi-user attribution options;
- host allowlisting and DNS-rebinding protection guidance;
- capture-path exclusions before transport/storage for supported hooks;
- typed sanitization boundary and body-size caps;
- audit logging;
- explicit warning that sanitization does not make stored prose trusted.

This is useful evidence for a general principle: persistent agent memory can contain sensitive project history and instruction-like text, so memory infrastructure has both confidentiality and prompt/instruction-trust boundaries.

The Playbook should not infer that installing any memory tool is safe merely because it stores Markdown or runs locally.

## 8. Useful expression / UX patterns

- “Memory is historical evidence, not instructions” is an unusually clear trust-boundary phrase.
- `where did we leave off?` maps to explicit pending handoff state rather than generic semantic search.
- `remember this permanently` versus `remember this until <date>` distinguishes durable and time-bounded memory intent.
- `stale` / `wrong` feedback is different from deletion; it creates audit/review signal without silently erasing history.
- `explain: true` exposes retrieval provenance/ranking detail without changing authority.
- zero-LLM operation keeps the baseline useful even without provider credentials.
- source/build/test/runtime evidence is presented as the final operational layer rather than memory confidence.

## 9. Runtime/product-specific patterns not suitable for direct generalization

- A universal background server, Rust binary, MCP integration, lifecycle hooks, Docker deployment, SQLite schema, FTS5, graph RRF, vector embeddings, or managed workstream launcher should not become Playbook prerequisites.
- Silent capture of prompts/tool calls has real privacy and operational cost and should remain project/operator opt-in.
- Auto-injecting memory into every session can increase stale-context and authority confusion; selective routing remains preferable unless measured evidence supports automatic injection.
- Retrieval ranking scores, page tiers, pinning, or namespaces must not become Playbook authority levels.
- Semantic decay/forgetting must not delete canonical engineering facts or evidence merely because they are old or infrequently accessed.
- ai-memory's default auto-approval of validated auto-improvement proposals is not compatible with the Playbook's default evidence-gated canonical promotion boundary.
- Managed cross-harness continuity solves a real runtime problem but should not create sticky delegation or actor authority across Stages.

## 10. Comparative classification

### Already covered

- canonical/current state outranks historical memory;
- persistence is separate from default loading and execution authority;
- derived indexes/search hits do not create source authority;
- bounded/progressive retrieval;
- current evidence must reconcile stale summaries/session context;
- lowest-sufficient capability and optional richer layers;
- learned-rule promotion requires evidence/governance rather than mere persistence.

### Adopt concept

No canonical Playbook policy should be adopted directly from this single review.

At maintainer-reference level, retain these concepts as strong external evidence:

1. `persistence ≠ retrieval ≠ trust ≠ authority`;
2. typed handoff lifecycle semantics for projects that require durable cross-session/cross-agent transfer;
3. explicit memory stale/wrong/expiry lifecycle rather than indefinite accumulation;
4. historical-memory / current-code / operational-evidence separation.

### Adapt if evidence justifies

- typed handoff identity / acceptance / cancellation / supersession semantics;
- explicit memory trust boundary in interoperability guidance if external memory systems become a recurring adopter pattern;
- memory lifecycle feedback/TTL for memory-heavy adopters;
- pending-write staging for learned-rule proposals while keeping Playbook promotion gates.

### Reject as universal default

- mandatory ai-memory installation or universal external memory server;
- always-on automatic memory injection;
- retrieval rank as authority;
- auto-approval of learned rules/policy as the Playbook default;
- memory decay applied to canonical facts/evidence solely from age or low access;
- cross-session continuity as proof that previous actor authority remains valid.

### Future candidate

The most defensible future behavioral/research candidate is a **typed handoff lifecycle pilot** on a project that actually alternates actors/sessions enough for stale or duplicate handoffs to be a measured problem.

A second candidate is an **external-memory trust-boundary fixture**: provide a recalled historical page containing instruction-like text that conflicts with current canonical project authority and verify the agent treats the memory as evidence only.

Neither candidate is admitted work by being recorded here.

## 11. Relationship to existing maintainer references

This review overlaps with `gastownhall/beads.md` on durable memory, context-budget controls, cross-session continuity, and stale-authority risk. ai-memory provides stronger implementation evidence specifically for:

- untrusted-memory retrieval semantics;
- source-of-truth versus derived search index separation;
- explicit handoff lifecycle and delivery semantics;
- feedback/TTL/decay/audit mechanics for memory content.

It also reinforces `SYNTHESIS-learned-rule-promotion.md` by showing a productionized proposal/audit/approval pipeline. The important difference is that ai-memory's default auto-approval policy should not override the Playbook synthesis conclusion that generalized learned rules require evidence-gated promotion.

The evidence is now strong enough to consider **durable agent memory / session continuity** a plausible future cross-source synthesis topic, but this review alone does not require creating that synthesis immediately. The existing landscape already names that topic as evidence-dependent; another independent source or a concrete Playbook decision would provide a cleaner synthesis trigger.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

`akitaonrails/ai-memory` is one of the strongest external implementation references reviewed so far for persistent AI-agent memory that does **not** treat memory as current instruction authority. Its Markdown-source/derived-index split, bounded retrieval discipline, explicit historical-evidence trust boundary, zero-LLM baseline, and typed handoff lifecycle are highly compatible with the Playbook's existing design philosophy.

The review does **not** show that the Playbook needs a universal memory subsystem. The strongest incremental lesson is narrower:

> Persistent cross-session memory is safest when storage, retrieval, trust, current authority, and execution are separate layers; durable handoff is safest when it has explicit lifecycle semantics rather than being only a prose summary.

Do not install ai-memory, introduce a universal memory service, change canonical owners, or admit implementation work solely from this reference.

## Revisit trigger

Revisit if:

- adopter projects repeatedly lose session/actor handoff state, consume stale handoffs, or duplicate continuation work;
- external/persistent memory tools become common enough that the Playbook needs an explicit interoperability trust contract;
- repeated sessions materially rediscover stable historical decisions despite correct canonical routing;
- stale/wrong remembered content causes observed decision errors;
- the learned-rule-promotion pilot needs a concrete pending-write / audit implementation reference;
- another independent reviewed source strengthens the case for a durable agent-memory / session-continuity synthesis.
