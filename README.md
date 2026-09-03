# AI 協作開發實戰手冊（AI Development Playbook）

> **可重用的 AI 工程協作流程（A reusable AI engineering workflow），用於 ChatGPT、Codex 與 GitHub。**
>
> Use GitHub as durable project memory and source of truth, ChatGPT for reasoning and bounded ephemeral execution, and Codex／coding agents for authorized repository implementation — with explicit context, permission, validation, evidence and cost controls.
>
> 以 GitHub 作為**持久化專案記憶（durable project memory）**與**單一事實來源（source of truth）**，由 ChatGPT 負責推理與**有界暫態執行（bounded ephemeral execution）**，Codex／**程式開發代理（coding agents）**負責經授權的儲存庫實作（repository implementation），並明確控制**上下文（Context）**、權限（permission）、驗證（validation）、證據（evidence）與成本（cost）。
>
> **主要文件語言（Primary documentation language）：繁體中文（Traditional Chinese）。**
>
> **術語呈現（Terminology）**：可自然翻譯的技術概念優先採「繁體中文（English）」；產品名、檔名、程式識別符、版本、固定 key／status 與需要精確比對的原文字串保留原文。

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本手冊設計成可由 **AI／代理（agent）**直接從 [`CHAT_INIT.md`](CHAT_INIT.md) 進行**啟動引導（bootstrap）**，並可透過目標專案 `AGENTS.md` 的**薄路由（thin routing）**快速套用到既有 GitHub **儲存庫（repository）**；不需要先把整份手冊載入**上下文（Context）**，也不需要把本 repository 複製進每個專案。

本儲存庫只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密協定、客戶資料或其他專案機密。

> **README 的責任是人類導向總覽（human-facing overview）+ 儲存庫路由器（repository router）。** 詳細**規範契約（normative contract）**由下方對應主題文件作為主要**權威來源（authority）**；AI／agent 的新聊天室最小**啟動引導（bootstrap）**直接使用 [`CHAT_INIT.md`](CHAT_INIT.md)，不要把 README 當成必經中繼站或第二份完整規則集。

## 30 秒開始使用

### 已經有 GitHub 專案

1. 在目標**儲存庫根目錄（repository root）** `AGENTS.md` 宣告 `masini1491/ai-development-playbook` 為**共通基準（common baseline）**，同時保留該專案自己的**治理規則（governance）**／**技術單一事實來源（technical source of truth）**。
2. 新 ChatGPT／AI／**程式開發代理工作階段（coding-agent session）**先讀本 repository 的 [`CHAT_INIT.md`](CHAT_INIT.md)。
3. 讓 AI 依目前**任務（Task）**只載入最低必要 Playbook **章節（section）**，並永遠以目標專案自己的正式規則為優先。

可先放入目標專案 `AGENTS.md` 的最小範本：

```markdown
## 共通 AI Development Playbook

本專案以 `masini1491/ai-development-playbook` 作為共通 AI 開發基準（common baseline）。
新 AI／agent session 先讀該 Playbook 的 `CHAT_INIT.md`，
再依目前 Task 只讀最低必要權威章節（canonical section）。

本專案自己的 `AGENTS.md`、正式技術文件與專案專屬治理（project-specific governance）
保留較高的專案權威；不要把整份 Playbook 無條件載入上下文（Context）。
```

最短概念：

`Project AGENTS.md 宣告共通基準（baseline） → AI 讀 CHAT_INIT → 任務導向權威路由（Task-based canonical routing） → 專案專屬權威（Project-specific authority）優先`

這套導入方式的目的不是「把更多規則塞進**提示詞（Prompt）**」，而是讓 AI 從一個很小的入口開始，按任務只讀需要的規則。

完整可複製骨架見 [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md)。

版本選擇：

- 想持續取得最新規則：追蹤 `main`。
- 想固定**可重現基準（reproducible baseline）**：鎖定（pin）`v0.1.0`。

## 這套 Playbook 解決什麼

它主要處理 **AI 輔助工程（AI-assisted engineering）**常見但容易被忽略的協作問題：

- **上下文工程（Context engineering）**：常駐載入（Always-on）／熱區（Hot）／冷區（Cold）／證據（Evidence）／歷史（Historical）分層，避免每次工作都載入整個**儲存庫記憶（repository memory）**。
- **代理治理（Agent governance）**：把持久化（persistence）、寫入（write）、執行（execution）、預設載入（default-load）的**權威邊界（authority）**分開，不因「AI 看得到」就推導成「AI 可以改／可以做」。
- **儲存庫記憶（Repository memory）**：以 GitHub **目前權威狀態（current canonical state）**保存可追溯專案記憶，避免只依賴舊聊天室或模型 memory。
- **任務路由（Task routing）**：從 `CHAT_INIT.md` 進入，依 task 直達最低必要**權威主責（canonical owner）／章節（section）**。
- **驗證與證據（Validation & evidence）**：區分**確定性檢查器（deterministic checker）**、**行為評估（behavioral evaluation）**、執行環境（runtime）／硬體（hardware）／正式環境（production）證據，以及**完成狀態回讀（completion read-back）**。
- **成本感知執行（Cost-aware execution）**：證據（Evidence）→ 上下文（Context）→ 模型（Model）→ 推理（Reasoning）→ 代理（Agent）→ 驗證（Validation），只有證據顯示不足時才逐級擴張。
- **暫態運算（Ephemeral compute）**：當既有**確定性工作負載（deterministic workload）**值得執行時，ChatGPT 可在受控**沙盒（sandbox）**進行**有界運算（bounded computation）**，但不因此取得 GitHub 寫入權。

## 這套 Playbook 的護城河（Core differentiators）

這套實戰手冊不試圖取代**代理執行環境（agent runtime）**、**技能套件（Skills package）**、**規格框架（spec framework）**或**企業合規套件（enterprise compliance suite）**；它真正的差異化，是把 AI 長期使用真實工程 repository 時最容易混淆的**專案記憶（project memory）**、**上下文（Context）**、**權威（authority）**、**證據（evidence）**與**執行成本（execution cost）**放進同一套可路由、可驗證的協作架構。

### 核心定位：面向 AI 的儲存庫資訊架構（Repository Information Architecture for AI）

這套實戰手冊的上位問題不是單純「怎麼寫 Prompt」，而是：**如何把一個真實工程儲存庫（repository）設計成 AI 能長期、安全、低成本重新理解與接續的資訊環境。**

不只是讓 AI「讀得到儲存庫」，而是設計其中的資訊如何被保存、分層、路由、載入與重新建立，使不同聊天室／不同代理（agents）都能以**最低充分上下文（minimum-sufficient Context）**找到目前真正有效的專案狀態。

一句話定位：

> **GitHub 原生 AI 工程控制平面（GitHub-native AI Engineering Control Plane）+ 持久化專案記憶架構（Durable Project Memory Architecture）**
>
> 讓 GitHub 成為 AI 可安全長期使用的**專案記憶（project memory）**與**工程控制平面（engineering control plane）**，並以最低充分上下文（minimum-sufficient Context）、明確權威（authority）、現實世界證據（real-world evidence）與執行成本（execution cost）控制，讓不同聊天室／不同代理（agents）都能重新建立正確的專案狀態。

目前最核心的五個護城河：

1. **面向 AI 的儲存庫資訊架構（Repository Information Architecture for AI）**：GitHub 不只是程式碼儲存（code storage），也不是把文件堆進 repository；資訊依**責任邊界（surface responsibility）**、**檢索意圖（retrieval intent）**、目前權威（current canonical）、協作（coordination）、證據（evidence）與歷史（history）設計，使 repository 能真正成為 AI 的持久化專案記憶與工程控制平面。
2. **上下文本身有生命週期（Context lifecycle）**：常駐載入（Always-on）／熱區（Hot）／冷區（Cold）／證據（Evidence）／目前權威（Current canonical）／歷史（Historical）各有不同載入責任；資訊被保存，不代表每個任務（Task）都要付出上下文成本（Context cost）。
3. **保存、載入、修改、執行的權威邊界（authority）分開**：`Persistence ≠ default loading ≠ write ≠ execution`。AI 能看到、能記住或技術上能呼叫工具，都不自動等於已被授權修改或執行。
4. **現實世界證據（Real-world evidence）是一級公民**：軟體／測試通過（software/test PASS）不會自動覆蓋硬體（hardware）、測試台（bench）、正式環境（production）或使用者觀察（user-observed）證據；特別適合包含實體設備、嵌入式與現場驗證的工程專案。
5. **最低充分成本（Minimum-sufficient cost）是共同最佳化目標（optimization objective）**：以 `Evidence → Context → Model → Reasoning → Agent → Validation` 控制整條工作流，只在證據顯示不足時逐級擴張，而不是預設使用最大上下文（Context）、最強模型或最多代理（Agent）。

這五點的共同目標不是增加**流程儀式成本（ceremony）**，而是讓 ChatGPT、Codex／**程式開發代理（coding agents）**、GitHub、**專案專屬真實狀態（project-specific truth）**、**未來工作（future work）**、**證據（evidence）**與權限在長期協作中**保持可分辨、可追溯、可安全接續**。

## 核心原則

> 先取得最低充分證據（Evidence），再使用最低充分上下文（Context）、模型（Model）、推理強度（Reasoning）、代理（Agent）與驗證範圍（Validation scope）；只有證據證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通手冊管「怎麼開發」；各實際專案儲存庫管「系統是什麼」。

跨專案 **AI 資訊架構（AI information architecture）**再補一條：

> 儲存庫（Repository）應讓 AI 以最低充分**檢索成本（retrieval cost）**找到唯一、最新、足夠的權威（authority）；資訊被保存，不代表每個任務（task）都要載入，也不代表它可被執行。

若本手冊與實際專案正式**治理規則（governance）／技術單一事實來源（technical source of truth）**衝突，以實際專案為準；若與使用者當次明確指示衝突，依使用者指示處理。

## 預設協作模型：以 GitHub 為核心

本手冊預設以 GitHub 儲存庫協作：

- GitHub `main`（或專案指定預設分支）是**目前單一事實來源（current source of truth）**。
- 根目錄（Root）`AGENTS.md` 保存穩定、長期的**專案治理（project governance）**與**專案專屬例外（project-specific exception）**。
- 根目錄（Root）`TASKS.md` 在預設**單一協作面模式（Single-Surface Mode）**中是**目前熱區協作面（current Hot coordination surface）**，不是**變更紀錄（changelog）**或永久願望清單。
- 專案（Project）可明確**選擇啟用（opt-in）** **冷區登錄表（Cold Registry）**、**熱區任務卷宗（Hot task dossier）**、**去敏證據暫存區（sanitized evidence staging）**；其 AI **載入／責任（loading / responsibility）**由 `AI_CONTEXT.md` 定義，實際 ChatGPT **寫入允許清單（write allowlist）**由 `REPOSITORY_EXECUTION.md` 定義。
- 已完成工作永久紀錄以 Git 歷史（Git history）為準。

### 一般專案儲存庫的高層分工

- **ChatGPT**：研究、需求／架構／規格討論、審查、**協作准入／範圍（coordination admission/scope）**、**有界暫態執行（bounded ephemeral execution）**、Codex **提示詞（Prompt）**規劃與交付、Codex **結果核對（result reconciliation）**。預設直接寫入（Default direct-write）只包含根目錄（root）`TASKS.md`；project 明確 opt-in 後可擴充到列入 allowlist 的 `BACKLOG.md`、Hot task dossier、sanitized evidence staging。
- **Codex／程式開發代理（coding agent）**：在使用者明確授權的**任務／階段（Task／Stage）**範圍內修改原始碼（source）／測試（tests）／文件（docs）／工具（tooling）等允許檔案（allowed files），完成**目標式驗證（targeted validation）**，並依**專案治理（project governance）**完成當次**協作記錄維護（coordination bookkeeping）**。
- **人類／開發者（Human / developer）**：需求、產品方向、現實世界／硬體證據（evidence）、最終核准，以及需要人工完成的驗證。

完整**授權（authorization）**、**權限（permission）**、Git 安全（Git safety）、**協作寫入允許清單（Coordination Write Allowlist）**與**面向儲存庫的文件政策（repository-facing documentation policy）**以 [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) 為權威來源（authority）；Hot／Cold／Evidence／Historical、**路由（routing）**與**檢索成本政策（retrieval-cost policy）**以 [`AI_CONTEXT.md`](AI_CONTEXT.md) 為權威來源（authority）。

典型流程：

`ChatGPT 讀最新 GitHub → 取得最低充分目前上下文（current context） → 持久化／協作准入（persistence/coordination admission） → 必要時進行有界確定性執行（bounded deterministic execution） → 產生最低充分 Codex 交接（handoff） → Codex 身分／權限／安全同步前置檢查（identity/permission/safe-sync preflight） → 執行指定階段（Stage） → 目標式驗證（Targeted Validation） → 協作記錄維護（coordination bookkeeping） → 必要 commit/push → ChatGPT 權威證據核對（canonical evidence reconciliation）`

## 新聊天室最短入口

AI／agent 新開專案聊天室時：

1. **直接讀 [`CHAT_INIT.md`](CHAT_INIT.md)** 建立**儲存庫身分（repository identity）／權威（authority）／任務路由（task routing）**起點；不必先讀或再回到 README。
2. 依最低必要路由選**權威主題（canonical topic）**；大型文件依**章節路由器（Section Router）／標題範圍讀取（heading bounded-read）**，明確目標（exact target）已知時可**直接葉節點略過（direct-leaf bypass）**。
3. 讀目標 repo 最新**治理規則（governance）**、**目前熱區協作面（current Hot coordination surface）**（若 project 採用）與任務直接相關的正式**單一事實來源（source of truth）**；Cold／Evidence／History 不因存在就無條件載入。
4. 若首次**導入（adoption）／工作流程覆核（workflow review）**或已讀範圍出現**具有實質價值的確定性工作負載（material deterministic workload）**，依 `CHATGPT_WORKFLOW.md` 的**執行機會掃描（Execution Opportunity Scan）**判斷是否值得 **ChatGPT 端執行（ChatGPT-side execution）**；不要為了能力盤點完整掃描沙盒（sandbox）。

人類若要了解整套手冊、分享內容或瀏覽主題，可從本 README 進入。

## 文件路由（Routing）

| 情境 | 主要文件 |
| --- | --- |
| 新聊天室最小啟動引導（bootstrap）／AI 任務路由器（task router） | [`CHAT_INIT.md`](CHAT_INIT.md) |
| AI 可讀性、上下文載入（Context loading）、Always-on／Hot／Cold／Evidence／Historical、任務／證據卷宗（task/evidence dossier）、路由（routing）／檢索成本（retrieval cost） | [`AI_CONTEXT.md`](AI_CONTEXT.md) |
| ChatGPT 規劃（planning）、協作准入（coordination admission）、AI 發起的持久工作（AI-originated durable work）、執行機會掃描（Execution Opportunity Scan）／ChatGPT 端執行環境（ChatGPT-side runtime）、Codex 提示詞模式／交付（Prompt mode／delivery）、可直接複製（copy-ready）、結果核對（result reconciliation）、工程回覆呈現／時間戳（presentation／timestamp） | [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) |
| Codex 模型（model）／推理（Reasoning）／上下文（Context）／代理（Agent）、執行模式（execution mode）、用量／成本（usage/cost）、工具排程／輸出（tool scheduling/output）、Codex 回報（reporting） | [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) |
| Git 安全、儲存庫身分（Repository Identity）、工作區／遠端權限（workspace／remote permission）、外部服務操作（external-service operation）、協作寫入允許清單（Coordination Write Allowlist）、ChatGPT／Codex 寫入分工、面向儲存庫的文件（repository-facing documentation） | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機執行環境（runtime）、PowerShell 7、工具鏈契約（toolchain contract） | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| 除錯、根因（root cause）、重試（retry）、CI／建置階段（build phase）、確定性強制檢查（deterministic enforcement）／行為評估（behavioral evaluation）／驗證執行位置（validation execution placement）、驗證（validation）、證據生命週期（evidence lifecycle）、重構證據（refactor evidence） | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術／協定研究、避免重造輪子、架構（architecture）、目標／能力（target/capability）、狀態／生命週期（state/lifecycle）、責任歸屬／重構邊界（ownership/refactor boundary） | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| 人機 UI／UX、任務流程（task flow）、設計系統參考（design-system reference）、互動（interaction）、無障礙（a11y）、國際化（i18n） | [`UI_UX.md`](UI_UX.md) |
| ESP32／嵌入式／硬體、開發板設定檔（board profile）、資源證據（resource evidence）、實體輸出／復原（physical-output/recovery）、測試台／硬體差異（bench/hardware delta） | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本實戰手冊本身 | [`AGENTS.md`](AGENTS.md) |

## 專案 `AGENTS.md` → 實戰手冊路由

若多個 repository 採用本手冊作為**共通基準（common baseline）**，project root `AGENTS.md` 建議只保存**精簡路由與專案專屬例外（project-specific exception）**，不要複製共通**政策（policy）**全文。

```markdown
## 共通實戰手冊路由

本專案以 `masini1491/ai-development-playbook` 作為共通開發基準（common baseline）。
本 `AGENTS.md` 與本儲存庫正式技術契約保存專案專屬權威；
若與共通實戰手冊衝突，依既定權威順序（authority hierarchy）處理。

不要完整掃描共通實戰手冊，只依目前任務（Task）讀最低必要章節：

- AI 上下文（AI Context）／Hot-Cold-Evidence／路由（routing）／載入效率
  → `AI_CONTEXT.md`
- ChatGPT 規劃（planning）／協作准入（coordination admission）／執行機會掃描（Execution Opportunity Scan）／提示詞交付（Prompt delivery）／結果核對（result reconciliation）
  → `CHATGPT_WORKFLOW.md`
- Codex 模型（model）／推理（Reasoning）／上下文（Context）／代理（Agent）／執行（execution）／成本（cost）／回報（reporting）
  → `CODEX_EXECUTION.md`
- Git／儲存庫／權限／協作寫入允許清單（Coordination Write Allowlist）／寫入邊界
  → `REPOSITORY_EXECUTION.md`
- 除錯／根因／重試／驗證
  → `DEBUG_VALIDATION.md`
- 架構／研究／狀態生命週期（state lifecycle）／責任歸屬（ownership）
  → `RESEARCH_ARCHITECTURE.md`
- 人機 UI／UX／設計系統／國際化（i18n）
  → `UI_UX.md`
- 嵌入式／硬體
  → `EMBEDDED_PROJECTS.md`
- Windows／PowerShell／本機工具鏈（toolchain，需要時）
  → `TOOLCHAIN.md`
```

**專案專屬治理（Project-specific governance）**可以更嚴格；舊路由（routing）或舊責任歸屬（ownership）讀到最新版手冊時做**有界核對（bounded reconciliation）**，不為**向後相容（backward compatibility）**永久保留錯誤主責（owner）。

## 本實戰手冊的維護方式

`masini1491/ai-development-playbook` 是共通規則來源，與一般產品／韌體儲存庫不同：

- 本儲存庫由 **ChatGPT 直接維護**規則與文件。
- Codex／程式開發代理（coding agent）對本儲存庫預設唯讀，只需要讀取並遵守，不參與修改。
- 本儲存庫若暫時出現 `TASKS.md`，只代表 ChatGPT 尚未完成的實戰手冊維護事項，不是 Codex 執行佇列（execution queue）。
- 維護本手冊自身的詳細規則見 [`AGENTS.md`](AGENTS.md)。

一般專案儲存庫仍採本手冊定義的 ChatGPT／Codex 分工，不因本 repository 的維護例外而改變。

## 跨代理規則對齊（Cross-Agent Alignment）

ChatGPT、Codex 或其他**程式開發代理（coding agent）**覆核（review）對方的交接（handoff）／停止（STOP）／驗證（validation）／完成摘要（completion summary）時：

- 先指出具體不一致，只要求重讀直接相關最低必要**權威來源（authority）**；不要完整重掃手冊。
- 低風險格式差異且不影響 authority／scope／completion／validation／security 時，可繼續實質分析。
- 影響**儲存庫權威（repository authority）**、任務／階段範圍（Task/Stage scope）、寫入邊界（write boundary）、完成（completion）、驗證（validation）、安全／憑證（security／credential）或硬體／執行環境證據（hardware/runtime evidence）時，先依**權威證據（canonical evidence）**重建可信狀態（trusted state），必要時 STOP。

## 跨聊天室回報時間戳

- ChatGPT 完整工程回覆：`CHATGPT_WORKFLOW.md`
- Codex **面向使用者回覆／送出前回報（user-facing reply / pre-send reporting）**：`CODEX_EXECUTION.md`

預設分別：

`回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

時間戳只協助**時效性／順序（freshness / ordering）**，不取代 repository HEAD、commit、diff、驗證證據（validation evidence）或目前協作狀態（current coordination state）。

## 面向儲存庫的文件（Repository-facing Documentation）與專案規模

公開 README 若說明 **AI 輔助開發（AI-assisted development）**、驗證（validation）、LOC／行數／檔案數等**宣稱（claim）**，應使用可重現的**權威證據（canonical evidence）**，且不得把 AI 產出或建置通過（build PASS）誇大為更高**證據等級（evidence tier）**。

**專案規模分類（Project-scale classification）**應依資訊責任而非單純副檔名；`TASKS`、`BACKLOG`、**當前任務卷宗（active task dossier）**、**證據收件匣（evidence inbox）**、**封存／歷史（archive/history）**等**作業記憶（operational memory）**若不屬該**衡量指標（metric）**語意，不應只因是 Markdown 就被混入**權威技術文件規模（canonical technical documentation scale）**。完整規則見 `REPOSITORY_EXECUTION.md` 與 `AI_CONTEXT.md` 的 **衍生中繼資料寫入閉合關卡（Derived Metadata Write-Closure Gate）**。

## 建議權威順序

一般情況：

1. 使用者當次明確指示
2. 實際目標 repository 最新正式**治理規則／技術單一事實來源（governance / technical source of truth）**
3. 本手冊
4. 實際目標 repository **目前熱區協作契約（current Hot coordination contract）**
5. **冷區／候選／歷史材料（Cold/Candidate / historical material）**（只在需要時，且依其原 evidence/decision 判斷）
6. 舊聊天室、舊 Prompt、快取／本機副本（cached/local copy）、memory

若同層正式**權威來源（authority）**衝突且無法判定，STOP 並指出衝突；不要猜測。

## 本手冊涵蓋的主要方法

包括但不限於：**AI 可讀儲存庫上下文架構（AI-readable repository Context architecture）**、**Hot／Cold／Evidence 協作（coordination）**、ChatGPT **專案規劃／提示詞交付（project planning / Prompt delivery）**、**有界暫態執行（bounded ephemeral execution）**、Codex **執行／成本紀律（execution/cost discipline）**、**儲存庫身分／權限關卡（Repository Identity / permission gates）**、**安全 Git 同步（safe Git sync）**、**漸進式讀取（Progressive Reading）**、`Evidence → Root Cause → Focused Patch → Targeted Validation`、**確定性強制檢查／行為評估（deterministic enforcement／behavioral evaluation）**、**失敗／重試紀律（failure/retry discipline）**、**驗證／證據生命週期（validation/evidence lifecycle）**、**工具鏈契約（toolchain contract）**、**先研究／避免重造輪子（research-first / Anti-Reinvent-Wheel）**、**狀態／生命週期完整性（state/lifecycle integrity）**、**責任歸屬／領域抽取（ownership/domain extraction）**、UI／UX／i18n、**嵌入式硬體證據（embedded hardware evidence）**與**開發板可攜性（board portability）**。

不是所有**專案（project）**都需要使用所有規則；依**任務（Task）**與風險只讀、只套用最低必要部分。

## 分享、採用與授權

這份實戰手冊是實務工作流程，不是任何平台或模型供應商的官方規格。不同帳號、方案或工具可能沒有相同模型名稱、權限機制或 UI；採用時將概念映射到自己的環境，並以最新官方產品文件與自己的 repository 規則為準。

本儲存庫採用 [MIT License](LICENSE)。你可以在 MIT License 條件下使用、修改、分享與再散布本內容；請保留授權文件要求的著作權與授權聲明。