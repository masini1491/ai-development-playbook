# Thin Activation Adapters

> **Role**：把不同 AI runtime 導向同一個 Playbook bootstrap；本檔是 distribution / activation adapter，不是新的 policy authority。
>
> **Authority**：實際規則仍以目標 project governance、`CHAT_INIT.md` 與其 routed canonical owner 為準。`PLAYBOOK_INDEX.json` 只提供 machine-readable discovery，不保存 current project state。

## Adapter contract

預設 generic route：

`Verify / resolve project workspace → read project AGENTS.md → resolve declared Playbook baseline（floating ref → cheap exact revision）→ optionally read PLAYBOOK_INDEX.json for machine discovery → read CHAT_INIT.md → route minimum-sufficient canonical owner → obey project-specific authority`

A host-specific adapter is optional when the runtime's native instruction discovery already reaches the project's intended canonical bootstrap. Do not retain an adapter merely for historical compatibility.

Retain a host-specific adapter only when it still provides a distinct routing, activation, precedence, or compatibility responsibility that native discovery does not reproduce. Native host support therefore creates a retirement / narrowing trigger, not automatic deletion authority.

### Conditional Activation / Adoption ≠ Activation

**Adoption ≠ unconditional activation。** 若 current project governance 已明確提供 project-native bootstrap／task classifier，用來先判定本次 task 是否需要 shared Playbook governance，runtime 可先走該 project-native gate；若 gate 判定本題不需 Playbook，留在 project-native route，不為了「已採用 Playbook」額外讀 `AGENTS.md`、probe Playbook baseline 或進入 Playbook `CHAT_INIT.md`。只有 gate 判定需要 activate Playbook 時，才讀 current adoption state、resolve declared baseline，並進入上述 generic activation route。

這個 conditional-activation exception 必須來自**目前可驗證的 project governance／bootstrap**，不得由 host instruction、舊聊天、memory、repository shape 或模型自己推測。Project 沒有明確 conditional gate、該 gate 無法 current-read，或本次 task 本身就是 project governance／adoption／mode／repository-maintenance 判斷時，維持 generic `AGENTS.md`-first route。

**Shared reporting 是窄化的 adoption-level exception。** 若 current project governance採用 shared `REPORTING.md` contract，substantive user-facing engineering reply即使在 project-native route中仍遵守該 contract；需要完整規則時只 direct-leaf 到 declared baseline 的 `REPORTING.md`，不因此進入 `CHAT_INIT.md` 或 activate其他 shared owners。Reporting applicability不建立 Task／write／execution／permission／validation authority。

### Bootstrap identity / baseline boundary

若 requested project 不是目前已驗證 workspace：不要用舊聊天、memory、repository name 或相似專案內容補成 current state。Runtime 支援 workspace / folder selection 或 access request 時，先請使用者開啟、選取或授權正確 project workspace，再重新執行 repository identity verification；不得自行掃描無關 filesystem、切換、clone 或猜測另一個 repository。詳細 repository identity / permission gate 仍由 `REPOSITORY_EXECUTION.md` 擁有。

Activation-time baseline responsibility只到「建立本次 identified Playbook revision」：

- project宣告 floating baseline（例如 `main`）時，在首次進入 Playbook `CHAT_INIT.md` 前，以最低成本合法 read-only identity probe把該 ref resolve成 exact immutable revision；Moving ref只負責選 revision，不要求 full clone／full fetch／全文掃描。
- project宣告 pinned SHA／tag時依該 baseline進入；不得因 upstream newer HEAD自行改用新版。
- 只知道「採用 Playbook」但 current project governance尚未提供 baseline時，維持 **baseline unresolved**；不得由 host instruction、舊聊天或本 Playbook自己的 current `main`猜補。
- Activation成立後，同一 session後續的 freshness trigger、verified-context reuse與 selective reload不再由 adapter維護，回 `AI_CONTEXT.md` → `Session-local Verified Context Reuse`；若需要 same-revision validation snapshot，再依 `INFORMATION_INTEGRITY.md` → `Snapshot Consistency Guard`。

若必要的 read-only workspace／repository identity／Playbook baseline probe 被 capability／permission gate 阻擋，adapter只保留 bootstrap survival boundary：先依 `REPOSITORY_EXECUTION.md` 取得該 exact operation 的最低合法 access，必要時依 `CHAT_INIT.md` → `Repository Read Acquisition / Recovery Gate` 切換合法 canonical read path；**fail over the read mechanism, not the authority**。仍無法建立 required current identity時，保持 dependency unresolved／blocked。Permission recovery、credential／scope分層與 acquisition mechanics不在本檔重述。

### Cross-agent host authority boundary

Host／agent-specific instruction surface（例如 `CLAUDE.md`、`GEMINI.md`、Copilot repository instructions、IDE rule 或其他 compatibility adapter）可以讓該 host **discover、read、route、follow** target repository 的 canonical governance；它的存在本身不會改變 target project 的 `Project AI mode`，也不會自動把該 host admission 成 canonical executor。

核心分離：

`Host compatibility ≠ Project AI mode ≠ task authorization ≠ write authority ≠ execution authority ≠ completion authority`

- Compatibility adapter 應只做 bootstrap／handoff pointer；不要複製 method、runtime、retrieval、storage、validation 或 completion policy，避免形成第二份 current-state authority。
- 如果多個 agent-instruction surfaces 同時被 runtime 載入，重疊的 bootstrap text 只視為 **compatibility handoff**，不得因此推導 parallel authority、multiple policy owners 或較高 permission。
- Adapter 應 hand off 到 **target repository 自己目前宣告的 canonical bootstrap／router**。不同 repository 可以有不同 native hot path；不得因某個 shared Playbook 或 host adapter 習慣某一 bootstrap shape，就覆蓋 target repository 的 current route。
- Host 能理解、建議或遵循 canonical governance，不等於該 host 已取得 mutation／runtime execution／credential／deployment authority。真正 actor admission 仍由 current user instruction、project governance、Task／Stage 與 capability gate共同決定。
- Host native behavior 或 adapter wording若與 current canonical governance衝突，以 current canonical authority為準；adapter 必須 narrow／stop，不得發明 fallback來保住 host-specific行為。

核心原則：**Compatibility grants discoverability and routing, not execution admission. Adapter presence must never silently rewrite Project AI mode or repository authority.**

Adapter 不應：

- 複製完整 Playbook policy 到 tool-specific config；
- 把 `PLAYBOOK_INDEX.json` 當成 policy/state authority；
- 因 runtime 有 filesystem / connector / credential capability 就擴張 write 或 execution scope；
- 宣稱 native hook / installer 已存在，除非該 runtime 實際另有 adapter implementation。

## Generic bootstrap payload

可放入支援 persistent instruction / project rule / startup prompt 的 runtime：

```text
Verify that the current workspace is the requested project repository. If it is not, ask the user to open/select/grant the correct workspace and re-verify; do not infer project state from prior context.
If current project governance exposes a project-native bootstrap/task router that explicitly decides whether shared Playbook activation is needed, follow that gate first. Adoption alone does not require Playbook activation for every task. If the gate says Playbook is not needed, stay on the project-native route. Do not invent this exception from memory or host instructions.
If current project governance adopts the shared reporting contract, keep `REPORTING.md` applicable to substantive user-facing engineering replies even on that project-native route; direct-read only that leaf as needed and do not activate other Playbook owners for reporting alone.
Otherwise, or once the project-native gate says Playbook activation is required, read this project's current AGENTS.md and determine whether it adopts masini1491/ai-development-playbook.
If adopted, resolve the project's declared Playbook baseline. For a floating ref, use the cheapest permitted read-only probe to identify the exact revision.
If a required bootstrap read/probe is blocked, recover only the minimum access needed for that exact read-only operation under current project/Playbook authority. If current canonical identity still cannot be established, keep that dependency unresolved; do not fall back to memory or expand authority.
Then read that revision's CHAT_INIT.md and load only the minimum-sufficient canonical sections for the current task. Do not use the Playbook README as a normal bootstrap router.
For machine-readable discovery you may consult PLAYBOOK_INDEX.json when actually needed, but it is routing-only.
Project-specific governance and technical source of truth remain higher authority.
Do not infer repository write or execution authority from access capability.
```

## ChatGPT Cold-start Compatibility Target

For ChatGPT-facing adapter design and regression, the preferred **low-capability cold-start compatibility target** is:

`Free ChatGPT + fresh chat + empty cache + connected GitHub repository access as the sole repository authority acquisition path`

This is a host／product compatibility target, not a Project AI mode definition and not a universal promise about every ChatGPT account or product revision. GitHub availability can vary by plan, workspace, and product surface; if the tested Free ChatGPT surface does not expose connected GitHub repository access, this profile is unavailable on that surface rather than silently substituting another acquisition path.

Target semantics:

- start without prior conversation state, preloaded project Context, warmed runtime cache, or previously materialized repository artifacts;
- establish current repository authority through the connected GitHub repository capability, without making public GitHub HTML/raw URLs, generic Web search, shell Git/clone, Python HTTP, stale memory, or another repository-acquisition mechanism a prerequisite for this regression profile;
- after repository authority is established, use only the additional ChatGPT-native capabilities actually available and materially required by the task, while preserving the same authority, identity, integrity, materialization, execution, and validation contracts;
- richer paid-plan surfaces, Codex, warmed caches, broader connectors, larger Context, or stronger runtimes remain optional acceleration unless a concrete project proves they are materially required;
- a successful run proves compatibility only for the tested product/runtime/repository revision/scenario; it does not establish universal Free ChatGPT capability.

If the core workflow cannot cold-start under this target, classify the blocker before changing the baseline: avoidable workflow dependency, unavailable-but-equivalent transport/materialization path, or genuinely material capability requirement. Do not weaken canonical identity, deterministic execution, validation, or evidence requirements merely to preserve this profile.

This target constrains **repository authority acquisition** for the regression profile; it does not prohibit task-required ChatGPT-native execution/runtime capabilities actually exposed by the tested surface. Repository acquisition, artifact handoff/materialization, runtime execution, and result evidence remain separate capability layers.

Core principle: **Project mode defines actor topology; activation adapters own concrete host/product compatibility targets. Optimize the cold-start baseline for the lowest sufficient verified capability, not for a particular subscription label as authority.**

## ChatGPT — copy-ready custom instruction

ChatGPT 的人類安裝用 persistent Custom Instructions 已獨立成純文字 distribution artifact：

[`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt)

這個 `.txt` 檔案只保存要貼進 ChatGPT Settings / Personalization / Custom Instructions 的完整 thin-bootstrap payload；沒有 Markdown code fence、前言或診斷文字。它是 user-level host adapter，不是 project-specific policy，也不會因被安裝就讓任何 project 自動採用 Playbook。

目前 distribution contract 將唯一 canonical ChatGPT host adapter 維持在 **1,500 characters 以內**。這個上限是 Playbook 的 distribution target，用來覆蓋目前較低容量的 ChatGPT Custom Instructions surface；即使某些 plan／surface 可接受更長 payload，也不另維護 5,000-character expanded variant。產品欄位限制仍屬 product-version-specific installation constraint，不是 Playbook policy authority；若產品限制 materially 改變，重新驗證 adapter／validator，而不是把更多 canonical policy 複製進 host setting。

Loading contract：

- 一般 project bootstrap **不得因為這個檔案存在就讀取它**；
- 只有安裝／更新 ChatGPT Custom Instructions、`ChatGPT Host Instruction Health Check`、設定 drift 比對，或維護這個 distribution artifact 本身時才需要讀取；
- normal project task 仍由 project governance 決定是否採用 Playbook、是否先走 project-native conditional-activation gate、採用哪個 baseline，再在 activation 成立時進 `CHAT_INIT.md`；
- 安裝／更新後使用 **fresh chat regression** 驗證，不把既有聊天室的舊 context 當成 host instruction 已生效的證據。

## ChatGPT Host Instruction Health Check

只有 fresh ChatGPT session 出現具體 activation／bootstrap symptom，才做 bounded Host Instruction Health Check；不要把一般回答錯誤、source/test failure 或單次 wording 差異都歸因於 Custom Instructions。

可觸發檢查的 material signals 包括：

- 未建立 target repository／project current identity 就直接使用 prior chat、memory 或 stale project facts；
- 未讀 current project governance 就自行套用 Playbook；
- current project 有明確 conditional-activation gate，ChatGPT 卻只因「已採用 Playbook」就無條件讀 `AGENTS.md`／probe baseline／載入 Playbook；
- 只知道 project「採用 Playbook」，卻在 declared baseline 尚未建立時自行預設 Playbook current `main`；
- Playbook activation 已依 current project gate 成立，但 fresh chat 跳過 declared baseline／`CHAT_INIT.md`，或無必要 broad-scan README／whole Playbook；
- generic continuation（例如「好，繼續」）把 AI-originated observation 自動升格成 canonical／executable work；
- 把 connector／filesystem／network／runtime capability 或 permission approval 當成 mutation／scope authority；
- 同類 activation behavior 在 fresh sessions 重複偏離 current adapter contract。

Health Check 建議流程：

`Fresh-chat anomaly → canonical/project reconciliation → activation mismatch plausible? → inspect current adapter revision → ask user to verify ChatGPT Custom Instructions only if needed → compare against CHATGPT_CUSTOM_INSTRUCTIONS.txt → full replacement if missing/stale/mixed → minimal fresh-chat regression`

一般原則：

- 除非產品實際提供 settings-read/write capability，ChatGPT 不得假裝能直接看到或修改使用者的 Custom Instructions；必要時請使用者開啟設定、貼出文字或截圖。
- 先確認 Playbook current adapter revision，再比對 host setting；不要拿舊聊天室中的 payload 當 current expected value。
- 若設定缺失、過期、混合多版或 materially inconsistent，使用 [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) **整段覆蓋**，不要做 delta patch。
- 若設定 current 但 behavior 仍偏離，優先用最小 fresh-chat regression 區分 product/runtime behavior 與設定 drift。
- Health Check 只做 diagnosis／recovery，不建立 project task、擴張 mutation authority，或把 runtime anomaly 自動持久化成 repository obligation。

核心原則：**先證明是 fresh-session activation symptom，再檢查 host instruction；project governance／declared baseline 仍是實際專案 authority。**

## ChatGPT-side Codex Host Instruction Health Check

當 ChatGPT 收到 Codex 回報時，先依 project／Playbook current authority 做一般 result reconciliation。只有回報出現**具體 activation／bootstrap symptom**，才觸發 bounded Host Instruction Health Check；不要把任何 Codex 錯誤都直接歸因於個人化設定。

可觸發檢查的 material signals 包括：

- 已驗證 workspace／repository 與 Codex 回報使用的 repository identity 不一致，且不像單純 project-state drift；
- project `AGENTS.md` 明確採用 Playbook，但 Codex 聲稱未採用，或跳過 declared baseline；
- floating baseline 應 resolve exact revision，Codex 卻完全未做 identity probe、用 memory 猜 SHA，或把 moving ref 冒充 immutable revision；
- 必要 read-only bootstrap probe 被 permission gate 阻擋，而 runtime 明明可 request approval，Codex 卻直接宣告 unavailable；
- Codex 在一般 bootstrap 無必要地讀 Playbook README、whole Playbook、BACKLOG／Cold／history 或做 broad repository scan；
- Codex 把 persistent host instruction、filesystem／network capability 或 permission approval 當成 mutation／scope expansion authority；
- 同類 activation behavior 在 fresh session 重複偏離 current adapter contract。

不應單獨觸發 host-instruction diagnosis 的例子：單次 timestamp 錯誤、source/test failure、正常 network outage、project technical mismatch、validation failure；這些先依各自 canonical owner 分類，除非另有 evidence 指向 activation／host config drift。

Health Check 建議流程：

`Codex report anomaly → canonical/project reconciliation → classify symptom → activation mismatch plausible? → inspect current adapter identity → ask user to verify the effective Codex global instruction surface only if needed → compare against CODEX_DESKTOP_INSTRUCTIONS.txt → full replacement if missing/stale/mixed → minimal fresh-session regression`

一般原則：

- ChatGPT 不得假裝能看到或修改使用者目前 effective Codex global instruction。Codex 現行文件化的 global discovery 在 `$CODEX_HOME`（預設 `~/.codex`）先讀 `AGENTS.override.md`，否則讀 `AGENTS.md`；必要時請使用者貼出實際生效檔內容或等價設定證據。不要用舊版 UI 路徑或舊聊天猜測 effective surface。
- 先確認 Playbook current adapter revision，再比較設定，避免拿舊聊天室裡的 host instruction 當 current expected value。
- 若 effective global instruction 缺失、過期、混合多版或 materially inconsistent，提供 [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) 的**完整內容作為整段覆蓋來源**；不要只給 delta patch 造成殘留規則。
- 若 effective global instruction 看起來 current，但 behavior 仍不符，優先跑最小 fresh-session regression 區分 runtime／permission／product behavior 與設定 drift，不反覆要求使用者重貼同一內容。
- Health Check 是 diagnosis／recovery，不授權修改 project repository、擴張 current task、或把 Codex runtime bug 持久化成 project work。

核心原則：**先證明是 activation symptom，再檢查 host instruction；不要把任何怪回報都當成設定壞掉。**

## Codex — copy-ready global host instruction

Codex 的人類安裝用 global persistent host instruction 已獨立成純文字 distribution artifact：

[`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt)

這個 `.txt` 檔案只保存 thin host-adapter payload；它本身不會被 Codex 自動載入，也不是 project-specific policy。依目前文件化的 Codex instruction discovery，預設安裝目標是 `$CODEX_HOME/AGENTS.md`（通常為 `~/.codex/AGENTS.md`）；若同層 `AGENTS.override.md` 存在，Codex 會優先使用 override。臨時 regression 可使用 override，但正式安裝／drift 比對必須先確認哪個 global file 實際生效。這個 install surface 是 product-version-specific compatibility contract；若 upstream discovery semantics materially 改變，重新驗證 adapter，而不是保留舊 UI 假設。

使用方式：開啟該 `.txt` → 全選 → 複製 → 完整取代目前 effective global instruction file 的 payload。不要把新版 append 到舊長版 instruction，以免多版規則同時生效。

Loading contract：

- 一般 project bootstrap **不得因為這個 distribution artifact 存在就讀取它**；
- 只有安裝／更新 Codex global host instruction、Host Instruction Health Check、effective-surface drift 比對，或維護這個 distribution artifact 本身時才需要讀取；
- `CODEX_DESKTOP_INSTRUCTIONS.txt` 是 human-installable distribution artifact，不是新的 policy authority；其語意仍由本檔與 routed canonical owners 擁有。

這個分離讓 `ACTIVATION_ADAPTERS.md` 保持 adapter semantics / diagnosis owner，而 `.txt` 只負責安全、明確的人工作業複製邊界。

## Runtime mappings

| Runtime family | Thin activation use |
| --- | --- |
| ChatGPT | For persistent user-level setup, install [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) as a thin host adapter. If current project governance exposes a project-native conditional-activation gate, follow it before loading Playbook state; otherwise use the generic bootstrap. Actual Playbook adoption/baseline still comes from current project governance before Playbook `CHAT_INIT.md`. |
| Codex / coding agent | For persistent user-level setup, install [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) through Codex's documented global `AGENTS.md` instruction chain; project `AGENTS.md` remains the project-level activation/governance surface. If the selected workspace is not the requested repository, request the minimum user workspace/access correction and re-run identity verification before loading project state. |
| Claude Code | When current Claude Code native instruction discovery already reaches the project's intended bootstrap through `AGENTS.md`, no separate `CLAUDE.md` shim is required. Keep or add `CLAUDE.md` only for a distinct Claude-specific bootstrap override, compatibility handoff, or routing / precedence distinction. This Playbook repository intentionally keeps one because root `AGENTS.md` is maintainer governance while ordinary task routing should enter through `CHAT_INIT.md`. Exact native discovery / configuration behavior remains upstream-owned and version-specific. |
| Cursor / Gemini / other coding assistants | Use the runtime's persistent project-instruction surface, if available, only to install the generic bootstrap pointer; keep detailed rules in the Playbook. |
| Custom CLI / IDE extension | Parse `PLAYBOOK_INDEX.json` for stable capability IDs / owner pointers, then read the canonical Markdown owner before making a decision. |

## Activation maturity boundary

This repository now provides **manual thin activation adapters + copy-ready ChatGPT/Codex host payloads + machine-readable routing discovery**. It does **not** claim native marketplace installers, hooks, generated per-tool command packs, or automatic startup integration for every runtime.

Core principle: **Adoption does not require unconditional activation. Activate by current project gate and pointer, not by policy copy or host-level assumption.**