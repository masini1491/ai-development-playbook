# Thin Activation Adapters

> **Role**：把不同 AI runtime 導向同一個 Playbook bootstrap；本檔是 distribution / activation adapter，不是新的 policy authority。
>
> **Authority**：實際規則仍以目標 project governance、`CHAT_INIT.md` 與其 routed canonical owner 為準。`PLAYBOOK_INDEX.json` 只提供 machine-readable discovery，不保存 current project state。

## Adapter contract

任何 runtime 只需要完成：

`Verify / resolve project workspace → read project AGENTS.md → resolve declared Playbook baseline（floating ref → cheap exact revision）→ optionally read PLAYBOOK_INDEX.json for machine discovery → read CHAT_INIT.md → route minimum-sufficient canonical owner → obey project-specific authority`

若 requested project 不是目前已驗證 workspace：不要用舊聊天、memory、repository name 或相似專案內容補成 current state。Runtime 支援 workspace / folder selection 或 access request 時，先請使用者開啟、選取或授權正確 project workspace，再重新執行 repository identity verification；不得自行掃描無關 filesystem、切換、clone 或猜測另一個 repository。詳細 repository identity / permission gate 仍由 `REPOSITORY_EXECUTION.md` 擁有。

若 project 採用 floating Playbook baseline（例如 `main`），在把該 baseline 視為本次 identified activation baseline 前，先用最低成本、已允許的 read-only identity probe resolve 成 exact immutable revision。Moving ref 只用來選 revision；後續需要 same-revision consistency 時仍依 `INFORMATION_INTEGRITY.md` 的 Snapshot Consistency Guard。這不要求 full clone、full fetch 或全文掃描 Playbook。

Adapter 不應：

- 複製完整 Playbook policy 到 tool-specific config；
- 把 `PLAYBOOK_INDEX.json` 當成 policy/state authority；
- 因 runtime 有 filesystem / connector / credential capability 就擴張 write 或 execution scope；
- 宣稱 native hook / installer 已存在，除非該 runtime 實際另有 adapter implementation。

## Generic bootstrap payload

可放入支援 persistent instruction / project rule / startup prompt 的 runtime：

```text
Verify that the current workspace is the requested project repository. If it is not, ask the user to open/select/grant the correct workspace and re-verify; do not infer project state from prior context.
Read this project's current AGENTS.md and determine whether it adopts masini1491/ai-development-playbook.
If adopted, resolve the project's declared Playbook baseline. For a floating ref, use the cheapest permitted read-only probe to identify the exact revision.
Then read that revision's CHAT_INIT.md and load only the minimum-sufficient canonical sections for the current task. Do not use the Playbook README as a normal bootstrap router.
For machine-readable discovery you may consult PLAYBOOK_INDEX.json when actually needed, but it is routing-only.
Project-specific governance and technical source of truth remain higher authority.
Do not infer repository write or execution authority from access capability.
```

## Runtime mappings

| Runtime family | Thin activation use |
| --- | --- |
| ChatGPT | Put the generic bootstrap in project/work instructions or send it once at session start; repository-native reads should then follow `CHAT_INIT.md`. |
| Codex / coding agent | Prefer project `AGENTS.md` as the activation surface; the launch prompt should point to current project governance rather than copy Playbook rules. If the selected workspace is not the requested repository, request the minimum user workspace/access correction and re-run identity verification before loading project state. |
| Claude Code / Cursor / Gemini / other coding assistants | Use the runtime's persistent project-instruction surface, if available, only to install the generic bootstrap pointer; keep detailed rules in the Playbook. |
| Custom CLI / IDE extension | Parse `PLAYBOOK_INDEX.json` for stable capability IDs / owner pointers, then read the canonical Markdown owner before making a decision. |

## Activation maturity boundary

This repository now provides **manual thin activation adapters + machine-readable routing discovery**. It does **not** claim native marketplace installers, hooks, generated per-tool command packs, or automatic startup integration for every runtime.

Core principle: **Activate by pointer, not policy copy.**
