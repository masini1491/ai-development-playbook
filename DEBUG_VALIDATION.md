# 除錯／驗證方法論（Debug / Validation Methodology）

> **Authority**：root cause、retry、build/CI phase、validation、evidence lifecycle、refactor evidence。
> **Read when**：目前問題涉及失敗原因、驗證範圍、evidence 有效性、重試／等待、behavior-preserving refactor。
> **Usually skip when**：只是一般 research、architecture ownership、Git permission／TASKS bookkeeping 或 UI／UX。
> **Progressive reading**：先依下方 Section Router 定位；找到 relevant heading 後只讀該 section 與必要相鄰 dependency，不預設載入全文。

## Section Router

- 根因／多來源結果／首次診斷 → `Root Cause 分類標籤`、`多來源／多 Agent 結果協調`、`首次接觸診斷 Harness`
- operational failure／retry／等待 → `執行失敗分類`、`重試紀律`、`長時間 Operation 監督`
- build／CI／昂貴流程 preflight → `Build／CI Phase Attribution`、`決定性 Fail-Fast Preflight`
- deterministic rule／validator／hook → `Deterministic Enforcement Admission Gate`
- completion／GitHub read-back → `完成證據關卡`
- validation scope／runtime backend → `驗證階梯`、`驗證涵蓋完整性`、`真實 Runtime／Backend Contract 驗證`
- verifier／evidence freshness → `Verifier Contract 生命週期`、`Evidence 等級`、`Evidence 取代生命週期`
- correctness fix／behavior-preserving refactor／搬移改名 → `正確性優先於重構`、`行為保持重構關卡`

## 預設流程（Default flow）

`Evidence → Root Cause → Focused Patch → Targeted Validation`

不要先重構再找原因；不要用更大的模型或更多 Agent 取代 evidence。

## Deterministic Enforcement Admission Gate

Playbook / project rule 不應因「很重要」就一律留在 instruction，也不應因想產品化就一律寫成 validator。先判斷它是否適合用 deterministic mechanism enforce。

推薦思路：

`Rule / invariant → deterministic, observable, low-false-positive? → validator / hook / script；否則 → human / AI reasoning contract，必要時再用 behavioral evaluation驗證`

適合升格為 automated enforcement，通常同時具備：

- **Observable**：結果可由檔案、schema、command exit、Git state、machine-readable metadata、exact path/reference 或其他客觀 artifact 直接觀察；
- **Deterministic**：相同輸入應得到穩定結果，不需要模型自由推論才能判定；
- **Low false-positive / false-negative risk**：工具不會因過度簡化 rule semantics 而頻繁誤擋正確工作或漏掉真正問題；
- **Material value**：違反後的 correctness/security/release/retrieval cost 足夠高，或人工/Agent 重複檢查成本明顯；
- **Cheaper than repeated remembering**：validator/hook 的維護與執行成本低於每次要求 Agent重新理解、記住與人工核對；
- **Clear ownership**：check 的 source of truth、scope、failure semantics 與修正責任可明確定義，不會建立第二份 policy authority。

典型適合機械化的項目包括：broken link/reference、stale filename、required file/field/schema、known generated-metadata drift、malformed config/frontmatter、declared path/role invariant、deterministic prerequisite、exact queue/evidence completeness marker 等。

下列通常**不得假裝可以由簡單 validator決定**：

- 某 refactor 是否值得現在做；
- AI-originated `CANDIDATE` 是否已足夠升格為 committed work；
- architecture trade-off 哪個方案最好；
- root-cause evidence 是否在特定複雜情境已達高信心；
- 使用者真正 intent、risk appetite 或產品優先序；
- 需要綜合模糊 evidence、現場條件、domain judgment 才能決定的事項。

對這類 judgment rule，若未來需要驗證 instruction 是否真的改變 Agent 行為，可建立 bounded behavioral scenario / eval；但**behavioral evaluation 本身不是所有規則的強制前置條件**，只有在風險、反覆 failure 或 adoption value 足以支持其成本時才做。

Automation 也必須服從最低充分原則：

- 不因能寫 script 就建立大型 validator framework；
- 小型 repo / 一次性 rule 可保持簡單 inline check；
- validator 若開始需要大量 heuristic、LLM grading 或 hidden state 才能判斷，應重新檢查它是否已跨出 deterministic boundary；
- 自動檢查只證明它實際檢查的 invariant，不得把單一綠燈升格成整體 correctness / security / completion PASS。

核心原則：**能可靠機械判斷的 constraint 優先交給工具；需要工程判斷的問題保留給 reasoning。產品化不是把所有規則 script 化，而是把最適合 deterministic enforcement 的那一小部分從「要求 AI 記住」升格成可驗證 contract。**

## Root Cause 分類標籤（Root-cause labels）

只使用：

- `CONFIRMED ROOT CAUSE`
- `HIGH-CONFIDENCE LIKELY ROOT CAUSE`
- `INSUFFICIENT OBSERVABILITY`

只有前兩者可直接 patch。

`INSUFFICIENT OBSERVABILITY` 時先取得能區分原因的最小 diagnostics / evidence；無法在目前 scope 內安全取得就 STOP。

## 多來源／多 Agent 結果協調（Independent Result Reconciliation）

當同一問題由多個**獨立 evidence producer** 回答，例如不同 Agent、reviewer、tool、runtime probe、static analyzer、test harness、外部 authority 或不同模型，先讓各來源在自己的 scope / authority / evidence contract 下完成判斷，再進行 synthesis；不得因為來源數量多就用簡單多數決取代證據判斷。

推薦流程：

`Independent conclusions → Normalize scope / authority / freshness → Agreement / Complement / Conflict / Unresolved → Evidence-weighted reconciliation → Next evidence only if needed`

一般原則：

- **Independent first, synthesis second。** 若多個 reviewer / Agent 本來就是為了降低共同偏誤而獨立工作，不要在它們完成前把彼此結論互相餵回去，除非 task contract 本來就是協作式 refinement。
- **Agreement ≠ truth by vote。** 多個來源同方向可以提高一致性，但若它們共享同一錯誤 upstream、同一 stale assumption、同一 mock 或同一 measurement profile，不能因「三個都這樣說」就升格為更高 evidence tier。
- **Conflict is a diagnostic signal, not a voting event。** 發生衝突時先比較：`scope / exact target / authority / freshness / phase / environment / measurement condition / assumption / completion criterion / evidence tier`。很多表面矛盾其實是不同來源回答了不同層級或不同條件。
- **Authority beats count。** 一個直接量到 production target 的 current canonical evidence，可以合理高於多個低 authority、stale、mock-only 或推論型結果；來源數量本身不形成 authority。
- **Complementary results 可並存。** 一個來源回答 root cause、另一個回答 blast radius、第三個只證明某 verifier stale，若 contract 不衝突，不必強迫收斂成單一句答案；synthesis 應保留各自證據角色。
- **保留 `UNRESOLVED`。** 若完成最低充分 reconciliation 後仍缺少能決勝的 canonical evidence，明確保留 unresolved / insufficient observability；不要只因 project 需要「一個答案」就挑較多人支持的一邊。
- 若衝突可以由一個低成本、低風險、可區分假說的 targeted check 解決，優先補該 evidence；不要因此自動增加 Agent 數量、升級最大 Context 或跑完整 regression。
- 若不同來源不是獨立的，例如同一 Agent 重述自己前一輪、不同模型共用完全相同的單一 summary、或多個工具都只是包裝同一 backend/result，synthesis 時不得把它們計成多份獨立 evidence。
- Security、safety、protocol、production/runtime 或其他高風險 decision 若存在 material conflict，依正式 authority / validation contract處理；本節不授權用「共識」降低既有 gate。

核心原則：**多個結果要先確認它們各自在回答什麼、憑什麼回答，再做 evidence-weighted synthesis；衝突時查 scope 與 authority，不用票數決定真相。**

## 首次接觸診斷 Harness（First-contact Diagnostic Harness / Test Consumer）

首次接觸新 hardware、network service、protocol、runtime/backend 或其他 external integration，且 production path 的實際行為／contract 尚未有足夠 observability 時，優先考慮 isolated diagnostic harness / test consumer，而不是直接把未知行為塞進 production runtime 或先用猜測式 patch 取得 evidence。

Diagnostic harness 一般應：

- default inert；
- bounded，具有明確 timeout / stop condition；
- read-only 優先；
- one-shot / explicit action 優先，不在背景無界執行；
- 不保存或輸出 secret / credential material；
- 不做 destructive / state-changing operation，除非該 mutation 本身就是已明確授權且不可替代的實驗條件；
- bounded retry，不做 infinite retry / polling；
- 只輸出足以區分假說或驗證 contract 的最低必要 evidence。

若 harness 需要真實 network、external service、hardware、credential 或其他高 capability execution，仍服從 `REPOSITORY_EXECUTION.md` 的 Task/Stage authorization、permission 與 credential boundary；「只是診斷」不會自動取得 mutation 或硬體執行授權。

Harness PASS 只證明其實際 target / backend / fixture / measurement profile 的 scope；不得把 isolated smoke、自建 test consumer、mock 或相似硬體結果直接升格成 production/network/hardware PASS。Embedded first-contact 的 target/device evidence delta 另見 `EMBEDDED_PROJECTS.md`。

核心原則：**先用最低風險、最低擾動的 isolated evidence consumer 了解未知 contract；diagnostic harness 是 observability 工具，不是繞過正式 production / authorization boundary 的捷徑。**

## 執行失敗分類（Operational failure taxonomy）

真正 execution/operational failure 分類：

- `SOURCE`
- `TOOLCHAIN`
- `ENVIRONMENT`
- `INFRASTRUCTURE`
- `SERVICE`
- `AUTHENTICATION`
- `AUTHORIZATION`
- `HARDWARE_REQUIRED`

可由使用者授權解除的 sandbox / network / filesystem / repository-metadata / execution permission gate，在解除前**不算真正 operational failure**；先依 `REPOSITORY_EXECUTION.md` 的 Authorization / Capability Layers 與 Permission-Gated Operation 處理。

`AUTHENTICATION` 表示已有必要 execution permission，但 service/account 身分驗證本身失敗，例如 credential 缺失、無效、過期或登入/session 無法成立。

`AUTHORIZATION` 表示 authentication 已成立或 service 可辨識身分，但該 identity / credential 對目前已授權 operation 缺少必要 service-side 權限。Credential 技術上具有較大權限時，也不得因此擴張 Task / Stage authorization。

`SERVICE` 可進一步區分 provider-side operational condition，例如：

- `RATE_LIMIT`
- `QUOTA_EXHAUSTED`
- `SERVICE_UNAVAILABLE`
- `PROVIDER_SIDE_ERROR`

Rate limit / quota exhausted 本身**不是** authentication failure，也不代表 credential 無效；先保存 reset/quota/evidence，依 `REPOSITORY_EXECUTION.md` 的最低充分 Access Capability 判斷是否可使用官方 public anonymous read-only fallback、等待 reset，或需要 authenticated access。不得以 quota exhausted 為理由盲目 retry、輪替帳號/token/installation、切 proxy/mirror/第三方來源，或擴大 credential capability。

只有 `SOURCE` evidence 可直接成為繼續修改 production source 的理由。

TOOLCHAIN / ENVIRONMENT / INFRASTRUCTURE / SERVICE / AUTHENTICATION / AUTHORIZATION / HARDWARE_REQUIRED 不得合理化 production source patch，也不是提高模型/Reasoning/Context/Multi-Agent 的理由。

## 重試紀律（Retry discipline）

同一**non-compile operational root cause** 預設最多自動 retry 1 次；第二次仍失敗時 STOP、分類並保存最小可重現 evidence。

Permission denial → request → approval → retry original operation 不算 operational retry。

Authentication / authorization failure 不應以盲目重試、擴大 network permission 或提高 credential privilege 方式處理；先確認目前 operation 是否在 Stage authorization 內、credential 是否為 intended identity、是否真的缺少 service-side capability。任何 credential/ACL/role mutation 仍需獨立明確授權。

Compile/source-fix loop 若 repository governance、正式 validation contract 或特定 Stage 有自己的 bounded 上限，服從該正式規則；不要用 non-compile cap 覆蓋它。

## 長時間 Operation 監督／無進展等待關卡（Long-running Operation Supervision / No-progress Wait Guard）

對 long-running build、test、download、deploy、code generation、package/signing 或其他可能長時間佔用 tool/process 的 operation，等待與 polling 也必須是 **bounded operation**；不得把「process 還沒結束」當成無限次要求使用者繼續等待的理由。

一般原則：

- 第一次等待可依工具與工作負載的合理特性給予 bounded interval；若需要再次延長，先取得最低成本的 progress evidence，例如 process/job 是否仍 alive、目前 phase/stage、最新 bounded log/tail、artifact/file activity、CI step state 或工具原生 progress indicator。
- 若 execution UI 每次延長 wait/poll 都需要使用者 approval，該 approval 只覆蓋**該次 bounded wait**；一次同意「繼續等」不等於授權 indefinite polling loop。
- 有可觀察 progress、已知某 phase 合理耗時，或目前 Stage 必須等待單一 operation 完成時，可以繼續 bounded wait；不要只因暫時 silent 就武斷 kill 正常工作。
- 若連續觀察沒有新增 progress evidence，先做 bounded status/tail/process inspection，判斷是 slow、silent-but-healthy、stalled、waiting on dependency、permission gate 或其他狀態；不得只重複「再等一下」而沒有新的判斷資訊。
- Process / CI step 已 exit non-zero、cancelled 或明確 fatal 時，立即停止等待；保存相關 log/evidence，轉入 failure classification / phase attribution，不得繼續 poll 已結束的 operation。
- 若目前工具無法提供足夠 observability，而繼續等待會持續消耗昂貴 usage window、鎖住 Stage 或需要反覆人工 approval，應 STOP 並回報 `INSUFFICIENT OBSERVABILITY` / operational state，而不是無限延長。
- Long-running operation 的 stdout/stderr 控制遵守 `CODEX_EXECUTION.md` 的 **Long-running tool output discipline**：優先保存完整 log 並只讀必要 bounded evidence，不把巨量 progress output 全部灌入 active Context。

核心目標是：**等待必須帶來新的完成機會或新的 evidence；沒有進展的等待本身不是 retry 策略。**

## Build／CI Phase Attribution（Build / CI Phase Attribution）

Multi-stage build / CI pipeline 的整體 `FAIL`、non-zero exit 或紅燈，不得自動等同於 `Compile FAIL` 或 production source failure。應先找出**第一個真正 fatal phase / command**，再依該 phase 的 ownership 與 evidence 分類。

常見 phase 可依實際 pipeline 區分：

`configure / dependency resolution → code generation → compile → link → firmware/image generation → size/partition check → post-build → packaging/signing → artifact publication → deploy/runtime smoke`

一般原則：

- 先找 first fatal evidence；warning、deprecation notice 或 earlier non-fatal diagnostic 若沒有因果 evidence，不得因較醒目就被當成 root cause。
- 較晚 phase 失敗不得自動推翻較早 phase 已成立的 evidence。例如 packaging FAIL 不等於 compile/link FAIL；artifact publication FAIL 也不等於 binary generation FAIL。
- 反之，較早 phase PASS 也不得冒充後段 PASS；每個 evidence 只對其實際涵蓋的 phase 有效。
- 修正某個 late-stage failure 後，優先重跑足以驗證受影響 phase 與必要 dependency chain 的最低充分 scope；除非修正改變了 source、toolchain、configuration、generated input 或其他會使 earlier evidence 失效的 material contract，否則不要機械式把整條 validation ladder 全部重跑。
- 若同一 command 同時負責多個 phase，應以 log / artifact / command semantics 判斷哪些子階段已完成、哪一步真正 fatal；不要只依 command 名稱粗略分類。

核心判斷：**Overall pipeline FAIL ≠ every phase FAIL；Late-stage failure ≠ earlier valid evidence invalidated。**

## 決定性 Fail-Fast Preflight（Deterministic Fail-Fast Preflight）

若昂貴或長時間 operation 的後段依賴某些**可在事前低成本、決定性驗證**的 input / metadata / prerequisite，優先在 expensive work 前做最小 preflight，避免跑到最後才因已知可檢查的空值、缺件或不合法設定失敗。

適用例例如：

- required version / build metadata；
- vendor/product/package identifier；
- required config key / manifest field；
- 必要 tool/runtime version；
- expected file/path/input artifact 是否存在且格式可判定；
- signing/packaging 所需 material 是否**存在且可用**（不得輸出 secret value）；
- partition/package/image metadata 中可在 build 前確定的 invariant。

Condition-triggered 原則：

- 只檢查真正會讓目前 expensive operation 在後段決定性失敗、而且可在事前可靠判斷的項目；不要為了形式建立大型 universal preflight framework。
- 已實際發生過 costly late failure、同類 job 頻繁執行、或 failure cost 明顯高時，優先把該 deterministic prerequisite 收斂成 repository-owned guard/verifier/CI pre-step；一次性低成本流程則可保持簡單 inline check。
- 若某 input 本來就必須由 build/runtime 中途產生，或事前值不可可靠知道，不得用猜測式 preflight 假裝已驗證。
- Preflight PASS 只證明 prerequisite 可進入 expensive operation；不代表 compile、package、sign、deploy 或 runtime 一定成功。
- Preflight 本身應比它避免的失敗便宜且穩定；若檢查成本接近完整 build，改用 targeted phase validation 或其他更有效 evidence。

推薦思路：

`cheap deterministic prerequisites → expensive operation → phase-attributed result → targeted retry/revalidation`

## 完成證據關卡（Completion Evidence Guard）

Agent 的自然語言 completion report、commit SHA 敘述、`TASKS.md` 狀態敘述或「已完成」不能單獨作為 repository completion authority。只要目前 Stage 宣稱發生 repository mutation、commit/push、queue bookkeeping 或 validation-state 變更，就應以 canonical repository evidence 做最低充分交叉確認。

這在長 session、連續多 Stage、context compaction、agent handoff、重新 attach repository，或任何可能造成 stale context / stale task state 的情況尤其重要，但不是只有這些情況才適用。

### ChatGPT 收到 Codex 結果時的 GitHub Remote Read-back

當 ChatGPT／planning agent 收到 Codex／coding agent 的執行結果，只要結果宣稱涉及 **GitHub repository tracked-file 修改、commit、push、`TASKS.md` queue bookkeeping、branch/HEAD 變更，或其他可由 GitHub canonical evidence確認的 repository state change**，ChatGPT 在接受「完成」、更新後續判斷、產生下一 Stage，或向使用者回報修改已成立前，**一律先到 GitHub 讀取 current remote evidence 核對實際結果**。

最低充分 read-back 依 claim 選用，不要求每次把整個 repository 全掃一遍：

- commit / push claim：確認 target repository、branch、最新 relevant commit／SHA；
- file modification claim：讀取 changed-file list／scoped diff，並在 correctness 判斷需要時讀 current target file relevant range；
- `TASKS.md` bookkeeping claim：讀最新 remote `TASKS.md` queue state；
- docs/spec/validation-state claim：讀被宣稱修改的 canonical file relevant section；
- 若 Codex 提供 commit SHA，可先以該 SHA 查 commit/diff，再確認它確實位於 intended remote branch/current state；不得只因 SHA 看起來合法就接受。

一般原則：

- **Codex report 是待驗證 claim，不是 GitHub authority。**「已 push」、「已修改某檔」、「TASKS 已移除」、「validation docs 已更新」等敘述，都必須以 GitHub current remote evidence交叉確認。
- GitHub read-back 是 read-only verification，不授權 ChatGPT修改該 repository，也不繞過 `REPOSITORY_EXECUTION.md` 的 Conversation-scoped Repository Write Lock；即使該 repository 不是目前 writable target，仍可在合法 read-only capability內核對 Codex 結果。
- 若結果只涉及 local-only、未 push 的 working-tree state，而且 GitHub理應尚無變更，不能假裝用 GitHub驗證 local mutation；應明確標記 remote 尚無該 evidence，要求／使用對應 local canonical evidence。使用者要求的是 GitHub result verification時，只有已進入 GitHub remote state的 claim才可由本 gate確認。
- 若 GitHub current state 與 Codex report 不一致，立即 STOP completion acceptance；先以 remote evidence重建 current state，指出 mismatch，不得用 Codex summary覆蓋 GitHub事實，也不得自動進下一 Stage。
- 若 GitHub connector／network／permission 暫時無法取得必要 remote evidence，標記 **REMOTE COMPLETION EVIDENCE UNAVAILABLE**；不得在未核對情況下把 Codex 的 repository-mutation claim提升為已確認完成。
- Read-back scope 應最低充分：確認此次宣稱的 repository、commit、changed files、關鍵內容與 queue/validation state；不因這條規則每次做 repo-wide audit、full code review 或重新跑 validation。

核心原則：**Codex 說它改了 GitHub，不等於 GitHub 真的已是那個狀態；ChatGPT 必須先 remote read-back，再接受 completion。**

最低充分 completion evidence 依 Stage 性質選用：

- pre-Stage baseline HEAD / branch / queue state（若需要比較）；
- post-Stage `HEAD` / `origin/<branch>` 與最新 relevant commit；
- scoped changed files / diff / stat，證明宣稱修改的 target 確實有本 Stage 的新 state；
- required validation evidence；
- `TASKS.md` queue state（若該 Stage 使用 TASKS）。

一般原則：

- 若 Stage 宣稱產生新的 repository mutation 或 commit，evidence 必須證明相對於 Stage baseline 確實出現符合 scope 的新 state；不得拿上一 Stage 的 SHA、diff、validation 或 queue state 重複當成本 Stage完成證據。
- 不使用「SHA 一定要變」作為 universal rule：read-only、validation-only、合法 no-op、already-satisfied 或未授權 commit 的 Stage 可以沒有新 commit；但其 completion claim 必須與該 Stage 預期 evidence 一致。
- 若 completion report 與 Git/current queue/validation authority 不一致，立即 STOP，標記該 completion report 不可靠；先以 canonical evidence 重建 current state，不得沿用錯誤 summary 直接進下一 Stage。
- Evidence mismatch 時不要優先要求同一 stale context「回想剛才做了什麼」；先做便宜、機械式的 Git / queue / scoped-diff 檢查，再決定是否需要新的 bounded session/handoff。
- Completion Evidence Guard 只確認「目前 repository / validation state 是否真的符合宣稱」，不取代 task-specific correctness review、runtime、hardware 或 production validation。

## 驗證階梯（Validation ladder）

由小到大：

1. static check
2. targeted verifier
3. targeted test
4. relevant build / compile
5. required matrix
6. full regression

只跑足以驗證目前 scope 的最低充分層級；repository formal merge gate 若明確要求更完整驗證則服從正式 gate。

## 驗證涵蓋完整性（Validation Coverage Integrity）

`exit 0` 不等於驗證真的涵蓋目標 implementation。

必須在有風險時證明 intended source/backend/runtime/feature 真正參與 compile/link/test，例如：
- sketch/layout 是否真的包含該 source
- conditional compile / feature flag 是否啟用
- CMake target 是否 link 到 intended backend
- mock/stub 是否意外取代 production path
- 正確 board/FQBN/target 是否被選中
- 正確 runtime/toolchain 是否被使用

因此 validation evidence 需要時應記錄：
- toolchain/version
- target/board/FQBN
- exact command
- tested commit SHA
- CI run

Local PASS 不等於 remote CI PASS；舊 commit PASS 不等於目前 HEAD PASS。

## 真實 Runtime／Backend Contract 驗證（Real-runtime / backend contract validation）

Static、mock、stub 或 host-only harness 只能證明其實際涵蓋的邏輯；若 production correctness 依賴特定 runtime/backend/framework 的 superclass、binding、registration、loader、proxy、lifecycle、serialization、database engine、browser/device API 或其他 runtime contract，mock/static PASS 不得冒充該 runtime contract 已驗證。

Condition-triggered 原則：

- 只有 correctness 確實依賴特定 runtime/backend contract 時，才需要讓對應 authority 參與 validation；純函式或與 runtime 無關的邏輯不必為形式增加 runtime test。
- 優先使用最低風險、最低成本且足以證明 contract 的真實 runtime/backend，例如 local emulator/runtime、ephemeral database、local service process、test container 或實際 framework test host。
- 可用 dummy credential、temporary state、loopback/local endpoint 或 sandbox resource 完成時，不要為了驗證 runtime contract 直接升到 production secret、production resource 或 remote mutation。
- 若 local real-runtime smoke 已能證明本次 contract，就不必無條件升到 remote/production；反之 local runtime PASS 也不得冒充 production/network/hardware PASS。

推薦依需求逐級增加 authority participation：

`Static / Mock → Targeted real-runtime/backend smoke → Integration / Remote service → Production / Hardware`

是否進入下一層仍服從最低充分 Validation scope。

## Verifier Contract 生命週期（Verifier Contract Lifecycle）

Verifier / static checker / test harness 本身也是會隨 production architecture 演進的 contract；驗證失敗不自動代表 production source 有 bug。

當既有 verifier 在 refactor、lifecycle、symbol、region boundary、route、ownership 或正式 contract 更新後失敗時：

1. 先重跑最小失敗 verifier，記錄精確 failed check / expected invariant / target region。
2. 對照最新高權威 contract、current production source 與必要 validation evidence。
3. 只有 evidence 證明「production invariant 仍成立，但 verifier assertion / symbol / region / wording 已過期」時，才可做最小 verifier-only patch。
4. 不得為了讓 verifier 變綠而弱化 safety/security invariant、刪除 assertion、改 production source，或把真正 source bug 假裝成 stale test。
5. 若無法區分 verifier drift 與 production defect，標記 `INSUFFICIENT OBSERVABILITY` 並 STOP；必要時建立獨立 source/validation task。

因此：

> Failing verifier ≠ source bug；Passing verifier ≠ coverage complete。

Verifier 更新後仍應執行直接相關交叉檢查，避免修正一支 stale verifier 時破壞其他正式 validation contract。

## Evidence 等級（Evidence tiers）

依專案需要區分：
- Software PASS
- Compile PASS
- Static/Test PASS
- Bench PASS
- Hardware PASS
- Network PASS
- Production PASS

不得把低層 evidence 翻譯成高層 PASS。

硬體/協議 evidence 可使用：
- `CONFIRMED_UPSTREAM`
- `CONFIRMED_LOCAL`
- `INFERRED`
- `UNKNOWN`
- `HARDWARE_TEST_PENDING`

相似裝置或 upstream evidence 不得自動改寫成 local hardware confirmed。

## Evidence 取代生命週期（Evidence Supersession Lifecycle）

歷史 PASS 應保留可追溯性，但不得因仍存在於文件或 Git history 就自動視為 current evidence。

Validation / evidence record 可依需要標記：

- `CURRENT`
- `SUPERSEDED`
- `HISTORICAL`
- `REVALIDATION_REQUIRED`

下列 material change 應觸發「舊 evidence 是否仍有效」的判斷：

- target / board / FQBN / PHY 改變
- toolchain / runtime contract 改變
- architecture / protocol / security / persistence contract 改變
- runtime ownership / lifecycle / initialization order 改變
- hardware mapping / electrical assumption 改變
- validation backend / verifier scope 改變
- implementation path 被重構到可能影響原驗證涵蓋範圍

原 evidence 若只證明舊 contract 或舊 implementation，不得被新狀態繼承；應標成 `SUPERSEDED` / `HISTORICAL`，並把新狀態保持 `REVALIDATION_REQUIRED` 或對應 Pending。

反之，若既有 evidence 仍為 `CURRENT`，而與該 evidence 相關的 source、contract、runtime/toolchain、target、environment assumption 與 validation backend 都沒有 material change，後續 Stage 應**重用既有 evidence**，不要機械式從 Validation ladder 最底層全部重跑。

Evidence reuse 原則：

- 先判斷本次 change / Stage 實際影響哪些 evidence scope；只把受影響部分標為 `REVALIDATION_REQUIRED`。
- 已驗證且未受影響的 baseline 可以直接沿用，後續 validation 聚焦剩餘未知或更高 authority 層級，例如 software baseline 已 CURRENT 時直接進 hardware/network evidence。
- 不得因「進入下一 Stage」本身就把所有舊 PASS 作廢；也不得為了省成本沿用已被 material change 影響的 evidence。
- 若無法判斷舊 evidence 是否仍適用，先縮小 change impact / dependency / contract 差異；仍無法確定時標記 `REVALIDATION_REQUIRED`，不要猜測。

文件可保留歷史測試事實，但 current summary 必須明確指出最新 superseding rule，避免舊 PASS 被誤讀成目前 PASS。

### 行為保持 ≠ 證據保持（Behavior-preserving ≠ Evidence-preserving）

`behavior-preserving`、`refactor-only`、`no intended semantic change` 描述的是**修改意圖與 protected behavior contract**，不代表既有 validation evidence 自動保持有效。每一份 evidence 是否仍為 `CURRENT`，應依它真正依賴的 implementation、binary、runtime、toolchain、measurement profile、hardware/environment assumption 判斷。

一般原則：

- File/module extraction、symbol relocation、link/layout 變化、compiler/config change、dependency rebuild、task/stack placement、instrumentation/logging 或其他結構性修改，即使 public behavior 預期完全相同，也可能改變 binary identity、timing、memory/resource layout、scheduler/cache behavior 或 measurement condition。
- 若舊 evidence 衡量的是 firmware/binary timing、latency、resource usage、heap、stack、hardware behavior、performance 或其他與實際 build identity 有關的結果，而本次 refactor 已改變該 identity 或相關 execution profile，舊數值只能保留為 `HISTORICAL` / `SUPERSEDED`；新 build 應建立最低充分的新 baseline，不得宣稱 bit-identical 或直接繼承舊 measurement。
- 反之，純 ownership/file-layout change 不代表所有不相關 evidence 都要失效。若某 API/wire/schema/security invariant 的 authority 與 validation backend 未受 material impact，可保持 `CURRENT`；只 revalidate 受影響範圍。
- Refactor 前應先列出「哪些 evidence 預期可保留、哪些可能失效」；完成後以 canonical diff/build identity/validation scope 重新分類，而不是等到下一個 hardware/runtime Stage 才發現 baseline 已不再可比。
- 若 instrumentation 本身可能改變 timing、logging load、network traffic、scheduler behavior 或 binary layout，應視為新的 **measurement profile**。跨 profile 數據可作方向性比較，但除非 observer effect 已被控制，不得假裝是嚴格單變因 A/B。
- Diagnostic instrumentation 優先 bounded、test-only、低擾動，量測必要 boundary 而非修改 production semantics；若 instrumentation 必須改變 behavior 才能觀察問題，需把它當成新的 experiment contract，而不是「只是加 log」。

核心原則：**Behavior preservation 與 evidence preservation 是兩個不同問題；驗證重用依 evidence dependency，不依 refactor 標籤。**

## 正確性優先於重構（Correctness before refactor）

發現 correctness bug 時優先：

1. root cause
2. focused correctness fix
3. targeted validation
4. behavior-preserving refactor（若仍有價值）
5. regression

不要預設把 bug fix、architecture redesign、cleanup、library extraction 打包成一次工作。

## 行為保持重構關卡（Behavior-Preserving Refactor Gate）

宣稱 behavior-preserving 的重構，應先建立可比較 baseline，而不是只在修改後看「有編譯過」。

推薦流程：

`Baseline → Freeze protected invariants → Bounded refactor → Targeted build/test → Compatibility comparison → Remaining cleanup stays Deferred`

開始前至少確認本次真正需要保護的 invariants，例如：

- public / wire protocol values、layout、CRC、retry、timeout
- API / route / command contract
- persistent schema / migration semantics
- state ownership / lifecycle
- GPIO / board / hardware mapping
- safety initialization / output inactive state
- resource/capacity/timing behavior（若屬正式 contract）

重構時：

- 只改完成本 Stage 所需的 ownership / file layout / naming / dependency direction；
- 若遇到需要 architecture redesign、behavior change、new abstraction 或 unrelated cleanup，STOP 或另建 task；
- 未完成的 deeper modularization / cleanup 必須保持 Deferred，不得在後續 feature task 裡順手完成。

驗證時優先比較 refactor 前後的 protected invariants；若 binary/resource usage 有變化但 behavior 預期不變，需記錄差異並判斷是否 material，不要只因數字不同就宣稱 regression，也不要完全忽略。

### 搬移／改名 Reference-Graph Closure Gate（Relocation / Reference-Graph Closure）

Move、rename、split、directory/domain relocation、module extraction 或其他會改變 path / symbol / route / anchor 的 behavior-preserving migration，完成條件不只是 target 已成功搬到新位置；還必須確認舊 reference graph 已最低充分收斂。

推薦流程：

`Target relocation → Inbound-reference inventory → Routing/import/anchor/manifest update → Stale-old-reference scan → Targeted validation`

一般原則：

- 檢查直接與間接 inbound references，例如 include/import、README/docs links、router/index、anchor、manifest、CI/workflow path、test fixture、schema `$ref`、tooling/verifier、generated-input source path 或 project-owned script reference；依實際 repo 結構取最低充分 scope，不要求固定全種類 checklist。
- **Moved successfully ≠ migration closed。** 新 target 可正常 build/render，不代表仍指向舊 path/symbol 的 consumer 已全部更新；舊 reference 若會造成 broken navigation、錯誤 authority、漏編譯、stale verifier 或 silent fallback，仍屬未完成 migration。
- 優先用 deterministic search/link/import/reference verifier 找 stale old identifier/path；沒有既有工具且 repo 很小時，可用 bounded search，不為形式建立大型 reference graph framework。
- 若 relocation 同時更新 canonical owner，需確認舊文件／route 不再繼續宣稱自己是 authority；不要只修 link 而留下雙 owner。
- Generated、vendored 或 upstream-controlled references 依其 generator/upstream authority處理；不得手改 generated output 製造不可維護 drift。
- 若發現 stale reference 指向的是刻意保留的 compatibility alias / redirect，應有明確 contract；不要因名稱仍存在就機械刪除。

核心原則：**搬移的完成是新位置可用、舊引用收斂、authority/routing 一致；不是只把檔案移成功。**

### 依 Evidence Boundary 排定重構時機（Refactor Timing by Evidence Boundary）

多個真實技術債候選同時存在時，不以「哪個檔案最大／最醜」決定先後；優先選擇 **ownership 清楚、behavior freeze 容易、validation coverage 強、external/runtime/hardware coupling 較低** 的 boundary，讓 refactor 可以被低風險地證明為 behavior-preserving。

一般原則：

- 若某 domain 的 correctness 高度依賴尚未完成的 hardware/runtime/recovery/timing evidence，而且現有結構沒有阻礙取得該 evidence，通常先完成 evidence gate，再做 structural extraction；避免同時改變 implementation identity 與待驗證現象，使 causal comparison 失去基準。
- 若現有結構本身正在阻礙 observability、使 owner 不可辨識、讓 verifier 無法可靠涵蓋，或讓必要 evidence 無法安全取得，則可先建立最小 behavior-preserving extraction / instrumentation Stage；必須明確記錄舊 baseline 哪些失效、哪些保留。
- Refactor timing 應考慮 current frozen baseline。正在進行 hardware/performance A/B、migration/cutover、recovery campaign 或其他依賴 binary/runtime identity 的驗證時，無關 correctness 的 cleanup 通常 Deferred，直到 baseline 不再需要或有正式新 baseline plan。
- 若某候選可依既有 deterministic verifier、host test、exact readback、compile 或其他強 evidence 守住 behavior，而另一候選只能依尚未完成的現場／硬體證據驗證，通常先處理前者；這是風險排序，不是宣稱所有低 coupling debt 都必須優先。
- 每完成一個 refactor Stage，重新讀 current dependency/evidence state再排下一刀；不得因最初 inventory 排出一串順序，就把後續 Stage 視為自動授權或不需重新評估。

核心原則：**現在最值得修的技術債，是能清楚恢復 ownership、又能用目前最強 evidence 守住 behavior，而不會無必要破壞正在使用 baseline 的那一塊。**

## 決策階段（Decision Stage）

若 implementation 前仍有高影響 architecture/security/state/persistence policy 未決：

`Evidence → Architecture/Policy Decision → Frozen invariants/contract → Implementation → Validation`

Decision-only Stage 不修改 production behavior。