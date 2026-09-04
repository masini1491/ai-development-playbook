from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from tools import adoption_doctor


class AdoptionDoctorTests(unittest.TestCase):
    def make_repo(self, files: dict[str, str]) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root

    def healthy_agents(self) -> str:
        return """# AGENTS.md

## AI Development Playbook baseline

本專案採用 `masini1491/ai-development-playbook` 作為共通 AI 開發基準。
Playbook baseline: `main`

新 session 讀取 `CHAT_INIT.md`。

## Authority boundary

本 repository 的正式 technical / governance source of truth 保存專案專屬權威。
project-specific authority 與 common Playbook 衝突，以 project-specific authority 為準。
採用 Playbook 本身不會新增 write / execution authority。

## Project-specific minimum contract

- Canonical technical source(s): `docs/ARCHITECTURE.md`
- Current coordination surface: `TASKS.md`
- Required validation: `python -m unittest`
- Project-specific exceptions or restrictions: `none`
"""

    def test_healthy_adoption_has_no_fail_or_warn(self) -> None:
        root = self.make_repo({
            "AGENTS.md": self.healthy_agents(),
            "TASKS.md": "# Tasks\n",
            "docs/ARCHITECTURE.md": "# Architecture\n",
        })
        findings = adoption_doctor.check_project(root)
        self.assertFalse([item for item in findings if item.severity in {"FAIL", "WARN"}])

    def test_official_minimal_template_can_become_doctor_clean(self) -> None:
        template_path = Path(__file__).resolve().parents[1] / "examples" / "minimal-project" / "AGENTS.md"
        text = template_path.read_text(encoding="utf-8")
        replacements = {
            "<path / document / source>": "`docs/ARCHITECTURE.md`",
            "<TASKS.md / equivalent / none>": "`TASKS.md`",
            "<command / document / manual gate / none>": "`python -m unittest`",
            "<rules / none>": "`none`",
        }
        for placeholder, value in replacements.items():
            self.assertIn(placeholder, text)
            text = text.replace(placeholder, value)

        root = self.make_repo({
            "AGENTS.md": text,
            "TASKS.md": "# Tasks\n",
            "docs/ARCHITECTURE.md": "# Architecture\n",
        })
        findings = adoption_doctor.check_project(root)
        problems = [item for item in findings if item.severity in {"FAIL", "WARN"}]
        self.assertFalse(problems, problems)

    def test_missing_agents_fails(self) -> None:
        root = self.make_repo({"README.md": "# Demo\n"})
        findings = adoption_doctor.check_project(root)
        self.assertEqual(["AGENTS_MISSING"], [item.code for item in findings])

    def test_missing_playbook_declaration_fails(self) -> None:
        root = self.make_repo({"AGENTS.md": "# AGENTS\n\nRead `CHAT_INIT.md`.\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("PLAYBOOK_DECLARATION_MISSING", codes)

    def test_missing_bootstrap_route_fails(self) -> None:
        text = self.healthy_agents().replace("新 session 讀取 `CHAT_INIT.md`。\n", "")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("BOOTSTRAP_ROUTING_MISSING", codes)

    def test_baseline_mention_without_explicit_assignment_warns(self) -> None:
        text = self.healthy_agents().replace("Playbook baseline: `main`", "需要最新規則時使用 `main`；可重現時 pin `v0.1.0`")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("BASELINE_NOT_EXPLICIT", codes)

    def test_multiple_explicit_baselines_warn(self) -> None:
        text = self.healthy_agents().replace("Playbook baseline: `main`", "Playbook baseline: `main`\nPlaybook baseline: `v0.1.0`")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("BASELINE_AMBIGUOUS", codes)

    def test_known_placeholders_warn(self) -> None:
        text = self.healthy_agents().replace("`docs/ARCHITECTURE.md`", "<path / document / source>")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("PLACEHOLDERS_PRESENT", codes)

    def test_missing_declared_coordination_surface_fails(self) -> None:
        root = self.make_repo({"AGENTS.md": self.healthy_agents()})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("COORDINATION_TARGET_MISSING", codes)

    def test_none_coordination_surface_is_valid(self) -> None:
        text = self.healthy_agents().replace("`TASKS.md`", "`none`")
        root = self.make_repo({"AGENTS.md": text})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("COORDINATION_NONE", codes)
        self.assertNotIn("COORDINATION_TARGET_MISSING", codes)

    def test_missing_authority_marker_warns(self) -> None:
        text = self.healthy_agents().replace("## Authority boundary", "## Project notes")
        text = text.replace("project-specific authority", "project rules")
        text = text.replace("本 repository 的正式 technical / governance source of truth 保存專案專屬權威。\n", "")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("PROJECT_AUTHORITY_UNCLEAR", codes)

    def test_missing_no_authority_expansion_marker_warns(self) -> None:
        text = self.healthy_agents().replace("採用 Playbook 本身不會新增 write / execution authority。\n", "")
        root = self.make_repo({"AGENTS.md": text, "TASKS.md": "# Tasks\n"})
        codes = [item.code for item in adoption_doctor.check_project(root)]
        self.assertIn("NO_AUTHORITY_EXPANSION_UNCLEAR", codes)

    def test_findings_are_stably_sorted(self) -> None:
        root = self.make_repo({"AGENTS.md": "# AGENTS\n"})
        findings = adoption_doctor.check_project(root)
        self.assertEqual(sorted(findings), findings)


if __name__ == "__main__":
    unittest.main()
