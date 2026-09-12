# Validation Discriminative Power / Oracle Independence｜Cross-project maintainer candidate

> **Maintainer-only candidate.** This file records pre-canonical research and a future review trigger. It is not a Playbook capability claim, canonical validation policy, admitted task, formal eval result, or execution authorization.
>
> **Current obligation: `NONE`.** Presence here does not create Hot/Cold work. Canonicalization requires a later evidence-based maintainer decision through normal governance.

## Candidate question

Current Playbook validation guidance already covers deterministic-enforcement admission, target/backend coverage, evidence tiers, verifier lifecycle, behavioral evaluation, and controlled fault injection. A remaining seam question is whether the Playbook should explicitly require a validation check to demonstrate enough **discriminative power** to distinguish a material defect from an intentional implementation/text change.

Candidate formulation:

> **A validation check should be able to name the material defect, invariant violation, or behavior regression that would make it fail. Expected results should be independently derived enough from the subject under test to distinguish that defect. Source-text or structural assertions are legitimate when that source/structure is itself the declared contract; they do not prove downstream runtime or agent behavior merely because required wording exists.**

Possible short name:

`Validation Discriminative Power / Oracle Independence Gate`

## Current classification

- Gap assessment: **PARTIAL SEAM GAP — HIGH CONFIDENCE**.
- External adoption state: **REFERENCE-ONLY**.
- Canonicalization decision: **WAIT**.
- Current obligation: **NONE**.

This candidate is retained for maintainer learning only. It should not appear in ordinary Playbook capability inventory, normal routing, adopter project context, or release-distributed Playbook content.

## Why it may matter

A verifier can be falsifiable yet still provide weak behavioral evidence. Examples include checks that:

- fail only when an intentional constant or wording decision changes;
- calculate the expected result with the same logic or helper as the subject under test;
- assert that source text contains a required phrase and then overclaim downstream behavior;
- assert on a mock/test double rather than the behavior of the real component;
- protect implementation shape while sleeping through the material defect the test is supposed to catch.

The missing question is not merely "can this test turn red?" but:

> **What meaningful break would this check catch, and is its oracle sufficiently independent to distinguish that break?**

## Primary public reference: `obra/superpowers`

Reviewed released baseline during the 2026-09-12 maintainer study:

- repository: `obra/superpowers`
- released/default branch baseline: `main`
- reviewed released commit: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0 at review time)
- development branch observed separately: `dev` at `5940bd8d48fe9488056a1f6718ed2670dc9596c0`
- relevant development reference: `skills/test-driven-development/writing-good-tests.md`
- relevant file blob at reviewed `dev`: `d3c4482fd30b4f9084bb61545fe73939a7502c28`

Relevant principles observed:

- "Every test names the break it catches."
- "Every test exercises the real thing."
- derive expectations independently rather than using the code under test as its own oracle;
- distinguish a real behavioral regression detector from a mere change detector;
- test scripts/config/agent instructions through controlled behavior when downstream behavior is the actual claim;
- use a mutation thought-check to ask which realistic production defect would make an existing test fail.

The useful lesson is narrower than importing Superpowers testing methodology wholesale:

> **Falsifiability alone is insufficient. A test can fail on intentional change while remaining unable to detect the material bug it supposedly protects against.**

### Evidence lineage note

Superpowers explicitly generalized part of this discipline from `kenn-io/agentsview` / `testing-without-tautologies`. Therefore those repositories are not counted as independent corroborating evidence merely because they are separate GitHub artifacts. The lineage remains useful because Superpowers subsequently evolved the guidance after observing that "can fail" still allowed low-value change detectors.

## Reconciliation with current Playbook

At the reviewed Playbook baseline `f229c6382b7373abb0542c5a22d68ed95fb21642`, existing canonical coverage already includes:

- `DEBUG_VALIDATION.md` → **Deterministic Enforcement Admission Gate**: asks whether an invariant is observable, deterministic, materially valuable, low-risk to enforce mechanically, and clearly owned;
- **Validation Coverage Integrity**: `exit 0` does not prove that the intended implementation/backend/runtime actually participated;
- **Real-runtime / backend contract validation**: mock/static evidence cannot impersonate a runtime contract it did not exercise;
- **Verifier Contract Lifecycle**: passing verifier does not imply complete coverage, and failing verifier does not automatically prove a source bug;
- **Behavioral Evaluation MVP**: separates expected behavior, forbidden behavior, and observable evidence, with cold-start controls against coaching;
- **Controlled Fault Injection** and evidence-tier boundaries where applicable.

These rules answer adjacent questions:

- Should this invariant be automated?
- Did validation exercise the intended target/runtime?
- Is the verifier still aligned with the current contract?
- Did an agent exhibit the expected/forbidden behavior?

The seam not yet stated explicitly is:

> **Does the check's assertion/oracle actually distinguish the material defect from an intentional implementation/text change?**

## Current repository evidence

A bounded review of the Playbook's current Python test modules did **not** identify an urgent existing failure pattern requiring immediate canonical repair.

Observed examples are generally behavior-oriented rather than source-presence-only:

- `tests/test_playbook_check.py` uses synthetic repository fixtures and expects actual routing/closure diagnostics;
- `tests/test_adoption_doctor.py` mutates synthetic `AGENTS.md` / coordination inputs and asserts diagnostic outcomes;
- `tests/test_behavioral_eval.py` tests the deterministic responsibilities the evaluator actually claims to own, while repository documentation explicitly avoids promoting metadata/schema validation into semantic behavioral PASS.

Therefore this candidate is currently preventive methodology refinement, not evidence that the existing 58-test suite is materially tautological or falsely green.

## Important boundary: text/structure can be the contract

Do **not** generalize the external slogan "behavior, not text" into a universal ban on structural assertions.

For a documentation-as-contract repository, text or structure may itself be the declared machine-consumed invariant. Legitimate examples include:

- a routing manifest must point to an existing canonical owner;
- a required heading/path/schema field must exist;
- a routing-only metadata field must retain its declared authority classification;
- a Markdown/internal reference must resolve.

Those checks become weak only when they are used as a proxy for a different claim.

Example distinction:

- legitimate: `PLAYBOOK_INDEX.json` declares owner `DEBUG_VALIDATION.md` → verify target/heading exists;
- insufficient behavioral proof: `DEBUG_VALIDATION.md` contains wording equivalent to "not observed != absent" → therefore a fresh agent will correctly preserve `UNKNOWN` semantics under pressure.

The second claim belongs in behavioral evaluation, not a source-text presence assertion.

## Risks of premature canonicalization

Do not promote this candidate merely because it is intuitively good testing advice. Premature expansion could create validation ceremony such as requiring every trivial structural check to have mutation infrastructure, negative fixtures, or an elaborate independent-oracle framework.

Specific risks:

- governance inflation around otherwise simple deterministic invariants;
- treating mutation testing as a universal obligation rather than a conditional evidence technique;
- subjective reviewer claims that a test is "not meaningful" without naming a concrete protected defect;
- duplicating existing coverage / behavioral-eval rules under a new vocabulary;
- discouraging legitimate structural checks where the structure itself is the contract.

## Revisit trigger

Re-open canonicalization when at least one material real case appears in this Playbook or a well-observed adopter where:

`validator/test PASS → real material regression still occurs → analysis shows the check was tautological, a change detector, mirror-oracle, mock-only proxy, or source-text proxy for a different behavioral claim`

Useful evidence would include one or more of:

- an actual escaped defect demonstrating weak discriminative power;
- a test/verifier that remains green under a realistic mutation it was expected to catch;
- repeated review evidence that agents create mirror expectations or source-presence tests and overclaim correctness;
- cross-project evidence that a compact quality gate prevents such failures without materially increasing validation ceremony.

Evidence favoring `NO CHANGE` would include:

- current Playbook rules repeatedly causing agents/reviewers to derive the needed distinction without explicit canonical wording;
- no real escaped defect after meaningful usage;
- an explicit rule producing more validation ceremony/noise than defect-detection value.

## Possible future minimum-sufficient boundary

If later evidence justifies promotion, prefer a thin addition inside the existing `DEBUG_VALIDATION.md` owner rather than a new capability/file/framework. A future rule should likely cover only:

1. name the material defect / invariant violation / behavior regression the check protects;
2. keep the expected oracle independent enough from the subject under test to distinguish that defect;
3. permit structural/text assertions when structure/text is itself the declared contract, but do not let them prove unrelated downstream behavior;
4. use negative fixture, controlled mutation, fault probe, or baseline comparison only when risk/value justifies the extra evidence cost.

Do not require a universal mutation-testing framework.

## Maintainer decision at capture

**KEEP AS REFERENCE CANDIDATE / WAIT.**

The concept remains worth remembering, but there is no current obligation to modify canonical Playbook rules, tooling, tests, behavioral scenarios, or adopter guidance. Revisit only on the trigger above or materially stronger independent evidence.
