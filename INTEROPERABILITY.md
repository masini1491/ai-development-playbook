# External Workflow Interoperability

This file is the canonical owner for how the Playbook interprets and governs **external AI engineering workflows, spec systems, skill runtimes, and governance frameworks** after a project chooses to use them.

It does **not** replace upstream documentation, mirror external product behavior, install integrations, or grant any runtime capability. Upstream repositories remain authoritative for their own commands, file formats, lifecycle rules, and supported integrations. This file only defines the Playbook-side semantic and authority mapping.

## Scope / Activation

Read this file only when the current project actually adopts, evaluates, or needs to reconcile an external workflow／skill／agent-governance system. It is not an always-on dependency.

Typical triggers:

- the project uses an external spec/change workflow;
- an installed skill runtime can automatically trigger execution procedures;
- project governance imports or depends on an external agent contract;
- multiple AI engineering systems coexist and their artifacts or permissions must be reconciled;
- a review asks whether adopting an external system changes Playbook authority, loading, evidence, or completion semantics.

Do not load this file merely because a supported external tool exists in the ecosystem.

## Generic Interoperability Contract

External adoption adds a capability or workflow; it does not erase the Playbook's authority distinctions.

Core invariants:

- **External artifact existence ≠ project authority.** Project-specific governance decides whether an external artifact is authoritative and for what scope.
- **Installation / availability ≠ task authorization.** A plugin, skill, command pack, CLI, hook, or marketplace installation does not create work by itself.
- **Automatic activation ≠ execution authority expansion.** A runtime may automatically select a relevant skill, but that does not widen the authorized Task／Stage, repository write scope, credential capability, or external-service permission.
- **External task list ≠ new durable obligation outside its parent authorization.** A tool may decompose already-authorized work; decomposition does not independently enlarge project commitment or scope.
- **External workflow status is scope-qualified.** `go`, `PASS`, `Converged`, `archived`, `complete`, or equivalent status means only what the upstream workflow and project integration contract define; it does not automatically prove repository, hardware, production, user-observed, or Playbook completion.
- **External result ≠ canonical completion evidence by default.** Results remain subject to the project's validation contract, evidence requirements, canonical read-back, and `INFORMATION_INTEGRITY.md` guards.
- **External routing metadata ≠ current project truth.** Generated commands, indexes, manifests, registries, or installation metadata help discovery／activation; they do not become project factual authority unless explicitly assigned that role.
- **Adoption does not force default loading.** External artifacts should be loaded according to current Task need and their project-assigned semantic class, not merely because they are durable.
- **Role-bounded integration should prefer least-capability surfaces.** 若 external integration 中某 actor 的 assigned responsibility 只需要 read／inspect／plan／review，且 integration surface 能在 capability 層不提供 write／delete／exec／admin 等非必要能力，優先採取較小 capability surface，而不是只靠 Prompt 要求 actor 不使用較大能力。Capability minimization 不取代 project authority，但可縮小 prompt injection、routing error 與 accidental mutation 的 blast radius。
- **External runtime auto-update ≠ previously validated behavior remains current.** 若 external skill／runtime／adapter 可自動更新或其 installed revision 會獨立漂移，先前 version-specific validation 只證明當時實際觀察到的 revision／behavior。當 current decision materially 依賴該 external runtime 的現行行為時，重新建立最低充分 installed／upstream identity 與 relevant current evidence；不得把舊 PASS 永久沿用。

Compact form:

`External adoption / installation ≠ persistence authority ≠ default-load authority ≠ write authority ≠ execution authority ≠ credential capability ≠ completion authority`

## Semantic Mapping Model

When integrating an external system, classify each relevant artifact or capability by its **project role**, not by filename alone.

Useful classes include:

- **Governance prerequisite** — rules the project explicitly makes authoritative before work proceeds.
- **Current canonical candidate** — an external spec or contract the project may designate as current truth for a defined domain.
- **Change / Hot detail** — active proposal, plan, design, delta spec, or task decomposition for current work.
- **Cold / candidate decision input** — assessed idea or future option that has not received current execution authorization.
- **Execution methodology** — reusable skill or procedure that controls *how* authorized work is performed.
- **Evidence / finding** — verification, convergence, review, diagnostic, or other result that informs a decision but does not independently own project truth.
- **Activation / distribution surface** — installer, plugin, hook, generated command pack, or runtime adapter that makes a capability discoverable or invokable.

Project governance may choose a different mapping when it states the relationship explicitly. The Playbook should not guess a stronger authority class from an external tool's reputation, installation state, or filename.

## Compatibility Profiles

The profiles below are **Playbook-side semantic examples**, not mirrors of upstream current state. If an upstream system changes, re-read its current canonical documentation before making a version-specific claim.

### OpenSpec

Typical current surfaces include `openspec/specs/` and `openspec/changes/`.

Playbook mapping:

- `openspec/specs/` can serve as a **Current canonical** requirements/spec surface when project governance explicitly designates it as such.
- `openspec/changes/<change>/` is normally **change intent / Hot detail** for the active change. Proposal, delta specs, design, and tasks describe work toward a future state; their existence alone does not overwrite current canonical truth.
- A change task list may decompose authorized implementation work, but it does not enlarge the parent Task／Stage scope or grant repository／credential authority on its own.
- OpenSpec verification output is **evidence / finding** within its verification scope. It does not automatically satisfy unrelated Playbook validation layers.
- Archive／sync semantics may update the project's designated current spec surface according to OpenSpec's own lifecycle, but the project must already have declared that surface authoritative; the Playbook does not promote it merely because archive occurred.
- A Store or cross-repository planning repository can be a shared planning/source surface, but repository location does not itself determine write, execution, or default-load authority in consuming repositories.

### GitHub Spec Kit

Typical artifacts and workflow stages include constitution, specification, plan, tasks, implementation, convergence, and optional idea assessment.

Playbook mapping:

- A Spec Kit constitution becomes project governance authority only when the project explicitly adopts it in that role. Once adopted, honor its declared scope instead of duplicating its rules into Playbook files.
- Spec／plan／tasks are **task-local planning artifacts**. Their authority is bounded by the parent feature／Task and project governance; generating additional tasks does not independently create broader durable obligations.
- A `go` decision from an idea-assessment workflow is a **decision artifact within that workflow**. It does not by itself grant repository mutation, credential, deployment, or external-service permission. A project may explicitly use that decision as its admission mechanism.
- Convergence findings are **evidence / reconciliation findings**. A `Converged` result is scope-qualified to the artifacts and checks actually compared; it does not automatically prove all Playbook completion or real-world validation requirements.
- Spec Kit installation, extensions, presets, bundles, or generated commands are **activation / distribution surfaces**; they do not change project authority merely by being present.

### Superpowers

Superpowers primarily supplies an execution methodology through composable skills and runtime integration.

Playbook mapping:

- A Superpowers skill is an **execution methodology**, not a source of Task authorization.
- Automatic skill triggering may select *how* to perform already-authorized work; it does not expand repository write scope, credentials, deployment permission, or the user's current goal.
- If project governance explicitly requires a specific skill／procedure, that requirement can become part of the project's execution contract, while the skill still does not create new work outside the authorized scope.
- Skill-produced plans, reviews, test results, or completion reports are **planning/evidence outputs according to their semantic role**; they remain subject to project canonical ownership and Playbook completion/read-back requirements.
- Plugin／marketplace installation and session-start activation are **distribution / activation capabilities**. Runtime activation maturity must not be confused with authority maturity or behavioral correctness evidence.

### Codex with ChatGPT

Codex with ChatGPT（C2C）提供 ChatGPT planning／review 與 Codex execution 之間的 external coordination/runtime integration，包含 bounded control protocol 與 read-only workspace evidence access。

Playbook mapping:

- C2C 在 Playbook 中屬於 `ChatGPT+Codex` collaboration profile 的 **optional external execution / coordination implementation**；它不是第三種 Project AI mode，也不因安裝而改變 `PROJECT_MODES.md` 的 actor topology authority。
- C2C Skill、protocol、setup／repair procedure 屬 **execution methodology / activation surface**。安裝、auto-update、automatic activation 或 protocol state 不會自行建立 Task／Stage authorization、repository write authority、credential authority 或 durable obligation。
- C2C 的 read-only workspace connector／MCP 屬 **data / evidence acquisition capability**。它可讓 planning／review actor 取得 current workspace、Git 與 execution evidence，但 connector capability 本身不授予該 actor repository mutation authority。
- `INIT`、`PLAN`、`EXECUTED`、`HANDOFF`、`DONE` 等 C2C protocol state 是 **coordination state**。其中 `EXECUTED`／agent-reported tests 仍是 execution claim；Playbook completion acceptance 繼續依 current canonical evidence、validation contract 與 required read-back。
- C2C HANDOFF 是 **continuity / rehydration artifact**。它可保存 goal、progress、known issue 與 next step，但 current code／diff／validation truth 仍應由 current workspace 重新取得；handoff 不恢復或擴張 authority。
- C2C 的 control-plane／data-plane separation 與 read-only review surface 可作為 interoperability implementation reference；其特定 message size、iteration limit、ChatGPT Project／connector topology、browser automation、Cloudflare tunnel、OAuth／pairing、repair 流程與 command syntax 仍由 upstream current canonical documentation 擁有，不提升為 Playbook universal policy。
- 若 project 實際採用 C2C，對 version-specific command、runtime、security、setup 或 compatibility claim 應重新讀 current upstream／installed revision；本 profile 只保存 Playbook-side semantic mapping，不鏡像 upstream implementation catalog。

### GSA-TTS Agentic Coding Playbook

The GSA-TTS Agentic Coding Playbook uses a universal behavioral contract plus a project layer, with executable skills and deterministic enforcement mechanisms.

Playbook mapping:

- If a project's own governance declares the GSA universal contract as a prerequisite, treat that dependency as part of **project governance**. Project-specific governance remains the authority for how multiple governance systems are composed.
- Do not copy the external universal contract into local Playbook surfaces merely to make it visible; preserve its upstream ownership and the project's declared resolution path.
- If the active GSA integration requires fail-closed contract availability, Playbook read fallbacks or convenience summaries must not silently weaken that prerequisite.
- GSA skills are **execution procedures** within the authority granted by the project; skill availability does not independently create tasks, credentials, or deployment permission.
- GSA validator／security results are scope-qualified evidence. Preserve the distinction between their checked controls and any additional project-specific Playbook validation or real-world evidence.

## Conflict / Precedence Resolution

The Playbook does not define a universal winner among external systems.

Resolve conflicts in this order:

1. current user instruction;
2. current target repository's project-specific governance and technical source of truth;
3. explicit integration／precedence declarations made by that project;
4. the adopted external system's canonical contract within its declared scope;
5. this Playbook's cross-project baseline;
6. derived summaries, cached copies, prior chat, or memory.

If two same-level external authorities conflict and the project has not defined precedence, STOP at the ambiguity boundary. Do not merge them by convenience or infer precedence from installation order, star count, runtime integration strength, or filename.

## Loading / Retrieval Rules

- Keep external integration semantics condition-triggered; do not add all compatibility profiles to every task's Context.
- Once the external system is known, direct-read the relevant profile section and the minimum upstream canonical source needed for the current claim.
- For version-specific behavior, upstream current canonical documentation is required; this file only provides the Playbook-side semantic mapping.
- Do not mirror large external command catalogs or workflow documentation into this repository. Prefer stable references and local authority mapping.

## Maturity Boundary

This file proves a **normative interoperability contract and compatibility profiles** only.

It does **not** prove:

- native marketplace installation;
- automatic startup hooks;
- generated per-runtime command packs;
- automatic detection of installed external workflows;
- cross-runtime semantic conformance;
- live fresh-session behavioral regression.

Those are separate implementation／activation／validation maturity layers and must be claimed only when corresponding executable evidence exists.

Core principle:

> **Use external systems for the workflow, skills, spec lifecycle, or compliance capability they are good at; use the Playbook to keep authority, loading, permission, evidence, and completion semantics from collapsing together.**
