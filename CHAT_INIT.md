# New Chat Initialization

本檔是新聊天室的最小 bootstrap，不應取代實際專案 repository 的正式規則。

## 啟動順序

新聊天室處理一個工程專案時：

1. 先讀本 playbook 的 `README.md` 與本檔。
2. 依 README routing 只讀本次必要主題文件，不完整掃描 playbook。
3. 明確確認本次**目標 Repository：`owner/repo`**。
4. 讀實際專案最新 `AGENTS.md`、`TASKS.md` 與最少必要正式 source of truth。
5. 若要產 Codex Prompt，遵守 `CODEX_PROMPT_RULES.md` 與 `REPOSITORY_EXECUTION.md`。
6. 若涉及 build/test/toolchain，依需要讀 `TOOLCHAIN.md` 與 `DEBUG_VALIDATION.md`。
7. 若涉及新協議、新硬體、新 SDK 或架構決策，再讀 research/embedded 文件。

## Authority

一般優先順序：

1. 使用者當次明確指示
2. 實際專案最新 `AGENTS.md` / architecture / security / protocol / hardware evidence / production source of truth
3. 本 playbook
4. 實際專案 `TASKS.md`
5. 舊聊天室、舊 Prompt、cached/local copy、記憶

若兩份同層正式文件互相衝突且無法判定 authority，不得猜；STOP 並指出衝突。

## Prompt Generation Gate

每份 Codex Prompt 必須在前段明確寫出：

- 目標 Repository：`owner/repo`
- 預期 Branch（通常 `main`）
- 推薦模型
- 推理強度
- 推薦理由
- 是否值得先用較便宜模型做前置蒐證
- 必要時 Context 建議 / Execution mode

不得只寫「門禁」「Yale」「後端」等可能和其他 repository 混淆的模糊名稱。

## Repository Identity Gate

任何 Codex 執行在讀取、修改、build、test 或 Git mutation 前，先確認 working repository 與 Prompt 的 `owner/repo` 完全一致。

至少確認：

- repository root
- origin remote identity
- current branch
- current HEAD
- 必要時 repository-specific sentinel file / structure

若 detected repository 與 expected repository 不一致：立即 STOP；回報 expected/detected repository、branch、HEAD；不得修改、不得自行切換/clone repo、不得把 Prompt 套到相似專案。

## 共通成本原則

> 選擇能安全完成目前授權工作所需的最低成本模型、推理強度、Context、Agent 數量與 Validation scope。

先降低不確定性，再提高模型成本。

## Windows / PowerShell baseline

本機互動式開發環境若以 Windows 為主：repository 只要使用自有 `.ps1`，正式 PowerShell runtime 應使用 PowerShell 7 / `pwsh`，不得 silent fallback 至 Windows PowerShell 5.1 / `powershell.exe`。詳細規則見 `TOOLCHAIN.md`。

## TASKS.md

`TASKS.md` 是 active unfinished-work / executable scoped Prompt queue，不是 changelog。

只有需要未來再次記住、追蹤或執行的工作才進 queue。一次性、已知位置、低風險且沒有後續追蹤價值的小 maintenance 可以直接用最低成本短 Prompt 處理。

完成工作以 Git history 為準；已完成項目從 TASKS 移除，不建立 Completed 區段。

## Debug / Validation

預設工作流：

`Evidence → Root Cause → Focused Patch → Targeted Validation`

Root cause 只使用：

- `CONFIRMED ROOT CAUSE`
- `HIGH-CONFIDENCE LIKELY ROOT CAUSE`
- `INSUFFICIENT OBSERVABILITY`

第三類不得猜測式 patch；先取得最小 observability 或 STOP。
