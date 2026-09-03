# Repository 執行規則（Repository Execution Rules）

> **Authority**：Repository identity、write scope、workspace／network／credential permission、remote Git、external-service operation、canonical repository evidence、coordination write allowlist、ChatGPT／Codex repository write boundary。
> **Read when**：目前工作涉及 Git/repository、permission/capability、remote service mutation/read-only boundary、TASKS/BACKLOG/evidence/task-dossier 寫入、repository-facing claims 或 ChatGPT/Codex 寫入分工。
> **Usually skip when**：只是純 architecture/research、source-level root cause/validation、UI／UX 或 embedded hardware semantics。
> **Progressive reading**：先依下方 Section Router 定位；找到 relevant heading 後只讀該 section 與必要相鄰 dependency，不預設載入全文。

AI-facing information surface 的 Hot / Cold / Evidence / Historical 語意、default-load policy、routing 與 retrieval-cost contract，以 `AI_CONTEXT.md` 為主要 authority；本檔只決定 repository mutation / permission / coordination write boundary。

## Section Router

- repo/branch/HEAD 身分、聊天室 writable target → `Repository 身分確認關卡`、`聊天室級 Repository 寫入鎖`
- workspace／sandbox／filesystem／network／credential capability → `Workspace 寫入能力關卡`、`授權與能力分層`、`權限關卡操作`
- sync／fetch／push → `安全 Remote Sync 啟動`、`Remote Git 權限關卡`
- external service read-only / mutation / staged operation → `權限關卡操作` 內的 external-service sections
- hash／LOC／manifest／public README claim → `Canonical Repository Evidence`、`Repository-facing 文件完整性`
- Hot / Cold / task dossier / evidence surface 的 AI loading semantics → `AI_CONTEXT.md`
- coordination surface mode／ChatGPT 可直接寫哪些 path → `Coordination Write Allowlist`、`ChatGPT／Codex Repository 寫入邊界`

## Repository 身分確認關卡（Repository Identity Gate）

每個 Codex Prompt 必須明確指定：

- 目標 Repository：`owner/repo`
- 預期 Branch（通常 `main`）

執行任何讀取、修改、build、test 或 Git mutation 前，先確認目前 working repository 與 Prompt 指定 repository 一致。

至少確認：
- repository root
- origin remote URL / repository identity
- current branch
- current HEAD
- 必要時 repository-specific sentinel file / structure

若 identity mismatch：立即 STOP，回報 expected/detected repository、branch、HEAD；不得修改任何檔案、不得自行切換 repository、不得自行 clone、不得將 Prompt 套用到相似專案。

## 聊天室級 Repository 寫入鎖（Conversation-scoped Repository Write Lock）

對遵循本手冊的 ChatGPT／planning conversation，**同一聊天室同一時間只能有一個明確的 `Current Write Target Repository`**。本聊天室直接發起的任何 repository mutation，必須先通過這個 gate；其他 repository 一律 read-only。

一般原則：

- 第一次需要 repository mutation 前，必須由使用者的明確指示足以辨識唯一 writable repository；若尚未能確定 `Current Write Target Repository`，所有 repository 維持 read-only，先釐清 target，不得先寫再補授權。
- Current Write Target 以外的 repository，即使可被 GitHub connector／credential 讀寫，也只能讀取、搜尋、比較、review、取得 evidence 或產生建議／Prompt；**不得建立、更新、刪除或改名其任何 path，包括 `TASKS.md`、`BACKLOG.md`、task/evidence dossier、`AGENTS.md`、source、docs、tests、workflow 或其他檔案。**
- `Current Write Target Repository` 只是 repository-level 必要條件，不增加任何 path/action 權限。實際 mutation 仍須同時符合該 repository governance、ChatGPT／Codex write boundary、目前 Task/Stage authorization、execution permission 與 credential capability。
- 發現另一 repository「也應同步」、「順便對齊」、「同樣需要修」或存在合理 cross-repo follow-up，只建立 read-only analysis／handoff；不得據此推導第二個 writable repository。
- 「好」、「繼續」、「照這樣做」等承接語句，以及對目前工作的一般同意，不構成 write-target switch。若新的 mutation request 指向不同 repository，必須由使用者明確指定切換 writable repository或等價清楚意圖。
- Write target 一旦明確切換，舊 target 立即回到 read-only；**同一聊天室不得同時保留兩個 writable repositories。**
- `masini1491/ai-development-playbook` 的 ChatGPT-maintainer 例外也受本 gate 限制：只有它是本聊天室 Current Write Target 時，ChatGPT 才可直接維護手冊。
- 本 gate 不限制合法的跨 repository read-only research／comparison，也不代表另一個 session 自動沿用本聊天室 target。

對本聊天室直接 repository mutation，可視為：

`Allowed mutation = Current Write Target match ∩ Repository governance ∩ Task/Stage authorization ∩ Execution permission ∩ Credential capability`

核心原則：**Repository access ≠ conversation write authority；先鎖定唯一 writable repository，再判斷該 repository 內實際允許寫什麼。**

## Workspace 寫入能力關卡（Workspace Write Capability Gate）

在任何需要修改 repository 的 Task / Stage 開始 file mutation 前，先確認 execution environment 對目標 working tree 具有完成該 Stage 所需的最小寫入能力。

Read-only work（research、code review、architecture analysis、evidence review、read-only validation inspection）若不需要 mutation，可在 read-only workspace 繼續。

Write-required work 若目前 workspace 為 read-only 或無法完成必要 file write：

- 標記 `WORKSPACE WRITE CAPABILITY MISSING`；
- runtime 可 request permission 時，主動要求最小必要 capability；
- 必須由使用者切換 workspace-write 時，清楚回報；
- capability 未取得前 STOP，不進 coding/debug loop；
- 不得分類為 SOURCE failure，也不得修改 production source 來「修」環境問題；
- 不得用 temporary copy、另一 clone、改 Git metadata location、廣泛 chmod、sudo 等 workaround 繞過。

取得 capability 後只恢復原本已授權 Stage，不代表 scope expansion。

## 安全 Remote Sync 啟動（Safe Remote-Sync Bootstrap）

執行已授權 Task/Stage 前：

1. Repository Identity Gate。
2. 依 Stage 性質完成 Workspace Write Capability Gate。
3. `git status --short`。
4. 確認 current branch / HEAD。
5. 確認無 merge / rebase / cherry-pick 等未完成 history operation。
6. 依 Remote Git Permission Gate 判斷 `git fetch origin` 是否需要先要求最小權限。
7. `git fetch origin`。
8. 只有 expected branch + clean tree + local 無 ahead/diverged 且可 fast-forward-only 時才同步。
9. 同步後重新讀最新 local project governance 與 current Hot coordination surface；不要因 project 採用 Cold/Evidence surface 就在每次 bootstrap 無條件全文載入它們。
10. 若指定 Task/Stage 已消失或被改變到 launch 失效，STOP，不得依舊 Prompt/記憶執行。

若 project governance 明確宣告固定 coordination surface，而同步後該 surface 缺失，不得把 missing 直接解讀為 EMPTY；先依最新 governance / Git evidence 判斷是否為尚未初始化、意外刪除或退出該 mode。

禁止 autonomous：
- `reset --hard`
- force push
- merge / rebase / cherry-pick
- auto-stash
- delete/discard unknown user work
- checkout overwrite
- rewrite history

Commit/push 必須服從使用者當次 launch 或 repository policy 的明確授權；coordination item 本身不自動授權 Git mutation。

## 授權與能力分層（Authorization / Capability Layers）

任何 Git、filesystem、toolchain、network 或 external-service operation，都應分開判斷：

1. **Task / Stage Authorization**：本次實際允許做什麼。
2. **Execution Permission**：sandbox / network / filesystem / metadata / runtime 是否允許執行。
3. **Credential Capability**：目前 account/token/key/session 技術上能做什麼。

真正允許執行的 operation 只能落在三者交集：

`Allowed operation = Task/Stage authorization ∩ Execution permission ∩ Credential capability`

較大的 execution permission 或 credential capability 都不代表 scope expansion；任一層不足時，只處理該層缺口。

## 權限關卡操作（Permission-Gated Operation）

本規則適用於目前已授權 Task / Stage 所必要的 Git、build、test、toolchain、filesystem、remote network、external API / CLI / HTTPS、package registry 或其他外部 operation。

1. 必要 operation 因 sandbox/filesystem/metadata/network/permission gate 受阻時，先判斷是否只是可由使用者批准解除的 permission gate；permission gate 本身不是 source/toolchain/environment/service failure。
2. 事前已知需要額外 permission 時，先要求最小 capability；不得故意先製造一次可預期 failure。
3. 事前未知時可正常執行一次；第一次明確 permission denial 後立即轉 permission flow。
4. Permission request 盡量說明 exact operation、為何必要、resource/path、service host/port（可限定時）與最低 permission scope。
5. 使用者批准後只重試原本被 gate 阻擋的必要 operation；approval 不授權 scope expansion、下一 Stage、額外 mutation 或其他 Git workflow。
6. `permission denial → request → approval → retry original operation` 不計 operational retry cap。
7. 使用者拒絕、runtime 無法取得 permission，或取得後仍真正失敗，才依 `DEBUG_VALIDATION.md` 分類。
8. 不得以 permission 問題自行使用 `sudo`、廣泛 chmod、刪 Git lock/state、重新 clone 覆蓋 working tree、stash/delete unknown work、reset-hard、force push、auto merge/rebase/cherry-pick 等 workaround。

### External network / service 邊界

- Network/sandbox approval 只允許目前已授權 operation建立必要連線，不自動授權 deploy、publish、configuration/resource/auth/credential mutation。
- Credential capability 大於目前 Stage scope 時，實際執行仍以 Stage authorization 為上限。
- 外部服務操作與 reporting 不得輸出或保存 secrets。
- Read-only / mutation 依 operation semantics 與 side effect 判斷，不只看 HTTP verb、CLI 名稱或 UI wording。
- side effect 定義不清楚時，先查 authority 或取得最小 read-only evidence；無法確認時不得假定安全 read-only。
- External-service 文件拆分依 `RESEARCH_ARCHITECTURE.md` 的 External-service authority separation。

### Public read-only anonymous-first（最低充分 Access Capability）

對已確認 public resource 的純 read-only operation，若官方 anonymous access 已足以取得本 Stage evidence，優先使用較低 access capability。

適用時需確認 resource public、operation 真正 read-only、使用 official endpoint、不需要 authenticated-only metadata，且 evidence quality 不因此下降。

推薦 escalation：

`public anonymous read-only → authenticated read-only（必要時）→ authenticated mutation（只有明確授權時）`

Anonymous-first 不是 anonymous-only；quota/rate limit 不足時可依 current Task 需要升級 authenticated read-only。不得因 quota exhausted 自行輪替其他 account/token/installation/proxy/mirror/third-party source。

核心原則：**Capability downgrade ≠ scope expansion；identity/source boundary change ≠ ordinary retry。**

### External service staged operation

外部服務同時有 read-only、live observation、mutation/admin capability 時，優先分 Stage：

1. **Read-only baseline**：確認 service/account/target identity、非敏感 config/resource metadata、access baseline。
2. **Live observation**：使用 read-only capability 觀察 current runtime evidence，不因觀測需要主動製造 mutation。
3. **Explicit mutation**：deploy/publish/config/resource/auth mutation 只有 exact target + exact mutation + validation scope 明確授權時才執行。

Stage 1/2 不推導 Stage 3。External-service validation 需區分 access/preflight、local/dry-run、remote mutation、read-only smoke、end-to-end/live、production/hardware evidence tier。

## Remote Git 權限關卡（Remote Git Permission Gate）

對目前 Task / Stage 所必要且本來已獲授權的 remote Git operation，套用 Authorization / Capability Layers 與 Permission-Gated Operation。

- 已知需要額外 network/metadata/filesystem permission 時先要求最低 capability；未知時首次 denial 後再要求。
- approval 後只重試原 remote Git operation。
- permission resolution 不計 operational retry。
- 無法 escalation 或 permission 後仍真正失敗時才分類。

### `git fetch origin` 特例

`git fetch origin` 可能同時需要 remote network access 與本地 Git metadata write capability。只要求實際缺少的 capability；fetch approval 不代表 pull/merge/rebase/push 授權。

### `git push` 邊界

Sandbox/network approval不等於 Git mutation authorization。只有目前 Task/launch/repository policy 本來已明確授權 push 時，permission escalation 才解除其 execution/network gate。

## Canonical Repository Evidence（Canonical Repository Evidence）

需要跨機器、跨 OS 或跨工作區重現的 repository evidence，不應無條件依賴 platform-transformed working-tree bytes。

適用例如 source hash/integrity manifest、project-scale/physical-line 統計、canonical baseline、source inventory、retention manifest。

原則：

1. 語意是某 Git ref/commit 的 tracked content 時，優先以 Git canonical object / tracked content 為 authority，例如 `git ls-tree`、`git cat-file`。
2. 必須從 working tree 計算時，明確定義 canonicalization；CRLF/LF、encoding/BOM 等若影響結果要正規化或說明。
3. 不把 `.git`、build/cache、generated、downloaded dependencies 或 untracked temp 混入 canonical source evidence，除非 contract 明確要求。
4. Hash/line count/manifest 計算方法本身屬 validation contract；跨平台不一致先查 canonicalization/tool behavior。
5. Repository 已有 canonical counter/hash tool 時，後續文件與 validation 優先使用該 authority，不另維護手工算法。

Canonical evidence 不取代 runtime/build/hardware validation。

## Repository-facing 文件完整性（Repository Documentation Integrity）

公開 README、showcase、project overview 若宣稱開發方式、驗證狀態、專案規模或 AI-assisted workflow，claim 應可追溯到正確 authority；README 本身不應成為另一套 execution/validation policy。

### AI-assisted development transparency

公開 repository 若明顯使用 ChatGPT、Codex 或其他 coding agent，可精簡說明 human-in-the-loop 分工：Human 負責需求/產品方向/現實 evidence/最終核准；ChatGPT/planning agent 負責研究、architecture/spec discussion、review、task decomposition；Codex/coding agent 在授權 scope內 implementation/tests/build/docs/repository maintenance。

AI 產生 code/analysis、command success 或 build exit 0 不等於產品完成所有必要 validation；公開 wording 必須符合 evidence tier。提及 provider 不得暗示贊助、認證或背書。

### Project Scale Reporting

README 或公開文件展示 LOC、行數、檔案數等 project-scale statistics 時：

- 說明統計基準，例如 Git tracked files / ref / commit；
- 定義 physical/logical/executable LOC 等 metric；physical lines 要說明 blank/comment；
- 說明排除項目，例如 third-party/build/cache/generated；
- taxonomy 依 repository 實際 structure 定義；
- 統計服從 Canonical Repository Evidence。

不要求每個 repository 建專用 counter。只有公開數字長期存在且頻繁改變、手工更新易漂移，或多份正式文件需同步時，才優先 deterministic counter。

已有 counter 的 repository，在真正影響該 metric scope 的 tracked-file 變更與相關 validation 完成後更新；數字未變時不要製造 README diff。

**Project-scale 分類應依資訊責任而非副檔名粗略推定。** 若統計目的是 implementation / canonical technical documentation scale，`TASKS.md`、`BACKLOG.md`、active task dossier、evidence inbox、archive/history 等 operational project memory 通常不應只因是 Markdown 就被算入同一「技術文件」指標。若 high-frequency coordination mutation會使 README/stat snapshot頻繁 stale，依 `AI_CONTEXT.md` 的 Derived Metadata Write-Closure Gate重新設計 scope，而不是擴大 ChatGPT 對 README 的 write authority。

核心原則：**公開 repository claim 應可由 canonical evidence 重現；README 負責說明，不自行複製底層治理規則。**

## Coordination Write Allowlist

一般 project 的 ChatGPT direct-write boundary 採**明確 allowlist + project opt-in**，不是廣泛 docs write。

### Default — Single-Surface Mode

若 project governance 沒有明確宣告其他模式，ChatGPT direct-write allowlist 只有：

- `/TASKS.md`

這保持既有 repository 的 backward compatibility；舊 project 不因更新本手冊自動取得 `/BACKLOG.md`、task dossier 或 evidence path 的 direct-write capability。

### Optional coordination / evidence surfaces

Project governance 可明確 opt-in 一個或多個額外 surface，例如：

- `/BACKLOG.md` — Cold Registry；
- `/tasks/active/*.md` 或 project-defined equivalent — Hot task dossier；
- `/evidence/inbox/*.md` 或 project-defined equivalent — sanitized evidence staging。

實際 path / glob 必須由 project governance 明確列入 `ChatGPT Coordination Write Allowlist` 或等價 contract；未列出的 path 一律 read-only。

Opt-in 不要求使用上述固定名稱；語意與 AI loading responsibility依 `AI_CONTEXT.md`，path 由 project決定。

### 不得自我擴權

- ChatGPT **不得直接修改 project `AGENTS.md`／governance 來把新 path 加進自己的 allowlist**。
- 啟用／擴大 allowlist 必須是使用者明確授權的 governance change，並由當時已具合法 mutation authority的 maintainer／Codex 執行；除非該 repository本身另有更高層明確例外。
- 使用者說「記一下」、「這個先留著」可以授權在**既有 allowlist內**保存對應資訊；不會自動建立新的 path permission。
- ChatGPT可寫入某 surface，不代表該 surface具有 execution authority；Hot/Cold/Evidence semantics依 `AI_CONTEXT.md`。

### Write-closure

ChatGPT 對 allowlisted surface 的合法 mutation，不得因 derived bookkeeping 反向推導對 README、manifest、showcase、source 或其他非 allowlisted path 的直接寫入權。若衍生檔需要同步，依 `AI_CONTEXT.md` 的 Derived Metadata Write-Closure Gate處理。

### Single-Surface → Multi-Surface adoption procedure

當既有 project 從 default Single-Surface Mode（通常只有 `/TASKS.md`）第一次 opt-in `/BACKLOG.md`、Hot task dossier、evidence staging或其他額外 coordination surface時，**不要把「新增檔案」本身當成 migration 完成**。先完成最低充分 governance／information-architecture transition，避免 ChatGPT 在新 path 尚未取得 authority前自我擴權，或讓 operational memory意外污染 README／project-scale／derived metadata。

推薦流程：

`Audit current surfaces / derived dependencies → User selects target semantics → Authorized governance mutation → Supporting path/tooling update → Validation → Canonical read-back → Data migration → New allowlist becomes active`

一般原則：

1. **Audit current state**：先讀 current project governance、`TASKS.md`／現有 coordination content、retention/ignore policy，以及 project-scale／manifest／README/showcase等可能把 Markdown 或新 path納入 derived output 的規則。
2. **Choose semantics before paths**：先確認真正需要的是 Cold Registry、Hot dossier、sanitized evidence staging或其他單一責任；不要為了「多層比較完整」一次啟用全部 surface。
3. **User authorization does not equal immediate self-expansion**：使用者可明確授權「啟用 BACKLOG／讓 ChatGPT可維護某 surface」這項治理變更，但在 project governance實際由合法 maintainer／Codex更新並生效前，ChatGPT仍不得直接修改 governance或先建立／寫入新 path。
4. **Governance first**：由當時具合法 mutation authority的 actor更新 `ChatGPT Coordination Write Allowlist`／等價 contract，並明確保留未列入 path為 read-only；必要時同步 routing、retention、security/sanitization與 actor responsibility。
5. **Close derived dependencies**：若 project-scale、manifest、public README/showcase、generated index或其他 derived metadata會因新 operational surface而頻繁變動，先在同一 migration Stage調整 classification／write-closure；不要讓每筆 coordination mutation反向要求更新非 allowlisted文件。
6. **Create only selected surfaces**：只建立已核准且有明確 owner/semantic的 path；Hot dossier/evidence staging不得因建立目錄就成為 every-task default load。
7. **Migrate state without changing commitment**：把現有 `TASKS.md` 內容分流到 Hot／Cold／Evidence時，只改資訊責任與位置；`CANDIDATE` 不因搬到 BACKLOG就變 `COMMITTED`，Cold不因拆檔就取得 execution authority，historical/evidence也不得升格成 current task。
8. **Validate and read back before use**：完成 project-required deterministic validation／CI（若適用）與 remote canonical read-back後，新的 allowlist才視為 effective；ChatGPT從此才可依新 contract直接維護新 surface。
9. **Keep migration bounded**：第一次 migration只處理 coordination architecture成立所必需的治理、derived dependency與狀態分流；AGENTS/README slimming、archive重整、unrelated refactor若不是必要 dependency，另行 admission，不順手擴張。

核心原則：**先讓 governance與 derived-information responsibility 對新 surface閉合，再搬資料、再開始使用；新增 coordination path不是 ChatGPT自我授權的捷徑。**

## Coordination Lifecycle / Admission

`TASKS.md`、`BACKLOG.md`、task dossier、evidence surface 的 semantic responsibility與 default-load policy由 `AI_CONTEXT.md` 維護。本節只定義 persistence / execution admission 與 backward compatibility。

### No persistence / Cold / Hot

Planning decision 預設先分：

`No persistence → Cold admission（若 project 有 Cold surface）→ Hot admission`

- **No persistence**：一次性 observation/recommendation，沒有 material durable tracking value。
- **Cold**：值得長期記得，但目前不是 executable/critical path；只有 project已 opt-in Cold surface時才使用。
- **Hot**：current executable / critical-path coordination，進 current Hot surface（通常 `/TASKS.md`）。

Single-Surface Mode 沒有 Cold surface時，不應把所有 future idea機械塞進 TASKS。只有真正達到 Hot/active tracking門檻或不保存會造成 material loss時才進 TASKS；其餘保持 discussion/architecture analysis，或由使用者另行授權 project採用 Cold Registry。

### Durable Work Admission

**Observation ≠ recommendation ≠ admitted work。** 發現問題、提出建議、使用者覺得「有道理」都不會自動把它升格成 project obligation。

在建立 durable TASKS/BACKLOG/task dossier前，至少確認存在 material durable value，例如：

- 使用者明確要求保存／處理；
- current task留下可具名且 material 的 unresolved；
- 明確 blocker / dependency / trigger；
- 現實或 architecture premise 改變，使新工作現在才成立；
- 已決定要做但等待時機/evidence；
- 不保存會使已確認的重要工作容易遺失。

AI 主動提出的改善若 evidence 尚不足，只因使用者簡短同意／覺得合理而希望「先記著」，優先以 `CANDIDATE` 或 project equivalent 的低 authority Cold item保存（project有 Cold surface時），清楚保留 why/evidence/trigger/current obligation；不得把 persistence本身當成必要性證據。

**Persistence does not increase recommendation authority。**

### Candidate / Committed / Hot promotion

- `CANDIDATE`：AI/review提出，值得保留重評，但未決定一定做；
- `COMMITTED`：已確認未來需要處理，只是現在不是 Hot；
- Hot：trigger/critical path成立後，先重新讀 current authority/evidence，再 promote到 Hot surface。

Project 不必使用固定字串，但不得把 Candidate因「已在 repo 裡」自動視為 committed debt。

Cold item不能直接 Short-launch。任何 Cold → Hot promotion 都是 planning/reconciliation decision；Codex不得因看到 BACKLOG item就自行執行或自行 promote。

### Task identity / revision

同一工作的 wording改善、evidence增加、status更新、implementation detail變清楚，而核心 goal / completion criterion / authority premise未改時，優先視為同一 task revision，避免建立 duplicate durable item。

目標本質、completion criterion、architecture premise materially改變，或 conditional branch真正成立形成獨立 execution/validation lifecycle時，才建立新 task／child task。

### Pending / Blocked classification

Pending-validation / Blocked 是否 Hot 或 Cold依 `AI_CONTEXT.md` 的 critical-path規則，不再機械式一律塞進 TASKS。

### Hot completion

Hot item成功且完成必要 evidence後，從 active Hot surface移除／收斂；completed history以 Git history為主，不在 active queue長期保留。

若 project採 persistent `TASKS.md` mode，最後一個 Hot item移除後可收斂成最低充分 `EMPTY` template。`EMPTY`只代表目前沒有 admitted Hot work，不代表沒有 Cold/Candidate/evidence/technical debt或專案已完成。

在宣告完成、移除 Hot entry 或進下一 Stage前，只要本 Stage宣稱 repository mutation、commit/push、coordination bookkeeping或 validation-state變更，依 `DEBUG_VALIDATION.md` Completion Evidence Guard做最低充分 canonical read-back。

## ChatGPT／Codex Repository 寫入邊界（ChatGPT / Codex Repository Write Boundary）

### ChatGPT — 一般 project

- 只可直接建立／更新 project governance**明確列入 ChatGPT Coordination Write Allowlist**的 path；default只有 root `/TASKS.md`。
- Project opt-in後，可直接維護其列出的 `/BACKLOG.md`、Hot task dossier、sanitized evidence staging；未列出的其他 path仍一律 read-only。
- `AGENTS.md`、README/docs、正式 architecture/protocol/validation authority、source、tests、scripts、tooling、workflow/CI、config、manifest、lock files等，除非 repository明確定義更高層特殊例外，仍由 ChatGPT唯讀。
- Evidence staging只能寫 repo-safe / sanitized內容；不得先把 secret/private raw material commit後再刪。
- 非 allowlisted檔案需要修改時，ChatGPT只做 analysis/planning、在適當 coordination surface保存最低充分 handoff，再由 Codex在明確 Stage授權內修改。
- 收到 Codex結果後，涉及 remote repository state claim時依 Completion Evidence Guard做 GitHub remote read-back。
- 使用者直接要求 ChatGPT修改非 allowlisted source/docs，不自動越過此 boundary；除非使用者明確修改治理 contract本身，且該 governance mutation以合法方式完成。

### Codex／coding agent

- 在使用者當次明確授權 Task/Stage scope內，依 repository governance修改 allowed files。
- 可依 project governance維護當次 Stage相關的 Hot coordination status/evidence bookkeeping，但不得自行執行其他未授權 Hot item，也不得因讀到 Cold/Candidate item就開始工作。
- Cold → Hot promotion、AI-originated candidate升格與新的 durable work admission原則上屬 planning/reconciliation decision；Codex只能在 Stage明確要求時做對應 bookkeeping。

### Shared coordination safety

- ChatGPT與Codex修改任何 shared coordination surface前都先讀 latest GitHub / synced local state，避免覆蓋彼此新內容。
- Coordination surface不是 changelog，也不是第二份 canonical architecture/evidence truth；canonicalization後依 `AI_CONTEXT.md` 收斂成 pointer + current delta。
- Hot/Cold/Evidence surface本身都不自動授權 Codex execution，也不擴張 ChatGPT對其他 path的寫入權。

### Playbook Repository 例外（Playbook repository exception）

`masini1491/ai-development-playbook` 本身是共通規則來源，由 ChatGPT直接維護；Codex對此 repository預設唯讀。此例外只適用 playbook自身，不改變一般 project repository的上述 boundary。
