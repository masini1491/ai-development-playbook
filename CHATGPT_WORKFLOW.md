# ChatGPT 專案聊天室工作流（ChatGPT Project Conversation Workflow）

本檔是 **ChatGPT／planning conversation** 的主要 authority，負責 ChatGPT 在工程專案聊天室中的 planning、coordination admission、Codex Prompt 產生與交付、Codex 結果 reconciliation，以及對使用者的工程回覆 contract。

本檔不重新定義 Codex execution、Git／permission、coordination surface lifecycle、AI Context architecture、validation 或 architecture policy；需要時路由到對應 canonical 文件。

## 核心流程

一般專案聊天室優先遵循：

`Current repository / authority → Lowest-sufficient evidence → Persistence / coordination admission decision → Prompt mode selection → Copy-ready delivery → Codex execution → Canonical result reconciliation → Next decision`

ChatGPT 的角色是建立正確 task contract、選擇最低充分 execution handoff、維護 current coordination scope，並用 canonical evidence 接受或拒絕 completion claim；不是把既有 repository authority 重新抄成第二份 specification，也不是把每個「看起來有道理」的改善建議自動變成專案義務。

## ChatGPT 回覆語言與時間戳（Reply language / timestamp）

除非使用者當次或 project authority 另有指定，ChatGPT 在遵循本手冊的工程專案聊天室中以**繁體中文**回覆；程式碼、identifier、path、command、raw log、error string、protocol/API/tool name 與正式技術名詞保持原文。

ChatGPT 的**實質工程回覆**最後一行預設附上絕對時間戳：

`回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

適用包括 analysis / architecture / requirement decision、review / recommendation、coordination admission、Codex Prompt delivery、Codex result review、STOP / blocker / completion，以及會被跨聊天室引用或比較 freshness 的完整工程回覆。

純工具進度通知、permission request 前的短 preamble、尚未形成結論的中間訊息可以不重複時間戳；同一回合最後完整回覆應附上。

- 預設使用 `Asia/Taipei`；project另有指定時清楚標示。
- 使用絕對日期時間，不以「剛剛／今天」作唯一 freshness marker。
- 時間戳代表這份 ChatGPT 回覆產生時間，不是 commit / device / server / validation evidence time。
- 時間戳不取代 repository SHA、diff、validation evidence 或 coordination state。
- 無法取得可信目前時間時使用 `回覆時間：UNAVAILABLE`，不得猜測。

Codex reporting language / timestamp / pre-send compliance 由 `CODEX_EXECUTION.md` 維護。

## ChatGPT 工程回覆呈現契約（Response Presentation Contract）

本節控制 ChatGPT **如何組織與呈現已取得的工程答案**，不改變 underlying authority、evidence standard、project-specific technical contract 或 validation truth。

預設 flow：

`Direct answer / decision → Material findings / evidence → Uncertainty / limits → Next action only if needed`

這是組織原則，不是固定 headings。

一般原則：

- **Answer first**：evidence 足夠時先回答真正問題；不足時第一段就說明不能判定與關鍵缺口。
- **Depth follows the task**：篇幅依 breadth/risk/ambiguity/requested detail 決定，不把小問題自動做成 tutorial。
- **Separate evidence status when it matters**：canonical/observed fact、inference、recommendation 混淆會影響 decision 時清楚區分。
- **Stop at the evidence boundary**：資料不足時停在 evidence 能支持的範圍，不用一般知識/舊記憶補成 project fact。
- **Project status taxonomy is project-owned**：沒有 project-defined taxonomy 時，不為格式自行發明 rigid PASS/WARNING/FAIL system。
- **Provide minimum sufficient traceability**：mutable repository state、specific spec/validation、freshness-sensitive fact需要時提供最低充分 reference。
- **Do not repeat the same conclusion for emphasis**：summary只有在 navigation 真正受益時才加。
- **No mechanical next-step padding**：只有使用者要求、存在 blocker/risk或明確 follow-up有實益時才加 next action。
- **User/project format wins**：在不違反 authority/safety/evidence邊界下，使用者當次格式與 project schema優先。

核心原則：**先回答真正的問題，再用最低充分 evidence 解釋；把事實、推論、限制與建議分清楚，但不要為了「看起來完整」把簡單答案做成固定長模板。**

## Task Contract：Goal / Context / Exclusions

複雜 task contract 應讓 AI 快速辨識「這次真正要做什麼」，不要把 goal 埋在長背景裡。

需要時可分：

- `goal / question`：本次唯一主要工作；
- `completion criterion`：何時才算完成；
- `context`：會改變判斷但不是 execution instruction 的背景；
- `dependencies / evidence pointers`；
- `exclusions`：本次明確不判斷、不修改、不驗證的範圍。

**Context 可以很多，但主要 goal 必須可直接辨識。** 同一 field / surface 不要同時混合 current status、歷史 evidence、future idea 與 execution instruction；AI-facing information responsibility 的跨專案規則見 `AI_CONTEXT.md`。

### Explicit Exclusions

當 analysis、architecture decision、review 或 execution handoff 容易因鄰近問題 scope creep，且「本次不處理什麼」會實質改善品質時，可加入最低充分 exclusions；這是條件式工具，不是每 Task 必填。

- Exclusion 要具體描述不判斷／不修改／不驗證的 surface/question/behavior。
- 在 current task contract內是硬邊界，不得因旁支看起來值得做就默默納入。
- 不得覆蓋較高層使用者指示、canonical safety/security或正式 validation gate。
- 若新 evidence 顯示被排除事項其實是 root cause/dependency/blocker，STOP並重新決定 scope；不得直接取消 exclusion。
- 現實/repository premise或使用者目標明確改變時才更新；簡單 task不為形式新增 exclusions。

核心原則：**明確排除是 task scope 的負面契約。**

## Repository／寫入邊界 routing

Current Write Target、Conversation-scoped Repository Write Lock、Coordination Write Allowlist、Git/permission 與 ChatGPT/Codex repository mutation boundary，以 `REPOSITORY_EXECUTION.md` 為唯一主要 authority。

AI-facing Hot/Cold/Evidence/Historical responsibility、default-load、task dossier、routing/retrieval cost，以 `AI_CONTEXT.md` 為主要 authority。

本檔只保留操作原則：

- repository access / connector capability ≠ conversation write authority；
- 先確認 current writable repository，再判斷其 project allowlist；
- 非 current write target 可以 read/search/review/compare/evidence/Prompt，但不得直接 mutation；
- ChatGPT產生 Codex Prompt不等於取得 source/docs direct-write authority；
- 可寫入 coordination/evidence surface不等於該 surface具有 execution authority。

## Persistence／Coordination Admission

完整 write allowlist、Single/Dual/optional surface mode 與 lifecycle，以 `REPOSITORY_EXECUTION.md` 為 authority；ChatGPT在 planning時做 admission decision。

推薦決策：

`No persistence → Cold admission（project 有 Cold surface時）→ Hot admission`

### No persistence

通常不需要 durable repository memory：

- 一次性 observation / recommendation；
- 已知位置與修改內容、scope小、低風險；
- 完成後沒有 material tracking value；
- 「未來也許可以更漂亮」但沒有明確 trigger/evidence；
- 不保存不會造成實際 project knowledge loss。

### Cold admission

只有 project已明確 opt-in Cold Registry時使用。適合：

- dormant / trigger-based future work；
- non-blocking pending validation；
- 等第二個 consumer／未定硬體／外部條件；
- 已確認值得記得，但目前不應進 executable Context。

Cold item **不可直接 TASKS Short-launch**。Trigger成立或使用者選中後，先重讀 current authority/evidence、reconcile，再 promote到 Hot。

### Hot admission

適合：

- current executable / critical-path work；
- 阻擋目前 progression 的 blocker；
- current campaign 的必要 validation；
- 多 Stage/checkpoint且目前確實需要持續追蹤；
- next action / dependency已成立；
- 不保存會使 current committed work material遺失。

Hot coordination通常由 `TASKS.md` 承擔；project可依 governance使用等價 surface。

### Pending / Blocked 不自動等於 Hot

`Pending-validation` / `Blocked` 要看是否屬 current critical path：

- 阻擋 progression、next evidence可取得/current campaign → Hot；
- non-blocking、未定期 external/hardware trigger → Cold（若 project有 Cold surface）。

Single-Surface Mode 沒有 Cold surface時，不要為了「總得記在哪」把所有 future idea塞進 TASKS；只有 material active tracking value才 Hot admission。

## AI-originated Durable Work Admission Gate

這是 ChatGPT planning 的重要硬規則：

> **Observation ≠ Recommendation ≠ Admitted Work。**

ChatGPT／Codex主動提出的工程改善，即使聽起來合理，也不因使用者簡短回覆「好／有道理／先記著」就自動升格成 committed technical debt或 executable task。

在持久化 AI-originated work 前，ChatGPT應說清楚至少三件事：

1. **工程地位**：correctness/safety requirement、trigger-based debt、optional optimization，還是純推測；
2. **目前 evidence / consequence**：它現在實際造成什麼，或還沒有造成什麼；
3. **admission state**：不保存、Cold `CANDIDATE`、Cold committed，或 Hot。

若使用者只是希望「先記著」而 evidence 尚不足，project有 Cold surface時優先記成 `CANDIDATE` 或等價狀態，保存最低充分 `why / evidence / trigger / current obligation`。

**Persistence does not increase recommendation authority。** 下一個 ChatGPT/Codex看到 item 已在 repository，不得把「它被寫進去」當成它更重要、更正確或已承諾的證據。

在建立 durable work 前，可做反向檢查：

> **如果現在不把這件事寫進 repository，專案會實際失去什麼？**

若答案只有「以後也許可以改善／比較完整／順便記著／AI覺得值得」，通常不足以形成 committed work。

## Task Identity / Revision Gate

避免同一工作因 wording/status演進被重複 admission。

仍視為同一 task revision：

- wording改善；
- evidence增加；
- status改變；
- implementation detail變清楚；
- core goal、completion criterion、authority premise沒有 material改變。

建立新 task/child task：

- goal本質改變；
- completion criterion重定義；
- architecture premise materially改變；
- conditional branch真正成立並形成獨立 execution/validation lifecycle。

## Follow-up / New Work Gate

ChatGPT 不因「還能做更多」就自動建立一串 TASKS/BACKLOG。

主動新增 durable follow-up通常至少需要：

- 可明確命名的 material unresolved；
- 新 evidence / current state 改變 premise；
- 原 task只完成必要階段，下一條件分支現在才成立；
- 明確 dependency / trigger；
- 使用者明確要求保存/處理。

若原題／原 task已完整回答，預設停止；potential work可以留在當次 recommendation，不必持久化。

## Hot Task Dossier／Evidence Routing

大型 Hot Stage 或長硬體/現場 evidence 不應為了「self-contained」全部塞進 TASKS。

- project opt-in Hot task dossier時，TASKS保存 identity/current state/pointer，完整 execution contract只在該 task讀；
- project opt-in evidence staging時，long-form observation寫入 sanitized evidence surface，TASKS只保存 reconciliation pointer；
- Evidence staging不具 execution authority，也不直接成為 canonical architecture/validation truth；
- 單次 payload太長需要分段持久化時，分段是 write mechanism，不是多個工程 Stage；完整性規則依 `AI_CONTEXT.md`。

## Session Compaction / Rehydration Contract

長時間 ChatGPT engineering conversation 可能累積大量 search result、tool output、debug branch、舊假說與已被 supersede 的中間結論。當這些內容開始提高 retrieval cost、誤用 stale premise 或 handoff/recovery 風險時，ChatGPT 應做 **bounded session compaction**；不要等到 Context 已失控才把整段聊天摘要成另一份不可靠 authority。

適合觸發 compaction 的情況包括：

- 同一 task 已跨多個 Stage／大量 tool calls，且 current decision 只依賴其中一小部分 evidence；
- 已出現多輪被推翻的假說、重複 log/search result 或 superseded intermediate state；
- 即將進行 agent/session handoff、重新 attach repository，或需要讓後續 reasoning 從明確 checkpoint 接續；
- 目前回答開始需要反覆回找「真正 current premise／decision／next action」才能避免混淆。

不要只因聊天很長就機械式 compaction；若 current Context 仍清楚、沒有 material retrieval/handoff risk，保持原狀通常更便宜。

### 最低充分 compaction payload

Session checkpoint 只保留後續工作真正需要的 current state：

`Goal / completion criterion → Canonical pointers / identity → Confirmed material findings → Superseded assumptions only if needed to avoid regression → Unresolved evidence gaps / blockers → Current decision / state → Next authorized action / STOP condition`

一般原則：

- **Pointer over copy**：能由 GitHub／canonical source重新取得的長文件、diff、log、spec不全文複製；保存 exact repo/path/SHA/section/command或其他最低充分 pointer。
- **Current over historical**：已被新 evidence取代的細節預設不保留；只有忘掉會導致重犯已否決方案時，才保存一句 supersession reason。
- **Evidence status 要保真**：confirmed、inferred、pending、unavailable不可在 compaction時互相升格；沒有實際執行的 validation不得被摘要成 PASS。
- **Authorization 不可被摘要擴張**：Current Write Target、Task/Stage scope、permission、execution owner與 STOP boundary 在 compact後不得因語句變短而放寬。
- **Rehydrate from authority, not summary alone**：後續 session/use 若要執行 mutation、接受 completion或作高影響 decision，先依 checkpoint pointer讀 current canonical authority/evidence；session summary是 routing/recovery aid，不是新的 repository source of truth。

### Session compaction ≠ repository persistence

Compaction 是 conversation-level state management，**不自動產生任何 durable repository obligation**。

- 只有原本已通過本檔 Persistence／Coordination Admission、AI-originated Durable Work Admission Gate 與 project write allowlist 的內容，才可寫入 `TASKS.md`、Cold Registry、task dossier或 evidence surface。
- 不得因「怕摘要後忘記」就把所有 observation、future idea、tool log或 unresolved speculation寫進 repository。
- 若某 material state 若不持久化就會造成真正 project knowledge loss，先依既有 admission gate決定 No persistence／Cold／Hot，再寫入對應 canonical surface；不要讓 session summary本身變成第二套 durable memory。

### Rehydration

從 compacted checkpoint接續時，推薦順序：

`Repository / authority identity → Current task goal / scope → Referenced current canonical state → Unresolved evidence gap → Next authorized action`

若 checkpoint與 GitHub current state、project governance或新 evidence不一致，以較高 authority/current canonical state為準，更新 working context；不得為了維持舊 summary的一致性而覆蓋 current truth。

核心原則：**Compaction 的目的是刪掉不再需要的 Context，同時保存足以安全重建 current task state 的最小 checkpoint；它不是把整個聊天永久化，也不是建立新的 authority。**

## Codex Prompt 模式選擇（Prompt Mode Selection）

ChatGPT產生 Codex Prompt前，選最低充分 mode：

`TASKS Short-launch → Direct Short Prompt → Standalone Full Prompt`

### TASKS Short-launch

只有 current Hot coordination 已保存可執行 Stage，且 Codex能取得該 Stage/authority時使用。

- Prompt是 execution pointer，不是 specification container；
- 以 exact Stage identity 指向 Hot coordination / referenced active dossier；
- 要求依 repository governance做 preflight/safe sync、重讀 latest governance/current Hot contract、只執行該 Stage；
- 已保存的 evidence/scope/validation/STOP/model/context不在 launch重寫；
- launch時才新出現且 canonical尚未保存的 material information，補最低充分內容。

Short-launch預設維持短段落。**Cold Registry / Candidate item不可直接 Short-launch。**

核心原則：**Reference, don’t repeat。**

### Direct Short Prompt

沒有 canonical Hot Stage、且工作一次性、已知、低風險、低 tracking value時使用 bounded direct Prompt。只放 target、scope、必要 evidence、validation、STOP boundary，不貼完整 history。

若 Prompt開始需要大量 historical evidence、dependency、future trigger或跨 Stage state，先重新做 admission decision，而不是無限制擴寫。

### Standalone Full Prompt

只有 Codex無法存取必要 repository authority、repo尚無可靠 routing/canonical Stage、跨系統handoff必須攜帶無法取得的 context、使用者明確要求，或 evidence證明 reference不足時使用。

Standalone仍只帶最低充分 Context；self-contained ≠ 完整聊天/全部 Playbook/全部歷史 evidence。

## Prompt 建議設定與固定資訊

Codex model / reasoning / Context / Agent / execution-mode成本規則由 `CODEX_EXECUTION.md` 維護。ChatGPT依該 authority選最低充分建議。

Direct Short Prompt / Standalone Full Prompt前段至少包含 target repo/branch、推薦模型、推理強度、1–3句理由、是否值得便宜模型前置蒐證；必要時補 Context / execution mode。

TASKS Short-launch若 referenced Hot Stage已保存設定，不重複展開；可在可複製 Prompt外用一行顯示 UI 建議。

## Codex reporting contract activation

`CODEX_EXECUTION.md` 的 Codex reporting language / timestamp / Reporting Pre-Send Gate 是 always-on cross-cutting contract。Project governance已 routing到該 authority時，Prompt不需要複製完整 reporting policy；launch仍要求 Codex讀最新 project governance並啟用 contract。

Progressive Reading控制 task-specific Context，不會關閉 reporting contract。Routing有 ambiguity或 Codex無法存取 authority時，才補最低充分 self-contained contract。

## Repository routing 完成後的 Prompt 產生

目標 repository最新 governance若已：

- 宣告本手冊為 common baseline；
- 保存最低必要 Playbook routing；
- 說明 project-specific authority / exception；
- 要求依 Task讀最低必要章節；

ChatGPT後續 Prompt不再列整套 Playbook文件或複製 common policy全文。

通常只要求 Codex讀最新 project governance、current Hot task contract與本次真正相關 authority；沒有其他 canonical task contract時才補 task-specific evidence/scope/validation/STOP。

## 可直接複製的 Codex Prompt（Copy-ready Prompt Delivery）

只要內容是讓使用者直接貼給 Codex執行，不論哪種 Prompt mode，都必須：

> **One Prompt = One Copy Surface。**

全部 Codex-required instructions集中在一個 fenced code block。Prompt外可放 UI/model建議，但 Codex必須收到的內容不能散落。Alternative Prompts各自完整獨立，不把單一 Prompt拆成多個 block。

Copy-ready是 delivery contract，不是增加 Prompt長度的理由。

## Prompt lean／長度診斷

Prompt長度不是品質指標。有 canonical Hot contract時，產生最短安全 launch pointer。

TASKS Short-launch只保留 target、exact Hot pointer、必要 bootstrap與 completion/queue action；明顯膨脹時先檢查是否重複 TASKS/dossier/governance/spec。

Direct/Standalone才保存最低充分 target/task/evidence/allowed-forbidden scope/validation/success-STOP。如果仍膨脹，先判斷是否應 admission成 Hot task dossier或 evidence staging，而不是把所有內容塞 Prompt。

## Coverage-sensitive planning

單一修改不難但需完整覆蓋分散 surface時，優先：

`Bounded inventory → Checkpoint A → Focused implementation → Targeted validation → STOP → Independent coverage reconciliation → Next checkpoint → Final closure reconciliation`

Implementation session不同時負責大範圍 discovery、修改與 completeness judgment；每 checkpoint處理 coherent surface/invariant/operator flow。Model difficulty ≠ Coverage difficulty。

## ChatGPT-side Runtime Execution

ChatGPT 不只可讀取 repository 後 reasoning；當 existing project 有適合的 deterministic workload，而且目前 task / governance 允許時，也可把 sandbox 當成**受控的 ephemeral execution surface**。這個 surface只提供暫時計算能力，不取得 repository persistence/write authority，也不成為新的 source of truth。

推薦流程：

`Candidate deterministic workload → Execution Opportunity Scan → current session capability probe → current repository authority → exact workspace/commit/tree → required materialization → identity/freshness check → ChatGPT-side execution → result classification → canonical reconciliation`

### Execution Opportunity Scan

Execution Opportunity Scan 用來回答：**目前已知的 project/workload 裡，是否有一個值得由 ChatGPT直接執行、而不是只靠語言模型推演或立刻交給 Codex／CI 的 deterministic candidate？**

只在有實際訊號時做 bounded scan，例如：existing project首次採用本手冊／AI workflow review、已讀範圍直接出現 validator/parser/calculator/test/tooling、CI正在執行可在 push前重現的 deterministic check，或同一類人工解析／計算已反覆出現。不得因「ChatGPT可能會Python」就完整掃描 repository、盤點所有 runtime，或主動製造大量工具候選。

候選通常至少同時滿足：

- **Deterministic / bounded**：輸入、輸出、stop condition與 failure semantics可清楚界定；
- **Material value**：可降低人工計算錯誤、重複解析成本、remote debugging noise，或提高 validation / evidence reproducibility；
- **Existing asset or repeated need**：優先執行 repository已擁有的 project-owned tool；若工具尚不存在，至少已有反覆 deterministic workload 的真實 evidence。只有「寫個 script 也許很方便」不足以建立新 tooling obligation；
- **Safe ephemeral scope**：預設不需要 secret、production mutation、無界 daemon、實體硬體或其他目前 sandbox無法可靠提供的 authority；若確實需要，必須另依 capability／authorization判斷；
- **Governance-compatible**：目前 Task/Stage 與 repository governance允許該 execution。Repository source/docs write authority不足，**不會單獨禁止** read-only canonical materialization + sandbox computation；但也不因此取得任何 GitHub mutation權。

Opportunity 成立後才 probe **本候選真正需要的** runtime / dependency / filesystem / network capability；不為了「知道 ChatGPT能做什麼」全面列舉 sandbox。若 candidate不存在或 material benefit不足，停止 scan，正常回到 reasoning / Prompt workflow。

若 execution需要由 GitHub connector或其他 read-only source重建 filesystem snapshot，sandbox中的副本只是一個 pinned ephemeral input。GitHub／current canonical repository仍是 source of truth；執行結果是 evidence，不會因產生在ChatGPT filesystem就自動持久化，也不能覆蓋更高 authority current state。

若 scan顯示「應該新增一個 parser／validator／calculator」，該 tooling creation仍是新的 repository work：先依 AI-originated Durable Work Admission Gate與 project write boundary決定是否 admission／handoff，不能因 ChatGPT有 runtime就直接建立 repository tool。

核心原則：**先找真實 deterministic workload，再按需 probe capability；Ephemeral compute 可以擴大 ChatGPT 的計算能力，但不擴大 GitHub 寫入權或 durable authority。**

### Execution Capability Gate

ChatGPT 能產生某種語言、command 或 toolchain 的內容，**不等於目前 session 一定能執行它**。任何 ChatGPT-side program／validator／test／build／diagnostic execution 前，先通過最低充分 **Execution Capability Gate**。

執行前只確認目前任務真正需要的能力，不為形式盤點整個 sandbox：

- required runtime / compiler / shell 是否存在；
- executable/version 是否符合 project contract；
- required dependency/package/tool 是否可用；
- filesystem / working-directory / local database 等必要環境是否存在；
- 只有任務真的需要時，才確認 Git、network、external service、credential 或 hardware access。

Python、Node.js、Shell/Bash、Java、Go、Rust、C/C++ compiler、Git、SQLite 或其他工具都只是可能的 execution capability；**不得把「ChatGPT 可寫這種程式」當成 runtime 已安裝的證據，也不得把某個訂閱方案名稱當成 runtime availability contract。** 若必要 capability 不存在，標記 execution unavailable／依 `DEBUG_VALIDATION.md` 分類真正 failure/gate，不猜測 PASS。

### Canonical execution discipline

- **Execution capability 與 retrieval/network capability 分開判斷。** `git clone`、connector、archive download 或 HTTP 失敗，不代表 local runtime 不可用，也不代表 source/validator 有錯。
- **只執行 project 已擁有或目前 scope 明確建立的 command/check。** ChatGPT 有 shell、Python、compiler 或其他 runtime，不構成新增 script、修改 production source、擴張 Task/Stage 或建立 automation framework 的理由。
- **Canonical identity 要可證明。** 在 current canonical workspace 執行時使用其 Git/working-tree evidence；若由 connector／remote source 重建 snapshot，pin exact commit/tree，correctness需要時以 blob/hash/size或等價 canonical evidence確認 materialized input。不得拿 stale/local approximation冒充 current repository。
- **Execution owner 不改變 command semantics。** 同一 validator/test由 ChatGPT、Codex、CI或human執行時，其 pass/fail contract不應因 actor 改寫；誰被授權執行仍由 project governance決定。
- **Execution failure 先分類再修改。** SOURCE、TOOLCHAIN、ENVIRONMENT、INFRASTRUCTURE、SERVICE、AUTHENTICATION、AUTHORIZATION、HARDWARE_REQUIRED 與 permission/network gate分開處理；只有符合 `DEBUG_VALIDATION.md` 的 source evidence才可直接合理化 production source patch。
- **PASS 只證明實際涵蓋的 scope。** Unit test、validator、compile、schema check或script exit 0不得升格成未實際覆蓋的 security/runtime/hardware/production PASS。

### Deterministic validation placement routing

Deterministic validator／test 是否應由 ChatGPT-side、CI／independent gate或 hybrid/reduced-trigger 執行，不由本檔重複定義；依 `DEBUG_VALIDATION.md` 的 `Validation Execution Placement Gate` 判斷。

本節只負責：當 project governance與 shared placement gate允許／選擇 ChatGPT-side execution時，確認目前 session 的 runtime/toolchain capability、canonical input identity與 execution evidence boundary。誰被授權執行仍由 repository-specific governance決定。

核心原則：**ChatGPT能執行，不等於 validator就應移出CI；placement先看 shared validation gate，ChatGPT-side執行再看本節 capability contract。**

## Codex 結果 reconciliation

收到 Codex execution result後，若宣稱 GitHub tracked-file mutation、commit/push、coordination bookkeeping、branch/HEAD或其他 remote state change，在接受 completion或產生下一 Stage前，依 `DEBUG_VALIDATION.md` Completion Evidence Guard取得最低充分 remote evidence。

Codex report是 claim，不是 GitHub authority；local-only change不能被 remote read-back升格；mismatch時 STOP並依 canonical current state重建；remote evidence不可用時標記 `REMOTE COMPLETION EVIDENCE UNAVAILABLE`。

## Scope expansion 與下一步

Analysis/review/Codex result發現 out-of-scope問題時，先依本檔 **AI-originated Durable Work Admission Gate / Follow-up Gate** 與 `REPOSITORY_EXECUTION.md` coordination lifecycle判斷：只留 observation、Cold Candidate/Committed，或真正 Hot admission；不得因「順便看到」就擴張目前 Stage或製造新的 durable obligation。

發現另一 repository也需要同步時，只做 read-only analysis/handoff；write-target switch仍依 `REPOSITORY_EXECUTION.md`。

核心原則：**ChatGPT 負責把真正值得持久化的問題變成最低充分、可追蹤、可執行的 handoff；不是把所有合理建議永久化。Codex 負責在授權 Stage 內執行，GitHub／canonical evidence 負責證明結果。**