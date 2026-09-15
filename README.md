# AI Development Playbook｜AI 協作開發實戰手冊

> **Give AI enough structure to work reliably without turning engineering into bureaucracy.**
>
> **讓 AI 有足夠結構可以可靠工作，但不要把工程變成流程儀式。**

## What this is / 這是什麼

**English**

AI Development Playbook is a reusable **GitHub-native governance and information-integrity layer** for ChatGPT, Codex, and other AI engineering workflows.

It helps long-lived repositories keep **current authority, durable memory, task admission, execution, validation, evidence, and context cost** separate instead of letting old chats, tool availability, or convenient summaries silently become project truth.

An adopting repository chooses one of two Project AI modes:

- `ChatGPT-Only`
- `ChatGPT+Codex`

These modes describe **AI actor topology**. They are not ChatGPT subscription tiers, model tiers, quotas, or fixed capability levels. Project governance still decides the actual path/action authority inside the selected mode.

Adoption also does **not** mean every task must load the shared Playbook. A project may keep ordinary tasks on its own project-native bootstrap/task-router path and activate the shared Playbook only when the current task actually needs common workflow governance.

For `ChatGPT-Only`, the preferred cold-start compatibility target is:

`Free ChatGPT + fresh chat + empty cache + GitHub Connect-only repository authority acquisition`

This is a **design/regression target**, not a promise that every Free account or product surface exposes the same tools. Richer surfaces should remain optional accelerators unless project evidence proves they are materially required.

**繁體中文**

AI Development Playbook 是一套可重用、**以 GitHub 為原生基礎的 AI 工程治理與資訊完整性層**，適用於 ChatGPT、Codex 與其他 AI 工程工作流程。

它的目的，是讓長期演進的 repository 能持續把**目前權威、持久記憶、工作准入、執行、驗證、證據與 Context 成本**分清楚，避免舊聊天室、工具可用性或方便閱讀的摘要默默變成 project truth。

採用本手冊的 repository 只選兩種 Project AI mode 之一：

- `ChatGPT-Only`
- `ChatGPT+Codex`

這兩種 mode 描述的是 **AI actor topology**，不是 ChatGPT 訂閱方案、模型等級、使用額度或固定能力層級；實際 path／action authority 仍由 project governance 決定。

正式 adoption 也**不代表每個 task 都要載入 shared Playbook**。專案可以讓一般任務維持自己的 project-native bootstrap／task-router hot path，只有本次工作真正需要共通 workflow governance 時才 activate Playbook。

對 `ChatGPT-Only`，目前偏好的 cold-start 相容性目標是：

`Free ChatGPT + fresh chat + empty cache + GitHub Connect-only repository authority acquisition`

這是**設計／迴歸測試目標**，不是宣稱所有 Free 帳號或產品 surface 都一定具備相同工具。較強 surface 應維持 optional accelerator，除非 project evidence 證明它們是實質必要條件。

> **Human-facing contract / 人類閱讀契約**：This README is the repository's primary human-facing surface. Normative rules remain in the linked canonical owners.／本 README 是此 repository 的主要人類閱讀介面；正式規則仍由下方連結的 canonical owners 擁有。

## Core mental model / 核心心智模型

**English**

The Playbook is built around a few deliberately separate ideas:

- **Persistence ≠ loading ≠ write ≠ execution authority.** Stored or visible information does not automatically belong in every task and does not grant mutation authority.
- **Current canonical state outranks historical memory.** Old chat, summaries, caches, handoffs, and external memory are evidence until reconciled with current authority.
- **Capability ≠ authority.** A tool being callable does not mean the current task is authorized to use it for mutation or scope expansion.
- **PASS ≠ done.** A passing test, workflow, or sub-check proves only its own scope; hardware, production, repository read-back, release, or deployment gates may remain separate.
- **Adoption ≠ unconditional activation.** Shared governance should be loaded only when the current project route says it is needed.
- **Use the lowest sufficient path.** Evidence, Context, model/reasoning, actor, runtime capability, and validation should expand only when the current level is insufficient.

**繁體中文**

Playbook 的核心刻意把幾個概念分開：

- **持久化 ≠ 載入 ≠ 寫入 ≠ 執行權限**：資訊被保存、看得到，不代表每個 task 都要讀，也不代表取得 mutation authority。
- **目前 canonical state 高於 historical memory**：舊聊天、摘要、cache、handoff、外部 memory 都只是 evidence，必須與 current authority reconciliation。
- **Capability ≠ authority**：工具能呼叫，不代表本次 task 有權因此擴張 mutation 或 scope。
- **PASS ≠ done**：test／workflow／子檢查 PASS 只證明自己的 scope；硬體、production、repository read-back、release、deployment 等 gate 仍可能獨立存在。
- **Adoption ≠ unconditional activation**：只有 project route 判定需要時才載入 shared governance。
- **優先最低充分路徑**：Evidence、Context、model/reasoning、actor、runtime capability 與 validation 都只有在目前層級不足時才擴張。

## 5-minute adoption / 5 分鐘導入

**English**

For an existing GitHub project:

1. Add a thin Playbook declaration to the project's current governance surface, commonly root `AGENTS.md`.
2. Choose one declared Playbook baseline, such as `main` or a pinned release/tag.
3. Choose exactly one Project AI mode: `ChatGPT-Only` or `ChatGPT+Codex`.
4. Keep the project's own bootstrap/task router authoritative. If it explicitly decides shared Playbook governance is not needed for a task, stay project-native.
5. When activation is required, resolve the declared baseline (including an exact revision when a floating ref matters), enter that revision's [`CHAT_INIT.md`](CHAT_INIT.md), and load only the minimum canonical owner(s) needed for the task.

Minimal adoption block:

```markdown
## Common AI Development Playbook

This project uses `masini1491/ai-development-playbook` as a common AI engineering baseline.
Playbook baseline: `main`
Project AI mode: ChatGPT-Only

Adoption does not require Playbook activation for every task. If this project declares a
project-native bootstrap / task router that decides whether shared governance is needed,
follow that gate first. When Playbook activation is required, resolve the declared baseline
and enter that revision's `CHAT_INIT.md`, then load only the minimum canonical sections
required by the current task.

This project's own governance and technical source of truth remain higher authority.
Do not load the whole Playbook into Context by default.
```

Use [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) when you want a fuller ready-to-adapt example.

**繁體中文**

對既有 GitHub 專案：

1. 在專案目前的 governance surface（常見是 root `AGENTS.md`）放入薄型 Playbook adoption 宣告。
2. 宣告一個 Playbook baseline，例如 `main` 或固定 release/tag。
3. Project AI mode 只選一種：`ChatGPT-Only` 或 `ChatGPT+Codex`。
4. 專案自己的 bootstrap／task router 維持權威；若它明確判定某 task 不需要 shared Playbook governance，就留在 project-native route。
5. 只有需要 activation 時，才解析 declared baseline（floating ref 在必要時解析 exact revision）、進入該 revision 的 [`CHAT_INIT.md`](CHAT_INIT.md)，再載入本題最低充分 canonical owner。

若需要較完整、可直接調整的 adoption example，請使用 [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md)。

## ChatGPT cold start / ChatGPT 冷啟動

**English**

The primary ChatGPT compatibility target does **not** depend on persistent Custom Instructions, warmed cache, a previous chat, Codex, public GitHub pages, shell Git, or Python HTTP for repository authority acquisition.

Preferred regression profile:

```text
Free ChatGPT
+ fresh chat
+ empty cache
+ GitHub Connect-only repository authority acquisition
```

After current repository authority is established, the session may use additional ChatGPT-native capabilities that are actually available and materially required, while preserving the same identity, integrity, execution, and validation gates.

If the core workflow fails under this profile, first ask whether the blocker is an avoidable convenience dependency, an alternate verifiable transport/materialization path, or a genuinely required capability. Do not silently promote a convenience dependency into the baseline.

**繁體中文**

主要 ChatGPT 相容性目標**不依賴** persistent Custom Instructions、warmed cache、舊聊天室、Codex、public GitHub page、shell Git 或 Python HTTP 來取得 repository authority。

偏好的 regression profile：

```text
Free ChatGPT
+ fresh chat
+ empty cache
+ GitHub Connect-only repository authority acquisition
```

建立 current repository authority 後，可以再使用該 ChatGPT surface 實際提供、而且本題實質需要的 ChatGPT-native capability，但仍必須維持相同 identity、integrity、execution 與 validation gate。

若核心 workflow 在這個 profile 下失敗，應先區分：是可以消除的 convenience dependency、仍有等價可驗證的 transport/materialization path，還是真的缺少 materially required capability；不要直接把方便路徑升格成 baseline prerequisite。

## Optional host adapters / 可選 host adapters

**English**

Persistent host instructions are **optional activation adapters**, not the core adoption mechanism and not project authority.

- [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) is a copy-ready ChatGPT host adapter for product surfaces where the current instruction field can accept it.
- [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) is the corresponding Codex host adapter where that product/runtime exposes a compatible persistent-instruction surface.
- [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md) owns the current activation, loading, health-check, and product-surface caveats.

Product UI names, field limits, and available persistent-instruction surfaces can change independently of Playbook policy. Do not treat README wording or an older screenshot as product authority. A host adapter being installed also does not prove that a project adopts the Playbook or grant repository mutation authority.

**繁體中文**

Persistent host instruction 是**可選 activation adapter**，不是核心 adoption mechanism，也不是 project authority。

- [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) 是給目前產品 surface 能容納該 payload 時使用的 ChatGPT copy-ready host adapter。
- [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) 是對應的 Codex host adapter，只有在該 product/runtime 提供相容 persistent-instruction surface 時才使用。
- [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md) 擁有目前的 activation、loading、health-check 與 product-surface caveat。

產品 UI 名稱、欄位限制與可用 persistent-instruction surface 都可能獨立於 Playbook policy 改變。不要把 README 舊文字或舊截圖當成產品權威；host adapter 被安裝也不代表某 project 已 adoption，更不會授予 repository mutation authority。

## Quick workflow / 快速流程

**English**

A typical project flow is:

```text
Current project identity / bootstrap
→ project-native activation gate when explicitly declared
→ shared Playbook activation only if needed
→ declared baseline + Project AI mode
→ minimum-sufficient canonical owner
→ current task / authority / evidence
→ lowest-sufficient authorized actor
→ execution or handoff
→ canonical read-back / reconciliation
→ done, next Stage, or STOP
```

`ChatGPT-Only` keeps Codex out of the repository AI workflow and aims to keep unnecessary ChatGPT capability requirements low. `ChatGPT+Codex` admits Codex only where current project governance/Stage actually assigns implementation work to it.

**繁體中文**

一般 project flow：

```text
目前 project identity / bootstrap
→ 若有明確宣告先走 project-native activation gate
→ 只有需要時才 activate shared Playbook
→ declared baseline + Project AI mode
→ 最低充分 canonical owner
→ current task / authority / evidence
→ 最低充分且已授權 actor
→ 執行或 handoff
→ canonical read-back / reconciliation
→ 完成、下一 Stage 或 STOP
```

`ChatGPT-Only` 不讓 Codex 進入 repository AI workflow，並盡量壓低不必要的 ChatGPT capability requirement；`ChatGPT+Codex` 也只有 current project governance／Stage 真正把 implementation 工作分派給 Codex 時才 handoff。

![AI Development Playbook quick workflow](assets/readme-workflow.svg)

> **Illustrative workflow / 流程概覽**：The diagram summarizes the stable human-facing flow only. Canonical rules remain in the linked owner documents, and product UI/version details are intentionally excluded.／本圖只摘要穩定的人類閱讀流程；正式規則仍以對應 canonical owner 為準，並刻意不放產品 UI／版本細節。

## What it covers / 主要涵蓋範圍

**English**

- **Project AI mode and actor admission** — choose `ChatGPT-Only` or `ChatGPT+Codex`, then apply lower-level repository authority.
- **Conditional activation** — adopted projects can keep low-cost project-native hot paths for tasks that do not need shared governance.
- **Context architecture** — Always-on / Hot / Cold / Evidence / Current / Historical responsibilities and progressive routing.
- **Repository and authority integrity** — current identity, path/action authority, permission boundaries, read-back, and source-vs-derived distinctions.
- **Task admission and coordination** — observation/recommendation/admitted-work separation, task identity, Stage boundaries, follow-up/new-work control.
- **Validation and evidence** — deterministic checks, behavioral evaluation, hardware/runtime/production evidence, completion reconciliation.
- **Runtime execution** — bounded ChatGPT-side deterministic execution when the current session actually has the required runtime/capabilities.
- **Interoperability** — external specs, skills, memory systems, and governance frameworks can coexist without inheriting authority merely by being connected.
- **Cost-aware execution** — use minimum-sufficient evidence, Context, model/reasoning, actor, and validation before escalating.

**繁體中文**

- **Project AI mode 與 actor admission**：先選 `ChatGPT-Only`／`ChatGPT+Codex`，再套用 lower-level repository authority。
- **Conditional activation**：已 adoption 的 project 可以讓不需要 shared governance 的 task 維持低成本 project-native hot path。
- **Context 架構**：Always-on／Hot／Cold／Evidence／Current／Historical responsibility 與 progressive routing。
- **Repository／authority integrity**：current identity、path/action authority、permission boundary、read-back、source-vs-derived 分離。
- **Task admission／coordination**：observation／recommendation／admitted-work 分離、task identity、Stage boundary、follow-up/new-work 控制。
- **Validation／evidence**：deterministic checks、behavioral eval、hardware/runtime/production evidence、completion reconciliation。
- **Runtime execution**：只有 current ChatGPT session 實際具備所需 runtime/capability 時，才做 bounded deterministic execution。
- **Interoperability**：external spec、skills、memory system、governance framework 可以共存，但不會只因被連接就繼承 authority。
- **成本感知執行**：Evidence、Context、model/reasoning、actor、validation 都先用最低充分層級，不足才升級。

## Evidence and behavioral evaluation / 證據與行為迴歸

**English**

The repository includes deterministic validators and behavioral-evaluation fixtures. Their purpose is to keep claims scoped to what was actually tested; they are not a second policy system.

Start here:

- [`evals/README.md`](evals/README.md) — behavioral evaluation structure and current evidence index.
- [`evals/`](evals/) — scenarios, supplemental cases, cold-start fixtures, regression matrix, and run records.
- [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) — canonical validation/evidence/completion contract.

Human-facing README examples should stay illustrative rather than duplicate a growing list of dated run snapshots.

**繁體中文**

Repository 內含 deterministic validator 與 behavioral-evaluation fixtures；它們的目的，是讓每個 claim 只涵蓋真正測到的範圍，不是第二套 policy system。

從這裡開始：

- [`evals/README.md`](evals/README.md)：behavioral evaluation 結構與目前 evidence index。
- [`evals/`](evals/)：scenario、supplemental case、cold-start fixture、regression matrix 與 run records。
- [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md)：canonical validation／evidence／completion contract。

README 只保留人類容易理解的概覽，不再複製會快速變舊的一長串 dated run snapshot。

## Adoption Doctor / 導入檢查器

**English**

Adoption Doctor is a deterministic, read-only, report-only check of a target project's Playbook adoption and routing contract.

Local Path Mode:

```text
python tools/adoption_doctor.py <project-root>
```

ChatGPT Snapshot Mode is also supported when the current ChatGPT session can acquire the exact minimum files, materialize a trustworthy temporary snapshot, and satisfy the runtime contract. Snapshot acquisition is separate from Doctor execution and does not create repository authority.

If exact materialization cannot be verified, report the acquisition/materialization gap rather than claiming deterministic validation passed.

**繁體中文**

Adoption Doctor 是 deterministic、read-only、report-only 的 adoption／routing contract 檢查器。

本機模式：

```text
python tools/adoption_doctor.py <project-root>
```

若 current ChatGPT session 能取得必要 exact files、建立可信 temporary snapshot 並滿足 runtime contract，也可使用 ChatGPT Snapshot Mode。Snapshot acquisition 與 Doctor execution 是不同層級，也不會建立 repository authority。

如果 exact materialization 無法驗證，就應回報 acquisition／materialization gap，不得宣稱 deterministic validation 已 PASS。

## Repository map / 文件地圖

**English**

Humans normally do not need to read these files in order. This map shows the main canonical owners and adapters.

| File | Primary responsibility |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Maintainer authority for this Playbook repository; human-surface contract; self-maintenance/write/execution boundaries |
| [`CHAT_INIT.md`](CHAT_INIT.md) | Minimum Playbook bootstrap/task router after activation; repository-read recovery |
| [`PROJECT_MODES.md`](PROJECT_MODES.md) | `ChatGPT-Only` / `ChatGPT+Codex`; mode-is-not-tier semantics; minimum ChatGPT capability floor; Free cold-start target |
| [`ACTIVATION_ADAPTERS.md`](ACTIVATION_ADAPTERS.md) | Thin host/runtime activation adapters, conditional activation, loading contract, health checks |
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | Context/information architecture, progressive routing, retrieval cost, Always-on/Hot/Cold/Evidence/Historical lifecycle |
| [`INFORMATION_INTEGRITY.md`](INFORMATION_INTEGRITY.md) | Identity, provenance, source-vs-derived authority, snapshot/search-hit/evidence guards |
| [`CHATGPT_WORKFLOW.md`](CHATGPT_WORKFLOW.md) | ChatGPT planning/coordination, work admission, actor admission, runtime execution, session compaction/rehydration, result reconciliation |
| [`CODEX_EXECUTION.md`](CODEX_EXECUTION.md) | Codex execution profile, reasoning/context/tool scheduling/reporting after Codex is actually selected |
| [`REPOSITORY_EXECUTION.md`](REPOSITORY_EXECUTION.md) | Repository identity, lower-level actor/path-action authority, permissions, write/read-back boundaries |
| [`DEBUG_VALIDATION.md`](DEBUG_VALIDATION.md) | Debugging, retry, validation, evidence lifecycle, completion, behavioral evaluation |
| [`PROJECT_BOOTSTRAP.md`](PROJECT_BOOTSTRAP.md) | Research/bootstrap lifecycle and bounded research-write/actor-transition contracts |
| [`RESEARCH_ARCHITECTURE.md`](RESEARCH_ARCHITECTURE.md) | Research, requirements, architecture, lifecycle, ownership |
| [`INTEROPERABILITY.md`](INTEROPERABILITY.md) | External systems/spec/skills/governance interoperability and authority mapping |
| [`CAPABILITY_INDEX.md`](CAPABILITY_INDEX.md) | Thin whole-repository capability/gap/absence discovery index |
| [`PLAYBOOK_INDEX.json`](PLAYBOOK_INDEX.json) | Machine-readable routing manifest; not policy/current-state authority |
| [`EMBEDDED_PROJECTS.md`](EMBEDDED_PROJECTS.md) | Embedded/hardware-specific workflow |
| [`UI_UX.md`](UI_UX.md) | UI/UX/i18n/design-system adaptation |
| [`TOOLCHAIN.md`](TOOLCHAIN.md) | Local runtime/toolchain/PowerShell contract |
| [`examples/minimal-project/AGENTS.md`](examples/minimal-project/AGENTS.md) | Minimal adoption example |

**繁體中文**

一般人類使用者不需要依序讀完這些檔案；這張表只說明主要 canonical owner／adapter 在哪裡。上表檔名與責任本身就是雙語共用的技術路由資訊；正式內容請依 task 只讀必要 owner。

## Human and AI reading paths / 人類與 AI 的讀取路徑

**English**

Human path:

`README → understand value/adoption → choose baseline + Project AI mode → add thin project declaration → hand task to AI`

AI path for an adopter project:

`Project identity/bootstrap → project-native activation gate when declared → project governance/adoption state when required → declared baseline + Project AI mode → Playbook CHAT_INIT only after activation → minimum canonical owner`

Maintaining this Playbook:

`Playbook AGENTS.md → maintainer routing when applicable → task-relevant canonical owner`

Whole-repository capability/gap/absence review:

`CAPABILITY_INDEX.md / PLAYBOOK_INDEX.json → bounded discovery → canonical-owner confirmation`

**繁體中文**

人類路徑：

`README → 理解價值／導入 → 選 baseline + Project AI mode → 加入薄型 project declaration → 交給 AI`

Adopter project 的 AI 路徑：

`Project identity/bootstrap → 若有宣告則先走 project-native activation gate → 需要時才讀 project governance/adoption state → declared baseline + Project AI mode → activation 後才進 Playbook CHAT_INIT → 最低充分 canonical owner`

維護本 Playbook：

`Playbook AGENTS.md → 需要時進 maintainer routing → task-relevant canonical owner`

整個 repository 的 capability／gap／absence review：

`CAPABILITY_INDEX.md / PLAYBOOK_INDEX.json → bounded discovery → canonical-owner confirmation`

## Relationship to real projects / 與實際專案的關係

**English**

The Playbook stores cross-project development methods, not product-specific truth. Each real project still owns its technical truth, current task/evidence, selected AI mode, repository write boundaries, activation routing, secrets, deployment values, hardware/protocol specifics, and release/branch state.

Do not copy the whole Playbook into every project. Keep only a thin adoption/routing layer in project governance, and keep project-specific truth in the project itself.

**繁體中文**

Playbook 保存跨專案共通的「怎麼開發」，不保存單一產品的「系統是什麼」。各 real project 仍自行擁有 technical truth、current task/evidence、AI mode、repository write boundary、activation routing、secret、deployment value、hardware/protocol specifics 與 release/branch state。

不要把整份 Playbook 複製進每個 project；只在 project governance 保留薄型 adoption／routing layer，project-specific truth 留在 project 自己的 canonical surface。

## License

MIT
