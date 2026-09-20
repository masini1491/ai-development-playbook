# 新聊天室初始化（New Chat Initialization）

本檔是新聊天室的**AI 最小 bootstrap + task router**。它只負責建立正確的 repository / authority / routing 起點，不重複保存 Git、coordination lifecycle、ChatGPT workflow、Codex execution、AI Context、toolchain、debug 或 validation 的完整規則。

本檔與其路由到的 canonical owners 是 **AI／agent-facing operational surfaces**；人類一般從 `README.md` 了解本手冊定位、導入與使用方式，不需要依序閱讀這些內部規則文件。

AI／agent 處理實際工程 Task 時，**可直接從本檔進入，不必先讀 `README.md`**。`README.md` 主要服務人類 overview、分享與手冊總覽；只有需要了解整套手冊、routing 無法由本檔判定，或使用者明確要求時再讀。

## Repository Read Acquisition / Recovery Gate

當本次 task materially 依賴 remote repository 的 current canonical content／artifact 時，先使用**最低充分、已授權、可建立 current identity 的 canonical acquisition route**。Acquisition mechanism 可以 fail over；source authority、task authority、write authority與 evidence semantics不得因此改變。

若 current canonical identity／content 仍無法可靠建立，標記 `REPOSITORY READ BLOCKED`／等價 evidence gap，只 block依賴該 evidence 的 action；不得以舊聊天、memory、未驗證 cache、search hit或相似 repository內容補成 current authority。

具體 mechanics 由既有 owners 擁有：

- GitHub repository read／enumeration／public anonymous acquisition／response-shape／large payload → `GITHUB_OPERATIONS.md` → `Repository Acquisition`、`GitHub Read Payload / Response-Shape Gate`
- access／credential／task／write authority與 permission recovery → `REPOSITORY_EXECUTION.md`
- connector／uploaded artifact／user-mediated handoff 到 runtime 的 materialization／integrity → `CHATGPT_RUNTIME_EXECUTION.md` → `Artifact Handoff / Materialization Gate`
- identity／provenance／snapshot consistency／search-currentness → `INFORMATION_INTEGRITY.md`

同一 session 已證明某 acquisition mechanism class blocked 時，不做等價無界重試；只有 capability／permission／source identity／user intent 等 material premise 改變，才重新路由。

核心原則：**Fail over the read mechanism, not the authority. Bootstrap只決定何時 current evidence足夠；具體 acquisition／transport／permission mechanics留在其 canonical owner。**

## 啟動順序

### Bootstrap Tier Model

本 Playbook 採用一個可由 adopter repository 重用的 **semantic bootstrap tier model**。Tier 定義的是「在往下一個 decision／action boundary 前，哪一類責任必須已解析」，**不是固定檔名、固定讀檔數量或所有 repository 都必須建立相同 surface 的要求**。

```text
Tier 0 — Authority / Identity
→ 我現在處理的是哪個 repository / revision / authority context？

Tier 1 — Work-State / Intent Routing
→ 這次是哪一類工作？目前 active mode / task / stage / lifecycle 是什麼？

Tier 2 — Canonical Domain Owner
→ 真正負責本題語意、技術、方法或工程 truth 的 canonical owner / leaf 是誰？

Tier 3 — Action Contract Closure
→ 即將執行的 action 還需要哪些 conditional contract？
→ applicable contract closed 才進入 ACTION READY

ACTION READY
→ perform the authorized action

Tier 4 — Completion Evidence Closure
→ 實際結果需要哪些 validation / read-back / reporting / completion evidence，才能形成 scope-qualified claim？
```

跨 repository 共通規則：

- **Tier 是 responsibility boundary，不是 ceremony。** Exact current target／owner／leaf 已唯一時，可依 `AI_CONTEXT.md` 的 Progressive Routing／Direct-leaf Bypass 直接命中；不為形式逐層讀中間文件。
- **Repository 可以有不同 mapping。** Tier 1 可以是 project mode、method routing、knowledge-domain routing、lifecycle state 或其他 repository-owned work classifier；Tier 2 可以是 source、method owner、knowledge leaf、architecture owner 等。可省略不適用的 surface，但不得省略仍 materially applicable 的 responsibility。
- **不得帶著 material unresolved prerequisite 跨 tier boundary。** Tier 0 的 repository／authority identity、Tier 1 的 active work identity、Tier 2 的 canonical owner，若會 material 改變後續 decision，就先解析到最低充分程度；不得用 memory／舊聊天／search hit 猜補。
- **Tier 3 由 `AI_CONTEXT.md` → `Action Contract Closure` 約束。** Progressive reading 可以少讀，但在 executable artifact、tool call、mutation、runtime、validation、handoff、delegation或其他 governed action 開始前，所有 applicable minimum canonical contract 必須 closure；未 closure 只 block受影響 action。
- **Tier 4 不得被 Tier 3 取代。** 已讀懂規則只代表可以開始 action，不代表 action 成功；PASS／completion／current-state claim 仍必須由實際 validation、canonical read-back、reporting或其他 owner-defined evidence成立。
- **Early tier 不應吸收 later-tier domain policy。** Bootstrap只保存 stable responsibility／routing semantics；GitHub、Prompt、delegation、runtime、validation、engineering method等具體 procedure留在其 canonical owner。

核心原則：**Bootstrap tiers define what must be resolved before moving forward；progressive routing defines how little must be loaded to resolve each tier。不同 repository 可以映射到不同 files／routers，但不能用 selective reading 合理化 materially unresolved tier。**

### This Playbook's Default Mapping

對採用本 Playbook 的一般工程 repository，預設以最低充分方式映射：

**Tier 0 — Authority / Identity**

- 明確確認目標 Repository：`owner/repo`；不要只使用可能對應多個 repository 的模糊名稱。
- 先讀實際目標 repository 最新 project governance、current Hot coordination surface（若採用）與本次 task 直接相關的最低必要正式 source of truth；Cold、Evidence、History 不因存在就預設載入。
- Currentness materially影響判斷時建立足夠的 ref／revision identity；project-specific governance 先於 shared Playbook detailed routing。

**Tier 1 — Work-State / Intent Routing**

- 從 current project governance 解析 `Project AI mode`。只接受 `ChatGPT-Only` 或 `ChatGPT+Codex`；未宣告是 **mode selection unresolved**，不是第三種 mode，也不得從 available tools、舊聊天室、repository shape或上一個 actor猜測。
- 建立本次 Task／Stage／lifecycle／current Hot identity到足以判斷 active work；mode-dependent implementation actor／handoff／broader mutation在 unresolved 時維持 `REPOSITORY_EXECUTION.md` 的 conservative boundary。
- 不依賴 unresolved mode／lifecycle 的合法 read-only work，可維持最低風險範圍。

**Tier 2 — Canonical Domain Owner**

- 依已建立的 repository／governance／work identity，用本檔「最低必要路由」直達本次 Task 所需的 canonical Playbook owner／section；不要為了熟悉規則完整掃描手冊，也不要把 `README.md` 當必要中繼站。
- 進入大型 owner 後優先使用 Section Router、heading、symbol或 stable pointer；exact target已唯一時 direct-leaf。
- Whole-repository capability／gap／absence review 才先讀 `CAPABILITY_INDEX.md`，再依 `PLAYBOOK_INDEX.json`／合理 owner search做 bounded coverage；negative claim semantics回 `AI_CONTEXT.md` → `Absence Claim Coverage Gate`。

**Tier 3 — Action Contract Closure**

- 跨 action boundary 前依 `AI_CONTEXT.md` → `Action Contract Closure` close最低充分 applicable contract。
- 若 current scope出現 material deterministic execution candidate，再做最低充分 Execution Opportunity Scan；成立才讀 `CHATGPT_RUNTIME_EXECUTION.md`。
- Prompt／Codex handoff／delegation、repository mutation／permission、GitHub operation、validation execution或其他 conditional action，只在該 action真正 applicable 時讀其 canonical owner；不把全部 action contract塞進 bootstrap。
- Repository identity、authority、required evidence或其他 material prerequisite unresolved 時，只 block受影響 action並做 bounded recovery；不得用舊聊天、cache或 memory 補成 current contract。

**Tier 4 — Completion Evidence Closure**

- Action完成後，回到該 action／domain owner要求的 validation、canonical read-back、reporting、completion evidence與 scope-qualified status。
- Tool success、artifact generation、commit存在、handoff已送出或某一局部 test PASS，都不得自行升格成較大的 completion claim。
- 若 current branch／artifact／external state在 action後跨過 material causal boundary，重新取得 owner要求的最低充分 post-action evidence。

推薦的通用 hot path：

`Tier 0 Authority → Tier 1 Work Identity → Tier 2 Canonical Owner → Tier 3 Action Contract Closure → ACTION READY → execute → Tier 4 Completion Evidence → STOP when sufficient`

## 最低必要路由

依目前 intent 直達最低充分 owner；exact section已知時直接讀該 leaf，不為形式先載完整 owner。

- Project AI mode selection／mode unresolved／是否讓 Codex 參與 repository workflow
  → `PROJECT_MODES.md`
- ChatGPT planning／task contract／coordination admission／AI-originated durable work／Codex Prompt mode與handoff／result reconciliation／ChatGPT user-facing delivery
  → `CHATGPT_WORKFLOW.md` → Section Router
- pre-implementation research-bootstrap／reference synthesis／requirements／architecture形成期的 bounded direct-write
  → `PROJECT_BOOTSTRAP.md`
- ChatGPT-side deterministic runtime／capability／materialization／execution evidence
  → `CHATGPT_RUNTIME_EXECUTION.md`
- Fresh ChatGPT／Codex session 出現 repository identity、floating baseline、undeclared mode、unexpected broad bootstrap、capability-as-authority 或其他 host-activation anomaly
  → 先 project／canonical reconciliation；仍合理懷疑 host-instruction drift 才讀 `ACTIVATION_ADAPTERS.md`
- AI Context lifecycle／Always-on-Hot-Cold-Evidence-Historical／routing／retrieval cost／Action Contract Closure
  → `AI_CONTEXT.md` → Section Router
- Whole-repository capability discovery／repository-level absence claim
  → `CAPABILITY_INDEX.md`；需要 machine discovery 才用 `PLAYBOOK_INDEX.json`，negative-claim semantics回 `AI_CONTEXT.md`
- External spec／change workflow／skills runtime／agent-governance interoperability
  → `INTEROPERABILITY.md`
- Semantic identity／derived authority／instruction-vs-data／provenance／lineage／temporal semantics／unknown／scope-qualified status／snapshot consistency／search-hit authority
  → `INFORMATION_INTEGRITY.md`
- Codex execution／model／Reasoning／Context／tool scheduling／delegation／cost／reporting
  → `CODEX_EXECUTION.md` → Section Router；一旦 Codex execution active，該檔宣告的 reporting contract屬 cross-cutting prerequisite
- Git／Repository Identity／workspace／permission／actor topology／write boundary／coordination write authority
  → `REPOSITORY_EXECUTION.md` → Section Router
- GitHub-specific repository acquisition／verified transport／Git object mutation／Actions／artifact／tag／Release
  → `GITHUB_OPERATIONS.md` → Section Router
- 除錯／root cause／retry／validation／evidence lifecycle／completion claim
  → `DEBUG_VALIDATION.md` → Section Router
- research／new technology／protocol／architecture／target-capability／state-lifecycle／ownership
  → `RESEARCH_ARCHITECTURE.md` → Section Router
- embedded／hardware／board-level／hardware validation
  → `EMBEDDED_PROJECTS.md`
- UI／UX／HMI／i18n／design-system adaptation
  → `UI_UX.md`
- local toolchain／runtime／PowerShell／Windows contract
  → `TOOLCHAIN.md`
- 維護本 Playbook自身
  → `AGENTS.md` + `AI_CONTEXT.md` → `AI Readability / Retrieval Cost Change Gate`；只有 whole-Playbook capability／absence review才先讀 `CAPABILITY_INDEX.md`

同一 Task跨 owner時，只讀真正參與本次 Tier 1–4 decision／action／evidence closure 的 sections；Cross-owner review不是 full-scan授權。若 owner內有 Section Router，先用它；足夠即 STOP。

## 權威與執行注意

Project AI mode selection、Authority、Repository Identity、repository actor topology／write boundary、coordination lifecycle、AI Context surface semantics、permission gates、ChatGPT Prompt delivery、Codex model／Reasoning、reporting timestamp、PowerShell baseline、root-cause labels 與 validation contract **不在本檔重複定義**。

需要其中任一規則時，讀上方對應 canonical 主題文件；實際專案最新正式 technical/governance source of truth 仍高於本手冊。

核心原則：**新聊天室先建立正確 repository、Project AI mode 與 authority，再按問題直達最低必要 current owner／section；whole-Playbook review先用薄 discovery index降低漏讀，再由 canonical owner確認。Bootstrap 不應成為第二份手冊，也不應無條件載入 Cold、Evidence、History或 README。**
