# External Governance / Agentic Engineering Landscape

> **Maintainer-only discovery inventory.** This file is not a capability index, task queue, roadmap, or authority surface. It exists only to avoid duplicate external research and to prioritize bounded maintainer reviews.
>
> Normal Playbook bootstrap, capability discovery, capability inventory, gap/absence review, implementation routing, validation routing, and adopter-project work must not route here. A listed repository does not become capability evidence or admitted work by appearing in this inventory.

## Status semantics

- `REVIEWED` — a bounded maintainer comparative review exists under `maintainer/references/`.
- `DISCOVERED` — candidate identified; no maintainer dossier yet.
- `DEFERRED` — intentionally not prioritized or not suitable for substantive maintainer review under current constraints.

For `DISCOVERED` entries, resolve the source's current exact immutable revision only when a real bounded review begins; do not treat this inventory as a freshness snapshot of unreviewed repositories.

## Landscape

| Repository | Category | Priority | Status | Why it is interesting | Reviewed revision / dossier |
| --- | --- | --- | --- | --- | --- |
| `Seekers2001/docs-governance` | Documentation governance / drift / evidence | HIGH | REVIEWED | Thin documentation spine, read-only audits, TEST-ID linkage, contract-first and regression governance patterns | `6907415467ebdbde1f50179f88340b66c74ad8d0` → `Seekers2001-docs-governance.md` |
| `ldastey-dev/agentic-context` | Context routing / multi-agent distribution | HIGH | REVIEWED | On-demand keyword routing, thin runtime adapters, generated wrappers, cross-platform deploy validation | `502dc83effca9cff6018859f05bcc581c8a11eb2` → `ldastey-dev-agentic-context.md` |
| `awslabs/aidlc-workflows` | Full AI SDLC governance / harness-neutral workflow | HIGH | REVIEWED | Deterministic workflow/phase/stage state machines, approval gates, append-only audit trail, human-affirmed durable learning, harness-neutral core and generated runtime projections | `227745d03bdd1879f51409eeba051e4c6c585b5f` → `awslabs-aidlc-workflows.md` |
| `Fission-AI/OpenSpec` | Spec / admission lifecycle / cross-repo planning | HIGH | REVIEWED | Explicit explore→propose admission boundary, current specs vs future deltas, update-vs-new identity heuristic, Stores for shared cross-repo planning | `e062b9572be933564ba3899d059377dfa1393e32` → `Fission-AI-OpenSpec.md` |
| `gastownhall/beads` | Durable agent memory / dependency-aware task graph | HIGH | REVIEWED | Structured long-horizon memory, typed provenance/dependency graph, external gates, atomic task claiming, semantic compaction, maintainer/contributor separation | `a690b0a8c4d1ddc4f0bd9bf767499625dd71bc96` → `gastownhall-beads.md` |
| `GSA-TTS/agentic-coding-playbook` | Governance / authority / compliance-oriented agent workflow | HIGH | REVIEWED | Universal contract + thin project layer, deterministic fail-closed prerequisite identity, pinned fallback acquisition, generated routing/validation | `9ea8add75a017bed007230a530da4a943c3eebdf` → `GSA-TTS-agentic-coding-playbook.md` |
| `github/spec-kit` | Spec-driven development / work admission | HIGH | REVIEWED | Explicit pre-admission idea assessment, constitution/spec/plan/tasks separation, read-only cross-artifact analysis, append-only implementation convergence, artifact persistence models | `0c8e31ff0a98c362696c2edb6a1bb25a37f68544` → `github-spec-kit.md` |
| `NeoLabHQ/context-engineering-kit` | Context self-reflection / pluginized learning | MEDIUM | REVIEWED | Reflect→curate→memorize loop, granular context loading, independent judge/meta-judge patterns, provider-aware capability degradation | `23e2428e809d77717f8acc9659c374a3a1fcb93e` → `NeoLabHQ-context-engineering-kit.md` |
| `humanlayer/advanced-context-engineering-for-coding-agents` | Brownfield context engineering / session compaction | MEDIUM | REVIEWED | Frequent intentional compaction, research→plan→implement, high-leverage upstream review, fresh-context checkpointing | `f2bc7aec4575418d2d2e83fec078266cc56d3e6a` → `humanlayer-advanced-context-engineering-for-coding-agents.md` |
| `obra/superpowers` | Procedure / skills / behavioral enforcement | MEDIUM | REVIEWED | Behavioral TDD for skills, trigger-only discovery metadata, context-isolated subagent execution, recovery ledger, role-sensitive child routing | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` → `obra-superpowers.md` |
| `cnfjlhj/completion-learn` | Post-completion learning / capability sedimentation | MEDIUM | REVIEWED | Completion ≠ retained capability, reduced-support/near-transfer drills, explicit no-change outcome, owner-first tool evolution | `66a91d56578976d7183381ac9be9c6e9130e24cf` → `cnfjlhj-completion-learn.md` |
| `Dicklesworthstone/agentic_coding_flywheel_setup` | Reproducible agent runtime bootstrap / integrity | MEDIUM | DEFERRED | Technically relevant, but the reviewed source license contains an explicit OpenAI/Anthropic restriction; substantive comparative ingestion/adoption is not pursued under that constraint | review halted at license gate; no dossier |

## Current review order

No additional discovered repository is currently queued. A new source should be added only when a concrete maintainer question or independent research need justifies it.

This inventory is research priority only. It does not authorize mutation, task admission, installation, adoption, or implementation.

## When to synthesize

Do not create a cross-source synthesis merely because more candidates were discovered. Create a maintainer topic synthesis only after multiple bounded reviews show a stable independent retrieval intent, such as a recurring failure mode, repeated architectural trade-off, or evidence pattern that is easier to reason about across sources than inside individual dossiers.

Candidate synthesis topics may eventually include:

- routing / context loading strategies;
- admission / task lifecycle;
- durable agent memory and compaction;
- runtime adapter / distribution architecture;
- self-reflection / learned-rule promotion;
- deterministic governance and documentation drift detection.

A synthesis remains maintainer evidence until independently promoted through normal Playbook governance.
