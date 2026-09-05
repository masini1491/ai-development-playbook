# Session Handoff Template

> **Role**：把 `CHATGPT_WORKFLOW.md` 的 `Session Compaction / Rehydration Contract` 轉成可直接交接的薄 adapter。
>
> **Authority boundary**：handoff 只是一個 retrieval / recovery index，不是 repository truth、permission grant、completion evidence 或 durable work admission。

## When to use

只在長 session 已出現 material retrieval / stale-premise / handoff risk 時建立；不要只因聊天變長就機械式產生。

## Compact payload

```json
{
  "handoff_version": 1,
  "repository": {
    "full_name": "owner/repo",
    "branch": "main",
    "observed_head": "<40-char SHA or UNKNOWN>"
  },
  "task": {
    "goal": "<current goal>",
    "completion_criterion": "<what counts as done>",
    "scope": ["<authorized scope>"]
  },
  "canonical_pointers": [
    {
      "path": "<repo path>",
      "section_or_symbol": "<optional exact pointer>",
      "observed_at": "<SHA/ref if material>"
    }
  ],
  "confirmed_findings": ["<current material finding>"],
  "superseded_assumptions": ["<only if forgetting it would cause regression>"],
  "evidence_gaps": ["<pending / unavailable / blocker>"],
  "current_decision": "<current state / decision>",
  "next_authorized_action": "<next action or STOP>",
  "stop_conditions": ["<authority/evidence condition that requires STOP>"]
}
```

Unknown values stay `UNKNOWN` / pending; do not guess to make the handoff look complete.

## Rehydration procedure

A fresh session must:

`Confirm repository / branch / current HEAD → read current project governance → read current Hot coordination if applicable → follow canonical pointers → reconcile checkpoint claims against current evidence → preserve / supersede evidence status → execute only if current authorization still holds`

If current canonical state differs from the handoff, current authority wins. A changed HEAD triggers bounded material-delta reconciliation; it does not automatically invalidate everything and does not automatically preserve stale claims.

## Persistence boundary

By default this template is conversation-level / transient. Persisting any field into `TASKS.md`, Cold Registry, evidence staging or another repository surface still requires the normal admission and write-authority gates.

Core principle: **Handoff carries pointers and bounded current state; rehydration re-establishes truth and authority from canonical sources.**
