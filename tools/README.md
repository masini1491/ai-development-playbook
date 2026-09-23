# Maintainer Tooling

> **Role:** Playbook maintainer tooling execution leaf. Read only when the current work actually executes, modifies, or validates `tools/**` or its tests.
>
> **Authority boundary:** Repository ownership / who may execute or mutate these tools remains in root `AGENTS.md`. Generic runtime/materialization semantics remain in `CHATGPT_RUNTIME_EXECUTION.md`; GitHub acquisition/transport remains in `GITHUB_OPERATIONS.md`; validation semantics remain in `DEBUG_VALIDATION.md`.

## Runtime contract

Current maintainer deterministic tooling uses:

- Python 3.11+
- Python standard library only for the current validator / Doctor / behavioral-eval tooling
- no package manager, requirements file, or extra config framework merely for the current minimal checks

Only a ChatGPT session that has actually verified the required runtime / dependency / filesystem / network capability may execute these repository programs. Codex / coding agents remain read-only and non-executing for this repository unless the user explicitly changes root `AGENTS.md`.

## Tool map

- `tools/playbook_check.py` — deterministic Markdown / routing checks.
  - Formal check: `python tools/playbook_check.py`
  - Unit tests: `python -m unittest tests/test_playbook_check.py`
- `tools/adoption_doctor.py` — read-only / report-only adoption-declaration and bootstrap-wiring checks for a specified project repository; it does not prove full routing integrity or behavioral routing correctness.
  - Unit tests: `python -m unittest tests/test_adoption_doctor.py`
- `tools/behavioral_eval.py` — deterministic run-record / regression-selection validation only. Behavioral scenario semantics and evidence classification remain in `DEBUG_VALIDATION.md` and `evals/README.md`; this tool does not itself judge semantic behavioral PASS.

These tools enforce only objective, machine-checkable invariants. Do not add AI-judgment heuristics such as duplicate-policy scoring, arbitrary section-length thresholds, architecture scores, or Context Cohesion scores and call them deterministic validation.

## Adoption Doctor input acquisition

The Doctor engine accepts a filesystem root and does not itself acquire GitHub credentials, call GitHub APIs, or receive target-repository write authority.

The Doctor parser prefers exactly one active instance of each structured adoption section as the deterministic input boundary for its responsibility: AI Development Playbook baseline, Authority boundary, and Project-specific minimum contract. Parser-active text excludes fenced Markdown, HTML comments, and Markdown blockquote lines so examples/history cannot satisfy declaration markers. When a preferred section is absent, the Doctor uses normalized active-text compatibility fallback and emits a warning; duplicate preferred sections do not fall back implicitly. This preserves older valid adoption shapes without treating the preferred headings as mandatory project governance. The Doctor still checks declaration/wiring markers only and does not prove the semantic correctness of routing or authority prose.

Two input acquisition modes are supported:

### Local Path Mode

An authorized local session passes an existing project root to:

`python tools/adoption_doctor.py <project-root>`

The Doctor reads that filesystem tree and does not modify it.

### ChatGPT GitHub Snapshot Mode

A ChatGPT session with authorized repository-read capability may acquire only the files required by the Doctor's active checks from the user-specified canonical repository / branch / ref, materialize them into a temporary or ephemeral snapshot, then run:

`python tools/adoption_doctor.py <snapshot-root>`

The snapshot is execution input only. It is not a new project authority and must not be written back to the target repository or used to mutate a Codex / human workspace.

Acquisition contract:

1. Prefer an available repository-native GitHub connector for canonical repository content.
2. Resolve the requested branch / ref consistently with the target the user asked to inspect.
3. Acquire `AGENTS.md` first, then only the additional files required by the Doctor checks activated by that governance.
4. Keep repository acquisition capability, local runtime/network capability, Doctor execution capability, and target-repository write authority separate.
5. If required files cannot be completely acquired because of connector / permission / ref / runtime limits, report `SNAPSHOT / REMOTE EVIDENCE UNAVAILABLE` or an equivalent acquisition gap. Do not turn an incomplete snapshot into a deterministic target-project FAIL.
6. Unverified cached/local content must not override newer canonical remote evidence.

If snapshot correctness depends on several repository files, use the same exact canonical revision in accordance with `INFORMATION_INTEGRITY.md` → `Snapshot Consistency Guard`.

## Execution / evidence boundary

The commands above are execution contracts for an authorized, capable ChatGPT maintainer session; they do not grant Codex, another agent, CI, pre-commit hooks, or GitHub Actions permission to run repository tooling.

A tool PASS proves only the invariant it actually checks. Formal repository completion / validation claims remain subject to `DEBUG_VALIDATION.md`, and GitHub mutation/read-back claims remain subject to `GITHUB_OPERATIONS.md`.

Core principle: **Load maintainer tooling detail only when tooling is actually in play; keep ownership in AGENTS, execution mechanics in this leaf, and broader runtime / GitHub / validation semantics in their existing canonical owners.**
