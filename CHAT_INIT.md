# 新聊天室初始化（New Chat Initialization）

本檔是新聊天室的**AI 最小 bootstrap + task router**。它只負責建立正確的 repository / authority / routing 起點，不重複保存 Git、coordination lifecycle、ChatGPT workflow、Codex execution、AI Context、toolchain、debug 或 validation 的完整規則。

AI／agent 處理實際工程 Task 時，**可直接從本檔進入，不必先讀 `README.md`**。`README.md` 主要服務人類 overview、分享與手冊總覽；只有需要了解整套手冊、routing 無法由本檔判定，或使用者明確要求時再讀。

## 啟動順序

新聊天室處理工程專案時：

1. 明確確認本次**目標 Repository：`owner/repo`**；不要只使用可能對應多個 repository 的模糊名稱。
2. 依本檔「最低必要路由」直接選出本次 Task 所需的 canonical 主題／section；不要為了「熟悉規則」完整掃描整份手冊，也不要把 `README.md` 當必要中繼站。
3. 讀實際目標 repository 最新 `AGENTS.md`／project governance、current Hot coordination surface（若採用）與本次 task 直接相關的最低必要正式 source of truth；Cold、Evidence、History 不因存在就預設載入。
4. 進入大型主題文件後，優先用 heading／symbol／stable pointer 直接命中 relevant section；若檔首有 Section Router，先用 router。Exact target 已唯一命中時可 direct-leaf bypass。
5. Whole-repository capability／gap／absence review：先讀薄 discovery surface `CAPABILITY_INDEX.md`，再依 pointer、`PLAYBOOK_INDEX.json`、合理 owner／repository search 做最低充分 bounded coverage；negative claim 在 final synthesis 前重新 reconciliation。詳細 authority 見 `AI_CONTEXT.md` → `Absence Claim Coverage Gate`。
6. 既有 project 首次採用本手冊，或已讀範圍明確出現 material deterministic execution candidate 時，才做最低充分 Execution Opportunity Scan；候選成立再讀 `CHATGPT_WORKFLOW.md` → `ChatGPT-side Runtime Execution`。
7. 依 project authority 確認目前 Task／Stage 的 scope、permission、evidence 與 validation requirement，再開始分析、產生 Prompt 或執行工作。
8. 若同層正式 authority 衝突、repository identity 不清楚，或 evidence 不足以安全決定下一步，STOP 並指出缺口；不得用舊聊天、cached copy 或 memory 猜補 current authority。

## 最低必要路由

依目前工作選讀：

- ChatGPT planning／task contract／澄清／coordination admission／AI-originated work
  → `CHATGPT_WORKFLOW.md`；依需要直達 `Task Contract：Goal / Context / Exclusions`、`Agent-Normalized Contract／Minimal Clarification Gate`、`Persistence／Coordination Admission`
- 新 repository／pre-implementation 階段由 ChatGPT 蒐集 reference、形成 research synthesis／requirements／architecture，Codex 尚未接手且需要 bounded direct-write
  → `PROJECT_BOOTSTRAP.md`；確認 `research-bootstrap` activation、Research Write Allowlist 與 exit/handoff gate，再依需要讀 `REPOSITORY_EXECUTION.md`
- ChatGPT-side deterministic runtime execution
  → `CHATGPT_WORKFLOW.md` → `ChatGPT-side Runtime Execution`
- Codex Prompt mode／delivery／copy-ready／Codex result reconciliation／ChatGPT user-facing response contract
  → `CHATGPT_WORKFLOW.md`；依對應 heading bounded-read
- AI 可讀性、Context lifecycle、Always-on／Hot／Cold／Evidence／Historical、task/evidence dossier、routing／retrieval cost
  → `AI_CONTEXT.md`；依需要直達 `AI Context Surface Model`、`Independent Retrieval Intent Gate`、`Context Cohesion Gate`、`Progressive Routing／Direct-leaf Bypass`、`AI Readability / Retrieval Cost Change Gate`
- Whole-repository capability discovery／repository-level absence claim
  → 先 `CAPABILITY_INDEX.md`；必要時 `PLAYBOOK_INDEX.json` 做 machine discovery，再讀 `AI_CONTEXT.md` → `Absence Claim Coverage Gate`
- Semantic identity／aggregate container／derived synthesis authority／durable confirmed fact ownership／provenance precision／remote snapshot consistency／search-hit authority-currentness
  → `INFORMATION_INTEGRITY.md`；只讀對應 guard；evidence lifecycle 的其他規則仍由 `DEBUG_VALIDATION.md` 負責
- Codex model／Reasoning／Context／Agent、execution mode、usage／cost、tool scheduling/output、Codex reporting
  → `CODEX_EXECUTION.md`；reporting 直達 `Codex 回報語言`、`Codex 回報時間戳（Always-on Reporting Timestamp）`、`Reporting Pre-Send Gate`，其他只讀 task-relevant section
- Git、Repository Identity、workspace／remote permission、Coordination Write Allowlist、ChatGPT／Codex 寫入分工、repository-facing documentation integrity
  → `REPOSITORY_EXECUTION.md`；先用檔首 `Section Router`
- 除錯、根因、重試、驗證、evidence lifecycle、後續 evidence 與歷史判斷／紀錄 reconciliation
  → `DEBUG_VALIDATION.md`；先用檔首 `Section Router`
- 研究、新技術／協定、architecture、target/capability、state/lifecycle、ownership
  → `RESEARCH_ARCHITECTURE.md`；先用檔首 `Section Router`
- 嵌入式／硬體／板級／硬體驗證差異
  → `EMBEDDED_PROJECTS.md`
- UI／UX／人機互動／i18n／design-system adaptation
  → `UI_UX.md`
- 本機工具鏈、runtime、PowerShell／Windows contract
  → `TOOLCHAIN.md`
- 維護本手冊自身
  → `AGENTS.md` + `AI_CONTEXT.md` → `AI Readability / Retrieval Cost Change Gate`；若建立在 whole-Playbook capability／absence review，先讀 `CAPABILITY_INDEX.md`

若同一 Task 跨兩個主題，只讀真正參與本次 decision／execution／validation 的 sections；Cross-owner review 也不是 full scan 授權，coverage 只擴張到足以支持本次 claim。

## 權威與執行注意

Authority、Repository Identity、ChatGPT／Codex 寫入邊界、coordination lifecycle、AI Context surface semantics、permission gates、ChatGPT Prompt delivery、Codex model／Reasoning、reporting timestamp、PowerShell baseline、root-cause labels 與 validation contract **不在本檔重複定義**。

需要其中任一規則時，讀上方對應 canonical 主題文件；實際專案最新正式 technical/governance source of truth 仍高於本手冊。

核心原則：**新聊天室先建立正確 repository 與 authority，再按問題直達最低必要 current owner／section；whole-Playbook review先用薄 discovery index降低漏讀，再由 canonical owner確認。Bootstrap 不應成為第二份手冊，也不應無條件載入 Cold、Evidence、History或 README。**
