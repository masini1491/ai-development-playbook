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

## AI-facing Surface Maintenance Trigger／Routing Integrity Check

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

- 新 target 可由預期 entry path 命中，不需要依賴模型猜 path／舊聊天室／全 repo 搜尋；
- 只更新必要 router／index，不因單一 leaf mutation製造全域 derived churn；
- current authority 沒有被 historical／cold／superseded route 重新暴露或混合加權；
- parent／child、dependency、conditional pointer 等會改變 task identity／scope 的關係仍完整；
- canonical owner 變更時，舊 owner 已降為 routing／historical／compatibility role，不留下雙 authority；
- 典型 current lookup 的 routing depth、default-load Context 與需要載入的 artifact 數量沒有無理由惡化；
- 若 mutation 使 lookup 明顯變長，先判斷能否用更薄 routing、canonicalization、cold isolation 或 direct-leaf bypass 修正，而不是要求 AI 永久多讀一個 global file。

Routing integrity check 是 **bounded maintenance check，不是每次 repo-wide audit**。小型 direct-reference repository 可以只檢查一條 path；大型 registry／router 架構才需要較完整的 parent/child、authority-class、stale-route 檢查。

核心原則：**Maintenance trigger 告訴你何時重新檢查 AI 資訊架構；Routing Integrity Check 確認一次 mutation 後 AI 仍找得到唯一 current authority；兩者都不自動決定要不要拆。**

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

至少問：

- **Always-on impact**：是否增加每個 task 都要付出的 baseline Context？低頻規則是否放錯位置？
- **Default-load frequency**：誰真的需要這份資訊？能否 condition-triggered？
- **Routing depth**：新增一層後，正常 task 是否多一次 lookup？若沒有明顯 Context 節省，是否值得？
- **Duplication / reconciliation**：是否建立第二份 policy、status、inventory 或 evidence？
- **Bounded-read quality**：AI 是否仍可依 section / symbol / exact path 只讀需要部分？
- **Search noise**：舊 wording、舊 filename、superseded content是否仍會混入 normal retrieval？
- **Write closure**：允許的高頻 mutation 是否會迫使不相關 derived files一起更新？
- **Net effect**：整體 expected retrieval cost 是下降、持平，還是只是把內容拆散？

刪除內容也要檢查：少字不一定更快；若刪掉必要 router / authority declaration，使 AI 必須多次搜尋才能重建 mental model，retrieval cost 反而上升。

本 gate 不要求固定 metric、benchmark 或 token accounting；只有在 repository 規模／使用頻率值得時才建立自動化量測。

核心原則：**Rule / structure quality = correctness + authority clarity + retrieval cost。讓 AI 讀得少，不是讓 repository 變得碎；是讓它更快命中唯一且足夠的 current authority。**