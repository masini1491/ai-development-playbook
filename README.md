# AI Development Playbook｜AI 協作開發實戰手冊

> **Give AI enough structure to work reliably without turning engineering into bureaucracy.**
>
> **讓 AI 有足夠結構可以可靠工作，但不要把工程變成流程儀式。**

## What this is / 這是什麼

**English**

AI Development Playbook is a reusable **GitHub-native governance and information-integrity layer** for ChatGPT, Codex, and other AI engineering workflows.

It treats GitHub as durable project memory and the source of truth, while each repository declares which authorized actor may plan, implement, validate, and maintain its artifacts. ChatGPT, Codex / coding agents, human maintainers, or other executors can all participate when current project governance gives them that responsibility. The goal is not to add more prompts or process overhead. The goal is to keep **context, authority, evidence, execution, validation, and cost** distinguishable as a project evolves across sessions and agents.

You do **not** need to load the entire repository into context or read it end to end. A project declares the Playbook as a common baseline, an AI session starts from [`CHAT_INIT.md`](CHAT_INIT.md), and then reads only the minimum canonical sections required by the current task.

**繁體中文**

AI Development Playbook 是一套可重用、**以 GitHub 為原生基礎的 AI 工程治理與資訊完整性層**，適用於 ChatGPT、Codex 與其他 AI 工程工作流程。

它把 GitHub 當成持久化專案記憶與單一事實來源，而每個 repository 由自己的 governance 宣告：哪些已授權角色可以規劃、實作、驗證與維護對應 artifact。ChatGPT、Codex／程式代理（coding agents）、human maintainer 或其他執行者，都只有在目前專案權威明確授權相應責任時才參與。目標不是增加更多提示詞或流程，而是讓專案跨聊天室、跨代理長期演進時，**上下文、權威、證據、執行、驗證與成本**仍然彼此可分辨。

你**不需要**完整載入或從頭讀完整個儲存庫。實際專案只要宣告 Playbook 為共通基準版本，AI 工作階段從 [`CHAT_INIT.md`](CHAT_INIT.md) 進入，再依目前任務只讀最低必要的權威章節。

> **Human-facing language / 人類閱讀語言**：This README follows the canonical bilingual human-surface contract in [`AGENTS.md`](AGENTS.md): English first with a high-quality Traditional Chinese counterpart at section level. `AGENTS.md` owns the normative layout / parity / split criteria; this README only follows that contract.／本 README 依 [`AGENTS.md`](AGENTS.md) 的權威雙語人類閱讀介面契約呈現：主要主題先以英文說明，再緊接高品質繁體中文對應內容。排版、語意一致性與拆分條件的規範權威在 `AGENTS.md`；README 本身只遵循，不自行治理。

> **Dogfooding note / 自我實作說明**：This repository is primarily maintained by ChatGPT under the explicit maintainer contract in [`AGENTS.md`](AGENTS.md). This is a governed maintainer workflow, **not** a claim of fully autonomous repository maintenance.／本儲存庫主要由 ChatGPT 依 [`AGENTS.md`](AGENTS.md) 的明確維護者契約進行維護；這是一套受治理的維護流程，**不是**「完全自主維護儲存庫」的宣稱。

## 5-minute quick start / 5 分鐘開始使用

**English**

If you already have a GitHub project:

1. Add a small Playbook declaration to the project-root `AGENTS.md`.
2. Choose one active Playbook baseline, such as `main` or a pinned release tag.
3. Start each new ChatGPT / AI / coding-agent session from that baseline's [`CHAT_INIT.md`](CHAT_INIT.md).
4. Let the AI route only to the canonical sections needed for the current task, while keeping the project's own governance and technical truth higher authority.

Minimal bootstrap:

```markdown
## Common AI Development Playbook

This project uses `masini1491/ai-development-playbook` as a common AI engineering baseline.
Playbook baseline: `main`

A new AI / agent session must first read the selected Playbook baseline's `CHAT_INIT.md`,
then load only the minimum canonical sections required by the current task.

This project's own `AGENTS.md`, technical source of truth, and project-specific governance
remain higher authority. Do not load the whole Playbook into Context by default.
```

Shortest path:

`Project AGENTS.md → Playbook baseline → CHAT_INIT.md → project governance/current truth → minimum-sufficient canonical owner`

Use `Playbook baseline: main` when you intentionally want current rules. Use a released tag when reproducibility matters.

The snippet above is the smallest bootstrap, not the full deterministic adoption contract. For a ready-to-adapt example that can be checked by Adoption Doctor, use [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md).

**繁體中文**

如果你已經有 GitHub 專案：

1. 在專案根目錄的 `AGENTS.md` 放入一小段 Playbook 導入宣告。
2. 只選一個目前有效的 Playbook 基準版本，例如 `main` 或固定的發行標籤（release tag）。
3. 新的 ChatGPT／AI／程式代理工作階段先讀該基準版本的 [`CHAT_INIT.md`](CHAT_INIT.md)。
4. 讓 AI 依目前任務只載入最低必要的權威章節，同時維持專案自己的治理規則與技術事實來源為較高權威。

上面的英文啟動宣告可以直接使用；AI 不需要為同一份專案導入宣告同時維護兩種語言版本。

最短路徑：

`專案 AGENTS.md → Playbook 基準版本 → CHAT_INIT.md → 專案治理／目前權威事實 → 最低充分權威主責文件`

想持續取得最新規則時使用 `Playbook baseline: main`；需要可重現時改用已發布的標籤。

上面只是最小啟動宣告，不是完整的確定性導入契約。若要使用可由 Adoption Doctor 檢查、可直接調整的範例，請從 [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) 開始。

## One-message ChatGPT bootstrap / 一句話讓 ChatGPT 開始使用

**English**

If you want to try the Playbook in ChatGPT without changing persistent settings first, start a fresh chat and send:

```text
Use the GitHub Connector to read the latest `main` of `masini1491/ai-development-playbook`.

Follow the repository's `AGENTS.md`, `CHAT_INIT.md`, and routing rules to initialize. Read only the minimum-sufficient canonical owners required for the current task; do not scan the whole repository or substitute stale memory for current GitHub state.

After initialization, use this Playbook to assist with my engineering work.
```

If the GitHub Connector is unavailable, ChatGPT should say so explicitly rather than silently relying on model memory or incomplete repository content.

For repeated use, see the persistent ChatGPT Custom Instructions setup below.

**繁體中文**

如果只是想先在 ChatGPT 快速試用 Playbook，不需要先修改永久設定。開一個新的 ChatGPT 聊天室並貼上：

```text
請透過 GitHub Connector 讀取 `masini1491/ai-development-playbook` 最新 `main`。

先依 repo 的 `AGENTS.md`、`CHAT_INIT.md` 與 routing 規則初始化，只讀本次任務最低充分的 canonical owners，不要完整掃描 repository，也不要以舊記憶代替 current GitHub state。

初始化完成後，請依這套 Playbook 協助我接下來的工程工作。
```

如果 GitHub Connector 無法使用，ChatGPT 應明確回報，而不是默默改用模型記憶或不完整的儲存庫內容繼續。

如果準備長期使用，再依下方的 ChatGPT Custom Instructions 設定進行持久化安裝。

## ChatGPT Custom Instructions setup and recovery / ChatGPT 自訂指令設定與復原

**English**

ChatGPT Custom Instructions are a **persistent user-level host setting**, not project governance and not proof that every project adopts this Playbook. For the current manually installed thin-activation setup:

1. Open ChatGPT Settings → Personalization → Custom Instructions (wording may vary by product version).
2. Open [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt), select all, and replace the Custom Instructions field with the complete file. Do not merge partial revisions.
3. Start a **fresh ChatGPT chat** for validation; do not use an already-contextualized conversation as proof that the new host instruction is active.
4. For repository/project work, the host instruction must still read current project governance first. The project itself decides whether it adopts this Playbook and which baseline it declares; adoption alone must not default to current Playbook `main`.

The copy-ready artifact is intentionally kept within **5,000 characters**, matching the field limit observed during this adapter's manual validation. Treat that number as a product-version-specific installation constraint, not a Playbook policy rule.

If fresh chats materially skip repository identity/governance, assume an undeclared Playbook baseline, broaden a generic continuation into new work, or treat capability as authority, use the bounded **ChatGPT Host Instruction Health Check** in [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md). If the setting is missing, stale, or mixed, replace the whole field with the current [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt), then rerun a minimal fresh-chat regression.

**繁體中文**

ChatGPT 自訂指令屬於**使用者層級的持久 host setting**，不是專案 governance，也不代表所有專案會因為這個設定就自動採用本 Playbook。以目前需要手動安裝的薄型啟動方式：

1. 開啟 ChatGPT 的 Settings／Personalization／Custom Instructions（不同產品版本介面文字可能略有差異）。
2. 開啟 [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt)，全選整份內容並完整取代 Custom Instructions 欄位；不要把不同版本以增量方式混在一起。
3. 用**全新 ChatGPT 聊天室**驗證；不要拿已累積舊 context 的既有聊天室當成新 host instruction 已生效的證據。
4. 進入 repository／project 工作後，host instruction 仍必須先讀 current project governance。是否採用 Playbook、採用哪個 baseline 都由專案自己宣告；不能只因「採用 Playbook」就預設使用 Playbook current `main`。

這份 copy-ready artifact 目前刻意維持在 **5,000 字元以內**，對應本 adapter 目前人工驗證時觀察到的 ChatGPT 欄位限制。這個數字是產品版本相關的安裝限制，不是 Playbook policy。

若 fresh chat 出現未確認 repository identity／governance、擅自假設 undeclared Playbook baseline、把「好，繼續」之類 continuation 擴張成新工作，或把 capability 誤當 authority，可依 [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md) 的 **ChatGPT Host Instruction Health Check** 做有界診斷。若設定缺失、過期或混合多版，請用目前完整的 [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) 整段覆蓋，再跑最小 fresh-chat regression。

## Codex Desktop setup and recovery / Codex Desktop 設定與復原

**English**

Codex personal instructions are a **persistent user/app-level setting**, not a repository file or an ordinary one-chat prompt. For the current manually installed thin-activation setup:

1. Open Codex Settings → Personalization → Codex Instructions (wording may vary by product version).
2. Open [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt), select all, and copy the complete file into Codex Instructions.
3. Replace the entire field; do not merge partial revisions.
4. Open the intended project repository/workspace, then start a fresh Codex chat.
5. If a required read-only bootstrap probe is blocked by sandbox or network permissions, Codex may ask for the minimum permission required for that exact operation; approval does not grant broader mutation authority.

This setup currently requires a one-time manual installation. A normal ChatGPT/Codex prompt does not by itself establish that the persistent Codex Instructions field has been changed, and ChatGPT must not claim it can inspect or modify that setting unless the product exposes an actual settings capability.

If Codex later reports behavior that materially conflicts with the expected activation flow, ChatGPT should first reconcile the current project state with canonical evidence, then use the bounded **Codex Host Instruction Health Check** in [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md). Typical signals include wrong repository/workspace identity, missing Playbook adoption despite a current project declaration, skipped floating-ref exact revision resolution, failure to request available minimum read permission, unexpected broad bootstrap reading, or treating host instructions/capabilities as mutation authority. A timestamp-only error or ordinary source/test failure is not enough by itself.

If the health check finds missing, stale, or mixed instructions, replace the whole Codex Instructions field with the current complete [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt), then verify with a minimal fresh-chat regression.

**繁體中文**

Codex 個人化指示屬於**使用者／App 層級的持久設定**，不是儲存庫檔案，也不是只對單一聊天室生效的普通提示。以目前需要手動安裝的薄型啟動方式：

1. 開啟 Codex 的 Settings／Personalization → Codex Instructions（不同產品版本的介面文字可能略有差異）。
2. 開啟 [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt)，全選整份內容，並複製到 Codex Instructions。
3. 將整個設定欄位完整取代，不要把不同版本以增量方式混在一起。
4. 開啟正確的專案儲存庫／工作區，再建立全新的 Codex 聊天。
5. 若啟動階段必要的唯讀查詢被 sandbox／network 權限限制擋住，Codex 可能會要求執行該操作所需的最低權限；核准只解除這個操作的能力限制，不代表取得更廣的修改權限。

目前這個設定仍需要使用者手動安裝一次。一般 ChatGPT／Codex 提示本身不能證明 Codex 個人化指示已被永久寫入；除非產品真的提供設定讀寫能力，ChatGPT 也不得宣稱自己能直接查看或修改該設定。

若日後 Codex 的回報與預期啟動行為有實質不一致，ChatGPT 應先核對專案目前狀態與權威證據，再依 [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md) 的 **Codex 個人化指示健康檢查（Host Instruction Health Check）** 做有界診斷。典型訊號包括：儲存庫／工作區身分錯誤、專案已宣告採用 Playbook 但 Codex 說未採用、浮動基準未解析成確切不可變版本、明明可以要求最低唯讀權限卻直接宣告 unavailable、啟動時出現不必要的大範圍讀取，或把個人化指示／工具能力誤當成修改權限。單純時間戳錯誤或一般原始碼／測試失敗，不足以單獨觸發這個診斷。

若健康檢查確認設定缺失、過期或混合多版，請用目前完整的 [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) 整段覆蓋 Codex Instructions，再用最小的全新聊天室迴歸測試驗證。

## Quick workflow / 快速流程

**English**

Start by finding existing references and current project authority. Resolve the responsibility and mutation surface, then choose the **lowest-sufficient authorized actor** from the repository's current actor topology. ChatGPT may execute work directly when it has both authority and capability; Codex / coding agents, human maintainers, or other actors may be selected when the project assigns them that responsibility. After execution or handoff, read back the current canonical state and reconcile the evidence before deciding whether the work is done or another Stage is needed.

**繁體中文**

先找現有參考與目前專案權威，再確認這一步真正需要的責任與修改範圍，接著依 repository 的 current actor topology 選擇**最低充分且已獲授權的執行角色**。ChatGPT 在同時具備authority與capability時可以直接執行；若專案把責任交給 Codex／其他程式代理、human maintainer 或其他角色，就依該治理交接。執行或交接完成後，再回讀目前 canonical state、核對證據，最後判斷是否完成或需要下一個 Stage。

![AI Development Playbook quick workflow](assets/readme-workflow.svg)

> **Illustrative workflow / 流程概覽**：The diagram is a human-facing summary, not a second normative authority. Canonical rules remain in the linked Playbook owner documents.／本圖是人類閱讀用的流程摘要，不是第二份規範權威；正式規則仍以 Playbook 對應的權威主責文件為準。

## Why this exists / 為什麼需要它

**English**

AI-assisted development often fails in ways that are not really coding failures:

- a useful idea silently becomes unauthorized work;
- a test passes and gets reported as if the real system is done;
- an old chat or cached summary overrides the current repository truth;
- an agent can technically call a tool, so capability is mistaken for authority;
- every task loads too much repository history, increasing cost and stale-context risk;
- multiple agents or workflows each carry a different idea of what is current.

The Playbook gives these failure modes explicit boundaries and routing instead of trying to solve them with a larger prompt.

**繁體中文**

AI 輔助開發很多失敗其實不是「程式寫不好」：

- AI 覺得某個改善很有價值，就默默把它變成未授權工作；
- 測試 PASS 被直接講成真實系統已完成；
- 舊聊天室或快取摘要覆蓋儲存庫目前的權威事實；
- 代理技術上能呼叫工具，就把技術能力誤當成權限；
- 每個任務都載入過多儲存庫歷史，增加成本與過時上下文風險；
- 不同代理／工作流程各自保留不同版本的「目前狀態」。

Playbook 的做法不是塞入更大的提示詞，而是把這些失敗模式變成清楚的權威、路由、證據與生命週期邊界。

## Before / After showcase / 前後對照案例

> **Illustrative, non-normative evidence layer / 說明性、非規範性證據層**：These cases summarize real Playbook behavioral regression fixtures and formal fresh-session results. They provide inspectable evidence of the behavior under test, **not third-party testimonials and not a replacement for policy**. Canonical rules remain in the linked owner documents.／以下案例整理 Playbook 已實際執行的行為迴歸測試情境與正式全新工作階段結果；它們是可檢查的行為證據，**不是第三方推薦，也不取代權威規則**。規範性規則仍由所連結的主責文件管理。

### 1. Useful Idea ≠ Authorized Work / 有價值的想法 ≠ 已授權工作

**Before**

An AI notices that a dependency-freshness scanner would be useful. The user replies, “OK, note it down.” A naive workflow can silently turn that suggestion into an authorized task, add it to the active queue, or even begin implementation.

**After**

The Playbook separates **observation → recommendation → admitted work**. In the formal `BEH-002` fresh-session run, the optional scanner stayed a low-commitment Cold candidate; persistence did not grant implementation authority, no write target was guessed, and promotion required a future trigger and reconciliation.

Evidence: [`BEH-002 formal run`](evals/runs/BEH-002-2026-09-07-formal-002.json) · Canonical owner: [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md)

**繁體中文**

AI 自己發現「相依套件版本更新檢查器（dependency freshness scanner）」看起來很有價值，使用者只說「好，先記著」。如果沒有工作准入邊界，這句話很容易被 AI 擴張成已承諾任務、加入 Hot 工作佇列，甚至直接開始實作。

Playbook 會把 **觀察 → 建議 → 准入工作** 分開。正式 `BEH-002` 全新工作階段實測中，這個可選檢查器只保持為低承諾的 Cold 候選項目；「被記錄」沒有變成實作權限，也沒有猜測寫入目標，未來要升級成 Hot 仍需真實觸發條件與一致性核對。

證據：[`BEH-002 正式測試`](evals/runs/BEH-002-2026-09-07-formal-002.json) · 權威主責：[`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md)

### 2. Test Passed ≠ Done / 測試通過 ≠ 真實世界已完成

**Before**

An external workflow reports `Converged` and `PASS`. It is tempting to call the feature fully done and deploy it immediately, even though hardware validation, canonical GitHub read-back, production smoke, or deployment permission may still be separate gates.

**After**

The Playbook keeps every positive status scoped to what it actually proves. In the formal `BEH-014` run, the model preserved pending hardware/device validation, production and repository-completion gates, and explicit deployment permission; it refused to promote the green workflow status into universal completion or deployment authority.

Evidence: [`BEH-014 formal run`](evals/runs/BEH-014-2026-09-07-formal-001.json) · Canonical owner: [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md)

**繁體中文**

外部工作流程顯示 `Converged`、`PASS`，很容易被直接講成「整個功能已完成，可以部署」，即使硬體驗證、GitHub 權威內容回讀、正式環境冒煙測試或部署權限其實仍是獨立關卡。

Playbook 要求每個 PASS 只證明它真正涵蓋的範圍。正式 `BEH-014` 實測中，模型保留待完成的硬體／裝置驗證、正式環境與儲存庫完成關卡，以及明確的部署權限；沒有把工作流程的綠燈升格成全域完成狀態或部署權限。

證據：[`BEH-014 正式測試`](evals/runs/BEH-014-2026-09-07-formal-001.json) · 權威主責：[`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md)

### 3. Who Actually Has Authority? / 現在到底該由誰做？

**Before**

A previous Stage used Codex, or a generic workflow assumes that implementation-facing artifacts must always be handed to a coding agent. That can create another Codex handoff even when the new work is read-only research—or block ChatGPT from a source/docs/tests mutation that the repository explicitly authorizes it to maintain.

**After**

The Playbook chooses the actor from the **current responsibility and repository-declared actor topology**, not from the previous actor or artifact type alone. `BEH-010` protects against handoff inertia across Stages; `BEH-019` protects the complementary case where ChatGPT is already the authorized implementation / maintenance actor and no Codex handoff should be invented.

Evidence: [`BEH-010 formal run`](evals/runs/BEH-010-2026-09-07-formal-002.json) · [`BEH-019 scenario`](evals/BEH_019_SUPPLEMENTAL.md) · Canonical owners: [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md), [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md)

**繁體中文**

上一個 Stage 曾由 Codex 執行，或舊式流程直接假設「只要碰到 implementation artifact 就一定要交給程式代理」，都可能造成錯誤分工：新的工作明明只是研究／證據整理卻又被慣性丟給 Codex；反過來，repository 已明確授權 ChatGPT 維護 source／docs／tests 時，也可能被通用舊規則錯誤擋住。

Playbook 現在依**目前責任與 repository 明確宣告的 actor topology**選擇執行角色，而不是只看上一個actor或artifact類型。`BEH-010` 防止跨Stage的handoff inertia；`BEH-019`則保護另一個互補情境：ChatGPT本來就是已授權的implementation／maintenance actor時，不應虛構Codex handoff。

證據：[`BEH-010 正式測試`](evals/runs/BEH-010-2026-09-07-formal-002.json) · [`BEH-019 情境`](evals/BEH_019_SUPPLEMENTAL.md) · 權威主責：[`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md)、[`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md)

These three cases are intentionally compact. The Showcase is a proof surface, not a second documentation system. More scenarios live under [`evals/`](evals/), while normative behavior stays with each canonical owner.

以上三個案例刻意保持小型。Showcase 是證據展示層，不是第二套文件系統；更多測試情境留在 [`evals/`](evals/)，規範性行為仍由各權威主責文件管理。

## What it controls / 它控制哪些問題

**English**

- **Context engineering** — Always-on / Hot / Cold / Evidence / Historical responsibilities keep each task from paying the context cost of the entire repository history.
- **Agent governance** — Persistence, default loading, write authority, and execution authority are separate concepts.
- **Repository actor topology** — Project governance declares which actor owns planning, source/docs/tests/tooling mutation, validation, Git, release, deployment, or other responsibilities; the Playbook supplies a conservative fallback rather than a universal ChatGPT→Codex workflow.
- **Repository memory** — Current canonical GitHub state outranks old chat state or model memory.
- **Task routing** — `CHAT_INIT.md` routes a task to the minimum canonical owner instead of encouraging whole-repository reading.
- **Workflow interoperability** — External spec, skills, or governance systems can coexist without losing Playbook authority / loading / evidence boundaries.
- **Validation and evidence** — Deterministic checks, behavioral evaluation, runtime / hardware / production evidence, and completion read-back remain distinct.
- **Cost-aware execution** — The Evidence → Context → Model → Reasoning → Agent → Validation chain expands only when evidence shows the cheaper level is insufficient.
- **Mixed-profile Codex execution** — The user still chooses the root model/reasoning, while a Prompt can authorize already-valid bounded child work to use a lower or higher model/reasoning profile when that improves end-to-end cost or quality; profile switching alone never creates delegation authority.
- **Ephemeral compute** — ChatGPT may run bounded deterministic workloads in a suitable sandbox without gaining repository write authority from that capability alone.

**繁體中文**

- **上下文工程（Context engineering）**：Always-on／Hot／Cold／Evidence／Historical 各有不同責任，不讓每個任務都付出整份儲存庫記憶的上下文成本。
- **代理治理（Agent governance）**：持久化（Persistence）、預設載入、寫入權限與執行權限分開判斷。
- **儲存庫角色拓撲（Repository actor topology）**：由project governance宣告planning、source／docs／tests／tooling修改、validation、Git、release、deployment等責任由誰承擔；Playbook只提供保守fallback，不把ChatGPT→Codex寫成所有repository的固定workflow。
- **儲存庫記憶（Repository memory）**：GitHub 目前的權威狀態高於舊聊天室或模型記憶。
- **任務路由（Task routing）**：從 `CHAT_INIT.md` 依任務直達最低必要的權威主責文件，而不是鼓勵全文掃描整個儲存庫。
- **工作流程互通（Workflow interoperability）**：外部規格、技能與治理框架可以共存，同時保留 Playbook 的權威、載入與證據邊界。
- **驗證與證據（Validation and evidence）**：確定性檢查、行為評估、執行環境／硬體／正式環境證據與完成後回讀彼此分開，不互相冒充。
- **成本感知執行（Cost-aware execution）**：Evidence → Context → Model → Reasoning → Agent → Validation 這條鏈只有在證據顯示較低成本層級不足時才逐級擴張。
- **Codex 混合 profile 執行（Mixed-profile Codex execution）**：root model／reasoning 仍由使用者選擇；同一份 Prompt 可授權原本就合法、可獨立 delegation 的 bounded child，依端到端成本／品質向較低或較高 model／reasoning profile 路由；但「想換 profile」本身不會產生 delegation authority。
- **暫態運算（Ephemeral compute）**：ChatGPT 可在合適的沙箱環境執行有界確定性工作負載，但不會只因「能執行」就取得儲存庫寫入權限。

## Core differentiators / 核心差異

**English**

The Playbook does not try to replace an agent runtime, skills package, spec framework, or enterprise compliance suite. Its job is to make long-running AI work on real repositories **reconstructable, bounded, and evidence-driven**.

Its five main differentiators are:

1. **Repository Information Architecture for AI** — Repository surfaces are organized around responsibility, retrieval intent, current authority, coordination, evidence, and history—not just file storage.
2. **Context has a lifecycle** — Information can be durable without being default-loaded into every task.
3. **Persistence ≠ loading ≠ write ≠ execution** — Being visible, remembered, or technically callable does not grant authority.
4. **Real-world evidence is first-class** — Software PASS does not automatically replace hardware, bench, production, or user-observed evidence.
5. **Minimum-sufficient cost is a shared optimization objective** — Use the cheapest sufficient evidence, context, model, reasoning, agent, and validation scope before escalating.

The common goal is **governance without bureaucracy**: enough structure to keep long-lived AI engineering coherent, without turning every small task into a heavyweight ceremony.

**繁體中文**

Playbook 不試圖取代代理執行環境（agent runtime）、技能套件、規格框架或企業合規套件。它的工作是讓 AI 長期操作真實儲存庫時，專案狀態仍然**可重建、有邊界、以證據驅動**。

五個主要差異：

1. **面向 AI 的儲存庫資訊架構（Repository Information Architecture for AI）**：GitHub 不只是檔案儲存，而是依資訊介面責任、檢索目的、目前權威、協作、證據與歷史來設計。
2. **上下文有生命週期**：資訊可以被持久保存，但不代表每個任務都要預設載入。
3. **持久化 ≠ 載入 ≠ 寫入 ≠ 執行**：看得到、記得住、技術上能呼叫，都不等於取得權限。
4. **真實世界證據是一級公民**：軟體 PASS 不會自動覆蓋硬體、工作台、正式環境或使用者實際觀察到的證據。
5. **最低充分成本是共同最佳化目標**：先使用最低充分的證據、上下文、模型、推理、代理與驗證範圍，不足才升級。

共同目標是**不增加官僚負擔的治理**：提供足夠結構讓長期 AI 工程保持一致，但不把每個小任務都變成重型流程。

## Core operating principles / 核心操作原則

**English**

> Get the minimum sufficient evidence first. Then use the minimum sufficient Context, Model, Reasoning, Agent, and Validation scope. Escalate only when evidence shows the current level is insufficient.

> The common Playbook defines **how to develop**. Each real project repository defines **what the system is**.

> A repository should let AI reach one sufficient current source of authority at minimum retrieval cost. Files, indexes, registries, summaries, metadata, and manifests are means, not goals.

**繁體中文**

> 先取得最低充分證據，再使用最低充分的上下文、模型、推理、代理與驗證範圍；只有證據顯示目前層級不足時才逐級擴張。

> 共通 Playbook 管**怎麼開發**；各實際專案儲存庫管**系統是什麼**。

> 儲存庫應讓 AI 以最低充分檢索成本命中唯一且足夠的目前權威來源；拆檔、索引、登錄表、摘要、中繼資料與清單（manifest）都只是手段，不是目標。

## Adoption Doctor / 導入檢查器

**English**

Adoption Doctor is a deterministic, read-only, report-only check of a target project's Playbook adoption and routing contract. It does not replace project-specific semantic review, and running it does not grant write authority to the target repository.

Local Path Mode:

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT GitHub Snapshot Mode:

`GitHub canonical → ChatGPT minimum-sufficient snapshot → adoption_doctor.py → PASS / WARN / FAIL report`

A ChatGPT session with repository-read capability may retrieve only the files required by the Doctor's active checks, materialize a temporary snapshot, and run the same deterministic engine when its runtime contract is satisfied. The snapshot is only an execution input; it is not a new source of truth.

**繁體中文**

Adoption Doctor 是唯讀／僅報告的確定性檢查，用來檢查目標專案的 Playbook 導入與路由契約。它不取代專案專屬的語意審查，也不會只因執行檢查就取得目標儲存庫的寫入權限。

本機路徑模式（Local Path Mode）：

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT GitHub 快照模式（Snapshot Mode）：

`GitHub canonical → ChatGPT minimum-sufficient snapshot → adoption_doctor.py → PASS / WARN / FAIL report`

具備儲存庫讀取能力的 ChatGPT 工作階段，可以只取得 Doctor 目前檢查所需的最低充分檔案，建立暫時快照，並在執行環境契約成立時執行同一套確定性檢查引擎。這份快照只作為執行輸入，不是新的事實來源。

## Repository map / 文件地圖

**English**

Humans normally do not need to read these files in order. This map explains where AI routes for specific responsibilities.

| File | Responsibility |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Maintainer authority for this Playbook repository: ChatGPT / Codex ownership, audience / surface contract, direct-write and execution exceptions, validator contract, mutation integrity |
| [`CHAT_INIT.md`](CHAT_INIT.md) | Minimum AI-session bootstrap, task router, repository-read recovery |
| [`PROJECT_BOOTSTRAP.md`](PROJECT_BOOTSTRAP.md) | Research bootstrap, reuse-first research, stage-transition actor revalidation, research write allowlist, post-adoption context closure, implementation actor transition / handoff |
| [`CAPABILITY_INDEX.md`](CAPABILITY_INDEX.md) | Thin whole-repository capability-discovery index for capability / gap / absence review |
| [`PLAYBOOK_INDEX.json`](PLAYBOOK_INDEX.json) | Routing-only machine manifest: stable capability IDs, owners, sections, implementation and adapter pointers |
| [`INTEROPERABILITY.md`](INTEROPERABILITY.md) | Playbook-side authority / loading / evidence mapping for external spec, skills, and governance systems |
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | AI-readable repository information architecture, progressive routing, retrieval cost, routing metadata, write closure |
| [`INFORMATION_INTEGRITY.md`](INFORMATION_INTEGRITY.md) | Semantic identity, durable fact ownership, provenance, snapshot / search-hit authority guards |
| [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) | ChatGPT planning / coordination authority, task contract, durable-work admission, actor admission / optional Codex handoff, runtime execution, session compaction / rehydration, response contract |
| [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) | Codex / coding-agent execution authority, model / reasoning / context / cost / tool scheduling / reporting when that actor is selected |
| [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) | Repository identity, actor topology / maintenance ownership, permission, write boundaries, remote write / read-back, repository-facing documentation integrity |
| [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) | Debug, root cause, retry, validation, evidence lifecycle, completion read-back, behavioral evaluation |
| [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) | Research, target / capability, architecture, state / lifecycle, ownership |
| [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) | Embedded / hardware / board-specific workflow |
| [`UI_UX.md`](UI_UX.md) | UI / UX / i18n / design-system adaptation |
| [`TOOLCHAIN.md`](TOOLCHAIN.md) | Local toolchain / runtime / PowerShell contract |
| [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) | Minimal project-adoption example |

**繁體中文**

一般人類使用者不需要依序閱讀這些文件；這張表說明 AI 在不同責任下會路由到哪裡。

| 文件 | 責任 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | 本 Playbook 儲存庫的維護權威：ChatGPT／Codex 維護責任、讀者／介面契約、直接寫入與執行例外、驗證器契約、修改完整性 |
| [`CHAT_INIT.md`](CHAT_INIT.md) | AI 工作階段最小啟動、任務路由器、儲存庫讀取復原 |
| [`PROJECT_BOOTSTRAP.md`](PROJECT_BOOTSTRAP.md) | 研究啟動、優先重用既有研究、階段轉換時重新驗證執行角色、研究寫入白名單、導入後上下文收斂、implementation actor轉換／交接 |
| [`CAPABILITY_INDEX.md`](CAPABILITY_INDEX.md) | 整個儲存庫的薄型能力探索索引，用於能力／缺口／不存在判斷 |
| [`PLAYBOOK_INDEX.json`](PLAYBOOK_INDEX.json) | 僅供路由的機器清單：穩定能力 ID、主責文件、章節、實作與介接器指標 |
| [`INTEROPERABILITY.md`](INTEROPERABILITY.md) | 外部規格、技能與治理系統的 Playbook 端權威／載入／證據對應 |
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | AI 可讀的儲存庫資訊架構、漸進式路由、檢索成本、路由中繼資料、寫入收斂 |
| [`INFORMATION_INTEGRITY.md`](INFORMATION_INTEGRITY.md) | 語意身分、持久事實歸屬、來源溯源、快照／搜尋命中的權威防護 |
| [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) | ChatGPT 規劃／協作權威、任務契約、持久工作准入、actor admission／條件式Codex交接、執行環境操作、工作階段壓縮／重新載入、回覆契約 |
| [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) | Codex／程式代理被選中時的執行權威、模型／推理／上下文／成本、工具排程與輸出、回報 |
| [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) | 儲存庫身分、actor topology／maintenance ownership、權限、寫入邊界、遠端寫入／回讀、面向儲存庫的文件完整性 |
| [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) | 除錯、根因、重試、驗證、證據生命週期、完成後回讀、行為評估 |
| [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) | 研究、目標／能力、架構、狀態／生命週期、責任歸屬 |
| [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) | 嵌入式／硬體／開發板專屬工作流程 |
| [`UI_UX.md`](UI_UX.md) | UI／UX／國際化（i18n）／設計系統調整 |
| [`TOOLCHAIN.md`](TOOLCHAIN.md) | 本機工具鏈／執行環境／PowerShell 契約 |
| [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) | 最小專案導入範例 |

## Human and AI reading paths / 人類與 AI 的讀取路徑

**English**

Human path:

`README → understand value and adoption → add thin bootstrap to project AGENTS.md → hand the task to AI / agent`

AI / agent path for a real project:

`Project AGENTS.md → resolve Playbook baseline → CHAT_INIT.md → project governance/current truth → minimum-sufficient canonical owner`

Maintaining this Playbook repository:

`Playbook AGENTS.md → task-relevant canonical owner`

Whole-repository capability / gap / absence review:

`CAPABILITY_INDEX.md / PLAYBOOK_INDEX.json → bounded discovery → canonical owner confirmation`

**繁體中文**

人類路徑：

`README → 理解價值與導入方式 → 在專案 AGENTS.md 加入薄型啟動宣告 → 交給 AI／代理`

實際專案的 AI／代理路徑：

`專案 AGENTS.md → 解析 Playbook 基準版本 → CHAT_INIT.md → 專案治理／目前權威事實 → 最低充分權威主責文件`

維護本 Playbook 儲存庫：

`Playbook AGENTS.md → 與任務相關的權威主責文件`

整個儲存庫的能力／缺口／不存在檢視：

`CAPABILITY_INDEX.md / PLAYBOOK_INDEX.json → 有界探索 → 確認權威主責文件`

## Relationship to real projects / 與實際專案的關係

**English**

The Playbook stores cross-project development methods, not product-specific truth. Each real project still owns its own:

- technical source of truth;
- current task / blocker / evidence;
- actor / maintenance ownership and repository write boundary;
- hardware pinout / protocol specifics;
- secrets / deployment values;
- release / branch state.

Do not copy the whole Playbook into every project. Keep a thin declaration / routing layer in the project's `AGENTS.md`, and keep project-specific truth in the project itself.

**繁體中文**

Playbook 保存跨專案共通的「怎麼開發」，不保存產品專屬的「系統是什麼」。每個實際專案仍自行擁有：

- 技術事實來源；
- 目前任務／阻塞點／證據；
- actor／maintenance ownership 與repository寫入邊界；
- 硬體腳位配置／協定細節；
- 機密資訊／部署值；
- 發行版本／分支狀態。

不要把整份 Playbook 複製進每個專案。只需在專案 `AGENTS.md` 保留薄型導入宣告／路由層，專案專屬事實則留在專案自己的權威資訊介面。

## License

MIT