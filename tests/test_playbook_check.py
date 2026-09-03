from __future__ import annotations

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

    def test_unclosed_fence_fails(self) -> None:
        root = self.make_repo({"README.md": "# Demo\n\n```text\nnot closed\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["FENCE_UNCLOSED"], [item.code for item in diagnostics])

    def test_diagnostics_are_stably_sorted(self) -> None:
        root = self.make_repo({"B.md": "[Missing](z.md)\n", "A.md": "[Missing](y.md)\n"})
        diagnostics = playbook_check.check_repository(root)
        self.assertEqual(["A.md", "B.md"], [item.path for item in diagnostics])


if __name__ == "__main__":
    unittest.main()
