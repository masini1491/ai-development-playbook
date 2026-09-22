# AI 可讀性／Context 架構（AI Readability / Context Architecture）

本檔是跨專案 **AI 可讀性、Context 載入效率、information surface responsibility、routing 與 durable project memory 分層**的主要 authority。

它回答的是：**AI 應該去哪裡讀、預設讀多少、哪些資訊應分開保存，以及 repository 結構變更會不會提高不必要的 retrieval cost。**

Git／permission、Conversation-scoped Repository Write Lock、ChatGPT 實際可直接修改哪些 path，仍由 `REPOSITORY_EXECUTION.md` 決定；本檔不授權任何 mutation。

## Section Router

- default-load／Always-on／Hot-Cold-Evidence-Current-Historical surface model → `AI Context Surface Model`、`Always-on Context Admission`
- instruction applicability／model-runtime evolution → `Instruction Applicability Lifecycle／Model-Upgrade Audit`
- information responsibility／control-data plane → `Information Surface Responsibility`、`Cross-Actor Control / Data Plane Separation`
- new surface admission／cohesion／progressive direct-leaf routing → `Independent Retrieval Intent Gate`、`Context Cohesion Gate`、`Progressive Routing／Direct-leaf Bypass`
- pre-action contract closure／required-artifact closure／absence claim／fail-fast ordering → `Action Contract Closure`、`Absence Claim Coverage Gate`、`Fail-fast Context Ordering`
- routing metadata／routing closure／AI-facing route regression → `Thin Routing Metadata`、`Routing Integrity Contract`、`Generated Routing Metadata／Drift Check`
- Hot／Cold coordination、dossier、evidence、history、freshness與 canonicalization → `Hot / Cold Coordination Semantics`、`Hot Task Dossier`、`Evidence Staging Surface`、`Historical / Search-noise Isolation`、`Current Snapshot Freshness`、`Canonicalization → Surface Slimming`
- derived metadata write closure／retention／retrieval cost／hot-path growth → `Derived Metadata Write-Closure Gate`、`Retention / Reconstruction Integration`、`AI Readability / Retrieval Cost Change Gate`

## 核心目標

> **Repository 應讓 AI 以最低充分 retrieval cost 找到唯一、最新、足夠的 authority。Correctness、authority clarity 與 AI retrieval efficiency 都是 maintainability 的一部分。**

概念上可用下式檢查資訊架構成本：

`Expected Retrieval Cost ≈ default-load frequency × loaded context + routing/search cost + reconciliation cost`

不要求實際計算 token，也不使用固定 KB／行數作 universal gate。

- 小檔若每個 task 都載入，可能比大型低頻 dossier 更昂貴。
- 大檔若可依 heading／symbol bounded-read，可能比拆成許多互相跳轉的小檔更有效率。
- 同一 policy 複製到多處的成本，不只包含字數，也包含 drift detection 與 authority reconciliation。

## AI Context Surface Model

跨專案可依實際需要採用下列資訊層；**這是 semantic model，不要求每個 repository 都建立全部檔案／目錄。**

| Surface | 主要責任 | 預設載入 | Execution authority |
| --- | --- | --- | --- |
| **Always-on** | 幾乎所有 task 都需要的穩定 governance / bootstrap | 是 | 無 |
| **Hot coordination** | current executable / critical-path work | 是或由 current task 直接載入 | 只有正式 Task/Stage authorization 才有 |
| **Hot detail** | 單一複雜 active task 的詳細 contract | 只有該 task | 由 Hot coordination 指向，不能獨立推導 |
| **Cold registry** | future / dormant / trigger-based durable memory | 否 | 無，不可直接 launch |
| **Evidence** | 實測／現場／外部 observation 與 provenance | 否 | 無 |
| **Current canonical** | architecture / protocol / validation / source 等目前正式 truth | task-specific | 依各 authority |
| **Historical / archive** | completed / superseded / archaeology | 否 | 無 |

核心原則：**Persistence authority、write authority、execution authority 與 default context-loading authority 是不同概念。** 某資訊被合法保存，不代表每個 task 都要讀，也不代表它可被執行。

## Always-on Context Admission

`AGENTS.md`、minimal bootstrap、每次 execution 都會載入的短 contract 等 **always-on surface**，每個 task 都會付出成本，因此只應保存：

- 高頻、跨任務、相對穩定的 governance；
- authority / routing / STOP boundary；
- 若省略會普遍造成安全或 correctness 問題的最低必要規則。

通常不應直接保存：

- mutable domain current facts；
- 大量 hardware measurements；
- 單一 feature implementation detail；
- long-term backlog；
- historical progress；
- 只有少數 task 才需要的完整 validation / protocol / UI contract。

低頻規則應 condition-triggered routing 到 topic owner；不要只因「這條很重要」就自動放進 every-task baseline。

## Instruction Applicability Lifecycle／Model-Upgrade Audit

`AGENTS.md`、Skills、bootstrap instructions 與其他高頻 instruction surfaces 不只佔用字數，也會改變 routing、pause／confirmation、testing、delegation 與 retry 行為；因此 **instruction surface 本身屬於 Context budget**。

當 model、agent runtime、orchestration 或 instruction-following behavior 發生 **material upgrade／material behavior change**，或已有 concrete evidence 顯示既有 instruction 造成過度 trigger、衝突、無效補丁、額外 pause／testing／delegation／retry 時，應做一次 bounded applicability audit：

- 保留仍具 stable authority、correctness、safety、user preference 或高頻 routing 價值的 instructions；
- 移除、縮窄 trigger、降為 condition-triggered routing，或移出 always-on surface 的規則，前提是它只為舊模型／舊 runtime 的具體缺陷存在，且 current behavior 已不再需要；
- 檢查互相衝突、重複、trigger 過廣，或會使小型 task 被迫載入／執行不必要 capability、validation、confirmation、delegation 的 instructions；
- 若新 runtime 已原生提供同等且可驗證的 capability，不保留一份會造成雙重 routing／雙重 ceremony 的舊補丁，除非它仍承擔獨立 authority；
- audit 只處理已能指出的 material change／behavior evidence；**不得因版本號更新、模型名稱改變或「可能更聰明」就做 repo-wide instruction rewrite。**

一條規則「最初為舊模型補缺陷而寫」本身也不是刪除理由。若它後來已成為穩定 governance、safety boundary、使用者偏好、authority declaration 或跨模型仍有價值的 operating contract，就繼續保留。

同樣地，audit 目標不是把 `AGENTS.md`／Skills 壓成最短文字；應最佳化 **minimum-sufficient, applicable, non-conflicting instruction set**。刪掉必要 authority 使模型必須重猜、重搜、重試，可能比多保留少量高價值 instruction 更昂貴。

核心原則：**Model/runtime evolution can invalidate workaround instructions, but not authority by default. Re-audit applicability only on material triggers; save wasted Context and agent work, not necessary reasoning.**

## Information Surface Responsibility

一個 AI-facing surface / field 應有一個主要語意角色。

例如：

- `TASKS.md` 不應同時充當 executable queue、永久 backlog、evidence archive、architecture truth 與 changelog；
- router/index 不應同時保存 routing、current status、工程結論與歷史 evidence；
- `Status:` 不應靠一段混合文字同時表示 software result、hardware pending、下一步與歷史原因。

若 AI 必須先讀大量內容才能分辨哪些句子是 instruction、current truth、evidence、history 或 future possibility，代表 information ownership 已混合。

這不是「一個概念只能一個檔案」規則；同一檔案可以有多個 section，但每個 surface 的 primary responsibility 應清楚。

## Cross-Actor Control / Data Plane Separation

多個 actor／agent 協作時，若 receiving actor 能直接從 current authoritative source 取得 repository、artifact 或 evidence，actor-to-actor transport 預設只攜帶最低充分的 **control state**，不要把 control message 當成大型 canonical data 的搬運通道。

可概念性區分：

- **Control plane**：goal、scope、authority-relevant state、bounded decision／status、canonical pointer、next action／STOP condition。
- **Data plane**：file body、diff、log、test output、repository state、execution evidence 與其他應由 current authoritative source 取得的資料。

一般原則：

- Receiving actor 能可靠 direct-read current data 時，優先 `pointer / identity → direct retrieval`，不要在 Prompt、handoff、agent message 或 coordination record 重複複製長 file／diff／log。
- Control-plane report 只證明 sender 傳送的 coordination state；它不自行證明 referenced data-plane state、repository completion 或 validation truth。當 decision／completion materially 依賴 current evidence 時，receiver 仍應取得最低充分 current evidence。
- 若 receiving actor 無法取得 required data plane、跨 system handoff 必須攜帶不可重取的 artifact，或 exact transport 本身就是 requirement，才使用 admitted minimum-sufficient artifact handoff，並保留 provenance／identity／integrity boundary。
- 不以固定 byte、token、line count 決定 control／data 分層；boundary 由 information responsibility、authority、retrievability 與 evidence semantics 決定。
- 不得為了迎合 transport／tool payload limitation 而扭曲 canonical repository architecture；transport recovery 與 information ownership 是不同問題。

核心原則：**Coordinate through the smallest sufficient control plane; retrieve substantive current evidence through its authoritative data plane whenever possible. Control state ≠ data evidence.**

## Independent Retrieval Intent Gate

建立新文件、task dossier、evidence dossier、router 或其他 durable artifact 前，先問：

> **它是否形成一個可以被獨立詢問／引用／載入，而且與既有 owner 有清楚 responsibility boundary 的 retrieval intent？**

只有資料變多、來源變多、檔案變長，不足以單獨構成拆分理由。

一般原則：

- 能自然更新既有 canonical owner，就不要為形式新建檔案。
- 若某一小段只有特定 task 才需要，而且留在 always-on / hot index 會迫使大量無關 task 載入，獨立 dossier 可能合理，即使它不大。
- 若大型文件仍高度 cohesive，且能用 Section Router / heading / symbol 精準 bounded-read，可保持聚合。
- 不以固定 KB、行數、段落數作 universal split threshold。
- Input artifact count ≠ canonical artifact count；十份來源／log 不代表要建立十份 canonical conclusion files。

## Context Cohesion Gate

Context optimization 不只檢查「能不能少讀」，也要檢查拆分後 AI 是否仍能可靠重建本次 reasoning 所需的共同 premise。

> **Context 優化應沿著已穩定的 evidence、retrieval intent 與 ownership boundary 進行；不要只為降低當下載入量，就把仍在共同演化的 reasoning unit 硬拆開。**

Active campaign／Stage 若仍高度共享 mutable premise、blocker、validation boundary、next action 或 production constraint，過早拆成多個 dossier／surface 可能降低單次 loaded context，卻增加 cross-file reconciliation、drift、stale premise 與 partial retrieval 的成本。

拆分前至少確認：

- Stage／evidence boundary 已足夠收斂；
- relevant canonical evidence 已 reconcile；
- current status、blocker、validation boundary 與 next action 已穩定到可被明確引用；
- 舊 premise 已標示 superseded，或不再需要跨新 surface 共同維護；
- 新單元具有獨立 retrieval intent 與清楚 ownership；
- 拆分後不需要高頻 cross-file synchronization 才能維持 correctness。

若上述條件尚未成立，可先用 section-level bounded read、Hot/Cold 分流、pointer 或其他低風險 slimming；等 evidence／Stage boundary 收斂後再進行第二輪 information architecture 拆分。

核心原則：**Progressive Reading 減少不必要載入；Context Cohesion Gate 避免把仍必須共同理解的資訊拆到難以可靠重建。不是越拆越快，而是在正確收斂點拆，才真正降低 end-to-end retrieval cost。**

## Progressive Routing／Direct-leaf Bypass

推薦 routing 思路：

`Minimal bootstrap → domain / owner selection → page / symbol selection → canonical target → expand only if evidence gap remains`

一般原則：

- Router 是 **disambiguation tool，不是 ceremony**。若 stable metadata、exact task identity、path、symbol 或 current pointer 已唯一命中 canonical target，直接讀 target；不要為了流程完整強迫多讀中間 router。
- **Section Router entry order is not execution order, authority precedence, or mandatory reading order.** Route directly to the minimum-sufficient owner／leaf；procedural order comes from the selected canonical contract。
- 大型 policy / docs 優先 section-level bounded read；大型 source 優先 `symbol/function cluster → caller/callee → file expansion`，不要一開始全文載入。
- 跨 topic 只讀真正參與本次 decision / execution / validation 的 sections；「相關」不等於「必讀」。
- Available context ≠ required context；資訊存在不代表本次必須載入。

### Session-local Verified Context Reuse

同一 session 已經以 current canonical evidence 確認 repository／ref、route、owner、leaf 或其他 task-relevant authority 後，若沒有 material freshness／scope trigger，可直接重用已載 Context；**不要為 routing ceremony 在每個 follow-up 重複 fetch、probe 或重跑相同 owner discovery。**

推薦流程：

`Verified current route / owner / leaf → reuse while material premises stay stable → freshness / scope trigger → cheap identity / bounded-diff probe → selectively invalidate / reload affected Context`

一般原則：

- 同一 follow-up、同一 narrow intent 或同一 canonical owner，且 currentness 不影響新結論時，沿用已確認 route／owner；只讀新出現的最低必要 leaf／evidence。
- Material trigger 包括：使用者／governance 明確要求 latest/current、concrete stale evidence、repository/ref identity 改變、剛完成會影響本題 authority 的 mutation、task scope／owner／authority materially 改變，或 current decision correctness 明確依賴 freshness。
- Identity／HEAD unchanged 時，保留已載 Context，不為形式重讀 canonical files。
- Identity／HEAD changed 時，先 bounded 比較 changed owners／paths／dependencies；只有與本題 material 相關的 Context 才 invalidated / reload。無關變更只更新 observed identity，不重建整個 mental model。
- 若 changed surface 可能透過 shared premise／generated metadata／cross-owner dependency 影響目前已載內容，或 bounded coverage 無法證明 selective reload 足夠，應擴張 rehydration 到最低充分共同 owner；必要時 STOP 在 freshness evidence boundary。
- Pinned SHA／tag／project-declared immutable baseline 仍是 authority；看到 upstream newer HEAD 不得自行把 pinned baseline升級。
- Session reuse 是**已驗證 Context 的 reuse**，不是 conversation memory 升格為 canonical authority；一旦 material trigger 成立，仍回 current authority reconciliation。

核心原則：**Reuse verified Context until something material invalidates it；freshness 應做 selective invalidation，不應預設 full reload。**

### Cross-boundary Revision Continuity

當一個 handoff、execution result、completion-driving artifact或其他跨 actor／session／execution boundary 的 artifact，會讓 consumer 依賴某個 **mutable revision-bearing object** 做後續 execution、acceptance或planning 時，producer 與 consumer 必須維持最低充分 revision continuity；不得只靠 conversation memory、自然語言 summary或「剛才應該沒變」推定 currentness。

推薦語義：

`producer observes exact revision → transport minimum identity → consumer resolves current revision → compare → bounded reconciliation → continue / repair / STOP only as required`

一般原則：

- **Only materially relied-upon objects participate.** 只有 producer 的 handoff／result correctness 實際依賴其 mutable state時才要求 transport revision identity；不得為形式讓所有 artifact 都攜帶所有可觀察 SHA／version。
- **Minimum transport identity**：至少能唯一辨識 semantic object、declared ref／baseline，以及 producer 實際觀察到的 exact revision。Git object 可用 exact commit SHA；其他系統可使用其 authoritative immutable revision／digest／version identity。格式完整不得補猜未觀察值。
- **Observed revision is provenance, not a pin.** Floating ref 在 producer觀察到某 SHA／revision後仍是 floating；該 observed revision只記錄 handoff／result形成時的 provenance，不會自行把 current project authority改成 pinned baseline。
- **Acquisition mechanism may differ; semantic object must match.** 不同 actor／runtime可以用不同合法工具取得 revision evidence，但比較前必須確認兩邊解析的是同一 object／ref／authority role；不得把 remote canonical revision、stale local tracking ref、pre-fetch local HEAD或其他不同語義的 revision直接當成同一值比較。
- **Same revision**：consumer確認 current revision與producer-observed revision一致時，可 reuse仍適用的 verified Context／contract，不為形式全文reload或重跑既有 evidence。
- **Changed revision**：revision不同只代表觸發 reconciliation，**不自動等於 FAIL、rollback、舊execution無效或全部 evidence失效**。先 bounded比較 changed owners／paths／dependencies與本 boundary實際依賴：
  - 差異與本次 authority／scope／procedure／validation／acceptance premise無 material關聯 → 保留既有結果並繼續；
  - 差異有 material影響但可在 current authority內相容修復 → selective reload、repair／reconcile、最低充分 revalidation後繼續；
  - 差異使原 actor／scope／Stage／permission／validation或 acceptance premise不再成立 → 只停止受影響 action，回 current authority做 revision／re-admission／revalidation；不得照舊 artifact慣性執行。
- **Unresolved current revision**：applicable mutable object 的 current revision無法可靠建立時，affected execution／acceptance action保持 unresolved並 fail closed；可繼續最低充分 read-only recovery，不得把舊 observed revision冒充 current truth。
- **Historical execution fact ≠ current acceptance.** Consumer使用較新 revision時，不得回頭改寫 producer在較舊 revision下實際已發生的 execution／observation。新版可以使 current acceptance、continuation或validation需要補充／失效，但 historical execution fact仍依其原 provenance保存。
- **Transport is required; verbose presentation is conditional.** Applicable continuity metadata必須能讓consumer取得，但正常一致時應compact／quiet；只有 mismatch、unresolved或 material impact需要對使用者展開差異與處置。上位contract不要求每次輸出固定status taxonomy。
- **Pinned authority**：current project authority明確是 immutable SHA／tag／version時，確認consumer仍使用同一pin即可；看到 upstream newer revision不構成 mismatch，也不得自行升級。

這個 contract處理跨 boundary 的 revision continuity；各 domain owner仍負責「何時該 object materially applicable、如何取得 current revision、實際 transport shape、mutation／validation／completion evidence」。不得因本節建立新的 universal metadata framework或要求每個 command反覆 probe。

核心原則：**Carry the revision that materially shaped the artifact, compare it with the consumer current authority/state, and reconcile only the affected assumptions. Revision mismatch is a reconciliation trigger, not an automatic failure.**

### Action Contract Closure

Progressive Routing 可以省略與目前工作無關的 owner／section，但**不得在治理某個 action 的最低充分 canonical contract 尚未完成解析前，就跨越該 action boundary。** `Minimum-sufficient reading` 限制的是需要載入多少 Context，不是允許只遵守已讀到的部分規則。

推薦流程：

`Proposed action → identify applicable canonical contract(s) → close minimum-sufficient prerequisites → ACTION READY → perform action → applicable post-action / pre-send / completion verification`

一般原則：

- **Action boundary 先於 action。** 即將產生 executable artifact、發出具 side effect 或 evidence impact 的 tool call、執行 mutation／program／validation、建立 handoff，或形成會驅動後續工作的正式 claim 前，先確認本 action 所需的 current canonical contract 已解析到足以安全執行；不得「先做再補讀」。
- **Closure 是 scoped，不是全文閱讀義務。** Exact owner／section／stable pointer 已知時 direct-leaf；只載入會 material 改變 authority、scope、procedure、validation、STOP 或 output contract 的最低充分內容。不得把本 gate 解讀為每次 action 前全文讀完 Playbook／owner。
- **Unresolved contract blocks only the affected action.** 必要 owner／identity／prerequisite 尚未能建立時，標記該 action unresolved／blocked 並繼續合法的 bounded read-only recovery；不要把單一 action blocker 擴張成整個聊天室停止，也不得用 memory／舊聊天／未驗證 cache 補成 current contract。
- **Cross-cutting activation 仍由其 owner 宣告。** 若 current authority 已把某 contract 定義為 always-on 或 conditional cross-cutting prerequisite，該 action 的 closure 必須包含它；本節不複製各 domain 的 prerequisite 清單，也不自行啟用不適用的 owner。
- **Closure ≠ execution evidence。** 讀完／解析完 governing contract只代表 action 可以開始；實際 artifact、tool result、mutation、validation、reporting 或 completion 是否合規，仍由對應 owner 的 post-action／pre-send／read-back／completion gate驗證。
- **Existing pre-action gate remains authoritative.** Repository identity、workspace capability、runtime capability、GitHub response-shape、delegation、validation或其他 owner 已有更具體 pre-action contract時，直接依該 owner執行；本節只提供共通 sequencing invariant，不建立第二份 domain policy。

#### Required Artifact Contract Closure

當 action 最終產生 **user-facing、handoff、executable、machine-consumed 或 completion-driving artifact**，且 applicable canonical owner 已宣告 required elements／metadata／authorization／identity／evidence fields 時，final artifact 必須對每一個 applicable requirement 完成最低充分 closure；不得只驗格式或位置就假設內容已存在。

通用檢查順序：

`Applicability → Presence → Placement → Authority / Evidence Source → Content Boundary → Final Artifact Closure`

- **Applicability**：先確認 requirement 是否真的適用於 current actor／mode／artifact／condition；optional 或 condition-triggered element 不因本節被升格成 universal required field。
- **Presence before placement**：適用的 required element 必須真的存在。**Placement check 永遠不能替代 presence check；缺失的 element 不會只因「沒有放錯位置」就 PASS。**
- **Placement**：required element 存在後，再確認它位於正確 surface／field／copy boundary；例如 UI launch metadata、executable body、machine manifest、final report 可以有不同 placement contract。
- **Authority / Evidence Source**：artifact 只能承載已由 applicable authority／evidence 建立的 identity、authorization、status 或 recommendation；不得因 artifact 需要某欄位就自行製造 authority、補猜 current state 或把 presentation surface 升格成 truth owner。
- **Content Boundary**：required element 必須帶到最低充分、可用的語義；空殼 placeholder 不算 closure，也不得為了「完整」把 repository-owned canonical contract／history／evidence 全文複製進 artifact。
- **Final Artifact Closure**：pre-send／pre-execution／completion gate 若適用，必須對**最後實際要送出／執行／持久化的 artifact**檢查上述 closure；planning 階段曾經考慮過某 element，不等於 final artifact 仍包含它。

各 domain owner 繼續擁有「哪些 element 在何種條件下 required、合法 exemption、實際 shape 與 evidence semantics」；本節只提供共通 closure method，不建立 universal artifact schema、固定欄位清單或第二份 domain policy。

核心原則：**Progressive reading permits selective loading, not partial compliance. Close the minimum canonical contract before crossing the action boundary；對 applicable required artifact element，先證明 presence，再檢 placement／authority／content boundary，最後以實際 final artifact closure。**

### Absence Claim Coverage Gate

Progressive Reading 的 STOP 條件取決於本次要支持的 **decision／claim**，不是 AI 目前已載入多少 Context。尤其 repository-level 的 negative claim（例如「不存在」、「缺少」、「尚未實作」、「沒有對應 contract／tooling」）需要比單一 positive lookup 更廣、但仍 bounded 的 retrieval coverage。

> **Not found in current Context ≠ absent from repository。Minimum-sufficient Context 的 `sufficient` 必須相對於本次 claim 所需的 evidence coverage。**

對 capability inventory、competitive comparison、productization gap analysis、architecture maturity review或其他 whole-repository／whole-Playbook review：

- 先把真正要判斷的 capability／claim拆成 bounded lookup units；不要因 review scope較廣就無條件全文掃描所有文件。
- **Positive claim**：找到 current canonical owner／implementation／tool／test／stable pointer 的充分 positive hit後，可停止該 capability分支；不需要為證明「有」而繼續掃描全 repository。
- **Negative claim**：宣稱 repository缺少某能力前，至少檢查合理 router、可能 canonical owner與可用的 repository search／stable machine surface；若命中相關 section／symbol，再 bounded-read該 target確認語意，而不是因 filename或目前已讀 topic沒出現就判 absent。
- Search沒有命中也不是 universal proof of absence；若 search/index capability不完整、branch/ref不明、permission受限或可能 owner未被涵蓋，應把結論降為 `NOT FOUND IN CHECKED SCOPE`／等價 evidence-bounded表述，而不是 repository-level absence。
- Capability可能分散為 **policy/spec、executable implementation、test/eval evidence、distribution/activation adapter** 等不同成熟層。找到其中一層後，要依使用者真正比較的層級描述「已有 spec、尚無 runner」或「已有 routing contract、尚無 machine manifest」，不要把「沒有某一 implementation layer」誤寫成「整個 capability不存在」。
- Cross-owner coverage不改變 authority：找到的 current canonical owner仍是語意 authority；router/search只是 discovery evidence，不成為第二份 policy。

典型 bounded path：

`Claim → CHAT_INIT / project router → likely canonical owner(s) → heading/symbol/repository search → positive hit STOP；若仍未找到 → coverage sufficiency check → bounded negative conclusion`

核心原則：**Presence 可由充分 positive evidence成立；absence必須有與 claim scope相稱的 bounded coverage。省 Context不是提早下結論，而是在足以支持結論時停止。**

### Fail-fast Context Ordering

當本次 task 有多個 prerequisite artifact / authority 可能需要讀取時，除了「讀得少」，也應優先安排**最能以低成本否決後續 work / Context 的資訊**。

推薦思路：

`Repository / authority → task goal / scope → current canonical premise → detailed design / source / evidence`

這不是固定讀取模板；實際順序依 task authority 與風險決定。核心是：

- 若較早的 authority / goal / scope 已顯示 repository、target、permission、premise 或 completion criterion 不成立，立即停止載入原本依賴它的後續 implementation detail；
- 先讀「一旦不成立，就能省掉大量後續 Context」的高 leverage artifact，再讀昂貴 design/source/evidence；
- fail-fast 只停止已被否決的分支，不得拿低 authority summary 取代仍必要的 canonical evidence；
- 若後續 artifact 才具有真正 decision authority，仍必須讀到該 authority，不能為了節省 Context 提前下結論。

核心原則：**Context ordering 應讓錯誤 premise 儘早失敗；不要先花大量成本理解一條之後才發現根本不該執行的路徑。**

## Thin Routing Metadata

Routing metadata 的責任是**幫 AI 找到該讀的 canonical content**，不是建立第二份 content/state database。

Router / index / manifest 優先只保存：

- stable ID / alias；
- path / slug / symbol；
- kind / domain / owner；
- entrypoint / pointer；
- 其他真正用於 routing 的最低 metadata。

除非它本身就是 canonical owner，不應複製：

- volatile current status；
- verification result；
- architecture conclusion；
- protocol value；
- evidence；
- 標準版次／freshness snapshot。

**Routing Metadata ≠ State Cache ≠ Content Summary。** Stale router 比沒有 router 更容易誤導 AI。

Top-level router 的大小應主要隨穩定 domain / owner 數量成長，不應隨 leaf artifact 數量線性膨脹；leaf keyword 不要全部塞回 always-on index。

### Stable machine identity vs human wording

若 repository 有 machine-readable routing，穩定 identity 優先使用 ID、path、slug、symbol 或其他結構識別；不要讓 README wording、顯示標題或翻譯文字成為唯一 routing key。

人類標題可以改善、翻譯或改 wording，而不應無必要破壞 machine routing identity。

## Routing Integrity Contract

Routing correctness 不只表示「target file 存在」。對任何 AI-facing bootstrap／router／manifest／index／stable pointer，應能以最低充分 evidence 證明：**declared intent 能到達實際存在、語意適用、authority 唯一且不無理由惡化 hot path 的 canonical destination。**

本 contract 是跨專案方法論，不規定 universal `CHAT_INIT.md`、`PLAYBOOK_INDEX.json`、Section Router、manifest schema或 checker。每個 adopter 應把自己的 bootstrap、router、manifest、canonical owner與 ordinary hot path 對應到下列檢查；小型 direct-reference repository 可用 bounded manual review，大型／高頻 repository 才在有實益時建立 project-local deterministic checker。

Routing integrity 分成四個互補層級：

- **Structural routing integrity**：宣告的 path／owner／section／stable ID／router destination 真實存在、可解析且沒有非法 duplicate／broken edge。這類 objective invariant 適合 deterministic `FAIL`。
- **Discovery closure**：會 materially 改變 **activation、owner selection、actor selection、authority、execution、validation 或 ordinary hot-path loading** 的 first-order routing decision，至少要有一條 bounded、可發現的 current route；不得要求模型先猜到某 owner 適用，才能找到會告訴它該 owner 適用的規則。
- **Authority / hot-path integrity**：route 不得建立第二份 policy/state authority，也不得只為形式讓 ordinary task 多載 global owner、額外 hop或重複 reconciliation。`Routing completeness ≠ every rule indexed`；leaf rule不因存在就必須升格為 global capability ID。
- **Behavioral routing correctness**：當「這個 intent 是否會命中正確 upstream decision」無法由 structure alone 證明時，用 bounded fresh-session／scenario evidence驗證；static pointer PASS 不得冒充 semantic routing PASS。Behavioral evaluation semantics仍由 `DEBUG_VALIDATION.md` 擁有。

Routing-affecting mutation 建議依序 closure：

`affected intent → expected entry surface → structural edge / target check → first-order discovery closure when applicable → authority uniqueness → ordinary hot-path cost → deterministic routing check when admitted → behavioral regression only when structural evidence is insufficient`

### Maintenance Trigger / Growth Budget

AI-friendly repository 不能只在第一次設計時成立；bootstrap、router、registry、index、coordination surface 與 canonical owner 會隨專案成長，因此應有 **repository-defined growth budget／maintenance trigger**，在 AI 讀取路徑開始退化前觸發 bounded information-architecture review。

Budget／trigger 可依 repository 規模與使用型態定義，例如：

- always-on／router surface 持續增長，使大多數 task 被迫載入更多無關 Context；
- routing entry／active item 數量已使單一 index 難以 bounded-read；
- 同一 domain 已形成多個穩定、可獨立檢索的子主題；
- current lookup 經常需要打開過多 canonical artifacts 才能回答一個穩定問題；
- historical／cold／superseded material 經搜尋後常被誤當 current authority；
- router/index 開始複製正文、volatile status 或 evidence，而不再只是 routing metadata；
- 新 canonical owner 存在，但 bootstrap／index／parent router 無法可靠命中。

**Playbook 不規定 universal KB、行數、entry count 或固定 depth。** Project 可自行設定可操作的 budget，但超過 budget 只代表「需要檢查」，不代表自動拆檔、建立新 router 或刪除歷史。實際 restructuring 仍須通過 `Independent Retrieval Intent Gate`、`Context Cohesion Gate` 與本檔的 `AI Readability / Retrieval Cost Change Gate`。

### Canonical／routing mutation 後的最低充分 integrity check

只要本次 mutation 新增、移動、重新分類、supersede 或替換 AI 會需要找到的 canonical artifact／information surface，應做最低充分 routing integrity check：

`Bootstrap / known entry → relevant router / owner → current canonical target → sufficient then STOP`

至少確認：

- routing surface 宣告的 file／owner／section／router／stable ID destination 真實存在且語意適用；「file exists」不足以證明其宣告的 nested router／section也存在；
- 新 target 可由預期 entry path 命中，不需要依賴模型猜 path／舊聊天室／全 repo 搜尋；
- 若 mutation涉及 first-order routing decision，human／machine／project-native discovery surface至少有一條符合實際 consumer 的 bounded route；不要求所有 leaf rule都被全域索引；
- 只更新必要 router／index，不因單一 leaf mutation製造全域 derived churn；
- current authority 沒有被 historical／cold／superseded route 重新暴露或混合加權；
- parent／child、dependency、conditional pointer 等會改變 task identity／scope 的關係仍完整；
- canonical owner 變更時，舊 owner 已降為 routing／historical／compatibility role，不留下雙 authority；
- 典型 current lookup 的 routing depth、default-load Context 與需要載入的 artifact 數量沒有無理由惡化；
- 若 mutation 使 lookup 明顯變長，先判斷能否用更薄 routing、canonicalization、cold isolation 或 direct-leaf bypass 修正，而不是要求 AI 永久多讀一個 global file。

Routing integrity check 是 **bounded maintenance check，不是每次 repo-wide audit**。小型 direct-reference repository 可以只檢查一條 path；大型 registry／router 架構才需要較完整的 parent/child、authority-class、stale-route 檢查。

核心原則：**Maintenance trigger 告訴你何時重新檢查 AI 資訊架構；Routing Integrity Check 確認一次 mutation 後 AI 仍找得到唯一 current authority；兩者都不自動決定要不要拆。**

### Optional Deterministic Hot-path Regression Guard

Repository 已有反覆 retrieval pain、高頻 AI 使用、machine routing metadata 或 routing regression evidence 時，可以把**可機械判定的 hot-path invariants**做成 lightweight deterministic check；這是條件式 maintenance mechanism，不是所有 repository 的必備 framework。

適合直接 `FAIL` 的通常是 correctness／routing integrity invariant，例如：

- required routing target 不存在；
- stable ID／route 發生非法 duplicate；
- routing-only schema 混入被 project 明確禁止的 state／content authority field；
- manifest／router 指向錯誤 owner、非法 path 或無法解析的 canonical target；
- project 已明確定義的 generated routing metadata 發生 deterministic drift。

適合作為 `WARN`／architecture review signal 的通常是 growth／cost heuristic，例如 always-on bytes、router size、entry count、routing hop depth、manifest growth 或其他 project-local budget。除非 repository 已有獨立 correctness evidence 與明確 contract，**不要把這類 heuristic 升成 universal hard failure。**

一般原則：

- 不建立跨 repository universal KB、行數、entry count、hop depth 或 token threshold；project-local threshold 只代表其自身 workload 的 review budget。
- Checker 驗證 structure／routing invariant，不複製 canonical policy／status／工程結論成第二份 authority。
- 新增 checker 本身也必須通過 maintenance-value／retrieval-cost 判斷；小型 direct-routing repository 若 bounded manual check 更便宜，就不要為形式自動化。
- Hot-path guard 不要求一次清理全部 legacy；主要形成 **forward ratchet**，防止新的 AI-facing mutation 在沒有 concrete retrieval／correctness benefit 時持續惡化 common path。
- 若 warning 長期沒有 decision value、false-positive noise 過高或 checker maintenance cost 超過捕捉到的 regression value，應縮減／移除，而不是因存在就永久保留。

核心原則：**Deterministically fail broken routing; review growth as a signal. Guard the hot path without turning local heuristics into universal correctness law.**

### Optional Context Budget Regression Gate

若 repository 的 high-frequency／always-on AI-facing surface 已能由實際 runtime／scanner semantics **deterministically enumerate**，且 recurring workload 顯示 Context growth 值得 machine-assisted regression control，可以建立 repository-specific Context budget；這是 opt-in guard，不是 Playbook-wide mandatory framework。

- Budget 可以使用穩定且可重現的 local proxy，例如 bytes、token-equivalent estimate、entry／frontmatter size 或其他與實際載入集合有直接關係的 metric；**不要求 exact tokenizer**，但應說明 metric／估算來源與已知 error boundary，不把 approximate accounting 冒充 exact token truth。
- 不建立跨 repository universal token／byte ceiling。Threshold 只代表該 repository 已量測 workload 的 regression budget；dynamic／無法可靠枚舉的 Context surface 繼續使用本檔 semantic gates，不為了量化製造假的精度。
- Legitimate feature／governance growth 若確實需要提高 budget，應在**同一 change evidence**中同時更新 baseline／ceiling與理由，使 budget growth 成為可 review 的顯式 decision，而不是靜默漂移。
- Context reduction 已落地並有 representative evidence 時，可將 ceiling **ratchet down** 鎖住改善；不要只因單次較小 measurement 就自動收緊，避免把 noise 變成 future false positive。
- Budget regression 預設屬 growth／cost signal；除非 repository 已明確把某 deterministic limit 定義為 correctness contract，超標不應自動等同功能錯誤。
- 若 metric 與實際 retrieval cost 的關聯失真、runtime loading semantics 已改變、false-positive noise 高，或維護 checker 的成本超過保護 common path 的價值，應重新校準、縮減或移除。

核心原則：**Measure only enumerable high-frequency Context; use project-local ceilings as a forward ratchet, not a universal correctness law.**

## Generated Routing Metadata／Drift Check

若 routing metadata 可以由 canonical structure 可靠推導，而且 workload 證明值得維護，優先 deterministic generation / check，避免人工維護第二份 inventory。

例如可由 current tracked paths 推導 manifest，再用 CI / verifier 檢查 missing / stale / extra entry。

但不得為形式建立 generator；小型 repository 用 bounded direct routing 更便宜時保持簡單。

任何 tracked derived metadata 仍必須通過下方 **Derived Metadata Write-Closure Gate**。

## Hot / Cold Coordination Semantics

`TASKS.md`、`BACKLOG.md`、active task dossier 的實際 write allowlist 與 opt-in mode 由 `REPOSITORY_EXECUTION.md` 定義；本節只定義 AI loading / semantic responsibility。

### Hot coordination

Hot surface 只保存 current executable / current critical-path coordination。

- Ready / executable now；
- 阻擋目前 progression 的 current blocker；
- 目前 campaign 的必要 Hardware/User/Production validation；
- next action 已成立的 dependency / checkpoint。

Hot index 應保持可快速建立 current mental model。若單一 Hot task contract 本身很長，可在 project opt-in 後把詳細 body 放入 **Hot task dossier**，Hot index 只保存 identity、current status、pointer、最低必要 critical-path delta。

### Cold registry

Cold surface 保存值得長期記得、但目前不應進 executable Context 的 future memory，例如：

- dormant / trigger-based work；
- future feature；
- non-blocking pending validation；
- long-term architecture debt；
- 等待第二個 consumer／未定期硬體／外部 trigger 的工作。

Cold registry **不具 execution authority**。Codex／execution agent 不得因讀到 Cold item 就直接執行。

Trigger 成立或使用者選中後：

`Read current authority → reconcile premise/evidence → promote to Hot coordination → 再依正常 Task/Stage authorization launch`

Cold registry 預設不在 ordinary bootstrap 載入；roadmap/debt review、trigger evaluation、使用者指定 cold item或 Hot surface 明確指向時才讀。

### Pending / Blocked 依 critical path 分類

`Pending-validation`、`Blocked` 本身不決定 Hot / Cold：

- 阻擋目前 progression、next evidence 已可取得或屬 current campaign → Hot；
- non-blocking、未定期 external/hardware trigger、目前其他工作可正常前進 → Cold。

## Candidate vs Committed Durable Work

Cold registry 可依 project 需要區分：

- `CANDIDATE`：AI／review 提出，值得保留重新評估，但尚未決定專案一定要做；
- `COMMITTED`：已確認未來需要處理，只是目前不是 Hot。

這兩者不要求所有 project 使用固定 status 字串；重要的是**AI-originated suggestion 不因被保存就自動變成 project obligation**。

**Persistence does not increase recommendation authority。** 一個 AI 建議被寫進 repository，不會因此比當初更正確、更必要；後續仍應回到原 evidence、decision、trigger 與 current authority重新判斷。

## Hot Task Dossier

大型 active task 若把完整 evidence、validation matrix、scope、STOP condition 全塞進 Hot index，會讓所有其他 task付出 Context 成本。Project 可 opt-in 獨立 Hot task dossier，例如 `tasks/active/*.md` 或 project-defined equivalent。

一般原則：

- Hot index 保存 task identity、current state、pointer、critical dependency；
- dossier 保存該 task 的完整 execution contract；
- 只有執行／review 該 task 時才讀 dossier；
- dossier 不因存在而取得 execution authority，必須由 current Hot coordination 明確引用；
- task 完成後不把 completed dossier永久留在 normal active search surface，依 project retention / Git history處理。

## Evidence Staging Surface

**Long-form evidence is not task specification。** 硬體實測、現場觀察、長 log／command-response、外部測試 evidence 不應因 ChatGPT write boundary 被迫塞進 executable queue 當 relay。

Project 可 opt-in 專用 evidence staging surface，例如 project-defined `evidence/inbox/*.md`。

Evidence staging：

- 保存 observation / provenance / measurement condition，不具 execution authority；
- 預設不在 ordinary bootstrap 載入；
- 只有 reconciliation、validation review、使用者指定或 task pointer需要時才讀；
- staging evidence ≠ canonical architecture / validation truth；正式結論仍需 reconciliation 後由 canonical owner吸收；
- canonical owner吸收後，coordination surface優先收斂成 pointer + task-local delta，不維護第二份完整事實。

### Sanitize before first Git write

Evidence 在第一次進 Git **之前**就必須符合 repository privacy / secret / public-safety contract；不得先 commit raw credential、token、MAC、私人 endpoint、家庭內網、個資或其他禁止材料，再靠後續刪除「清理」。Git history 仍會保留先前 commit。

敏感 raw artifact 若真的需要保存，優先留在 repo 外；Git 只保存允許的 redacted digest、metadata、hash 或非敏感 pointer。

### Logical evidence completeness

若單次 tool/runtime payload 無法一次寫入長 evidence，可以 deterministic chunked persistence；但 chunking 是 write mechanism，不是多個工程 Task。

一份 logical evidence 應有可判讀的 completeness contract，例如：

`INCOMPLETE → COMPLETE`

或 manifest / expected-parts / final read-back 等價機制。**只有完整 artifact 才能作正式 reconciliation input**；不得在 part 2/3 時把半份資料誤當完整 evidence。

大量 raw serial/log/CSV/JSON 若有保存價值，可與 AI-readable evidence summary 分層；raw artifact 預設不載入，只由 dossier按需要指向。

## Historical / Search-noise Isolation

Historical、superseded、archived material 應清楚標示並預設不進 current task context。

若 semantic/code search 無法天然排除 history，repository 可在有實際噪音 evidence 時採用 `archive/` / `history/` 或其他結構隔離；不要只靠文件第一行寫 Historical，就假設所有 retrieval tool 都會先尊重它。

Normal task 取得 historical snippet 時，先辨識其 authority / freshness，不得因 wording 命中就與 current canonical evidence 等權。

詳細 completed execution history 優先依 Git history 保存；active docs 不維護冗長 Prompt-era changelog。

## Current Snapshot Freshness

任何自稱 `Current` 的 summary / status snapshot 若複製 canonical state，應有清楚 owner 與 freshness/update trigger；否則優先只做 routing，不複製 mutable current state。

Router/index 特別不應為方便顯示而長期 cache volatile status。

若 current snapshot 已 stale，應先以 canonical current evidence重建；不要因它位於 README / checklist / index 就給予較高 authority。

## Canonicalization → Surface Slimming

Evidence、decision、architecture 或 validation conclusion 一旦被正式 canonical owner吸收，Hot/Cold/evidence surface應移除重複全文，只保留：

- pointer；
- 尚未被 canonical owner吸收的 current delta；
- 仍需要追蹤的 trigger / completion / pending information。

Coordination surface不是第二份 canonical truth；Git history保存已完成的演進。

## Derived Metadata Write-Closure Gate

一個合法 ChatGPT-writable / high-frequency coordination surface 的 mutation，不應無必要強制同步修改其 write allowlist 外的 README、manifest、project-scale snapshot、showcase或其他 derived artifact。

若存在這種 dependency，先重新判斷：

1. derived metric / manifest 是否真的需要把 coordination / evidence / history 算進 canonical scope；
2. 是否可由 runtime / CI / deterministic read-time generation 取得，而不 commit snapshot；
3. 是否可延後到真正修改 canonical technical artifact 的 Stage 再 reconcile；
4. 是否應調整分類，使 operational project memory 不污染 implementation / canonical technical documentation metric；
5. 只有 dependency 真正是 correctness / release contract 時，才要求同 transaction closure。

**不要為了 derived bookkeeping 擴大 ChatGPT write authority。**

例如 project-scale 想呈現 implementation size 時，`TASKS.md`、`BACKLOG.md`、task dossier、evidence inbox、archive 等 operational memory 通常不應只因是 Markdown 就被混入「技術文件規模」，否則每次 planning mutation 都會製造無關 README churn。

## Retention / Reconstruction Integration

Project 一旦新增 BACKLOG、task dossier、evidence staging 或其他 durable memory surface，應同步判斷其 backup / retention / required-file / restore contract。

不要讓 AI 長期 memory在正常使用時存在，卻在 repository reconstruction、backup、migration、public/private sync 或 recovery 時被漏掉。

是否需要 retention manifest 仍依 project 風險與既有機制決定；不為每個小 repo建立新 framework。

## AI Readability / Retrieval Cost Change Gate

新增、刪除、搬移、拆分、合併規則／文件／source boundary／router／coordination surface 時，除了 correctness 與 authority，也必須檢查 AI retrieval impact。

若正在檢討 **adopter repository 的 ordinary AI hot path**，先確認 shared Playbook activation 是否本來就屬於該 hot path；project-native conditional-activation semantics仍由 `ACTIVATION_ADAPTERS.md` → `Conditional Activation / Adoption ≠ Activation` 擁有。不要先假設 Playbook 已 activation，再只優化 activation 後的 router／manifest／Context。

至少問：

- **Always-on impact**：是否增加每個 task 都要付出的 baseline Context？低頻規則是否放錯位置？
- **Default-load frequency**：誰真的需要這份資訊？能否 condition-triggered？
- **Routing depth**：新增一層後，正常 task 是否多一次 lookup？若沒有明顯 Context 節省，是否值得？
- **Duplication / reconciliation**：是否建立第二份 policy、status、inventory 或 evidence？
- **Bounded-read quality**：AI 是否仍可依 section / symbol / exact path 只讀需要部分？
- **Search noise**：舊 wording、舊 filename、superseded content是否仍會混入 normal retrieval？
- **Write closure**：允許的高頻 mutation 是否會迫使不相關 derived files一起更新？
- **Net effect**：整體 expected retrieval cost 是下降、持平，還是只是把內容拆散？

### Hot-path growth ratchet

新的 AI-facing mutation 不應在沒有 concrete retrieval／correctness／scope-isolation benefit 時，惡化一般高頻 task 的最低充分 working set，例如增加 always-on Context、固定 routing hop、重複 reconciliation 或不必要的 tool round-trip。

- Ratchet 主要約束 **new mutation**；既有 legacy 不因歷史大小自動 `FAIL`，可依實際 retrieval pain 漸進 normalize。
- 若新增一層 routing／metadata／checker，應能指出它換來的 precision、correctness、scope isolation、Context 節省或 regression detectability；只有「結構比較完整」不足以合理化成本。
- Common path 變長不必然錯；但增加的 retrieval cost 必須有本題或可重複 workload 的 material benefit，而不是 ceremony。

刪除內容也要檢查：少字不一定更快；若刪掉必要 router / authority declaration，使 AI 必須多次搜尋才能重建 mental model，retrieval cost 反而上升。

本 gate 不要求固定 metric、benchmark 或 token accounting；只有在 repository 規模／使用頻率值得時才建立自動化量測或 deterministic hot-path guard。

核心原則：**Rule / structure quality = correctness + authority clarity + retrieval cost。讓 AI 讀得少，不是讓 repository 變得碎；是讓它更快命中唯一且足夠的 current authority。**
