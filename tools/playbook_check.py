#!/usr/bin/env python3
"""Minimal deterministic checks for ai-development-playbook Markdown routing."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.parse import unquote

MIN_PYTHON = (3, 11)
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__"}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")
URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
HTML_ANCHOR_RE = re.compile(r"<(?:a|[^>]+)\b(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
CHAT_INIT_ROUTER_HEADING = "最低必要路由"


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    line: int
    code: str
    message: str


def _relative_display(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def _strip_link_destination(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    elif " " in target:
        target = target.split(None, 1)[0]
    return unquote(target)


def _is_external_or_nonfile(target: str) -> bool:
    if not target:
        return True
    if WINDOWS_DRIVE_RE.match(target):
        return False
    if target.startswith("//"):
        return True
    return bool(URL_SCHEME_RE.match(target))


def _resolve_target(source: Path, root: Path, target: str) -> tuple[Path, str | None]:
    path_part, sep, fragment = target.partition("#")
    if not path_part:
        return source, fragment if sep else None
    if path_part.startswith("/"):
        resolved = root / path_part.lstrip("/")
    else:
        resolved = source.parent / path_part
    return resolved.resolve(), fragment if sep else None


def _outside_fence_lines(text: str):
    open_fence: tuple[str, int] | None = None
    for line_no, line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            char = marker[0]
            if open_fence is None:
                open_fence = (char, len(marker))
            elif char == open_fence[0] and len(marker) >= open_fence[1]:
                open_fence = None
            continue
        if open_fence is None:
            yield line_no, line


def _github_slug_base(heading: str) -> str:
    heading = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.replace("`", "").lower().strip()
    slug_chars: list[str] = []
    for char in heading:
        if char.isspace():
            slug_chars.append("-")
        elif char.isalnum() or char in {"-", "_"}:
            slug_chars.append(char)
    return "".join(slug_chars)


def _markdown_anchor_ids(text: str) -> set[str]:
    anchors = {match.group(1) for match in HTML_ANCHOR_RE.finditer(text)}
    counts: dict[str, int] = {}
    for _line_no, line in _outside_fence_lines(text):
        heading_match = HEADING_RE.match(line)
        if not heading_match:
            continue
        base = _github_slug_base(heading_match.group(2).strip())
        if not base:
            continue
        count = counts.get(base, 0)
        slug = base if count == 0 else f"{base}-{count}"
        counts[base] = count + 1
        anchors.add(slug)
    return anchors


def _check_local_links(path: Path, root: Path, text: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    anchor_cache: dict[Path, set[str]] = {}
    for line_no, line in _outside_fence_lines(text):
        for match in MARKDOWN_LINK_RE.finditer(line):
            target = _strip_link_destination(match.group(1))
            if _is_external_or_nonfile(target):
                continue
            resolved, fragment = _resolve_target(path, root, target)
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                diagnostics.append(Diagnostic(_relative_display(path, root), line_no, "LOCAL_TARGET", f"Local target escapes repository root: {target}"))
                continue
            if not resolved.exists():
                diagnostics.append(Diagnostic(_relative_display(path, root), line_no, "LOCAL_TARGET", f"Missing local target: {target}"))
                continue
            if fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                anchors = anchor_cache.get(resolved)
                if anchors is None:
                    anchors = _markdown_anchor_ids(resolved.read_text(encoding="utf-8"))
                    anchor_cache[resolved] = anchors
                if fragment not in anchors:
                    diagnostics.append(Diagnostic(_relative_display(path, root), line_no, "LOCAL_ANCHOR", f"Missing Markdown heading anchor: {target}"))
    return diagnostics


def _heading_aliases(heading: str) -> set[str]:
    aliases = {heading}
    for separator in ("（", " (", "／"):
        if separator in heading:
            aliases.add(heading.split(separator, 1)[0].rstrip())
    return aliases


def _heading_map(lines: list[str]) -> dict[str, list[int]]:
    headings: dict[str, list[int]] = {}
    in_fence: tuple[str, int] | None = None
    for line_no, line in enumerate(lines, start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            char = marker[0]
            if in_fence is None:
                in_fence = (char, len(marker))
            elif char == in_fence[0] and len(marker) >= in_fence[1]:
                in_fence = None
            continue
        if in_fence is not None:
            continue
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = heading_match.group(2).strip()
            for alias in _heading_aliases(heading):
                headings.setdefault(alias, []).append(line_no)
    return headings


def _section_ranges(lines: list[str], heading_name: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or match.group(2).strip() != heading_name:
            continue
        level = len(match.group(1))
        end = len(lines)
        for next_index in range(index + 1, len(lines)):
            next_match = HEADING_RE.match(lines[next_index])
            if next_match and len(next_match.group(1)) <= level:
                end = next_index
                break
        ranges.append((index + 1, end))
    return ranges


def _check_section_router(path: Path, root: Path, text: str) -> list[Diagnostic]:
    lines = text.splitlines()
    headings = _heading_map(lines)
    diagnostics: list[Diagnostic] = []
    for start, end in _section_ranges(lines, "Section Router"):
        for index in range(start, end):
            line = lines[index]
            if "→" not in line:
                continue
            for target in CODE_SPAN_RE.findall(line):
                target = target.strip()
                if target.lower().endswith(".md"):
                    if any(ch in target for ch in "*?[]"):
                        continue
                    resolved = (root / target).resolve()
                    if not resolved.exists():
                        diagnostics.append(Diagnostic(_relative_display(path, root), index + 1, "ROUTER_OWNER", f"Missing canonical owner target: {target}"))
                    continue
                if target not in headings:
                    diagnostics.append(Diagnostic(_relative_display(path, root), index + 1, "ROUTER_SECTION", f"Missing heading target: {target}"))
    return diagnostics


def _check_chat_init_router(path: Path, root: Path, text: str) -> list[Diagnostic]:
    if path.name != "CHAT_INIT.md":
        return []
    lines = text.splitlines()
    diagnostics: list[Diagnostic] = []
    for start, end in _section_ranges(lines, CHAT_INIT_ROUTER_HEADING):
        for index in range(start, end):
            line = lines[index]
            if "→" not in line:
                continue
            for target in CODE_SPAN_RE.findall(line):
                target = target.strip()
                if not target.lower().endswith(".md"):
                    continue
                if any(ch in target for ch in "*?[]"):
                    continue
                resolved = (root / target).resolve()
                if not resolved.exists():
                    diagnostics.append(Diagnostic(_relative_display(path, root), index + 1, "ROUTER_OWNER", f"Missing canonical owner target: {target}"))
    return diagnostics


def _check_fences(path: Path, root: Path, text: str) -> list[Diagnostic]:
    open_fence: tuple[str, int, int] | None = None
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        char = marker[0]
        length = len(marker)
        if open_fence is None:
            open_fence = (char, length, line_no)
        elif char == open_fence[0] and length >= open_fence[1]:
            open_fence = None
    if open_fence is None:
        return []
    return [Diagnostic(_relative_display(path, root), open_fence[2], "FENCE_UNCLOSED", f"Unclosed Markdown fence opened with {open_fence[0] * open_fence[1]}")]


def check_repository(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    for path in _markdown_files(root):
        text = path.read_text(encoding="utf-8")
        diagnostics.extend(_check_local_links(path, root, text))
        diagnostics.extend(_check_section_router(path, root, text))
        diagnostics.extend(_check_chat_init_router(path, root, text))
        diagnostics.extend(_check_fences(path, root, text))
    return sorted(diagnostics)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run minimal deterministic Markdown checks for the playbook.")
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root. Defaults to the parent of tools/.")
    return parser


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        required = ".".join(str(part) for part in MIN_PYTHON)
        actual = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"ERROR TOOLCHAIN Python {required}+ required; found {actual}", file=sys.stderr)
        return 2
    args = _build_parser().parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR RUNTIME Repository root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        diagnostics = check_repository(root)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR RUNTIME {exc}", file=sys.stderr)
        return 2
    if diagnostics:
        for item in diagnostics:
            print(f"ERROR {item.code} {item.path}:{item.line}")
            print(item.message)
        print(f"FAIL: {len(diagnostics)} error(s)")
        return 1
    print("PASS: playbook deterministic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
