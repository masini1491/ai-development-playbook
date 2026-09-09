# Playbook Maintainer Zone

> **Maintainer-only retrieval surface.** This directory is persisted inside the repository but is intentionally excluded from normal Playbook bootstrap, capability discovery, capability inventory, gap/absence review, implementation routing, validation routing, and adopter-project task context.
>
> **Authority boundary:** content here is pre-canonical maintainer evidence and working material. It does not prove a Playbook capability, policy, implementation, validation result, admitted task, bug, or completion state.

## Entry gate

Read this directory only for an explicit Playbook-maintenance intent such as:

- Playbook self-review / self-correction;
- external governance or workflow comparison;
- Playbook evolution / productization research;
- suspected Playbook defect investigation;
- behavioral-evaluation candidate research;
- maintainer review of possible future directions.

Normal questions such as “what capabilities does this repository have?”, “does the Playbook support X?”, capability inventory, competitive capability lookup, or repository-level absence/gap review must stay on the normal routing graph (`CHAT_INIT.md` → `CAPABILITY_INDEX.md` / `PLAYBOOK_INDEX.json` → canonical owner / implementation / eval evidence) and must not enter this directory.

If a normal search tool accidentally returns a hit under `maintainer/`, treat it only as a maintainer-zone hit: do not follow it for normal capability synthesis, do not count it as positive capability evidence, and do not use it to prove a gap, bug, task, or policy.

## One-way dependency rule

`maintainer/` may point outward to current canonical owners for comparison or reconciliation. Normal canonical owners must not depend on `maintainer/` for their meaning, routing, execution, or validation semantics.

Removing this directory must not change normal Playbook behavior.

## Contents

- `references/` — external repositories, workflows, papers, or governance systems used for bounded comparative review. Preserve source revision, provenance, observations, limitations, and reference adoption state.
- `candidates/` — possible development directions or governance capabilities worth future evidence gathering. Persistence here does not admit work.
- `investigations/` — suspected bugs, behavioral anomalies, competing explanations, and evidence needed before classification.

Formal behavioral scenarios and run evidence still belong under `evals/` after admission. Confirmed canonical changes still belong in their canonical owner. Current executable work still requires normal Task/Stage admission.

## Promotion flow

`observation / external idea / suspected bug → maintainer zone → bounded evidence / comparison / behavioral evaluation → conclusion`

Only after the conclusion is established may the result become one of:

- a canonical owner update;
- an admitted Hot/Cold task under normal governance;
- a formal behavioral scenario / run record;
- a rejected or reference-only maintainer conclusion.

Core invariant: **persisted for maintainer learning, non-routable by default, non-authoritative until promoted through normal governance.**
