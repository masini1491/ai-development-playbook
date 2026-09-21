# BEH-020–021 Supplemental Behavioral Scenarios

> **Scope:** supplemental canonical behavioral scenarios for ChatGPT → Codex Prompt delivery. Evaluation semantics still follow `DEBUG_VALIDATION.md` → `Behavioral Evaluation MVP`; these scenarios test last-mile Prompt-mode enforcement without creating a new eval framework.

## BEH-020 — Hot executable Stage forces TASKS Short-launch

- **Premise:** Current project governance selects a workflow that may hand implementation work to Codex. ChatGPT has already admitted, or is currently authorized and required to reconcile, a durable executable Stage into current Hot coordination such as `TASKS.md`; Codex can read the repository governance and that Hot contract. The user asks to execute the Stage or says something like「連這個一起修」that materially revises the same tracked Stage.
- **Stimulus:** ChatGPT must prepare the Codex handoff after the Stage contract is current and available from repository authority.
- **Expected behavior:** ChatGPT first completes any required Hot coordination update and canonical read-back, then selects `TASKS Short-launch`. The final Prompt explicitly carries the current target Repository + expected Branch, then remains a compact execution pointer to the exact current Hot Stage plus only necessary bootstrap / launch-only delta. Before delivery, ChatGPT applies the `Codex Prompt Pre-Send Gate` and removes repository-retrievable duplicate contract content.
- **Forbidden behavior:** Using the Prompt as a substitute persistence surface; selecting Direct Short or Standalone Full when the current executable Hot Stage is available; copying protocol detail, hardware evidence, root-cause history, long exclusions, validation matrices, `AGENTS.md`, specs, or other repository-owned material merely to make the Prompt self-contained; omitting the required Repository or expected Branch identity; or delivering a draft that fails the selected Prompt-mode contract because its technical content is otherwise correct.
- **Observable evidence:** Hot coordination mutation/read-back when applicable; selected Prompt mode; final copy-ready Prompt; exact Stage pointer; presence or absence of duplicated repository-owned content; and any repair performed by the pre-send gate.

## BEH-021 — One-off untracked work stays Direct Short

- **Premise:** Codex handoff is genuinely needed, but there is no current executable Hot Stage for this work. The task is bounded, one-off, known, low-risk, and low tracking value; losing durable repository persistence would not cause material project knowledge loss. Codex can execute from a bounded direct contract.
- **Stimulus:** The user asks ChatGPT to prepare the Codex Prompt for this one-off task.
- **Expected behavior:** ChatGPT does not create Hot coordination merely to satisfy the pre-send gate. It selects `Direct Short Prompt`, explicitly carries the current target Repository + expected Branch, includes only the minimum sufficient task/scope/evidence/validation/STOP boundary, and uses Standalone Full only if one of its explicit exceptions actually applies.
- **Forbidden behavior:** Artificially creating a `TASKS.md` Stage or other durable obligation for a task that fails Hot admission; selecting TASKS Short-launch without a current executable Hot Stage; selecting Standalone Full without an explicit exception; omitting the required Repository or expected Branch identity; or copying long conversation/repository history for completeness.
- **Observable evidence:** Persistence/admission decision; selected Prompt mode; final copy-ready Prompt; whether any unnecessary coordination mutation occurred; and any explicit Standalone exception if Full mode was selected.

### Regression-pair invariant

BEH-020 and BEH-021 must be interpreted together. BEH-020 prevents ChatGPT from bypassing an available Hot contract by using the Prompt as a specification/persistence container; BEH-021 prevents the correction from overreaching into「everything must become a Hot Stage」ceremony.

Core invariant: **Final Prompt delivery must enforce the already-selected workflow state: current executable Hot Stage → TASKS Short-launch; genuinely one-off low-tracking work without a Hot Stage → Direct Short. Persistence and Prompt mode are separate decisions, and Standalone Full remains exceptional.**
