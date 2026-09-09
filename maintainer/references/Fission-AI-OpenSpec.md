# Fission-AI/OpenSpec

- Source: `Fission-AI/OpenSpec`
- Reviewed revision: `e062b9572be933564ba3899d059377dfa1393e32`
- Source tree: `10f256265a7f55ba0a0d92a6fc9a6171685579ac`
- License: MIT
- Source role: external spec-driven change / admission / cross-repository planning reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps materially with existing Playbook concerns around separating current truth from proposed work, keeping planning artifacts semantically distinct, explicit work admission, task identity/revision decisions, progressive rigor, cross-repository authority boundaries, and evidence-vs-completion separation.

OpenSpec's `openspec/specs/` versus `openspec/changes/<change>/` model closely matches the Playbook-side interoperability mapping already present in `INTEROPERABILITY.md`: current specs may be designated canonical project truth, while proposal / delta specs / design / tasks are future-state change detail until the project promotes them through its lifecycle.

The Playbook also already distinguishes observation, recommendation, and admitted work; OpenSpec operationalizes a similar boundary in a product-facing way with `explore` (no artifacts or code) followed by an explicit `propose` action that creates a durable change.

## 2. Same failure mode, different architecture

### Pre-admission thinking

OpenSpec's `/opsx:explore` intentionally creates no change folder, artifacts, or code. The user can investigate alternatives and abandon dead ends without repository persistence, then explicitly start `/opsx:propose` when ready. The Playbook achieves the same authority goal through `Observation ≠ Recommendation ≠ Admitted Work` and persistence/admission gates rather than a dedicated command mode.

A useful difference is provenance: OpenSpec says the AI carries exploration conversation context into the proposal, but the exploration itself is not archived. That is lightweight and low-friction, but a long or cross-session exploration may require additional provenance/rehydration discipline if the exact reasoning matters later.

### Current truth versus future change

OpenSpec makes the split concrete:

- `specs/` = what the system currently does;
- `changes/<name>/` = proposed future modification;
- delta specs express only ADDED / MODIFIED / REMOVED behavior;
- archive merges the deltas into main specs and preserves the change folder in history.

The Playbook uses semantic owners (`Current canonical`, Hot detail, Evidence, Historical) rather than prescribing one universal file layout or archive operation.

### Artifact dependency versus phase gate

OpenSpec's default schema models `proposal → specs/design → tasks`, but explicitly says dependencies are enablers rather than mandatory next-step gates. Artifacts remain editable at any time, and teams can define custom schemas.

The Playbook similarly avoids forcing every project into one fixed lifecycle; its Task/Stage, actor, validation, and permission gates are authority/correctness boundaries rather than a mandatory spec waterfall.

### Task identity / revision

OpenSpec's user-facing rule is simple: refine the same change when the goal is still the same; start a new change when the intent fundamentally changes or scope explodes into different work. This is closely aligned with the Playbook's `Task Identity / Revision Gate`, expressed as a lightweight product heuristic instead of a general governance contract.

### Verification

OpenSpec's optional `/opsx:verify` compares implementation against tasks, specs, and design using completeness / correctness / coherence. It uses heuristic code search and inference for some checks, explicitly degrades when artifacts are missing, and does not block archive automatically.

The Playbook already treats such output as scope-qualified evidence rather than universal completion authority. Deterministic validation, behavioral evaluation, canonical read-back, and real-world evidence remain separate layers.

### Cross-repository planning

OpenSpec Stores (beta) let planning live in a standalone Git repository. A component repo may either route OpenSpec commands to that store or keep its own local OpenSpec root while referencing store specs as read-only upstream context. Worksets only open multiple folders together; they do not copy source context, choose affected repos, or grant edit permission.

This strongly aligns with the Playbook's cross-repository write lock and capability-vs-authority rules: visibility / common workspace / repository relationship does not imply mutation authority.

## 3. External capabilities / implementation maturity worth further evidence

These are external implementation patterns, not whole-Playbook absence claims.

### A. Explicit `explore → propose` admission UX

OpenSpec gives users a concrete no-persistence thinking mode and a named transition that creates durable work. This is a strong user-facing implementation of the same semantic boundary the Playbook already defines abstractly.

### B. Delta-to-canonical promotion lifecycle

Brownfield changes are represented as deltas rather than full future copies. Archive promotes those deltas into current specs while preserving the historical change. This is a clean productized example of future-state detail becoming current canonical truth through an explicit lifecycle action.

### C. Cross-repo requirements Store + local implementation plans

OpenSpec can keep shared behavior in one planning repo while component repos own their local implementation changes. References expose canonical upstream context without routing tasks or granting edit authority. This is a mature concrete pattern for shared requirements across repositories.

### D. Schema-defined artifact DAG

OpenSpec lets teams define artifact types and dependency relationships in schemas. The graph determines what context enables another artifact without requiring one rigid global phase order. This may be useful as a comparison point for future machine-readable planning/routing experiments.

### E. Multi-tool distribution maturity

OpenSpec installs skill/command surfaces for many coding assistants and normalizes different invocation syntaxes. This is another external example of a stronger runtime-distribution layer than this Playbook's current manual thin adapters.

## 4. Useful expression / UX patterns

- `explore → propose → apply → archive` communicates `think → agree → build → record` in a compact mental model.
- Review order is fail-fast: read proposal first and stop immediately if the problem/scope is wrong, then inspect specs, then tasks/design.
- `same goal, better approach → update; fundamentally different intent → new change` is a concise user-facing identity heuristic.
- Plain Markdown artifacts remain directly editable; tool state does not hide the actual planning content.
- Store commands prominently report the actual OpenSpec root being used, which reduces silent cross-repository targeting mistakes.
- Worksets explicitly state that opening folders together does not copy context or grant write permission.

## 5. Runtime/product-specific patterns not suitable for direct generalization

- `openspec/specs/` is only project truth when the project chooses it as such; the Playbook must not universally replace project-specific technical/canonical owners with OpenSpec specs.
- `archive` is an OpenSpec lifecycle event, not universal Playbook completion evidence. Code, tests, deployment, hardware, or user-observed validation may remain separate.
- `/opsx:verify` contains heuristic LLM/search judgment. Its CRITICAL/WARNING/SUGGESTION taxonomy is useful inside that workflow but is not a deterministic guarantee or universal Playbook validation taxonomy.
- Stores, references, working context, and worksets are explicitly beta at the reviewed revision; their command/file contracts may change.
- OpenSpec's no-phase-gate philosophy is a product choice. Some projects still require hard approval, security, release, or regulatory gates.
- Tool-specific slash-command/skill installation and invocation syntax are distribution implementation details, not authority semantics.

## 6. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Explore-to-admission UX experiment** — compare the current natural-language Playbook admission contract against an explicit no-persistence `explore` mode followed by a named `propose/admit` transition. Measure accidental durable-work promotion, user friction, and scope clarity.
2. **Task identity wording fixture** — test whether the simple `same goal → revise; fundamentally different intent → new task/change` heuristic improves fresh-session behavior on borderline Task Identity / Revision cases.
3. **Delta-to-canonical pilot** — on one adopter with a stable requirements owner, compare full future-state planning versus delta-first change artifacts for review cost, drift, merge/reconciliation cost, and historical clarity.
4. **Cross-repo planning-store pilot** — compare a central read-only requirements/planning repo plus local component implementation plans against duplicated per-repo requirements. Measure provenance, stale copies, write-target ambiguity, and agent retrieval cost.
5. **Artifact-DAG experiment** — compare fixed sequential planning instructions with a machine-readable artifact dependency graph whose edges enable context without forcing phase order.
6. **Verification calibration** — compare OpenSpec-style heuristic completeness/correctness/coherence review against the Playbook validation ladder and canonical completion evidence to identify where heuristic review adds value without being mistaken for proof.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

OpenSpec does not currently demonstrate a missing core authority layer in this Playbook. In fact, its current/future separation, explicit explore/propose boundary, update-vs-new identity heuristic, and cross-repository Store model strongly reinforce several existing Playbook contracts.

The highest-value transferable idea is **explicit admission UX**: make pre-admission exploration visibly cheap and non-persistent, then require a clear transition before durable work is created. The Playbook already owns the underlying rule; the open question is whether a similarly simple user-facing mechanism improves behavioral reliability enough to justify additional product/procedure surface.

The second-highest-value pattern is the **shared requirements store + local implementation ownership** model for projects that genuinely span repositories. It should remain an evidence candidate until repeated adopter need justifies a concrete Playbook-side integration pattern.

Do not change canonical policy, create a new universal spec directory, or install OpenSpec solely from this reference.

## Revisit trigger

Revisit if:

- fresh-session evaluations still confuse recommendation/exploration with admitted durable work;
- Task Identity / Revision cases remain difficult for users or agents despite the existing canonical gate;
- multiple adopter projects need one requirements source across several code repositories;
- active changes repeatedly duplicate full future specs or create expensive reconciliation noise;
- native multi-tool activation/distribution becomes a material Playbook productization goal.