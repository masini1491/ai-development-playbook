# AI 協作開發實戰手冊（AI Development Playbook）

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本儲存庫只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密協定、客戶資料或其他專案機密。

> **README 的責任是 overview + router。** 詳細 normative contract 由下方對應主題文件作為主要 authority；不要把 README 當成第二份完整規則集。

## 本實戰手冊的維護方式

`masini1491/ai-development-playbook` 是共通規則來源，與一般產品／韌體儲存庫不同：

- 本儲存庫由 **ChatGPT 直接維護**規則與文件。
- Codex／程式開發代理（coding agent）對本儲存庫預設唯讀，只需要讀取並遵守，不參與修改。
- 本儲存庫若暫時出現 `TASKS.md`，只代表 ChatGPT 尚未完成的實戰手冊維護事項，不是 Codex 執行佇列。
- 維護本手冊自身的詳細規則見 [`AGENTS.md`](AGENTS.md)。

一般專案儲存庫仍採本手冊定義的 ChatGPT／Codex 分工，不因本 repository 的維護例外而改變。

## 核心原則

> 先取得最低充分證據（Evidence），再使用最低充分上下文（Context）、模型（Model）、推理強度（Reasoning）、Agent 與驗證範圍（Validation scope）；只有證據證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通手冊管「怎麼開發」；各實際專案儲存庫管「系統是什麼」。

因此若本手冊與實際專案的 `AGENTS.md`、架構、安全規則、協定、硬體證據或正式可信來源（source of truth）衝突，以實際專案的正式規則為準；若與使用者當次明確指示衝突，依使用者當次指示處理。

## 預設協作模型：以 GitHub 為核心

本手冊預設以 **GitHub 儲存庫協作**：

- GitHub `main`（或專案明確指定的預設分支）是目前可信來源（current source of truth）。
- 儲存庫根目錄 `AGENTS.md` 保存穩定、長期的專案治理與專案專屬例外。
- 儲存庫根目錄 `TASKS.md` 是 ChatGPT／Codex 共用的**進行中未完成工作／可執行限定範圍 Prompt 佇列**，不是 changelog 或永久願望清單。
- 已完成工作的永久紀錄以 Git history 為準。

### 一般專案儲存庫的高層分工

- **ChatGPT**：研究、需求／架構／規格討論、審查、TASKS admission/scope、Codex Prompt 規劃與交付、Codex result reconciliation；對一般 project repository 預設只直接寫 root `TASKS.md`。
- **Codex／coding agent**：在使用者明確授權的 Task／Stage 範圍內修改 source/tests/docs/tooling 等 allowed files，完成 targeted validation，並依規則維護 `TASKS.md` 狀態。
- **Human / developer**：需求、產品方向、現實世界／硬體 evidence、最終核准，以及需要人工完成的驗證。

完整 authorization、workspace/remote permission、Git safety、TASKS lifecycle、write boundary 與 repository-facing documentation policy 以 [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) 為 authority。

典型流程：

`ChatGPT 讀最新 GitHub → 規劃／更新未完成工作 → 產生最低充分 Codex handoff → Codex 做 identity／permission／safe-sync preflight → 執行指定 Stage → Targeted Validation → TASKS bookkeeping → 必要的 commit／push → ChatGPT 依 canonical evidence reconciliation`

如果使用者採用純本機 Git、GitLab 或其他協作平台，可以保留相同治理概念並映射到對應平台；本手冊範例以 GitHub 為主要協作模型。

## 新聊天室最短入口

新開專案聊天室時：

1. 先讀 [`CHAT_INIT.md`](CHAT_INIT.md) 建立 repository／authority／routing 起點。
2. 回到本 README 的文件路由，只讀本次 Task 最低必要的主題文件。
3. 讀實際目標儲存庫最新 `AGENTS.md`／`TASKS.md`（若存在）與任務直接相關的正式 source of truth。

不要為了「熟悉規則」預設完整掃描本儲存庫。

## 文件路由（Routing）

| 情境 | 主要文件 |
| --- | --- |
| 新聊天室最小 bootstrap | [`CHAT_INIT.md`](CHAT_INIT.md) |
| ChatGPT 專案聊天室 planning、TASKS admission、Codex Prompt mode／delivery、copy-ready、Codex result reconciliation、ChatGPT 回覆時間戳 | [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) |
| Codex model／Reasoning／Context／Agent、execution mode、usage/cost、tool scheduling/output、Codex reporting | [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) |
| Git 安全、Repository Identity、workspace／remote permission、external-service operation、TASKS、ChatGPT／Codex 寫入分工、repository-facing documentation | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機 runtime、PowerShell 7、toolchain contract | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| 除錯、root cause、retry、CI/build phase、validation、evidence lifecycle、refactor evidence | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術／協定研究、避免重造輪子、architecture、target/capability、state/lifecycle、ownership/refactor boundary | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| 人機 UI／UX、task flow、design-system reference、interaction、a11y、i18n | [`UI_UX.md`](UI_UX.md) |
| ESP32／嵌入式／硬體、board profile、resource evidence、physical-output/recovery、bench/hardware delta | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本實戰手冊本身 | [`AGENTS.md`](AGENTS.md) |

## 專案 `AGENTS.md` → 實戰手冊路由

若多個 repository 採用本手冊作為共通 baseline，建議在各 project root `AGENTS.md` 保存一份**精簡路由**：

```markdown
## 共通實戰手冊路由

本專案以 `masini1491/ai-development-playbook` 作為共通開發基準。
本 `AGENTS.md` 與本儲存庫正式技術契約保存專案專屬權威；
若與共通實戰手冊衝突，依既定 authority hierarchy 處理。

不要完整掃描共通實戰手冊，只依目前 Task 讀最低必要章節：

- ChatGPT planning／TASKS admission／Codex Prompt delivery／結果 reconciliation
  → `CHATGPT_WORKFLOW.md`
- Codex model／Reasoning／Context／Agent／execution／成本
  → `CODEX_EXECUTION.md`
- Git／儲存庫／權限／外部服務操作／TASKS／寫入邊界
  → `REPOSITORY_EXECUTION.md`
- 除錯／根因／重試／驗證
  → `DEBUG_VALIDATION.md`
- 架構／研究／state lifecycle／ownership
  → `RESEARCH_ARCHITECTURE.md`
- 人機 UI／UX／設計系統／i18n
  → `UI_UX.md`
- 嵌入式／硬體
  → `EMBEDDED_PROJECTS.md`
- Windows／PowerShell／本機工具鏈（需要時）
  → `TOOLCHAIN.md`
```

這份 routing 不要求逐字複製；project-specific governance 可以更嚴格，但不要把共通 policy 全文複製進每個 repository 造成 drift。

若 project 仍指向舊版手冊檔名或舊 ownership 結構，讀取最新版手冊時依 project governance 做 bounded reconciliation；不為了 backward compatibility 永久保留 common authority 的錯誤 ownership。

## 跨 Agent 規則對齊

ChatGPT、Codex 或其他 coding agent 在 review 對方的 Prompt、handoff、STOP、validation/completion summary 時，若發現內容與最新版手冊不一致：

- 先指出**具體不一致**，再只要求重讀直接相關的最低必要主題文件；不要要求完整重掃手冊。
- 若只是低風險格式／呈現差異且不影響 authority、scope、completion、validation 或 security，可以繼續分析實質 evidence。
- 若不一致會影響 repository authority、Task/Stage scope、write boundary、completion claim、validation correctness、安全／credential 或 hardware/runtime evidence，先依 canonical repository / validation evidence 重建可信狀態，必要時 STOP，再繼續。

詳細判斷由上方對應主題文件的 canonical policy 決定；README 不重複其全文。

## 跨聊天室回報時間戳

ChatGPT 與 Codex 的時間戳**分 owner 維護**：

- ChatGPT 完整工程回覆：`CHATGPT_WORKFLOW.md`
- Codex STOP／validation／completion／final report：`CODEX_EXECUTION.md`

預設格式分別為：

`回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

時間戳只協助 freshness / ordering，不取代 repository HEAD、commit、diff、validation evidence 或 TASKS state。各專案如有不同時區或 reporting contract，以 project/user authority 為準。

## Repository-facing 文件與專案規模

公開 README 若說明 AI-assisted development、人類參與迴路、validation 狀態、LOC／行數／檔案數等 project claim，應使用可重現的 canonical repository evidence，且不得把 AI 產出、command success 或 build PASS 誇大為更高層 validation。

完整的 **AI-assisted development transparency、Project Scale Reporting、Deterministic Counter Trigger 與 canonical evidence** 規則集中於 [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md)；本 README 不再維護第二份 policy。

## 建議權威順序

一般情況：

1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance / technical source of truth
3. 本手冊
4. 實際目標 repository `TASKS.md` 的進行中工作佇列
5. 舊聊天室、舊 Prompt、cached/local copy、memory

若同層正式 authority 衝突且無法判定，STOP 並指出衝突；不要猜測。

## 本手冊涵蓋的主要方法

包括但不限於：ChatGPT project-conversation planning / Prompt delivery、Codex execution/cost discipline、Repository Identity / permission gates、safe Git sync、TASKS lifecycle、Progressive Repository Reading、Evidence → Root Cause → Focused Patch → Targeted Validation、failure/retry discipline、validation coverage/evidence lifecycle、toolchain contract、research-first / Anti-Reinvent-Wheel、state/lifecycle integrity、ownership admission / progressive domain extraction、UI/UX/i18n、embedded hardware evidence 與 board portability。

不是所有 project 都需要使用所有規則；依 Task 與風險只讀、只套用最低必要部分。

## 分享、採用與授權

這份實戰手冊是實務工作流程，不是任何平台或模型供應商的官方規格。不同帳號、方案或開發工具可能沒有相同的模型名稱、權限機制或 UI；採用時應將概念映射到自己的環境，並以最新官方產品文件與自己的 repository 規則為準。

本儲存庫採用 [MIT License](LICENSE)。你可以在 MIT License 條件下使用、修改、分享與再散布本內容；請保留授權文件要求的著作權與授權聲明。