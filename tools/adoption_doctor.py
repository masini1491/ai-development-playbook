#!/usr/bin/env python3
"""Read-only adoption/readability doctor for projects using ai-development-playbook."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

MIN_PYTHON = (3, 11)
PLAYBOOK_REPO = "masini1491/ai-development-playbook"
BASELINE_ASSIGN_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:playbook\s+baseline|baseline|ref)\s*[:：]\s*`?(main|v\d+\.\d+\.\d+)`?\s*[。.]?\s*$"
)
VERSION_TOKEN_RE = re.compile(r"`?(v\d+\.\d+\.\d+)`?")
FIELD_RE_TEMPLATE = r"(?im)^\s*[-*]\s*{label}\s*:\s*(.+?)\s*$"
PATHISH_RE = re.compile(r"^[A-Za-z0-9_.\-/]+$")
PLACEHOLDER_MARKERS = (
    "<path / document / source>",
    "<TASKS.md / equivalent / none>",
    "<command / document / manual gate / none>",
    "<rules / none>",
)


@dataclass(frozen=True, order=True)
class Finding:
    severity_rank: int
    code: str
    message: str

    @property
    def severity(self) -> str:
        return {0: "FAIL", 1: "WARN", 2: "INFO", 3: "PASS"}[self.severity_rank]


def _finding(severity: str, code: str, message: str) -> Finding:
    ranks = {"FAIL": 0, "WARN": 1, "INFO": 2, "PASS": 3}
    return Finding(ranks[severity], code, message)


def _strip_inline_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def _extract_field(text: str, label: str) -> str | None:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(label=re.escape(label)))
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _baseline_findings(text: str) -> list[Finding]:
    explicit = sorted(set(BASELINE_ASSIGN_RE.findall(text)))
    if len(explicit) == 1:
        return [_finding("PASS", "BASELINE_EXPLICIT", f"Explicit Playbook baseline: {explicit[0]}")]
    if len(explicit) > 1:
        return [_finding("WARN", "BASELINE_AMBIGUOUS", f"Multiple explicit Playbook baselines declared: {', '.join(explicit)}")]

    mentions = set()
    if re.search(r"(?<![\w/])main(?![\w/])", text):
        mentions.add("main")
    mentions.update(VERSION_TOKEN_RE.findall(text))
    if mentions:
        return [_finding("WARN", "BASELINE_NOT_EXPLICIT", f"Playbook baseline is mentioned but not declared as one explicit value: {', '.join(sorted(mentions))}")]
    return [_finding("WARN", "BASELINE_MISSING", "No recognizable Playbook baseline declaration found.")]


def _coordination_findings(root: Path, text: str) -> list[Finding]:
    value = _extract_field(text, "Current coordination surface")
    if value is None:
        return [_finding("WARN", "COORDINATION_UNDECLARED", "Project-specific minimum contract does not declare a current coordination surface.")]
    value = _strip_inline_code(value)
    if any(marker in value for marker in PLACEHOLDER_MARKERS) or value.startswith("<"):
        return [_finding("WARN", "COORDINATION_PLACEHOLDER", f"Current coordination surface still contains a placeholder: {value}")]
    if value.lower() == "none":
        return [_finding("PASS", "COORDINATION_NONE", "Current coordination surface is explicitly none.")]
    if PATHISH_RE.match(value):
        target = (root / value).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return [_finding("FAIL", "COORDINATION_OUTSIDE_ROOT", f"Declared coordination surface escapes repository root: {value}")]
        if not target.is_file():
            return [_finding("FAIL", "COORDINATION_TARGET_MISSING", f"Declared coordination surface does not exist: {value}")]
        return [_finding("PASS", "COORDINATION_TARGET", f"Declared coordination surface exists: {value}")]
    return [_finding("WARN", "COORDINATION_UNPARSED", f"Could not deterministically resolve coordination surface declaration: {value}")]


def _validation_findings(text: str) -> list[Finding]:
    value = _extract_field(text, "Required validation")
    if value is None:
        return [_finding("WARN", "VALIDATION_UNDECLARED", "Project-specific minimum contract does not declare required validation.")]
    value = _strip_inline_code(value)
    if any(marker in value for marker in PLACEHOLDER_MARKERS) or value.startswith("<"):
        return [_finding("WARN", "VALIDATION_PLACEHOLDER", f"Required validation still contains a placeholder: {value}")]
    if value.lower() == "none":
        return [_finding("INFO", "VALIDATION_NONE", "Required validation is explicitly none.")]
    return [_finding("PASS", "VALIDATION_DECLARED", f"Required validation is declared: {value}")]


def check_project(root: Path) -> list[Finding]:
    root = root.resolve()
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return [_finding("FAIL", "AGENTS_MISSING", "AGENTS.md is required for repository-declared Playbook adoption.")]

    text = agents.read_text(encoding="utf-8")
    findings: list[Finding] = [_finding("PASS", "AGENTS_PRESENT", "AGENTS.md exists.")]

    if PLAYBOOK_REPO in text:
        findings.append(_finding("PASS", "PLAYBOOK_DECLARED", f"Playbook adoption declaration references {PLAYBOOK_REPO}."))
    else:
        findings.append(_finding("FAIL", "PLAYBOOK_DECLARATION_MISSING", f"AGENTS.md does not reference {PLAYBOOK_REPO}."))

    if "CHAT_INIT.md" in text:
        findings.append(_finding("PASS", "BOOTSTRAP_ROUTED", "AGENTS.md routes new sessions to CHAT_INIT.md."))
    else:
        findings.append(_finding("FAIL", "BOOTSTRAP_ROUTING_MISSING", "AGENTS.md does not route Playbook adoption through CHAT_INIT.md."))

    findings.extend(_baseline_findings(text))

    present = sorted(marker for marker in PLACEHOLDER_MARKERS if marker in text)
    if present:
        findings.append(_finding("WARN", "PLACEHOLDERS_PRESENT", f"Known minimal-adoption placeholders remain: {', '.join(present)}"))
    else:
        findings.append(_finding("PASS", "PLACEHOLDERS_CLEARED", "Known minimal-adoption placeholders are cleared."))

    findings.extend(_coordination_findings(root, text))
    findings.extend(_validation_findings(text))

    has_heading = bool(re.search(r"(?im)^#{1,6}\s+Authority boundary\b", text))
    has_project_authority = "project-specific authority" in text or ("本 repository" in text and "權威" in text)
    if has_heading and has_project_authority:
        findings.append(_finding("PASS", "PROJECT_AUTHORITY_MARKER", "Project-specific authority boundary marker is present."))
    else:
        findings.append(_finding("WARN", "PROJECT_AUTHORITY_UNCLEAR", "No clear project-specific authority boundary marker was detected; semantic authority is not proven by this doctor."))

    markers = (
        "採用 Playbook 本身不會新增",
        "adoption does not grant",
        "does not grant",
        "不代表取得額外",
    )
    if any(marker.lower() in text.lower() for marker in markers):
        findings.append(_finding("PASS", "NO_AUTHORITY_EXPANSION_MARKER", "Playbook adoption includes a no-authority-expansion marker."))
    else:
        findings.append(_finding("WARN", "NO_AUTHORITY_EXPANSION_UNCLEAR", "No explicit marker was detected saying Playbook adoption does not expand write/execution/deployment/secret authority."))

    return sorted(findings)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run read-only deterministic checks for ai-development-playbook project adoption.")
    parser.add_argument("project", type=Path, help="Target project repository root.")
    return parser


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        required = ".".join(str(part) for part in MIN_PYTHON)
        actual = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"ERROR TOOLCHAIN Python {required}+ required; found {actual}", file=sys.stderr)
        return 2

    args = _build_parser().parse_args(argv)
    root = args.project.resolve()
    if not root.is_dir():
        print(f"ERROR RUNTIME Project root is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        findings = check_project(root)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR RUNTIME {exc}", file=sys.stderr)
        return 2

    counts = {"FAIL": 0, "WARN": 0, "INFO": 0, "PASS": 0}
    for item in findings:
        counts[item.severity] += 1
        print(f"{item.severity} {item.code} {item.message}")

    result = "FAIL" if counts["FAIL"] else "PASS"
    print(f"RESULT {result}: {counts['FAIL']} fail(s), {counts['WARN']} warning(s), {counts['INFO']} info, {counts['PASS']} pass(es)")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
