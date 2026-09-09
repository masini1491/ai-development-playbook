# github/spec-kit

- Source: `github/spec-kit`
- Reviewed revision: `0c8e31ff0a98c362696c2edb6a1bb25a37f68544`
- Source tree: `b21e06610bf7cc11bc7ea128f63b8266605df86e`
- License: MIT
- Source role: external spec-driven development / idea admission / artifact-convergence reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps strongly with this Playbook on separating project principles from task-specific implementation detail, distinguishing requirements from technical plans and executable tasks, clarifying underspecified work before implementation, read-only cross-artifact review, explicit work admission, bounded iteration, and reconciling implementation against intended scope before completion.

Spec Kit is more prescriptive about a particular artifact chain: project constitution → feature spec → implementation plan → tasks → implementation → convergence. This Playbook instead defines generic authority/task/evidence contracts that must fit repositories with many different canonical technical surfaces and project workflows.

## 2. Same failure mode, different architecture

### Idea assessment before work admission

The bundled `assess` extension intentionally sits before SDD. It uses `intake → research → define → shape → decide` and ends in one of three explicit outcomes: `go`, `needs-clarification`, or `kill`. A `go` only hands the result to `speckit.specify`; it does not itself create the implementation spec or write application code. A `kill` is explicitly treated as a successful assessment outcome, not a workflow failure.

This closely matches the Playbook's `Observation ≠ Recommendation ≠ Admitted Work`, Minimal Clarification Gate, Follow-up/New Work Gate, and maintainer-zone promotion boundaries. Spec Kit productizes those semantics as a named pre-delivery pipeline.

A notable strength is that the decision step requires an adequate evidence threshold before `go`, records `unknown` rather than glossing over it, and sends unresolved ideas back to the specific earlier assessment stage that can reduce uncertainty.

### Constitution versus project governance

Spec Kit establishes a project constitution with binding principles. Its plan template has a mandatory Constitution Check before research and a re-check after design. `analyze` treats conflicts with a constitution MUST as CRITICAL, and `converge` also gives constitution MUST violations highest severity.

This resembles the Playbook's project-governance precedence, Task/Stage gates, and canonical policy owners. The important difference is that the Playbook cannot assume every adopter has or should create a single `constitution.md`; existing target-repository governance remains authoritative.

Spec Kit's own constitution also separates amendment from ordinary feature work: changing a principle requires an explicit governance change and propagation to dependent templates/guidance. That is a useful expression of `policy change ≠ task implementation`.

### Requirements, plan, and tasks as different semantic surfaces

Spec Kit explicitly separates:

- `spec.md`: what/why, requirements, stories, success criteria;
- `plan.md`: technical approach and design choices;
- `tasks.md`: executable work breakdown;
- implementation: current code state.

This aligns with this Playbook's information-surface responsibility and Task Identity / Revision rules. Spec Kit's separation is especially useful as an example of preventing implementation detail from prematurely contaminating requirement capture.

However, those artifact roles are project conventions rather than universal semantic authorities. In this Playbook, a target repository may place requirements, architecture, implementation truth, tasks, and evidence elsewhere.

### Read-only pre-implementation reconciliation

`/speckit.analyze` is strictly read-only. It builds requirement/story/task coverage models, checks ambiguity, duplication, underspecification, constitutional alignment, coverage gaps, terminology drift, ordering conflicts, and other inconsistencies, then offers remediation without applying it automatically.

This closely matches the Playbook's bounded review, absence-claim discipline, deterministic-vs-judgment separation, and preference for evidence before mutation. The command also explicitly uses progressive disclosure and a bounded findings count rather than dumping all artifacts into context.

### Implementation convergence without rewriting intent

`/speckit.converge` compares the present codebase against `spec.md`, `plan.md`, and `tasks.md`, with the constitution as governing constraints. It does not edit application code or rewrite existing spec/plan/tasks; when gaps remain, its sole write is an append-only Convergence phase at the end of `tasks.md` with traceable source refs and stable new task IDs.

This is an interesting comparison for the Playbook's Task Identity / Revision Gate and completion reconciliation. When a convergence finding is demonstrably unfinished work already implied by an admitted feature's current canonical intent, appending a remediation task can be treated as closure/revision of existing admitted work rather than unrelated new work.

But the Playbook should retain a stricter boundary: a gap detector must not use “more could be done” or code improvements outside current admitted scope to create durable work. Any analogous mechanism must prove the finding derives from already-authorized intent or separately pass admission.

### Artifact persistence models

Spec Kit does not force one post-change persistence strategy. It names three models:

- flow-back: any artifact may change, then reconcile;
- flow-forward: completed feature artifacts become historical records and later changes get new feature directories;
- living spec: `spec.md` remains the contract and downstream plan/tasks are regenerated or revised.

This is directly relevant to this Playbook's Current Canonical / Historical / Derived / Evidence separation. The useful pattern is making the temporal/persistence model explicit rather than silently assuming every spec or task file keeps the same authority forever.

### Extensions and capability distribution

Spec Kit has a broad extension/preset/bundle ecosystem and 30+ coding-agent integrations. Its README explicitly says community components are independently maintained and should be reviewed before installation.

This reinforces the Playbook's `installation ≠ authority`, external-artifact, and interoperability contracts. Runtime/plugin capability may extend workflows, but it must not silently become project governance or execution authorization.

## 3. External capabilities / implementation maturity worth further evidence

These are external implementation patterns, not whole-Playbook absence claims.

### A. Explicit idea-assessment pipeline with kill as a valid outcome

The `assess` extension gives pre-admission evidence gathering a clear lifecycle and durable decision artifact. It strongly distinguishes “interesting idea” from “approved for specification.”

### B. Cross-artifact coverage analysis

`analyze` maps requirements and acceptance criteria to tasks and reports unmapped requirements/tasks before implementation. This is a mature productized form of requirements-to-work traceability.

### C. Append-only convergence remediation

`converge` creates stable, source-referenced remediation tasks without rewriting existing task history. It is a concrete approach to “implementation drift becomes explicit remaining work.”

### D. Explicit artifact persistence strategy

Naming flow-back, flow-forward, and living-spec modes helps teams decide whether a feature artifact is mutable current truth, historical evidence, or a source that regenerates downstream derivatives.

### E. Governance checks embedded in multiple lifecycle stages

The constitution is checked during planning, artifact analysis, and convergence rather than being loaded once and assumed to remain satisfied.

### F. Progressive, bounded artifact analysis

Both `analyze` and `converge` explicitly load only the minimum high-signal sections needed and bound the assessment to artifact-defined scope. This is independently consistent with the Playbook's minimum-sufficient retrieval goal.

## 4. Useful expression / UX patterns

- `intake → research → define → shape → decide` makes pre-admission evidence work easy to reason about.
- `go | needs-clarification | kill` provides a small explicit decision vocabulary.
- “Killing ideas here is a success, not a failure” reduces pressure to convert every explored idea into work.
- `Constitution Check` before research and after design makes governance compliance a repeated lifecycle check rather than a one-time bootstrap event.
- `analyze` is read-only and asks before remediation, which preserves evidence/mutation separation.
- `converge` writes only append-only, traceable remaining tasks and leaves the file byte-for-byte unchanged when no work remains.
- Stable refs such as `FR-003`, `SC-002`, `US1/AC2`, plan decisions, and constitution principles make remediation provenance inspectable.
- The three persistence models give teams explicit language for how current and historical artifacts evolve.

## 5. Runtime/product-specific patterns not suitable for direct generalization

- `constitution.md`, `spec.md`, `plan.md`, and `tasks.md` are Spec Kit conventions; this Playbook must continue routing to the target repository's actual canonical owners.
- Spec Kit's normal feature lifecycle is intentionally structured; not every engineering task needs a full specify→plan→tasks→implement pipeline.
- A `go` decision from an LLM-driven assessment is still judgment evidence. It cannot replace user/project admission authority when the target repository requires explicit approval.
- Convergence may append tasks automatically inside Spec Kit's feature workflow. A generic Playbook mechanism must first prove those tasks are within already-admitted scope; otherwise Follow-up/New Work Gate still applies.
- Heuristic artifact-to-code coverage and severity classification are not deterministic correctness proofs.
- Constitution MUST conflicts being CRITICAL is valid only because that project's constitution is already established as governing authority; an external or optional framework cannot self-promote to that role.
- Community extensions/presets/bundles and agent integrations are distribution surfaces, not authority sources.

## 6. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Idea-assessment vs current admission UX** — compare Playbook natural-language `Observation ≠ Recommendation ≠ Admitted Work` handling with a compact `intake → evidence → define → options → decide` maintainer/adopter workflow. Measure accidental task admission, unresolved assumptions, and user friction.
2. **Kill-as-success behavioral fixture** — create a fresh-session evaluation where the highest-quality result is rejecting an attractive AI-originated improvement rather than adding it to TASKS. Verify the agent treats rejection/deferment as successful governance.
3. **Requirement-to-task coverage pilot** — on one adopter with stable requirement IDs, compute read-only coverage between canonical requirements and admitted tasks. Measure whether it finds material omissions without creating false “absence” claims.
4. **Convergence-within-scope pilot** — after implementation, derive append-only remediation candidates only from already-admitted intent. Test whether Task Identity / Revision correctly distinguishes closure work from genuinely new work.
5. **Artifact persistence declaration** — evaluate whether projects benefit from explicitly declaring a persistence model (mutable current owner / historical flow-forward / derived-from-owner) for major planning/spec surfaces.
6. **Repeated governance-check experiment** — compare bootstrap-only governance loading with targeted re-checks at plan, pre-implementation review, and completion reconciliation; measure stale-governance violations versus context cost.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

Spec Kit does not demonstrate that this Playbook should adopt a universal spec directory or a mandatory constitution/spec/plan/tasks lifecycle. The Playbook's broader authority model is intentionally more adaptable to existing repositories.

The strongest transferable idea is the **pre-admission decision pipeline**, especially the explicit distinction between `go`, `needs-clarification`, and `kill`, with kill treated as a valid successful conclusion. This is a productized expression of a governance principle the Playbook already owns and could be useful in behavioral evaluation before any canonical mutation is considered.

The second strongest idea is **append-only convergence scoped to existing intent**. It offers a concrete way to preserve task history while turning verified implementation gaps into traceable remaining work. The crucial Playbook-side condition is that such work must be demonstrably contained within current admitted scope; otherwise it is new work and still requires admission.

The artifact-persistence model taxonomy is also valuable. It gives maintainers a useful vocabulary for deciding whether a planning/spec surface is current canonical truth, historical record, or a derived artifact. This may become useful in future adopter guidance if repeated ambiguity appears in real projects.

Do not install Spec Kit, create a universal `specs/` structure, or change canonical Playbook policy solely from this reference.

## Revisit trigger

Revisit if:

- AI-originated improvements are still being accidentally admitted despite current Observation/Recommendation/Admitted Work rules;
- adopter projects repeatedly discover missing requirement coverage only after implementation;
- completion reconciliation repeatedly finds in-scope unfinished work but has no clean durable way to preserve it without rewriting task history;
- teams repeatedly disagree whether specs/plans/tasks are current truth, history, or disposable derived artifacts;
- governance rules are read correctly at bootstrap but later lifecycle stages drift from them.