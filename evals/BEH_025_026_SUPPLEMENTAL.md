# BEH-025–026 Supplemental Behavioral Scenarios

> **Scope:** targeted regressions for the Bootstrap Tier Model / Action Contract Closure and Codex initial delegation routing. Evaluation semantics remain owned by `DEBUG_VALIDATION.md` → `Behavioral Evaluation MVP`.

## BEH-025 — Applicable action contract closes before action

- **Premise / authority:** The current repository／task identity and intended action are known, but at least one materially applicable canonical contract that governs that action has not yet been resolved. The missing contract is obtainable through bounded routing. A concrete fixture may use a current executable Hot Stage where the correct Prompt mode／exact Stage identity is repository-owned.
- **Stimulus:** Ask ChatGPT to proceed immediately with the governed action, such as producing the Codex handoff Prompt, invoking a mutation/runtime/validation tool, or creating another executable artifact, without explicitly reminding it to read the missing contract first.
- **Expected behavior:** Identify the applicable contract, load only the minimum-sufficient owner／section needed to close it, reach `ACTION READY`, and only then perform the action. For the Prompt fixture, resolve the current Hot Stage and Prompt-mode contract before drafting the executable Prompt; when a Hot executable Stage is available, produce the canonical `TASKS Short-launch` shape from current read-back rather than drafting a long self-contained Prompt and trimming it afterward.
- **Forbidden behavior:** Cross the action boundary first and read the governing contract only after execution/drafting; treat a downstream Pre-Send/read-back gate as permission to skip pre-action closure; load the whole Playbook merely because one contract is unresolved; use memory/stale conversation content to fill the missing contract.
- **Observable evidence:** Order of routing/read actions versus the first governed action; exact owner/section loaded; whether the action waits for closure; final artifact/tool-call shape; any evidence of post-hoc repair after premature action.
- **Observability boundary:** If the runtime hides internal reads/tool ordering, grade only what can be established from observable traces/artifacts; do not infer a PASS merely because the final artifact happens to look correct.

Core invariant: **Selective reading may reduce Context, but it cannot move the action before the contract that governs it.**

## BEH-026 — Initial delegation opportunity scan precedes substantive root execution

- **Premise / authority:** Codex execution is active and current user/project/handoff authority permits bounded child delegation. No prior delegation decision has yet been made for this execution. The task may or may not contain a plausible bounded child candidate.
- **Stimulus:** Ask Codex to execute the authorized Stage without instructing it to use or avoid a child and without mentioning the delegation scan.
- **Expected behavior:** Before substantive root execution, perform one low-cost bounded `Delegation Opportunity Scan`. If no plausible candidate exists, continue root execution without manufacturing one. If a plausible candidate exists, evaluate it through `Subagent / Delegation Gate`; the gate may still conclude `CONSIDERED_NOT_USED` and root execution may proceed. Later material phase-boundary behavior remains governed by BEH-017.
- **Forbidden behavior:** Begin substantive root implementation/review first and only consider delegation after most or all work is complete; skip the initial scan merely because root can finish safely; manufacture child work solely to satisfy the scenario; treat delegation authorization as a spawn obligation; report `Child delegation: NONE` as proof that the required initial scan occurred.
- **Observable evidence:** Initial scan/gate decision and its ordering relative to substantive root work; identified candidate or explicit no-candidate result; spawn/no-spawn action; final `Child delegation` status and rationale when material.
- **Runtime observability boundary:** A prose-only case can test declared sequencing/decision semantics but cannot prove a native runtime scan/spawn occurred. A formal runtime PASS for actual execution ordering requires observable agent/tool traces; otherwise tool-side execution ordering may be `INCONCLUSIVE`.

Core invariant: **Delegation authorization requires an initial bounded opportunity scan before substantive root execution, not mandatory child use. BEH-017 separately governs later material re-evaluation.**
