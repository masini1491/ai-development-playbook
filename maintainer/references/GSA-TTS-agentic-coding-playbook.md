# GSA-TTS/agentic-coding-playbook

- Source: `GSA-TTS/agentic-coding-playbook`
- Reviewed revision: `9ea8add75a017bed007230a530da4a943c3eebdf`
- Source tree: `66fc46420d6290d9e65490b9eb4404e79e15edbf`
- License: CC0 1.0
- Source role: external governance / authority / compliance-oriented agent workflow reference
- Authority: none over this Playbook
- Adoption state: `REFERENCE-ONLY`
- Review type: bounded comparative review for Playbook self-maintenance

## 1. Already-covered concerns

The reviewed source overlaps strongly with this Playbook on thin project governance layered over a reusable baseline, progressive context loading, explicit permission boundaries, least privilege, fail-closed prerequisites, canonical-owner separation, deterministic validation, skills/procedures loaded only when relevant, immutable/pinned upstream acquisition, and the principle that an external framework does not replace project-specific authority.

Its domain is materially different: it is optimized for U.S. federal/FIPS Moderate development and includes NIST/OMB/OWASP mappings, ATO artifacts, data-classification constraints, security controls, and federal deployment procedures. Those compliance rules are not generally applicable to this Playbook's cross-domain adopter base.

## 2. Same failure mode, different architecture

### Universal contract + thin project layer

The source defines one universal `AGENTS.md` behavioral contract and a thin project `AGENTS.md` that adds project-specific rules without copying the universal rules. The project layer declares a required contract version and cannot override the universal layer.

This is close to this Playbook's baseline + adopter-project governance model and its `Activate by pointer, not policy copy` principle. Both designs avoid copy/paste drift and preserve project-local authority for project-specific facts. The GSA design is more prescriptive about a conventional filesystem installation and contract schema.

### Deterministic prerequisite gate

A downstream project must prove that the universal contract is available before work begins. The check is deterministic and fail-closed; self-attestation or repository prose claiming the contract is available cannot satisfy it. A structured `contract.role: universal` marker prevents a thin project file from accidentally satisfying the prerequisite.

This is a particularly mature example of converting a governance prerequisite into a low-ambiguity machine check. It resembles this Playbook's repository identity/read-acquisition/permission gates and Deterministic Enforcement Admission Gate, but it protects one specific contract-availability invariant.

### Acquisition fallback without authority promotion

The contract lookup uses ordered acquisition: environment-provided home path, fresh git-ignored cache, fetch from a pinned canonical release, then halt. A fallback cache remains explicitly a fallback rather than becoming the canonical source.

This closely parallels this Playbook's Repository Read Acquisition / Recovery Gate: recovery changes transport, not authority. The GSA implementation is useful evidence that this principle can be enforced mechanically for a narrowly defined artifact.

### Progressive context routing

`CONTEXT-GUIDE.md` is a curated task router, while `INDEX.yaml` is the complete inventory. Skills load only when invoked. This separates normal task routing from exhaustive inventory and is conceptually close to `CHAT_INIT.md`, `CAPABILITY_INDEX.md`, `PLAYBOOK_INDEX.json`, Section Routers, and direct-leaf bypass.

A notable difference is default-load cost: the GSA guide declares a large Tier-1 set for every task, even while offering a compact coding shortcut. This Playbook deliberately pushes harder toward minimum-sufficient owner reads and lower always-on context.

### Governance plus deterministic tooling

The source combines prose contracts with validators for document frontmatter, skills, plans, ADRs, landscape data, repository audit, pre-deployment checks, environment doctor, generated indexes, and contract availability. It also uses CI/pre-commit enforcement.

This aligns with this Playbook's split between judgment rules and deterministic enforcement, but the GSA repository has a much broader compliance-specific validator surface.

### Explicit permission matrix

The project template gives separate `Permitted Actions`, `Actions Requiring Approval`, and `Prohibited Actions` sections. The universal contract also requires minimum permissions and human approval for destructive operations, external network access, dependency changes, CI/CD changes, commit/push, and higher-classification data access.

This is structurally similar to this Playbook's operation-authority intersection and permission-gated operation recovery. The GSA template is a useful adopter-facing expression pattern because project-specific permissions are easy to inspect without duplicating universal policy.

### Compliance traceability

Documents carry structured frontmatter such as status, tier, audience, keywords, load priority, review cycle, and NIST mappings. The repository generates a machine-readable index and validates metadata consistency.

This is more metadata-heavy than this Playbook. The transferable principle is not the federal taxonomy itself, but that routing metadata, authority role, lifecycle status, and external control mappings can be machine-checked independently from prose.

## 3. External capabilities / implementation maturity worth further evidence

These are external implementation patterns, not whole-Playbook absence claims.

### A. Machine-verifiable prerequisite identity

The combination of `contract.role`, version declaration, project `requires_contract`, deterministic probe, and fail-closed result is a strong implementation of “prerequisite presence is a fact, not an LLM judgment.”

### B. Explicit fallback freshness stamp

The git-ignored fallback cache records source URL, release tag, and fetch time. Freshness is compared against the pinned release, while fallback usage remains visible to the user.

### C. Generated inventory + freshness validation

A machine-readable document index is generated from document metadata and checked for freshness in CI, reducing hand-maintained routing/index drift.

### D. Structured adopter permission surface

A thin project template explicitly separates allowed, approval-required, and prohibited operations, which can make execution authority easier to audit than dispersed prose.

### E. Domain control traceability

Security and compliance guidance is mapped to external frameworks and evidence surfaces. This is useful for regulated adopter profiles, though not appropriate as universal Playbook policy.

### F. Human-reviewed external-guidance monitoring

The repository monitors authoritative guidance feeds and compares detected changes against a registry, but requires human review before canonical updates. This is a concrete example of automated evidence discovery without automated authority promotion.

## 4. Useful expression / UX patterns

- `contract.role: universal` versus `contract.role: project-layer` makes authority identity explicit and machine-readable.
- `requires_contract` states compatibility at the project boundary rather than relying on prose implication.
- “STOP AND CHECK BEFORE DOING ANY WORK” is paired with an actual deterministic probe, not just a warning.
- Home → fresh cache → pinned fetch → halt is a clear acquisition ladder with visible fallback semantics.
- `CONTEXT-GUIDE.md` explicitly says it is a curated load-order guide, not a full inventory; `INDEX.yaml` owns exhaustive inventory.
- Skills are self-contained and loaded only when invoked.
- Project templates expose permission categories in one place rather than copying universal security rules.
- Generated-index freshness and link checking reduce documentation drift through cheap deterministic checks.

## 5. Runtime/domain-specific patterns not suitable for direct generalization

- Federal/FIPS/ATO/NIST/OMB/OWASP requirements are domain constraints, not universal software-agent governance.
- A 16K-word always-load Tier 1 is too expensive as a general Playbook default and conflicts with this Playbook's minimum-sufficient retrieval goal.
- A fixed conventional home path and git-ignored cache are one distribution mechanism; this Playbook must remain usable through repository-native connectors, public canonical reads, uploads, and other recovery transports.
- A structured role marker is valuable only where a deterministic artifact identity invariant exists; adding frontmatter to every Playbook document would create metadata cost without necessarily improving retrieval.
- A universal prerequisite must not become a way for external content to outrank target-repository governance or the user's current instruction.
- Pre-commit/CI hard blocks are appropriate only for deterministic, observable, low-false-positive invariants that pass this Playbook's enforcement-admission criteria.
- The source's permission defaults are federal/security-oriented and should not be copied into adopter repositories whose project governance intentionally grants different authority.

## 6. Evidence candidates

These are maintainer research candidates only; none is admitted work.

1. **Baseline identity marker pilot** — test whether an explicit machine-readable Playbook identity/revision/role marker would reduce false baseline matches or recovery ambiguity beyond current immutable-SHA resolution.
2. **Acquisition fallback stamp pilot** — for user-mediated or cached Playbook recovery, compare current provenance reporting with a small machine-readable source/revision/fetched-at record; measure stale-baseline and authority-confusion errors.
3. **Generated routing freshness experiment** — determine whether selected routing/index surfaces can be deterministically checked against canonical owners without turning the index into a duplicate source of semantic truth.
4. **Adopter permission-matrix UX experiment** — compare current project `AGENTS.md` authority prose with a compact allowed / approval-required / prohibited table while preserving the existing operation-authority intersection.
5. **Prerequisite-gate behavioral evaluation** — create a cold-start scenario where a project claims a required baseline is present but deterministic evidence contradicts it; verify fail-closed behavior and recovery routing.
6. **External-guidance discovery pattern** — where an adopter has regulated upstream sources, test automated change detection that produces evidence candidates only and requires explicit canonical promotion.

## Current maintainer conclusion

Keep as `REFERENCE-ONLY`.

The strongest transferable implementation is the **machine-verifiable prerequisite identity + fail-closed acquisition ladder**. It independently reinforces several existing Playbook principles: recovery mechanism must not change authority, self-attestation cannot prove a prerequisite, and deterministic invariants should be enforced mechanically when they are cheap and unambiguous.

However, this Playbook already resolves a floating baseline to an immutable revision and has a broader acquisition/recovery gate. There is not yet evidence that adding a universal frontmatter contract schema or fixed local cache would improve cross-environment reliability enough to justify the extra protocol.

A lower-cost candidate is to test whether **provenance/freshness metadata for recovered baseline artifacts** materially improves read recovery and stale-baseline diagnosis. That can be evaluated without changing normal bootstrap or making every document carry structured metadata.

The source also provides useful evidence for keeping **curated routing separate from exhaustive inventory**. Its own large always-load tier illustrates the trade-off: progressive disclosure helps, but a broad mandatory baseline can still dominate context. This supports retaining this Playbook's stricter minimum-sufficient routing rather than adopting the GSA loading tiers.

Do not import federal compliance controls, install its tooling, or add universal prerequisite machinery solely from this reference.

## Revisit trigger

Revisit if:

- baseline recovery repeatedly accepts stale/wrong artifacts or loses provenance across transport fallbacks;
- adopter projects repeatedly misclassify project-specific permission versus baseline authority;
- routing/index drift becomes a repeated source of incorrect owner selection despite current validation;
- a regulated adopter needs machine-traceable mappings from Playbook procedures to external control frameworks;
- cold-start evaluations show agents trusting repository claims about prerequisites instead of deterministic evidence.