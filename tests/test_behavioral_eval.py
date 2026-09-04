from __future__ import annotations

import unittest

from tools import behavioral_eval


class BehavioralEvalTests(unittest.TestCase):
    def valid_record(self) -> dict[str, object]:
        return {
            "scenario_id": "BEH-008",
            "playbook_sha": "0" * 40,
            "run_time": "2026-09-05T00:00:00+08:00",
            "stimulus": "Review repository capability gaps.",
            "observed_actions": ["Read capability index", "Read canonical owner"],
            "response_reference": "conversation evidence retained by evaluator",
            "classification": "PASS",
            "classification_reason": "Negative claims were reconciled against canonical evidence.",
            "run_kind": "formal",
        }

    def test_valid_formal_record_passes(self) -> None:
        self.assertEqual([], behavioral_eval.validate_record(self.valid_record()))

    def test_unknown_scenario_fails(self) -> None:
        record = self.valid_record()
        record["scenario_id"] = "BEH-999"
        self.assertTrue(any("scenario_id" in item for item in behavioral_eval.validate_record(record)))

    def test_short_sha_fails(self) -> None:
        record = self.valid_record()
        record["playbook_sha"] = "abc123"
        self.assertTrue(any("playbook_sha" in item for item in behavioral_eval.validate_record(record)))

    def test_invalid_classification_fails(self) -> None:
        record = self.valid_record()
        record["classification"] = "MAYBE"
        self.assertTrue(any("classification" in item for item in behavioral_eval.validate_record(record)))

    def test_empty_observed_actions_fails(self) -> None:
        record = self.valid_record()
        record["observed_actions"] = []
        self.assertTrue(any("observed_actions" in item for item in behavioral_eval.validate_record(record)))

    def test_retrospective_requires_contract_sha(self) -> None:
        record = self.valid_record()
        record["run_kind"] = "retrospective"
        self.assertTrue(any("scenario_contract_sha" in item for item in behavioral_eval.validate_record(record)))
        record["scenario_contract_sha"] = "1" * 40
        self.assertEqual([], behavioral_eval.validate_record(record))

    def test_comparison_group_requires_fixed_inputs(self) -> None:
        first = self.valid_record()
        first["comparison_group"] = "g1"
        second = self.valid_record()
        second["comparison_group"] = "g1"
        second["playbook_sha"] = "2" * 40
        errors = behavioral_eval.validate_comparison_groups([first, second])
        self.assertEqual(1, len(errors))

    def test_summary_counts_classifications(self) -> None:
        records = []
        for classification in ("PASS", "PASS", "FAIL", "INCONCLUSIVE"):
            record = self.valid_record()
            record["classification"] = classification
            records.append(record)
        self.assertEqual(
            ["BEH-008: 2 PASS / 1 FAIL / 1 INCONCLUSIVE"],
            behavioral_eval.summarize(records),
        )


if __name__ == "__main__":
    unittest.main()
