# 實戰手冊維護規則（Playbook Maintenance Rules）

本 repository 是公開、可分享的跨專案 AI-assisted development 方法論。維護時優先保持通用、精簡、可路由、可驗證，並控制 AI retrieval / Context 成本。

## 維護責任（Maintenance ownership）

本 repository 是**共通規則來源**，不是一般 product / firmware implementation repository。

固定維護邊界：

- **ChatGPT 是本 repository 的主要 AI maintainer**，可直接讀取、建立、更新、刪除本手冊內的規則與文件。
- ChatGPT 對本 repository 的 direct-write 也包含本手冊自身的最小 deterministic tooling 與其 tests；目前只限 `/tools/playbook_check.py` 與 `/tests/test_playbook_check.py`。這是 Playbook maintainer 例外，不授權一般 project 的 ChatGPT 修改 source/tooling，也不授權 Codex 寫入本 repository。
- **本 repository 的 AI 程式執行權只屬於 ChatGPT**：只有 ChatGPT 可執行本 repository 內的 validator、tests 或其他程式／script。Codex、其他 coding agent 或自動化 agent 即使具備技術執行能力，也只能讀取，不得執行；GitHub Actions、pre-commit 或其他自動執行機制也不應代跑，除非使用者日後明確改變本規則。
- **Codex / coding agent 對本 repository 預設唯讀**：可讀取並遵守本手冊，但不得以一般 project coordination → Codex implementation workflow 修改本 repository，也不得執行本 repository 內的程式／tests。
- 本 repository 的 `TASKS.md` 若存在，只作為 ChatGPT 維護本手冊時的暫時 unfinished-work queue；不代表要交由 Codex 執行。
- 對一般目標 project repository，ChatGPT direct-write path 依 `REPOSITORY_EXECUTION.md` 的 **Coordination Write Allowlist**：default 只有 root `TASKS.md`；project 可明確 opt-in `BACKLOG.md`、Hot task dossier或 sanitized evidence staging。其他 path 仍 read-only，由 Codex 在明確授權 scope 內修改。
- 不得把一般 project 的 ChatGPT coordination write boundary反向套用到本手冊自身。

若使用者日後明確變更本 repository 的維護 ownership，再依最新指示調整。

### 本 repository 的 minimal validator contract

本手冊自身的 deterministic Markdown/routing check 使用 `/tools/playbook_check.py`，tests 使用 `/tests/test_playbook_check.py`。

- Runtime：Python 3.11+。
- Dependency：Python standard library only；不要為第一版 validator 建立 package manager、requirements 或額外 config framework。
- 正式檢查：由 ChatGPT 執行 `python tools/playbook_check.py`。
- Unit tests：由 ChatGPT 執行 `python -m unittest tests/test_playbook_check.py`。
- 上述 command 是 ChatGPT 的 execution contract，不構成 Codex、其他 agent、CI 或自動化工具的執行授權。
- Validator v1 只處理可客觀判定的結構／routing invariant；不得加入需要 AI judgment 的 duplicate-policy、section-length、architecture score 或類似 heuristic。
- 若未來真的讓 Codex 維護或執行本 repository tooling，必須另由使用者明確授權；本段不建立 Codex write / execution exception。

## 適用範圍（Scope）

只保存「怎麼開發」的共通方法，不保存任何特定專案的：
- secrets / credentials
- 客戶或個人資料
- 私有 endpoint / key
- 真實部署位址
- 專案專屬 GPIO / wiring
- 未公開 protocol secrets
- 只對單一產品成立的 current state

若某條規則只適用單一 repository，應留在該 repository 的 governance / architecture / coordination surface，而不是搬進本手冊。

## 文件責任與讀取紀律（Document ownership / reading discipline）

`README.md` 是 **human-facing overview + repository router**：保存手冊定位、核心原則、文件路由與必要高層摘要；詳細 normative contract 由對應主題文件作為唯一主要 authority。

`CHAT_INIT.md` 是**新聊天室最小 bootstrap + task router**：AI 可直接從它進入，不必先讀 README；它只負責建立 repository / authority / minimal routing 起點，不複製完整 Git、coordination、Prompt、toolchain 或 validation policy。

`AI_CONTEXT.md` 是 **跨專案 AI-readable repository information architecture authority**：負責 Always-on / Hot / Cold / Evidence / Current / Historical surface semantics、Progressive Routing、Independent Retrieval Intent、Thin Metadata、Derived Metadata Write-Closure 與 Readability / Retrieval Cost Change Gate；不得在其他文件複製完整 context policy。

`CHATGPT_WORKFLOW.md` 是 **ChatGPT／planning conversation authority**：負責 coordination admission、AI-originated durable work、Task identity/revision、Codex Prompt mode / delivery、copy-ready contract、Codex result reconciliation、ChatGPT 回覆 presentation contract 與時間戳；不得收進 Codex execution / cost policy全文。

`CODEX_EXECUTION.md` 是 **Codex／coding agent execution authority**：負責 model / reasoning / Context / Agent、execution mode、cost / usage budgeting、tool scheduling/output、escalation 與 Codex reporting。

`REPOSITORY_EXECUTION.md`、`DEBUG_VALIDATION.md`、`RESEARCH_ARCHITECTURE.md` 等 shared topic 文件只保存真正跨 agent 共用的 repository、permission/write boundary、evidence、validation、architecture contract。

讀者與 coding agent 不應預設完整掃描全部文件；先從 `CHAT_INIT.md` 進入，再依 task topic讀最低必要主題／section。Exact target 已明確時可 direct-leaf bypass，不為 routing ceremony 多讀中間層。

## 權威順序（Authority）

本手冊不覆蓋實際專案的正式 technical source of truth。

一般 authority：
1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance/technical truth
3. 本手冊
4. 實際專案 current Hot coordination contract
5. 舊 Prompt / 舊聊天 / cached copy / memory

Cold/Candidate item、historical material或 AI 先前建議不因被持久化而升高 authority。

## 變更紀律（Change discipline）

新增規則前先確認：
- 是否真的跨專案重複出現
- 是否可由既有章節吸收
- 是否會和現有規則重複/衝突
- 是否有明確失敗案例或工程收益
- 是否形成獨立 retrieval intent；若沒有，優先更新既有 canonical owner
- 是否會提高 always-on/default-load Context、routing depth、search noise、duplication/reconciliation 或 derived write closure 成本

任何新增、刪除、搬移、拆分、合併 rule / file / router / information surface，都必須通過 `AI_CONTEXT.md` 的 **AI Readability / Retrieval Cost Change Gate**。少字、拆檔或新增 index 本身都不代表 AI 更快。

優先修改既有主題文件，不要為每個新細節建立新檔。但若跨專案 evidence 顯示已形成穩定、可獨立 retrieval、具有清楚 ownership 的新 information architecture domain，可建立新 canonical owner；建立後其他文件只做 routing。

若不同 agent / lifecycle 已形成清楚且持續的 ownership boundary，例如 ChatGPT planning 與 Codex execution，應依 owner 分離 canonical policy；**不要因舊檔名或舊 routing 存在就永久保留 ownership mixing**。

若規則已存在 canonical topic owner，README、CHAT_INIT、其他文件只保留最低必要 routing；不要因方便閱讀再複製完整 normative policy。

## 禁止重複規則（No duplicated policy）

穩定規則只保留一個主要 authority；其他文件以簡短引用/routing 為主，避免同一 policy 在多檔全文複製造成 drift。

Routing metadata 優先只保存穩定 ID/path/owner/entrypoint；除非本身是 canonical owner，不複製 volatile current status、validation result、architecture conclusion 或 evidence。

## 公開安全與可分享性（Public-safety / shareability）

所有新增內容在 commit 前檢查：
- 不含 secrets
- 不含私人身份/生活資料
- 不含 private repository 內容
- 不含未授權第三方程式碼的大段複製
- 外部 reference 若有必要，尊重 license/provenance

任何 evidence-like內容在**第一次 Git write 前**就必須 sanitized；不得先 commit敏感內容再靠後續刪除處理。

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
- stale filename / superseded wording 是否仍污染 active routing
- AI default-load / always-on / bounded-read / routing depth 是否惡化
- 是否因新增 surface 產生不必要的 tracked derived-metadata write closure
- 若在 local workspace 執行，使用 `git diff --check`

涉及 policy ownership 搬移時，額外確認：
- canonical rule 沒有遺失；
- 舊位置已改成 routing/reference 或必要 domain-specific delta；
- `CHAT_INIT` / README routing 指向新的主要 authority；
- 沒有同一完整 normative policy 同時留在多個檔案。

不要為純文件 wording 修改跑不相關 build/test。

## 版本演進理念（Versioning philosophy）

Git history 是本手冊演進紀錄。不要在文件內維護冗長 completed changelog；重大 policy 變動可透過清楚 commit message 追溯。