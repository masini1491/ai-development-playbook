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

For **AI project mode selection**, this file is the canonical owner. `REPOSITORY_EXECUTION.md` → `Repository Actor Topology / Maintenance Ownership` remains the lower-level authority mechanism that decides path/action authority, permissions, write-target locking, and safe fallback behavior **inside the selected mode**. Its generic actor-topology language does not create additional user-selectable AI project modes.

## `ChatGPT-Only`

ChatGPT is the repository's AI maintainer across planning and implementation work. Within the intersection of current project governance, Current Write Target, Task/Stage authorization, execution permission, and credential capability, ChatGPT may perform the repository work assigned to the AI maintainer, including canonical docs, source, tests, tooling, validation, and authorized Git mutation.

Codex is not part of the repository workflow. Do not invent a Codex handoff merely because work touches source, tests, tooling, build, or implementation artifacts.

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

ChatGPT should normalize that choice into the repository's durable governance before relying on it across future sessions. A chat-only choice is sufficient for the current conversation when explicit, but a fresh session must not rely on old chat memory instead of current repository governance.

Changing an existing project's mode is a governance change. Do not infer a mode switch from a one-off handoff, temporary tool outage, generic continuation such as「好／繼續」, or the fact that one actor completed the previous Stage.

核心原則：**User chooses one of two AI project modes; repository governance persists it; lower-level authority gates still decide what the selected actors may actually do.**
