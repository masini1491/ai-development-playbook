from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable

SCENARIO_IDS = {f"BEH-{index:03d}" for index in range(1, 10)}
CLASSIFICATIONS = {"PASS", "FAIL", "INCONCLUSIVE"}
RUN_KINDS = {"formal", "retrospective"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    scenario_id = record.get("scenario_id")
    if scenario_id not in SCENARIO_IDS:
        errors.append("scenario_id must be a current Behavioral Evaluation MVP ID")

    playbook_sha = record.get("playbook_sha")
    if not isinstance(playbook_sha, str) or not SHA_RE.fullmatch(playbook_sha):
        errors.append("playbook_sha must be a 40-character lowercase Git SHA")

    classification = record.get("classification")
    if classification not in CLASSIFICATIONS:
        errors.append("classification must be PASS, FAIL, or INCONCLUSIVE")

    run_kind = record.get("run_kind", "formal")
    if run_kind not in RUN_KINDS:
        errors.append("run_kind must be formal or retrospective")

    for field in ("run_time", "stimulus", "classification_reason"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    actions = record.get("observed_actions")
    if not isinstance(actions, list) or not actions or not all(isinstance(item, str) and item.strip() for item in actions):
        errors.append("observed_actions must be a non-empty list of strings")

    reference = record.get("response_reference")
    if not isinstance(reference, str) or not reference.strip():
        errors.append("response_reference must be a non-empty string")

    contract_sha = record.get("scenario_contract_sha")
    if run_kind == "retrospective":
        if not isinstance(contract_sha, str) or not SHA_RE.fullmatch(contract_sha):
            errors.append("retrospective runs require scenario_contract_sha")
    elif contract_sha is not None and (not isinstance(contract_sha, str) or not SHA_RE.fullmatch(contract_sha)):
        errors.append("scenario_contract_sha must be a 40-character lowercase Git SHA when provided")

    return errors


def load_record(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")
    return data


def validate_comparison_groups(records: Iterable[dict[str, Any]]) -> list[str]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        group = record.get("comparison_group")
        if isinstance(group, str) and group.strip():
            grouped[group].append(record)

    errors: list[str] = []
    for group, items in grouped.items():
        scenario_ids = {item.get("scenario_id") for item in items}
        playbook_shas = {item.get("playbook_sha") for item in items}
        stimuli = {item.get("stimulus") for item in items}
        if len(scenario_ids) != 1 or len(playbook_shas) != 1 or len(stimuli) != 1:
            errors.append(
                f"comparison_group {group!r} must keep scenario_id, playbook_sha, and stimulus fixed"
            )
    return errors


def summarize(records: Iterable[dict[str, Any]]) -> list[str]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        scenario_id = record.get("scenario_id")
        classification = record.get("classification")
        if scenario_id in SCENARIO_IDS and classification in CLASSIFICATIONS:
            counts[scenario_id][classification] += 1

    lines: list[str] = []
    for scenario_id in sorted(counts):
        counter = counts[scenario_id]
        lines.append(
            f"{scenario_id}: {counter['PASS']} PASS / {counter['FAIL']} FAIL / "
            f"{counter['INCONCLUSIVE']} INCONCLUSIVE"
        )
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Behavioral Evaluation run records and print a deterministic summary."
    )
    parser.add_argument("records", nargs="+", type=Path, help="JSON run-record paths")
    args = parser.parse_args(argv)

    loaded: list[dict[str, Any]] = []
    failed = False
    for path in args.records:
        try:
            record = load_record(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"FAIL {path}: {exc}")
            failed = True
            continue

        errors = validate_record(record)
        if errors:
            failed = True
            for error in errors:
                print(f"FAIL {path}: {error}")
        else:
            print(f"PASS {path}")
            loaded.append(record)

    group_errors = validate_comparison_groups(loaded)
    for error in group_errors:
        print(f"FAIL comparison: {error}")
        failed = True

    if loaded:
        print("SUMMARY")
        for line in summarize(loaded):
            print(line)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
