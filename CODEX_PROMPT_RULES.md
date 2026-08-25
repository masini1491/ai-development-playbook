# Codex Prompt／成本規則（Codex Prompt / Cost Rules）

## 核心原則

選擇能安全完成目前任務的**最低成本**模型、推理強度、Context、Agent 數量與 Validation scope。

不是選最強模型，而是選最低充分模型。

## Prompt 開頭固定資訊

每份 Codex Prompt 前段至少包含：

- 目標 Repository：`owner/repo`
- 預期 Branch
- 推薦模型：Luna / Terra / Sol
- 推理強度：Low / Medium / High
- 推薦理由：1～3 句
- 是否值得先用較便宜模型做前置蒐證：是/否 + 理由
- 必要時補 Context 建議
- 必要時補 Execution mode

模型與推理強度由使用者在 Codex UI 手動選擇。Codex 不得自行 Luna→Terra→Sol，也不得自行 Low→Medium→High。

## 回報語言

除非使用者當次另有指定，Codex 的進度、STOP、validation、error explanation、summary 與最終回報一律使用**繁體中文**。

程式碼、identifier、file/path、command、raw log、error string、protocol field、API name、library/tool name 與既有正式技術名詞保持原文；不得為了翻譯而改寫 source semantics、machine contract 或 evidence 原文。

Prompt 不需要為每個 Stage 重複整段語言規則；若 repository governance 已引用本 playbook，通常只需在必要時簡短寫「請使用繁體中文回報」。

## Prompt 執行關卡（Prompt execution gates）

對一般 project repository，Codex Prompt 應依任務需要引用 `REPOSITORY_EXECUTION.md` 的共通 gates，而不是每份 Prompt 重複全文：

1. Repository Identity Gate
2. 若 Stage 需要 mutation：Workspace Write Capability Gate
3. Git state / unfinished-operation preflight
4. Remote Git Permission Gate / Permission-Gated Operation
5. safe `git fetch origin` + fast-forward-only sync
6. re-read latest `AGENTS.md` / `TASKS.md`
7. execute scoped Stage
8. Targeted Validation

若 runtime 已知必要 remote operation 需要 permission escalation，Codex 應主動要求最小權限，不要故意先執行已知會失敗的 command。

一般 project repository 的 ChatGPT direct-write authority 只限 root `TASKS.md`；Prompt 中若需要修改其他 path，應由 Codex 在明確授權 scope 內執行。

`masini1491/ai-development-playbook` 本身由 ChatGPT 直接維護，Codex 預設唯讀，不應產生用 Codex 修改 playbook 的 implementation Prompt。

### Repository `AGENTS.md` 已完成 Playbook routing 時

若目標 repository 的最新 `AGENTS.md` 已明確：

- 宣告 `masini1491/ai-development-playbook` 為共通 baseline；
- 保存最低必要的 playbook routing；
- 說明 project-specific authority / exception；
- 要求依 Task 只讀必要章節而非完整掃描；

則後續 Stage Prompt **不必再重複列出整套 playbook 文件或貼上共通規則全文**。

Prompt 只需：

1. 要求先讀最新 project `AGENTS.md`；
2. 依 `AGENTS.md` routing 與本次 Task 讀最低必要 playbook 章節；
3. 保存本次 task-specific evidence / scope / validation / STOP condition。

只有下列情況才應在 Prompt 額外指定某個 playbook 文件：

- `AGENTS.md` 尚未建立 routing；
- routing 不完整或存在 ambiguity；
- 本次 Task 需要一個不容易由 routing 推導的特殊章節；
- 需要明確 freeze 某個 common contract 作為本 Stage 的判斷基準。

`AGENTS.md` routing 只降低重複 Prompt 與 discovery cost，不代表 playbook repository 內容已自動存在於 execution environment。若需要 external access，仍依 Permission-Gated Operation 處理。

## TASKS 收錄／直接短 Prompt（TASKS Admission / Direct Short Prompt）

**產生 Codex Prompt 不代表一定要建立 `TASKS.md`。**

一次性、修改位置與內容／root cause 已知、scope 小、風險低、完成後無追蹤價值，而且不實質影響 behavior、architecture、protocol、security、hardware、persistence、runtime state 或重要 validation state 的 maintenance，通常直接使用最低充分的一次性短 Prompt；不應為了形式先建立 queue item。

這類工作通常可從 **Luna / Low、Context L0→1、Agent 1、Focused patch** 起步，再依實際 evidence 調整。

需要後續追蹤、Blocked / Deferred / Pending-validation、多 Stage、有 dependency / trigger、root cause 未確認、可能接續 implementation、具有 material project/validation effect，或若不記錄便容易遺漏時，才應建立／更新 `TASKS.md`。

完整 Admission threshold 與 lifecycle 以 `REPOSITORY_EXECUTION.md` 為 authority；本節只負責 Prompt-generation routing，不重複維護完整 queue policy。

## 模型分工

### Luna
適合：
- Git / docs / search / 整理
- mechanical patch
- 已知 root cause 的小修
- behavior-preserving refactor
- targeted tests / verifier
- deterministic、contract 已 freeze 的 implementation

### Terra
適合：
- 一般程式開發
- runtime / state ownership
- persistence
- integration / debugging
- hardware-facing logic
- 多個直接相關模組的 bounded reasoning

### Sol
只考慮：
- 高風險跨模組 architecture
- security / authentication / crypto
- 複雜 protocol/state machine
- concurrency / distributed consistency
- 錯誤設計會造成大範圍後果的決策

Repository 很大不是使用 Sol 或 High 的理由。

## 推理強度校準（Reasoning Calibration）

「最低充分 reasoning」應以 evidence 校準，而不是只憑直覺往下壓成本。

對**穩定、可重複、已有代表性 validation/eval** 的工作，可定期比較目前 reasoning 與低一級設定：

- 使用相同或可比較的代表性 task / fixture / validation contract；
- 比較 correctness、required evidence、validation quality 與 task success；
- 只有在必要品質沒有下降時，才把較低 reasoning 升為新的預設；
- 若低一級導致漏讀 contract、錯誤 root cause、驗證不足或需要更多 retry，保留較高 reasoning；
- 不得只為省 Credits 降低已證明必要的 reasoning。

這是**校準既有預設**的方法，不是要求每個 Stage 都先跑一次低一級 reasoning A/B test；不得為了省一次推理成本，反而製造重複 execution 與 validation 浪費。

## 升級處理（Escalation）

Codex 無權自行換模型。達到 escalation condition 時：

1. STOP
2. 保留 evidence handoff
3. 回報目前 root cause / observability 狀態
4. 列出已完成 validation 與 remaining blocker
5. 建議下一模型/推理強度
6. 由使用者決定是否重新 launch

換模型後沿用既有 evidence，不得只因換模型就重新 repo-wide exploration。

## Context

採 Progressive Repository Reading；從最小 Context 開始：

- L0：Git preflight + current error/log/diff + AGENTS/TASKS
- L1：direct symbol / target / test
- L2：caller/callee/owner/direct dependency
- L3：完整 relevant file
- L4：relevant module/directory
- L5：repo-wide

只有 evidence 不足且能說明缺少哪個答案時才能擴張。

不要預設最大 Context、1M context、Fast、Ultra、Max 或 Multi-Agent。

## Agent 數量

預設 1。

只有真正獨立、彼此不共享 root cause，而且平行化有明確成本效益的 workstream 才考慮 Multi-Agent。

不得把加 agent 當作 retry 方法。

## 執行模式（Execution mode）

優先選擇符合 task 的最小模式：

- Read-only evidence
- Focused patch
- Behavior-preserving refactor
- Architecture decision
- Validation-only
- Hardware evidence

不要為了少貼幾次 Prompt 把不同決策階段、implementation、hardware validation 強行打包。

## Scope 擴張不等於模型升級（Scope Expansion ≠ Model Escalation）

任務中發現 out-of-scope 問題：

- 記錄成新的 TASKS item，或
- STOP 並回報

不能因為新問題比較難，就把目前 Stage 自動升成更大的模型/Context/scope。

## 精簡 Prompt（Prompt lean）

穩定規則應放在 repository governance / playbook，不應在每個 Stage 重複全文。

Stage Prompt 只保存：
- target repo
- target stage
- task-specific evidence
- allowed scope
- forbidden scope
- targeted validation
- success/STOP condition

以降低 Context inflation。

### Tool／Skill 暴露面紀律（Tool / Skill Surface Discipline）

若目前 execution surface 可以控制 tools、connectors、MCP、skills 或其他 agent capabilities：

- 只暴露本 Stage 真正需要的能力；
- 避免把無關 tools / connectors / skills 與冗長 description 帶入 Context；
- tool description 應精簡但足以讓 agent 正確判斷何時使用、輸入/輸出邊界與限制；
- 不要為了「可能會用到」預設載入所有 capability。

若目前 surface 不提供 capability filtering / tool trimming，不得為符合此規則而建立額外 workaround、複製工具或改造 task scope。

精簡 Prompt 或 tool surface 後，評估重點不是 Token 單一數字，而是代表性 task 的 task success、correctness、required evidence 與 validation quality 是否維持；若成功率下降或增加 retry / recovery 成本，應恢復必要 Context / capability。
