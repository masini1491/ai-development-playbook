# Playbook Maintenance Rules

本 repository 是公開、可分享的跨專案 AI-assisted development 方法論。維護時優先保持通用、精簡、可路由、可驗證。

## Maintenance ownership

本 repository 是**共通規則來源**，不是一般 product / firmware implementation repository。

固定維護邊界：

- **ChatGPT 是本 repository 的主要 AI maintainer**，可直接讀取、建立、更新、刪除本 playbook 內的規則與文件。
- **Codex / coding agent 對本 repository 預設唯讀**：可讀取並遵守本 playbook，但不得以一般 project `TASKS.md → Codex implementation` workflow 修改本 repository。
- 本 repository 的 `TASKS.md` 若存在，只作為 ChatGPT 維護 playbook 時的暫時 unfinished-work queue；不代表要交由 Codex 執行。
- 對一般目標 project repository，仍適用本 playbook 定義的 ChatGPT / Codex 分工：ChatGPT 只直接寫 root `TASKS.md`，其他 path 唯讀；非 `TASKS.md` 修改由 Codex 在明確授權 scope 內執行。
- 不得把「一般 project 的 ChatGPT only-`TASKS.md` write boundary」反向套用到本 playbook 自身。

若使用者日後明確變更本 repository 的維護 ownership，再依最新指示調整。

## Scope

只保存「怎麼開發」的共通方法，不保存任何特定專案的：
- secrets / credentials
- 客戶或個人資料
- 私有 endpoint / key
- 真實部署位址
- 專案專屬 GPIO / wiring
- 未公開 protocol secrets
- 只對單一產品成立的 current state

若某條規則只適用單一 repository，應留在該 repository 的 `AGENTS.md` / architecture / TASKS，而不是搬進本 playbook。

## Reading discipline

`README.md` 是 router。讀者與 coding agent 不應預設完整掃描全部文件；先讀 README / CHAT_INIT，再依 task topic 讀最少必要文件。

## Authority

本 playbook 不覆蓋實際專案的正式 technical source of truth。

一般 authority：
1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance/technical truth
3. 本 playbook
4. 實際專案 TASKS queue
5. 舊 Prompt / 舊聊天 / cached copy / memory

## Change discipline

新增規則前先確認：
- 是否真的跨專案重複出現
- 是否可由既有章節吸收
- 是否會和現有規則重複/衝突
- 是否有明確失敗案例或工程收益

優先修改既有主題文件，不要為每個新細節建立新檔。

## No duplicated policy

穩定規則只保留一個主要 authority；其他文件以簡短引用/routing 為主，避免同一 policy 在多檔全文複製造成 drift。

## Public-safety / shareability

所有新增內容在 commit 前檢查：
- 不含 secrets
- 不含私人身份/生活資料
- 不含 private repository 內容
- 不含未授權第三方程式碼的大段複製
- 外部 reference 若有必要，尊重 license/provenance

## Language

文件以繁體中文為主；API、protocol、model、Git、toolchain 等技術名詞可保留英文。

## Git safety

預設 main 是 source of truth。修改前確認 repository identity、branch、HEAD 與 working state；禁止 force push、reset-hard、rewrite history 或丟棄未知 user work。

若遇 permission denial，遵守 `REPOSITORY_EXECUTION.md` 的 Permission-Gated Operation。

## Validation

純 Markdown policy 修改至少檢查：
- links / routing 是否一致
- 同名規則是否產生 contradiction
- fenced code / headings 是否完整
- 若在 local workspace 執行，使用 `git diff --check`

不要為純文件 wording 修改跑不相關 build/test。

## Versioning philosophy

Git history 是 playbook 演進紀錄。不要在文件內維護冗長 completed changelog；重大 policy 變動可透過清楚 commit message 追溯。
