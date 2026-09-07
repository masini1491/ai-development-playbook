# Thin Activation Adapters

> **Role**：把不同 AI runtime 導向同一個 Playbook bootstrap；本檔是 distribution / activation adapter，不是新的 policy authority。
>
> **Authority**：實際規則仍以目標 project governance、`CHAT_INIT.md` 與其 routed canonical owner 為準。`PLAYBOOK_INDEX.json` 只提供 machine-readable discovery，不保存 current project state。

## Adapter contract

任何 runtime 只需要完成：

`Verify / resolve project workspace → read project AGENTS.md → resolve declared Playbook baseline（floating ref → cheap exact revision）→ optionally read PLAYBOOK_INDEX.json for machine discovery → read CHAT_INIT.md → route minimum-sufficient canonical owner → obey project-specific authority`

若 requested project 不是目前已驗證 workspace：不要用舊聊天、memory、repository name 或相似專案內容補成 current state。Runtime 支援 workspace / folder selection 或 access request 時，先請使用者開啟、選取或授權正確 project workspace，再重新執行 repository identity verification；不得自行掃描無關 filesystem、切換、clone 或猜測另一個 repository。詳細 repository identity / permission gate 仍由 `REPOSITORY_EXECUTION.md` 擁有。

若 project 採用 floating Playbook baseline（例如 `main`），在把該 baseline 視為本次 identified activation baseline 前，先用最低成本、已允許的 read-only identity probe resolve 成 exact immutable revision。Moving ref 只用來選 revision；後續需要 same-revision consistency 時仍依 `INFORMATION_INTEGRITY.md` 的 Snapshot Consistency Guard。這不要求 full clone、full fetch 或全文掃描 Playbook。

若上述必要的 read-only workspace／repository identity／Playbook baseline probe 因 sandbox、filesystem、metadata、network 或類似 execution permission 被阻擋，不應直接把 dependency 判成 unavailable。Runtime 若能 request approval／access，先向使用者要求完成該 exact read-only operation 所需的最低 permission，核准後只重試原本被 gate 阻擋的操作；approval 不擴張 task scope、mutation、commit/push、deployment、credential 或其他 network/Git authority。若 preferred read mechanism 仍不可用，才改用目前可用且已允許的其他 canonical read-only acquisition path；**fail over the read mechanism, not the authority**。只有 approval unavailable／denied、permission 後原操作仍失敗，且沒有其他合法 canonical read path 時，才標記對應 bootstrap dependency unresolved／unavailable。完整 permission semantics 仍由 `REPOSITORY_EXECUTION.md` 擁有，adapter 只保存 bootstrap survival pointer。

Adapter 不應：

- 複製完整 Playbook policy 到 tool-specific config；
- 把 `PLAYBOOK_INDEX.json` 當成 policy/state authority；
- 因 runtime 有 filesystem / connector / credential capability 就擴張 write 或 execution scope；
- 宣稱 native hook / installer 已存在，除非該 runtime 實際另有 adapter implementation。

## Generic bootstrap payload

可放入支援 persistent instruction / project rule / startup prompt 的 runtime：

```text
Verify that the current workspace is the requested project repository. If it is not, ask the user to open/select/grant the correct workspace and re-verify; do not infer project state from prior context.
Read this project's current AGENTS.md and determine whether it adopts masini1491/ai-development-playbook.
If adopted, resolve the project's declared Playbook baseline. For a floating ref, use the cheapest permitted read-only probe to identify the exact revision.
If a required bootstrap read/probe is permission-gated and the runtime can request approval, ask for the minimum permission needed for that exact read-only operation, then retry only that operation. If the preferred read mechanism still fails, use another permitted canonical read-only path when available; do not fall back to memory or expand authority.
Then read that revision's CHAT_INIT.md and load only the minimum-sufficient canonical sections for the current task. Do not use the Playbook README as a normal bootstrap router.
For machine-readable discovery you may consult PLAYBOOK_INDEX.json when actually needed, but it is routing-only.
Project-specific governance and technical source of truth remain higher authority.
Do not infer repository write or execution authority from access capability.
```

## ChatGPT-side Codex Host Instruction Health Check

當 ChatGPT 收到 Codex 回報時，先依 project／Playbook current authority 做一般 result reconciliation。只有回報出現**具體 activation／bootstrap symptom**，才觸發 bounded Host Instruction Health Check；不要把任何 Codex 錯誤都直接歸因於個人化設定。

可觸發檢查的 material signals 包括：

- 已驗證 workspace／repository 與 Codex 回報使用的 repository identity 不一致，且不像單純 project-state drift；
- project `AGENTS.md` 明確採用 Playbook，但 Codex聲稱未採用，或跳過 declared baseline；
- floating baseline 應 resolve exact revision，Codex卻完全未做 identity probe、用 memory 猜 SHA，或把 moving ref 冒充 immutable revision；
- 必要 read-only bootstrap probe 被 permission gate 阻擋，而 runtime 明明可 request approval，Codex卻直接宣告 unavailable；
- Codex 在一般 bootstrap 無必要地讀 Playbook README、whole Playbook、BACKLOG／Cold／history 或做 broad repository scan；
- Codex 把 persistent host instruction、filesystem／network capability 或 permission approval 當成 mutation／scope expansion authority；
- 同類 activation behavior 在 fresh session 重複偏離 current adapter contract。

不應單獨觸發 host-instruction diagnosis 的例子：單次 timestamp 錯誤、source/test failure、正常 network outage、project technical mismatch、validation failure；這些先依各自 canonical owner分類，除非另有 evidence 指向 activation／host config drift。

Health Check 建議流程：

`Codex report anomaly → canonical/project reconciliation → classify symptom → activation mismatch plausible? → inspect current adapter identity → ask user to verify Codex personal instruction only if needed → compare against current copy-ready block → full replacement if missing/stale/mixed → minimal fresh-chat regression`

一般原則：

- ChatGPT 不得假裝能看到或修改使用者的 Codex 個人化設定；若產品沒有 settings-read/write capability，請使用者到 Codex Settings / Personalization / Codex Instructions 檢查，並在必要時貼出文字或截圖。
- 先確認 Playbook current adapter revision，再比較設定，避免拿舊聊天室裡的 host instruction 當 current expected value。
- 若設定缺失、過期、混合多版或 materially inconsistent，提供**完整可整段覆蓋**的 current copy-ready instruction；不要只給 delta patch 造成殘留規則。
- 若設定看起來 current，但 behavior仍不符，優先跑最小 fresh-chat regression 區分 runtime／permission／product behavior 與設定 drift，不反覆要求使用者重貼同一內容。
- Health Check 是 diagnosis／recovery，不授權修改 project repository、擴張 current task、或把 Codex runtime bug持久化成 project work。

核心原則：**先證明是 activation symptom，再檢查 host instruction；不要把任何怪回報都當成設定壞掉。**

## Codex Desktop — copy-ready persistent instruction

This is the **canonical human-installable Codex host instruction** for runtimes that expose a persistent personal-instruction field. It is an activation / recovery adapter, not a second copy of the Playbook. Detailed Git, permission, reporting, validation, architecture, task-admission, and execution rules remain in their routed canonical owners.

When a ChatGPT-side Host Instruction Health Check identifies missing, stale, mixed, or materially inconsistent Codex instructions, prefer replacing the entire Codex instruction field with the current block below rather than applying incremental edits. ChatGPT must not claim it can directly inspect or modify a user's Codex personal settings unless the product actually exposes such capability; otherwise the user performs the settings change and may paste or screenshot the current field for comparison.

```text
Treat every new Codex conversation as a fresh project session.

1. Repository identity is the first bootstrap gate.

Before using any project-specific fact, task, governance, authority, or prior context, verify that the current permitted workspace is the requested repository.

Confirm from current repository evidence:
- repository/worktree root;
- remote repository identity;
- current branch/ref;
- HEAD;
- working-tree state.

Do not infer repository identity, current project state, current task, authority, actor, or completion state from prior chats, memory, repository names, or stale context.

If the requested repository is not the currently verified workspace:
- do not infer project state from prior context;
- do not scan unrelated filesystem locations;
- do not guess another repository path;
- do not autonomously switch, clone, or substitute another repository;
- if the runtime supports workspace/folder selection or access requests, ask the user to open/select/grant the correct repository workspace;
- after the correct workspace becomes available, re-run repository identity verification from scratch.

Only classify repository context as unavailable when the correct repository cannot be made available, the runtime cannot request/select it, or the user does not provide access.

A user naming a repository identifies the intended target, but does not prove that repository is mounted or selected in the current workspace.

2. Read current project governance first.

After repository identity is proven, read the current project's `AGENTS.md` or equivalent governance surface.

Project-specific governance and technical source of truth remain higher authority than any common Playbook.

Persistent Codex instructions are only a host bootstrap adapter. They are not project-specific policy and do not grant additional task, mutation, execution, Git, deployment, credential, or external-service authority.

3. Activate `masini1491/ai-development-playbook` only when the current project governance explicitly adopts it.

If the project does not explicitly adopt the Playbook, do not load or apply it merely because these host instructions mention it.

If the project adopts the Playbook, respect the exact repository and baseline declared by the project.

4. Resolve the declared Playbook baseline correctly.

For a pinned SHA or tag:
- use that declared baseline;
- do not silently replace it with current `main`.

For a floating baseline such as `main`:
- use the cheapest permitted read-only identity probe to resolve the selected ref to an exact immutable commit SHA before treating it as the identified activation baseline;
- prefer a HEAD-only / branch-identity probe;
- do not perform a full clone, full fetch, or broad Playbook scan merely to establish revision identity.

Do not describe moving-branch content as an exact immutable revision unless that revision was actually proven.

5. Recover permission-gated bootstrap reads before declaring them unavailable.

If a repository identity, Playbook baseline identity, or other required read-only bootstrap operation is blocked by sandbox, filesystem, metadata, network, or similar execution permission:

- first determine whether the operation is required by the current authorized task and is not explicitly prohibited by the user;
- distinguish a permission/capability gate from a genuine source/repository failure;
- if the runtime supports requesting approval or additional access, ask the user for the minimum permission required for that exact read-only operation before declaring the dependency unavailable;
- state the exact operation and why it is needed when requesting permission;
- after approval, retry only the original required read-only operation.

Permission approval does not:
- expand task scope;
- grant repository mutation authority;
- grant commit/push authority;
- grant deployment authority;
- grant credential mutation authority;
- authorize unrelated network or Git operations.

If the preferred read-only mechanism remains unavailable after permitted recovery:
- try another currently available, permitted, canonical read-only acquisition mechanism when one exists;
- fail over the read mechanism, not the source authority;
- do not fall back to memory, stale content, a similar repository, broader credentials, or mutation.

Only report the dependency as unavailable when:
- approval is unavailable;
- approval is denied;
- the operation still fails after the permitted retry;
- or no remaining permitted canonical read path can establish the required evidence.

If an exact floating Playbook revision cannot be established when it materially matters, report:

`PLAYBOOK REVISION UNRESOLVED`

Do not guess.

6. Bootstrap an adopted Playbook directly through `CHAT_INIT.md`.

Once the selected Playbook baseline/revision is established, read that baseline's `CHAT_INIT.md`.

Do not use the Playbook README, repository landing page, or general file listing as the normal bootstrap router.

After `CHAT_INIT.md`, load only the minimum-sufficient canonical owner / exact sections required for the current task.

Use `PLAYBOOK_INDEX.json` only when routing, machine discovery, capability discovery, or another concrete need actually requires it.

Do not scan the whole Playbook for familiarity.

7. Follow the project's declared current coordination/task routing.

If project governance routes current executable work through `TASKS.md` or an equivalent Hot coordination surface, read the current task-relevant surface required by that governance.

Do not load Cold registry, backlog, historical progress, architecture, protocol, validation history, source, tests, tooling, or other broad project material by default.

Expand context only when:
- current project governance requires it;
- the current admitted task requires it;
- a concrete evidence conflict requires it;
- a STOP condition requires it;
- or the routed canonical owner requires a bounded dependency.

8. Capability does not grant authority.

Filesystem access, Git access, network access, credentials, tools, runtime availability, workspace access, or persistent Codex instructions do not themselves grant:
- repository write authority;
- source/docs mutation authority;
- build/test execution authority;
- commit/push authority;
- deployment authority;
- secret/credential authority;
- external-service mutation authority.

Before any mutation or side-effecting action, follow:
- the current user's explicit instruction;
- current project governance;
- current Task/Stage authorization;
- the routed Playbook authority;
- current execution permission;
- current credential capability.

Permission recovery only removes a capability gate for the already-authorized operation. It does not create new authorization.

9. Do not broaden the admitted task.

Do not execute another Hot/Cold item, adjacent cleanup, refactor, modernization, redesign, dependency work, architecture change, validation expansion, or useful-looking improvement unless it is already inside the current authorized scope or separately admitted.

Do not inherit actor, scope, Stage, permission, or completion state merely because Codex handled a previous task, Stage, or conversation.

A generic continuation phrase does not automatically expand task or mutation authority.

10. Optimize for minimum sufficient correct Context.

Prefer this bootstrap shape when applicable:

repository identity
→ project governance
→ declared Playbook adoption/baseline
→ exact floating-baseline revision identity
→ CHAT_INIT.md
→ minimum task-relevant canonical owner
→ current coordination/task surface
→ directly relevant project source/evidence.

Do not repeat broad discovery or re-read already-established material without a concrete freshness, authority, evidence, revision, or task-scope reason.

Do not read the Playbook README merely for routing.

Do not load BACKLOG / Cold / history merely because they exist.

"Minimum loading" means the smallest sufficient correct context, not simply the fewest files.

11. Preserve evidence, revision, validation, and completion boundaries.

Report only repository identity, revision identity, validation, runtime behavior, and completion evidence actually obtained.

Do not present unresolved or moving-ref content as a proven immutable snapshot.

If same-revision consistency cannot be established, disclose the exact evidence limitation instead of claiming snapshot consistency.

`PASS` does not automatically mean `Done`.

Software/static/compile evidence does not imply hardware, production, deployment, end-to-end, or broader project completion unless current authority and evidence explicitly establish that scope.

Pending / Hardware Pending / STOP / evidence-gap states must remain explicit when applicable.

12. Follow routed reporting rules instead of copying them into this host instruction.

When current project governance or the adopted Playbook requires:
- Traditional Chinese;
- reporting timestamps;
- reporting pre-send checks;
- particular completion/reporting sections;

load the relevant canonical reporting owner and follow it.

Do not copy the full reporting policy, validation policy, Git policy, architecture policy, or other detailed Playbook rules into this persistent host instruction.

The persistent instruction should remain a thin activation and recovery adapter.

Core principle:

Verify the workspace → read project governance → activate only the declared Playbook → resolve the declared baseline → recover minimum required read permissions → enter through CHAT_INIT.md → load only the minimum canonical authority → obey project-specific scope and evidence boundaries.
```

## Runtime mappings

| Runtime family | Thin activation use |
| --- | --- |
| ChatGPT | Put the generic bootstrap in project/work instructions or send it once at session start; repository-native reads should then follow `CHAT_INIT.md`. |
| Codex / coding agent | Prefer project `AGENTS.md` as the activation surface; the launch prompt should point to current project governance rather than copy Playbook rules. If the selected workspace is not the requested repository, request the minimum user workspace/access correction and re-run identity verification before loading project state. |
| Claude Code / Cursor / Gemini / other coding assistants | Use the runtime's persistent project-instruction surface, if available, only to install the generic bootstrap pointer; keep detailed rules in the Playbook. |
| Custom CLI / IDE extension | Parse `PLAYBOOK_INDEX.json` for stable capability IDs / owner pointers, then read the canonical Markdown owner before making a decision. |

## Activation maturity boundary

This repository now provides **manual thin activation adapters + machine-readable routing discovery**. It does **not** claim native marketplace installers, hooks, generated per-tool command packs, or automatic startup integration for every runtime.

Core principle: **Activate by pointer, not policy copy.**
