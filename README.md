# AI Development Playbook

一套可重用的 **ChatGPT + Codex + GitHub** 協作開發方法論，目標是用最低充分成本完成可驗證、可追溯、可安全接續的工程工作。

本 repository 只保存**跨專案共通方法**，不保存任何特定產品的 GPIO、憑證、私密 protocol、客戶資料或其他專案機密。

## 核心原則

> 先取得最低充分 Evidence，再使用最低充分 Context、Model、Reasoning、Agent 與 Validation scope；只有 evidence 證明不足時才逐級擴張。

另一條同等重要的原則：

> 共通 playbook 管「怎麼開發」；各實際專案 repository 管「系統是什麼」。

因此若本 playbook 與實際專案的 `AGENTS.md`、architecture、security、protocol、hardware evidence 或正式 source of truth 衝突，以實際專案的正式規則為準；若與使用者當次明確指示衝突，依使用者當次指示處理。

## 新聊天室最短入口

新開專案聊天室時，先讀：

1. [`CHAT_INIT.md`](CHAT_INIT.md)
2. 再依本 README 的 routing 只讀本次需要的主題文件
3. 最後讀實際目標 repository 的最新 `AGENTS.md` / `TASKS.md` 與 task-relevant source of truth

不要為了「熟悉規則」預設完整掃描本 repository。

## 文件 Routing

| 情境 | 讀取文件 |
| --- | --- |
| 新聊天室初始化 | [`CHAT_INIT.md`](CHAT_INIT.md) |
| 產生 Codex Prompt、模型/推理/Context/Agent 成本控制 | [`CODEX_PROMPT_RULES.md`](CODEX_PROMPT_RULES.md) |
| Git 安全、Repository Identity、remote sync、TASKS、Permission Gate | [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) |
| Windows、本機 runtime、PowerShell 7、toolchain contract | [`TOOLCHAIN.md`](TOOLCHAIN.md) |
| Debug、root cause、retry、validation、evidence 等級 | [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) |
| 新技術/協議研究、避免重造輪子、architecture/target/capability | [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) |
| ESP32 / embedded / hardware evidence / board profile / diagnostic harness | [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) |
| 維護本 playbook 本身 | [`AGENTS.md`](AGENTS.md) |

## 建議 Authority 順序

一般情況建議：

1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance / technical source of truth
3. 本 playbook
4. 實際目標 repository `TASKS.md` active queue
5. 舊聊天室、舊 Prompt、cached/local copy、記憶

`TASKS.md` 不得覆蓋更高層 architecture / security / protocol / hardware evidence。

## 適用方式

這不是要求所有 repository 使用相同 framework、語言、CI 或硬體。它提供的是：

- Repository Identity Gate
- Git / remote-sync safety
- Permission-Gated Operation
- TASKS unfinished-work queue
- Progressive Repository Reading
- Codex 模型 / reasoning / context / agent 成本控制
- Evidence → Root Cause → Focused Patch → Targeted Validation
- Operational failure taxonomy / retry cap
- Validation Coverage Integrity
- Windows / PowerShell 7 baseline（僅在 repository 使用 `.ps1` 時）
- Research-first / Anti-Reinvent-Wheel Gate
- Hardware evidence 與 target/board portability discipline

## 分享與採用

這份 playbook 是實務工作流，不是任何平台或模型供應商的官方規格。不同帳號、方案或開發工具可能沒有相同的模型名稱、權限機制或 UI；採用時應將概念映射到自己的環境，並以最新官方產品文件與自己的 repository rules 為準。

目前 repository 尚未加入授權條款；公開可閱讀不等於已授權再散布、修改或商用。若要正式讓他人重用，建議日後另行選擇適合的 LICENSE。
