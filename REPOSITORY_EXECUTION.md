# Repository 執行規則（Repository Execution Rules）

> **Authority**：Repository identity、write scope、workspace／network／credential permission、remote Git、external-service operation、canonical repository evidence、TASKS lifecycle、ChatGPT／Codex repository write boundary。
> **Read when**：目前工作涉及 Git/repository、permission/capability、remote service mutation/read-only boundary、TASKS、repository-facing claims 或 ChatGPT/Codex 寫入分工。
> **Usually skip when**：只是純 architecture/research、source-level root cause/validation、UI／UX 或 embedded hardware semantics。
> **Progressive reading**：先依下方 Section Router 定位；找到 relevant heading 後只讀該 section 與必要相鄰 dependency，不預設載入全文。

## Section Router

- repo/branch/HEAD 身分、聊天室 writable target → `Repository 身分確認關卡`、`聊天室級 Repository 寫入鎖`
- workspace／sandbox／filesystem／network／credential capability → `Workspace 寫入能力關卡`、`授權與能力分層`、`權限關卡操作`
- sync／fetch／push → `安全 Remote Sync 啟動`、`Remote Git 權限關卡`
- external service read-only / mutation / staged operation → `權限關卡操作` 內的 external-service sections
- hash／LOC／manifest／public README claim → `Canonical Repository Evidence`、`Repository-facing 文件完整性`
- TASKS queue／admission／debt → `TASKS.md 生命週期`
- ChatGPT／Codex 哪些 path 可寫 → `ChatGPT／Codex Repository 寫入邊界`

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
- Current Write Target 以外的 repository，即使可被 GitHub connector／credential 讀寫，也只能讀取、搜尋、比較、review、取得 evidence 或產生建議／Prompt；**不得建立、更新、刪除或改名其任何 path，包括 `TASKS.md`、`AGENTS.md`、source、docs、tests、workflow 或其他檔案。**
- `Current Write Target Repository` 只是 repository-level 必要條件，不增加任何 path/action 權限。實際 mutation 仍須同時符合該 repository governance、ChatGPT／Codex write boundary、目前 Task/Stage authorization、execution permission 與 credential capability。
- 發現另一 repository「也應同步」、「順便對齊」、「同樣需要修」、「規則看起來應一起改」或存在合理 cross-repo follow-up，只建立 read-only analysis／handoff；不得據此推導第二個 writable repository。
- 「好」、「繼續」、「照這樣做」等承接語句，以及對目前工作的一般同意，不構成 write-target switch。若新的 mutation request 指向不同 repository，必須由使用者**明確指定切換 writable repository**或等價清楚意圖；在此之前 STOP 該 repository mutation。
- Write target 一旦明確切換，舊 target 立即回到 read-only；**同一聊天室不得同時保留兩個 writable repositories。**
- `masini1491/ai-development-playbook` 的 ChatGPT-maintainer 例外也受本 gate 限制：只有它是本聊天室 Current Write Target 時，ChatGPT 才可直接維護手冊；若聊天室目前鎖定其他 project repository，手冊在該聊天室同樣 read-only。
- 這個 write lock 不限制合法的跨 repository read-only research／comparison，也不代表另一個獨立聊天室或另行明確啟動的 execution session 自動沿用本聊天室 target；每個 conversation/session 依其自己的明確授權建立 write boundary。

對本聊天室直接 repository mutation，可視為：

`Allowed mutation = Current Write Target match ∩ Repository governance ∩ Task/Stage authorization ∩ Execution permission ∩ Credential capability`

核心原則：**Repository access ≠ conversation write authority；先鎖定唯一 writable repository，再判斷該 repository 內實際允許寫什麼。**

## Workspace 寫入能力關卡（Workspace Write Capability Gate）

在任何**需要修改 repository** 的 Task / Stage 開始 file mutation 前，先確認 execution environment 對目標 working tree 具有完成該 Stage 所需的最小寫入能力。

Read-only work（例如 research、code review、architecture analysis、evidence review、read-only validation inspection）若不需要 mutation，可在 read-only workspace 繼續。

Write-required work（例如 source/tests/docs 修改、`TASKS.md` bookkeeping、commit preparation）若目前 workspace 為 read-only 或無法進行必要 file write：

- 標記為 `WORKSPACE WRITE CAPABILITY MISSING`；
- 若 runtime 提供 workspace-write / sandbox permission request，主動要求最小必要 capability；
- 若必須由使用者在 Codex UI / execution setting 切換為 workspace-write，清楚回報所需設定；
- capability 未取得前 STOP，不進入 coding/debug loop；
- 不得分類為 SOURCE failure，也不得修改 production source 來「修」環境問題；
- 不得用 temporary copy、另一份 clone、另一 repository、改 Git metadata location、廣泛 chmod、sudo 或其他 workaround 繞過。

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
9. 同步後重新讀最新 local `AGENTS.md` / `TASKS.md`。
10. 若指定 Task/Stage 已消失或被改變到 launch 失效，STOP，不得依舊 Prompt/記憶執行。

若 project governance 明確宣告採用 persistent `TASKS.md` mode，而同步後 `TASKS.md` 缺失，不得把「檔案不存在」直接解讀為 EMPTY；先依最新 project governance / Git evidence 判斷是否為尚未初始化、意外刪除或明確退出 TASKS mode。需要建立／恢復檔案時仍須落在目前授權的 bookkeeping scope。

禁止 autonomous：
- `reset --hard`
- force push
- merge / rebase / cherry-pick
- auto-stash
- delete/discard unknown user work
- checkout overwrite
- rewrite history

Commit/push 必須服從使用者當次 launch 或 repository policy 的明確授權；TASKS item 本身不自動授權 Git mutation。

## 授權與能力分層（Authorization / Capability Layers）

任何 Git、filesystem、toolchain、network 或 external-service operation，都應分開判斷三個互不等價的邊界：

1. **Task / Stage Authorization**：使用者與 repository governance 本次實際允許做什麼。
2. **Execution Permission**：sandbox / network / filesystem / repository metadata / runtime 是否允許執行該 operation。
3. **Credential Capability**：目前 account、token、key、session 或 service credential 技術上能做什麼。

真正允許執行的 operation 只能落在三者交集內：

`Allowed operation = Task/Stage authorization ∩ Execution permission ∩ Credential capability`

因此：

- execution permission 比目前 Stage 大，不代表 scope expansion；
- credential 具備 deploy、write、admin 或 delete 能力，不代表目前 Stage 已授權使用；
- network approval 只解除目前已授權 operation 的連線 gate，不建立新的 Git / service mutation authorization；
- Task / Stage 已授權某項 mutation，也仍須滿足必要 execution permission 與 credential capability；
- 任一層不足時，只處理該層實際缺口，不得以其他層的較大能力補推授權。

## 權限關卡操作（Permission-Gated Operation）

本規則適用於目前已授權 Task / Stage 所必要的 Git、build、test、toolchain、filesystem、remote network、external API / CLI / HTTPS、package registry / dependency retrieval 或其他外部服務 operation。

1. 必要 operation 若因 sandbox、filesystem、repository metadata、execution permission、network policy、`Permission denied` / `Access denied` / `EACCES` / `EPERM`、唯讀 workspace 或等價 execution gate 受阻，先判斷是否只是可由使用者批准解除的 permission gate。Permission gate 本身不是 source、toolchain、environment、infrastructure、service、authentication 或 authorization failure。
2. 若**事前已知**該必要 operation 需要額外 sandbox / network / filesystem / metadata permission，應在執行前主動要求最小必要 capability；不得故意先執行已知會被拒絕的 command 來製造一次 failure。
3. 若事前無法判定是否需要額外 permission，可正常執行一次；第一次明確 permission denial 後立即轉 Permission-Gated Operation，不進入 operational failure taxonomy。
4. Permission request 應盡量說明：
   - exact command / operation；
   - 為何目前 Task / Stage 必須執行；
   - 被阻擋 resource/path（若已知）；
   - service host / port（外部連線且能合理限定時）；
   - 所需的最低 permission scope/type。
5. 使用者批准後，只重試原本被 gate 阻擋的必要 operation。Approval 不授權 scope expansion、額外檔案修改、下一 Stage、其他 Git workflow、deploy/publish、resource mutation 或任何原 Stage 未授權操作。
6. `permission denial → request minimum permission → approval → retry original operation` 不計 operational retry cap。只有取得必要 permission 後同一 operation 仍真正失敗，才開始 operational retry accounting 與 failure classification。
7. 若使用者拒絕、runtime 無法 request/obtain permission，或取得最低必要 permission 後 operation 仍真正失敗，才依 evidence 進入 `DEBUG_VALIDATION.md` 的 operational failure taxonomy。
8. 不得以 permission 問題為理由自行使用危險 workaround，例如 `sudo`、`chmod -R 777`、未經批准的廣泛 `chmod` / `icacls`、刪除 Git state/lock file、重新 clone 覆蓋 working tree、改 Git metadata location、stash/delete/discard unknown user work、reset-hard、force push、auto merge/rebase/cherry-pick 或改用另一 repository。疑似 stale lock 也不得在沒有 evidence 與明確授權時自行刪除。

### External network / service 邊界

對 remote Git、cloud/service CLI、HTTP API、package registry、dependency download、MQTT/service administration 或其他外部 operation：

- 若已知目前必要 operation 需要 external network，先要求最低 network approval；若未知，首次明確 sandbox/network denial 後再要求。
- Network/sandbox approval 只允許**目前已授權 operation**建立必要外部連線，不自動授權 deploy、publish、subscribe/disconnect、configuration mutation、authentication/authorization/ACL mutation、secret/credential mutation、resource create/delete 或其他 service-side write。
- 若原 Task / Stage 本來已明確授權某項 remote mutation，network approval 也只解除該項 operation 的 execution gate，不擴張到其他 remote action。
- Credential capability 大於目前 Stage scope 時，實際執行範圍仍以 Stage authorization 為上限。
- 外部服務操作與 error/reporting 不得輸出 password、token、Authorization header、private key、shared secret、credential material 或不必要的 secret-derived characteristics，也不得把 credential 寫進 Git。
- **Read-only / mutation 必須依 operation semantics 與可觀察 side effect 判斷**，不得只看 HTTP verb、CLI command 名稱、tool/plugin label 或 UI wording。`GET` 不保證無 side effect，`POST` 也不必然代表 mutation；真正判斷點是是否會改變 remote state、credential/security state、resource lifecycle、session/connection、delivery/job 狀態，或觸發其他具有持久／外部效果的 operation。
- 若 service/tool 對 side effect 定義不清楚，先查 authority/documentation 或以最小 read-only evidence確認；無法確認時不得把它假定成安全 read-only operation。
- 若需要判斷 external-service 文件應如何依 provider、credential、configuration、resource lifecycle、deployment/mutation 或 validation authority 拆分，以 `RESEARCH_ARCHITECTURE.md` 的 **External-service authority separation** 為主要規則；本節不重複維護文件架構 policy。

### Public read-only anonymous-first（最低充分 Access Capability）

對 GitHub 或其他 service 的**已確認 public resource**，若目前 operation 是純 read-only，而且官方 endpoint 的 anonymous / unauthenticated access 已足以取得本 Stage 所需 evidence，優先使用較低的 access capability，避免不必要消耗 authenticated API quota 或暴露較大 credential capability。

適用條件必須同時成立：

- resource visibility 已確認為 public；若 private 或 visibility 不確定，不得先假設 anonymous 可替代；
- operation 依實際 semantics 為 read-only，不造成 remote state / session / delivery / resource lifecycle 等 side effect；
- 使用 provider 官方 endpoint / protocol，不為省 quota 自行切 mirror、proxy、scraper、第三方 gateway 或其他非 authority source；
- 不需要 private、installation-only、account-specific、organization-specific 或 authenticated-only metadata；
- anonymous access 不會降低目前 Stage 必要的 evidence quality、provenance、完整性或可重現性。

推薦 capability escalation：

`public anonymous read-only → authenticated read-only（必要時）→ authenticated mutation（只有明確授權時）`

一般原則：

- `anonymous-first` 是**最低充分 Access Capability**，不是 `anonymous-only`；anonymous rate limit、quota 或 capability 不足時，可在目前 Task / Stage 確實需要的範圍內升級 authenticated read-only。
- authenticated read-only access 因 `RATE_LIMIT` / `QUOTA_EXHAUSTED` 暫時不可用時，若上述條件仍成立，改用同一 provider 官方 anonymous read-only endpoint 可視為 capability downgrade，而不是 scope expansion；治理規則本身不要求額外 Task authorization。
- 但 execution environment 若對 anonymous request 本身仍要求 network / sandbox approval，照常走 Permission-Gated Operation；本節不繞過 runtime permission gate。
- 不得因 quota exhausted 自行輪替另一帳號、另一 token、另一 installation、另一 credential、proxy/mirror 或第三方服務；這些屬新的 identity / authority boundary，必須依目前 Task scope與相關授權另行判斷。
- public anonymous fallback 不得被用來碰觸 private repository、private issue/attachment、installation-only resource，或把已知需要 authentication 的 evidence 改成較弱的猜測。

核心原則：**Capability downgrade ≠ scope expansion；但 identity/source boundary change ≠ ordinary retry。**

### External service staged operation

當 external service 同時存在 read-only API、live runtime evidence 與 mutation/admin capability時，優先把 operation 分成明確 Stage，而不是一次取得較大 scope：

1. **Stage 1 — Read-only baseline**：確認 service/account/target identity、非敏感 resource/config metadata、credential 是否存在（不讀 secret value）、API access 與目前 baseline evidence。
2. **Stage 2 — Live observation**：在真實 application/device/client 正常運作時，使用 read-only capability 觀察 current connection、subscription/session/resource/status、reconnect/disconnect、delivery 或其他 live evidence；不因觀測需要而主動製造 mutation。
3. **Stage 3 — Explicit mutation**：deploy、publish、configuration change、resource create/delete、disconnect/kick、ACL/auth/credential mutation 或其他 service-side write，只有目前 Task / Stage 明確授權 exact target + exact mutation + validation scope 時才可執行。

Stage 1 / 2 的 read-only approval、evidence 或 credential capability不得自動推導 Stage 3 mutation authorization。若觀測結果不足以判斷 root cause，取得最小下一層 evidence或 STOP；不要為了「方便測試」直接升到 mutation。

External-service validation 必須區分 access/preflight PASS、local/dry-run PASS、remote mutation success、read-only smoke PASS、end-to-end/live runtime PASS 與 production/hardware PASS；低層 PASS 不得翻譯成更高層完成。

## Remote Git 權限關卡（Remote Git Permission Gate）

對目前 Task / Stage 所必需且**本來已獲授權**的 remote Git operation，套用上述 Authorization / Capability Layers 與 Permission-Gated Operation。

- 若已知 remote Git operation 需要額外 network / repository-metadata / filesystem permission，執行前先要求實際缺少的最低 capability。
- 若事前未知，可正常嘗試一次；首次明確 permission denial 後立即進 permission flow。
- approval 後只重試原 remote Git operation，不附帶執行其他 Git mutation。
- permission resolution 不計 operational retry。
- 使用者拒絕、runtime 無 escalation 能力，或取得 permission 後相同 operation 仍真正失敗，才依 evidence 分類。

### `git fetch origin` 特例

`git fetch origin` 可能同時需要兩種互相獨立的最低 capability：

1. remote network access；
2. 本地 `.git/FETCH_HEAD`、lock/ref 與 repository metadata 的 filesystem / metadata write capability。

只要求實際缺少的 capability。批准後只重試完全相同的 fetch；不得把 fetch permission 解讀為 pull、merge、rebase、push 或其他 Git mutation authorization。

### `git push` 邊界

Sandbox/network permission approval **不等於 Git mutation authorization**。

只有當目前 Task / launch / repository policy 原本就已明確授權 push 時，permission escalation 才能解除該 push 的 execution/network gate；不得把 permission approval 解讀成新的 push 授權。

## Canonical Repository Evidence（Canonical Repository Evidence）

需要跨機器、跨 OS 或跨工作區重現的 repository evidence，不應無條件依賴 platform-transformed working-tree bytes。

適用範圍例如：

- source hash / integrity manifest
- project-scale / physical-line 統計
- canonical baseline snapshot
- reproducible source inventory
- retention / required-file manifest 驗證

原則：

1. 若 evidence 的語意是「某個 Git ref/commit 內實際追蹤的內容」，優先以 Git canonical object / tracked content 為 authority，例如 `git ls-tree`、`git cat-file` 或等價機制。
2. 若必須從 working tree 計算，應明確定義 canonicalization contract；text file 的 CRLF/LF、encoding/BOM 或其他平台轉換若會影響 hash/line count，必須先正規化或明確宣告其語意。
3. 不得把 `.git`、build/cache、generated artifacts、downloaded dependencies 或未追蹤暫存檔混入 canonical source evidence，除非該 evidence contract 明確要求。
4. Hash / line count / manifest 的計算方法本身屬 validation contract；跨平台結果不一致時先檢查 canonicalization / tool behavior，不得先推論 source 被修改。
5. 若 repository 已有 canonical counter/hash tool，後續文件與 validation 優先使用該 authority，不要同時維護另一套手工算法造成 drift。

Canonical evidence 解決的是「如何重現 repository 事實」，不取代 runtime/build/hardware validation。

## Repository-facing 文件完整性（Repository Documentation Integrity）

公開 README、showcase、project overview 或其他 repository-facing 文件若宣稱開發方式、驗證狀態、專案規模或 AI-assisted workflow，應讓 claim 可追溯到正確 authority；README 本身不應成為另一套重複的 execution/validation policy。

### AI-assisted development transparency

公開 repository 若明顯使用 ChatGPT、Codex 或其他 coding agent 作為主要開發方式，README 可精簡說明 human-in-the-loop 責任分工，例如：

- **Human / developer**：需求、產品方向、現實世界／硬體 evidence、最終核准，以及需要人工完成的 validation；
- **ChatGPT / planning agent**：研究、architecture/spec discussion、review、task decomposition 與 Prompt / unfinished-work planning；
- **Codex / coding agent**：在授權 scope 內 implementation、tests、static/build validation、docs 與 repository maintenance。

一般原則：

- AI 產生 code／analysis、command success 或 build exit code 0 不等於產品已完成所有必要 validation；公開 wording 必須符合實際 evidence tier。
- 若 README 提及 OpenAI／ChatGPT／Codex，不得暗示 provider 對 project/product/hardware/security decision 提供贊助、認證或背書，除非確有正式關係。
- README 只需摘要責任分工；詳細 ChatGPT/Codex write boundary、Task/Stage authorization、completion evidence 仍由本文件與其他 canonical topic file 維護。

### Project Scale Reporting

若 README 或公開文件展示 LOC、行數、檔案數量或其他 project-scale statistics：

- 說明統計基準，例如 Git tracked files、正式 ref/commit 或其他可重現來源；
- 定義指標，例如 physical lines、logical/executable LOC、file count；若是 physical lines，說明是否包含 blank/comment；
- 說明主要排除項目，例如 `.git`、third-party dependencies、downloaded packages、build/cache、generated artifacts；
- 分類方式依 repository 實際 structure 定義，不要求所有專案使用同一 taxonomy；
- 統計應服從本文件的 Canonical Repository Evidence，不因不同 OS newline/working-tree transform 產生無法解釋的 drift。

不要求每個 repository 建立專用計數 script。只有當公開數字長期存在且頻繁改變、手工更新容易漂移，或同一統計要同步到多個正式文件時，才優先建立 repository-owned deterministic counter。

已有正式 counter 的 repository，在主要 tracked-file 變更與相關 validation 完成後更新統計；數字未變時不要製造無意義 README diff。跨 repository showcase/private→public 同步若有特殊規則，留在各 project governance。

核心原則：**公開 repository claim 應可由 canonical evidence 重現；README 負責說明，不自行複製底層治理規則。**

## TASKS.md 生命週期（TASKS.md Lifecycle）

`TASKS.md` 是一般 project repository 的唯一 active unfinished-work / executable scoped Prompt queue（若 repository 採此模式）。對採用此模式的 repository，`TASKS.md` 應作為**持久、固定路徑的 coordination surface**；有無 active work 以檔案內容的 queue state 表達，不以檔案存在與否表達。

只保留：
- TODO
- Blocked
- Deferred
- Pending-validation

完成紀錄以 Git history 為準；不建立 Completed 區段。

### EMPTY queue

當最後一個 unfinished item 被移除時，不刪除 `TASKS.md`；改為收斂成最低充分的 `EMPTY` queue template。Idle template 應保持很短，只需保留：

- 本檔是 active unfinished-work / executable scoped Prompt queue；
- Completed 不保留，完成事實以 Git history 為準；
- 本檔存在不代表授權任何 Stage；
- `Queue status: EMPTY` 或等價明確狀態；
- 目前沒有 TODO / Blocked / Deferred / Pending-validation；
- 必要時一行 routing，要求新增工作前依 project governance 與本節 Admission threshold 判斷是否收錄。

`EMPTY` **只代表目前沒有被 admission 進 active queue 的 unfinished work**。不得由 EMPTY 推論專案已完成、沒有技術債、沒有未觸發 roadmap、沒有 historical/pending evidence，或其他正式文件中的 validation / product state 已全部完成。

若 repository 明確採用 persistent TASKS mode，而 `TASKS.md` 缺失，missing 與 EMPTY 不等價；先依 project governance / Git evidence 判斷原因。只有 repository 明確退出 TASKS mode 或 governance 被明確修改時，才應刪除該固定 coordination surface。

### 收錄門檻（Admission threshold）

以下通常可不進 TASKS：
- 一次性
- 已知位置
- 已知修改內容/root cause
- scope 小、風險低
- 完成後無追蹤價值
- 不影響 behavior/architecture/protocol/security/hardware/persistence/runtime/重要 validation

以下任一情況應進 TASKS：
- 需要後續追蹤
- Blocked / Deferred / Pending-validation
- 多 Stage
- 有 dependency / trigger
- root cause 未確認
- 可能後續 implementation
- material system/validation effect
- 不記錄容易遺漏

Task 成功驗證後刪除/更新該 unfinished item；最後一項移除後依上述 EMPTY queue contract 收斂 `TASKS.md`，不因 queue 清空而刪檔。

### 觸發式技術債／佇列衛生（Triggered Technical Debt / Queue Hygiene）

**發現技術債不等於立即修，也不等於應把所有候選一次塞進 `TASKS.md`。** `TASKS.md` 是 active unfinished-work / executable scoped Prompt queue，不是 refactor 願望清單或永久 debt register。

一般原則：

- 對不影響目前 correctness、安全、正式 contract 或必要 validation 的 maintenance、documentation、structure、naming 或 modularity debt，若立即處理會打擾正在使用的 baseline、增加 unrelated diff、擴張目前 Stage 或使重要 evidence 失效，優先保持 Deferred，而不是「順手清掉」。
- 多個真實 refactor candidate 同時存在時，只把**下一個可執行且有明確 trigger / dependency / validation boundary** 的 Stage 提升為 active work。其他候選若不記錄容易遺失，才以精簡 Deferred item 保存；不得把整份 architecture wish list 轉成可執行 queue。
- Deferred debt 至少應能回答：`why / owner or surface / trigger / blocked-by or dependency / allowed scope / required revalidation`。若連 trigger 與完成邊界都尚不清楚，優先保留在 architecture analysis / discussion，而不是建立模糊 TASKS item。
- Trigger 成立且同一 owner/surface 本來就要合法修改時，可以在不擴張 behavior scope 的前提下合併低風險 maintenance；但必須保留明確 scope，不能把「反正正在改附近」當成 general cleanup、renaming spree、library extraction 或 architecture redesign 的授權。
- 若目前有被 freeze 的 runtime/hardware/performance baseline，與該 baseline 無關且不影響 correctness 的 debt 通常等到 baseline 不再需要、或同一 surface 出現合法修改 Stage 時再處理。若 debt 本身正在阻礙取得必要 evidence，則可另立最小 scoped Stage，不必為了保護 baseline 永久延後。
- Active debt Stage 完成後重新評估 repository current state，再決定下一個候選；不要因先前 inventory 一次列出很多問題，就自動串行執行全部後續 refactor。

核心原則：**技術債用 trigger、ownership 與 evidence boundary 管理，不用「看到就修」或「全部排進 TASKS」管理。**

在宣告 Task/Stage 完成、移除對應 queue entry 或進入下一 Stage 前，只要本 Stage 宣稱發生 repository mutation、commit/push、queue bookkeeping 或 validation-state 變更，必須依 `DEBUG_VALIDATION.md` 的 **Completion Evidence Guard**，以最低充分 canonical repository evidence 交叉確認完成狀態。若 agent completion report 與 current Git / scoped diff / validation / `TASKS.md` state 不一致，立即 STOP；不得以自然語言 summary 覆蓋 repository evidence，也不得沿用該 completion report 繼續下一 Stage。

## ChatGPT／Codex Repository 寫入邊界（ChatGPT / Codex Repository Write Boundary）

對**一般目標 project repository**，預設固定分工：

### ChatGPT

- 只對 repository root `TASKS.md` 具有建立、讀取與更新權；採用 persistent TASKS mode 時，正常 queue lifecycle 不刪除該檔。只有 repository 明確退出 TASKS mode 或使用者明確修改此治理 contract 時，才可依授權刪除。
- 除 `TASKS.md` 外，所有 repository path 一律唯讀，包括 `AGENTS.md`、README/docs、source、tests、scripts、tooling、workflow/CI、config、manifest、lock files 等。
- 可以讀取、分析 evidence、比較版本、提出修改方案與產生 Codex Prompt，但不得直接建立、更新、刪除或改名其他 path。
- 若非 `TASKS.md` 檔案需要修改：先讀最新 evidence、避免 duplicate task，必要時只在 root `TASKS.md` 建立/更新 scoped unfinished task / executable Prompt，再由 Codex 執行真正修改。
- 收到 Codex／coding agent 的執行結果後，若結果涉及 GitHub repository tracked-file 修改、commit、push、queue bookkeeping 或其他遠端 repository state claim，ChatGPT 在接受「完成」或據此推進下一 Stage 前，必須依 `DEBUG_VALIDATION.md` 的 **Completion Evidence Guard** 執行 GitHub remote read-back；Codex 的自然語言 summary 本身不是完成 authority。
- 使用者直接要求 ChatGPT 修改 AGENTS/README/source，也不自動越過此 boundary；除非使用者明確修改這條治理規則本身。

### Codex／coding agent

- 在使用者當次明確授權的 Task / Stage scope 內，依 repository governance 修改 `TASKS.md` 以外的 allowed files。
- 同時可維護 `TASKS.md` 的執行狀態：更新 Blocked / Deferred / Pending-validation evidence、成功完成並驗證後移除 entry；queue 清空時依 EMPTY queue contract 收斂檔案，不刪除固定 coordination surface。
- 不得因具有 workspace write capability 就自行執行 queue 中其他未授權項目。

### `TASKS.md` 共同維護

`TASKS.md` 是 **ChatGPT 與 Codex 共同維護**的唯一 active unfinished-work / executable scoped Prompt queue：

- ChatGPT 主要負責 analysis、admission、scope、建立/調整 future work、避免 duplicate。
- Codex 主要負責執行當次授權 Stage 後的 status/evidence bookkeeping 與完成後移除 entry。
- 雙方修改前都應先讀最新 GitHub / synced local `TASKS.md`，避免覆蓋彼此新內容。
- `TASKS.md` 不是 changelog；Completed 不保留，完成紀錄以 Git history 為準。
- Queue 無 unfinished item 時保留最小 `EMPTY` state；EMPTY 是 queue state，不是 project completion state。
- `TASKS.md` 本身不授權 Codex 自動開始任何 Stage，也不擴張 ChatGPT 對其他 path 的寫入權。

### Playbook Repository 例外（Playbook repository exception）

`masini1491/ai-development-playbook` 本身是共通規則來源，由 ChatGPT 直接維護；Codex 對此 repository 預設唯讀。此例外只適用 playbook 自身，不改變一般 project repository 的上述 boundary。