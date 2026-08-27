# Repository 執行規則（Repository Execution Rules）

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

### External service staged operation

當 external service 同時存在 read-only API、live runtime evidence 與 mutation/admin capability 時，優先把 operation 分成明確 Stage，而不是一次取得較大 scope：

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

## TASKS.md 生命週期（TASKS.md Lifecycle）

`TASKS.md` 是一般 project repository 的唯一 active unfinished-work / executable scoped Prompt queue（若 repository 採此模式）。

只保留：
- TODO
- Blocked
- Deferred
- Pending-validation

完成紀錄以 Git history 為準；不建立 Completed 區段。

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

Task 成功驗證後刪除/更新該 unfinished item；完全清空時刪除 `TASKS.md`。

在宣告 Task/Stage 完成、移除對應 queue entry 或進入下一 Stage 前，只要本 Stage 宣稱發生 repository mutation、commit/push、queue bookkeeping 或 validation-state 變更，必須依 `DEBUG_VALIDATION.md` 的 **Completion Evidence Guard**，以最低充分 canonical repository evidence 交叉確認完成狀態。若 agent completion report 與 current Git / scoped diff / validation / `TASKS.md` state 不一致，立即 STOP；不得以自然語言 summary 覆蓋 repository evidence，也不得沿用該 completion report 繼續下一 Stage。

## ChatGPT／Codex Repository 寫入邊界（ChatGPT / Codex Repository Write Boundary）

對**一般目標 project repository**，預設固定分工：

### ChatGPT

- 只對 repository root `TASKS.md` 具有建立、讀取、更新與刪除權。
- 除 `TASKS.md` 外，所有 repository path 一律唯讀，包括 `AGENTS.md`、README/docs、source、tests、scripts、tooling、workflow/CI、config、manifest、lock files 等。
- 可以讀取、分析 evidence、比較版本、提出修改方案與產生 Codex Prompt，但不得直接建立、更新、刪除或改名其他 path。
- 若非 `TASKS.md` 檔案需要修改：先讀最新 evidence、避免 duplicate task，必要時只在 root `TASKS.md` 建立/更新 scoped unfinished task / executable Prompt，再由 Codex 執行真正修改。
- 使用者直接要求 ChatGPT 修改 AGENTS/README/source，也不自動越過此 boundary；除非使用者明確修改這條治理規則本身。

### Codex／coding agent

- 在使用者當次明確授權的 Task / Stage scope 內，依 repository governance 修改 `TASKS.md` 以外的 allowed files。
- 同時可維護 `TASKS.md` 的執行狀態：更新 Blocked / Deferred / Pending-validation evidence、成功完成並驗證後移除 entry、queue 清空時刪除 `TASKS.md`。
- 不得因具有 workspace write capability 就自行執行 queue 中其他未授權項目。

### `TASKS.md` 共同維護

`TASKS.md` 是 **ChatGPT 與 Codex 共同維護**的唯一 active unfinished-work / executable scoped Prompt queue：

- ChatGPT 主要負責 analysis、admission、scope、建立/調整 future work、避免 duplicate。
- Codex 主要負責執行當次授權 Stage 後的 status/evidence bookkeeping 與完成後移除 entry。
- 雙方修改前都應先讀最新 GitHub / synced local `TASKS.md`，避免覆蓋彼此新內容。
- `TASKS.md` 不是 changelog；Completed 不保留，完成紀錄以 Git history 為準。
- `TASKS.md` 本身不授權 Codex 自動開始任何 Stage，也不擴張 ChatGPT 對其他 path 的寫入權。

### Playbook Repository 例外（Playbook repository exception）

`masini1491/ai-development-playbook` 本身是共通規則來源，由 ChatGPT 直接維護；Codex 對此 repository 預設唯讀。此例外只適用 playbook 自身，不改變一般 project repository 的上述 boundary。