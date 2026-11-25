"""Reproduce available audits, not final scientific eligibility."""
import csv
import json
from pathlib import Path
from collections import Counter
from scripts.statistical_sensitivity import mcnemar_bounds, wilcoxon_min_exact_two_sided

ROOT = Path(__file__).resolve().parent

def read(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def main():
    records = read("data/provisional_screening_register.csv")
    gates = read("appraisal/provisional_evidence_gates.csv")
    ids = [int(r["record_id"]) for r in records]
    assert sorted(ids) == list(range(1,560)), "Corpus identity mismatch"
    priority = {r["record_id"] for r in records if r["priority_43"] == "YES"}
    assert len(priority) == 43
    assert len(gates) == 43 and {r["record_id"] for r in gates} == priority
    print(json.dumps({
        "status": "PROVISIONAL",
        "records": len(records),
        "priority_records": len(priority),
        "abstract_availability": Counter(r["abstract_available"] for r in records),
        "adjudication": Counter(r["independent_adjudication"] for r in records),
        "formal_appraisal": Counter(r["formal_rob"] for r in gates),
        "mcnemar_sensitivity": mcnemar_bounds(150,127,119),
        "wilcoxon_min_exact_p": wilcoxon_min_exact_two_sided(5),
        "final_prisma": None,
        "warning": "Reproduces available register summaries and sensitivity bounds only; source authentication and independent decisions remain outstanding."
    }, indent=2))

if __name__ == "__main__":
    main()
