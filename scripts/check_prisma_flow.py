"""Check final PRISMA arithmetic; never impute missing counts."""
import json
import sys

def check(d):
    keys = ["records_identified","duplicates_removed","other_removed","records_screened","records_excluded","reports_sought","reports_not_retrieved","reports_assessed","included_reports","included_studies"]
    if any(type(d.get(k)) is not int or d[k] < 0 for k in keys):
        return ["Missing or invalid verified counts"]
    reasons = d.get("full_text_exclusions_by_reason")
    if not isinstance(reasons, dict) or any(type(v) is not int or v < 0 for v in reasons.values()):
        return ["Missing or invalid full-text exclusion reasons"]
    errors = []
    if d["records_identified"] - d["duplicates_removed"] - d["other_removed"] != d["records_screened"]:
        errors.append("Identification arithmetic mismatch")
    if d["reports_sought"] - d["reports_not_retrieved"] != d["reports_assessed"]:
        errors.append("Retrieval arithmetic mismatch")
    if d["reports_assessed"] - sum(reasons.values()) != d["included_reports"]:
        errors.append("Report eligibility arithmetic mismatch")
    if d["included_studies"] > d["included_reports"]:
        errors.append("Study/report mapping requires verification")
    if d["records_excluded"] > d["records_screened"]:
        errors.append("Record exclusions exceed screened records")
    return errors

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        errors = check(json.load(f))
    print(json.dumps({"arithmetic_errors": errors, "arithmetic_pass": not errors, "warning": "Arithmetic alone does not authenticate counts or record-report-study mappings."}, indent=2))
    sys.exit(bool(errors))
