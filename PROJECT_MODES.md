# Project AI Modes

> **Authority**：AI project mode selection for repositories adopting this Playbook.
> **Read when**：starting a new project, normalizing project governance, or deciding whether Codex participates in the repository workflow.

The Playbook exposes exactly two supported AI project modes:

- `ChatGPT-Only`
- `ChatGPT+Codex`

A project should declare one mode in its current governance, preferably with the stable field:

```text
Project AI mode: ChatGPT-Only
```

or:

```text
Project AI mode: ChatGPT+Codex
```

If a project has not declared either value, that is **mode not yet selected**, not a third mode. Until selection is explicit, do not guess from available tools, previous sessions, repository shape, or the presence/absence of Codex; retain the conservative authority fallback from `REPOSITORY_EXECUTION.md`.

For **AI project mode selection**, this file is the canonical owner. `REPOSITORY_EXECUTION.md` → `Repository Actor Topology / Maintenance Ownership` remains the lower-level authority mechanism that decides path/action authority, permissions, write-target locking, and safe fallback behavior **inside the selected mode**. Lower-level actor/path-action declarations do not create additional user-selectable AI project modes.

### Mode is not a subscription or capability tier

`ChatGPT-Only` and `ChatGPT+Codex` describe the repository's **AI actor topology**, not a ChatGPT subscription plan, model tier, usage quota, or universal product-capability claim. Do not select or reinterpret a mode merely from account tier, model name, tool availability, or an assumption about what a particular ChatGPT product surface usually provides.

Runtime capability remains session-specific. The same declared mode may operate on different ChatGPT surfaces with different connectors, execution runtimes, filesystem/network access, context limits, or other capabilities; current task execution must still pass the relevant capability and authority gates.

## `ChatGPT-Only`

ChatGPT is the repository's AI maintainer across planning and implementation work. Within the intersection of current project governance, Current Write Target, Task/Stage authorization, execution permission, and credential capability, ChatGPT may perform the repository work assigned to the AI maintainer, including canonical docs, source, tests, tooling, validation, and authorized Git mutation.

Codex is not part of the repository workflow. Do not invent a Codex handoff merely because work touches source, tests, tooling, build, or implementation artifacts.

### Minimum-sufficient ChatGPT capability floor

For a `ChatGPT-Only` project, design the **core workflow** to require the lowest sufficient ChatGPT capability set that can preserve correctness, authority, provenance, validation truth, and required execution semantics. Do not make a stronger ChatGPT execution surface, richer runtime, broader connector set, larger context, or other higher capability a prerequisite merely because it is more convenient.

Recommended design pressure:

`core requirement → lowest sufficient ChatGPT capability path → verify capability/evidence → execute | admitted fallback | explicit capability gap`

- Prefer bounded retrieval, progressive routing, verified cache/reuse, deterministic adapters, verifiable artifact transport/materialization, and other designs that reduce unnecessary capability requirements without weakening evidence.
- Absence of a convenient/direct capability does not by itself prove the core workflow is impossible; an alternate path may be used only when it preserves the same required authority/integrity semantics and is actually verified.
- Do not simulate unavailable capabilities, weaken canonical identity/integrity checks, replace required deterministic execution with model inference, or silently reduce validation standards merely to keep the workflow on a weaker surface.
- When the task materially requires a capability the current ChatGPT session does not have and no admitted equivalent path exists, report the scoped capability gap or STOP. `ChatGPT-Only` does not require pretending every ChatGPT session can complete every task.
- Capabilities that are optional acceleration/convenience should remain optional; capabilities that are materially required for correctness should be declared and gated explicitly.

Host／product-specific cold-start compatibility targets are not Project AI mode semantics. Concrete ChatGPT host regression profiles, including the current preferred low-capability cold-start target, are owned by `ACTIVATION_ADAPTERS.md` → `ChatGPT Cold-start Compatibility Target`. This section only keeps the stable requirement: **design ChatGPT-Only workflows for the lowest sufficient verified capability set without weakening authority, identity, integrity, or validation truth.**

`ChatGPT-Only` does **not** mean unlimited ChatGPT authority. It does not bypass project-specific restrictions, human approval, validation gates, deployment/release permission, secrets boundaries, or any other higher-authority contract.

## `ChatGPT+Codex`

ChatGPT remains the planning / research / architecture / coordination / review and reconciliation actor. Codex participates as the coding-agent implementation actor for repository mutation assigned to it by project governance or the current authorized Stage.

Actor choice remains stage-local: read-only research, evidence work, synthesis, review, or work already authorized for ChatGPT should not be handed to Codex by habit. Conversely, a mutation assigned to Codex should not be absorbed by ChatGPT merely because ChatGPT has a writable connector or runtime.

The exact implementation scope may still be narrowed by project governance or a Task/Stage contract, but it must not create a third AI project mode.

## Human / CI / external systems

Human maintainers, CI, hardware validation, deployment systems, external services, and other non-AI actors can still participate under project governance. Their existence does not create additional AI project modes.

Other AI coding agents are not separate Playbook project modes. If a project intentionally substitutes another coding agent for Codex, that is a project-specific implementation detail under the `ChatGPT+Codex` collaboration profile only when current governance explicitly maps the Codex/coding-agent responsibility to that executor; it does not create a third mode.

## Initialization / persistence

A user may select the mode naturally in a ChatGPT project-start conversation, for example:

```text
這個專案用 ChatGPT-Only。
```

or:

```text
這個專案用 ChatGPT+Codex。
```

An explicit chat choice is sufficient to resolve the mode for the **current conversation**. Durable persistence into `AGENTS.md` or equivalent project governance is a separate repository mutation: perform it only when Current Write Target, existing governance mutation authority, current Task/Stage authorization, and permission/capability all allow that write. Mode selection itself does not grant ChatGPT permission to rewrite governance. If durable persistence is not currently authorized, retain the current-chat choice for this session and leave the repository unchanged rather than self-expanding authority.

A fresh session must not rely on old chat memory instead of current repository governance. If the durable declaration is still absent, the fresh session returns to **mode not yet selected** until the user or current project governance explicitly selects one again.

Changing an existing project's mode is a governance change. Do not infer a mode switch from a one-off handoff, temporary tool outage, generic continuation such as「好／繼續」, or the fact that one actor completed the previous Stage.

核心原則：**User chooses one of two AI project modes; mode is actor topology rather than product tier; ChatGPT-Only should minimize unnecessary capability requirements without weakening correctness or evidence; host/product compatibility targets belong to activation adapters; durable persistence still requires ordinary governance-write authority; lower-level authority gates decide what the selected actors may actually do.**
