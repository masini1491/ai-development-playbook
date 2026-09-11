# Information Integrity Guards

> **Authority**：跨專案 semantic identity、derived artifact authority、durable confirmed fact ownership、evidence provenance precision／provisional-vs-settled observation／lineage independence／temporal semantics／negative observation semantics、scope-qualified status propagation、private-to-public generalization、remote snapshot consistency、search-result authority/currentness。
>
> **Read when**：目前工作涉及 aggregate/bundle identity、跨來源 synthesis、evidence metadata/provenance/independence、estimate／preflight value 與 post-execution actual 的 evidence boundary、時間或多 clock 語意、negative observation／unknown、status scope、private evidence 公開泛化、remote canonical snapshot validation、repository search hit authority，或把 confirmed fact 保存到 report／analysis／eval 等 derived artifact。
>
> 本檔只保存跨專案 integrity contract；domain-specific ID 格式、lifecycle 名稱、資料 schema、validation ladder 與公開／機密分類細節仍由各 project owner 決定。

## Semantic Identity / Container Guard

Physical container 不等於 semantic identity。

若同一檔案、bundle、batch、multi-agent report 或其他容器中包含多個可被獨立詢問、驗證、更新、取代或引用的事實／task／evidence unit：

- 每個獨立 unit 應保留自己的 stable semantic identity 或可唯一定位的 canonical identity；
- 不得只因它們共享一個 physical container，就把原本獨立的 authority、evidence、task identity 壓成單一 aggregate identity；
- container 可以是 storage / transport / presentation unit，但不得因此取得其中所有 child unit 的 authority；
- 若舊 aggregate artifact 已混合多個獨立 identities，修正時優先保留 audit provenance，建立／恢復 per-unit current identity，再把 aggregate 降為 archive、wrapper 或 derived view，而不是重寫歷史。

核心原則：**Container may group identities; it does not merge their authority.**

## Derived Synthesis Authority Guard

由既有 canonical facts、evidence、task records 或多來源結果產生的 summary、comparison、matrix、report、ranking、prompt、eval summary 或其他 synthesis，預設是 **derived artifact**。

- derived synthesis 可以形成新的分析結論，但不得冒充 underlying source fact／execution evidence／task authorization；
- 沒有新增 observation、execution、draw/cast、measurement 或其他 source event 時，不得只因產生一份新總表就創造新的 source-fact identity；
- synthesis 若需要跨來源比較，應保留足以回到各 source identity 的 provenance／pointer；
- 若 synthesis 與 source authority 衝突，先回 canonical source reconciliation，不得讓較方便閱讀的 aggregate view 靜默覆蓋 source truth；
- derived mirror／showcase／generated repository 若 freshness 會影響使用，可記錄它代表的 source revision／baseline；但 baseline pointer 只說明 derivation scope，不會把 derived artifact 升格成 source authority，也不會擴張原 source 的 publication／privacy boundary。

核心原則：**Derived synthesis may add interpretation; it does not inherit or manufacture source authority.**

## Durable Confirmed Fact Ownership Guard

若某 confirmed fact 具有跨 session、跨 task 或未來 decision 的持續價值，它不應只存在 report、analysis、prompt、eval record、conversation summary 或其他 derived artifact 裡。

在 durable reuse 前：

1. 找到該 fact 的合理 canonical factual owner；
2. 若 owner 尚未保存該 confirmed fact，先依 project governance 建立／更新 owner；
3. derived artifact 只引用或 snapshot 該 fact，並保留必要 provenance；
4. 若目前沒有 mutation authority，明確標記 canonical persistence 尚未完成，不得把 derived copy 冒充已 canonicalized。

這不要求每個一次性 observation 都建立新檔案；只有會持續影響未來 decision／retrieval 的 confirmed fact 才需要 durable factual ownership。

核心原則：**A durable confirmed fact needs a canonical factual owner before derived reuse becomes its de facto memory.**

## Provenance Precision Guard

Evidence metadata 必須保存實際可證明的 precision，不得用格式完整度冒充 evidence 完整度。

- 來源只提供分鐘級 timestamp，就保存 minute precision；不得補造秒數。
- 只知道 date、commit、runtime name、tool version 或其他單一 provenance field，不代表其他 provenance fields 已被驗證。
- `source commit known` 不等於 `raw runtime payload verified`；`command reported PASS` 不等於完整 execution environment 已知。
- unavailable／unknown／unverified 應保持原狀；可以明確標記 precision 或 verification boundary，但不得猜值填滿 schema。
- 後續取得更高精度 evidence 時，可以追加／升級 provenance；不得把後來取得的 metadata 回寫成「當時已知」。

核心原則：**Preserve evidence precision; verification does not propagate transitively across provenance fields.**

## Provisional Estimate / Settled Observation Guard

Pre-execution estimate、forecast、reservation、preflight approximation 或其他 provisional value 可以支援 planning／admission／budgeting，但**不是 post-execution actual observation，也不得只因 execution 已完成就自動升格為 settled fact**。

一般原則：

- cost、latency、token／credit usage、resource consumption、duration、size、throughput 或其他 execution quantity，若在執行前只能估算，應保留 `estimated`／`provisional`／等價 evidence status；不得以格式完整、模型精準或 historical average 為由呈現成 measured actual。
- 若 correctness、billing、quota accounting、SLA 判斷、capacity planning、completion report 或其他 material decision 依賴 settled value，且 execution surface 能取得 post-execution measurement／provider record／authoritative usage evidence，應以 actual evidence reconciliation estimate，而不是讓 preflight value 靜默成為 final truth。
- `reserved / held / budgeted / predicted / expected` 與 `consumed / billed / measured / observed / settled` 是不同 semantic states；只有 authoritative contract 明確定義兩者等價時才可合併。
- Reconciliation 可以保留 `estimate → actual → delta / settlement`，也可以只更新 current derived view；若原估算本身具有 audit、billing dispute、benchmark 或 planning-comparison 價值，不應為了方便而覆寫掉原 provisional record。
- 若 execution surface 沒有可靠 actual／settlement evidence，或本次只需 planning estimate 而 final actual 不影響 correctness，不為形式建立 accounting framework；但 user-facing／durable record 必須繼續標示它是 estimate，不得冒充 measured or settled value。
- Tolerance、rounding、provider billing unit、sampling window、reconciliation cadence 與 authoritative usage source 由 target project／service contract決定；本 guard 不寫死單一成本模型。

核心原則：**Estimate is planning evidence, not settled evidence. When a material decision depends on actual usage and authoritative post-execution evidence exists, reconcile instead of promoting the estimate by convenience.**

## Evidence Lineage / Independence Guard

多個 source artifact／repository／article／report／issue／dataset 看起來彼此不同，不代表它們形成同等數量的**獨立證據**。當「有多少份證據互相支持」會影響 confidence、research conclusion 或 implementation boundary 時，應辨識 material provenance lineage。

一般原則：

- fork、mirror、copy、translation、syndication、repackaging、共同 upstream dataset、共同 measurement run 或明顯由同一 primary source 派生的多個 artifact，預設屬同一 evidence family，除非有額外 evidence 證明其中存在獨立 observation／verification；
- independence 依 evidence 的形成來源與 causal/provenance lineage 判斷，不依 hostname、repository 數量、publisher 數量或搜尋結果數量判斷；
- 同 lineage 的多份 artifact 仍可用來確認 wording、implementation divergence、distribution 狀態或 historical propagation，但不得只靠數量把 confidence 包裝成 independent corroboration；
- 一份 primary source 加上一份真正獨立的 local observation／independent test 可以形成不同 evidence units；但 local artifact 若只是重播同一 upstream vector，不自動成為獨立事實來源；
- lineage 無法可靠判定時，標記 `LINEAGE UNKNOWN`／等價 uncertainty，避免用「多來源一致」暗示已確認獨立性；
- 不要求固定多來源。若一份高 authority evidence 已足以回答，就停止；本 guard 只防止 source count inflation，不要求為形式增加來源。

核心原則：**Source count ≠ independent evidence count. Corroboration depends on provenance lineage, not artifact count.**

## Temporal Semantics / Clock Identity Guard

同一事件常同時存在多個合法時間欄位；它們的 clock／語意不同，不得因格式相同就互換。

常見時間 identity 包括：

`source / event time → observation / acquisition time → callback / processing time → publication / effective time → derived artifact generation time`

一般原則：

- callback arrival／ingestion time 不等於 device／ECU／exchange／upstream event timestamp；retrieval time 不等於 source 最後更新時間；publication time 也不自動等於 effective time；
- 若 decision 依賴 ordering、freshness、latency、session mapping 或 deadline，應保存足以辨識 clock domain、timezone、precision 與欄位語意的 metadata；
- 不同 clock 之間只有在已建立可靠 mapping／ordering contract 時才可計算 latency 或先後；wall-clock、monotonic clock、device clock 與 remote service clock 不得直接相減後宣稱精確延遲；
- 缺少 source/event timestamp 時，可保存「observed at／received at」，但不得把 acquisition time 回填成 source time；
- derived summary／report 的 generated time 只說明 synthesis 何時形成，不會刷新 underlying evidence 的 event/freshness time；
- 只有一個時間欄且其語意明確、不影響判斷時，不為形式建立多 clock schema。

核心原則：**Timestamp format does not define timestamp meaning. Preserve clock identity before comparing time, freshness or order.**

### Reporting Wall-clock Source Guard

AI／agent 若需要「目前時間」作 user-facing reporting timestamp、acquisition/observation marker 或 clock sanity check，**時間來源本身也是 evidence decision**；不得把模型自然語言生成的時間感當成 clock evidence。

推薦 hierarchy：

`direct platform / runtime wall clock → conditional external wall-clock sanity / fallback anchor → UNAVAILABLE`

一般原則：

- execution／platform surface 若能直接提供 current wall clock，且 OS/runtime UTC、local timezone 或其他可交叉檢查的讀值彼此一致，優先使用該來源；不為形式額外連外校時。
- Model-inferred time、聊天上下文推算、上一則回覆時間、commit author/committer timestamp、檔案 mtime 或其他不是 current-clock contract 的欄位，**不得**升格為可信目前時間。
- Monotonic clock 適合量測 elapsed duration／RTT，不是絕對 wall-clock source；只有與可信 wall-clock anchor 建立 mapping 後才可推導 absolute time。
- Runtime/platform clock unavailable、明顯自相矛盾或已有 concrete stale evidence 時，才考慮 external service time 作 **sanity/fallback anchor**。External anchor 的 freshness／cache／transport semantics 必須一起判斷，不能只看一個 timestamp 字串。
- HTTP `Date` 代表 HTTP response 的時間語意，不保證每次 request 都是 fresh origin wall clock。GitHub／其他 API 的 `Date` 可受 cache、revalidation、intermediary 或秒級 precision 影響；單次 raw offset 不足以證明 local runtime clock drift。
- 需要 fresh external sanity evidence 時，可依 surface 能力使用 cache-bypass／revalidation hint、unique nonce、`Age`／`Cache-Control`／request identity 等 metadata 與多次 bounded samples；若 freshness仍無法建立，標記 `TIME SOURCE INCONCLUSIVE`，不要挑一筆方便的 sample 當標準答案。
- 外部 sample 與 coherent runtime clock衝突時，先區分 **local clock error**、**remote/cache staleness**、**transport delay/precision**；沒有足夠 evidence 不宣稱其中任一方「漂移」。
- 若 runtime clock 已可直接驗證正常，但最終 AI 回覆仍出現 `??:??`、placeholder、錯誤時區、明顯 stale timestamp 或格式缺失，優先分類為 **reporting / formatting failure**；除非另有 evidence，不反推為 system-clock failure。
- Reporting timestamp 只需符合其 contract 所要求的 precision；來源只到秒／分鐘時不得包裝成更高精度的 clock accuracy claim。

核心原則：**Use directly observed runtime/platform wall clock for reporting; use external HTTP time only as a cache-aware fallback or sanity anchor; model-inferred time is not clock evidence.**

## Negative Observation / Unknown Semantics Guard

「沒有觀察到」與「已證明不存在」是不同 evidence statement。Timeout、silence、not advertised、search miss、bounded passive observation、parser unavailable、unsupported query、empty result 或其他 negative result，只能支持其**實際觀察 contract**允許的結論。

一般原則：

- `NO X OBSERVED`／`NOT ADVERTISED`／`NOT FOUND IN CHECKED SCOPE` 等狀態預設不等於 `X ABSENT`、`X UNSUPPORTED`、`X OFFLINE` 或特定 root cause；
- 要把 negative observation 升格成 absence claim，必須有足以支持該 claim 的 coverage／sensitivity／expected-detectability contract，例如已知完整 enumeration surface、明確 authoritative registry 或能可靠排除其他 failure modes 的 measurement method；
- `UNKNOWN`、unreadable、ambiguous、timeout 或 missing metadata 不得偷偷轉成 `0`、`false`、empty、legacy、unsupported、PASS 或其他 convenient default；
- 若安全／correctness policy 要求 unknown 時停止，可以 **fail closed operationally**；但「因 unknown 而拒絕執行」仍不等於「已證明某事實為 false／absent」；
- 同一 negative result 若可能由多個原因造成，除非 observation 能區分原因，否則保持原因集合／uncertainty，不以最方便的單一原因完成故事；
- repository-level search absence 的更具體 coverage contract 仍由 `AI_CONTEXT.md` → `Absence Claim Coverage Gate` 管理。

核心原則：**Not observed ≠ absent. Unknown may block action without becoming a fabricated fact.**

## Scope-Qualified Status / Propagation Guard

`PASS`、`FAIL`、`MISMATCH`、`CURRENT`、`FROZEN`、`READY`、`SUPPORTED`、`AVAILABLE` 等 status 只有在其**semantic scope**清楚時才可可靠傳播。當不同層級／dimension 的 status 容易被誤讀成同一件事時，應附 owner／object／stage／evidence scope。

一般原則：

- 局部 arithmetic／parser／member／adapter `PASS` 不得自動擴張成 system／product／hardware／production `PASS`；validation evidence tier 的具體升格規則仍由 `DEBUG_VALIDATION.md` 管理；
- calculation `MISMATCH` 不自動等於 engineering acceptance `FAIL`；source discrepancy、execution result、engineering judgment 與 completion state 可以是不同 status dimensions；
- `requirements FROZEN` 不自動代表 architecture、provider、implementation、evidence 或 deployment topology 也 frozen；freeze／lock／ready 類標籤應說明其 decision scope；
- aggregate status 只有在存在明確 aggregation contract 時才可形成；不得用 parent label 抹掉 child status／unknown／pending；
- `UNKNOWN` 不得為了填滿 dashboard/schema 自動轉成 PASS 或 FAIL；若 workflow 需要 operational default，必須把 default action 與 factual status 分開；
- mutable status 應有一個 canonical owner；router、summary、mirror 或 derived view若複製 status，必須避免成為第二份可獨立演化的 owner。

核心原則：**A status is true only for its named semantic scope; status does not propagate across dimensions by convenience.**

## Private-to-Public Generalization / Mosaic Guard

Private／internal／customer／project-specific evidence 可以協助形成通用方法，但**不會因被摘要或去掉名稱就自動變成可公開 provenance**。當 durable artifact 要從 private evidence 進入 public／broader-distribution surface 時，應在第一次公開 durable write 前完成抽象化與 mosaic-risk review。

一般原則：

- 優先萃取 general principle／method，而不是複製 private solution；移除名稱、帳號、位置、精確 identifier、專屬 revision、unique geometry／value combination、raw screenshot、private filename／metadata 與其他可回推 source identity 的資訊；
- 去識別不能只看單一檔案。應考慮與 repository 其他公開頁面、commit metadata、圖表、數值、時間與 routing pointer 交叉比對後，是否可能重建特定 private source／project／person；
- 若要把 private-derived principle 寫成 public normative rule，優先用合法 public／primary evidence 重新驗證；若無法取得足夠 public evidence，降級為 generic caution／open question／internal-only conclusion，而不是把 private provenance包裝成 public authority；
- public derived artifact 可以在 governance允許時保存不洩密的 abstract source-baseline／freshness pointer；但 baseline 不公開 private content、不轉移 license／publication right，也不讓 public mirror 取代 private source authority；
- 先 commit raw private artifact、再靠後續 commit 刪除不算安全 sanitize；Git history／artifact cache 可能仍保留內容。若 raw evidence 必須保存，應留在允許的 private evidence surface；
- 本 guard 只定義跨專案 generalization integrity；哪些資料屬 confidential／personal／regulated，以及是否允許公開，仍由 target project governance／applicable policy 決定。

核心原則：**Private evidence may inform a public abstraction; it does not become public provenance by summarization. Review the mosaic, not only each file.**

## Original vs Retrospective Evidence Guard

後續 evidence 可以改變**目前應相信的結論**，但不得改寫「較早 decision point 當時實際知道什麼、實際判斷什麼」。若一個 engineering record 需要跨時間比較、incident review、validation backtest、experiment evaluation、behavioral eval、architecture decision trace 或其他 hindsight-sensitive用途，應把 original state 與 retrospective analysis 分層保存。

推薦最小模型：

`Original premise / evidence / decision → later observation → retrospective analysis / supersession`

一般原則：

- 原始 hypothesis、task contract、decision rationale、validation expectation、fresh-session response、measurement interpretation或其他 time-bound judgment，一旦被用作後續比較基準，不應因知道結果後而靜默重寫成較接近後來事實的版本。
- 新 production／hardware／benchmark／user-observed／external evidence 出現後，可以更新 current canonical truth、建立 supersession、追加 correction 或形成新的 decision；但要保留足以重建舊 decision point 的 original record／Git provenance。
- retrospective root-cause、postmortem explanation、backtest、reclassification 或 hindsight synthesis 應明確標示其時間與來源，不得呈現成「原本就已知道／已預測／已驗證」。
- correction 若只是 typo、轉錄錯誤或客觀 metadata repair，可以修改原 record，但應保留最低充分 correction provenance；若修改會改變原 decision semantics，優先使用新 revision／append／supersession，而不是覆寫歷史。
- project 不必為每個普通 note 建立 append-only framework；只有原始判斷本身具有 audit、comparison、validation、experiment、incident或 future decision價值時才需要此 guard。

這與 `DEBUG_VALIDATION.md` 的 evidence supersession互補：**supersession 決定現在什麼 evidence有效；本 guard 保存較早 decision point 當時究竟知道與判斷了什麼。**

核心原則：**Later evidence may change current truth; it must not manufacture hindsight into the original record.**

## Snapshot Consistency Guard

當 ChatGPT／agent 先從 remote canonical repository 取得多個檔案，再 materialize 成 ephemeral/local snapshot 交給 Doctor、validator、test harness 或其他 deterministic check 時，**同一次 validation run 的 repository inputs 必須對齊同一個 exact canonical revision**。

推薦流程：

`Resolve requested branch/ref → pin exact commit SHA / immutable revision → fetch every validation input from that revision → build snapshot → execute validator`

一般原則：

- branch／tag／moving ref 可以用來選擇目標，但開始取得 validation inputs 前應先 resolve 成 immutable revision；
- 同一次 snapshot 不得混用 `AGENTS.md@commit-A`、coordination surface `@commit-B`、validator `@commit-C`，即使三者取得時都名義上來自 `main`；
- validator 自身若屬被驗證 repository 的 canonical tooling，也應從同一 pinned revision 取得，除非 validation contract 明確指定 external/versioned validator authority；
- snapshot 只需包含 validator 真正需要的最低充分 inputs；consistency guard 不要求 full clone／full repository materialization；
- 若 connector／runtime 無法保證所有必要 input 來自同一 pinned revision，應回報 `SNAPSHOT CONSISTENCY UNAVAILABLE`／等價 evidence gap，不得把混合 revision 的 PASS 冒充單一 canonical state 的 validation result；
- validation 完成後 remote branch 已前進，不會追溯使該 run 無效；但結果只能宣稱對 pinned revision 成立。若要宣稱 current branch 最新狀態，重新 resolve current revision 並建立新 snapshot。

核心原則：**One validation snapshot, one canonical revision. Moving refs select a revision; they are not themselves a consistency boundary.**

## Search Hit Authority Guard

Repository search、全文搜尋、semantic search、code search、filename match 或其他 discovery mechanism 命中某 artifact，只證明它在被搜尋範圍內**可被發現／可能相關**；不因此取得 current、canonical、execution 或 policy authority。

推薦判斷：

`Search hit → identify owner / authority class / currentness → resolve canonical target → use or discard`

一般原則：

- 搜尋命中 historical、archive、deprecated、cold、superseded、generated summary、old task、migration note 或 stale copy 時，先回 current router／governance／canonical owner 判斷，不得因 query match 很強就直接採用；
- search result excerpt、ranking、filename、snippet freshness 或搜尋引擎排序都不是 authority signal；
- search hit 可以作 discovery evidence，幫助找到可能 owner／symbol／path；真正 decision 仍由 current canonical authority 與必要 provenance 決定；
- 若 repository 沒有足夠 routing／metadata 判定 hit 是否 current，應明確保持 uncertainty 或做 bounded reconciliation，不得自動把「找到」翻成「現在有效」；
- 這與 absence 判斷對稱：`not found` 不等於 absent；同樣地，`found` 也不等於 authoritative/current。

核心原則：**Search relevance ≠ authority. A hit locates evidence; it does not promote that evidence to current truth.**

## Boundary

這些 guards 不要求所有 project 使用 global monotonic ID，也不規定 Tarot/Vault 類的 `reflective_only`、`waiting_for_reality` 等 domain lifecycle；不替代 target project 的 confidentiality classification、validation ladder 或 domain schema。跨專案只採用上面的 identity、derived authority、durable ownership、provenance precision、provisional-vs-settled observation、lineage independence／temporal semantics、negative-observation／unknown semantics、scope-qualified status、private-to-public generalization、original-vs-retrospective evidence、snapshot consistency 與 search-hit authority 原則。