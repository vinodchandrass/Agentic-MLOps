import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_prisma_flow import check

def fixture():
    # Synthetic example, not research results.
    return dict(records_identified=559, duplicates_removed=9,
                other_removed=0, records_screened=550, records_excluded=500,
                reports_sought=50, reports_not_retrieved=5, reports_assessed=45,
                full_text_exclusions_by_reason={"synthetic_reason":35},
                included_reports=10, included_studies=8)

class PrismaTests(unittest.TestCase):
    def test_consistent_synthetic_flow(self):
        self.assertEqual(check(fixture()), [])
    def test_unknown_is_not_zero(self):
        d=fixture()
        d["duplicates_removed"]=None
        self.assertTrue(check(d))
    def test_identification_mismatch(self):
        d=fixture()
        d["records_screened"]=551
        self.assertTrue(check(d))
    def test_retrieval_mismatch(self):
        d=fixture()
        d["reports_not_retrieved"]=6
        self.assertTrue(check(d))
    def test_exclusion_mismatch(self):
        d=fixture()
        d["full_text_exclusions_by_reason"]={"synthetic_reason":34}
        self.assertTrue(check(d))
    def test_study_count_mismatch(self):
        d=fixture()
        d["included_studies"]=11
        self.assertTrue(check(d))
    def test_negative_count(self):
        d=fixture()
        d["duplicates_removed"]=-1
        self.assertTrue(check(d))
