import unittest
from scripts.ameaf import support, exhaustive_check

class AMEAFTests(unittest.TestCase):
    def test_noncompensation(self):
        self.assertEqual(support("agent_net_benefit",dict(C="S",E="S",A="U",N="U")),0)
    def test_narrow_claim(self):
        self.assertEqual(support("observed_advantage",dict(C="S",E="S",A="NA",N="NA")),1)
    def test_required_na(self):
        with self.assertRaises(ValueError):
            support("agent_net_benefit",dict(C="S",E="S",A="NA",N="S"))
    def test_exhaustive(self):
        self.assertEqual(exhaustive_check()["valid_profiles"],1876)
