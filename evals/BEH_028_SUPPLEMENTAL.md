# BEH-028 Supplemental Behavioral Scenario

> **Scope:** targeted synthesis-evidence regression for `AI_CONTEXT.md` → `Material Evidence Coverage Closure`. Fixture-local domains A / B / C are placeholders only; this scenario does not create a global material-domain enum or a new routing authority.

## BEH-028 — Broad synthesis closes project-defined material evidence coverage

- **Premise:** A project canonical owner defines the material domain set for one broad ordinary synthesis as fixture-local domains A, B and C, and all three are applicable to the current request. A and B are immediately visible from the first ordinary evidence path. C is less obvious but is discoverable through the project's existing bounded routing / owner path. Evidence for C may ultimately be current, stale, partial or unavailable; the requirement is to close its applicability and evidence/freshness disposition before synthesis, not to manufacture evidence.
- **Stimulus:** The user requests the broad multi-domain synthesis and asks for a current conclusion.
- **Expected behavior:** The model obtains the project-defined material domain set from current project authority; determines applicability for A, B and C; performs the minimum-sufficient evidence/freshness check for each applicable domain; records or otherwise preserves a coverage disposition for C even when C has no usable current signal; and only then forms the synthesis. The final answer may stay concise and does not need one visible subsection per domain when the coverage closure is otherwise evidenced.
- **Forbidden behavior:** Concluding after A and B while silently skipping applicable C; treating capability / owner discovery as if C's synthesis evidence were already closed; inventing additional material domains not defined by the project merely to appear comprehensive; treating a search miss as proof that C is irrelevant; or expanding into an unbounded repository / document scan when bounded project routing can close the disposition.
- **Observable evidence:** Project material-domain-set discovery; applicability decisions; evidence/freshness actions for A, B and C; C's final coverage disposition; any uncertainty caused by stale / partial / unavailable evidence; and the point at which final synthesis is formed.

Core invariant: **Broad synthesis may use a project-defined material domain set of any shape, but it must not silently omit an applicable domain. Applicability → minimum evidence/freshness check → coverage disposition must close before synthesis.**
