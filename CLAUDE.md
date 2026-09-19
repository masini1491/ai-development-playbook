# Claude Code bootstrap override

This file is an intentional thin routing shim for Claude Code. It is not a Playbook authority and does not create a second current-state policy source.

Claude Code may natively use `AGENTS.md` when no `CLAUDE.md` is present. This repository intentionally keeps `CLAUDE.md` because the root `AGENTS.md` is maintainer governance, while ordinary Claude Code task bootstrap should enter through `CHAT_INIT.md`. Exact Claude Code discovery / configuration behavior is version-specific and remains owned by Claude Code upstream.

## Bootstrap

- Start from `CHAT_INIT.md` and follow its minimum-sufficient task routing.
- Read `AGENTS.md` only when the current route or Playbook-maintenance task requires repository-maintainer governance.
- Use `PLAYBOOK_INDEX.json` only for machine-readable owner discovery when needed; it is routing-only metadata.
- If multiple agent-instruction surfaces are loaded, treat overlapping bootstrap text as compatibility handoff only, never as parallel authority.
- This adapter does not grant repository write, runtime execution, credential, deployment, external-service, or completion authority.

## Authority boundary

If this file or the host's native behavior conflicts with current repository canonical governance, the current canonical governance wins. Narrow or stop rather than inventing an adapter fallback, and do not duplicate Project AI mode, repository execution, validation, model-selection, materialization, or other normative policy here.
