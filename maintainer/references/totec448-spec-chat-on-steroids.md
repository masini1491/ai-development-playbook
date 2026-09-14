# `totec448-spec/chat-on-steroids` comparative review

> **Maintainer-only pre-canonical evidence.** This dossier records a bounded external-runtime comparison. It does not establish a Playbook capability, policy, required dependency, runtime integration, validation result, or execution authority.

## Review identity

- External repository: `totec448-spec/chat-on-steroids`
- Reviewed revision: `f51acbccdd734f524799ea92bb747be765fba1e4`
- Review date: `2026-09-14`
- Playbook comparison baseline: `cace44ee34ea315feb39d12dc577711712200e2f`
- Category: ChatGPT local execution runtime / persistent multi-agent orchestration / session continuity
- Priority: HIGH
- Maintainer state: REVIEWED

## Why this source matters

Chat On Steroids (CoS) is not primarily a governance framework. It is a local execution/runtime layer around ChatGPT browser conversations, exposing local files, patching, shell/terminal, recorded sessions, persistent workers, desktop control, and external MCP plugins. Its design is therefore useful as implementation evidence for several Playbook concepts without being a replacement for Playbook authority or routing.

The most relevant comparison surfaces are:

1. child routing and child profile selection;
2. persistent worker identity and reuse;
3. session continuity across provider conversations;
4. Goal/Loop autonomous continuation;
5. a pre-production Codex Desktop bridge design.

## 1. Child routing and profile selection

CoS exposes an `agents` tool with `spawn`, `message`, `status`, and `finish`. Workers are browser ChatGPT conversations subordinate to a prime conversation. A worker may request its own model and reasoning effort, and workers can sleep after finishing rather than being destroyed immediately.

This overlaps strongly with the Playbook's current:

- `Child Routing Forecast`;
- `Delegation Opportunity Scan`;
- `Subagent / Delegation Gate`;
- root/child model and reasoning profile routing.

The main architectural difference is ownership. Playbook rules decide whether bounded work should be delegated; CoS implements an actual worker runtime and lifecycle. CoS therefore provides runtime evidence for delegation mechanics, but it does not replace the Playbook's authority, scope, admission, or cost/quality decision gates.

### Comparative conclusion

Playbook delegation governance is already more explicit about *when* delegation is justified. CoS is more explicit about *how a delegated worker lives over time*.

No canonical Playbook gap was found in basic delegation admission or child-profile routing.

## 2. Persistent worker identity and reuse

CoS workers retain their ChatGPT conversation when they finish. A finished worker can become sleeping, keep durable history/identity, and later be messaged and reused. Sleeping workers do not consume an active slot in the same way as working workers.

CoS also treats identity as stronger than a short local worker label: prime family/run and exact worker conversation matter, and ambiguous identity fails closed.

This surfaces a distinction that is not currently explicit in the Playbook:

```text
Delegation admission
!=
Agent lifetime
!=
Execution concurrency
```

A child may be valid for one bounded responsibility without acquiring permanent authority for later work. Likewise, a runtime may keep a child alive after one subtask without implying that later work should automatically route back to it.

### Candidate invariant

> **Persistent child identity must not imply persistent delegation authority.**

If a future execution surface exposes reusable/persistent child identity, reuse may be worth considering when continuity materially reduces bootstrap, context, specialization, or reconciliation cost. However, each new bounded responsibility must still satisfy the current delegation gate; prior successful delegation is not sticky authority.

### Admission status

This is a **research candidate only**. It should not yet be added to `CODEX_EXECUTION.md` because CoS has its own durable worker runtime, and current Codex child lifecycle semantics have not been independently shown to provide equivalent sleeping/reuse behavior.

## 3. Session continuity across provider conversations

CoS distinguishes a durable local session from a replaceable ChatGPT conversation. Its `Compact & Resume` flow can move the same local work session from one provider conversation to another while preserving local project association, history, queued work, and worker history.

This maps closely to the Playbook's existing Session Compaction / Rehydration contract:

- preserve a minimum sufficient checkpoint;
- distinguish durable task/project authority from transient conversation context;
- rehydrate from current repository/canonical authority;
- do not treat a fresh chat as inherited execution authority.

### Comparative conclusion

CoS is useful implementation evidence for the principle:

```text
Durable work/session identity != provider conversation identity
```

But the Playbook already expresses the needed provider-neutral governance semantics. No new canonical framework is required merely because CoS has a richer local persistence layer.

## 4. Goal / Loop autonomous continuation

CoS has explicit runtime modes:

- Goal may decide the requested objective is complete and send no further message;
- Loop continues within the user's brief until disabled;
- recent 2.1.11 work narrows continuation decision context by using authored conversation context while excluding recorded tool bodies.

This is runtime orchestration, not a direct Playbook analogue. The Playbook already separates:

```text
Observation != Recommendation != Admitted Work
```

and prevents completion from automatically creating durable follow-up work merely because more improvement is possible.

### Comparative conclusion

The useful abstraction is:

> **Continuation capability does not create continuation authority.**

A runtime may automate continued execution only while the work remains inside the already-authorized task/brief and runtime policy. CoS Goal/Loop itself should remain provider/runtime-specific rather than becoming a new Playbook mode.

## 5. Codex Desktop bridge research

CoS contains `docs/codex-desktop-bridge.md`, explicitly marked as a design draft rather than a production tool. The document reports successful background send to an exact existing Codex Desktop thread using a supported `codex queue --thread <UUID> --message ...` path.

The same RFC also states that production integration still requires bounded and supported enumeration/read/wait semantics, exact identity handling, staleness behavior, and read-back evidence. A send acknowledgement by itself is not treated as completion evidence.

This aligns with the Playbook's Completion Evidence Guard: an operation acknowledgement is not sufficient proof of canonical state or completion when read-back is required.

### Comparative conclusion

The bridge is HIGH-interest interoperability research, but remains pre-production external evidence. It must not be promoted to a Playbook runtime integration until current Codex-supported list/read/wait/read-back behavior is independently verified and a provider-neutral boundary can be stated without assuming private CoS machinery.

## Security and authority observations

CoS is a powerful local runtime, not a sandboxed toy environment. Its published documentation makes several boundaries explicit:

- `exec_command` runs with the logged-in user's normal OS privileges and is not confined to approved filesystem roots;
- desktop control is a separate broad capability surface;
- session recording is durable local history and is not equivalent to encrypted credential storage;
- Core, Desktop, and Plugins are separate connector/permission surfaces;
- unknown or ambiguous identity is intended to fail closed where mutation or attribution could target the wrong owner.

These details reinforce a Playbook principle: capability availability does not itself grant task, repository, mutation, credential, or deployment authority.

## Documentation-quality note

The reviewed source is generally careful about evidence levels and ownership, but a small documentation inconsistency was observed around current macOS Desktop availability: current setup/product material describes macOS Desktop support with explicit permission requirements, while one Security-policy limitation line still states Desktop is unavailable on macOS/Linux. This should be treated as source documentation drift, not as evidence against the broader runtime architecture.

## Overall comparison

| Surface | CoS contribution | Playbook status |
| --- | --- | --- |
| Child routing | Real persistent worker runtime | Delegation governance already canonical |
| Child profile routing | Per-worker model/reasoning | Already canonical in provider-neutral form |
| Persistent worker reuse | Sleeping/revivable worker identity | **New research candidate**; not canonical |
| Session continuity | Durable local session across ChatGPT conversations | Existing Playbook contract already covers provider-neutral semantics |
| Goal/Loop | Autonomous continuation runtime | Keep runtime-specific; do not create a Playbook mode |
| Codex Desktop bridge | Exact-thread send research; read-back incomplete | HIGH-interest pre-production interoperability evidence |

## Maintainer conclusion

`totec448-spec/chat-on-steroids` is a strong real-world runtime reference and should remain a HIGH-priority reviewed source.

The strongest new research question is not "should Playbook adopt CoS workers?" but:

> **How should a provider-neutral Playbook distinguish delegation admission from reusable child lifetime when a runtime exposes persistent agents?**

Current recommendation:

- keep CoS as external maintainer evidence;
- do not add a CoS dependency or runtime adapter;
- do not add Goal/Loop as a Playbook mode;
- do not assume Codex supports CoS-style sleeping child reuse;
- preserve `Persistent child identity must not imply persistent delegation authority` as a research candidate for future cross-runtime evidence;
- keep the Codex Desktop bridge in pre-production research until supported read/list/wait/read-back semantics are independently verified.

No canonical policy change is admitted by this dossier.
