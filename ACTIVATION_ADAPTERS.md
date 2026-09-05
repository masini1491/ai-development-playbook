# Thin Activation Adapters

> **Role**：把不同 AI runtime 導向同一個 Playbook bootstrap；本檔是 distribution / activation adapter，不是新的 policy authority。
>
> **Authority**：實際規則仍以目標 project governance、`CHAT_INIT.md` 與其 routed canonical owner 為準。`PLAYBOOK_INDEX.json` 只提供 machine-readable discovery，不保存 current project state。

## Adapter contract

任何 runtime 只需要完成：

`Resolve project repository / baseline → read project AGENTS.md → resolve Playbook baseline → optionally read PLAYBOOK_INDEX.json for machine discovery → read CHAT_INIT.md → route minimum-sufficient canonical owner → obey project-specific authority`

Adapter 不應：

- 複製完整 Playbook policy 到 tool-specific config；
- 把 `PLAYBOOK_INDEX.json` 當成 policy/state authority；
- 因 runtime 有 filesystem / connector / credential capability 就擴張 write 或 execution scope；
- 宣稱 native hook / installer 已存在，除非該 runtime 實際另有 adapter implementation。

## Generic bootstrap payload

可放入支援 persistent instruction / project rule / startup prompt 的 runtime：

```text
This project uses masini1491/ai-development-playbook as a common AI engineering baseline.
First read this project's current AGENTS.md and resolve its declared Playbook baseline.
For machine-readable discovery you may consult PLAYBOOK_INDEX.json, but it is routing-only.
Then read the selected baseline's CHAT_INIT.md and load only the minimum-sufficient canonical sections for the current task.
Project-specific governance and technical source of truth remain higher authority.
Do not infer repository write or execution authority from access capability.
```

## Runtime mappings

| Runtime family | Thin activation use |
| --- | --- |
| ChatGPT | Put the generic bootstrap in project/work instructions or send it once at session start; repository-native reads should then follow `CHAT_INIT.md`. |
| Codex / coding agent | Prefer project `AGENTS.md` as the activation surface; the launch prompt should point to current project governance rather than copy Playbook rules. |
| Claude Code / Cursor / Gemini / other coding assistants | Use the runtime's persistent project-instruction surface, if available, only to install the generic bootstrap pointer; keep detailed rules in the Playbook. |
| Custom CLI / IDE extension | Parse `PLAYBOOK_INDEX.json` for stable capability IDs / owner pointers, then read the canonical Markdown owner before making a decision. |

## Activation maturity boundary

This repository now provides **manual thin activation adapters + machine-readable routing discovery**. It does **not** claim native marketplace installers, hooks, generated per-tool command packs, or automatic startup integration for every runtime.

Core principle: **Activate by pointer, not policy copy.**
