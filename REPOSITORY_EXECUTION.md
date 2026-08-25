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

## Safe Remote-Sync Bootstrap

執行已授權 Task/Stage 前：

1. Repository Identity Gate。
2. `git status --short`。
3. 確認 current branch / HEAD。
4. 確認無 merge / rebase / cherry-pick 等未完成 history operation。
5. `git fetch origin`。
6. 只有 expected branch + clean tree + local 無 ahead/diverged 且可 fast-forward-only 時才同步。
7. 同步後重新讀最新 local `AGENTS.md` / `TASKS.md`。
8. 若指定 Task/Stage 已消失或被改變到 launch 失效，STOP，不得依舊 Prompt/記憶執行。

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

已授權 Task/Stage 的必要 Git/build/test/toolchain/filesystem operation 若因 sandbox、filesystem、execution permission、read-only workspace、`Permission denied` / `Access denied` / `EACCES` / `EPERM` 等受阻：

1. 先判斷是否是可由使用者批准解除的 permission gate。
2. 第一次 permission denial 不得直接判定 source/repository/remote/toolchain/environment/infrastructure 故障。
3. 若 runtime 支援 permission request，要求完成目前 operation 所需的**最小權限**，說明：
   - command/operation
   - 為何目前 Stage 必須執行
   - 最小 permission scope/type
4. 使用者批准後只重試原本被擋的 operation；approval 不等於 scope expansion、額外檔案修改、下一 Stage 或高風險 Git 授權。
5. `permission denial → request → approval → retry original operation` 不計 operational retry cap。
6. 若使用者拒絕、環境無法要求權限、或取得權限後仍真正失敗，才依 evidence 進入 operational failure taxonomy。

### `git fetch origin` 特例

若出現 `.git/FETCH_HEAD: Permission denied`、Git lock/ref metadata write denial、sandbox 阻擋 `.git` metadata：先走 Permission-Gated Operation；批准後只重試原 fetch。

不得用危險 workaround 繞過 permission gate，例如：
- `sudo`
- `chmod -R 777`
- 未經批准的廣泛 `chmod` / `icacls`
- 刪除 `.git/FETCH_HEAD`
- 未確認原因刪除 `.git/index.lock` 或其他 lock/state file
- 重新 clone 覆蓋 working tree
- 改用另一 repository
- stash/delete/discard unknown user work

## TASKS.md Lifecycle

`TASKS.md` 是唯一 active unfinished-work / executable scoped Prompt queue（若 repository 採此模式）。

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

## ChatGPT / Agent write boundary

每個 repository 應自行定義 agent 的 direct-write 邊界。若採保守模式，可規定 ChatGPT 只直接寫 root `TASKS.md`，其他 source/docs/tests/workflows 由明確授權的 coding agent 或使用者修改。

本 playbook 不強迫所有 repository 使用相同 boundary，但 boundary 必須明確、可預測、不可因方便而默默放寬。
