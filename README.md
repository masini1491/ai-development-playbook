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
2. 用單一 explicit declaration 選定目前 Playbook baseline，例如 `Playbook baseline: main`；需要可重現時改成已發布 tag，不要同時宣告多個 active baseline。
3. 新 ChatGPT／AI／**程式開發代理工作階段（coding-agent session）**先讀所選 baseline 的 [`CHAT_INIT.md`](CHAT_INIT.md)。
4. 讓 AI 依目前**任務（Task）**只載入最低必要 Playbook **章節（section）**，並永遠以目標專案自己的正式規則為優先。

可先放入目標專案 `AGENTS.md` 的最小 bootstrap：

```markdown
## 共通 AI Development Playbook

本專案以 `masini1491/ai-development-playbook` 作為共通 AI 開發基準（common baseline）。
Playbook baseline: `main`

新 AI／agent session 先讀所選 Playbook baseline 的 `CHAT_INIT.md`，
再依目前 Task 只讀最低必要權威章節（canonical section）。

本專案自己的 `AGENTS.md`、正式技術文件與專案專屬治理（project-specific governance）
保留較高的專案權威；不要把整份 Playbook 無條件載入上下文（Context）。
```

最短概念：

`Project AGENTS.md 宣告共通基準 + 單一 baseline → AI 讀 CHAT_INIT → 任務導向權威路由（Task-based canonical routing） → 專案專屬權威（Project-specific authority）優先`

這套導入方式的目的不是「把更多規則塞進**提示詞（Prompt）**」，而是讓 AI 從一個很小的入口開始，按任務只讀需要的規則。

上面片段只示範**最小 bootstrap**。若要完成可由 Adoption Doctor deterministic 檢查的 adoption contract，請使用 [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md)，填完 `Project-specific minimum contract`，並保留 project-specific authority 與 no-authority-expansion boundary；不要為了通過 Doctor 把詳細 governance 重複搬進 declaration layer。

版本選擇：

- 想持續取得最新規則：保留 `Playbook baseline: main`。
- 想固定**可重現基準（reproducible baseline）**：把唯一 declaration 改成已發布 tag，例如 `Playbook baseline: v0.1.0`。

### Adoption Doctor

Adoption Doctor 是 read-only／report-only deterministic check，用來檢查目標專案的 Playbook adoption 與 routing contract；它不替代 project-specific semantic review，也不因檢查取得 target repository write authority。

Local Path Mode：

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT GitHub Snapshot Mode：可要求具備 GitHub repository read capability 的 ChatGPT 對指定 canonical repository／branch／ref 執行 Adoption Doctor。ChatGPT 只取得 Doctor active checks 所需的最低充分檔案，在自己的 temporary／ephemeral snapshot 執行同一套 deterministic engine；不需要碰觸由 Codex／human 管理的本機 workspace，也不得把不完整 remote snapshot 造成的 missing-file 診斷誤報成 target repository FAIL。

概念流程：

`GitHub canonical → ChatGPT minimum-sufficient snapshot → adoption_doctor.py → PASS / WARN / FAIL report`

`adoption_doctor.py` 本身仍是 filesystem-based、standard-library、無 GitHub credential／API／write capability；GitHub read 與 snapshot acquisition 屬外部 authorized ChatGPT layer。

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

> 儲存庫（Repository）應讓 AI 以最低充分**檢索成本（retrieval cost）**命中唯一且足夠的目前權威（current authority）；拆檔、index、registry、summary、metadata 或 manifest 都只是手段，不是目標。

## 文件地圖

| 文件 | 用途 |
|---|---|
| `CHAT_INIT.md` | 新聊天室最小 bootstrap + task router |
| `AI_CONTEXT.md` | AI-readable repository information architecture：Always-on / Hot / Cold / Evidence / Current / Historical、Progressive Routing、retrieval cost、routing metadata、write closure |
| `CHATGPT_WORKFLOW.md` | ChatGPT／planning conversation authority：coordination admission、Task contract／最低必要澄清、AI-originated durable work、ChatGPT-side runtime execution、Execution Opportunity Scan、Codex Prompt mode／delivery、copy-ready contract、Codex result reconciliation、session compaction／rehydration、ChatGPT 回覆 presentation contract |
| `CODEX_EXECUTION.md` | Codex／coding agent execution authority：Model / Reasoning / Context / Agent、execution mode、cost / usage、tool scheduling/output、escalation、Codex reporting |
| `REPOSITORY_EXECUTION.md` | Git / repository identity、permission、ChatGPT coordination write allowlist、Codex implementation write boundary、remote write/read-back、repository-facing documentation integrity |
| `DEBUG_VALIDATION.md` | debug、root cause、retry、validation、evidence lifecycle、completion read-back、behavioral evaluation |
| `RESEARCH_ARCHITECTURE.md` | research、target/capability、architecture、state/lifecycle、ownership |
| `EMBEDDED_PROJECTS.md` | embedded / hardware / board-specific workflow |
| `UI_UX.md` | UI / UX / i18n / design-system adaptation |
| `TOOLCHAIN.md` | local toolchain / runtime / PowerShell contract |
| `examples/minimal-project/AGENTS.md` | 最小 project adoption 範例 |

建議讀取順序：

1. 新聊天室先讀 `CHAT_INIT.md`。
2. 再依 task 類型讀 1～2 份必要文件／section。
3. 最後讀實際專案自己的 `AGENTS.md`、current Hot coordination surface 與 task-specific technical source of truth。

## 與實際專案的關係

本手冊只定義共通方法；實際專案仍需自行保存：
- project-specific source of truth
- current task / blocker / evidence
- hardware pinout / protocol specifics
- secrets / deployment values
- release / branch state

實際專案不應把本手冊全文複製進自己的 repository；只需在自己的 `AGENTS.md` 放最小 routing / authority 說明。

## License

MIT
