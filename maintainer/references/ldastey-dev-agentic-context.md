# ldastey-dev/agentic-context

- Source: `ldastey-dev/agentic-context`
- Reviewed revision: `502dc83effca9cff6018859f05bcc581c8a11eb2`
- Source role: external context-engineering / multi-agent distribution reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## Observations

The reviewed source overlaps materially with existing Playbook concerns around progressive/on-demand context loading, single-source-of-truth ownership, thin per-runtime adapters, evidence-over-opinion discipline, and routing that loads task-relevant detail instead of the full rule set.

The main architectural contrast is routing and distribution strategy:

- `agentic-context` uses a leaf-oriented keyword-to-file router in `.context/index.md`; multiple keyword matches may load multiple standards/playbooks for one task.
- This Playbook prefers authority/owner-first routing, stable machine capability identities, bounded canonical-owner reads, and direct-leaf bypass when an exact target is already known.
- `agentic-context` deploys/copies standards, playbooks, conventions, and selected per-agent adapters into target repositories; this Playbook instead normally resolves the adopting project's declared Playbook baseline to an immutable revision and reads canonical owners from that revision.

External implementation strengths worth retaining as evidence candidates include:

- multi-agent deployment tooling for Claude Code, GitHub Copilot, Cursor, Devin, and Windsurf;
- generated Claude/Copilot skill wrappers derived from canonical playbook frontmatter rather than hand-maintained copies;
- cross-platform distribution tests for Bash and PowerShell, including portability constraints for macOS Bash 3.2 and Windows PowerShell 5.1;
- clear maintainer UX for source-to-target layout, adding standards/playbooks/agents, and "what belongs where / what does not belong here" guidance.

## Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Leaf keyword routing vs owner/capability routing** — compare route accuracy, false-positive loading, missed owners, multi-domain over-loading, and retrieval cost across fixed task stimuli.
2. **Routing metadata duplication / stale snapshot** — test whether duplicated policy summaries in routing/index surfaces drift when a canonical standard changes, and whether deterministic tooling catches that drift.
3. **Context-budget freshness** — test whether human-facing claims about always-in-context size remain accurate as the actual always-on surface evolves, and whether a freshness/routing-integrity check detects stale claims.
4. **Vendored deployment vs immutable baseline pointer** — compare local/offline availability, provenance clarity, update/rollback cost, stale-rule incidence, and fresh-session reproducibility.
5. **Generated runtime wrappers** — only if future activation evidence justifies it, compare generic pointer-based activation against generated native wrappers for trigger reliability, correct owner routing, extra context, and runtime-specific drift.

## Useful UX / expression patterns

Useful presentation ideas include the simple `Always in context / On demand / Reference` explanation for first-time users, an explicit source-to-target mapping table, and maintainer checklists that route contributors by change type. These are UX patterns, not new policy authority.

## Limitations / do not assume

- The reviewed source's fixed engineering thresholds (for example coverage, CI-stage, architecture, or runtime-specific portability requirements) are project/product choices and are not suitable as universal Playbook policy without independent evidence.
- Bash/PowerShell version support, runtime-specific file locations, interactive agent selectors, and target-repository copy/deploy behavior are implementation choices, not cross-project governance requirements.
- The observed duplicated summaries and stale-size signal are useful comparative evidence, but they do not prove a repository-wide defect beyond the checked scope.
- This dossier must not be used by normal capability discovery to claim that the Playbook supports deployment generators, native skill wrappers, or any other external implementation listed here.
- No item here is admitted work, a canonical bug, or a Hot/Cold obligation.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`. The source does not currently demonstrate a missing core governance layer in this Playbook. Its clearest relative strength is distribution/activation implementation maturity; this Playbook remains comparatively stronger in explicit authority separation, thin routing metadata, immutable baseline identity, and routing-closure semantics.

The lowest-sufficient future evidence work, if explicitly admitted later, is a bounded comparison of leaf keyword routing versus owner/capability routing plus a deterministic stale-routing-metadata experiment. Do not mutate canonical policy or add distribution tooling solely from this reference.

## Revisit trigger

Revisit if adopter repositories repeatedly show activation/distribution friction that thin pointer-based adapters do not solve, if routing errors suggest owner-first discovery is underperforming, or if independent experiments show generated runtime wrappers or local deployment materially improve reliability without unacceptable drift/reconciliation cost.
