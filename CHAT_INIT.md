# 新聊天室初始化（New Chat Initialization）

本檔是新聊天室的**最小 bootstrap**。它只負責建立正確的 repository / authority / routing 起點，不重複保存 Git、TASKS、Prompt、toolchain、debug 或 validation 的完整規則。

詳細方法以 `README.md` 路由到的主題文件為準。

## 啟動順序

新聊天室處理工程專案時：

1. 明確確認本次**目標 Repository：`owner/repo`**；不要只使用「門禁」、「後端」、「Yale」等可能對應多個 repository 的模糊名稱。
2. 讀本手冊的 `README.md`，依 task topic 只選最低必要主題文件；不要為了「熟悉規則」完整掃描整份手冊。
3. 讀實際目標 repository 最新 `AGENTS.md`、`TASKS.md`（若存在）與本次 task 直接相關的最低必要正式 source of truth。
4. 依 project authority 與本手冊 routing 確認目前 Task / Stage 的 scope、permission、evidence 與 validation requirement，再開始分析、產生 Prompt 或執行工作。
5. 若發現同層正式 authority 衝突、repository identity 不清楚，或目前 evidence 不足以安全決定下一步，STOP 並指出實際缺口；不要用舊聊天、cached copy 或 memory 猜測補齊。

## 最低必要路由

依目前工作選讀：

- Codex Prompt、模型／推理／Context／Agent／成本
  → `CODEX_PROMPT_RULES.md`
- Git、Repository Identity、workspace／remote permission、TASKS、寫入分工、repository-facing documentation integrity
  → `REPOSITORY_EXECUTION.md`
- 除錯、根因、重試、驗證、evidence lifecycle
  → `DEBUG_VALIDATION.md`
- 研究、新技術／協定、architecture、target/capability、ownership
  → `RESEARCH_ARCHITECTURE.md`
- 嵌入式／硬體／板級／硬體驗證差異
  → `EMBEDDED_PROJECTS.md`
- UI／UX／人機互動／i18n／design-system adaptation
  → `UI_UX.md`
- 本機工具鏈、runtime、PowerShell／Windows contract
  → `TOOLCHAIN.md`
- 維護本手冊自身
  → `AGENTS.md`

## 權威與執行注意

Authority、Repository Identity、ChatGPT／Codex 寫入邊界、TASKS lifecycle、permission gates、Codex Prompt 固定欄位、模型／Reasoning 規則、回報時間戳、PowerShell baseline、root-cause labels 與 validation contract **不在本檔重複定義**。

需要其中任一規則時，讀上方對應 canonical 主題文件；實際專案最新正式 technical/governance source of truth 仍高於本手冊。

核心原則：**新聊天室先建立正確 repository 與 authority，再按問題讀最低必要規則；bootstrap 不應成為第二份手冊。**