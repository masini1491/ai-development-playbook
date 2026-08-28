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

新開、Branch / Fork、Resume 或跨 session handoff 後，若 Model / Reasoning 會影響成本或能力：

- **只有 execution surface 明確暴露可驗證的 UI / session selection metadata 時**，才在真正執行 repository 工作前核對其是否與目前 Prompt 推薦一致；若 authority 明確顯示不一致，STOP 並請使用者確認／切換。
- 若 agent / runtime **無法觀察 Codex UI selection**，不得把「看不到 UI 設定」本身當成 STOP condition，也不得用模型自我描述、backend/runtime model identity 或其他未建立對應關係的名稱，推定使用者在 UI 選錯 Model / Reasoning。
- 在 UI selection 不可觀察時，以使用者本次 launch 與 Prompt 指定的推薦設定作為操作前提繼續；必要時可提醒使用者自行確認，但不得因此阻塞原本已授權的 Stage。
- 不要假設 parent / previous session 的 model 或 reasoning 設定一定被繼承；這條是**使用者／UI 操作注意事項**，不是要求 agent 具備不存在的 UI introspection capability。

## 回報語言

除非使用者當次另有指定，Codex 的進度、STOP、validation、error explanation、summary 與最終回報一律使用**繁體中文**。

程式碼、identifier、file/path、command、raw log、error string、protocol field、API name、library/tool name 與既有正式技術名詞保持原文；不得為了翻譯而改寫 source semantics、machine contract 或 evidence 原文。

Prompt 不需要為每個 Stage 重複整段語言規則；若 repository governance 已引用本 playbook，通常只需在必要時簡短寫「請使用繁體中文回報」。

## 回報時間戳（Reporting timestamp）

為了讓多個 project chat、Codex session、handoff 與跨聊天室貼回的結果可以直接比較新舊，Codex 的 **STOP、validation summary、completion summary 與最終回報** 最後一行都應附上絕對時間戳。

預設格式：

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

一般原則：

- 使用絕對日期時間，不使用「剛剛」、「今天早上」、「稍早」等相對時間作唯一 freshness marker。
- 預設使用 `Asia/Taipei`；若使用者當次明確指定其他時區，改用該時區並清楚標示。
- 時間戳代表**這份回報產生／完成的時間**，不是 commit time、device time、server event time 或 validation evidence 發生時間；這些若重要應各自保留原始時間來源。
- 不因加入時間戳而省略 commit SHA、branch、validation evidence、TASKS state 或其他 completion evidence；時間戳只協助判斷回報新舊，不是 repository authority。
- 若 execution environment 無法取得可信的目前時間，不得猜測；明確標記 `回報時間：UNAVAILABLE`，並保留其他 canonical completion evidence。

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

## Usage window-aware execution budgeting

若目前使用方案同時存在短期 usage window、週期性／較長期 usage budget、purchased credits 或其他多層 resource constraint，應把它們視為**不同的成本邊界**，不要只看單一總額度。

Condition-triggered 原則：

- 不把任何特定方案名稱、5-hour/weekly 數字、模型 credit rate 或 promotional pricing 寫成穩定 baseline；這些 volatile product facts 以當下官方 Rate Card / Help Center / product UI 為準。
- 若存在短期 window，大型工作應避免把低價值 discovery、重複 repo-wide exploration、無效 retry、非必要 full regression、verbose tool output 與高成本 reasoning 全集中在同一 window。
- 優先維持 `最低充分 Evidence → 最低充分 Model/Reasoning/Context → Targeted Validation`；不要為了保留短期額度而降低已證明必要的 reasoning 或跳過 required validation。
- 可將可安全分離的 workstream 分階段執行，例如先用較便宜模型取得 bounded evidence，再啟動較昂貴 implementation/architecture Stage；但不得只為避開 usage window 人為切碎具有共同 state / root cause / transaction boundary 的工作。
- 若當前產品沒有短期 window 或類似限制，本節不增加額外 execution ceremony。

### Product / Billing Authority Separation（產品／計費 Authority 分離）

涉及 pricing、credits、usage limits、model availability、promotional pricing 或其他 volatile product fact 時，不得只比較數字新舊；先確認每份 authority 的實際適用 scope：

`產品／功能 → 方案／workspace → metering / billing mode → 適用期間`

一般原則：

- 多份官方文件出現不同費率或限制時，優先使用**明確針對目前產品／功能、方案與 metering mode 的最新專用 authority**；不得把其他 ChatGPT feature、workspace、API、legacy metering、不同 billing mode 或不同方案的數字直接交叉套用。
- 專用產品 Rate Card 明確被其他官方頁面引用為該功能 authority 時，以專用 Rate Card 為該功能的主要費率來源；不要因另一份較廣泛 Rate Card 顯示較低或較新的數字就自行覆蓋。
- Included plan usage、purchased credits、usage-based / pay-as-you-go、legacy metering、API billing 等必須分開判斷；名稱相同的 model 不代表各 billing surface 使用相同 rate。
- 官方文件無法確定目前帳號／workspace 實際適用版本時，標記為不確定；若 product UI / Usage panel 能提供 account-specific evidence，優先用它確認實際 applicability。不得自行平均、推導、選較便宜的數字或把 promotion 期限延伸成穩定 baseline。
- 本 Playbook只保存 authority-selection 方法，不保存容易變動的固定 rate table；當次成本判斷仍以最新官方 evidence 為準。

核心目標是**降低同一 resource window 裡的浪費，而不是降低必要品質**。

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

## Coverage-sensitive work decomposition（覆蓋敏感工作拆分）

有些工作**單一修改的 reasoning 難度不高，但要求完整覆蓋很多分散 surface**；例如 UI/UX consistency、設定頁 labels/actions、文件一致性、命名／錯誤訊息清理、migration cleanup、重複 API surface 或 verifier coverage。這類工作不能只用「每一項都很簡單」判斷適合一次塞進大型 Prompt。

核心區分：**Model difficulty ≠ Coverage difficulty。**

當漏掉任一 surface 會造成 material inconsistency，而每個 surface 又能安全獨立驗證時，優先縮小 Stage / checkpoint，而不是先升級模型：

`Inventory / bounded evidence → Checkpoint A → Focused implementation → Targeted validation → STOP → Independent coverage reconciliation → Checkpoint B → … → Final closure reconciliation`

一般原則：

- 若修改 surface 尚未完整掌握，可先做一次 bounded read-only inventory；不要讓 implementation session 同時負責大範圍 discovery、修改與 completeness judgment。
- 每個 checkpoint 只處理一個 coherent surface / invariant / operator flow，保留明確 allowed scope、forbidden scope、targeted validation 與 STOP condition。
- Checkpoint 完成後不得因 queue 中還有下一項就自動繼續；先完成 completion evidence，再由 ChatGPT、human 或其他獨立 review pass 依 canonical diff / verifier / current repository evidence 做 coverage reconciliation，必要時修正下一 checkpoint scope。
- Independent review 的價值在於把 **implementation** 與 **completeness judgment** 分離；尤其在完整性無法被 deterministic verifier 全面證明時，不要只靠同一 implementation context 自我宣告「全部處理完」。
- 每個 checkpoint 優先重用仍為 CURRENT 的既有 evidence；除非 material change 使其失效，不因拆 Stage 就機械式重跑 broad build / regression。
- 最後保留一個 bounded closure checkpoint，用來補強 verifier、檢查跨 surface consistency、reconcile remaining gaps 與 completion evidence；closure 不是重新開啟整個 implementation scope。
- Model / Reasoning 應按**各 checkpoint 的實際內在難度與風險**選擇。原始工作很長或 surface 很多，不代表必須從 Luna 升 Terra / Sol；若拆小後 Luna 足夠，就維持較低成本。反之，單一 checkpoint 若涉及 security、state、protocol 或其他高風險 reasoning，仍應正常升級。
- 不要為了符合本規則過度碎片化共享同一 transaction、root cause、state transition 或必須原子完成的工作；拆分只有在能降低 coverage risk 且不破壞 correctness boundary 時才有價值。

核心原則：**Coverage-sensitive work 先縮小 Stage，再考慮升級模型；省的是大 Prompt 中的漏項與返工，不是必要推理。**

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

### 長時間／高頻 Tool Output 紀律（Long-running tool output discipline）

已知會長時間執行、持續顯示 progress/status，或可能產生大量 stdout/stderr 的 command/process，不應預設把全部輸出直接送入 active model Context。

優先在 **command / tool source 層**降低低價值輸出：

1. 若工具原生支援，使用 quiet / silent / no-progress / concise mode。
2. 需要完整紀錄時，將完整 stdout/stderr redirect 到 log/artifact/file，而不是全部即時回送模型。
3. 正常成功路徑先取得 exit status、duration、必要 summary 與少量關鍵 evidence。
4. 失敗時先讀 relevant error、tail、matched region 或 bounded log window；只有 evidence 不足時才逐步擴張。
5. 不要把「讓模型先接收巨量 log，再要求它摘要」當成主要節流方式；最有效的 Context 控制是在輸出進入 active Context 前就抑制不必要內容。

但 output suppression 不得破壞 validation contract：required diagnostics、audit evidence、failure reproduction、security/safety evidence 或 repository formal gate 所需完整 log 應保留在適當 artifact/file 中，並在需要時可被 targeted read。若工具的 quiet mode 會隱藏判斷 PASS/FAIL 所需 evidence，就不要使用該模式或另保留完整 log。

### 異常／失控 Generation STOP Guard（Runaway / Corrupted Generation STOP Guard）

若 agent / model 的輸出本身出現**明顯且持續的 corrupted / runaway generation**，例如大量無意義重複 token、重複 punctuation、失去語意的亂碼、反覆輸出相同段落，或在沒有新增 evidence 的情況下持續重複同一 conclusion / action，應立即 STOP；不得把「繼續讓它輸出看看會不會自行恢復」視為 retry 或 recovery 策略。

一般原則：

- 只針對明顯且持續的異常 generation；單次正常重述、短暫格式重複或合理 recap 不應誤判為 runaway。
- 一旦異常開始，優先停止**模型 generation**，避免繼續累積無價值 Output Tokens / Credits、Context pollution 與錯誤 downstream action。
- STOP 後先保存 working tree / current diff、最後可信的 Git / validation / tool evidence，以及仍在執行的 external process / job 狀態；不要因停止模型輸出而自動假設外部 build/test/process 也已停止。
- 異常開始後新產生的自然語言 conclusion、completion claim、commit/TASKS 敘述或未經 canonical evidence 驗證的 action result，預設視為**不可信**；依 `DEBUG_VALIDATION.md` 的 Completion Evidence Guard 重建 current state。
- 若 external process 仍正常執行，依 `DEBUG_VALIDATION.md` 的 Long-running Operation Supervision 獨立判斷是否 bounded wait / inspect / STOP；不得因 model generation 異常就武斷 kill 正常 process，也不得用 process 尚在跑作為繼續 corrupted generation 的理由。
- Recovery 優先使用新的 bounded session / handoff，只帶入最後可信 evidence、current Git state、必要 diff / log 與未完成 scope；不要把大量 corrupted output 原封不動重新餵進新 Context。
- 若異常發生在 context compaction、長 thread、handoff 或其他 state transition 後，可以記錄相關時間點，但沒有直接 evidence 時不得宣稱 compaction 就是 root cause；使用 `INSUFFICIENT OBSERVABILITY`。

這條同時是成本與正確性 guard：**省的是已失去資訊價值的輸出與錯誤後續工作，不是必要推理。**