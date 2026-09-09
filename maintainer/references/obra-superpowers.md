# obra/superpowers

- Source: `obra/superpowers`
- Reviewed revision: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- Source tree: `22c18dc41f9ac4c19a1af4fc516f94292c72e44b`
- Release represented by reviewed manifest: `6.3.0`
- License: MIT
- Source role: external procedure / skills / behavioral-enforcement / subagent-workflow reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## Existing Playbook relationship

This Playbook already has a `Superpowers` compatibility profile in `INTEROPERABILITY.md`. That profile classifies Superpowers primarily as an **execution methodology**: installation or automatic skill triggering does not create Task authorization, expand repository/credential/deployment authority, or make skill-produced outputs canonical by itself.

This dossier does not replace that current interoperability mapping. It reviews the current upstream implementation for maintainer lessons, behavioral-evaluation patterns, context/runtime trade-offs, and possible future evidence candidates.

## 1. Already-covered concerns

The reviewed source overlaps strongly with existing Playbook concerns around:

- requirements/design before implementation;
- root-cause-first debugging;
- TDD and falsifiable tests;
- fresh verification before completion claims;
- bounded delegation and independent review;
- lowest-sufficient model selection for child roles;
- context isolation through fresh subagents;
- durable recovery state for long agent workflows;
- progressive procedure loading;
- user/project governance precedence over reusable methodology;
- behavioral evaluation for judgment/procedure rules.

The architectural difference is that Superpowers packages these concerns as **mandatory automatically triggered skills** across coding-agent runtimes. This Playbook defines authority and routing contracts first and treats any installed skill system as optional execution methodology unless the target project's governance explicitly requires it.

## 2. Same failure mode, different architecture

### Process documentation tested like software

The most important independent pattern is in `writing-skills`: skill creation/editing is explicitly modeled as TDD for process documentation.

The workflow is:

`pressure scenario → observe baseline failure/rationalization → write or change skill → rerun scenario → close loopholes → re-verify`

Its mapping is direct: pressure scenario = test case, skill document = production code, baseline violation = RED, compliance with the skill = GREEN, and rationalization hardening = refactor.

This strongly resembles this Playbook's `Behavioral Evaluation MVP`, which exists specifically because deterministic validators cannot reliably prove judgment/procedure behavior. The difference is admission cost: Superpowers declares an Iron Law requiring a failing behavioral test for every new or edited skill, while this Playbook intentionally requires behavioral evaluation only when materiality, repeated failure risk, or decision value justifies the cost.

The transferable idea is therefore **RED-before-rule-change for high-risk behavioral contracts**, not a universal requirement that every prose edit spawn a behavioral run.

### Pressure testing and rationalization capture

Superpowers recommends testing discipline-enforcing skills under combined pressures such as time, sunk cost, fatigue, or social pressure, recording the exact rationalizations an agent uses and editing the skill to close those loopholes.

This is a useful refinement candidate for Playbook behavioral evaluation. Current BEH scenarios define premise, stimulus, expected/forbidden behavior, and observable evidence; pressure variants could test whether a rule survives realistic incentives to bypass it without changing the canonical scenario identity.

Pressure variation should remain controlled. A comparison run must still fix the Playbook revision, material premise, core stimulus, and observable criteria rather than turning every run into a different scenario.

### Trigger metadata must not become a shortcut specification

`writing-skills` documents a particularly relevant failure mode: when a skill description summarized the workflow, an agent sometimes followed the description instead of reading the full skill and therefore missed required steps. The recommended description contains **trigger conditions only**, not a compressed workflow.

This independently reinforces the Playbook's `Thin Routing Metadata` principle:

`routing metadata should help find the owner; it should not become a second semantic owner.`

The important maintainer question is broader than skills: can a capability/index/router summary accidentally become “good enough” for the model to skip the canonical owner? If yes, adding more helpful summary text may reduce rather than improve behavioral reliability.

### Mandatory skill discovery versus minimum-sufficient routing

`using-superpowers` says that if there is even a small chance a skill applies, the agent must invoke it before any response/action, including clarification or repository exploration. Relevant skills are mandatory once selected.

That is intentionally much more aggressive than this Playbook. This Playbook keeps external workflows condition-triggered, does not load an integration merely because it exists, and explicitly distinguishes installation/automatic activation from execution authority.

Do **not** generalize the “1% chance → load/invoke” rule. It would increase default context/tool ceremony and conflict with minimum-sufficient retrieval. The useful part is instead the clear precedence statement: direct user/project instructions outrank reusable skills.

### Process-depth classification

The current `brainstorming` skill uses three paths:

- `Spike` — cheap feasibility probe, throwaway result;
- `Bounded` — small existing-flow change, short in-chat design;
- `Architectural` — full alternatives/design/spec/plan workflow.

Hidden complexity can only ratchet toward the heavier path. All three paths retain a human approval gate before implementation.

This provides a concrete **ceremony budget** implementation. It is comparable to this Playbook's Minimal Clarification Gate and lowest-sufficient workflow principle, but Superpowers' universal approval-before-implementation rule is more restrictive than this Playbook. In Playbook projects, already-authorized bounded work does not necessarily require a fresh human approval for every implementation action.

The transferable concept is: **ceremony may scale with complexity while material authority boundaries do not disappear merely because a task is small.**

### Plan granularity and semantic task boundaries

`writing-plans` defines a task as the smallest unit that owns its own test cycle and is worth an independent review gate. Setup/config/docs are folded into the task whose deliverable needs them; tasks are split only when a reviewer could meaningfully reject one while approving another.

This is a useful contrast to arbitrary “2–5 minute step” decomposition. The semantic definition — independent deliverable + independent reviewability — is more transferable than the literal time estimate.

The Playbook already separates Task Identity / Revision from wording and bookkeeping changes. A future planning heuristic could use independent reviewability as evidence for whether something is truly a separate execution unit, without making Superpowers plan files canonical.

### Fresh-subagent task execution

`subagent-driven-development` dispatches fresh implementers with isolated context, followed by task review that covers spec compliance and code quality, plus a broad final branch review. It tells the coordinator to construct only the context the child needs rather than inheriting the parent session history.

This aligns with the Playbook's child-routing and Progressive Context principles. The Playbook remains stricter on delegation admission: a child must first represent a legitimate bounded subtask; different model/context alone is not delegation authority.

Superpowers also batches multiple tiny same-shape edits into one child instead of mechanically spawning one child per plan item. This is a useful example of **semantic delegation granularity** rather than agent-count maximization.

### Durable execution ledger for compaction recovery

Superpowers explicitly warns that conversation memory may be lost after compaction and that coordinators have re-dispatched already completed work. Its SDD workflow therefore creates a per-plan git-ignored ledger/workspace under `.superpowers/sdd/<plan>/`, records completion/fix rounds/decisions, and tells resumed controllers to trust the ledger plus Git history over their own recollection.

This is adjacent to the Playbook's Session Compaction / Rehydration Contract, but the layers differ:

- Playbook checkpoint = conversation recovery/routing aid;
- Superpowers ledger = execution-runtime scratch state for one implementation plan.

A project choosing an execution ledger would still need a clear authority boundary: the ledger should not silently become canonical requirements, durable backlog, or completion evidence merely because it survived context loss.

### “Rulings, not stalls” versus authority-sensitive clarification

Superpowers SDD tells the controller to decide many plan ambiguities itself, record a ruling, and keep going; it names only a narrow set of stop conditions such as destructive/security-sensitive operations, outside-worktree side effects, or a plan so broken that every path is a guess.

This is a deliberate autonomy/productivity choice and should **not** be imported wholesale. The Playbook's Minimal Clarification Gate still requires clarification/STOP when uncertainty materially changes task identity, scope, authority, permission, completion criteria, or safety boundaries.

A useful narrower pattern is the explicit ruling record: when the agent is legitimately authorized to choose among implementation details, recording `decision + reason + cost if wrong` can make reversible judgment visible without turning every choice into a user interruption.

### Child model routing

Superpowers recommends explicit child-model selection by role:

- cheap model for mechanical, tightly specified work;
- standard model for integration/judgment;
- strongest model for architecture and broad final review;
- escalation after repeated failed fix rounds.

It also warns that omitted model overrides can silently inherit an unnecessarily expensive parent model.

This is closely aligned with `CODEX_EXECUTION.md`'s lowest-sufficient child routing. The Playbook currently adds two important constraints that should remain:

1. model switching itself is not delegation authority;
2. final reporting must disclose materially distinct requested child model/reasoning profiles and preserve the effective-profile observability boundary.

Superpowers provides useful independent evidence for role-sensitive child routing, but not a reason to replace the Playbook's current root/child authority and transparency contract.

### Verification and debugging discipline

`verification-before-completion` requires fresh evidence for each completion claim and explicitly says an agent's success report is insufficient without independent diff/verification. `systematic-debugging` requires evidence/root-cause investigation before fixes, a minimal single-hypothesis test, and escalation back to architectural questioning after repeated failed fix attempts.

These patterns substantially overlap with the Playbook's `Evidence → Root Cause → Focused Patch → Targeted Validation`, canonical completion read-back, and failure/retry discipline. They are reinforcing external evidence rather than newly discovered missing capabilities.

## 3. Behavioral-evidence maturity boundary

The upstream README says skill-behavior tests use the external `superpowers-evals` drill harness, cloned locally into `evals/`, while plugin/infrastructure tests live in this repository under `tests/`.

At the reviewed revision:

- this repository contains substantial runtime/plugin integration test surfaces under `tests/`;
- `writing-skills` specifies the RED/GREEN pressure-scenario methodology;
- the bounded review did **not** inspect or validate the external `superpowers-evals` corpus/runs;
- therefore this dossier does not claim that every current skill has independently verified behavioral coverage or quote a universal pass rate.

Commit/release prose mentioning micro-tests is useful provenance but is not a substitute for fixed-scenario run evidence when making formal behavioral claims.

## 4. External capabilities / implementation maturity worth further evidence

These are external implementation patterns, not whole-Playbook absence claims.

### A. TDD-style behavioral hardening for procedure text

Baseline agent failure is captured before the rule is written, and exact rationalizations are used as regression targets.

### B. Trigger-only discovery metadata

Skill descriptions are deliberately prevented from becoming compressed workflow substitutes, based on observed shortcut behavior.

### C. Runtime execution ledger

Long multi-child workflows maintain durable scratch identity/progress independently of conversation memory.

### D. Role-sensitive explicit child-model routing

Child profile is chosen from task judgment level, with explicit escalation and a warning against accidental expensive inheritance.

### E. Multi-runtime packaging maturity

The reviewed repository contains adapters/manifests for multiple coding-agent ecosystems. The Codex manifest at this revision identifies version `6.3.0`, points at the shared `skills/` directory, and explicitly declares `hooks: {}` to suppress unintended Codex hook auto-discovery.

This is useful distribution-engineering evidence but does not change the Playbook's current activation-maturity claims.

### F. Semantic task/review unit definition

A plan task is defined by an independently testable deliverable and meaningful reviewer boundary, not only by elapsed time or checklist size.

## 5. Useful expression / UX patterns

- `Spike / Bounded / Architectural` gives users a simple ceremony-depth vocabulary.
- “Hidden complexity upgrades the path” provides a clear one-way ratchet when scope turns out larger than expected.
- Pressure scenarios explicitly test rules under the incentives most likely to break them.
- Rationalization tables pair common bypass thoughts with the governing correction.
- Skill description = trigger only; body = procedure keeps routing separate from policy content.
- Fresh implementer + independent reviewer separates implementation trajectory from review judgment.
- Per-plan ledger makes context-loss recovery deterministic enough to avoid re-running completed tasks.
- `decision + why + cost if wrong` is a useful form for reversible autonomous rulings.

## 6. Patterns not suitable for direct generalization

- “1% chance a skill applies → invoke it” would over-load context/tooling in a Playbook designed for minimum-sufficient routing.
- Mandatory brainstorming/user approval before every code change is a Superpowers workflow choice, not a universal Playbook authority requirement.
- Mandatory behavioral RED/GREEN testing for every prose edit would be too costly; the Playbook's Behavioral Evaluation Admission criteria should remain risk/value based.
- Automatic continuation through ambiguities must not override Playbook clarification/STOP requirements for scope, authority, permission, safety, or completion boundaries.
- “Most capable model for final review” is a useful heuristic, not a universal requirement; lowest-sufficient model still depends on actual risk/complexity.
- Fresh child per task is not automatically optimal; tightly coupled work, trivial same-shape edits, or coordination cost can make another execution shape better.
- A git-ignored SDD ledger is scratch execution state, not automatically project canonical truth or durable admitted work.
- Plugin installation and skill auto-activation do not expand execution authority; current `INTEROPERABILITY.md` already owns this invariant.

## 7. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Trigger-summary shortcut behavioral fixture** — compare a router/skill description that contains only trigger metadata against one that summarizes key procedure steps. Measure whether agents skip the canonical owner or collapse multi-step behavior into the summary.
2. **Pressure-variant BEH pilot** — add controlled pressure variants to one existing material BEH scenario while fixing the same canonical revision, premise, expected/forbidden behavior, and grading criteria. Measure whether the rule survives time/sunk-cost/“just do it” pressure.
3. **RED-before-policy-hardening experiment** — for one repeatedly failing procedure rule, first capture a fresh-session failure at the current rule, then change wording/procedure, then rerun the exact scenario. Compare this with policy changes made from intuition alone.
4. **Execution-ledger recovery pilot** — on one genuinely long multi-child Codex Stage, keep a non-authoritative per-Stage scratch ledger of child/task state and compare post-compaction duplicate-work/recovery errors against conversation checkpoint alone.
5. **Semantic task-boundary experiment** — compare checklist/time-based task splitting against `independently testable deliverable + independently reviewable boundary` on one multi-step adopter change.
6. **Autonomous-ruling boundary fixture** — give an agent an implementation ambiguity that is safe/reversible in one case and authority/scope-changing in another. Verify it records a ruling and continues only in the first case, but asks/stops in the second.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

Superpowers does not currently show that this Playbook needs a universal mandatory skill layer. The Playbook already has a Superpowers interoperability profile and intentionally keeps external skill activation separate from project authority.

The strongest transferable idea is **behavioral TDD for high-risk procedure changes**: when a rule is being strengthened because agents actually bypass it, capture the bypass first, then prove the revised rule changes behavior under the same scenario. This is already compatible with `Behavioral Evaluation MVP`; the open question is whether selected high-risk rule changes should use RED/GREEN more systematically.

The most novel retrieval lesson is **trigger-only routing metadata**. Superpowers reports an observed failure where descriptive metadata summarizing the workflow became a shortcut that caused agents to skip the full procedure. That directly reinforces the Playbook's Thin Routing Metadata design and deserves a bounded behavioral fixture before any routing-surface hardening is considered.

The SDD execution ledger is also worth testing for very long multi-child Codex runs, but only as non-authoritative scratch recovery state. It should not be added globally unless real adopter evidence shows conversation checkpoint + Git evidence is insufficient.

Do not install Superpowers, make all Playbook procedures mandatory skills, add universal approval gates, or change canonical policy solely from this reference.

## Revisit trigger

Revisit if:

- agents repeatedly follow router/index summaries without loading the canonical owner;
- material behavioral rules are edited repeatedly without clear evidence that the wording changes behavior;
- BEH scenarios pass in neutral prompts but fail reliably under realistic pressure/rationalization;
- long multi-child Codex executions duplicate completed work after compaction or session recovery;
- adopter task plans repeatedly split work at arbitrary checklist boundaries that make review/validation ownership unclear;
- child model routing repeatedly inherits expensive root profiles despite bounded mechanical subtasks.