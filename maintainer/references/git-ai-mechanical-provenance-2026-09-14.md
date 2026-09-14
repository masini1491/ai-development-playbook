# git-ai Mechanical Provenance Review — 2026-09-14

> Maintainer-only pre-canonical evidence. This file does **not** establish a Playbook capability, policy, required dependency, validation PASS, or adopter requirement.

## Review target

Evaluate whether `git-ai-project/git-ai` can serve as an optional mechanical-attribution provider for a possible future Playbook capability tentatively described as **AI Mutation Provenance / Mechanical Attribution**.

Playbook baseline reviewed:

- repository: `masini1491/ai-development-playbook`
- main: `c5d6fdd66d17ebeb99a6d0ed7cb9b574a2bd6a95`

External source baseline reviewed:

- repository: `git-ai-project/git-ai`
- main: `0670e7ef27590af0e8ff5409267f3f4b09b8fcb4`
- current main version bump: `1.7.6`
- latest published release observed: `v1.7.5`
- Git AI Standard: `authorship/3.0.0`

## Observed fit

Current Playbook already owns semantic engineering provenance at the governance/evidence level:

- Task / Stage authorization;
- actor selection and responsibility;
- delegation / child-profile reporting;
- repository authority and bounded mutation;
- validation evidence and completion read-back.

`git-ai` addresses a different layer: line-level mechanical attribution. Its standard stores AI authorship logs in `refs/notes/ai`, maps file line ranges to session / trace or known-human identities, and carries agent identity including tool, conversation/session id, and model. Session records also expose optional `custom_attributes`.

Potential interoperability shape:

```text
Playbook semantic provenance
Task / Stage → actor responsibility → evidence / validation
                         ↓
optional provider bridge
Task / Stage identity → git-ai custom attributes
                         ↓
mechanical provenance
AI session / trace / model → actual lines → commit
```

This is complementary rather than substitutive. Mechanical attribution must not grant mutation authority, prove correctness, or establish ultimate responsibility.

## Privacy / storage boundary

The reviewed OSS documentation states that unauthenticated OSS mode keeps code, prompts, and agent-usage data local; prompts are stored in local SQLite while attribution metadata is written to Git notes. OSS error/exception telemetry is enabled by default but can be disabled or redirected. Cloud / Teams / Enterprise modes collect broader session/tool/token/prompt data and therefore have materially different privacy boundaries.

A future Playbook integration must remain provider-agnostic and must not require full prompts, complete transcripts, hidden reasoning, or chain-of-thought in Git.

## Known limitations / negative evidence

Mechanical attribution is evidence, not infallible authorship authority.

Current public issue evidence includes attribution edge cases. In particular, issue `#995` describes token-aligned human-override boundaries that can cause subsequent AI-written lines to disappear from the Git note and appear human-authored by omission. The issue is open at the reviewed source state.

More importantly for Codex integration, `tests/integration/pre_commit_unit.rs` contains an ignored integration test:

`test_pre_commit_checkpoint_context_uses_inflight_bash_agent_context`

Its own test comment states that the expected Codex Bash-agent context handoff into pre-commit attribution is **currently broken** because the context does not survive the subprocess boundary in daemon mode. Therefore source support for Codex must not be translated into a claim that every Codex execution path has verified end-to-end attribution.

The reviewed source also distinguishes Codex telemetry surfaces; for example, the token-usage extractor documents support for session rollout format while headless `codex exec` log format is not tracked by that parser.

## Runtime canary attempted in this ChatGPT session

Desired bounded canary:

1. ordinary Codex edit;
2. Codex edit followed by human override;
3. root + child/subagent-shaped edits in one repository;
4. commit → Git note / `git ai blame` attribution check;
5. Task / Stage identity injected through `custom_attributes` and preserved into attribution metadata.

Current ChatGPT runtime capability probe:

- `git`: available;
- `python3`: available;
- `git-ai`: unavailable;
- `codex`: unavailable;
- outbound DNS / direct GitHub download from the shell: unavailable.

No runtime-native git-ai/Codex canary was therefore executed.

Playbook repository governance also explicitly forbids substituting GitHub Actions, Codex, another coding agent, pre-commit automation, or other automation for a missing ChatGPT runtime/toolchain when executing Playbook-repository programs unless the user explicitly changes that rule. This review did not reinterpret the user's authorization to investigate provenance as a blanket governance change allowing such substitution.

Status:

```text
RUNTIME_CANARY_BLOCKED
```

This is not a provider FAIL. It means the current ChatGPT execution surface cannot establish the desired runtime evidence.

## Admission conclusion

Current evidence supports the **architectural gap** and the interoperability idea, but does not support promoting `git-ai` as a verified Playbook adapter yet.

Current maintainer conclusion:

- `AI Mutation Provenance / Mechanical Attribution` remains a plausible provider-agnostic capability candidate;
- `git-ai` remains a strong external reference / experimental provider candidate;
- do **not** make `git-ai` a required dependency;
- do **not** make `% AI`, accepted-rate, or attribution metadata a quality/correctness metric;
- do **not** let mechanical attribution override Task/Stage authority, Git canonical state, validation evidence, or human responsibility;
- do **not** add Adoption Doctor warnings merely because a project has no mechanical-attribution provider;
- do **not** promote a canonical adapter contract until a runtime canary covers at least ordinary Codex edits, human override, multi-session/subagent attribution, Git-note/blame closure, and the proposed custom-attribute bridge.

## Promotion gate

A future promotion review should require bounded runtime evidence for:

```text
Codex edit
+ human override
+ multi-session/root-child attribution
+ commit / refs/notes/ai / git-ai blame closure
+ Task/Stage custom-attribute preservation
+ explicit observability / failure boundary
```

If those pass, consider a thin provider-agnostic canonical contract in `REPOSITORY_EXECUTION.md` with only a pointer from validation / Codex reporting surfaces as needed. If attribution remains partial or execution-surface dependent, keep `git-ai` experimental while the general provenance capability may be reconsidered independently.
