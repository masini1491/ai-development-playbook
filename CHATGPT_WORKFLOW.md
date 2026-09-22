# ChatGPT 專案聊天室工作流（ChatGPT Project Conversation Workflow）

本檔是 **ChatGPT／planning conversation** 的主要 authority，負責 ChatGPT 在工程專案聊天室中的 planning、coordination admission、Codex Prompt 產生與交付、Codex 結果 reconciliation，以及 ChatGPT-specific conversation delivery delta。

跨 actor／跨 workflow 的 substantive user-facing reporting、timestamp與 Reporting Pre-Send Gate由 `REPORTING.md` 擁有。本檔不重新定義 Codex execution、Git／permission、coordination surface lifecycle、AI Context architecture、validation 或 architecture policy；需要時路由到對應 canonical 文件。

## Section Router

- cross-actor回覆語言／result-first／scope fidelity／timestamp／Reporting Pre-Send Gate → `REPORTING.md`；ChatGPT-specific progress rendering → `ChatGPT Reporting Delta`
- task contract／clarification／scope exclusion → `Task Contract：Goal / Context / Exclusions`
- durable work／Hot-Cold admission／follow-up → `Persistence／Coordination Admission`、`AI-originated Durable Work Admission Gate`、`Task Identity / Revision Gate`、`Follow-up / New Work Gate`
- 長 session compaction／freshness／handoff → `Session Compaction / Rehydration Contract`
- actor 選擇／Codex handoff／Prompt mode → `Actor Admission / Handoff Gate`、`Codex Prompt 模式選擇`、`Prompt 建議設定與固定資訊`、`Child Delegation Forecast`、`Child Delegation / Profile-Override Authorization Handoff`
- copy-ready Prompt／launch settings separation／Prompt slimming／last-mile enforcement → `可直接複製的 Codex Prompt`、`Prompt Artifact Separation / Canonical Shapes`、`Codex Prompt Pre-Send Gate`、`Prompt lean／長度診斷`
- ChatGPT sandbox／deterministic runtime → `CHATGPT_RUNTIME_EXECUTION.md`
- Codex completion reconciliation → `Codex 結果 reconciliation`
- repository write／permission／Git boundary → `REPOSITORY_EXECUTION.md`
- Codex model／reasoning／Agent／execution cost → `CODEX_EXECUTION.md`

## 核心流程

一般專案聊天室優先遵循：

`Current repository / authority → Lowest-sufficient evidence → Persistence / coordination admission decision → Actor admission → Prompt mode only if handoff is needed → Draft Prompt → Prompt Pre-Send Gate → Execution / handoff → Canonical result reconciliation → Next decision`

ChatGPT 的角色是建立正確 task contract、選擇最低充分 authorized actor / execution handoff、維護 current coordination scope，並用 canonical evidence 接受或拒絕 completion claim；不是把既有 repository authority 重新抄成第二份 specification，也不是把每個「看起來有道理」的改善建議自動變成專案義務。

## ChatGPT Reporting Delta

所有 ChatGPT substantive user-facing engineering replies先遵守 `REPORTING.md`；本檔只保留 conversation actor真正不同的 delivery delta。

- ChatGPT timestamp literal使用 `回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`（或合法 timezone override）；timestamp source／final-line／UNAVAILABLE semantics不在此重複。
- analysis／architecture／review／recommendation、coordination decision、Codex Prompt delivery、Codex result reconciliation、STOP／blocker／completion等只要形成 substantive user-facing reply，都適用 shared reporting contract。
- ChatGPT-specific planning schema、Prompt artifact、session handoff與result reconciliation仍由本檔後續 sections擁有。

### Progress Visibility

當 current work有有限、可辨識且有決策價值的 stages／checks／items時，ChatGPT可附簡潔 progress indicator，例如 `██████░░░░ 60%〔3/5 stages〕`；這是可選的 conversation presentation aid，不是 completion signal。

Percentage／denominator／subset scope／blocker visibility等 integrity rules直接服從 `REPORTING.md` → `Progress Integrity`；open-ended work不為了視覺完整捏造百分比。單步、低風險或 indicator不增加決策價值時省略。

## Task Contract：Goal / Context / Exclusions

複雜 task contract 應讓 AI 快速辨識「這次真正要做什麼」，不要把 goal 埋在長背景裡。

需要時可分：

- `goal / question`：本次唯一主要工作；
- `completion criterion`：何時才算完成；
- `context`：會改變判斷但不是 execution instruction 的背景；
- `dependencies / evidence pointers`；
- `exclusions`：本次明確不判斷、不修改、不驗證的範圍。

**Context 可以很多，但主要 goal 必須可直接辨識。** 同一 field / surface 不要同時混合 current status、歷史 evidence、future idea 與 execution instruction；AI-facing information responsibility 的跨專案規則見 `AI_CONTEXT.md`。

### Agent-Normalized Contract／Minimal Clarification Gate

完整 task schema／Prompt contract 是 **Agent 的正規化責任**，不是要求使用者逐欄填寫的表單。ChatGPT 應先從使用者當次自然語言、current repository authority、已確認 context 與安全可推導的 project defaults 提取已知欄位，再只針對真正會改變 decision／execution 的缺口澄清。

推薦流程：

`Natural-language request → Extract known contract → Normalize safe defaults / N/A → Identify decision-changing uncertainty → Ask minimum necessary clarification only if needed → Proceed at the narrowest safe scope`

一般原則：

- 能由使用者當次訊息或 current canonical context 明確取得的 goal、target、scope、completion、constraint，不要求使用者用另一套固定格式重填。
- 只有缺少資訊會實質改變 **task identity、target repository、scope、completion criterion、authority、permission、execution feasibility、validation requirement 或安全邊界** 時，才需要澄清。
- 澄清只問最低必要問題；若一個問題就足以解除 blocker，不把整份 internal schema／checklist丟給使用者。
- 能安全標成 `N/A`、project-defined default 或 current canonical value 的欄位，直接正規化；不得為形式製造 user friction。
- 若資訊不足但可在清楚縮小 scope 後安全處理，優先 reduced scope，並明確保留未判斷／未授權部分；不要要求與當前 decision無關的資料。
- Internal schema 可以比 user-facing input 更完整；除非使用者要求 audit、正式 record、copy-ready technical contract 或 debugging trace，不需要把全部 normalization detail 展示出來。
- 這個 gate 不授權猜測 project fact、permission、secret、runtime capability 或 high-impact premise；遇到這類 material uncertainty 仍須回 canonical authority 或 STOP。

核心原則：**Contract completeness is an agent responsibility；clarification cost 只應隨 genuinely missing、decision-changing uncertainty 增加。**

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

ChatGPT在 planning時負責**做 admission decision**，但不重新定義 coordination surface semantics或 repository write mechanics：

- Hot／Cold／Candidate／Committed semantic responsibility、critical-path與 default-load policy → `AI_CONTEXT.md` → `Hot / Cold Coordination Semantics`
- persistence surface availability、write allowlist、promotion／execution admission與 completion bookkeeping → `REPOSITORY_EXECUTION.md` → `Coordination Lifecycle / Admission`

推薦 planning decision：

`No persistence → Cold admission（project有合法 Cold surface時）→ Hot admission`

### No persistence

若本次 observation／recommendation沒有 material durable tracking value，或不保存不會造成 current project work loss，維持 conversation-local，不為「完整」建立 repository item。

### Cold admission

當工作值得 durable memory、但依 current `AI_CONTEXT.md` semantics不是 executable／critical path，且 project已合法 opt-in Cold surface時，ChatGPT可提出／執行 Cold admission。Cold不直接 Short-launch；trigger成立後仍需 current reconciliation與 Hot promotion。

### Hot admission

當 current work依 `AI_CONTEXT.md` 已屬 executable／critical path，且 repository persistence authority成立時，ChatGPT才 admission到 current Hot surface。Hot admission不自行擴張 implementation actor、source mutation或 validation authority。

### Pending / Blocked 不自動等於 Hot

ChatGPT不以 `Pending`／`Blocked` label本身決定 admission；直接依 `AI_CONTEXT.md` 的 critical-path classification，然後把結果交給 `REPOSITORY_EXECUTION.md` 的合法 persistence action。

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

### Proactive New-Session Handoff Gate

Bounded compaction 與 fresh-session handoff 是不同強度的 conversation-state action。當同一聊天室的可觀察 session-health risk 已高到「繼續在原 session reasoning」比「建立最低充分 checkpoint 後重新 rehydrate」更容易誤用 stale premise、遺漏 constraint 或增加 recovery cost 時，ChatGPT 應**主動建議從下一個適當 Stage／decision boundary 開新聊天室接續**；不要等到實際 context failure、明顯失憶或使用者主動抱怨才處理。

可支持主動 handoff 的 material signals 包括：

- current answer 已反覆需要重新定位 current premise／decision／authority，才能避免被大量舊 branch 或 superseded state干擾；
- 使用者需要糾正先前已明確成立的 material constraint／evidence／scope，且原因與長 session 的 stale-context confusion一致；
- 同一 session 已跨多個 Stage、大量 tool output／search evidence，而下一階段只需要其中一小部分 current working set；
- 已做過 bounded compaction／checkpoint，但不久後又出現相同 retrieval confusion 或 stale-premise風險；
- 下一步即將進入 architecture freeze、completion acceptance、repository mutation、deployment／external mutation或其他高影響 decision，而目前 session-health risk 足以 materially影響 correctness。

一般原則：

- **不要捏造 context meter。** 除非 execution surface 明確暴露可信的 current-context／remaining-capacity metadata，ChatGPT 不得宣稱「已用掉 X%」「只剩 Y tokens」或用猜測的 hidden threshold當 handoff evidence；有可靠 meter時也只把它當一項 evidence，不取代 observable correctness/retrieval signals。
- **Length alone ≠ handoff trigger。** 聊天很長但 current working set仍清楚、canonical pointers穩定、沒有 material stale/retrieval risk時，不為形式反覆催使用者換聊天室。
- 若 material risk 可在本 session 用一次 bounded compaction／canonical reconciliation安全消除，先採較低成本手段；若風險仍存在，或剛好位於自然 Stage boundary，主動建議 fresh session。
- 建議 handoff 時先完成**最低充分 checkpoint**；可使用 `SESSION_HANDOFF_TEMPLATE.md` 或等價 payload，但不複製整段聊天。Checkpoint 保持 evidence status、scope、permission、STOP condition 與 canonical pointers，不把 summary升格成 current truth。
- Fresh session 必須依下方 Rehydration contract重新確認 current repository／authority；**new chat ≠ inherited authority**。
- Handoff recommendation 是 conversation-level recovery decision，不自動建立 TASKS／Cold item／durable obligation，也不擴張 repository write、execution、deployment或credential authority。
- 若下一步 correctness materially依賴已受污染／無法可靠 reconciliation 的 context，先停在 handoff boundary；若只是成本／便利性改善而非 correctness blocker，清楚建議新聊天室即可，不把它假裝成安全性 STOP。

推薦流程：

`Observe session-health signals → bounded compaction / canonical reconciliation if sufficient → material risk remains? → minimum checkpoint → recommend fresh session → fresh-session canonical rehydration`

核心原則：**不要等到聊天室真的失控才換；也不要假裝知道隱藏 token 百分比。以可觀察的 stale/retrieval risk 判斷何時 fresh-session handoff 比繼續累積同一 Context 更可靠。**

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

**Recovered context / identity ≠ recovered authority.** Rehydration artifact 即使成功恢復 repository identity、task context、routing 或 continuity，也只恢復 knowledge / orientation；它不會自行恢復 mutation、completion acceptance 或 high-impact decision authority。進入 authority-sensitive action 前，仍須由對應的 current authoritative source 重新建立當下 authority。

若 checkpoint與 GitHub current state、project governance或新 evidence不一致，以較高 authority/current canonical state為準，更新 working context；不得為了維持舊 summary的一致性而覆蓋 current truth。

長期 project chat 即使沒有發生 compaction，也不得把 session 開始時載入的 actor 分工視為永久 current。當 **Stage 完成、task responsibility materially 改變、準備建立 Codex handoff，或 current Playbook / project governance 可能已演進且會影響 actor choice** 時，做一次 bounded actor-routing rehydration：只重讀會改變本次 actor / authority / capability decision 的 current sections，不全文重載 Playbook。若 current authority與 responsibility均未 material 改變，則沿用已確認 contract，避免 per-message rehydration成本。

核心原則：**Compaction 的目的是刪掉不再需要的 Context，同時保存足以安全重建 current task state 的最小 checkpoint；它不是把整個聊天永久化，也不是建立新的 authority。長期聊天室在 responsibility transition仍需 bounded rehydrate current actor routing，不能靠舊分工慣性決定下一個 executor。**

### Playbook Freshness Probe

Generic session-local verified-context reuse、material freshness trigger、cheap identity／bounded-diff probe、selective invalidation／reload 與 freshness evidence gap，統一由 `AI_CONTEXT.md` → `Session-local Verified Context Reuse` 擁有。本節只保存 **Playbook baseline-specific delta**。

- **Floating declared baseline**（例如 project governance 明確採用 current/latest `main`）：當 `AI_CONTEXT.md` 的 material freshness trigger成立，對該 declared ref做最低成本 identity probe，再依 generic selective-invalidation contract只重讀受影響的 Playbook owner／section。
- **Pinned SHA／tag baseline**：該 pinned baseline本身是 project authority；看到 upstream newer HEAD、經過一段時間或另一 session已有新版，都不得自行升級。只有 current project governance／使用者合法改變 baseline時才切換。
- **Playbook-specific material boundary**：Stage／task responsibility改變、準備 Codex handoff、repository mutation／completion acceptance，或其他 decision若 correctness materially依賴 Playbook current actor／authority／validation／reporting contract，可構成 generic freshness trigger；若不影響本次 decision，不為形式 probe。
- Playbook identity probe只回答 declared baseline/ref identity；它不授權 repository write、execution、deployment、credential、external-service action，也不取代 target project自己的 current governance read-back。

核心原則：**Generic freshness semantics live in AI_CONTEXT；本節只決定 declared Playbook baseline如何參與 freshness。Floating baseline按 material trigger檢查，pinned baseline不自動漂移。**

## Actor Admission / Handoff Gate

**Codex handoff 不是 project workflow 的預設下一步。** ChatGPT 在準備產生 Codex Prompt、或上一個 Stage 完成準備決定 next action 時，先判斷目前工作真正需要哪個 actor。

推薦流程：

`Next work → decompose materially distinct responsibilities → resolve current Stage/task responsibility per responsibility → current authority + capability → lowest-sufficient authorized actor per responsibility → ChatGPT direct work + residual handoff | single-actor execution | STOP`

一般原則：

- 官方／外部資料 retrieval、bounded research、fixture / corpus 蒐集、provenance、comparison、schema / edge-case synthesis、read-only review，以及目前 session可安全完成的 deterministic evidence processing，若 current authority／capability已允許 ChatGPT完成，**以該 responsibility 為單位**優先由 ChatGPT直接完成；同一整體工作另有 residual coding-agent mutation，不會自動取消這個 ChatGPT-direct判斷。
- **先拆 responsibility，再看 mutation。** 一個工作同時包含高量 research／evidence／reasoning／synthesis 與較小的 downstream repository mutation 時，不得只因最後 artifact 需要另一 actor寫入，就把整段 upstream work一起分派給該 actor。對每個 materially distinct responsibility 分別選 lowest-sufficient authorized actor；另一 actor只接真正需要其 unique authority／capability 的 residual work。
- **Cost-aware 不等於 correctness downgrade。** 在候選 actor都能維持相同 authority、evidence與completion標準時，應考慮 scarce Codex quota／usage、Context與大量 retrieval成本、重複 research、retry與handoff overhead；ChatGPT能以較低 scarce-agent成本安全完成的 responsibility，預設留在 ChatGPT。不得為省成本降低 validation、source authority、security、privacy或必要 deterministic execution。
- **Action access ≠ responsibility assignment。** Read/write permission、connector capability或runtime capability只回答某 actor能否執行某 action；current Task／Stage responsibility回答誰擁有這段工作。Permission/capability不得反向製造 responsibility，也不得把 artifact persistence executor自動升格成整個 Stage executor。
- **已成立的 Stage assignment 先遵守，成本優化走 revision。** 若 current admitted Stage已明確把某 responsibility分派給另一 actor，ChatGPT不得只因自己也能做就靜默吸收；若新 evidence顯示存在 materially cheaper且仍合法的 decomposition，先依 `Task Identity / Revision Gate` revision同一 Stage的 actor split並完成 canonical read-back，再按新分工執行。
- Residual handoff必須避免重做已完成 upstream work：Prompt／handoff只攜帶最低充分 established result、evidence pointer、remaining mutation／validation與STOP boundary；除非 current evidence顯示 upstream result stale／insufficient，不要求 receiving actor重新做整份 research。
- Production/application/firmware source、executable tests、build/dependency/tooling、CI/release/deploy只是常見 implementation artifacts，**artifact type alone does not select Codex**。只有 `Project AI mode: ChatGPT+Codex`，而且 current project governance／authorized Stage把本次 required mutation明確分派給 coding-agent responsibility時，才進 Codex handoff；`ChatGPT-Only` 則由 ChatGPT在其實際 authority／capability交集內執行或 STOP。
- **Previous actor ≠ next actor。** 上一 Stage由 Codex完成，只代表上一 Stage需要Codex；不能用它作下一 Stage的 actor evidence。
- Project已進 implementation phase也不代表所有後續 research / evidence / fixture工作都屬 Codex；phase決定 write boundary的一部分，但 actor仍依 current responsibility判斷。
- ChatGPT capability也不是無條件 direct-execution authority。需要 runtime/tool時仍依 `CHATGPT_RUNTIME_EXECUTION.md` → `Execution Capability Gate`；需要 repository mutation時仍依 `REPOSITORY_EXECUTION.md` 的 current write boundary。
- 若 actor choice受 stale session context影響，先依本檔 `Session Compaction / Rehydration Contract` 做 bounded actor-routing rehydration，再決定；不得要求使用者用「不用 Codex 就能做？」之類提醒來解除 handoff inertia。

核心原則：**Choose the actor from the current work, not from the previous Stage. Handoff is a decision, not a habit.**

## Codex Prompt 模式選擇（Prompt Mode Selection）

只有 `Actor Admission / Handoff Gate` 已判定目前工作確實需要 Codex handoff，才選最低充分 Prompt mode：

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

**Root launch settings 是給使用者操作 Codex UI／launch surface 的 metadata，不是 Codex executable task instruction。** 每次 ChatGPT 交付 **user-facing Codex handoff** 時，除非下列 explicit exemption 成立，final response **MUST** 在 copy-ready fenced Prompt **外面**提供最低充分 root launch recommendation；不要為了固定欄位把它們塞進 Codex execution body。

最低 required launch metadata：

- `Root model`
- `Root reasoning`
- `Why`
- `Cheap-model evidence pass`

`Context / execution mode` 只有在 materially 影響 launch 時才需要。

Explicit exemptions 只有：

- 使用者明確要求 **prompt-only output**；
- 使用者或 current authority 已明確固定本次 root profile，不需要 ChatGPT 再做 recommendation；
- current execution surface 不提供 user-selectable root profile，因此這組 UI recommendation 不具可操作性。

Exemption 只移除不適用的 user-facing recommendation；不改寫 `CODEX_EXECUTION.md` 的 model／reasoning semantics，也不允許把 root launch metadata移進 executable Prompt。

最低充分 user-facing launch metadata shape：

```text
Codex Launch Settings
- Root model: ...
- Root reasoning: ...
- Why: ...
- Cheap-model evidence pass: YES | NO
- Context / execution mode: ...   # only when material
```

Copy-ready Prompt 本身只保留 Codex實際執行所需的 repository／task／Stage／scope／validation／STOP／launch-only delta。Direct Short / Standalone需要的 target repo／branch intent仍屬 executable contract；**root model／reasoning建議與推薦理由不屬 executable contract**。

TASKS Short-launch若 referenced Hot Stage已保存 execution settings，不在 launch body重複；除非上面的 explicit exemption 成立，ChatGPT仍必須在 fenced Prompt外顯示最低充分 root launch recommendation。

### Child Delegation Forecast

ChatGPT 在 `Actor Admission / Handoff Gate` 已判定需要 Codex handoff 後、產生 copy-ready Prompt 前，對 current Task／Stage 做一次低成本 **pre-execution forecast**，判斷目前 evidence 是否已顯示值得 Codex 在 runtime 進一步評估的 bounded child candidate。這是 planning hint，不是 execution decision。

最低充分狀態：

- `Child Delegation Forecast: NONE`：目前沒有 materially plausible child candidate；不要為了形式創造一個。
- `Child Delegation Forecast: POSSIBLE`：已有 plausible candidate，但是否值得 delegation 仍取決於 runtime evidence／topology。
- `Child Delegation Forecast: STRONG_CANDIDATE`：目前已知工作中已有 bounded、可獨立驗證，且預期具 material cost／quality／specialization／isolation benefit 的 candidate；仍不形成 spawn 義務。

Forecast 是 **ChatGPT planning state**，不是每份 Codex Prompt都必須 transport 的欄位。Transport policy：

- `NONE` → **不放進 executable Prompt**；不要輸出 `Child Delegation Forecast: NONE`、rationale或「請重新判斷」boilerplate。Codex runtime本來就依 `CODEX_EXECUTION.md` 做 `Delegation Opportunity Scan`。
- `POSSIBLE`／`STRONG_CANDIDATE` → 只有當已辨識的 bounded candidate **會 material 改善 Codex 初始 decomposition** 時，才把最低充分 cue送進 Prompt；通常一個短句即可，不要求固定 status label／三行模板。
- Hot contract／project governance已保存等價 cue → launch只引用，不再 transport第二份 forecast。

例如真正有 material candidate時，可只寫：

```text
A bounded independent-audit child may be useful; re-evaluate it through the current delegation gate.
```

Forecast 不授權 spawn、parallelization、child profile override、scope／write／permission／credential／deployment 擴張。Codex 仍必須依 `CODEX_EXECUTION.md` 的 `Delegation Opportunity Scan` 與 `Subagent / Delegation Gate` 在 execution time 自行判斷；`POSSIBLE`／`STRONG_CANDIDATE` ≠ must delegate，`NONE` 也不禁止 Codex 在 runtime 出現新 material evidence 時重新辨識合法 candidate。

ChatGPT 在 Codex completion reconciliation 時可把 forecast 與既有 `Child delegation: NONE | CONSIDERED_NOT_USED | USED` 對照，作為後續 planning feedback；forecast／actual 不一致本身不是 failure，也不要求建立新的 trace store、schema 或 logging framework。

核心原則：**Do the forecast every time it is required; transport only materially useful forecast information. Internal planning state ≠ Prompt metadata.**

核心原則：**ChatGPT may forecast delegation value during planning; Codex retains execution-time delegation authority. Forecast ≠ spawn instruction.**

### Child Delegation / Profile-Override Authorization Handoff

A handoff Prompt may carry authorization established by applicable user／project／Playbook authority; **the Prompt does not manufacture authority merely by containing the instruction**. Prompt wording is an authorization transport surface, not the origin of repository／execution／delegation authority.

ChatGPT 必須把 **child delegation authorization** 與 **child profile-override authorization** 視為兩個獨立維度：前者只回答「Codex 是否可對通過 runtime delegation gate 的 bounded subtask spawn child」，後者只在 child 已合法成立後回答「是否可指定不同 model／reasoning」。允許 profile override **永遠不會**自行建立 delegation authority；project 也可以合法地允許 child delegation、但要求所有 child 繼承 root profile。

除非使用者或 current project governance 明確禁止 subagent／Multi-Agent，ChatGPT 產生 Codex handoff 時，預設確保 applicable current authority已建立最低充分 bounded child delegation authorization，且 Codex能從 current project governance／Hot contract取得它；只有 repository-owned surface無法承載本次必要 authorization時，才由 admitted Prompt做最低充分 **transport**。在 higher authority 未禁止 mixed-profile execution 時，也可用同樣方式分開承載 profile-override authorization。Prompt只傳遞已成立的 authorization，不自行創造或擴張它；repository authority已有等價資訊時只 reference、不重複。這些 authorization只打開合法 routing能力，**不代表要求 Codex一定 spawn child或一定 override profile**。

最低充分語義必須保留：

- **Delegation authorization**：只有原本就符合 `CODEX_EXECUTION.md` 的 `Subagent / Delegation Gate` 的 bounded subtask 才可 spawn child；authorization ≠ spawn obligation。
- **Profile-override authorization**：只有 child 已合法成立，且 current authorization另外允許 profile override時，Codex才可依 `CODEX_EXECUTION.md` 的最低充分 end-to-end cost／quality原則，在 runtime向上或向下 override child model／reasoning；沒有這層 authorization時 child繼承 parent profile。
- **不得為了換 model／reasoning、少一次 root UI 操作、降低單價或 retry 而創造 child**；root profile仍由使用者決定，main critical path若需要 root escalation則走既有 STOP／relaunch gate。
- completion／final report仍依 `CODEX_EXECUTION.md` 分別回報 `Child delegation: NONE | CONSIDERED_NOT_USED | USED` 與 `Child profile override: NONE | USED`，並遵守 observability boundary。

ChatGPT 不需要在產 Prompt 時預先列舉所有可能 child 或硬編每個 profile。若 exact bounded subtask／profile 只有 runtime 才能判斷，可直接授權 Codex在上述 gate內自行選最低充分 child profile；若目前 evidence 已足以固定某個 child role／profile，則可在 Prompt 中明確 pin 該 override。

TASKS Short-launch 也適用本預設，但保持 lean：若 project governance／Hot contract 尚未提供等價 authorization，最多補兩條彼此獨立的 compact semantics，例如：

```text
Bounded child delegation is permitted only through the current CODEX_EXECUTION gates; do not expand task scope or authority.
Child profile override is permitted only for an already-admitted child through the current CODEX_EXECUTION profile/data-egress gates.
```

若只允許 delegation、不允許 mixed-profile execution，就只提供第一層並讓 child繼承 parent profile；不為形式補第二層。若 current task 明顯不適合 delegation、execution surface不支援 child profile override，或 higher authority禁止 subagent／mixed-profile routing，則依實際 authority關閉對應維度，不得把兩者綁成 all-or-nothing。

核心原則：**Child delegation authority ≠ child profile-override authority. Root profile 是 launch choice；合法 child profile 是 runtime routing choice；profile switching 不建立 delegation authority。**

## Shared reporting contract activation

`REPORTING.md` 是 adoption-level、cross-actor、activation-independent 的 substantive user-facing reporting contract。Project governance已保存 thin reporting pointer時，即使本次 task經 project-native gate留在 local route，也不會關閉 shared reporting；只需在必要時 direct-leaf 到 declared baseline 的 `REPORTING.md`，不因此 activate `CHAT_INIT.md` 或其他 shared owners。

Codex-specific child delegation／profile transparency仍由 `CODEX_EXECUTION.md` 保存；copy-ready Prompt不複製 shared reporting全文。Routing有 ambiguity或 receiving actor無法取得 declared reporting owner時，才用最低充分 self-contained transport修補，不建立第二份 canonical policy。

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

### Prompt Artifact Separation / Canonical Shapes

ChatGPT 交付 Codex handoff時，先分清三個 surface：

```text
ChatGPT planning state
≠ user-facing Codex launch settings
≠ Codex executable Prompt
```

- planning-only state（例如 `Child Delegation Forecast: NONE`）預設不 transport；
- root model／reasoning／推薦理由／cheap-model evidence-pass等 UI metadata放 fenced Prompt外；
- fenced Prompt只放 Codex真正需要執行的 contract。

#### TASKS Short-launch canonical shape

Short-launch 的 Stage pointer 必須來自**最後一次 current canonical Hot read-back**。若 ChatGPT剛更新／revision Hot Stage，先 read-back，再引用 exact path + exact Stage identity；不得用記憶、舊 wording或自行 paraphrase出的 Stage名稱代替 canonical identity。

最低充分形狀：

```text
Repository: <owner/repo>
Branch: <expected branch, usually main>

Before interpreting project execution state or reading current Hot coordination, complete the current safe remote-sync bootstrap:
- verify repository / branch / HEAD and preserve unrelated work;
- safely `git fetch origin`;
- perform only the permitted fast-forward-only sync of the expected branch;
- then re-read the latest project governance and current Hot coordination.

After that, execute only:
`<Hot path> → <exact Stage identity from current canonical read-back>`.

Follow that Stage's current scope / validation / STOP contract, perform only the authorized work,
and report completion with canonical evidence. Do not execute adjacent Hot / Cold work.

<optional one-line child-routing authorization only when current repository authority does not already provide it>
```

Launch-time material delta若尚未 canonicalize且確實會改變 execution，可補最低充分內容；若它需要 durable tracking，先更新 Hot contract而不是把 Short-launch變成第二份 specification。

#### Direct Short canonical shape

沒有可引用的 current Hot Stage時，bounded one-off work至少維持：

```text
Repository: <owner/repo>
Branch: <expected branch, usually main>

Before interpreting mutable project execution state, complete the current safe remote-sync bootstrap:
- verify repository / branch / HEAD and preserve unrelated work;
- safely `git fetch origin`;
- perform only the permitted fast-forward-only sync of the expected branch;
- then re-read the latest project governance.

Task:
<one bounded executable goal>

Scope:
<minimum necessary allowed / forbidden boundary>

Validation:
<minimum sufficient check>

STOP:
<material blocker / authority / unexpected-scope condition>

Do not expand beyond this task.
```

不需要的欄位省略；Standalone Full只在既有 exception成立時，從這個 bounded contract增加**Codex無法從 repository取得但完成工作真正必需**的 context，不把聊天歷史或 Playbook全文搬進去。

核心原則：**Stable artifact shape beats repeated prose policy. Exact canonical task identity goes inside the Prompt; user launch metadata and internal planning state stay outside unless they materially change execution.**

## Codex Prompt Pre-Send Gate

讀懂 Prompt policy、正確解釋 Hot／Cold 或先前已選對 Prompt mode，**都不足以證明最後送出的 Codex Prompt artifact 合規**。每一次 copy-ready Codex Prompt 在交付前，都必須對**最終草稿本身**做一次 bounded pre-send check；這是 last-mile execution control，不是新的 Prompt mode 或 persistence framework。

送出前依序確認：

1. **Actor check**：current responsibility／authority仍需要 Codex handoff。若 premise 已改變，回到 `Actor Admission / Handoff Gate`；不得因 Prompt已寫好就照送。
2. **Persistence closure**：若 current work 依本檔 admission rules 屬 durable／tracked Stage，且 ChatGPT 具有 current coordination write authority，先完成必要 Hot admission／revision與 canonical read-back；**不得把 Prompt 當 Stage persistence surface**。反之，一次性、低風險、低 tracking value work 不得為了本 gate 被強迫建立 Hot task。
3. **Prompt-mode check**：若 current Hot coordination已有可執行 Stage且 Codex能取得該 Stage／authority，最終草稿必須是 `TASKS Short-launch`；沒有 Hot Stage且符合一次性 bounded條件時才使用 `Direct Short Prompt`；`Standalone Full Prompt` 必須能指出本檔已列出的至少一個 explicit exception。
4. **Repository-identity presence check**：每一份 executable Codex Prompt 都必須明確包含 `Repository: <owner/repo>` 與 `Branch: <expected branch>`，且值來自 current repository／task authority；不得省略 branch、保留 placeholder、或用模糊的 base intent 取代 expected branch。這是 `REPOSITORY_EXECUTION.md` → `Repository Identity Gate` 的 artifact-level closure。
5. **Remote-freshness ordering check**：當 execution 依賴 floating／current repository state、governance、`TASKS.md` 或其他 mutable coordination truth時，final Prompt 必須先要求完成 current safe remote-sync bootstrap（identity/worktree → safe fetch → permitted fast-forward-only sync），**再** re-read latest governance／Hot state並解讀 Stage。不得把 pre-fetch local `origin/main`、stale working tree或舊 `TASKS.md` 當 remote canonical truth。
6. **Exact-pointer check（Short-launch）**：Stage pointer來自最後一次 current canonical Hot read-back，且 path + Stage identity可直接回查；不得自行 paraphrase／縮寫／猜測 Stage名稱。若剛做 Hot revision卻尚未 read-back，先完成 read-back再產 Prompt。
7. **Launch-settings presence check**：若 final response 正在交付 user-facing Codex handoff，且 `Prompt 建議設定與固定資訊` 沒有 explicit exemption，確認 final draft 已在 executable Prompt 外提供 `Root model`、`Root reasoning`、`Why`、`Cheap-model evidence pass`；`Context / execution mode` 仍只在 material 時 required。**沒有產生 launch settings 不能因「沒有放錯位置」而通過下一項 separation check。**
8. **Artifact-separation check**：root model／reasoning、推薦理由、cheap-model evidence-pass與其他 user launch settings在 fenced Prompt外；planning-only `Child Delegation Forecast: NONE` 不得進 executable body。POSSIBLE／STRONG_CANDIDATE forecast與 child-routing authorization只有 materially需要且 repository authority未已提供等價資訊時才用最低充分文字 transport。
9. **Reference / duplication check**：逐段檢查 final draft 是否重複 Codex 可由 current repository取得的 TASKS／dossier／AGENTS／spec／validation owner／protocol detail／hardware evidence／root-cause history／長 exclusions 或其他 canonical content。能由 pointer可靠取得的內容刪除重複正文，只保留 launch-time material delta。
10. **Full-Prompt exception check**：若 draft 是 Standalone Full，明確確認「為什麼 reference不足」；只有 self-contained／比較保險／資訊很重要／前面研究很多，都不是 exception。
11. **Fail-closed repair**：任一檢查不合格時，先修正 persistence、重新選 mode、refresh exact pointer或縮減／重生 Prompt，然後重新檢查。**技術內容正確不能豁免 delivery contract；未通過本 gate 的 Prompt 不得送出。**

這個 gate 檢查的是 Prompt artifact 是否符合已成立的 workflow state，不取代前面的 admission／authority／freshness decision，也不要求建立字數、token 或 keyword hard limit。若未來 execution surface提供可靠 structured-output validator，可用它檢查可機械判定的部分；semantic duplication／mode適用性仍依本 contract判斷，不假裝簡單長度 heuristic等價於 compliance。

核心原則：**A correct planning decision is not sufficient; the final Codex Prompt must independently satisfy the current Prompt Mode and duplication contract before delivery.**

## Prompt lean／長度診斷

Prompt長度不是品質指標。有 canonical Hot contract時，產生最短安全 launch pointer。

**Prompt lean 不等於 Hot contract lean。** `TASKS.md`／active dossier 的 Hot contract 不以字數最短為目標；優先確保最低充分 execution completeness、information density、清楚結構、non-duplication 與 decomposability。凡會 material 影響 scope、evidence、validation、STOP boundary 或 child decomposition 的 detail 可以保留；若主要內容變成 long-form history／raw evidence／既有 governance 或 spec 的重複，依 `Hot Task Dossier／Evidence Routing` 與 canonical owner 改用 pointer／staging，而不是靠刪掉必要 contract 來縮短。

Child Routing 改變的是 **context distribution**，不是 root responsibility：root 仍需理解並 reconcile current Hot contract；每個 child 預設只取得其 bounded subtask 所需的最低充分 Context，不把整份 Stage／history 無條件複製給 child。Child Routing 也不是讓重複、膨脹的 TASKS 或 launch Prompt 變得免費的理由。

TASKS Short-launch只保留 target、exact Hot pointer、必要 bootstrap與 completion/queue action；明顯膨脹時先檢查是否重複 TASKS/dossier/governance/spec。

Direct/Standalone才保存最低充分 target/task/evidence/allowed-forbidden scope/validation/success-STOP。如果仍膨脹，先判斷是否應 admission成 Hot task dossier或 evidence staging，而不是把所有內容塞 Prompt。

## Coverage-sensitive planning

單一修改不難但需完整覆蓋分散 surface時，優先：

`Bounded inventory → Checkpoint A → Focused implementation → Targeted validation → STOP → Independent coverage reconciliation → Next checkpoint → Final closure reconciliation`

Implementation session不同時負責大範圍 discovery、修改與 completeness judgment；每 checkpoint處理 coherent surface/invariant/operator flow。Model difficulty ≠ Coverage difficulty。

## ChatGPT-side Runtime Execution

ChatGPT-side deterministic workload execution、execution capability、artifact handoff / materialization、runtime asset reuse 與 canonical execution discipline 已移至 `CHATGPT_RUNTIME_EXECUTION.md`。只有 ChatGPT 本身需要執行 deterministic workload 時才載入該 owner；純 planning / coordination / Prompt drafting 不為形式載入。

## Codex 結果 reconciliation

收到 Codex execution result後，若宣稱 GitHub tracked-file mutation、commit/push、coordination bookkeeping、branch/HEAD或其他 remote state change，在接受 completion或產生下一 Stage前，依 `DEBUG_VALIDATION.md` Completion Evidence Guard取得最低充分 remote evidence。

Codex report是 claim，不是 GitHub authority；local-only change不能被 remote read-back升格；mismatch時 STOP並依 canonical current state重建；remote evidence不可用時標記 `REMOTE COMPLETION EVIDENCE UNAVAILABLE`。

完成 reconciliation 後，**不要直接因「Codex剛完成」就產生下一個 Codex Prompt**；先回到 `Actor Admission / Handoff Gate`，依下一項工作的 current responsibility重新選 actor。

## Scope expansion 與下一步

Analysis/review/Codex result發現 out-of-scope問題時，先依本檔 **AI-originated Durable Work Admission Gate / Follow-up Gate** 與 `REPOSITORY_EXECUTION.md` coordination lifecycle判斷：只留 observation、Cold Candidate/Committed，或真正 Hot admission；不得因「順便看到」就擴張目前 Stage或製造新的 durable obligation。

發現另一 repository也需要同步時，只做 read-only analysis/handoff；write-target switch仍依 `REPOSITORY_EXECUTION.md`。

核心原則：**ChatGPT 負責把真正值得持久化的問題變成最低充分、可追蹤、可執行的工作，並在每個 responsibility transition重新選最低充分 authorized actor；Codex只負責需要其 implementation authority的 Stage。GitHub／canonical evidence 負責證明結果。**
