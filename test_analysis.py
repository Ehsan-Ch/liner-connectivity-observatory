import unittest
from analysis import ROOT, compare, experiment, ranks
from build import render


class AnalysisTests(unittest.TestCase):
    def test_ties_use_average_ranks(self):
        self.assertEqual(ranks([7, 4, 9, 7]), [2.5, 4, 1, 2.5])

    def test_missing_values_remain_excluded_and_zero_is_observed(self):
        rows = [{"code": "a", "teu": 0, "index": 9}, {"code": "b", "teu": 3, "index": 2},
                {"code": "c", "teu": None, "index": 5}, {"code": "d", "teu": 1, "index": None}]
        out = compare(rows)
        self.assertEqual((out["matched"], out["index_only"], out["traffic_only"]), (2, 1, 1))
        self.assertEqual(out["rho"], -1)
        self.assertEqual(out["rows"][0]["gap"], 1)

    def test_degenerate_correlation_is_missing(self):
        self.assertIsNone(compare([{"code": "a", "teu": 3, "index": 4}])["rho"])

    def test_snapshot_coverage_and_published_report(self):
        result = experiment()
        for cohorts in result["cohorts"].values():
            for c in cohorts.values():
                self.assertEqual(c["eligible"], sum(c[k] for k in ("matched","index_only","traffic_only","neither")))
        self.assertEqual(result["cohorts"][2024]["All regions"]["matched"], 0)
        self.assertEqual((ROOT/"index.html").read_text(encoding="utf-8"), render())
