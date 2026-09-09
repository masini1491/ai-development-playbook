# External Governance / Agentic Engineering Landscape

> **Maintainer-only discovery inventory.** This file is not a capability index, task queue, roadmap, or authority surface. It exists only to avoid duplicate external research and to prioritize bounded maintainer reviews.
>
> Normal Playbook bootstrap, capability discovery, capability inventory, gap/absence review, implementation routing, validation routing, and adopter-project work must not route here. A listed repository does not become capability evidence or admitted work by appearing in this inventory.

## Status semantics

- `REVIEWED` — a bounded maintainer comparative review exists under `maintainer/references/`.
- `DISCOVERED` — candidate identified; no maintainer dossier yet.
- `DEFERRED` — intentionally not prioritized for review at present.

For `DISCOVERED` entries, resolve the source's current exact immutable revision only when a real bounded review begins; do not treat this inventory as a freshness snapshot of unreviewed repositories.

## Landscape

| Repository | Category | Priority | Status | Why it is interesting | Reviewed revision / dossier |
| --- | --- | --- | --- | --- | --- |
| `Seekers2001/docs-governance` | Documentation governance / drift / evidence | HIGH | REVIEWED | Thin documentation spine, read-only audits, TEST-ID linkage, contract-first and regression governance patterns | `6907415467ebdbde1f50179f88340b66c74ad8d0` → `Seekers2001-docs-governance.md` |
| `ldastey-dev/agentic-context` | Context routing / multi-agent distribution | HIGH | REVIEWED | On-demand keyword routing, thin runtime adapters, generated wrappers, cross-platform deploy validation | `502dc83effca9cff6018859f05bcc581c8a11eb2` → `ldastey-dev-agentic-context.md` |
| `awslabs/aidlc-workflows` | Full AI SDLC governance / harness-neutral workflow | HIGH | REVIEWED | Deterministic workflow/phase/stage state machines, approval gates, append-only audit trail, human-affirmed durable learning, harness-neutral core and generated runtime projections | `227745d03bdd1879f51409eeba051e4c6c585b5f` → `awslabs-aidlc-workflows.md` |
| `Fission-AI/OpenSpec` | Spec / admission lifecycle / cross-repo planning | HIGH | REVIEWED | Explicit explore→propose admission boundary, current specs vs future deltas, update-vs-new identity heuristic, Stores for shared cross-repo planning | `e062b9572be933564ba3899d059377dfa1393e32` → `Fission-AI-OpenSpec.md` |
| `gastownhall/beads` | Durable agent memory / dependency-aware task graph | HIGH | DISCOVERED | Structured long-horizon memory, blockers/dependencies, atomic task claiming, semantic compaction, maintainer/contributor separation | resolve at review |
| `GSA-TTS/agentic-coding-playbook` | Governance / authority / compliance-oriented agent workflow | HIGH | DISCOVERED | Universal contract + project layer, fail-closed prerequisites, deterministic checks and governance composition | resolve at review |
| `github/spec-kit` | Spec-driven development / work admission | HIGH | DISCOVERED | Constitution/spec/plan/tasks/implement flow, idea shaping and decision gates, implementation/spec convergence | resolve at review |
| `NeoLabHQ/context-engineering-kit` | Context self-reflection / pluginized learning | MEDIUM | DISCOVERED | Reflect→memorize loops, granular loading, judge/subagent patterns, claims about reliability vs token cost worth independent verification | resolve at review |
| `humanlayer/advanced-context-engineering-for-coding-agents` | Brownfield context engineering / session compaction | MEDIUM | DISCOVERED | Frequent intentional compaction, research→plan→implement, durable specs and context-window management in large codebases | resolve at review |
| `obra/superpowers` | Procedure / skills / behavioral enforcement | MEDIUM | DISCOVERED | Structured design→plan→implementation flow, TDD, verification-before-completion, subagent workflows and skill behavior evaluation | resolve at review |
| `cnfjlhj/completion-learn` | Post-completion learning / capability sedimentation | MEDIUM | DISCOVERED | Distinguishes task completion from durable learning; useful for maintainer promotion criteria and self-correction flow | resolve at review |
| `Dicklesworthstone/agentic_coding_flywheel_setup` | Reproducible agent runtime bootstrap / integrity | MEDIUM | DISCOVERED | Manifest-driven generation, doctor checks, checksum verification, idempotent setup, immutable release/SHA discipline | resolve at review |

## Current review order

Unless a concrete incident or maintainer question changes priority, the lowest-sufficient next review order is:

1. `gastownhall/beads` — durable memory, dependency graph, and multi-agent task ownership.
2. `GSA-TTS/agentic-coding-playbook` — authority/fail-closed/compliance composition.
3. `NeoLabHQ/context-engineering-kit` — self-reflection and durable-learning promotion patterns.
4. `github/spec-kit` — spec-driven admission, shaping, and convergence patterns now that OpenSpec provides the lighter comparison baseline.
5. `humanlayer/advanced-context-engineering-for-coding-agents` — brownfield session/context management and compaction discipline.

This order is research priority only. It does not authorize mutation, task admission, installation, adoption, or implementation.

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
