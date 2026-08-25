# Repository Execution Rules

## Repository Identity Gate

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

## Workspace Write Capability Gate

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

## Safe Remote-Sync Bootstrap

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

## Permission-Gated Operation

已授權 Task/Stage 的必要 Git/build/test/toolchain/filesystem operation 若因 sandbox、filesystem、execution permission、`Permission denied` / `Access denied` / `EACCES` / `EPERM` 等受阻：

1. 先判斷是否是可由使用者批准解除的 permission gate。
2. 第一次 permission denial 不得直接判定 source/repository/remote/toolchain/environment/infrastructure 故障。
3. 若 runtime 支援 permission request，要求完成目前 operation 所需的**最小權限**，說明：
   - exact command / operation
   - 為何目前 Stage 必須執行
   - 被阻擋 resource/path（若已知）
   - 最小 permission scope/type
4. 使用者批准後只重試原本被擋的 operation；approval 不等於 scope expansion、額外檔案修改、下一 Stage 或高風險 Git 授權。
5. `permission denial → request → approval → retry original operation` 不計 operational retry cap。
6. 若使用者拒絕、環境無法要求權限、或取得權限後仍真正失敗，才依 evidence 進入 operational failure taxonomy。

## Remote Git Permission Gate

對目前 Task / Stage 所必需且**本來已獲授權**的 remote Git operation：

- 若 runtime / sandbox policy 已明確知道該 operation 需要額外 sandbox、network、filesystem 或 repository-metadata permission，必須在執行前主動要求最小必要權限；不得故意先執行已知會被拒絕的 command 再把 denial 當 failure。
- 若事前無法判定是否需要 escalation，可正常執行一次；第一次明確 permission denial 後立即轉 Permission-Gated Operation。
- approval 後只重試原 operation，不附帶執行其他 Git mutation。
- permission resolution 不計 operational retry。
- 使用者拒絕、runtime 無 escalation 能力，或取得 permission 後相同 operation 仍真正失敗，才進入 operational failure taxonomy。

### `git fetch origin` 特例

若出現：

- `.git/FETCH_HEAD` write denial
- Git lock/ref metadata write denial
- sandbox repository-metadata write denial
- required network permission gate

先走 Remote Git Permission Gate / Permission-Gated Operation；批准後只重試原 fetch。

### `git push` 邊界

Sandbox/network permission approval **不等於 Git mutation authorization**。

只有當目前 Task / launch / repository policy 原本就已明確授權 push 時，permission escalation 才能解除該 push 的 execution/network gate；不得把 permission approval 解讀成新的 push 授權。

不得用危險 workaround 繞過 permission gate，例如：
- `sudo`
- `chmod -R 777`
- 未經批准的廣泛 `chmod` / `icacls`
- 刪除 `.git/FETCH_HEAD`
- 未確認原因刪除 `.git/index.lock` 或其他 lock/state file
- 重新 clone 覆蓋 working tree
- 改用另一 repository
- stash/delete/discard unknown user work

## Canonical Repository Evidence

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

## TASKS.md Lifecycle

`TASKS.md` 是一般 project repository 的唯一 active unfinished-work / executable scoped Prompt queue（若 repository 採此模式）。

只保留：
- TODO
- Blocked
- Deferred
- Pending-validation

完成紀錄以 Git history 為準；不建立 Completed 區段。

### Admission threshold

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

## ChatGPT / Codex Repository Write Boundary

對**一般目標 project repository**，預設固定分工：

### ChatGPT

- 只對 repository root `TASKS.md` 具有建立、讀取、更新與刪除權。
- 除 `TASKS.md` 外，所有 repository path 一律唯讀，包括 `AGENTS.md`、README/docs、source、tests、scripts、tooling、workflow/CI、config、manifest、lock files 等。
- 可以讀取、分析 evidence、比較版本、提出修改方案與產生 Codex Prompt，但不得直接建立、更新、刪除或改名其他 path。
- 若非 `TASKS.md` 檔案需要修改：先讀最新 evidence、避免 duplicate task，必要時只在 root `TASKS.md` 建立/更新 scoped unfinished task / executable Prompt，再由 Codex 執行真正修改。
- 使用者直接要求 ChatGPT 修改 AGENTS/README/source，也不自動越過此 boundary；除非使用者明確修改這條治理規則本身。

### Codex / coding agent

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

### Playbook repository exception

`masini1491/ai-development-playbook` 本身是共通規則來源，由 ChatGPT 直接維護；Codex 對此 repository 預設唯讀。此例外只適用 playbook 自身，不改變一般 project repository 的上述 boundary。
