import unittest
from project_demo.workflow import accuracy, check_claim
from project_demo.common import read_json


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = read_json("data/scenarios.json")

    def test_all_cases(self):
        for case in self.data:
            self.assertEqual(
                check_claim(case["claim"], case["evidence"])["status"],
                case["expected_status"],
            )

    def test_exact_gain(self):
        row = self.data[0]
        self.assertEqual(check_claim(row["claim"], row["evidence"])["value"], 11.0)

    def test_no_testset_mixing(self):
        row = self.data[0]
        row["evidence"]["candidate"]["evaluation_set_sha256"] = "different"
        self.assertEqual(
            check_claim(row["claim"], row["evidence"])["status"], "unsupported"
        )

    def test_invalid_counts(self):
        for correct, total in [(1, 0), (101, 100), (-1, 10), (True, 10)]:
            with self.assertRaises(ValueError):
                accuracy({"correct": correct, "total": total})

    def test_duplicate_citation_requirement(self):
        row = self.data[0]
        row["claim"]["required_evidence"] = ["baseline", "baseline"]
        with self.assertRaises(ValueError):
            check_claim(row["claim"], row["evidence"])
