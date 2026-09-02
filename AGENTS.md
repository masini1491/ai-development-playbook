# 實戰手冊維護規則（Playbook Maintenance Rules）

本 repository 是公開、可分享的跨專案 AI-assisted development 方法論。維護時優先保持通用、精簡、可路由、可驗證。

## 維護責任（Maintenance ownership）

本 repository 是**共通規則來源**，不是一般 product / firmware implementation repository。

固定維護邊界：

- **ChatGPT 是本 repository 的主要 AI maintainer**，可直接讀取、建立、更新、刪除本手冊內的規則與文件。
- **Codex / coding agent 對本 repository 預設唯讀**：可讀取並遵守本手冊，但不得以一般 project `TASKS.md → Codex implementation` workflow 修改本 repository。
- 本 repository 的 `TASKS.md` 若存在，只作為 ChatGPT 維護本手冊時的暫時 unfinished-work queue；不代表要交由 Codex 執行。
- 對一般目標 project repository，仍適用本手冊定義的 ChatGPT / Codex 分工：ChatGPT 只直接寫 root `TASKS.md`，其他 path 唯讀；非 `TASKS.md` 修改由 Codex 在明確授權 scope 內執行。
- 不得把「一般 project 的 ChatGPT only-`TASKS.md` write boundary」反向套用到本手冊自身。

若使用者日後明確變更本 repository 的維護 ownership，再依最新指示調整。

## 適用範圍（Scope）

只保存「怎麼開發」的共通方法，不保存任何特定專案的：
- secrets / credentials
- 客戶或個人資料
- 私有 endpoint / key
- 真實部署位址
- 專案專屬 GPIO / wiring
- 未公開 protocol secrets
- 只對單一產品成立的 current state

若某條規則只適用單一 repository，應留在該 repository 的 `AGENTS.md` / architecture / TASKS，而不是搬進本手冊。

## 文件責任與讀取紀律（Document ownership / reading discipline）

`README.md` 是 **overview + router**：保存手冊定位、核心原則、文件路由與必要的高層摘要；詳細 normative contract 應由對應主題文件作為唯一主要 authority。

`CHAT_INIT.md` 是**新聊天室最小 bootstrap**：只負責告訴新 session 如何確認目標 repository、依 README routing 讀最低必要主題文件，以及先取得哪些 project-local authority；不得再複製完整 Git、TASKS、Prompt、toolchain 或 validation policy。

`CHATGPT_WORKFLOW.md` 是 **ChatGPT／planning conversation authority**：負責 TASKS admission routing、Codex Prompt mode / delivery、copy-ready contract、Codex result reconciliation、ChatGPT 工程回覆 presentation contract 與回覆時間戳；不得再把 Codex execution / cost policy 全文收進來。

`CODEX_EXECUTION.md` 是 **Codex／coding agent execution authority**：負責 model / reasoning / Context / Agent、execution mode、cost / usage budgeting、tool scheduling/output、escalation 與 Codex reporting；不得再維護 ChatGPT Prompt-generation workflow。

`REPOSITORY_EXECUTION.md`、`DEBUG_VALIDATION.md`、`RESEARCH_ARCHITECTURE.md` 等 shared topic 文件只保存真正跨 ChatGPT / Codex 共用的 repository、evidence、validation、architecture contract。

讀者與 coding agent 不應預設完整掃描全部文件；先從 README / CHAT_INIT 進入，再依 task topic 讀最少必要主題文件。

## 權威順序（Authority）

本手冊不覆蓋實際專案的正式 technical source of truth。

一般 authority：
1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance/technical truth
3. 本手冊
4. 實際專案 TASKS queue
5. 舊 Prompt / 舊聊天 / cached copy / memory

## 變更紀律（Change discipline）

新增規則前先確認：
- 是否真的跨專案重複出現
- 是否可由既有章節吸收
- 是否會和現有規則重複/衝突
- 是否有明確失敗案例或工程收益

優先修改既有主題文件，不要為每個新細節建立新檔。

但若不同 agent / lifecycle 已形成清楚且持續的 ownership boundary，例如 ChatGPT conversation planning 與 Codex execution，應依 owner 分離 canonical policy；**不要因舊檔名或舊 routing 存在就永久保留 ownership mixing**。下游專案可在讀取最新版手冊時做 governance reconciliation。

若規則已存在 canonical topic owner，README、CHAT_INIT、其他主題文件只保留最低必要摘要／routing；不要因方便閱讀再複製一份完整 normative policy。

## 禁止重複規則（No duplicated policy）

穩定規則只保留一個主要 authority；其他文件以簡短引用/routing 為主，避免同一 policy 在多檔全文複製造成 drift。

## 公開安全與可分享性（Public-safety / shareability）

所有新增內容在 commit 前檢查：
- 不含 secrets
- 不含私人身份/生活資料
- 不含 private repository 內容
- 不含未授權第三方程式碼的大段複製
- 外部 reference 若有必要，尊重 license/provenance

## 語言（Language）

文件以繁體中文為主；API、protocol、model、Git、toolchain、正式英文名稱與必要 cross-reference 等技術名詞可保留英文。

中文正文優先使用「手冊／實戰手冊」，不要在不需要正式英文辨識的地方混用 `Playbook`。

## Git 安全（Git safety）

預設 main 是 source of truth。修改前確認 repository identity、branch、HEAD 與 working state；禁止 force push、reset-hard、rewrite history 或丟棄未知 user work。

若遇 permission denial，遵守 `REPOSITORY_EXECUTION.md` 的 Permission-Gated Operation。

## 驗證（Validation）

純 Markdown policy 修改至少檢查：
- links / routing 是否一致
- 同名規則是否產生 contradiction
- fenced code / headings 是否完整
- 若在 local workspace 執行，使用 `git diff --check`

涉及 policy ownership 搬移時，額外確認：
- canonical rule 沒有遺失；
- 舊位置已改成 routing/reference 或必要 domain-specific delta；
- README / CHAT_INIT routing 指向新的主要 authority；
- 沒有同一完整 normative policy 同時留在多個檔案。

不要為純文件 wording 修改跑不相關 build/test。

## 版本演進理念（Versioning philosophy）

Git history 是本手冊演進紀錄。不要在文件內維護冗長 completed changelog；重大 policy 變動可透過清楚 commit message 追溯。