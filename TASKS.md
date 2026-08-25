# TASKS

## Stage A — Workspace / Remote Permission / Agent Write Governance

**Status:** TODO  
**推薦模型：** Luna  
**推理強度：** Low  
**推薦理由：** 這是明確、低風險的 governance/documentation maintenance；既有專案已有成熟參考規則，不需要高階架構推理。  
**是否值得先用較便宜模型做前置蒐證：** 不需要；直接使用既有 repository evidence。  
**Context 建議：** Small / 只讀必要 policy files。  
**Execution mode 建議：** 單 Agent、focused maintenance。

### 目標 Repository

`masini1491/ai-development-playbook`

預期 branch：`main`

### 目的

把三個已在實際 ChatGPT / Codex 協作中形成、且跨專案都需要一致處理的治理規則收斂成 stable playbook governance：

1. Codex / sandbox 更新後 workspace 可能變成 read-only，導致需要修改 repository 的 Stage 無法正常寫檔。
2. Remote Git operation（尤其 `git fetch origin`）若需要 sandbox/network/repository-metadata permission，而 Codex 沒有主動要求使用者授權，會直接執行失敗。
3. ChatGPT 與 Codex 的 repository 寫入責任必須明確分工：ChatGPT 只直接讀寫 root `TASKS.md`；其他 repository path 對 ChatGPT 一律唯讀，真正修改由 Codex 執行；`TASKS.md` 由 ChatGPT 與 Codex 共同維護。

### Repository Identity Gate

開始前先確認：

- expected repository = `masini1491/ai-development-playbook`
- origin 對應此 repository
- current branch = `main`
- current HEAD
- working tree / unfinished Git operation 狀態

若 detected repository 不符，立即 STOP；不得自行切換、clone 或將本 Stage 套用到其他 repository。

### Safe remote-sync bootstrap

1. 先完成 Repository Identity Gate。
2. 檢查 `git status --short`、branch、HEAD、merge/rebase/cherry-pick state。
3. 需要 `git fetch origin` 時，先依下方 Remote Git Permission Gate 判斷是否需主動要求最小權限。
4. 只允許 clean expected branch 的 fast-forward-only sync。
5. dirty、unexpected branch、ahead/diverged、non-fast-forward 或 unfinished history operation → STOP。
6. 同步後重新讀最新 `AGENTS.md`、`TASKS.md`；若本 Stage 已消失或內容實質改變，STOP。

### Permission-Gated Operation

遵守現有 playbook 與 repository 規則。Permission denial 本身不先分類為 SOURCE / TOOLCHAIN / ENVIRONMENT / INFRASTRUCTURE / SERVICE failure。

若 runtime 支援 permission escalation：

- 要求完成目前必要 operation 所需的最小權限；
- 說明 exact command / operation；
- 說明為何本 Stage 必須執行；
- 若已知，說明被阻擋 resource/path；
- 說明最小 permission scope/type。

使用者批准後，只重試原本被阻擋的 operation；approval 不代表 scope expansion、下一 Stage、額外檔案修改或新的 Git mutation 授權。

`permission denial → request → approval → retry original operation` 不計 operational retry cap。

### 必須新增：Workspace Write Capability Gate

在任何**需要修改 repository** 的 Stage 開始 coding / file mutation 前，先確認目前 execution environment 對目標 working tree 具有完成該 Stage 所需的最小寫入能力。

#### Read-only work

例如：

- research
- code review
- architecture analysis
- evidence review
- read-only validation inspection

若工作本身不需要 mutation，read-only workspace 可以繼續。

#### Write-required work

例如：

- source patch
- tests 修改
- docs 修改
- `TASKS.md` bookkeeping
- commit preparation

若目前 workspace 明確為 read-only 或無法進行必要 file write：

- 標記為 `WORKSPACE WRITE CAPABILITY MISSING`；
- 若 runtime 提供可由使用者調整的 workspace-write / sandbox permission，主動要求最小必要 capability；
- 若必須由使用者在 Codex UI / execution setting 切換為 workspace-write，清楚回報所需設定；
- 在 capability 未取得前 STOP，不進入 coding/debug loop；
- 不得把此狀態分類為 SOURCE failure；
- 不得修改 production source 來「修」環境問題；
- 不得用 temporary copy、另一份 clone、另一 repository、改 Git metadata location、廣泛 chmod、sudo 或其他 workaround 繞過。

取得 workspace write capability 後，只恢復原本已授權 Stage；不授權額外 scope。

### 必須新增：Remote Git Permission Gate

對目前 Task / Stage 所必需且**本來已獲授權**的 remote Git operation，例如 `git fetch origin` 或已明確授權的 `git push`：

1. 若 runtime / sandbox policy 已明確知道該 operation 需要額外 sandbox、network、filesystem 或 repository-metadata permission，Codex 必須**在執行前主動要求最小必要權限**，不得故意先執行一個已知會被拒絕的 command 再把 denial 當 failure。
2. 若事前無法判定是否需要 escalation，可正常執行一次。
3. 第一次明確 `Permission denied` / `Access denied` / `EACCES` / `EPERM` / repository-metadata write denial → 立即視為 permission gate，主動要求最小權限。
4. Permission request 至少說明：
   - exact command / operation
   - 為何目前 Stage 必須執行
   - 被阻擋 resource/path（若已知）
   - 最小 permission scope/type
5. 使用者批准後只重試原 operation，不擴大 scope，不附帶執行其他 Git mutation。
6. Permission resolution 不計 operational retry。
7. 使用者拒絕、runtime 無 escalation 能力，或取得 permission 後相同 operation 仍真正失敗，才進入 operational failure taxonomy。

#### `git fetch origin` 特例

下列情況先走 Remote Git Permission Gate / Permission-Gated Operation：

- `.git/FETCH_HEAD` write denial
- Git ref / lock metadata write denial
- sandbox repository-metadata denial
- required network permission gate

批准後只重試原 `git fetch origin`。

#### `git push` 邊界

Sandbox/network permission approval **不等於 Git mutation authorization**。

只有當目前 Task / launch / repository policy 本來就已明確授權 push 時，permission escalation 才可用來解除該 push 的 execution/network gate。

不得把「使用者批准 network/sandbox permission」解讀成「新授權 Codex push」。

### 必須新增：ChatGPT / Codex Repository Write Boundary

將本 playbook 的預設 GitHub-backed collaboration mode 明確定義為以下固定分工：

#### ChatGPT

- 對 repository root `TASKS.md` 具有讀取、建立、更新與刪除權。
- 除 `TASKS.md` 外，**所有 repository path 對 ChatGPT 一律唯讀**，包括但不限於：
  - `AGENTS.md`
  - README / docs / architecture / spec / validation
  - source / headers / tests
  - scripts / tooling / workflow / CI
  - config / manifests / lock files
  - 其他任意 tracked 或 untracked project files
- ChatGPT 可以讀取這些檔案、分析 evidence、比較版本、提出修改方案、產生 Codex Prompt；但不得直接建立、更新、刪除或改名。
- 若判斷非 `TASKS.md` 檔案需要修改：
  1. 先讀最新 repository evidence；
  2. 確認是否真的需要 task，並避免建立等價重複項目；
  3. 必要時只在 root `TASKS.md` 建立或更新 scoped unfinished task / executable Codex Prompt；
  4. 由 Codex 執行真正的非 `TASKS.md` 修改。
- 使用者要求「幫我改 AGENTS / README / source」時，ChatGPT 不得因使用者意圖明確就直接越過此邊界；應將需求轉為 `TASKS.md` + Codex execution workflow，除非使用者之後明確改變這條治理規則本身。

#### Codex / coding agent

- Codex 在使用者當次明確授權的 Task / Stage scope 內，依 repository governance 修改 `TASKS.md` 以外的 allowed files。
- Codex 同時可以維護 `TASKS.md` 的執行狀態：更新 Blocked / Deferred / Pending-validation evidence、在成功完成並驗證後移除對應 item、queue 清空時刪除 `TASKS.md`。
- Codex 不得因具有 workspace write capability 就自行執行 queue 中其他未授權項目。

#### `TASKS.md` 共同維護語意

`TASKS.md` 是 **ChatGPT 與 Codex 共同維護**的唯一 active unfinished-work / executable scoped Prompt queue：

- ChatGPT 主要負責：分析、admission、scope、建立/調整 future work、避免 duplicate。
- Codex 主要負責：執行當次授權 Stage 後的 status/evidence bookkeeping、完成後移除 entry。
- 雙方都必須先讀最新 GitHub / synced local `TASKS.md` 再修改，避免覆蓋彼此的新內容。
- `TASKS.md` 不是 changelog；Completed 不保留，完成紀錄以 Git history 為準。
- `TASKS.md` 本身不授權 Codex 自動開始任何 Stage，也不擴張 ChatGPT 對其他 path 的寫入權。

### 預期啟動順序

將共通流程收斂為：

`Repository Identity Gate → Workspace Write Capability Gate → Git state / unfinished-operation preflight → Remote Git Permission Gate → git fetch origin → FF-only sync → re-read AGENTS/TASKS → execute Stage → Targeted Validation`

Read-only Stage 可在 Workspace Write Capability Gate 判定不需要寫入後直接繼續。

### Allowed files

Codex 本 Stage 依最小必要修改原則，優先只修改：

- `AGENTS.md`（本次 **ChatGPT / Codex Repository Write Boundary** 應成為 stable playbook governance，必要時以短且 authoritative 的形式落地）
- `REPOSITORY_EXECUTION.md`
- `CHAT_INIT.md`
- `CODEX_PROMPT_RULES.md`（僅需短引用 / Prompt generation requirement 時）
- `README.md`（僅 routing / concise core-summary 真有必要時）
- `TASKS.md`（共同 queue；完成後移除此 Stage，若無其他 unfinished work則刪除）

避免在多檔全文複製同一 policy；stable authority + short references/routing 為主。

### Forbidden scope

- 不新增與本 Stage 無關的 governance。
- 不改模型命名體系。
- 不改 MIT License。
- 不建立 scripts / CI / tooling。
- 不改任何其他 project repository。
- 不把 Windows local baseline 擴張成所有 CI 必須 Windows。
- 不把 ChatGPT direct-write boundary 放寬到 `TASKS.md` 以外任何 path。
- 不把 Codex 的 workspace-write capability解讀成自動授權 queue 中其他 task。
- 不使用 sudo、`chmod -R 777`、reset-hard、force push、auto-stash、autonomous merge/rebase/cherry-pick、delete/discard unknown work。

### Progressive reading

先讀：

1. `AGENTS.md`
2. `TASKS.md`
3. `REPOSITORY_EXECUTION.md`
4. `CHAT_INIT.md`
5. `CODEX_PROMPT_RULES.md`
6. 必要時 `README.md`

不要 repo-wide scan。

可把下列既有專案 governance 當語意參考，但只在需要確認 wording 時讀最少必要區段，不要複製專案專屬內容：

- `masini1491/access-control-system` `AGENTS.md` — Permission-Gated Operation / `git fetch origin` 特例
- `masini1491/esp32-wfrac-local-bridge` `AGENTS.md` — permission escalation / remote sync
- `masini1491/esp32-vag-data-server` `AGENTS.md` — permission request 必須包含 command、必要性、resource/path、最小 scope

### Validation

最小且充分：

1. 檢查 README / AGENTS / CHAT_INIT / REPOSITORY_EXECUTION / CODEX_PROMPT_RULES 之間沒有 contradiction。
2. 確認 Workspace Write Capability Gate 與 Permission-Gated Operation 不被混成同一概念。
3. 確認 Remote Git Permission Gate 同時涵蓋：
   - known-in-advance permission need → proactive request
   - unknown → first denial → request
   - approval → retry original operation only
   - permission resolution not counted as retry
   - push permission ≠ push authorization
4. 確認 `git fetch origin` `.git/FETCH_HEAD` / ref / lock / metadata denial 特例存在。
5. 確認 ChatGPT 對 repository 的 direct-write authority 僅限 root `TASKS.md`；其他 path 明確唯讀。
6. 確認非 `TASKS.md` 修改必須透過 scoped task / Codex workflow 執行。
7. 確認 `TASKS.md` 被明確定義為 ChatGPT + Codex 共同維護的唯一 active unfinished-work queue，且 Completed 仍由 Git history 保存。
8. 確認不鼓勵 dangerous workaround。
9. `git diff --check`。
10. 純 Markdown governance maintenance，不跑不相關 build/test。

### Completion

成功完成與驗證後：

- 移除本 Stage；
- 若 `TASKS.md` 已無其他 unfinished item，刪除 `TASKS.md`；
- 使用 focused commit；
- 只有在目前 launch / repository policy 已明確授權時才 normal push；不得 force push；
- 以繁體中文回報變更摘要、validation evidence、commit SHA 與是否已 push。
