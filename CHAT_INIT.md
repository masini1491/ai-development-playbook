# 新聊天室初始化（New Chat Initialization）

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

## 權威順序（Authority）

一般優先順序：

1. 使用者當次明確指示
2. 實際專案最新 `AGENTS.md` / architecture / security / protocol / hardware evidence / production source of truth
3. 本 playbook
4. 實際專案 `TASKS.md`
5. 舊聊天室、舊 Prompt、cached/local copy、記憶

若兩份同層正式文件互相衝突且無法判定 authority，不得猜；STOP 並指出衝突。

## Prompt 產生關卡（Prompt Generation Gate）

每份 Codex Prompt 必須在前段明確寫出：

- 目標 Repository：`owner/repo`
- 預期 Branch（通常 `main`）
- 推薦模型
- 推理強度
- 推薦理由
- 是否值得先用較便宜模型做前置蒐證
- 必要時 Context 建議 / Execution mode

不得只寫「門禁」「Yale」「後端」等可能和其他 repository 混淆的模糊名稱。

## 跨聊天室回報時間戳（Reporting timestamp）

ChatGPT 在本工程聊天室中的正式專案分析、review、GitHub 讀取結果、Prompt 規劃與 completion/STOP 回報，最後一行應附：

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

這個時間戳只用於跨聊天室 freshness / ordering，不取代 repository HEAD、commit SHA、diff、validation evidence 或 `TASKS.md` state。不要只用「剛剛」、「今天」、「稍早」等相對時間。Codex 的對應規則見 `CODEX_PROMPT_RULES.md`。

## Repository 身分確認關卡（Repository Identity Gate）

任何 Codex 執行在讀取、修改、build、test 或 Git mutation 前，先確認 working repository 與 Prompt 的 `owner/repo` 完全一致。

至少確認：

- repository root
- origin remote identity
- current branch
- current HEAD
- 必要時 repository-specific sentinel file / structure

若 detected repository 與 expected repository 不一致：立即 STOP；回報 expected/detected repository、branch、HEAD；不得修改、不得自行切換/clone repo、不得把 Prompt 套到相似專案。

## Workspace／Remote 權限關卡（Workspace / Remote Permission Gates）

若 Stage 需要修改 repository，Codex 在 file mutation 前確認 workspace 具備最小必要寫入能力；read-only workspace 對 write-required Stage 必須 STOP 或主動要求 workspace-write capability，不得進入 coding loop。

Remote Git operation 若 runtime 已知需要 sandbox/network/repository-metadata permission，應先主動要求最小權限；若事前未知，第一次明確 permission denial 後轉 Permission-Gated Operation。Permission approval 只解除原 operation 的 gate，不等於額外 Git mutation authorization。

詳細規則見 `REPOSITORY_EXECUTION.md`。

## ChatGPT／Codex 寫入分工

對一般 project repository：

- ChatGPT 只直接讀寫 root `TASKS.md`；其他 path 一律唯讀。
- 非 `TASKS.md` 修改由 Codex 在使用者明確授權的 Task / Stage scope 內執行。
- `TASKS.md` 由 ChatGPT 與 Codex 共同維護；Completed 不保留，完成紀錄以 Git history 為準。

`masini1491/ai-development-playbook` 本身是例外：它是共通規則來源，由 ChatGPT 直接維護，Codex 預設唯讀。

## 共通成本原則

> 選擇能安全完成目前授權工作所需的最低成本模型、推理強度、Context、Agent 數量與 Validation scope。

先降低不確定性，再提高模型成本。

## Windows／PowerShell 基準（baseline）

本機互動式開發環境若以 Windows 為主：repository 只要使用自有 `.ps1`，正式 PowerShell runtime 應使用 PowerShell 7 / `pwsh`，不得 silent fallback 至 Windows PowerShell 5.1 / `powershell.exe`。詳細規則見 `TOOLCHAIN.md`。

## TASKS.md

對一般 project repository，`TASKS.md` 是 active unfinished-work / executable scoped Prompt queue，不是 changelog。

只有需要未來再次記住、追蹤或執行的工作才進 queue。一次性、已知位置、低風險且沒有後續追蹤價值的小 maintenance 可以直接用最低成本短 Prompt 處理。

完成工作以 Git history 為準；已完成項目從 TASKS 移除，不建立 Completed 區段。

## 除錯／驗證（Debug / Validation）

預設工作流：

`Evidence → Root Cause → Focused Patch → Targeted Validation`

Root cause 只使用：

- `CONFIRMED ROOT CAUSE`
- `HIGH-CONFIDENCE LIKELY ROOT CAUSE`
- `INSUFFICIENT OBSERVABILITY`

第三類不得猜測式 patch；先取得最小 observability 或 STOP。
