# AI 協作開發實戰手冊（AI Development Playbook）

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本儲存庫只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密協定、客戶資料或其他專案機密。

## 本實戰手冊的維護方式

`masini1491/ai-development-playbook` 是共通規則來源，與一般產品／韌體儲存庫不同：

- 本儲存庫由 **ChatGPT 直接維護**規則與文件。
- Codex／程式開發代理（coding agent）對本儲存庫預設唯讀，只需要讀取並遵守，不參與修改。
- 本儲存庫若暫時出現 `TASKS.md`，只代表 ChatGPT 尚未完成的實戰手冊維護事項，不是 Codex 執行佇列。

這是本實戰手冊的**維護例外**；一般專案儲存庫仍採下方的 ChatGPT／Codex 分工。

## 核心原則

> 先取得最低充分證據（Evidence），再使用最低充分上下文（Context）、模型（Model）、推理強度（Reasoning）、Agent 與驗證範圍（Validation scope）；只有證據證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通手冊管「怎麼開發」；各實際專案儲存庫管「系統是什麼」。

因此若本手冊與實際專案的 `AGENTS.md`、架構、安全規則、協定、硬體證據或正式可信來源（source of truth）衝突，以實際專案的正式規則為準；若與使用者當次明確指示衝突，依使用者當次指示處理。

## 預設協作模型：以 GitHub 為核心的工作流程

本手冊預設以 **GitHub 儲存庫協作**：

- GitHub `main`（或專案明確指定的預設分支）是目前可信來源（current source of truth）。
- 儲存庫根目錄的 `AGENTS.md` 保存穩定、長期的專案治理規則。
- 儲存庫根目錄的 `TASKS.md` 是 ChatGPT／Codex 共用的**進行中未完成工作／可執行限定範圍 Prompt 佇列**，不是一般變更紀錄或永久待辦清單。
- 阻塞（Blocked）、延後（Deferred）、待驗證（Pending-validation）或其他尚未完成的工作可留在 `TASKS.md`；成功完成並驗證後應移除對應項目。
- 已完成工作的永久紀錄以 Git 提交／歷史為準，不在 `TASKS.md` 建立 Completed 區段。

### 一般專案儲存庫的寫入分工

- **ChatGPT**：只直接建立、讀取、更新、刪除根目錄 `TASKS.md`；其餘儲存庫路徑一律唯讀。負責研究、需求／架構／規格討論、審查、任務收錄／範圍判斷，以及 Codex Prompt 規劃。
- **Codex／程式開發代理**：在使用者明確授權的 Task／Stage 範圍內修改原始碼、測試、文件、工具與工作流程等非 `TASKS.md` 檔案，並在執行後維護 `TASKS.md` 的狀態、證據與移除作業。
- **`TASKS.md`**：由 ChatGPT 與 Codex 共同維護；本身不授權 Codex 自動開始其他 Stage。

典型流程：

`ChatGPT 讀最新 GitHub → 規劃／更新未完成工作佇列 → Codex 執行 Repository Identity、workspace／permission gates 與安全同步 → 執行指定 Stage → Targeted Validation → 更新 TASKS → commit／push`

如果使用者採用純本機 Git、GitLab 或其他協作平台，可以保留相同治理概念並映射到對應平台；本儲存庫的預設說明與範例以 GitHub 為核心的工作流程為主。

## 跨 Agent 規則對齊（Cross-agent Playbook Alignment）

ChatGPT、Codex 或其他程式開發代理在審查對方的 Prompt、交接（handoff）、STOP 回報、驗證摘要、完成摘要或其他正式工程回報時，若發現其**內容或回報形式與目前最新版手冊不一致**，不要默默沿用，也不要只把文字重新排版後就假設原回報已符合治理規則。

先指出具體不一致之處，再依影響程度處理：

- 若只是低風險的呈現／格式不一致，而且不影響儲存庫權威來源、完成聲明、驗證正確性、Stage 授權、寫入邊界、安全／憑證處理、執行期／硬體證據，或下一 Stage 是否可安全開始，可以繼續分析其實質證據；同時應建議對方重新讀取與該不一致直接相關的**最低必要手冊章節**。
- 若不一致會影響上述權威來源、完成、驗證、範圍或安全邊界，不能只修格式後繼續。先依正式儲存庫狀態與驗證證據重建可信狀態，必要時 STOP，再決定是否能繼續目前 Stage。
- 不要求對方為單一不一致完整重掃整份手冊。建議應具體指出：哪個回報／行為不符合、應重讀哪個最低必要章節、重讀後應重新檢查哪個聲明、Stage 或證據。
- 典型路由：儲存庫／Git／TASKS／權限／完成權威 → `REPOSITORY_EXECUTION.md`；除錯／根因／重試／驗證／CI／完成證據 → `DEBUG_VALIDATION.md`；模型／推理／上下文／Agent／回報／成本紀律 → `CODEX_PROMPT_RULES.md`；架構／目標／研究／外部服務權威 → `RESEARCH_ARCHITECTURE.md`；人機 UI／UX／設計系統／互動語意 → `UI_UX.md`；嵌入式／硬體／資源／目標證據 → `EMBEDDED_PROJECTS.md`；工具鏈／環境／長時間建置 → `TOOLCHAIN.md`。
- 跨 Agent 審查的目的不是互相挑格式，而是避免過期治理規則、錯誤完成聲明、範圍漂移、證據膨脹或過期成本策略在不同 ChatGPT／Codex session 與交接之間繼續傳播。

核心原則：**發現對方不符合本手冊時，指出具體不一致並只要求最低必要重讀；若不一致影響權威、範圍、完成或驗證，先重新驗證證據，再繼續工作。**

## 跨聊天室回報時間戳（Cross-chat Reporting Timestamp）

為了在多個專案聊天室、Codex session 與跨聊天室貼回結果時快速判斷哪一份較新，ChatGPT 與 Codex 的**正式工程結果回報**應在最後一行附上絕對時間戳。

預設格式：

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

原則：

- 使用絕對日期時間；不要只寫「剛剛」、「今天」、「稍早」。
- 預設時區為 `Asia/Taipei`；若使用者當次明確指定其他時區，改用指定時區並標示。
- 時間戳表示**該份回報產生／完成的時間**，只用於新舊判斷與排序；不是提交時間、Git 權威、驗證事件時間或裝置／伺服器時間。
- 時間戳不得取代儲存庫身分、分支、HEAD／commit、diff、驗證證據、TASKS 狀態或其他正式完成證據。
- ChatGPT 的專案分析、審查、Prompt、GitHub 讀取結果與實戰手冊維護回報應遵守此規則；一般非工程閒聊不要求強制附加。
- Codex 的詳細回報規則見 `CODEX_PROMPT_RULES.md`。

## 專案 `AGENTS.md` → 實戰手冊路由

若多個儲存庫都採用本手冊作為共通基準，建議在各專案根目錄 `AGENTS.md` 保存一份**精簡路由**，讓 Codex／程式開發代理知道共通方法論的權威與最低必要讀取路徑；不要在每個專案複製整份手冊。

核心原則：

- `AGENTS.md` 保存專案專屬治理、正式例外與路由；共通規則仍只由本手冊維護。
- 不要因為 `AGENTS.md` 引用本手冊，就預設每個 Stage 完整掃描本儲存庫；只依目前 Task 讀最低必要章節。
- 專案自己的架構、安全規則、協定、硬體證據與技術可信來源仍高於本手冊；路由不改變權威階層。
- `AGENTS.md` 中的外部儲存庫參照只解決「應讀什麼」，不自動提供網路、檔案系統或憑證存取能力。若執行環境尚未取得手冊內容，依 `REPOSITORY_EXECUTION.md` 的 Permission-Gated Operation 要求最低必要權限。
- 若某方法只在特定工作偶爾需要，而不是跨專案基準，優先考慮按需載入的 Skill／工作流程；不要把所有專門流程都塞進每個 `AGENTS.md`。

建議的最小路由範本：

```markdown
## 共通實戰手冊路由

本專案以 `masini1491/ai-development-playbook` 作為共通開發基準。
本 `AGENTS.md` 與本儲存庫的正式技術契約保存專案專屬權威；
若與共通實戰手冊衝突，依既定權威階層處理。

不要完整掃描共通實戰手冊，只依目前 Task 讀最低必要章節：

- Git／儲存庫／權限／外部服務操作
  → `REPOSITORY_EXECUTION.md`
- 除錯／根因／重試／驗證
  → `DEBUG_VALIDATION.md`
- 架構／研究／外部服務權威
  → `RESEARCH_ARCHITECTURE.md`
- 人機 UI／UX／設計系統／互動語意
  → `UI_UX.md`
- 嵌入式／硬體
  → `EMBEDDED_PROJECTS.md`
- Codex 模型／推理／上下文／Agent／Prompt 紀律
  → `CODEX_PROMPT_RULES.md`
- Windows／PowerShell／本機工具鏈契約（需要時）
  → `TOOLCHAIN.md`
```

這份路由是基準探索入口，不要求所有專案 `AGENTS.md` 使用逐字相同措辭；專案專屬規則可以更嚴格，但不應複製共通 policy 造成規則漂移。

## README 開發透明度（README Development Transparency）

公開儲存庫若明顯採用 ChatGPT／Codex 或其他程式開發代理作為主要開發方式，建議 README 精簡說明**人類參與迴路（human-in-the-loop）**的責任分工：

- **人類／開發者（Human / developer）**：需求、產品方向、硬體選擇、現實世界證據、最終核准，以及需要人工完成的驗證。
- **ChatGPT**：研究、架構／規格討論、審查、任務拆分，以及 `TASKS.md`／Codex Prompt 規劃。
- **Codex／程式開發代理**：限定範圍實作、測試、靜態／建置驗證、文件與儲存庫維護。

AI 產生的程式碼／分析不因生成完成、command 成功或 build exit code 0 就自動等於產品已通過驗證；仍應依專案風險完成適當的人類審查、協定／網路／硬體／正式環境驗證。

若 README 提及 OpenAI／ChatGPT／Codex，不應暗示 OpenAI 對專案、產品、硬體或安全決策提供贊助、認證或背書，除非確有正式關係。

## 專案規模報告（Project Scale Reporting）

若 README 或公開文件展示專案規模、LOC 或行數統計：

- 必須說明統計基準，例如 Git tracked files、正式 ref／commit 或其他可重現來源。
- 必須定義統計指標，例如實體行數（physical lines）、邏輯／可執行程式碼行數（logical/executable LOC）、檔案數量等。
- 若是實體行數，需說明是否包含空白行／註解。
- 應說明主要排除項目，例如 `.git`、第三方程式庫、已下載相依套件、建置／快取、產生物。
- 分類方式依儲存庫實際結構定義，不強迫所有專案使用同一分類。

### 決定性計數器觸發條件（Deterministic Counter Trigger）

不要求每個儲存庫都建立 `project-scale.ps1` 或其他 LOC 統計腳本。

只有當 README 長期展示規模統計，而且數字頻繁變動、專案規模使手動計數容易漂移，或同一統計需同步到多個正式文件時，才優先建立由儲存庫自行維護、可重現的決定性計數器。

已有正式計數器的儲存庫，在主要追蹤檔案變更與驗證完成後再更新規模統計；若數字未變，不製造無意義的 README 變更。跨儲存庫 showcase／private→public 同步屬專案專屬規則，不是本手冊的共通要求。

## 新聊天室最短入口

新開專案聊天室時，先讀：

1. [`CHAT_INIT.md`](CHAT_INIT.md)
2. 再依本 README 的路由只讀本次需要的主題文件
3. 最後讀實際目標儲存庫的最新 `AGENTS.md`／`TASKS.md` 與任務相關的正式可信來源

不要為了「熟悉規則」預設完整掃描本儲存庫。

## 文件路由（Routing）

| 情境 | 讀取文件 |
| --- | --- |
| 新聊天室初始化 | [`CHAT_INIT.md`](CHAT_INIT.md) |
| 產生 Codex Prompt、模型／推理／上下文／Agent 成本控制 | [`CODEX_PROMPT_RULES.md`](CODEX_PROMPT_RULES.md) |
| Git 安全、Repository Identity、工作區／遠端權限、TASKS、寫入分工 | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機執行環境、PowerShell 7、工具鏈契約 | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| 除錯、根因、重試、驗證、證據等級 | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術／協定研究、避免重造輪子、架構／目標／能力 | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| 人機 UI／UX、設計系統、互動、無障礙、UI 一致性驗證 | [`UI_UX.md`](UI_UX.md) |
| ESP32／嵌入式／硬體證據／板級設定／診斷工具 | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本實戰手冊本身 | [`AGENTS.md`](AGENTS.md) |

## 建議權威順序（Authority Order）

一般情況建議：

1. 使用者當次明確指示
2. 實際目標儲存庫最新正式治理／技術可信來源
3. 本手冊
4. 實際目標儲存庫 `TASKS.md` 的進行中工作佇列
5. 舊聊天室、舊 Prompt、快取／本機副本、記憶

`TASKS.md` 不得覆蓋更高層的架構、安全規則、協定或硬體證據。

## 適用方式

這不是要求所有儲存庫使用相同 framework、語言、CI 或硬體。它提供的是：

- 儲存庫身分關卡（Repository Identity Gate）
- 工作區寫入能力關卡（Workspace Write Capability Gate）
- Git／遠端同步安全
- 遠端 Git 權限關卡／需授權操作（Remote Git Permission Gate / Permission-Gated Operation）
- ChatGPT／Codex 儲存庫寫入邊界
- TASKS 未完成工作佇列
- 漸進式儲存庫讀取（Progressive Repository Reading）
- Codex 模型／推理／上下文／Agent 成本控制
- 證據 → 根因 → 聚焦修補 → 針對性驗證（Evidence → Root Cause → Focused Patch → Targeted Validation）
- 操作失敗分類／重試上限
- 驗證覆蓋完整性（Validation Coverage Integrity）
- Windows／PowerShell 7 基準（僅在儲存庫使用 `.ps1` 時）
- 研究優先／避免重造輪子關卡（Research-first / Anti-Reinvent-Wheel Gate）
- 人機 UI／UX、設計系統適配與 UI 一致性契約
- 硬體證據與目標／板級可攜性紀律
- README 開發透明度／專案規模報告
- 完成證據防護（Completion Evidence Guard）與跨聊天室回報時間戳
- 跨 Agent 實戰手冊規則對齊／最低必要重讀

## 分享、採用與授權

這份實戰手冊是實務工作流程，不是任何平台或模型供應商的官方規格。不同帳號、方案或開發工具可能沒有相同的模型名稱、權限機制或 UI；採用時應將概念映射到自己的環境，並以最新官方產品文件與自己的儲存庫規則為準。

本儲存庫採用 [MIT License](LICENSE)。你可以在 MIT License 條件下使用、修改、分享與再散布本內容；請保留授權文件要求的著作權與授權聲明。