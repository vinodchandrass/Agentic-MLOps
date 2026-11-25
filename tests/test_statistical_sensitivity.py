import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from statistical_sensitivity import mcnemar_bounds, wilcoxon_min_exact_two_sided

class SensitivityTests(unittest.TestCase):
    def test_reported_bounds(self):
        r = mcnemar_bounds(150,127,119)
        self.assertEqual(r["feasible_tables"],24)
        self.assertAlmostEqual(r["min_p"],0.0078125)
        self.assertAlmostEqual(r["max_p"],0.34089094122009733)
        self.assertEqual(r["tables_p_below_0_05"],3)
    def test_equal_margins(self):
        self.assertEqual(mcnemar_bounds(10,5,5)["min_p"],1)
    def test_wilcoxon(self):
        self.assertEqual(wilcoxon_min_exact_two_sided(5),0.0625)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            mcnemar_bounds(10,11,5)
        with self.assertRaises(ValueError):
            wilcoxon_min_exact_two_sided(0)
