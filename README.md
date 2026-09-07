# AI Development Playbook｜AI 協作開發實戰手冊

> **Give AI enough structure to work reliably without turning engineering into bureaucracy.**
>
> **讓 AI 有足夠結構可以可靠工作，但不要把工程變成流程儀式。**

## What this is / 這是什麼

**English**

AI Development Playbook is a reusable **GitHub-native governance and information-integrity layer** for ChatGPT, Codex, and other AI engineering workflows.

It treats GitHub as durable project memory and source of truth, ChatGPT as the reasoning and bounded ephemeral-compute layer, and Codex / coding agents as authorized repository implementers. The goal is not to add more prompts or process. The goal is to keep **context, authority, evidence, execution, validation, and cost** distinguishable as a project evolves across sessions and agents.

You do **not** need to load or read the whole repository. A project declares the Playbook as a common baseline, an AI session starts from [`CHAT_INIT.md`](CHAT_INIT.md), and then reads only the minimum canonical sections required by the current task.

**繁體中文**

AI Development Playbook 是一套可重用的 **GitHub-native AI 工程治理與資訊完整性層**，適用於 ChatGPT、Codex 與其他 AI engineering workflows。

它把 GitHub 當成持久化專案記憶與單一事實來源，由 ChatGPT 負責推理與有界暫態運算，Codex／coding agents 負責經授權的 repository implementation。目標不是增加 Prompt 或流程，而是讓專案跨聊天室、跨代理長期演進時，**上下文、權威、證據、執行、驗證與成本**仍然彼此可分辨。

你**不需要**完整載入或從頭讀完這個 repository。實際專案只要宣告 Playbook 為共通 baseline，AI session 從 [`CHAT_INIT.md`](CHAT_INIT.md) 進入，再依目前 Task 只讀最低必要的 canonical sections。

> **Human-facing language contract / 人類閱讀語言契約**：`README.md` 是本 repository 唯一的 primary human-facing surface。每個主要主題以 **English first → Traditional Chinese counterpart** 的固定方式呈現；兩種語言維持 contract-level semantic parity，但不要求逐句翻譯、相同句數或完全相同修辭。其餘 AI-facing canonical surfaces 依 semantic precision、stable terminology 與 retrieval reliability 選擇最適合的自然語言。

> **Dogfooding note / 自我實作說明**：This repository is primarily maintained by ChatGPT under the explicit maintainer contract in [`AGENTS.md`](AGENTS.md). This is a governed maintainer workflow, **not** a claim of fully autonomous repository maintenance.／本 repository 主要由 ChatGPT 依 [`AGENTS.md`](AGENTS.md) 的明確 maintainer contract 維護；這是受治理的 maintainer workflow，**不是**「完全自主維護」宣稱。

## 5-minute first use / 5 分鐘開始使用

**English**

If you already have a GitHub project:

1. Add a small Playbook declaration to the project-root `AGENTS.md`.
2. Choose one active Playbook baseline, such as `main` or a pinned release tag.
3. Start a new ChatGPT / AI / coding-agent session by reading that baseline's [`CHAT_INIT.md`](CHAT_INIT.md).
4. Let the AI route to only the canonical sections needed for the current task, while keeping the project's own governance and technical truth higher authority.

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

Shortest model:

`Project AGENTS.md → Playbook baseline → CHAT_INIT.md → project governance/current truth → minimum-sufficient canonical owner`

Use `Playbook baseline: main` when you intentionally want current rules. Use a released tag when reproducibility matters.

The snippet above is the smallest bootstrap, not the full deterministic adoption contract. For a ready-to-adapt example that can be checked by Adoption Doctor, use [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md).

**繁體中文**

如果你已經有 GitHub 專案：

1. 在 project root 的 `AGENTS.md` 放一小段 Playbook declaration。
2. 只選一個目前有效的 Playbook baseline，例如 `main` 或固定 release tag。
3. 新的 ChatGPT／AI／coding-agent session 先讀該 baseline 的 [`CHAT_INIT.md`](CHAT_INIT.md)。
4. 讓 AI 依目前 Task 只載入最低必要 canonical sections，同時保持專案自己的 governance 與 technical truth 為較高權威。

上面的英文 bootstrap 可以直接使用；AI 不需要 project declaration 也同時維護兩份語言版本。

最短模型：

`Project AGENTS.md → Playbook baseline → CHAT_INIT.md → project governance/current truth → minimum-sufficient canonical owner`

想持續取得 current rules 時使用 `Playbook baseline: main`；需要可重現時改成已發布 tag。

上面只是最小 bootstrap，不是完整 deterministic adoption contract。若要使用可由 Adoption Doctor 檢查的範例，請從 [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) 開始。

## Why this exists / 為什麼需要它

**English**

AI coding often fails in ways that are not really "coding" failures:

- a useful idea silently becomes unauthorized work;
- a test passes and gets reported as if the real system is done;
- an old chat or cached summary overrides the current repository truth;
- an agent can technically call a tool, so capability is mistaken for authority;
- every task loads too much repository history, increasing cost and stale-context risk;
- multiple agents or workflows each carry a different idea of what is current.

The Playbook gives these failure modes explicit boundaries and routing instead of trying to solve them with a larger prompt.

**繁體中文**

AI coding 很多失敗其實不是「程式寫不好」：

- AI 覺得某個改善很有價值，就默默把它變成未授權工作；
- test PASS 被直接講成真實系統已完成；
- 舊聊天室或 cached summary 覆蓋 current repository truth；
- agent 技術上能呼叫工具，就把 capability 誤當 authority；
- 每個 Task 都載入過多歷史，增加成本與 stale-context 風險；
- 不同 agent／workflow 各自保留不同版本的「目前狀態」。

Playbook 的做法不是塞更大的 Prompt，而是把這些 failure modes 變成清楚的 authority、routing、evidence 與 lifecycle 邊界。

## Before / After showcase / 前後對照案例

> **Illustrative, non-normative evidence layer / 說明性、非規範性證據層**：These cases summarize real Playbook behavioral-regression fixtures and formal fresh-session results. They are inspectable evidence of the behavior being tested, **not third-party testimonials and not replacement policy**. Canonical rules remain in the linked owner documents.／以下案例整理 Playbook 已實際執行的 behavioral-regression fixtures 與 formal fresh-session results；它們是可檢查的行為證據，**不是第三方推薦，也不取代 canonical policy**。

### 1. Useful Idea ≠ Authorized Work / 有價值的想法 ≠ 已授權工作

**Before**

An AI notices that a dependency-freshness scanner would be useful. The user replies, “OK, note it down.” A naive workflow can silently turn that suggestion into a committed task, add it to the active queue, or even begin implementation.

**After**

The Playbook separates **observation → recommendation → admitted work**. In the formal `BEH-002` fresh-session run, the optional scanner stayed a low-commitment Cold candidate; persistence did not grant implementation authority, no write target was guessed, and promotion required a future trigger and reconciliation.

Evidence: [`BEH-002 formal run`](evals/runs/BEH-002-2026-09-07-formal-002.json) · Canonical owner: [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md)

**繁體中文**

AI 自己發現 dependency freshness scanner 看起來很有價值，使用者只說「好，先記著」。沒有 admission boundary 時，這句話很容易被 AI 擴張成 committed task、Hot queue，甚至直接開始實作。

Playbook 會把 **observation → recommendation → admitted work** 分開。正式 `BEH-002` fresh-session 實測中，這個 optional scanner 只保持為低承諾 Cold candidate；「被記錄」沒有變成 implementation authority，也沒有猜測 write target，未來要升級成 Hot 仍需真實 trigger 與 reconciliation。

### 2. Test Passed ≠ Done / 測試通過 ≠ 真實世界已完成

**Before**

An external workflow reports `Converged` and `PASS`. It is tempting to call the feature fully done and deploy it immediately, even though hardware validation, canonical GitHub read-back, production smoke, or deployment permission may still be separate gates.

**After**

The Playbook keeps every positive status scoped to what it actually proves. In the formal `BEH-014` run, the model preserved pending hardware/device validation, production and repository-completion gates, and explicit deployment permission; it refused to promote the green workflow status into universal completion or deployment authority.

Evidence: [`BEH-014 formal run`](evals/runs/BEH-014-2026-09-07-formal-001.json) · Canonical owner: [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md)

**繁體中文**

外部 workflow 顯示 `Converged`、`PASS`，很容易被直接講成「整個 feature 已完成，可以部署」，即使 hardware validation、GitHub canonical read-back、production smoke 或 deployment permission 其實仍是獨立 gate。

Playbook 要求每個 PASS 只證明它真的涵蓋的 scope。正式 `BEH-014` 實測中，模型保留 pending hardware/device validation、production／repository completion 與 deployment permission，沒有把 workflow 綠燈升格成 universal completion 或 deployment authority。

### 3. Who Actually Has Authority? / 現在到底該由誰做？

**Before**

Codex implemented the previous Stage, so the next generic “OK, continue” automatically produces another Codex handoff—even when the new work is only bounded documentation research, provenance, and evidence synthesis.

**After**

The Playbook chooses the actor from the **current responsibility**, not the previous actor. In the formal `BEH-010` run, ChatGPT re-evaluated the new Stage, kept the research read-only, did the evidence work directly, and deferred Codex until a later Stage actually required coding-agent-owned mutation.

Evidence: [`BEH-010 formal run`](evals/runs/BEH-010-2026-09-07-formal-002.json) · Canonical owner: [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md)

**繁體中文**

上一個 Stage 是 Codex 做 source implementation，下一句「好，繼續」如果直接繼承上一個 actor，就可能又產生 Codex Prompt，即使新的工作其實只有 bounded official-document research、provenance 與 evidence synthesis。

Playbook 依**目前 responsibility**重新選 actor，而不是沿用 previous actor。正式 `BEH-010` 實測中，ChatGPT 重新判斷新 Stage、維持 read-only research、直接完成 evidence work，直到後續真的出現 coding-agent-owned mutation 才考慮 Codex handoff。

These three cases intentionally stay small. The Showcase is a proof surface, not a second documentation system. More scenarios live under [`evals/`](evals/), while normative behavior stays with each canonical owner.

以上三個案例刻意保持小型。Showcase 是 proof surface，不是第二套文件系統；更多 scenario 留在 [`evals/`](evals/)，normative behavior 仍由各 canonical owner 負責。

## What it controls / 它控制哪些問題

**English**

- **Context engineering** — Always-on / Hot / Cold / Evidence / Historical responsibilities prevent every task from paying for the whole repository memory.
- **Agent governance** — Persistence, default loading, write authority, and execution authority are separate concepts.
- **Repository memory** — Current canonical GitHub state outranks old chat state or model memory.
- **Task routing** — `CHAT_INIT.md` routes a task to the minimum canonical owner instead of encouraging whole-repository reading.
- **Workflow interoperability** — External spec, skills, or governance systems can coexist without losing Playbook authority / loading / evidence boundaries.
- **Validation and evidence** — Deterministic checks, behavioral evaluation, runtime / hardware / production evidence, and completion read-back remain distinct.
- **Cost-aware execution** — Evidence → Context → Model → Reasoning → Agent → Validation expands only when evidence shows the cheaper level is insufficient.
- **Ephemeral compute** — ChatGPT may run bounded deterministic workloads in a suitable sandbox without gaining repository write authority from that capability alone.

**繁體中文**

- **上下文工程（Context engineering）**：Always-on／Hot／Cold／Evidence／Historical 各有不同責任，不讓每個 Task 都付出整份 repository memory 的 Context 成本。
- **代理治理（Agent governance）**：Persistence、default loading、write authority、execution authority 分開判斷。
- **儲存庫記憶（Repository memory）**：GitHub current canonical state 高於舊聊天室或模型 memory。
- **任務路由（Task routing）**：從 `CHAT_INIT.md` 依 Task 直達最低必要 canonical owner，而不是鼓勵全文掃描。
- **外部工作流互通（Workflow interoperability）**：外部 spec／skills／governance framework 可以共存，同時保留 Playbook 的 authority／loading／evidence boundaries。
- **驗證與證據（Validation and evidence）**：deterministic checks、behavioral evaluation、runtime／hardware／production evidence、completion read-back 不互相冒充。
- **成本感知執行（Cost-aware execution）**：Evidence → Context → Model → Reasoning → Agent → Validation，只有 evidence 顯示不足時才逐級擴張。
- **暫態運算（Ephemeral compute）**：ChatGPT 可在合適 sandbox 執行有界 deterministic workload，但不因「能執行」就取得 repository write authority。

## Core differentiators / 核心差異

**English**

The Playbook does not try to replace an agent runtime, skills package, spec framework, or enterprise compliance suite. Its job is to make long-running AI work against real repositories **reconstructable, bounded, and evidence-driven**.

Its five main differentiators are:

1. **Repository Information Architecture for AI** — GitHub is organized around surface responsibility, retrieval intent, current authority, coordination, evidence, and history, not just file storage.
2. **Context has a lifecycle** — Information can be durable without being default-loaded into every task.
3. **Persistence ≠ loading ≠ write ≠ execution** — Being visible, remembered, or technically callable does not grant authority.
4. **Real-world evidence is first-class** — Software PASS does not automatically replace hardware, bench, production, or user-observed evidence.
5. **Minimum-sufficient cost is a shared optimization objective** — Use the cheapest sufficient evidence, context, model, reasoning, agent, and validation scope before escalating.

The common goal is **governance without bureaucracy**: enough structure to keep long-lived AI engineering coherent, without turning every small task into a heavyweight ceremony.

**繁體中文**

Playbook 不試圖取代 agent runtime、skills package、spec framework 或 enterprise compliance suite。它的工作是讓 AI 長期操作真實 repository 時，專案狀態仍然**可重建、有邊界、以 evidence 驅動**。

五個主要差異：

1. **面向 AI 的儲存庫資訊架構（Repository Information Architecture for AI）**：GitHub 不只是 file storage，而是依 surface responsibility、retrieval intent、current authority、coordination、evidence、history 設計。
2. **Context 有生命週期**：資訊可以被 durable 保存，但不代表每個 Task 都要 default-load。
3. **Persistence ≠ loading ≠ write ≠ execution**：看得到、記得住、技術上能呼叫，都不等於取得權限。
4. **Real-world evidence 是一級公民**：software PASS 不會自動覆蓋 hardware、bench、production 或 user-observed evidence。
5. **Minimum-sufficient cost 是共同最佳化目標**：先用最低充分 evidence、Context、Model、Reasoning、Agent、Validation scope，不足才升級。

共同目標是 **governance without bureaucracy**：提供足夠結構讓長期 AI engineering 保持一致，但不把每個小 Task 都變成重型流程。

## Core operating principles / 核心操作原則

**English**

> Get the minimum sufficient evidence first. Then use the minimum sufficient Context, Model, Reasoning, Agent, and Validation scope. Escalate only when evidence shows the current level is insufficient.

> The common Playbook defines **how to develop**. Each real project repository defines **what the system is**.

> A repository should let AI reach one sufficient current authority at minimum retrieval cost. Files, indexes, registries, summaries, metadata, and manifests are means, not goals.

**繁體中文**

> 先取得最低充分 Evidence，再使用最低充分 Context、Model、Reasoning、Agent 與 Validation scope；只有 evidence 證明不足時才逐級擴張。

> 共通 Playbook 管**怎麼開發**；各實際 project repository 管**系統是什麼**。

> Repository 應讓 AI 以最低充分 retrieval cost 命中唯一且足夠的 current authority；拆檔、index、registry、summary、metadata、manifest 都只是手段，不是目標。

## Adoption Doctor / 導入檢查器

**English**

Adoption Doctor is a read-only / report-only deterministic check for a target project's Playbook adoption and routing contract. It does not replace project-specific semantic review and does not gain target-repository write authority by running a check.

Local Path Mode:

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT GitHub Snapshot Mode:

`GitHub canonical → ChatGPT minimum-sufficient snapshot → adoption_doctor.py → PASS / WARN / FAIL report`

A ChatGPT session with repository-read capability may retrieve only the files required by Doctor's active checks, materialize a temporary snapshot, and run the same deterministic engine when its runtime contract is satisfied. The snapshot is only an execution input; it is not a new source of truth.

**繁體中文**

Adoption Doctor 是 read-only／report-only deterministic check，用來檢查目標 project 的 Playbook adoption 與 routing contract。它不取代 project-specific semantic review，也不因執行檢查而取得 target repository write authority。

Local Path Mode：

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT GitHub Snapshot Mode：

`GitHub canonical → ChatGPT minimum-sufficient snapshot → adoption_doctor.py → PASS / WARN / FAIL report`

具備 repository-read capability 的 ChatGPT session，可以只取得 Doctor active checks 所需的最低充分檔案，建立 temporary snapshot，並在 runtime contract 成立時執行同一 deterministic engine。Snapshot 只作 execution input，不是新的 source of truth。

## Repository map / 文件地圖

**English**

Humans normally do not need to read these files in order. This map explains where AI routes for specific responsibilities.

| File | Responsibility |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Maintainer authority for this Playbook repository: ChatGPT / Codex ownership, audience / surface contract, direct-write and execution exceptions, validator contract, mutation integrity |
| [`CHAT_INIT.md`](CHAT_INIT.md) | Minimum AI-session bootstrap, task router, repository-read recovery |
| [`PROJECT_BOOTSTRAP.md`](PROJECT_BOOTSTRAP.md) | Research bootstrap, reuse-first research, stage-transition actor revalidation, research write allowlist, post-adoption context closure, implementation handoff |
| [`CAPABILITY_INDEX.md`](CAPABILITY_INDEX.md) | Thin whole-repository capability-discovery index for capability / gap / absence review |
| [`PLAYBOOK_INDEX.json`](PLAYBOOK_INDEX.json) | Routing-only machine manifest: stable capability IDs, owners, sections, implementation and adapter pointers |
| [`INTEROPERABILITY.md`](INTEROPERABILITY.md) | Playbook-side authority / loading / evidence mapping for external spec, skills, and governance systems |
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | AI-readable repository information architecture, progressive routing, retrieval cost, routing metadata, write closure |
| [`INFORMATION_INTEGRITY.md`](INFORMATION_INTEGRITY.md) | Semantic identity, durable fact ownership, provenance, snapshot / search-hit authority guards |
| [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) | ChatGPT planning / coordination authority, task contract, durable-work admission, runtime execution, Codex handoff, session compaction / rehydration, response contract |
| [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) | Codex / coding-agent execution authority, model / reasoning / context / cost / tool scheduling / reporting |
| [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) | Repository identity, permission, write boundaries, remote write / read-back, repository-facing documentation integrity |
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
| [`AGENTS.md`](AGENTS.md) | 本 Playbook repository maintainer authority：ChatGPT／Codex ownership、audience／surface contract、direct-write／execution exception、validator contract、mutation integrity |
| [`CHAT_INIT.md`](CHAT_INIT.md) | AI session 最小 bootstrap、task router、repository read recovery |
| [`PROJECT_BOOTSTRAP.md`](PROJECT_BOOTSTRAP.md) | research bootstrap、reuse-first research、Stage transition actor revalidation、research write allowlist、post-adoption context closure、implementation handoff |
| [`CAPABILITY_INDEX.md`](CAPABILITY_INDEX.md) | whole-repository capability／gap／absence review 的薄型 discovery index |
| [`PLAYBOOK_INDEX.json`](PLAYBOOK_INDEX.json) | routing-only machine manifest：stable capability ID、owner、section、implementation、adapter pointers |
| [`INTEROPERABILITY.md`](INTEROPERABILITY.md) | 外部 spec／skills／governance systems 的 Playbook-side authority／loading／evidence mapping |
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | AI-readable repository information architecture、progressive routing、retrieval cost、routing metadata、write closure |
| [`INFORMATION_INTEGRITY.md`](INFORMATION_INTEGRITY.md) | semantic identity、durable fact ownership、provenance、snapshot／search-hit authority guards |
| [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) | ChatGPT planning／coordination authority、task contract、durable-work admission、runtime execution、Codex handoff、session compaction／rehydration、response contract |
| [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) | Codex／coding-agent execution authority、model／reasoning／context／cost／tool scheduling／reporting |
| [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) | repository identity、permission、write boundaries、remote write／read-back、repository-facing documentation integrity |
| [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) | debug、root cause、retry、validation、evidence lifecycle、completion read-back、behavioral evaluation |
| [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) | research、target／capability、architecture、state／lifecycle、ownership |
| [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) | embedded／hardware／board-specific workflow |
| [`UI_UX.md`](UI_UX.md) | UI／UX／i18n／design-system adaptation |
| [`TOOLCHAIN.md`](TOOLCHAIN.md) | local toolchain／runtime／PowerShell contract |
| [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) | 最小 project adoption 範例 |

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

`README → 理解價值與導入方式 → 把 thin bootstrap 放進 project AGENTS.md → 交給 AI／agent`

實際 project 的 AI／agent 路徑：

`Project AGENTS.md → resolve Playbook baseline → CHAT_INIT.md → project governance/current truth → minimum-sufficient canonical owner`

維護本 Playbook repository：

`Playbook AGENTS.md → task-relevant canonical owner`

Whole-repository capability／gap／absence review：

`CAPABILITY_INDEX.md / PLAYBOOK_INDEX.json → bounded discovery → canonical owner confirmation`

## Relationship to real projects / 與實際專案的關係

**English**

The Playbook stores cross-project development method, not product-specific truth. Each real project still owns its own:

- technical source of truth;
- current task / blocker / evidence;
- hardware pinout / protocol specifics;
- secrets / deployment values;
- release / branch state.

Do not copy the whole Playbook into every project. Keep a thin declaration / routing layer in the project's `AGENTS.md`, and keep project-specific truth in the project itself.

**繁體中文**

Playbook 保存跨專案共通的「怎麼開發」，不保存產品專屬的「系統是什麼」。每個實際 project 仍自行擁有：

- technical source of truth；
- current task／blocker／evidence；
- hardware pinout／protocol specifics；
- secrets／deployment values；
- release／branch state。

不要把整份 Playbook 複製進每個 project。只需在 project `AGENTS.md` 保留薄型 declaration／routing layer，project-specific truth 留在 project 自己的 canonical surfaces。

## License

MIT
