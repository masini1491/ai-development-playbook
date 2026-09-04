# 新聊天室初始化（New Chat Initialization）

本檔是新聊天室的**AI 最小 bootstrap + task router**。它只負責建立正確的 repository / authority / routing 起點，不重複保存 Git、coordination lifecycle、ChatGPT workflow、Codex execution、AI Context、toolchain、debug 或 validation 的完整規則。

AI／agent 處理實際工程 Task 時，**可直接從本檔進入，不必先讀 `README.md`**。`README.md` 主要服務人類 overview、分享與手冊總覽；只有需要了解整套手冊、routing 無法由本檔判定，或使用者明確要求時再讀。

## 啟動順序

新聊天室處理工程專案時：

1. 明確確認本次**目標 Repository：`owner/repo`**；不要只使用「門禁」、「後端」、「Yale」等可能對應多個 repository 的模糊名稱。
2. 依本檔「最低必要路由」直接選出本次 Task 所需的 canonical 主題文件；不要為了「熟悉規則」完整掃描整份手冊，也不要把 `README.md` 當必要中繼站。
3. 讀實際目標 repository 最新 `AGENTS.md`／project governance、**current Hot coordination surface**（若 project 採用；通常是 `TASKS.md`）與本次 task 直接相關的最低必要正式 source of truth。`BACKLOG`、evidence、archive/history 等 Cold/非預設 surface 不因存在就無條件載入。
4. 進入大型主題文件後，若檔首提供 Section Router / Progressive reading 指示，先定位 relevant heading，只讀該 section 與必要相鄰 dependency；不要因已選到 topic file 就預設載入全文。
5. 若 exact task identity、path、symbol、pointer 已能唯一命中 canonical target，可直接讀 target；router 用於消歧，不是必經 ceremony。
6. 若本次是**既有 project 首次採用本手冊／AI workflow review**，或目前已讀範圍明確出現 repository-owned deterministic validator、parser、calculator、test/tooling 或反覆人工 deterministic 計算流程，先做最低充分 **Execution Opportunity Scan**：只判斷是否存在 material ChatGPT-side execution candidate，不為了能力盤點完整掃描 repository 或 sandbox；只有候選成立時才路由到 `CHATGPT_WORKFLOW.md` 的 `ChatGPT-side Runtime Execution` 並 probe 本次真正需要的 capability。
7. 依 project authority 與本手冊 routing 確認目前 Task / Stage 的 scope、permission、evidence 與 validation requirement，再開始分析、產生 Prompt 或執行工作。
8. 若發現同層正式 authority 衝突、repository identity 不清楚，或目前 evidence 不足以安全決定下一步，STOP 並指出實際缺口；不要用舊聊天、cached copy 或 memory 猜測補齊。

## 最低必要路由

依目前工作選讀：

- ChatGPT 專案聊天室 planning、task contract／最低必要澄清、coordination admission、AI-originated work、Execution Opportunity Scan／ChatGPT-side Runtime Execution、Codex Prompt mode／delivery、copy-ready、Codex result reconciliation、ChatGPT 回覆時間戳
  → `CHATGPT_WORKFLOW.md`；task contract 輸入不完整時優先定位 `Agent-Normalized Contract／Minimal Clarification Gate`
- AI 可讀性、Context loading、Always-on／Hot／Cold／Evidence／Historical、task/evidence dossier、routing/retrieval cost
  → `AI_CONTEXT.md`
- Codex model／Reasoning／Context／Agent、execution mode、usage／cost、tool scheduling/output、Codex reporting
  → `CODEX_EXECUTION.md`
- Git、Repository Identity、workspace／remote permission、Coordination Write Allowlist、ChatGPT／Codex 寫入分工、repository-facing documentation integrity
  → `REPOSITORY_EXECUTION.md`
- 除錯、根因、重試、驗證、evidence lifecycle、後續 evidence 與歷史判斷／紀錄 reconciliation
  → `DEBUG_VALIDATION.md`；涉及新 evidence 是否取代舊 evidence、歷史紀錄是否仍可作 current authority 時優先定位 `Evidence 取代生命週期`
- 研究、新技術／協定、architecture、target/capability、state/lifecycle、ownership
  → `RESEARCH_ARCHITECTURE.md`
- 嵌入式／硬體／板級／硬體驗證差異
  → `EMBEDDED_PROJECTS.md`
- UI／UX／人機互動／i18n／design-system adaptation
  → `UI_UX.md`
- 本機工具鏈、runtime、PowerShell／Windows contract
  → `TOOLCHAIN.md`
- 維護本手冊自身
  → `AGENTS.md` + `AI_CONTEXT.md` 的 Readability / Retrieval Cost Change Gate（涉及規則／routing 結構變更時）

若同一 Task 同時跨兩個主題，只讀真正參與本次 decision / execution / validation 的 sections；不要因跨 topic 就把兩份文件全文都載入。

## 權威與執行注意

Authority、Repository Identity、ChatGPT／Codex 寫入邊界、coordination lifecycle、AI Context surface semantics、permission gates、ChatGPT Prompt delivery、Codex model／Reasoning、reporting timestamp、PowerShell baseline、root-cause labels 與 validation contract **不在本檔重複定義**。

需要其中任一規則時，讀上方對應 canonical 主題文件；實際專案最新正式 technical/governance source of truth 仍高於本手冊。

核心原則：**新聊天室先建立正確 repository 與 authority，再按問題直接路由到最低必要 current surface／section；bootstrap 不應成為第二份手冊，也不應無條件載入 Cold、Evidence、History 或 README。**