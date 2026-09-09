# cnfjlhj/completion-learn

- Source: `cnfjlhj/completion-learn`
- Reviewed revision: `66a91d56578976d7183381ac9be9c6e9130e24cf`
- Source tree: `b7c765cc4b155b8680484b72daa0d478796198bd`
- License: MIT
- Source role: external post-completion learning / capability-sedimentation / tool-evolution-routing reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps materially with existing Playbook concerns around:

- task completion not automatically proving durable capability;
- persistence/admission being separate from observation/recommendation;
- explicit promotion before tentative learning becomes reusable policy/tooling;
- preventing one-off incidents from hardening into system rules;
- distinguishing existing-owner improvement from genuinely new capability boundaries;
- post-completion evidence review;
- lowest-sufficient durable residue rather than replaying a whole session;
- explicit user/project authority before chaining additional mutation.

Its implementation is much narrower and more human-learning oriented. `completion-learn` is a completion-only debrief skill organized as `Self → Collaboration → Tool`. This Playbook is primarily an engineering-governance system; maintainer learning must therefore translate the idea into repository authority/evidence semantics rather than copy the human self-improvement framing.

## 2. Same failure mode, different architecture

### Completion ≠ capability retained

The strongest external idea is the explicit separation among:

- `mostly assisted performance`
- `partial internalization`
- `durable capability gain`

The skill uses this private judgment to decide what kind of next drill is appropriate. A task can succeed while most of the judgment still came from scaffolding, tooling, or the current interaction.

This maps directly to an important Playbook distinction:

> **one successful execution under strong prompting or live maintainer guidance does not prove that the Playbook itself now carries the capability.**

For Playbook maintenance, a useful translation is:

- **assisted compliance** — behavior succeeded because the current prompt/chat supplied substantial missing guidance;
- **partial canonicalization** — some reusable contract exists, but behavior still depends materially on extra scaffolding;
- **durable Playbook capability** — fresh-session behavior can be recovered from current canonical routing/owners with the expected evidence and authority boundaries.

The Playbook already uses fresh-session behavioral evaluation and immutable-revision evidence to separate current-chat success from durable contract behavior. `completion-learn` independently reinforces that distinction and gives it a compact mental model.

### Reduced-support and transfer tests

The skill does not end with generic advice. Its `Next deliberate practice` intentionally removes one layer of support or moves to a nearby transfer task:

- mostly assisted → user performs one small step independently before tool help;
- partial internalization → same bottleneck, human-first/tool-second;
- durable gain → nearby transfer task rather than exact repetition.

Translated to Playbook behavioral evaluation, this suggests a useful distinction between:

- **same-fixture regression** — does the exact rule now pass the scenario that originally failed?;
- **reduced-scaffolding check** — does the rule still work when extra explanatory prompting is removed and only canonical routing remains?;
- **near-transfer check** — does the same principle hold on a different but semantically adjacent scenario?

This could improve evidence quality for high-risk governance changes without claiming model “learning” across sessions.

### Completion-only trigger

`completion-learn` explicitly refuses to auto-trigger mid-task and requires the task to be complete enough for an honest retrospective. If completion is unclear, it stops.

This aligns strongly with the Playbook's separation between active execution state and post-task learning/promotion. A debrief that runs while evidence is still evolving risks promoting temporary explanations, provisional fixes, or current-session tactics before completion/reconciliation has stabilized them.

A useful Playbook-side invariant is therefore:

`active task evidence → completion/reconciliation → maintainer learning review → possible promotion`

not:

`interesting observation during execution → immediate canonical rule/tool mutation`.

### Sedimentation audit before creating a reusable skill

The external `skill-sedimentation` checklist asks whether the workflow repeated, is likely to recur, has a clear boundary, overlaps an existing skill, has a concrete verifier/checklist/artifact, and would reduce future ambiguity/context/operator error.

It prefers:

- no new skill when the pattern is situational;
- extend an existing skill when the behavior is adjacent to an existing trigger boundary;
- a new skill only when the workflow is stable, reusable, and clearly distinct.

This closely matches the Playbook's Independent Retrieval Intent Gate, Information Surface Responsibility, Deterministic Enforcement Admission Gate, and Follow-up/New Work Gate. The Playbook is more conservative about evidence: “repeated twice inside one task” is useful local evidence but should not by itself prove cross-project/general capability admission.

### Optimize existing boundary before adding another surface

The tool-evolution notes distinguish:

- optimize an existing skill without changing its boundary;
- extend an existing skill;
- add a complementary skill;
- do nothing.

The source's preferred order emphasizes improving an existing surface before proliferating new ones.

That aligns with the Playbook's context architecture: new durable artifacts/surfaces should exist only when they form an independent retrieval intent and clear responsibility boundary. “The current rule underperforms” does not automatically mean “create another owner.”

### Recommendation versus mutation

The source explicitly says low-confidence or one-off patterns should stop at recommendation. Its tool-routing note allows automatic chaining only when the session already authorizes autonomous improvement, the candidate is concrete, and the smallest next change is obvious.

The Playbook should preserve its stricter authority model:

- recommendation does not create admitted work;
- generic “autonomous improvement” language is insufficient if current project Task/Stage, repository write scope, or governance mutation authority does not cover the change;
- external skill routing cannot create new canonical policy or durable obligation by itself.

The transferable principle is the same: **diagnosis before mutation, and recommendation is a valid terminal state.**

## 3. Existing maintainer-zone relationship

The current maintainer zone already implements a closely related flow:

`observation / external idea / suspected bug → maintainer evidence → bounded comparison / behavioral evidence → conclusion → optional canonical promotion`

A maintainer dossier itself is not capability evidence, admitted work, policy, implementation, or validation authority. This already prevents the main failure `completion-learn` is designed to avoid on the tooling side: a vivid completed task immediately hardening into a system change.

The external reference therefore does **not** show that a new canonical “learning layer” is missing. Its value is mainly in sharpening promotion evidence:

1. ask whether the successful outcome was assisted or durable;
2. test with less scaffolding or near-transfer where material;
3. prefer existing semantic owners before new surfaces;
4. allow `no change` / `recommendation only` as successful outcomes.

## 4. External implementation patterns worth further evidence

These are external patterns, not whole-Playbook absence claims.

### A. Assisted-performance versus durable-capability classification

A lightweight internal classification before promotion may prevent maintainers from treating one successful runtime interaction as proof that canonical policy is sufficient.

### B. Reduced-support validation

Removing one layer of prompt/runtime guidance after a successful run can test whether the canonical contract itself carries the behavior.

### C. Near-transfer validation

A semantically adjacent fresh scenario can distinguish memorized fixture compliance from generalized rule application.

### D. Completion-gated learning

Learning review begins only after completion/reconciliation is stable, reducing the chance of sedimenting provisional execution state.

### E. “No new skill” as an explicit positive outcome

The source makes non-codification a normal result rather than a failure to improve the system. This is valuable for preventing policy/surface accretion.

## 5. Useful expression / UX patterns

- `task completed ≠ capability gained` is a compact warning against overclaiming durable improvement.
- `mostly assisted / partial internalization / durable gain` gives a small vocabulary for evidence strength.
- `Next deliberate practice` is framed as a test, not encouragement.
- `Self → Collaboration → Tool` delays tool mutation until upstream human/collaboration causes are considered.
- `Candidate / Why it repeats / Best home / Boundary / Next action` is a compact sedimentation-review shape.
- `Stop at recommendation` is a first-class routing outcome.
- `optimize existing → extend existing → complementary skill → no change` encourages boundary discipline before new-surface proliferation.

## 6. Claims and limitations requiring caution

- The reviewed repository is primarily a skill/prompt/reference package; no formal behavioral-evaluation harness or run corpus was established in the bounded review.
- The three residue categories are judgment heuristics, not deterministic measurable states.
- Human capability internalization is not directly equivalent to AI fresh-session behavioral reliability; the Playbook should translate the concept into observable canonical-routing/eval evidence rather than anthropomorphize model learning.
- A workflow repeating twice within one task is not sufficient universal evidence for cross-project policy/skill admission.
- The source's `Self` axis includes emotional/attention/judgment reflection that may be useful to an individual but should not become repository governance by default.
- Automatic tool chaining under “session already authorizes autonomous improvement” is broader than this Playbook's repository/task/write authority model and should not be imported as-is.

## 7. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Assisted-vs-durable classification pilot** — after one governance behavior succeeds, classify whether success relied on current-chat scaffolding, canonical rule + extra prompting, or canonical routing alone. Compare classification against later fresh-session BEH results.
2. **Reduced-scaffolding BEH variant** — for one recently fixed BEH scenario, rerun with the same canonical authority but remove explanatory wording that merely restates the expected policy. Check whether behavior still holds.
3. **Near-transfer BEH variant** — preserve the same rule/authority and grading semantics but alter the domain details so the agent must apply the principle rather than echo fixture language.
4. **Completion-gated promotion fixture** — present a compelling mid-task lesson before final reconciliation, then change the final evidence. Verify the maintainer flow does not promote the provisional lesson early.
5. **No-change sedimentation review** — take several completed maintainer investigations and explicitly classify `existing owner update / new surface / behavioral fixture / implementation / recommendation-only / no change`; measure whether explicit `no change` reduces unnecessary surface growth.
6. **Existing-owner-first routing experiment** — compare “create a new procedure/surface” against “optimize/extend current owner” for repeated failures and measure retrieval cost, duplication, and behavioral improvement.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

The source independently reinforces a principle that is already central to this Playbook's current evidence discipline: **successful task completion is weaker evidence than durable fresh-session behavior recovered from canonical authority.**

The strongest transferable refinement is an **assisted-compliance → reduced-scaffolding → near-transfer** evidence ladder for selected high-risk behavioral-rule changes. This would complement, not replace, the existing Behavioral Evaluation MVP. It should first be tried as bounded evaluation methodology rather than added as a universal rule or framework.

The second useful refinement is making `recommendation-only / no change` an explicit successful outcome of maintainer learning review. The current maintainer zone already semantically allows this; the external source suggests that naming the outcome may help resist unnecessary rule/tool accumulation.

The source does not justify a universal post-task debrief, a new canonical learning database, or automatic skill evolution. The Playbook's current maintainer-zone promotion boundary is already the stronger authority architecture.

Do not install `completion-learn`, create new canonical surfaces, or modify current policy solely from this reference.

## Revisit trigger

Revisit if:

- a governance rule appears to pass only when the launch prompt heavily restates the desired behavior;
- exact BEH fixtures pass but adjacent scenarios still fail;
- maintainers repeatedly infer durable Playbook capability from one guided success;
- completed investigations routinely produce new rules/surfaces despite weak recurrence evidence;
- provisional mid-task lessons are repeatedly promoted before final completion evidence stabilizes;
- the maintainer-zone promotion flow needs a clearer explicit terminal state for `recommendation only` or `no change`.