# AI Development Playbook

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本 repository 只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密 protocol、客戶資料或其他專案機密。

## 本 Playbook 的維護方式

`masini1491/ai-development-playbook` 是共通規則來源，與一般 product / firmware repository 不同：

- 本 repository 由 **ChatGPT 直接維護**規則與文件。
- Codex / coding agent 對本 repository 預設唯讀，只需要讀取並遵守，不參與修改。
- 本 repository 若暫時出現 `TASKS.md`，只代表 ChatGPT 尚未完成的 playbook 維護事項，不是 Codex execution queue。

這是 playbook 自身的 maintenance exception；一般 project repository 仍採下方的 ChatGPT / Codex 分工。

## 核心原則

> 先取得最低充分 Evidence，再使用最低充分 Context、Model、Reasoning、Agent 與 Validation scope；只有 evidence 證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通 playbook 管「怎麼開發」；各實際專案 repository 管「系統是什麼」。

因此若本 playbook 與實際專案的 `AGENTS.md`、architecture、security、protocol、hardware evidence 或正式 source of truth 衝突，以實際專案的正式規則為準；若與使用者當次明確指示衝突，依使用者當次指示處理。

## 預設協作模型：GitHub-backed workflow

本 playbook 預設以 **GitHub repository 協作**：

- GitHub `main`（或專案明確指定的預設 branch）是 current source of truth。
- Repository root 的 `AGENTS.md` 保存穩定、長期的專案治理規則。
- Repository root 的 `TASKS.md` 是 ChatGPT / Codex 共用的 **active unfinished-work / executable scoped Prompt queue**，不是一般 changelog 或永久待辦清單。
- 尚未完成、Blocked、Deferred、Pending-validation 的工作可留在 `TASKS.md`；成功完成並驗證後應移除對應項目。
- 已完成工作的永久紀錄以 Git commit/history 為準，不在 `TASKS.md` 建立 Completed 區段。

### 一般 Project Repository 的寫入分工

- **ChatGPT**：只直接建立、讀取、更新、刪除 root `TASKS.md`；其餘 repository path 一律唯讀。負責 research、需求/架構/規格討論、review、task admission/scope、Codex Prompt 規劃。
- **Codex / coding agent**：在使用者明確授權的 Task / Stage scope 內修改 source、tests、docs、tooling、workflow 等非 `TASKS.md` 檔案，並在執行後維護 `TASKS.md` 的 status/evidence/removal。
- **`TASKS.md`**：由 ChatGPT 與 Codex 共同維護；本身不授權 Codex 自動開始其他 Stage。

典型流程：

`ChatGPT 讀最新 GitHub → 規劃 / 更新 unfinished queue → Codex 做 Repository Identity + workspace/permission gates + safe sync → 執行指定 Stage → Targeted Validation → 更新 TASKS → commit / push`

如果使用者採用純 local Git、GitLab 或其他協作平台，可以保留相同 governance 概念並映射到對應平台；本 repository 的預設說明與範例以 GitHub-backed workflow 為主。

## README Development Transparency

公開 repository 若明顯採用 ChatGPT / Codex 或其他 coding agent 作為主要開發方式，建議 README 精簡說明 human-in-the-loop 的責任分工：

- Human / developer：需求、產品方向、硬體選擇、現實世界 evidence、最終核准與需要人工完成的 validation。
- ChatGPT：research、架構/規格討論、review、task decomposition、`TASKS.md` / Codex Prompt 規劃。
- Codex / coding agent：scoped implementation、tests、static/build validation、文件與 repository maintenance。

AI-generated code / analysis 不因生成完成、command 成功或 build exit 0 就自動等於 validated product completion；仍應依專案風險完成適當 human review、protocol/network/hardware/production validation。

若 README 提及 OpenAI / ChatGPT / Codex，不應暗示 OpenAI 對專案、產品、硬體或安全決策提供贊助、認證或背書，除非確有正式關係。

## Project Scale Reporting

若 README 或公開文件展示 project size / LOC / line count：

- 必須說明統計基準，例如 Git tracked files、canonical ref/commit 或其他可重現 source。
- 必須定義 metric：physical lines、logical/executable LOC、file count 或其他。
- 若是 physical lines，需說明是否包含 blank/comment。
- 應說明主要排除項目，例如 `.git`、third-party libraries、downloaded dependencies、build/cache、generated artifacts。
- category 依 repository 實際結構定義，不強迫所有專案使用同一分類。

### Deterministic Counter Trigger

不要求每個 repository 都建立 `project-scale.ps1` 或其他 LOC script。

只有當 README 長期展示規模統計，而且數字頻繁變動、專案規模使手動計數容易 drift、或同一統計需同步到多個正式文件時，才優先建立 repository-owned deterministic counter。

已有 canonical counter 的 repository，在主要 tracked change 與 validation 完成後再更新 scale statistics；若數字未變，不製造無意義 README change。跨 repository showcase/private→public 同步屬 project-specific policy，不是本 playbook 的共通要求。

## 新聊天室最短入口

新開專案聊天室時，先讀：

1. [`CHAT_INIT.md`](CHAT_INIT.md)
2. 再依本 README 的 routing 只讀本次需要的主題文件
3. 最後讀實際目標 repository 的最新 `AGENTS.md` / `TASKS.md` 與 task-relevant source of truth

不要為了「熟悉規則」預設完整掃描本 repository。

## 文件 Routing

| 情境 | 讀取文件 |
| --- | --- |
| 新聊天室初始化 | [`CHAT_INIT.md`](CHAT_INIT.md) |
| 產生 Codex Prompt、模型/推理/Context/Agent 成本控制 | [`CODEX_PROMPT_RULES.md`](CODEX_PROMPT_RULES.md) |
| Git 安全、Repository Identity、workspace/remote permission、TASKS、寫入分工 | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機 runtime、PowerShell 7、toolchain contract | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| Debug、root cause、retry、validation、evidence 等級 | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術/協議研究、避免重造輪子、architecture/target/capability | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| ESP32 / embedded / hardware evidence / board profile / diagnostic harness | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本 playbook 本身 | [`AGENTS.md`](AGENTS.md) |

## 建議 Authority 順序

一般情況建議：

1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance / technical source of truth
3. 本 playbook
4. 實際目標 repository `TASKS.md` active queue
5. 舊聊天室、舊 Prompt、cached/local copy、記憶

`TASKS.md` 不得覆蓋更高層 architecture / security / protocol / hardware evidence。

## 適用方式

這不是要求所有 repository 使用相同 framework、語言、CI 或硬體。它提供的是：

- Repository Identity Gate
- Workspace Write Capability Gate
- Git / remote-sync safety
- Remote Git Permission Gate / Permission-Gated Operation
- ChatGPT / Codex repository write boundary
- TASKS unfinished-work queue
- Progressive Repository Reading
- Codex 模型 / reasoning / context / agent 成本控制
- Evidence → Root Cause → Focused Patch → Targeted Validation
- Operational failure taxonomy / retry cap
- Validation Coverage Integrity
- Windows / PowerShell 7 baseline（僅在 repository 使用 `.ps1` 時）
- Research-first / Anti-Reinvent-Wheel Gate
- Hardware evidence 與 target/board portability discipline
- README development transparency / project-scale reporting

## 分享、採用與授權

這份 playbook 是實務工作流，不是任何平台或模型供應商的官方規格。不同帳號、方案或開發工具可能沒有相同的模型名稱、權限機制或 UI；採用時應將概念映射到自己的環境，並以最新官方產品文件與自己的 repository rules 為準。

本 repository 採用 [MIT License](LICENSE)。你可以在 MIT License 條件下使用、修改、分享與再散布本內容；請保留授權文件要求的 copyright 與 permission notice。
