# AI 可讀性／Context 架構（AI Readability / Context Architecture）

本檔是跨專案 **AI 可讀性、Context 載入效率、information surface responsibility、routing 與 durable project memory 分層**的主要 authority。

它回答的是：**AI 應該去哪裡讀、預設讀多少、哪些資訊應分開保存，以及 repository 結構變更會不會提高不必要的 retrieval cost。**

Git／permission、Conversation-scoped Repository Write Lock、ChatGPT 實際可直接修改哪些 path，仍由 `REPOSITORY_EXECUTION.md` 決定；本檔不授權任何 mutation。

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

## Information Surface Responsibility

一個 AI-facing surface / field 應有一個主要語意角色。

例如：

- `TASKS.md` 不應同時充當 executable queue、永久 backlog、evidence archive、architecture truth 與 changelog；
- router/index 不應同時保存 routing、current status、工程結論與歷史 evidence；
- `Status:` 不應靠一段混合文字同時表示 software result、hardware pending、下一步與歷史原因。

若 AI 必須先讀大量內容才能分辨哪些句子是 instruction、current truth、evidence、history 或 future possibility，代表 information ownership 已混合。

這不是「一個概念只能一個檔案」規則；同一檔案可以有多個 section，但每個 surface 的 primary responsibility 應清楚。

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
- 大型 policy / docs 優先 section-level bounded read；大型 source 優先 `symbol/function cluster → caller/callee → file expansion`，不要一開始全文載入。
- 跨 topic 只讀真正參與本次 decision / execution / validation 的 sections；「相關」不等於「必讀」。
- Available context ≠ required context；資訊存在不代表本次必須載入。

### Absence Claim Coverage Gate

Progressive Reading 的 STOP 條件取決於本次要支持的 **decision／claim**，不是 AI 目前已載入多少 Context。尤其 repository-level 的 negative claim（例如「不存在」、「缺少」、「尚未實作」、「沒有對應 contract／tooling」）需要比單一 positive lookup 更廣、但仍 bounded 的 retrieval coverage。

> **Not found in current Context ≠ absent from repository。Minimum-sufficient Context 的 `sufficient` 必須相對於本次 claim 所需的 evidence coverage。**

對 capability inventory、competitive comparison、productization gap analysis、architecture maturity review或其他 whole-repository／whole-Playbook review：

- 先把真正要判斷的 capability／claim拆成 bounded lookup units；不要因 review scope較廣就無條件全文掃描所有文件。
- 本 Playbook 自身的 whole-repository capability discovery可先讀 `CAPABILITY_INDEX.md` 作薄 discovery surface，再回 canonical owner確認；一般 project只有在自己明確提供等價 index時才使用。Discovery index不成為第二份 authority。
- **Positive claim**：找到 current canonical owner／implementation／tool／test／stable pointer 的充分 positive hit後，可停止該 capability分支；不需要為證明「有」而繼續掃描全 repository。
- **Negative claim**：宣稱 repository缺少某能力前，至少檢查合理 router、可能 canonical owner與可用的 repository search／stable machine surface；若命中相關 section／symbol，再 bounded-read該 target確認語意，而不是因 filename或目前已讀 topic沒出現就判 absent。
- Search沒有命中也不是 universal proof of absence；若 search/index capability不完整、branch/ref不明、permission受限或可能 owner未被涵蓋，應把結論降為 `NOT FOUND IN CHECKED SCOPE`／等價 evidence-bounded表述，而不是 repository-level absence。
- Capability可能分散為 **policy/spec、executable implementation、test/eval evidence、distribution/activation adapter** 等不同成熟層。找到其中一層後，要依使用者真正比較的層級描述「已有 spec、尚無 runner」或「已有 routing contract、尚無 machine manifest」，不要把「沒有某一 implementation layer」誤寫成「整個 capability不存在」。
- Cross-owner coverage不改變 authority：找到的 current canonical owner仍是語意 authority；router/search只是 discovery evidence，不成為第二份 policy。

#### Final Negative-Claim Reconciliation

Whole-repository／whole-Playbook review 的 negative claim 可能不是在 retrieval planning 時就存在，而是在比較、評分或 final synthesis 過程才新生成。因此 **Absence Claim Coverage Gate 必須在最終回答前再執行一次**，不能只在最初 routing 階段做。

推薦 closure：

`Draft synthesis → extract material negative/gap claims → per-claim capability/index/router/likely-owner check → bounded canonical read → maturity-layer correction → final answer`

- 把草稿中會影響評價／推薦／產品定位的「缺少／沒有／尚未實作／不支援／仍需補」逐條視為新的 evidence obligation。
- 若該 claim 是 synthesis 階段才出現，必須重新走 bounded existence check；不得因前面已做過一次 repository review就假設 coverage自然包含這個新 claim。
- 對本 Playbook可先用 `CAPABILITY_INDEX.md` 找 owner，再讀 canonical target；若 index未列出該 capability，仍可用 `CHAT_INIT.md` router、合理 owner與 repository search補 coverage。**Index miss ≠ repository absence。**
- Repository search／connector search miss只能作 discovery evidence，不能單獨關閉 negative claim；若已知 search coverage不可靠，優先使用 router／index／known owner直接讀取。
- 找到任一 maturity layer後，先修正 claim scope，例如 `contract exists; automated harness not evidenced`；只有相稱 coverage仍無 positive evidence時，才允許 whole-repository absence wording。
- 若時間／Context／permission不足以完成 closure，保留 evidence-bounded wording，不要為了給完整排名而補猜。

核心原則：**Negative-claim coverage 既是 retrieval gate，也是 synthesis closure gate；AI 最後新想到的「缺點」也必須重新接受 repository evidence查證。**

典型 bounded path：

`Claim → CHAT_INIT / capability index / project router → likely canonical owner(s) → heading/symbol/repository search → positive hit STOP；若仍未找到 → coverage sufficiency check → bounded negative conclusion`

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

若 repository 有 machine-readable routing，穩定 identity 優先使用 ID、path、slug、symbol 或其他結構識別；不要讓 README wording、顯示標題或自然語言摘要本身變成唯一 machine identity。

這不表示每個 repository 都必須新增 YAML / JSON manifest；只有當現有 Markdown router、path / symbol lookup 或搜尋已不足以維持可靠 routing，且新增 machine surface 的收益高於 write closure / drift 成本時才建立。

## Derived Metadata Write-Closure

新增 machine-readable index / manifest / generated metadata 前，必須同時定義 write closure；否則 derived metadata 很快變成 stale authority trap。

至少要回答：

- canonical owner是誰；
- metadata是 hand-maintained、generated還是 hybrid；
- canonical source變更後誰／什麼流程更新 metadata；
- stale如何被 deterministic detect；
- metadata mismatch時哪一方優先；
- 是否真的有 consumer使用這個 surface。

若無法回答，優先不要建立新的 derived metadata layer。

核心原則：**Read optimization 必須有 write closure。沒有更新／驗證路徑的 machine index，不是免費 Context optimization，而是新的 reconciliation debt。**

## AI Readability / Retrieval Cost Change Gate

任何新增、刪除、搬移、拆分、合併 AI-facing rule / file / router / information surface 前，先檢查 end-to-end retrieval cost，而不是只看單檔大小。

至少比較：

1. **Default-load cost**：是否讓更多 task 每次都讀更多內容？
2. **Routing cost**：AI為了找到 canonical target是否需要更多 hops / search / intermediate docs？
3. **Reconciliation cost**：是否新增重複 policy、summary、metadata或可能 stale的 derived state？
4. **Write-closure cost**：canonical content變更後，是否多出必須同步更新的 index/manifest/cache？
5. **Failure cost**：如果漏讀／讀錯／metadata stale，會造成什麼實際錯誤？

只有總體收益清楚時才新增 surface；若只是「看起來比較結構化」，但沒有 consumer、沒有 failure evidence或會建立 dual authority，維持現況通常更好。

## Routing Integrity Check

新增／搬移／重新命名 canonical section、router、entrypoint或 derived routing surface後，至少做一次 bounded integrity check：

`Bootstrap / known entry → relevant router / owner → current canonical target → sufficient then STOP`

確認：

- 新 target可由合理入口找到；
- 舊 pointer沒有成為主要 dead-end；
- 不需要為找到一個 leaf讀取不相干的大量文件；
- Cold／Historical／superseded surface沒有被誤升格為 default/current authority；
- 新 router/index沒有複製 volatile state或建立第二份 policy authority；
- 沒有為了形式增加無必要 routing depth。

若 integrity check顯示 AI需要更多 Context才能找到同一份 authority，或新 surface容易 stale，應回退／簡化，而不是再疊一層 router修補。

核心原則：**Routing change 必須改善或至少不惡化 end-to-end retrieval；「多一個 index」不是自動改善。**
