# AI 協作開發實戰手冊（AI Development Playbook）

> **A reusable AI engineering workflow for ChatGPT, Codex and GitHub.**
>
> Use GitHub as durable project memory and source of truth, ChatGPT for reasoning and bounded ephemeral execution, and Codex／coding agents for authorized repository implementation — with explicit context, permission, validation, evidence and cost controls.
>
> **Primary documentation language: Traditional Chinese（繁體中文）.**

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本手冊設計成可由 AI／agent **直接從 [`CHAT_INIT.md`](CHAT_INIT.md) bootstrap**，並可透過目標專案 `AGENTS.md` 的薄路由快速套用到既有 GitHub repository；不需要先把整份手冊載入 Context，也不需要把本 repository 複製進每個專案。

本儲存庫只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密協定、客戶資料或其他專案機密。

> **README 的責任是 human-facing overview + repository router。** 詳細 normative contract 由下方對應主題文件作為主要 authority；AI／agent 的新聊天室最小 bootstrap 直接使用 [`CHAT_INIT.md`](CHAT_INIT.md)，不要把 README 當成必經中繼站或第二份完整規則集。

## 30 秒開始使用

### 已經有 GitHub 專案

1. 在目標 repository root `AGENTS.md` 宣告 `masini1491/ai-development-playbook` 為 common baseline，同時保留該專案自己的 governance／technical source of truth。
2. 新 ChatGPT／AI／coding-agent session 先讀本 repository 的 [`CHAT_INIT.md`](CHAT_INIT.md)。
3. 讓 AI 依目前 Task 只載入最低必要 Playbook section，並永遠以目標專案自己的正式規則為優先。

可先放入目標專案 `AGENTS.md` 的最小範本：

```markdown
## 共通 AI Development Playbook

本專案以 `masini1491/ai-development-playbook` 作為共通 AI 開發基準。
新 AI／agent session 先讀該 Playbook 的 `CHAT_INIT.md`，
再依目前 Task 只讀最低必要 canonical section。

本專案自己的 `AGENTS.md`、正式技術文件與 project-specific governance
保留較高的專案權威；不要把整份 Playbook 無條件載入 Context。
```

最短概念：

`Project AGENTS.md 宣告 baseline → AI 讀 CHAT_INIT → Task-based canonical routing → Project-specific authority 優先`

這套導入方式的目的不是「把更多規則塞進 Prompt」，而是讓 AI 從一個很小的入口開始，按任務只讀需要的規則。

## 這套 Playbook 解決什麼

它主要處理 AI-assisted engineering 常見但容易被忽略的協作問題：

- **Context engineering**：Always-on／Hot／Cold／Evidence／Historical 分層，避免每次工作都載入整個 repository memory。
- **Agent governance**：把 persistence、write、execution、default-load authority 分開，不因「AI 看得到」就推導成「AI 可以改／可以做」。
- **Repository memory**：以 GitHub current canonical state 保存可追溯專案記憶，避免只依賴舊聊天室或模型 memory。
- **Task routing**：從 `CHAT_INIT.md` 進入，依 task 直達最低必要 canonical owner／section。
- **Validation & evidence**：區分 deterministic checker、behavioral evaluation、runtime/hardware/production evidence 與 completion read-back。
- **Cost-aware execution**：Evidence → Context → Model → Reasoning → Agent → Validation，只有證據顯示不足時才逐級擴張。
- **Ephemeral compute**：當既有 deterministic workload 值得執行時，ChatGPT 可在受控 sandbox 進行 bounded computation，但不因此取得 GitHub 寫入權。

## 核心原則

> 先取得最低充分證據（Evidence），再使用最低充分上下文（Context）、模型（Model）、推理強度（Reasoning）、Agent 與驗證範圍（Validation scope）；只有證據證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通手冊管「怎麼開發」；各實際專案儲存庫管「系統是什麼」。

跨專案 AI information architecture 再補一條：

> Repository 應讓 AI 以最低充分 retrieval cost 找到唯一、最新、足夠的 authority；資訊被保存，不代表每個 task 都要載入，也不代表它可被執行。

若本手冊與實際專案正式 governance／technical source of truth 衝突，以實際專案為準；若與使用者當次明確指示衝突，依使用者指示處理。

## 預設協作模型：以 GitHub 為核心

本手冊預設以 GitHub 儲存庫協作：

- GitHub `main`（或專案指定預設分支）是 current source of truth。
- Root `AGENTS.md` 保存穩定、長期的 project governance 與 project-specific exception。
- Root `TASKS.md` 在 default Single-Surface Mode 中是 current Hot coordination surface，不是 changelog 或永久願望清單。
- Project 可明確 opt-in Cold Registry、Hot task dossier、sanitized evidence staging；其 AI loading / responsibility 由 `AI_CONTEXT.md` 定義，實際 ChatGPT write allowlist由 `REPOSITORY_EXECUTION.md` 定義。
- 已完成工作永久紀錄以 Git history 為準。

### 一般專案儲存庫的高層分工

- **ChatGPT**：研究、需求／架構／規格討論、審查、coordination admission/scope、bounded ephemeral execution、Codex Prompt 規劃與交付、Codex result reconciliation。Default direct-write只包含 root `TASKS.md`；project明確 opt-in後可擴充到列入 allowlist的 `BACKLOG.md`、Hot task dossier、sanitized evidence staging。
- **Codex／coding agent**：在使用者明確授權的 Task／Stage 範圍內修改 source/tests/docs/tooling 等 allowed files，完成 targeted validation，並依 project governance維護當次 coordination bookkeeping。
- **Human / developer**：需求、產品方向、現實世界／硬體 evidence、最終核准，以及需要人工完成的驗證。

完整 authorization、permission、Git safety、Coordination Write Allowlist 與 repository-facing documentation policy 以 [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) 為 authority；Hot/Cold/Evidence/Historical、routing與 retrieval-cost policy 以 [`AI_CONTEXT.md`](AI_CONTEXT.md) 為 authority。

典型流程：

`ChatGPT 讀最新 GitHub → 取得最低充分 current context → persistence/coordination admission → 必要時 bounded deterministic execution → 產生最低充分 Codex handoff → Codex identity/permission/safe-sync preflight → 執行指定 Stage → Targeted Validation → coordination bookkeeping → 必要 commit/push → ChatGPT canonical evidence reconciliation`

## 新聊天室最短入口

AI／agent 新開專案聊天室時：

1. **直接讀 [`CHAT_INIT.md`](CHAT_INIT.md)** 建立 repository／authority／task routing 起點；不必先讀或再回到 README。
2. 依最低必要路由選 canonical topic；大型文件依 Section Router/heading bounded-read，exact target明確時可 direct-leaf bypass。
3. 讀目標 repo最新 governance、current Hot coordination surface（若 project 採用）與任務直接相關的正式 source of truth；Cold/Evidence/History 不因存在就無條件載入。
4. 若首次 adoption／workflow review 或已讀範圍出現 material deterministic workload，依 `CHATGPT_WORKFLOW.md` 的 Execution Opportunity Scan 判斷是否值得 ChatGPT-side execution；不要為了能力盤點完整掃描 sandbox。

人類若要了解整套手冊、分享內容或瀏覽主題，可從本 README 進入。

## 文件路由（Routing）

| 情境 | 主要文件 |
| --- | --- |
| 新聊天室最小 bootstrap／AI task router | [`CHAT_INIT.md`](CHAT_INIT.md) |
| AI 可讀性、Context loading、Always-on／Hot／Cold／Evidence／Historical、task/evidence dossier、routing／retrieval cost | [`AI_CONTEXT.md`](AI_CONTEXT.md) |
| ChatGPT planning、coordination admission、AI-originated durable work、Execution Opportunity Scan／ChatGPT-side runtime、Codex Prompt mode／delivery、copy-ready、結果 reconciliation、工程回覆 presentation／timestamp | [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) |
| Codex model／Reasoning／Context／Agent、execution mode、usage/cost、tool scheduling/output、Codex reporting | [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) |
| Git 安全、Repository Identity、workspace／remote permission、external-service operation、Coordination Write Allowlist、ChatGPT／Codex 寫入分工、repository-facing documentation | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機 runtime、PowerShell 7、toolchain contract | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| 除錯、root cause、retry、CI/build phase、deterministic enforcement／behavioral evaluation／validation execution placement、validation、evidence lifecycle、refactor evidence | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術／協定研究、避免重造輪子、architecture、target/capability、state/lifecycle、ownership/refactor boundary | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| 人機 UI／UX、task flow、design-system reference、interaction、a11y、i18n | [`UI_UX.md`](UI_UX.md) |
| ESP32／嵌入式／硬體、board profile、resource evidence、physical-output/recovery、bench/hardware delta | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本實戰手冊本身 | [`AGENTS.md`](AGENTS.md) |

## 專案 `AGENTS.md` → 實戰手冊路由

若多個 repository 採用本手冊作為 common baseline，project root `AGENTS.md` 建議只保存**精簡路由與 project-specific exception**，不要複製共通 policy全文。

```markdown
## 共通實戰手冊路由

本專案以 `masini1491/ai-development-playbook` 作為共通開發基準。
本 `AGENTS.md` 與本儲存庫正式技術契約保存專案專屬權威；
若與共通實戰手冊衝突，依既定 authority hierarchy 處理。

不要完整掃描共通實戰手冊，只依目前 Task 讀最低必要章節：

- AI Context／Hot-Cold-Evidence／routing／載入效率
  → `AI_CONTEXT.md`
- ChatGPT planning／coordination admission／Execution Opportunity Scan／Prompt delivery／結果 reconciliation
  → `CHATGPT_WORKFLOW.md`
- Codex model／Reasoning／Context／Agent／execution／成本／reporting
  → `CODEX_EXECUTION.md`
- Git／儲存庫／權限／Coordination Write Allowlist／寫入邊界
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

Project-specific governance可以更嚴格；舊 routing或舊 ownership讀到最新版手冊時做 bounded reconciliation，不為 backward compatibility 永久保留錯誤 owner。

## 本實戰手冊的維護方式

`masini1491/ai-development-playbook` 是共通規則來源，與一般產品／韌體儲存庫不同：

- 本儲存庫由 **ChatGPT 直接維護**規則與文件。
- Codex／程式開發代理（coding agent）對本儲存庫預設唯讀，只需要讀取並遵守，不參與修改。
- 本儲存庫若暫時出現 `TASKS.md`，只代表 ChatGPT 尚未完成的實戰手冊維護事項，不是 Codex 執行佇列。
- 維護本手冊自身的詳細規則見 [`AGENTS.md`](AGENTS.md)。

一般專案儲存庫仍採本手冊定義的 ChatGPT／Codex 分工，不因本 repository 的維護例外而改變。

## 跨 Agent 規則對齊

ChatGPT、Codex 或其他 coding agent review對方 handoff／STOP／validation/completion summary時：

- 先指出具體不一致，只要求重讀直接相關最低必要 authority；不要完整重掃手冊。
- 低風險格式差異且不影響 authority/scope/completion/validation/security時，可繼續實質分析。
- 影響 repository authority、Task/Stage scope、write boundary、completion、validation、安全／credential或 hardware/runtime evidence時，先依 canonical evidence重建可信 state，必要時 STOP。

## 跨聊天室回報時間戳

- ChatGPT 完整工程回覆：`CHATGPT_WORKFLOW.md`
- Codex user-facing reply / pre-send reporting：`CODEX_EXECUTION.md`

預設分別：

`回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

時間戳只協助 freshness / ordering，不取代 repository HEAD、commit、diff、validation evidence或 current coordination state。

## Repository-facing 文件與專案規模

公開 README若說明 AI-assisted development、validation、LOC／行數／檔案數等 claim，應使用可重現 canonical evidence，且不得把 AI產出或 build PASS誇大為更高 evidence tier。

Project-scale classification 應依資訊責任而非單純副檔名；`TASKS`、`BACKLOG`、active task dossier、evidence inbox、archive/history等 operational memory若不屬該 metric語意，不應只因是 Markdown 就被混入 canonical technical documentation scale。完整規則見 `REPOSITORY_EXECUTION.md` 與 `AI_CONTEXT.md` 的 Derived Metadata Write-Closure Gate。

## 建議權威順序

一般情況：

1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance / technical source of truth
3. 本手冊
4. 實際目標 repository current Hot coordination contract
5. Cold/Candidate / historical material（只在需要時，且依其原 evidence/decision判斷）
6. 舊聊天室、舊 Prompt、cached/local copy、memory

若同層正式 authority 衝突且無法判定，STOP並指出衝突；不要猜測。

## 本手冊涵蓋的主要方法

包括但不限於：AI-readable repository Context architecture、Hot/Cold/Evidence coordination、ChatGPT project planning / Prompt delivery、bounded ephemeral execution、Codex execution/cost discipline、Repository Identity / permission gates、safe Git sync、Progressive Reading、Evidence → Root Cause → Focused Patch → Targeted Validation、deterministic enforcement／behavioral evaluation、failure/retry discipline、validation/evidence lifecycle、toolchain contract、research-first / Anti-Reinvent-Wheel、state/lifecycle integrity、ownership/domain extraction、UI/UX/i18n、embedded hardware evidence 與 board portability。

不是所有 project 都需要使用所有規則；依 Task 與風險只讀、只套用最低必要部分。

## 分享、採用與授權

這份實戰手冊是實務工作流程，不是任何平台或模型供應商的官方規格。不同帳號、方案或工具可能沒有相同模型名稱、權限機制或 UI；採用時將概念映射到自己的環境，並以最新官方產品文件與自己的 repository 規則為準。

本儲存庫採用 [MIT License](LICENSE)。你可以在 MIT License 條件下使用、修改、分享與再散布本內容；請保留授權文件要求的著作權與授權聲明。
