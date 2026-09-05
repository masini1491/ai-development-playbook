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
MATRIX_SCHEMA_VERSION = 1
MATRIX_AUTHORITY = "selection-only"


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


def load_regression_matrix(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("regression matrix top-level JSON value must be an object")
    return data


def validate_regression_matrix(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if matrix.get("schema_version") != MATRIX_SCHEMA_VERSION:
        errors.append(f"regression matrix schema_version must be {MATRIX_SCHEMA_VERSION}")
    if matrix.get("authority") != MATRIX_AUTHORITY:
        errors.append(f"regression matrix authority must be {MATRIX_AUTHORITY}")

    full_baseline = matrix.get("full_baseline")
    if not isinstance(full_baseline, list) or set(full_baseline) != SCENARIO_IDS or len(full_baseline) != len(SCENARIO_IDS):
        errors.append("regression matrix full_baseline must contain each current Behavioral Evaluation MVP ID exactly once")

    change_classes = matrix.get("change_classes")
    if not isinstance(change_classes, dict) or not change_classes:
        errors.append("regression matrix change_classes must be a non-empty object")
        return errors

    for change_class, scenario_ids in change_classes.items():
        if not isinstance(change_class, str) or not change_class.strip():
            errors.append("regression matrix change class names must be non-empty strings")
            continue
        if (
            not isinstance(scenario_ids, list)
            or not scenario_ids
            or not all(isinstance(item, str) for item in scenario_ids)
        ):
            errors.append(f"regression matrix change class {change_class!r} must contain a non-empty list of scenario IDs")
            continue
        if len(scenario_ids) != len(set(scenario_ids)):
            errors.append(f"regression matrix change class {change_class!r} contains duplicate scenario IDs")
        unknown = sorted(set(scenario_ids) - SCENARIO_IDS)
        if unknown:
            errors.append(
                f"regression matrix change class {change_class!r} contains unknown scenario IDs: {', '.join(unknown)}"
            )
    return errors


def select_regression_scenarios(matrix: dict[str, Any], change_class: str) -> list[str]:
    change_classes = matrix.get("change_classes")
    if not isinstance(change_classes, dict) or change_class not in change_classes:
        raise KeyError(change_class)
    scenario_ids = change_classes[change_class]
    if not isinstance(scenario_ids, list):
        raise ValueError(f"invalid scenario list for change class {change_class!r}")
    return list(scenario_ids)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Behavioral Evaluation run records and deterministic regression-selection metadata."
    )
    parser.add_argument("records", nargs="*", type=Path, help="JSON run-record paths")
    parser.add_argument("--matrix", type=Path, help="Regression matrix JSON path")
    parser.add_argument("--change-class", help="Print the scenario IDs selected for one regression change class")
    args = parser.parse_args(argv)

    failed = False
    matrix: dict[str, Any] | None = None
    if args.matrix is not None:
        try:
            matrix = load_regression_matrix(args.matrix)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"FAIL matrix {args.matrix}: {exc}")
            failed = True
        else:
            matrix_errors = validate_regression_matrix(matrix)
            if matrix_errors:
                failed = True
                for error in matrix_errors:
                    print(f"FAIL matrix {args.matrix}: {error}")
            else:
                print(f"PASS matrix {args.matrix}")

    if args.change_class:
        if matrix is None:
            print("FAIL matrix: --change-class requires a valid --matrix")
            failed = True
        elif not validate_regression_matrix(matrix):
            try:
                selected = select_regression_scenarios(matrix, args.change_class)
            except KeyError:
                print(f"FAIL matrix: unknown change class {args.change_class!r}")
                failed = True
            except ValueError as exc:
                print(f"FAIL matrix: {exc}")
                failed = True
            else:
                print(f"REGRESSION {args.change_class}: {' '.join(selected)}")

    if not args.records and args.matrix is None:
        parser.error("provide at least one run record or --matrix")

    loaded: list[dict[str, Any]] = []
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
