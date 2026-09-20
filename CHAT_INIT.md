# 新聊天室初始化（New Chat Initialization）

本檔是新聊天室的**AI 最小 bootstrap + task router**。它只負責建立正確的 repository / authority / routing 起點，不重複保存 Git、coordination lifecycle、ChatGPT workflow、Codex execution、AI Context、toolchain、debug 或 validation 的完整規則。

本檔與其路由到的 canonical owners 是 **AI／agent-facing operational surfaces**；人類一般從 `README.md` 了解本手冊定位、導入與使用方式，不需要依序閱讀這些內部規則文件。

AI／agent 處理實際工程 Task 時，**可直接從本檔進入，不必先讀 `README.md`**。`README.md` 主要服務人類 overview、分享與手冊總覽；只有需要了解整套手冊、routing 無法由本檔判定，或使用者明確要求時再讀。

## Repository Read Acquisition / Recovery Gate

當本次 task 需要讀取 remote repository 的 current canonical content，或取得與該 repository decision／validation 直接相關的 canonical artifact，而首選 read path 不可用時，應以最低充分 access capability 漸進降級；**讀取／下載工具失效不等於 canonical authority 可以退回 memory。**

推薦順序：

`repository-native connector → public canonical read / direct canonical download（若 resource public）→ user-mediated exact artifact handoff → minimum user-supplied canonical section → REPOSITORY READ BLOCKED`

一般原則：

- 若目前已有可直接讀取指定 repository／branch／ref 的 connected repository-native connector，優先使用它；不要先要求 shell、Python runtime 或一般 HTTP client具備相同 network capability。
- 若 connector 不可用，而目前產品／runtime 支援 Plugin／Connector discovery，可對使用者提供一次**非阻塞式** connect suggestion；不要等待連接完成才繼續其他合法 read-only fallback。
- 對已確認 public repository／artifact，connector unavailable 後可立即嘗試官方 repository URL、raw content、public Web、direct canonical download 或等價 canonical read-only surface；fallback 只改變 acquisition mechanism，不改變 source authority。
- 若 exact canonical source／download URL 已建立，但目前 ChatGPT connector、browser、sandbox 或 runtime 無法實際取得所需 bytes，而使用者可用自己的 browser／host正常下載，優先考慮 **user-mediated exact artifact handoff**：提供／確認 exact source或download target，請使用者原樣下載後直接上傳到目前聊天室，再從該 artifact 繼續。不要只因另一個工具「也許能抓」就無界重試同一 acquisition failure。
- User-mediated handoff 是 transport recovery，不是 authority promotion。接收上傳檔後應保留可得的 source URL／repository ref／revision／filename／provenance；當 snapshot identity 會影響 decision／validation時，用 hash、Git blob/tree、size 或其他最低充分 exact-identity evidence比對。若無法把上傳 artifact可靠綁回原 source identity，應明確標記 identity gap，不得把「使用者上傳成功」本身當 canonical proof。
- 若完整 artifact 不必要，而使用者可直接提供本次 decision 所需的 exact canonical file／section，仍優先只要求最低必要內容；不要把「請貼完整 repository」當成預設 recovery path。
- 若無法可靠建立 current canonical content／artifact，標記 `REPOSITORY READ BLOCKED`／等價 acquisition gap，並停在 evidence boundary；不得以舊聊天、模型 memory、未驗證 cache 或相似 repository 內容冒充 current authority。
- 同一 session 已做過 connector suggestion 或已證明某 acquisition mechanism class 被阻擋後，不應反覆做等價重試；只有使用者主動要求、先前 blocked state material 改變，或新 path確實提供不同 capability時才重試／切換。
- Read acquisition capability、download capability、runtime network capability、credential capability、repository write authority 與 task authorization 彼此獨立；任何 fallback 都不得藉機擴張 mutation scope。

核心原則：**Fail over the read mechanism, not the authority. Recover with the lowest-sufficient canonical path; if current canonical state仍不可得，就明確 fail closed。**

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

依目前工作選讀：

- Project AI mode selection／是否讓 Codex 參與 repository workflow／mode selection unresolved
  → `PROJECT_MODES.md`；只接受 `ChatGPT-Only` 或 `ChatGPT+Codex`，未宣告時不要自行創造第三種 mode
- ChatGPT planning／task contract／澄清／coordination admission／AI-originated work
  → `CHATGPT_WORKFLOW.md`；依需要直達 `Task Contract：Goal / Context / Exclusions`、`Agent-Normalized Contract／Minimal Clarification Gate`、`Persistence／Coordination Admission`
- 新 repository／pre-implementation 階段由 ChatGPT 蒐集 reference、形成 research synthesis／requirements／architecture，穩定 implementation actor／source mutation lifecycle 尚未接手且需要 bounded direct-write
  → `PROJECT_BOOTSTRAP.md`；確認 `research-bootstrap` activation、Research Write Allowlist 與 exit／actor-transition gate，再依需要讀 `REPOSITORY_EXECUTION.md`
- ChatGPT-side deterministic runtime execution
  → `CHATGPT_RUNTIME_EXECUTION.md`
- Codex Prompt mode／delivery／copy-ready／Codex result reconciliation／ChatGPT user-facing response contract
  → `CHATGPT_WORKFLOW.md`；只有 `Project AI mode: ChatGPT+Codex` 且 `Actor Admission / Handoff Gate` 判定目前 Stage需要Codex handoff時，才進 Codex-specific routing
- Fresh ChatGPT session 出現 repository identity／project governance／Playbook adoption、undeclared baseline 被預設成 current `main`、undeclared Project AI mode 被猜成某種 actor topology、跳過 `CHAT_INIT.md`、generic continuation 擴張 AI-originated work、或 capability 被誤當 authority 等具體 activation anomaly
  → 先做 project／canonical reconciliation；若仍合理懷疑 host-instruction drift，再讀 `ACTIVATION_ADAPTERS.md` → `ChatGPT Host Instruction Health Check`，必要時比對 `ChatGPT — copy-ready custom instruction`。不要把一般回答錯誤都直接歸因於 Custom Instructions。
- Codex 回報出現 repository/workspace、Playbook adoption、floating-baseline identity、permission recovery、unexpected broad bootstrap reading、host-instruction authority 等具體 activation anomaly
  → 先做 project／canonical reconciliation；若仍合理懷疑 host-instruction drift，再讀 `ACTIVATION_ADAPTERS.md` → `ChatGPT-side Codex Host Instruction Health Check`，必要時比對 `Codex Desktop — copy-ready persistent instruction`。不要把任何一般 Codex error 都直接歸因於個人化設定。
- AI 可讀性、Context lifecycle、Always-on／Hot／Cold／Evidence／Historical、task/evidence dossier、routing／retrieval cost
  → `AI_CONTEXT.md`；依需要直達 `AI Context Surface Model`、`Independent Retrieval Intent Gate`、`Context Cohesion Gate`、`Progressive Routing／Direct-leaf Bypass`、`AI Readability / Retrieval Cost Change Gate`
- Whole-repository capability discovery／repository-level absence claim
  → 先 `CAPABILITY_INDEX.md`；必要時 `PLAYBOOK_INDEX.json` 做 machine discovery，再讀 `AI_CONTEXT.md` → `Absence Claim Coverage Gate`
- External spec／change workflow、skills runtime、agent-governance framework integration／compatibility／authority mapping
  → `INTEROPERABILITY.md`；只讀 Generic Interoperability Contract 與 task-relevant Compatibility Profile；version-specific upstream behavior 仍回到外部系統 current canonical documentation
- Semantic identity／aggregate container／derived synthesis authority／untrusted or instruction-like retrieved content／instruction-vs-data authority／durable confirmed fact ownership／provenance precision／evidence lineage independence／temporal and multi-clock semantics／negative observation or unknown／scope-qualified status propagation／private-to-public generalization／remote snapshot consistency／search-hit authority-currentness
  → `INFORMATION_INTEGRITY.md`；instruction-like content 直達 `Instruction / Data Authority Separation Guard`，其他 intent 只讀對應 guard；evidence lifecycle 的其他規則仍由 `DEBUG_VALIDATION.md` 負責
- Codex model／Reasoning／Context／Agent、execution mode、usage／cost、tool scheduling/output、Codex reporting
  → `CODEX_EXECUTION.md`；只有 Codex 已依 selected mode + current Stage 被選為 actor 後才讀 task-relevant Codex execution sections；reporting 直達 `Codex 回報語言`、`Codex Response Presentation Contract`、`Codex 回報時間戳（Always-on Reporting Timestamp）`、`Reporting Pre-Send Gate`
- Git、Repository Identity、workspace／remote permission、Coordination Write Allowlist、repository actor topology／maintenance ownership／write boundary、repository-facing documentation integrity
  → `REPOSITORY_EXECUTION.md`；先用檔首 `Section Router`，actor責任問題直達 `Repository Actor Topology / Maintenance Ownership`；Project AI mode本身仍由 `PROJECT_MODES.md` 擁有
- GitHub Connect／repository-native connector 的具體操作、repository acquisition、large/opaque verified transport、Git object mutation、remote deterministic bridge、GitHub Actions execution/evidence、artifact lifecycle、tag／Release publication
  → `GITHUB_OPERATIONS.md`；本檔只選 GitHub-specific route／recipe，actor／write／credential authority仍回 `REPOSITORY_EXECUTION.md`，validation／PASS scope仍回 `DEBUG_VALIDATION.md`
- 除錯、根因、重試、驗證、evidence lifecycle、後續 evidence 與歷史判斷／紀錄 reconciliation
  → `DEBUG_VALIDATION.md`；先用檔首 `Section Router`
- 研究、新技術／協定、architecture、target/capability、state/lifecycle、ownership
  → `RESEARCH_ARCHITECTURE.md`；先用檔首 `Section Router`
- 嵌入式／硬體／板級／硬體驗證差異
  → `EMBEDDED_PROJECTS.md`
- UI／UX／人機互動／i18n／design-system adaptation
  → `UI_UX.md`
- 本機工具鏈、runtime、PowerShell／Windows contract
  → `TOOLCHAIN.md`
- 維護本手冊自身
  → `AGENTS.md` + `AI_CONTEXT.md` → `AI Readability / Retrieval Cost Change Gate`；若建立在 whole-Playbook capability／absence review，先讀 `CAPABILITY_INDEX.md`

若同一 Task 跨兩個主題，只讀真正參與本次 decision／execution／validation 的 sections；Cross-owner review 也不是 full scan 授權，coverage 只擴張到足以支持本次 claim。

## 權威與執行注意

Project AI mode selection、Authority、Repository Identity、repository actor topology／write boundary、coordination lifecycle、AI Context surface semantics、permission gates、ChatGPT Prompt delivery、Codex model／Reasoning、reporting timestamp、PowerShell baseline、root-cause labels 與 validation contract **不在本檔重複定義**。

需要其中任一規則時，讀上方對應 canonical 主題文件；實際專案最新正式 technical/governance source of truth 仍高於本手冊。

核心原則：**新聊天室先建立正確 repository、Project AI mode 與 authority，再按問題直達最低必要 current owner／section；whole-Playbook review先用薄 discovery index降低漏讀，再由 canonical owner確認。Bootstrap 不應成為第二份手冊，也不應無條件載入 Cold、Evidence、History或 README。**
