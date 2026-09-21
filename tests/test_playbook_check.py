from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from tools import playbook_check


class PlaybookCheckTests(unittest.TestCase):
    def make_repo(self, files: dict[str, str]) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root

    def adapter_text(self, host: str) -> str:
        return f"""# {host} bootstrap compatibility

This file is a thin repository bootstrap shim for {host}. It is not a Playbook authority and does not create a second current-state policy source.

## Bootstrap

- Start from `CHAT_INIT.md` and follow its minimum-sufficient task routing.
- Read `AGENTS.md` only when the current route or Playbook-maintenance task requires repository-maintainer governance.
- Use `PLAYBOOK_INDEX.json` only for machine-readable owner discovery when needed; it is routing-only metadata.
- If multiple agent-instruction surfaces are loaded, treat overlapping bootstrap text as compatibility handoff only, never as parallel authority.
- This adapter does not grant repository write, runtime execution, credential, deployment, external-service, or completion authority.

## Authority boundary

If this file or the host's native behavior conflicts with current repository canonical governance, the current canonical governance wins. Narrow or stop rather than inventing an adapter fallback, and do not duplicate Project AI mode, repository execution, validation, model-selection, materialization, or other normative policy here.
"""

    def valid_adapter_files(self) -> dict[str, str]:
        files = {"AGENTS.md": "# Governance\n"}
        for relative, host in playbook_check.CROSS_AGENT_ADAPTERS.items():
            files[relative] = self.adapter_text(host)
        return files

    def test_valid_local_link_passes(self) -> None:
        root = self.make_repo({"README.md": "[Context](AI_CONTEXT.md)\n", "AI_CONTEXT.md": "# Context\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_missing_local_link_fails(self) -> None:
        root = self.make_repo({"README.md": "[Old](OLD_FILE.md)\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["LOCAL_TARGET"], [item.code for item in diagnostics])

    def test_valid_local_heading_anchor_passes(self) -> None:
        root = self.make_repo({"README.md": "[Gate](DEBUG_VALIDATION.md#deterministic-enforcement-admission-gate)\n", "DEBUG_VALIDATION.md": "# Validation\n\n## Deterministic Enforcement Admission Gate\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_missing_local_heading_anchor_fails(self) -> None:
        root = self.make_repo({"README.md": "[Gate](DEBUG_VALIDATION.md#missing-gate)\n", "DEBUG_VALIDATION.md": "# Validation\n\n## Existing Gate\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["LOCAL_ANCHOR"], [item.code for item in diagnostics])

    def test_external_link_is_ignored(self) -> None:
        root = self.make_repo({"README.md": "[GitHub](https://github.com/example/repo)\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_link_inside_fence_is_ignored(self) -> None:
        root = self.make_repo({"README.md": "```markdown\n[Example](missing.md)\n```\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_section_router_accepts_heading_with_parenthetical_suffix(self) -> None:
        root = self.make_repo({"DEBUG_VALIDATION.md": "# Validation\n\n## Section Router\n\n- deterministic → `Gate`\n\n## Gate（Deterministic Gate）\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_section_router_accepts_heading_with_slash_suffix(self) -> None:
        root = self.make_repo({"DEBUG_VALIDATION.md": "# Validation\n\n## Section Router\n\n- retry → `Long Operation`\n\n## Long Operation／No-progress Wait Guard（Long-running Operation Supervision）\n"})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_section_router_requires_existing_heading(self) -> None:
        root = self.make_repo({"DEBUG_VALIDATION.md": "# Validation\n\n## Section Router\n\n- deterministic → `Existing Section`、`Missing Section`\n\n## Existing Section\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTER_SECTION"], [item.code for item in diagnostics])
        self.assertIn("Missing Section", diagnostics[0].message)

    def test_section_router_requires_owner_file(self) -> None:
        root = self.make_repo({"REPOSITORY_EXECUTION.md": "# Repo\n\n## Section Router\n\n- context → `AI_CONTEXT.md`\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTER_OWNER"], [item.code for item in diagnostics])

    def test_chat_init_router_requires_owner_file(self) -> None:
        root = self.make_repo({"CHAT_INIT.md": "# Init\n\n## 最低必要路由\n\n- validation\n  → `DEBUG_VALIDATION.md`\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTER_OWNER"], [item.code for item in diagnostics])

    def test_chat_init_declared_section_router_requires_owner_router(self) -> None:
        root = self.make_repo({
            "CHAT_INIT.md": "# Init\n\n## 最低必要路由\n\n- context\n  → `AI_CONTEXT.md` → Section Router\n",
            "AI_CONTEXT.md": "# Context\n\n## Existing Section\n",
        })
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTER_SECTION"], [item.code for item in diagnostics])
        self.assertIn("Declared Section Router missing", diagnostics[0].message)

    def test_chat_init_declared_section_router_passes_when_owner_has_router(self) -> None:
        root = self.make_repo({
            "CHAT_INIT.md": "# Init\n\n## 最低必要路由\n\n- context\n  → `AI_CONTEXT.md` → Section Router\n",
            "AI_CONTEXT.md": "# Context\n\n## Section Router\n\n- context → `Existing Section`\n\n## Existing Section\n",
        })
        self.assertEqual([], playbook_check.check_repository(root))

    def test_unclosed_fence_fails(self) -> None:
        root = self.make_repo({"README.md": "# Demo\n\n```text\nnot closed\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["FENCE_UNCLOSED"], [item.code for item in diagnostics])

    def test_diagnostics_are_stably_sorted(self) -> None:
        root = self.make_repo({"B.md": "[Missing](z.md)\n", "A.md": "[Missing](y.md)\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["A.md", "B.md"], [item.path for item in diagnostics])

    def test_chatgpt_custom_instructions_at_limit_passes(self) -> None:
        root = self.make_repo({"CHATGPT_CUSTOM_INSTRUCTIONS.txt": "a" * 1500})
        self.assertEqual([], playbook_check.check_repository(root))

    def test_chatgpt_custom_instructions_over_limit_fails(self) -> None:
        root = self.make_repo({"CHATGPT_CUSTOM_INSTRUCTIONS.txt": "a" * 1501})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["CHATGPT_CUSTOM_INSTRUCTIONS"], [item.code for item in diagnostics])
        self.assertIn("exceeds 1500 characters", diagnostics[0].message)

    def test_chatgpt_custom_instructions_markdown_fence_fails(self) -> None:
        root = self.make_repo({"CHATGPT_CUSTOM_INSTRUCTIONS.txt": "```text\nbootstrap\n```\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["CHATGPT_CUSTOM_INSTRUCTIONS"], [item.code for item in diagnostics])
        self.assertIn("copy-ready plain text", diagnostics[0].message)

    def test_cross_agent_adapters_pass_when_thin_and_aligned(self) -> None:
        root = self.make_repo(self.valid_adapter_files())
        self.assertEqual([], playbook_check.check_repository(root))

    def test_cross_agent_adapter_allows_host_specific_preamble(self) -> None:
        files = self.valid_adapter_files()
        files["CLAUDE.md"] = files["CLAUDE.md"].replace(
            "## Bootstrap",
            "Claude Code may need a host-specific bootstrap override before the shared contract.\n\n## Bootstrap",
        )
        root = self.make_repo(files)
        self.assertEqual([], playbook_check.check_repository(root))

    def test_cross_agent_adapter_missing_file_fails(self) -> None:
        files = self.valid_adapter_files()
        del files["GEMINI.md"]
        root = self.make_repo(files)
        diagnostics = playbook_check.check_repository(root)
        self.assertTrue(any(item.code == "CROSS_AGENT_ADAPTER" and "GEMINI.md" in item.message for item in diagnostics))

    def test_cross_agent_adapter_requires_authority_boundary(self) -> None:
        files = self.valid_adapter_files()
        files["CLAUDE.md"] = files["CLAUDE.md"].replace(
            "current canonical governance wins",
            "the adapter decides",
        )
        root = self.make_repo(files)
        diagnostics = playbook_check.check_repository(root)
        self.assertTrue(any(item.code == "CROSS_AGENT_ADAPTER" and "Authority boundary missing phrase" in item.message for item in diagnostics))

    def test_cross_agent_adapter_drift_fails(self) -> None:
        files = self.valid_adapter_files()
        files["GEMINI.md"] += "\nExtra host-specific policy.\n"
        root = self.make_repo(files)
        diagnostics = playbook_check.check_repository(root)
        self.assertTrue(any(item.code == "CROSS_AGENT_ADAPTER" and "adapters drift" in item.message.lower() for item in diagnostics))

    def test_machine_index_valid_targets_and_sections_pass(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [
                {"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "啟動順序", "kind": "contract"}
            ],
            "implementations": {"check": "tools/check.py"},
            "adapters": {
                "activation": "ACTIVATION_ADAPTERS.md",
                "claude_code_bootstrap": "CLAUDE.md",
                "gemini_cli_bootstrap": "GEMINI.md",
                "github_copilot_bootstrap": ".github/copilot-instructions.md",
            },
            "behavioral_regression": {"matrix": "evals/regression_matrix.json", "runner": "tools/check.py"},
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest, ensure_ascii=False),
            "CHAT_INIT.md": "# Init\n\n## 啟動順序\n",
            "ACTIVATION_ADAPTERS.md": "# Adapter\n",
            "CLAUDE.md": "# Claude Code\n",
            "GEMINI.md": "# Gemini CLI\n",
            ".github/copilot-instructions.md": "# GitHub Copilot\n",
            "tools/check.py": "",
            "evals/regression_matrix.json": "{}",
        })
        self.assertEqual([], playbook_check.check_repository(root))


    def test_machine_index_requires_cross_agent_adapter_pointers(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [
                {"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "啟動順序", "kind": "contract"}
            ],
            "adapters": {"activation": "ACTIVATION_ADAPTERS.md"},
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest, ensure_ascii=False),
            "CHAT_INIT.md": "# Init\n\n## 啟動順序\n",
            "ACTIVATION_ADAPTERS.md": "# Adapter\n",
            "CLAUDE.md": "# Claude Code\n",
            "GEMINI.md": "# Gemini CLI\n",
            ".github/copilot-instructions.md": "# GitHub Copilot\n",
        })
        diagnostics = playbook_check._check_machine_index(root)
        self.assertEqual(3, sum(item.code == "MANIFEST_ADAPTER" for item in diagnostics))
        self.assertTrue(any("claude_code_bootstrap" in item.message for item in diagnostics))
        self.assertTrue(any("gemini_cli_bootstrap" in item.message for item in diagnostics))
        self.assertTrue(any("github_copilot_bootstrap" in item.message for item in diagnostics))

    def test_machine_index_missing_target_fails(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [{"id": "missing", "owner": "MISSING.md", "kind": "contract"}],
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest),
            "CHAT_INIT.md": "# Init\n",
        })
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["MANIFEST_TARGET"], [item.code for item in diagnostics])

    def test_routing_closure_requires_chat_init_owner_in_manifest(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [{"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "啟動順序", "kind": "contract"}],
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest, ensure_ascii=False),
            "CHAT_INIT.md": "# Init\n\n## 啟動順序\n\n## 最低必要路由\n\n- context → `AI_CONTEXT.md`\n",
            "AI_CONTEXT.md": "# Context\n",
        })
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTING_CLOSURE"], [item.code for item in diagnostics])
        self.assertIn("AI_CONTEXT.md", diagnostics[0].message)

    def test_routing_closure_rejects_manifest_only_owner(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [
                {"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "啟動順序", "kind": "contract"},
                {"id": "context", "owner": "AI_CONTEXT.md", "kind": "contract"},
                {"id": "stale", "owner": "STALE.md", "kind": "contract"},
            ],
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest, ensure_ascii=False),
            "CHAT_INIT.md": "# Init\n\n## 啟動順序\n\n## 最低必要路由\n\n- context → `AI_CONTEXT.md`\n",
            "AI_CONTEXT.md": "# Context\n",
            "STALE.md": "# Stale\n",
        })
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["ROUTING_CLOSURE"], [item.code for item in diagnostics])
        self.assertIn("STALE.md", diagnostics[0].message)

    def test_routing_closure_passes_when_human_and_machine_owners_match(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [
                {"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "啟動順序", "kind": "contract"},
                {"id": "context", "owner": "AI_CONTEXT.md", "kind": "contract"},
            ],
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest, ensure_ascii=False),
            "CHAT_INIT.md": "# Init\n\n## 啟動順序\n\n## 最低必要路由\n\n- context → `AI_CONTEXT.md`\n",
            "AI_CONTEXT.md": "# Context\n",
        })
        self.assertEqual([], playbook_check.check_repository(root))

    def test_machine_index_missing_section_fails(self) -> None:
        manifest = {
            "schema_version": 1,
            "authority": "routing-only",
            "bootstrap": {"path": "CHAT_INIT.md"},
            "capabilities": [{"id": "bootstrap", "owner": "CHAT_INIT.md", "section": "Missing", "kind": "contract"}],
        }
        root = self.make_repo({
            "PLAYBOOK_INDEX.json": json.dumps(manifest),
            "CHAT_INIT.md": "# Init\n\n## Existing\n",
        })
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["MANIFEST_SECTION"], [item.code for item in diagnostics])


if __name__ == "__main__":
    unittest.main()
