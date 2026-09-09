# Maintainer Synthesis — Learned-Rule Promotion / Self-Correction

> **Maintainer-only evidence synthesis.** This file is not a canonical policy owner, capability claim, task queue, behavioral-eval result, or implementation authority. It exists only because several independently reviewed references now show the same stable retrieval intent: how a Playbook maintainer should decide whether an observed lesson deserves durable promotion.

## Sources reconciled

This synthesis reconciles these bounded reference dossiers:

- `awslabs-aidlc-workflows.md`
- `NeoLabHQ-context-engineering-kit.md`
- `cnfjlhj-completion-learn.md`
- `obra-superpowers.md`

All remain `REFERENCE-ONLY`. Their upstream mechanics, terminology, prompts, runtimes, and product assumptions are not imported by this synthesis.

Current Playbook authority remains outside `maintainer/`. The existing maintainer-zone invariant still governs:

`observation / external idea / suspected bug → maintainer evidence → bounded comparison / behavioral evidence → conclusion → optional promotion through normal governance`

## Stable cross-source pattern

Across the reviewed systems, the repeated failure mode is the same:

> **A successful task, plausible reflection, repeated observation, or persuasive reviewer conclusion can be mistaken for durable system knowledge too early.**

The sources address that failure with different mechanisms:

- **AI-DLC** — tentative stage learning is surfaced, explicitly kept/rejected, scoped, conflict-checked, persisted, and applied only from a later workflow boundary.
- **Context Engineering Kit** — reflection is separated from curation and durable memory; proposed memory is checked for evidence, stability, redundancy, conflict, and actionability before persistence.
- **completion-learn** — task completion is separated from retained capability; reduced-support or transfer exercises test whether the apparent learning survives with less scaffolding; `recommendation only / no change` is a valid terminal state.
- **Superpowers** — high-risk procedure text can be behaviorally hardened RED→GREEN: observe the bypass before editing the rule, then rerun the same pressure scenario and close the actual loophole rather than editing from intuition alone.

These independent patterns strongly converge on one maintainer principle:

**Reflection is evidence generation, not promotion. Promotion should happen only after a bounded curation step proves the lesson is stable enough, correctly owned, non-duplicative, authority-safe, and—when behavior is the claim—supported by suitable fresh-session evidence.**

## Proposed maintainer evidence model

This is a **research model only**, not a new canonical contract.

A candidate lesson can be reasoned about through six distinct questions:

### 1. Completion gate — is the source event stable enough to learn from?

Do not sediment a lesson merely because it appeared during execution.

Prefer:

`active evidence → completion / reconciliation → learning review`

If the final evidence is still changing, keep the observation in maintainer evidence or investigation state. Mid-task explanations are especially vulnerable to later root-cause correction.

### 2. Residue strength — what exactly succeeded?

A successful run can have different evidentiary strength:

- **Assisted compliance** — behavior depended materially on current-chat instruction, maintainer coaching, copied expected behavior, or runtime scaffolding not owned by canonical Playbook routing.
- **Partial canonicalization** — a canonical owner exists and contributes materially, but extra non-canonical scaffolding still appears necessary.
- **Durable Playbook behavior** — a fresh/bounded session recovers the rule through current canonical routing and performs the expected behavior without depending on hidden prior-chat trajectory.

This classification should remain scope-qualified. It does not imply model training or permanent learning.

### 3. Curation gate — is the lesson worth persisting at all?

Check:

- materiality: would recurrence matter?;
- recurrence/stability: is this more than a one-off?;
- evidence quality: what observation or eval supports it?;
- counter-explanation: could the failure come from routing, runtime, capability, permission, environment, or model variance instead of policy wording?;
- redundancy: does an existing canonical owner already express the principle?;
- retrieval value: would persistence reduce future ambiguity/context cost enough to justify another artifact or rule?;
- false-positive risk: could a generalized rule block valid work?

A strong review can legitimately end with:

- `NO CHANGE`
- `RECOMMENDATION ONLY`
- `MORE EVIDENCE NEEDED`

Those are successful maintainer outcomes, not failed self-improvement.

### 4. Owner gate — where would a durable result belong?

Prefer, in order:

1. **existing owner clarification/repair** when the semantic responsibility is already correct;
2. **existing owner extension** when the same retrieval intent legitimately broadens;
3. **behavioral scenario/evidence** when the main uncertainty is whether existing wording changes behavior;
4. **deterministic enforcement** only when the invariant passes the existing deterministic-admission criteria;
5. **new durable surface** only when an independent retrieval intent and clear responsibility boundary genuinely exist;
6. **no persistence** when reuse value is weak.

Do not create a second authority surface merely because the current one underperformed once.

### 5. Behavioral evidence gate — if the claim is behavioral, what test is sufficient?

For material judgment/procedure changes, the reviewed references suggest an evidence ladder:

**A. RED / baseline failure**

When practical, capture the actual failure before strengthening the rule. This distinguishes a real behavioral gap from speculative wording improvement.

**B. Same-fixture regression**

After the change, rerun the fixed scenario with the same authority, premise, stimulus, and observable criteria.

**C. Reduced-scaffolding check**

Remove prompt text that merely restates the desired policy. Confirm the agent still finds and applies the canonical owner through normal routing.

**D. Near-transfer check**

Change domain details while preserving the same rule semantics and grading contract. This tests whether the result is broader than memorized fixture wording.

**E. Pressure variant when justified**

For discipline rules that are likely to fail under time/sunk-cost/"just continue" pressure, add a controlled pressure variant without silently changing the core scenario identity.

Not every rule needs all five levels. Existing Behavioral Evaluation admission/cost rules still apply; use the lowest sufficient evidence for the risk.

### 6. Activation boundary — when does the new durable rule take effect?

A clean stability boundary reduces self-modifying-session ambiguity.

The strongest cross-source candidate is:

**A newly promoted general rule should normally affect the next fresh workflow/session, not retroactively redefine the authority contract of the execution that generated it.**

Exceptions may exist for an explicitly authorized immediate bug/policy correction, but the maintainer should distinguish:

- correcting current canonical truth because evidence proves it wrong now;
- learning a generalized future rule from the completed incident.

Those are not the same mutation.

## Why this is not yet a canonical Playbook change

The current Playbook already contains most of the required semantic defenses:

- maintainer zone is pre-canonical and non-routable by default;
- observation/recommendation/admitted-work separation;
- Task Identity / Revision and Follow-up/New Work gates;
- Information Surface Responsibility and Independent Retrieval Intent;
- Deterministic Enforcement Admission Gate;
- Behavioral Evaluation MVP with fixed revisions and PASS/FAIL/INCONCLUSIVE;
- fresh-session/canonical-evidence discipline;
- current authority versus historical/evidence separation.

The external research therefore does **not** demonstrate a missing fundamental governance layer.

The unresolved question is narrower:

> Would an explicit maintainer curation/promotion UX and a more deliberate behavioral evidence ladder reduce premature promotion and guided-success overclaiming enough to justify additional canonical procedure text or tooling?

That question requires evidence before policy mutation.

## Consolidated evidence candidates

These candidates replace several overlapping per-source ideas for synthesis purposes; the original dossier candidates remain preserved in their source files.

1. **Promotion dry-run pilot** — take one real maintainer candidate and produce a non-mutating preview containing: candidate lesson, source evidence, residue-strength classification, competing explanations, intended owner, redundancy/conflict check, authority impact, proposed activation boundary, and terminal decision. Measure whether this catches a promotion error or merely adds ceremony.
2. **RED→GREEN→reduced-scaffolding BEH pilot** — use one material procedure rule with an observed failure. Preserve the baseline failure, patch only the relevant canonical owner, rerun exact fixture, then rerun without explanatory launch scaffolding.
3. **Near-transfer behavioral pilot** — apply the same rule to a semantically adjacent cold-start scenario with different surface details. Grade against the same principle rather than exact wording.
4. **No-change outcome audit** — sample completed maintainer dossiers/investigations and explicitly classify their correct terminal state. Check whether naming `NO CHANGE / RECOMMENDATION ONLY` reduces unnecessary policy/tool/surface growth.
5. **Next-session activation experiment** — compare immediate mid-session generalized-rule activation with next-fresh-session activation for reproducibility, authority clarity, and surprise cost.

None of these is admitted work merely because it appears here.

## Lowest-sufficient next experiment

The strongest next experiment is **Promotion dry-run pilot**.

Reason:

- it directly exercises the new maintainer zone;
- it can reuse existing evidence without changing canonical policy;
- it tests whether the recurring external idea—explicit curation before persistence—adds real error detection;
- it can terminate with `NO CHANGE`, preserving low ceremony if it proves unhelpful;
- it does not require a new runtime engine, database, skill framework, or universal post-task debrief.

A sensible pilot target would be a future real candidate where the maintainer is already considering canonical promotion, rather than manufacturing a synthetic rule solely to exercise the process.

## Current synthesis conclusion

The cross-source evidence is now strong enough to justify this **maintainer retrieval synthesis**, but not strong enough to justify a canonical rule change.

Current best maintainer mental model:

`finish/reconcile → classify evidence strength → curate → choose existing owner / eval / deterministic check / new surface / no change → promote only through normal governance → prefer next-session activation for generalized learned rules`

And for high-risk behavioral procedure changes:

`observe real failure (RED) → focused canonical change → exact regression (GREEN) → reduced scaffolding → near transfer / pressure only when risk justifies`

The central invariant remains:

**A lesson can be useful without becoming policy; a successful run can be real without proving durable Playbook capability; and self-correction is strongest when promotion itself is evidence-gated.**

## Revisit trigger

Revisit this synthesis if:

- a real promotion candidate is put through the dry-run pilot;
- a reduced-scaffolding or near-transfer BEH produces materially different results from the exact fixture;
- maintainers repeatedly promote observations that later prove runtime/routing-specific;
- `NO CHANGE` outcomes measurably reduce surface growth without hiding real defects;
- canonical owners begin to need explicit wording for promotion/activation semantics after repeated evidence rather than one external-reference review.