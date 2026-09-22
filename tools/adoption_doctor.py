#!/usr/bin/env python3
"""Read-only adoption/readability doctor for projects using ai-development-playbook."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
import re
import sys

MIN_PYTHON = (3, 11)
PLAYBOOK_REPO = "masini1491/ai-development-playbook"
ALLOWED_PROJECT_AI_MODES = ("ChatGPT-Only", "ChatGPT+Codex")
BASELINE_DECL_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?playbook\s+baseline\s*[:：]\s*(.+?)\s*$"
)
BASELINE_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
VERSION_TOKEN_RE = re.compile(r"`?(v\d+\.\d+\.\d+)`?")
SHA_TOKEN_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
PROJECT_AI_MODE_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?Project AI mode\s*[:：]\s*(.+?)\s*$")
LEGACY_CHATGPT_PROJECT_MODE_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?ChatGPT Project Mode\s*[:：]\s*(.+?)\s*$")
MARKDOWN_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
FIELD_RE_TEMPLATE = r"(?im)^\s*[-*]\s*{label}\s*:\s*(.+?)\s*$"
PLACEHOLDER_MARKERS = (
    "<ChatGPT-Only | ChatGPT+Codex>",
    "<path / document / source>",
    "<TASKS.md / equivalent / none>",
    "<command / document / manual gate / none>",
    "<rules / none>",
)
MARKDOWN_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
ADOPTION_BASELINE_SECTION = "AI Development Playbook baseline"
AUTHORITY_SECTION = "Authority boundary"
MINIMUM_CONTRACT_SECTION = "Project-specific minimum contract"


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


def _is_placeholder(value: str) -> bool:
    return any(marker in value for marker in PLACEHOLDER_MARKERS) or value.startswith("<")


def _without_fenced_markdown(text: str) -> str:
    """Preserve line structure while blanking fenced Markdown blocks."""
    rendered: list[str] = []
    active_fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        if active_fence is None:
            match = MARKDOWN_FENCE_RE.match(line)
            if match:
                token = match.group(1)
                active_fence = (token[0], len(token))
                rendered.append("\n" if line.endswith("\n") else "")
            else:
                rendered.append(line)
            continue

        char, minimum_length = active_fence
        closing = re.match(rf"^\s*{re.escape(char)}{{{minimum_length},}}\s*$", line.rstrip("\r\n"))
        if closing:
            active_fence = None
        rendered.append("\n" if line.endswith("\n") else "")
    return "".join(rendered)


def _named_markdown_sections(text: str, heading: str) -> list[str]:
    """Return active Markdown sections whose heading exactly matches the requested heading."""
    active_text = _without_fenced_markdown(text)
    lines = active_text.splitlines(keepends=True)
    sections: list[str] = []

    for index, line in enumerate(lines):
        match = MARKDOWN_HEADING_RE.match(line.rstrip("\r\n"))
        if not match or match.group(2).strip().casefold() != heading.casefold():
            continue

        level = len(match.group(1))
        end = len(lines)
        for next_index in range(index + 1, len(lines)):
            next_match = MARKDOWN_HEADING_RE.match(lines[next_index].rstrip("\r\n"))
            if next_match and len(next_match.group(1)) <= level:
                end = next_index
                break
        sections.append("".join(lines[index:end]))

    return sections


def _section_scope(
    text: str,
    heading: str,
    code_prefix: str,
    severity: str,
) -> tuple[str, list[Finding]]:
    sections = _named_markdown_sections(text, heading)
    if len(sections) == 1:
        return sections[0], []
    if not sections:
        return "", [
            _finding(
                severity,
                f"{code_prefix}_SECTION_MISSING",
                f"Required adoption section {heading!r} is missing; Doctor will not fall back to whole-file matching for this responsibility.",
            )
        ]
    return "", [
        _finding(
            severity,
            f"{code_prefix}_SECTION_AMBIGUOUS",
            f"Required adoption section {heading!r} appears {len(sections)} times; Doctor will not choose one implicitly.",
        )
    ]


def _valid_baseline_token(value: str) -> bool:
    if SHA40_RE.fullmatch(value):
        return True
    if not BASELINE_TOKEN_RE.fullmatch(value):
        return False
    if value in {".", ".."} or value.startswith(("/", ".")) or value.endswith(("/", ".")):
        return False
    if ".." in value or "//" in value or "@{" in value or value.endswith(".lock"):
        return False
    return True


def _baseline_findings(text: str) -> list[Finding]:
    declarations = [_strip_inline_code(value.rstrip("。.").strip()) for value in BASELINE_DECL_RE.findall(text)]
    if len(declarations) > 1:
        rendered = ", ".join(declarations)
        return [_finding("WARN", "BASELINE_AMBIGUOUS", f"Multiple explicit Playbook baseline declarations found: {rendered}")]
    if len(declarations) == 1:
        value = declarations[0]
        if _is_placeholder(value) or not _valid_baseline_token(value):
            return [_finding("WARN", "BASELINE_INVALID", f"Playbook baseline declaration is not a valid-looking Git ref / 40-character lowercase SHA: {value}")]
        return [_finding("PASS", "BASELINE_EXPLICIT", f"Explicit Playbook baseline: {value}")]

    mentions = set()
    if re.search(r"(?<![\w/])main(?![\w/])", text):
        mentions.add("main")
    mentions.update(VERSION_TOKEN_RE.findall(text))
    mentions.update(SHA_TOKEN_RE.findall(text))
    if mentions:
        return [_finding("WARN", "BASELINE_NOT_EXPLICIT", f"Playbook baseline is mentioned but not declared as one explicit `Playbook baseline:` value: {', '.join(sorted(mentions))}")]
    return [_finding("WARN", "BASELINE_MISSING", "No recognizable `Playbook baseline:` declaration found.")]


def _project_ai_mode_findings(text: str) -> list[Finding]:
    active_text = _without_fenced_markdown(text)
    modes = [_strip_inline_code(value) for value in PROJECT_AI_MODE_RE.findall(active_text)]
    legacy_modes = [_strip_inline_code(value) for value in LEGACY_CHATGPT_PROJECT_MODE_RE.findall(active_text)]

    if not modes:
        if legacy_modes:
            rendered = ", ".join(legacy_modes)
            return [_finding(
                "WARN",
                "PROJECT_AI_MODE_LEGACY_ONLY",
                "Legacy `ChatGPT Project Mode:` declaration found without current `Project AI mode:`; "
                f"migrate to one of {', '.join(ALLOWED_PROJECT_AI_MODES)} and keep project phase as a separate concept. "
                f"Legacy value(s): {rendered}",
            )]
        return [_finding(
            "WARN",
            "PROJECT_AI_MODE_UNDECLARED",
            "No `Project AI mode:` declaration found; select ChatGPT-Only or ChatGPT+Codex instead of inferring actor topology.",
        )]

    findings: list[Finding] = []
    if len(modes) > 1:
        findings.append(_finding(
            "FAIL",
            "PROJECT_AI_MODE_AMBIGUOUS",
            f"Multiple `Project AI mode:` declarations found: {', '.join(modes)}",
        ))
    else:
        mode = modes[0]
        if _is_placeholder(mode):
            findings.append(_finding(
                "WARN",
                "PROJECT_AI_MODE_PLACEHOLDER",
                f"Project AI mode still contains a placeholder: {mode}",
            ))
        elif mode not in ALLOWED_PROJECT_AI_MODES:
            findings.append(_finding(
                "FAIL",
                "PROJECT_AI_MODE_INVALID",
                f"Unsupported Project AI mode: {mode}; allowed values are {', '.join(ALLOWED_PROJECT_AI_MODES)}.",
            ))
        else:
            findings.append(_finding("PASS", "PROJECT_AI_MODE_DECLARED", f"Project AI mode is declared: {mode}"))

    if legacy_modes:
        findings.append(_finding(
            "WARN",
            "PROJECT_AI_MODE_LEGACY_COEXISTS",
            "Legacy `ChatGPT Project Mode:` coexists with `Project AI mode:`; rename/remove the legacy field so project phase and AI collaboration mode cannot be confused.",
        ))

    return findings


def _declaration_findings(text: str, label: str, code_prefix: str) -> list[Finding]:
    value = _extract_field(text, label)
    if value is None:
        return [_finding("WARN", f"{code_prefix}_UNDECLARED", f"Project-specific minimum contract does not declare {label}.")]
    value = _strip_inline_code(value)
    if _is_placeholder(value):
        return [_finding("WARN", f"{code_prefix}_PLACEHOLDER", f"{label} still contains a placeholder: {value}")]
    if not value:
        return [_finding("WARN", f"{code_prefix}_EMPTY", f"{label} is empty.")]
    return [_finding("PASS", f"{code_prefix}_DECLARED", f"{label} is declared: {value}")]


def _coordination_findings(root: Path, text: str) -> list[Finding]:
    value = _extract_field(text, "Current coordination surface")
    if value is None:
        return [_finding("WARN", "COORDINATION_UNDECLARED", "Project-specific minimum contract does not declare a current coordination surface.")]
    value = _strip_inline_code(value)
    if _is_placeholder(value):
        return [_finding("WARN", "COORDINATION_PLACEHOLDER", f"Current coordination surface still contains a placeholder: {value}")]
    if value.lower() == "none":
        return [_finding("PASS", "COORDINATION_NONE", "Current coordination surface is explicitly none.")]
    if not value:
        return [_finding("WARN", "COORDINATION_UNPARSED", "Current coordination surface is empty.")]

    declared = Path(value)
    if declared.is_absolute() or PureWindowsPath(value).is_absolute():
        return [_finding("FAIL", "COORDINATION_OUTSIDE_ROOT", f"Declared coordination surface must be repository-relative: {value}")]

    target = (root / declared).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return [_finding("FAIL", "COORDINATION_OUTSIDE_ROOT", f"Declared coordination surface escapes repository root: {value}")]
    if not target.is_file():
        return [_finding("FAIL", "COORDINATION_TARGET_MISSING", f"Declared coordination surface does not exist: {value}")]
    return [_finding("PASS", "COORDINATION_TARGET", f"Declared coordination surface exists: {value}")]


def _validation_findings(text: str) -> list[Finding]:
    value = _extract_field(text, "Required validation")
    if value is None:
        return [_finding("WARN", "VALIDATION_UNDECLARED", "Project-specific minimum contract does not declare required validation.")]
    value = _strip_inline_code(value)
    if _is_placeholder(value):
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

    baseline_text, section_findings = _section_scope(
        text,
        ADOPTION_BASELINE_SECTION,
        "ADOPTION_BASELINE",
        "FAIL",
    )
    findings.extend(section_findings)
    authority_text, section_findings = _section_scope(
        text,
        AUTHORITY_SECTION,
        "AUTHORITY_BOUNDARY",
        "WARN",
    )
    findings.extend(section_findings)
    minimum_contract_text, section_findings = _section_scope(
        text,
        MINIMUM_CONTRACT_SECTION,
        "MINIMUM_CONTRACT",
        "WARN",
    )
    findings.extend(section_findings)

    if PLAYBOOK_REPO in baseline_text:
        findings.append(_finding("PASS", "PLAYBOOK_DECLARED", f"Playbook adoption declaration references {PLAYBOOK_REPO}."))
    else:
        findings.append(_finding("FAIL", "PLAYBOOK_DECLARATION_MISSING", f"The {ADOPTION_BASELINE_SECTION!r} section does not reference {PLAYBOOK_REPO}."))

    if "CHAT_INIT.md" in baseline_text:
        findings.append(_finding("PASS", "BOOTSTRAP_ROUTED", "The adoption baseline section contains a CHAT_INIT.md bootstrap route marker for shared Playbook activation."))
    else:
        findings.append(_finding("FAIL", "BOOTSTRAP_ROUTING_MISSING", "The adoption baseline section has no CHAT_INIT.md bootstrap route marker for cases where shared Playbook activation is required."))

    findings.extend(_baseline_findings(baseline_text))
    findings.extend(_project_ai_mode_findings(baseline_text))

    scoped_adoption_text = "\n".join(
        part for part in (baseline_text, authority_text, minimum_contract_text) if part
    )
    present = sorted(marker for marker in PLACEHOLDER_MARKERS if marker in scoped_adoption_text)
    if present:
        findings.append(_finding("WARN", "PLACEHOLDERS_PRESENT", f"Known minimal-adoption placeholders remain in the structured adoption sections: {', '.join(present)}"))
    else:
        findings.append(_finding("PASS", "PLACEHOLDERS_CLEARED", "Known minimal-adoption placeholders are cleared from the structured adoption sections."))

    findings.extend(_declaration_findings(minimum_contract_text, "Canonical technical source(s)", "CANONICAL_SOURCES"))
    findings.extend(_coordination_findings(root, minimum_contract_text))
    findings.extend(_validation_findings(minimum_contract_text))
    findings.extend(_declaration_findings(minimum_contract_text, "Project-specific exceptions or restrictions", "PROJECT_EXCEPTIONS"))

    has_project_authority = "project-specific authority" in authority_text or ("本 repository" in authority_text and "權威" in authority_text)
    if authority_text and has_project_authority:
        findings.append(_finding("PASS", "PROJECT_AUTHORITY_MARKER", "Project-specific authority boundary marker is present in the Authority boundary section."))
    else:
        findings.append(_finding("WARN", "PROJECT_AUTHORITY_UNCLEAR", "No clear project-specific authority boundary marker was detected in the Authority boundary section; semantic authority is not proven by this doctor."))

    markers = (
        "採用 Playbook 本身不會新增",
        "adoption does not grant",
        "不代表取得額外",
        "不會跳過 Current Write Target",
    )
    if any(marker.lower() in authority_text.lower() for marker in markers):
        findings.append(_finding("PASS", "NO_AUTHORITY_EXPANSION_MARKER", "The Authority boundary section includes a no-authority-expansion marker."))
    else:
        findings.append(_finding("WARN", "NO_AUTHORITY_EXPANSION_UNCLEAR", "No explicit marker was detected in the Authority boundary section saying Playbook adoption does not expand write/execution/deployment/secret authority."))

    return sorted(findings)

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run read-only deterministic checks for ai-development-playbook project adoption. "
            "RESULT PASS means zero FAIL findings; Doctor-clean means zero FAIL and zero WARN."
        )
    )
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
    clean = "YES" if not counts["FAIL"] and not counts["WARN"] else "NO"
    print(f"RESULT {result}: {counts['FAIL']} fail(s), {counts['WARN']} warning(s), {counts['INFO']} info, {counts['PASS']} pass(es)")
    print(f"DOCTOR_CLEAN {clean}: clean means 0 FAIL and 0 WARN")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
