"""Synthetic validator tests only. No actual AMLOps reviewer decisions are present."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_review import assess

COLUMNS = ["record_id", "reviewer_1_decision", "reviewer_2_decision", "adjudicated_decision"]


def synthetic():
    return [{"record_id": str(i), "reviewer_1_decision": "",
             "reviewer_2_decision": "", "adjudicated_decision": ""}
            for i in range(1, 560)]


class ReviewLedgerTests(unittest.TestCase):
    def test_preserves_559_ids_without_claiming_inclusion(self):
        result = assess(synthetic(), COLUMNS)
        self.assertEqual(result["status"], "PROVISIONAL")
        self.assertEqual(result["paired_review_rows"], 0)
        self.assertEqual(result["adjudicated_rows"], 0)
        self.assertFalse(result["final_prisma_ready"])

    def test_missing_record_detected(self):
        result = assess(synthetic()[:-1], COLUMNS)
        self.assertEqual(result["status"], "INVALID")
        self.assertTrue(result["errors"])

    def test_duplicates_detected(self):
        rows = synthetic()
        rows[-1]["record_id"] = "1"
        result = assess(rows, COLUMNS)
        self.assertEqual(result["status"], "INVALID")

    def test_zeros_are_not_exclusions(self):
        rows = synthetic()
        rows[0]["reviewer_1_decision"] = "0"
        result = assess(rows, COLUMNS)
        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["paired_review_rows"], 0)

    def test_partial_votes_not_agreement(self):
        rows = synthetic()
        rows[0]["reviewer_1_decision"] = "INCLUDE"
        result = assess(rows, COLUMNS)
        self.assertEqual(result["paired_review_rows"], 0)


if __name__ == "__main__":
    unittest.main()
