# Codex 執行／成本規則（Codex Execution / Cost Rules）

本檔是 **Codex／coding agent execution** 的主要 authority，負責 model / reasoning / Context / Agent / execution mode、cost / usage budgeting、tool scheduling/output discipline、escalation、Codex reporting 與 execution-side resource control。

ChatGPT 如何做 TASKS admission、選 Prompt mode、產生／交付 copy-ready Prompt、review Codex result 與自己的回覆時間戳，改由 `CHATGPT_WORKFLOW.md` 維護。

## 核心原則

選擇能安全完成目前任務的**最低成本**模型、推理強度、Context、Agent 數量與 Validation scope。

不是選最強模型，而是選最低充分模型。

本檔大部分章節仍依 Task 做 Progressive Reading；但 **Codex user-facing reporting contract 是 always-on cross-cutting contract**。只要 project `AGENTS.md`／正式 routing 已把 Codex reporting 指向本檔，每個 Codex execution 都至少必須取得本檔的「Codex 回報語言」、「Codex 回報時間戳」與「Reporting Pre-Send Gate」規則，再依 Task 讀其他最低必要章節。不得因本次工作只是 MQTT、BLE、文件、maintenance、validation 或其他特定 domain，就把 reporting contract 判成無關而跳過。

模型與推理強度由使用者在 Codex UI 手動選擇。Codex 不得自行 Luna→Terra→Sol→Astra，也不得自行 Low→Medium→High。

新開、Branch / Fork、Resume 或跨 session handoff 後，若 Model / Reasoning 會影響成本或能力：

- 只有 execution surface 明確暴露可驗證的 UI / session selection metadata 時，才在真正執行 repository 工作前核對其是否與目前 Prompt 推薦一致；若 authority 明確顯示不一致，STOP 並請使用者確認／切換。
- 若 agent / runtime 無法觀察 Codex UI selection，不得把「看不到 UI 設定」本身當成 STOP condition，也不得用模型自我描述、backend/runtime model identity 或其他未建立對應關係的名稱，推定使用者在 UI 選錯 Model / Reasoning。
- 在 UI selection 不可觀察時，以使用者本次 launch 與 Prompt 指定的推薦設定作為操作前提繼續；必要時可提醒使用者自行確認，但不得因此阻塞原本已授權 Stage。
- 不假設 parent / previous session 的 model 或 reasoning 設定一定被繼承。

## Codex 回報語言

除非使用者當次另有指定，Codex 的**實質 user-facing 回覆**一律使用**繁體中文**，包括 analysis conclusion、progress conclusion、STOP、permission/blocker explanation、validation、error explanation、summary、completion 與 final report。

程式碼、identifier、file/path、command、raw log、error string、protocol field、API name、library/tool name 與既有正式技術名詞保持原文；不得為了翻譯改寫 source semantics、machine contract 或 evidence 原文。

純 tool output、command stdout/stderr、execution surface 自動產生的 progress/status UI 不需要為符合本規則另外翻譯或包裝成自然語言回覆。

## Codex 回報時間戳（Always-on Reporting Timestamp）

Codex 的**每一個實質 user-facing 回覆**最後一行都應附上絕對時間戳，而不只限於 STOP、validation、completion 或 final report：

`回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

實質 user-facing 回覆至少包括：

- analysis / architecture / requirement conclusion；
- progress conclusion、目前狀態判斷或下一步決策；
- permission / blocker / STOP explanation；
- validation / error explanation；
- completion summary / final report；
- 其他會被使用者閱讀、跨 session 貼回、比較 freshness 或作為後續 execution 依據的自然語言回覆。

不需要額外時間戳的情況限於：

- execution surface 自動顯示的 tool progress / spinner / status；
- raw command output / log 本身；
- 沒有形成獨立 user-facing message 的內部 tool call 中間狀態。

如果 Codex 已經產生一則獨立、可被使用者看見並據此判斷狀態的自然語言訊息，就視為實質 user-facing reply，不因它被稱為「進度」、「中間說明」或「不是 final」而免除時間戳。

一般原則：

- 使用絕對日期時間，不用「剛剛」、「今天早上」等相對時間作唯一 freshness marker。
- 預設 `Asia/Taipei`；使用者明確指定其他時區時改用該時區並清楚標示。
- 時間戳代表這份 Codex 回覆產生／完成時間，不是 commit、device、server event 或 validation evidence 發生時間。
- 時間戳不取代 commit SHA、branch、validation evidence、TASKS state 或其他 completion evidence。
- execution environment 無法取得可信目前時間時，不得猜測；標記 `回報時間：UNAVAILABLE`。
- 這是 cross-cutting reporting contract，可由 project governance / playbook routing 啟用；**不要求 ChatGPT 為了 activation 把完整 reporting policy 或固定時間句重複塞進每一份 Codex launch Prompt**。

## Reporting Pre-Send Gate

Reporting policy 被讀取或在 Prompt 中重述，仍不等於最後送出的文字一定符合 contract。對每一個實質 user-facing reply，Codex 在送出前必須對**最終草稿本身**執行一次 bounded pre-send compliance check；這是 reporting contract 的最後一哩 gate，不是新的 project-specific policy。

送出前至少依序確認：

1. **User-facing classification**：本次輸出若會形成使用者可見、可據此判斷狀態或作為後續工作依據的自然語言訊息，就進入本 gate；不得因稱為 progress、intermediate、summary 或非 final 而跳過。
2. **Language check**：最終草稿的自然語言回覆符合本檔「Codex 回報語言」或使用者／project 當次明確覆蓋的 reporting language；技術原文不需翻譯。
3. **Timestamp source check**：使用可信的目前時間產生 absolute timestamp；若 execution environment 無法取得可信目前時間，使用 `回報時間：UNAVAILABLE`，不得猜測、沿用舊時間或保留 `YYYY-MM-DD HH:mm` placeholder。
4. **Final-line check**：檢查最終草稿最後一個非空白行是否為本 contract 要求的 timestamp line，且沒有任何正文、附註、citation、summary 或其他內容出現在其後。
5. **Fail-closed repair**：若 language、timestamp presence、格式或 final-line position 任一項不合格，先修正最終草稿並重新檢查；**未通過 pre-send check 的 user-facing reply 不得送出**。

若 execution surface 原生提供 output validator、response post-processing hook、schema check 或其他可在送出前對最終文字做 deterministic validation 的能力，優先用它執行上述可機械判定項目；若沒有這類能力，仍必須做 bounded final-draft self-check。不得把 model-only self-check 宣稱為平台層 deterministic guarantee，也不得為了單一 timestamp 規則自行建立高複雜度 validator、agent loop 或外部服務。

Pre-Send Gate 只驗證 reporting artifact 是否符合 contract，不證明其中的 Git、validation、completion 或 technical claim 為真；這些仍由 `DEBUG_VALIDATION.md`、`REPOSITORY_EXECUTION.md` 與 project authority 的 canonical evidence 決定。

本 gate 與 Always-on Reporting Timestamp 同屬 `CODEX_EXECUTION.md` 的 canonical Codex-reporting authority。README、`CHATGPT_WORKFLOW.md`、project `AGENTS.md` 與 individual Codex Prompt 只需要 routing/reference，不應複製完整 normative checklist。

核心原則：**先檢查實際要送出的 final draft，再送出；「我已讀過規則」不是 reporting compliance evidence。**

ChatGPT 自己的 reply timestamp 由 `CHATGPT_WORKFLOW.md` 維護，兩者不要混用。

## Prompt execution gates

Codex 對一般 project repository 執行 Prompt 時，依任務需要引用 `REPOSITORY_EXECUTION.md` 的共通 gates：

1. Repository Identity Gate
2. mutation Stage 的 Workspace Write Capability Gate
3. Git state / unfinished-operation preflight
4. Remote Git Permission Gate / Permission-Gated Operation
5. safe `git fetch origin` + fast-forward-only sync
6. re-read latest `AGENTS.md` / `TASKS.md`
7. execute scoped Stage
8. Targeted Validation

若 runtime 已知必要 remote operation 需要 permission escalation，主動要求最小權限，不故意先執行已知會失敗的 command。

一般 project repository 的 ChatGPT / Codex write boundary 與 playbook repository exception 以 `REPOSITORY_EXECUTION.md` 為 authority，本檔不重複維護。

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

### Astra
只在**目前 execution surface 已實際提供**，且 evidence 顯示 Sol 對該高難度 end-to-end task 很可能需要昂貴 retry／返工，或 Astra 的較高成功率／較少 iteration 有合理機會降低整體 task cost 時考慮。

Astra 不作一般 development、repository discovery、grep/find、mechanical patch 或例行 validation 的預設模型。

模型選擇比較的是 **end-to-end task cost / correctness / completion probability**，不是只比較單位 token rate；也不得因 Astra 是最新或最強模型就跳過 Luna → Terra → Sol 的最低充分原則。

Astra 的 availability、credit/token rate、Fast multiplier、Context 與 promotional terms 屬 volatile product facts，每次依當下官方 authority 判斷，不寫死進 Playbook。

因此模型階梯是 **Luna → Terra → Sol → Astra（條件式最高階）**；新增 Astra 不代表把原本適合 Sol 的工作全部上移。

Repository 很大不是使用 Sol／Astra 或 High 的理由。

## 推理強度校準（Reasoning Calibration）

「最低充分 reasoning」應以 evidence 校準，不只憑直覺往下壓成本。

對穩定、可重複、已有代表性 validation/eval 的工作，可定期比較目前 reasoning 與低一級設定：

- 使用相同或可比較的代表性 task / fixture / validation contract；
- 比較 correctness、required evidence、validation quality 與 task success；
- 只有必要品質沒有下降時，才把較低 reasoning 升為新的預設；
- 若低一級導致漏讀 contract、錯誤 root cause、驗證不足或更多 retry，保留較高 reasoning；
- 不得只為省 Credits 降低已證明必要的 reasoning。

這是校準既有預設的方法，不要求每個 Stage 都做 reasoning A/B test。

## Usage window-aware execution budgeting

若目前使用方案同時存在短期 usage window、週期性／較長期 budget、purchased credits 或其他多層 resource constraint，視為**不同成本邊界**，不要只看單一總額度。

Condition-triggered 原則：

- 不把特定方案名稱、固定 window 數字、model credit rate 或 promotional pricing 寫成穩定 baseline；volatile product facts 以當下官方 Rate Card / Help Center / product UI 為準。
- 若官方 authority 顯示同一 account / plan 的多個 supported agentic features 可能共享 included usage allowance、usage-credit balance 或其他 resource pool，評估 Codex usage／credits 消耗時先確認 **resource pool scope 與同帳號 concurrent / recent agentic workloads**；不得把 quota／balance 變化預設全部歸因於目前 Codex thread，也不得在 shared-consumption evidence 尚未排除前直接推論 Codex token efficiency、model multiplier 或 client regression。Supported feature set、共享方式與 account-specific applicability 以最新官方 authority / Usage UI 為準，不把功能清單寫死。
- 對 reset、credit、quota restoration 等 usage-resource action，在建議使用或實際消耗前先確認 resource semantics：additive、replacement、banked、pay-as-you-go 或其他當下官方定義。不得把 reset 一律視為額外額度，也不得在 semantics 未確認時假設 unused allowance 會保留。
- 若存在短期 window，大型工作避免把低價值 discovery、重複 repo-wide exploration、無效 retry、非必要 full regression、verbose tool output 與高成本 reasoning 全集中在同一 window。
- 維持 `最低充分 Evidence → 最低充分 Model/Reasoning/Context → Targeted Validation`；不為保留短期額度降低已證明必要的 reasoning 或跳過 required validation。
- 可安全分離的 workstream 可以分階段執行，但不只為避開 usage window 人為切碎共享同一 state / root cause / transaction boundary 的工作。
- 當產品沒有短期 window 或類似限制時，本節不增加 ceremony。

### Product / Billing Authority Separation

涉及 pricing、credits、usage limits、model availability、promotional pricing 或其他 volatile product fact 時，先確認每份 authority 的適用 scope：

`產品／功能 → 方案／workspace → metering / billing mode → 適用期間`

一般原則：

- 多份官方文件出現不同費率或限制時，優先使用明確針對目前產品／功能、方案與 metering mode 的最新專用 authority。
- 專用產品 Rate Card 被其他官方頁面引用為該功能 authority 時，以專用 Rate Card 為主要費率來源。
- Included plan usage、purchased credits、usage-based / pay-as-you-go、legacy metering、API billing 分開判斷；model 名稱相同不代表各 billing surface rate 相同。
- 無法確定目前 account / workspace 實際適用版本時標記不確定；若 product UI / Usage panel 有 account-specific evidence，優先用它確認 applicability。
- 本手冊只保存 authority-selection 方法，不保存容易變動的固定 rate table。

核心目標是**降低同一 resource window 裡的浪費，而不是降低必要品質**。

## 升級處理（Escalation）

Codex 無權自行換模型。達到 escalation condition 時：

1. STOP
2. 保留 evidence handoff
3. 回報目前 root cause / observability 狀態
4. 列出已完成 validation 與 remaining blocker
5. 建議下一模型／推理強度
6. 由使用者決定是否重新 launch

換模型後沿用既有 evidence，不得只因換模型就重新 repo-wide exploration。

## Progressive Context

採 Progressive Repository Reading；從最小 Context 開始：

- L0：Git preflight + current error/log/diff + AGENTS/TASKS
- L1：direct symbol / target / test
- L2：caller/callee/owner/direct dependency
- L3：完整 relevant file
- L4：relevant module/directory
- L5：repo-wide

只有 evidence 不足且能說明缺少哪個答案時才擴張。

**Progressive Reading 只控制 task-specific Context expansion，不得用來跳過本檔 always-on reporting contract。** 若 project governance 已 routing 到本檔，Codex 每次 execution 都至少取得 reporting contract，再對其他章節維持最低充分讀取。

不要預設最大 Context、1M context、Fast、Ultra、Max 或 Multi-Agent。

## Agent 數量

預設 1。

只有真正獨立、彼此不共享 root cause，而且平行化有明確成本效益的 workstream 才考慮 Multi-Agent。

不得把加 agent 當 retry 方法。

## 執行模式（Execution mode）

優先選 task 的最小模式：

- Read-only evidence
- Focused patch
- Behavior-preserving refactor
- Architecture decision
- Validation-only
- Hardware evidence

不要為了少貼幾次 Prompt 把不同決策階段、implementation、hardware validation 強行打包。

## Scope Expansion ≠ Model Escalation

任務中發現 out-of-scope 問題時，依 project governance / TASKS routing 記錄成新 item 或 STOP 回報；不能因新問題比較難就把目前 Stage 自動升成更大的 model / Context / scope。

## Source readability boundary

Prompt／Context／tool output 的節流規則不延伸到 human-maintained source code。Codex 不得為降低 Token、LOC、diff display 或輸出長度，把 production/test source 壓成多 statement one-liner、做 source minification 或降低既有可讀性。

Behavior-preserving／mechanical Stage 的完整 readability baseline 以 `RESEARCH_ARCHITECTURE.md` 的 Readability Preservation 為 authority。

## Tool／Skill Surface Discipline

若 execution surface 可控制 tools、connectors、MCP、skills 或其他 agent capabilities：

- 只暴露本 Stage 真正需要的能力；
- 避免無關 tools / connectors / skills 與冗長 description 進入 Context；
- tool description 精簡但足以判斷使用時機與輸入／輸出邊界；
- 不為「可能會用到」預設載入所有 capability。

若 surface 不提供 capability filtering / trimming，不為符合本規則建立額外 workaround、複製工具或改造 task scope。

## Independent Tool Scheduling Discipline

對已確認彼此獨立、read-only、conflict-free，且不需要依前一結果做 adaptive decision 的 tool checks，若 execution surface 原生支援安全 batch／parallel，優先在單一 bounded execution 中批次或平行執行，完整保留並逐項檢查結果後再回模型。

一般原則：

- dependency 不存在、shared state 不變、順序不影響 correctness、每項結果可獨立判讀時才 batch／parallel。
- dependent、state-changing、write、side-effectful、approval-sensitive、adaptive、waiting／polling 或需前一 evidence 決定下一步的操作維持 serial。
- Batch／parallel 不減少 task scope、reasoning、validation、tool coverage、結果完整性或 evidence quality。
- 一項 failure 會改變其他 check 的必要性、參數或安全性時，不符合獨立條件，拆回 serial 或更小 batch。
- surface 不支援可靠 batch／parallel 時，不建立高複雜度 scheduler、額外 Multi-Agent 或有副作用 workaround。

省的是不必要的 model→tool→model 重入，不是必要推理或驗證。

## Long-running tool output discipline

已知長時間執行、持續顯示 progress/status 或可能產生大量 stdout/stderr 的 process，不預設把全部輸出送入 active model Context。

優先：

1. 工具原生支援時使用 quiet / silent / no-progress / concise mode。
2. 需要完整紀錄時 redirect 到 log/artifact/file。
3. 正常成功路徑先取得 exit status、duration、必要 summary 與少量關鍵 evidence。
4. 失敗時先讀 relevant error、tail、matched region 或 bounded log window；evidence 不足才擴張。
5. 不把「先餵巨量 log 再讓模型摘要」當主要節流方式。

Output suppression 不得破壞 validation contract；required diagnostics / audit / failure reproduction / security-safety evidence / formal gate log 應保留在適當 artifact/file，並可 targeted read。

## Runaway / Corrupted Generation STOP Guard

若 agent / model 輸出出現明顯且持續的 corrupted / runaway generation，例如大量無意義重複 token、punctuation、亂碼、重複相同段落，或沒有新增 evidence 卻持續重複同一 conclusion / action，立即 STOP；不得把「繼續輸出看看會不會恢復」視為 retry。

一般原則：

- 只針對明顯且持續的異常 generation；正常短暫重述不誤判。
- 優先停止模型 generation，避免無價值 Output Tokens / Credits、Context pollution 與錯誤 downstream action。
- STOP 後保存 working tree / current diff、最後可信 Git / validation / tool evidence，以及 external process / job state。
- 異常開始後新產生、未經 canonical evidence 驗證的 completion claim / commit / TASKS 敘述預設不可信；依 `DEBUG_VALIDATION.md` Completion Evidence Guard 重建 current state。
- external process 若仍正常執行，依 `DEBUG_VALIDATION.md` 的 Long-running Operation Supervision 獨立判斷 wait / inspect / STOP；不因 model generation 異常就武斷 kill。
- Recovery 優先新的 bounded session / handoff，只帶最後可信 evidence、current Git state、必要 diff / log 與未完成 scope。
- 沒有直接 evidence 時，不宣稱 context compaction 或其他 state transition 是 root cause；使用 `INSUFFICIENT OBSERVABILITY`。

核心原則：**省的是已失去資訊價值的輸出與錯誤後續工作，不是必要推理。**