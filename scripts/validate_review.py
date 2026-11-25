#!/usr/bin/env python3
"""Structural integrity checks for a frozen 559-record systematic-review ledger.

No scientific decisions are inferred. This is NOT a PRISMA generator.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

EXPECTED_IDS = set(range(1, 560))
DECISIONS = {"INCLUDE", "EXCLUDE", "UNCLEAR"}
FINAL_DECISIONS = {"INCLUDE", "EXCLUDE"}
RECORD_STATES = {"RETAINED", "DUPLICATE_REMOVED", "OTHER_REMOVED"}
RETRIEVAL_STATES = {"RETRIEVED", "NOT_RETRIEVED", "NOT_SOUGHT"}
MINIMUM = {"record_id", "reviewer_1_decision", "reviewer_2_decision",
           "adjudicated_decision"}
FINAL_FIELDS = {"record_status", "report_id", "study_id", "retrieval_status",
                "full_text_decision", "exclusion_reason", "evidence_anchor"}


def clean(value):
    return (value or "").strip().upper()


def assess(rows, columns, require_final=False):
    errors = []
    blockers = []
    missing = sorted(MINIMUM - set(columns))
    if missing:
        return {"status": "INVALID", "errors": ["Missing fields: " + ", ".join(missing)],
                "final_prisma_ready": False}

    ids = []
    for index, row in enumerate(rows, start=2):
        try:
            ids.append(int((row.get("record_id") or "").strip()))
        except ValueError:
            errors.append(f"Line {index}: invalid record_id")
    duplicates = sorted(i for i, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"Duplicate internal IDs: {duplicates[:20]}")
    absent = sorted(EXPECTED_IDS - set(ids))
    unexpected = sorted(set(ids) - EXPECTED_IDS)
    if len(rows) != 559 or absent or unexpected:
        errors.append(f"Corpus mismatch: rows={len(rows)}, missing IDs={absent[:20]}, "
                      f"unexpected IDs={unexpected[:20]}")

    for col, allowed in [("reviewer_1_decision", DECISIONS),
                         ("reviewer_2_decision", DECISIONS),
                         ("adjudicated_decision", FINAL_DECISIONS),
                         ("record_status", RECORD_STATES),
                         ("retrieval_status", RETRIEVAL_STATES),
                         ("full_text_decision", FINAL_DECISIONS)]:
        if col not in columns:
            continue
        invalid = [row.get("record_id") for row in rows
                   if clean(row.get(col)) and clean(row.get(col)) not in allowed]
        if invalid:
            errors.append(f"Invalid {col} on records: {invalid[:20]}")

    reviewer_pairs = sum(
        clean(row.get("reviewer_1_decision")) in DECISIONS and
        clean(row.get("reviewer_2_decision")) in DECISIONS
        for row in rows
    )
    adjudicated = sum(clean(row.get("adjudicated_decision")) in FINAL_DECISIONS
                      for row in rows)
    pending_review = len(rows) - reviewer_pairs
    pending_adjudication = len(rows) - adjudicated

    if reviewer_pairs < 559:
        blockers.append(f"{pending_review} rows lack authenticated paired reviewer decisions")
    if pending_adjudication:
        blockers.append(f"{pending_adjudication} rows lack final adjudication")
    if FINAL_FIELDS - set(columns):
        blockers.append("Missing PRISMA report-stage columns: " +
                        ", ".join(sorted(FINAL_FIELDS - set(columns))))
    else:
        for row in rows:
            rid = row["record_id"]
            state = clean(row.get("record_status"))
            if not state:
                blockers.append(f"Record {rid}: record_status not documented")
                continue
            if state != "RETAINED":
                if not (row.get("evidence_anchor") or "").strip():
                    blockers.append(f"Record {rid}: removal provenance missing")
                continue
            if not (row.get("report_id") or "").strip():
                blockers.append(f"Record {rid}: report_id missing")
            retrieval = clean(row.get("retrieval_status"))
            if not retrieval:
                blockers.append(f"Record {rid}: retrieval_status missing")
            if retrieval == "RETRIEVED":
                decision = clean(row.get("full_text_decision"))
                if not decision:
                    blockers.append(f"Record {rid}: full_text_decision missing")
                elif decision == "EXCLUDE" and not (row.get("exclusion_reason") or "").strip():
                    blockers.append(f"Record {rid}: exclusion reason missing")
                elif decision == "INCLUDE" and not (row.get("study_id") or "").strip():
                    blockers.append(f"Record {rid}: study_id missing")
            if not (row.get("evidence_anchor") or "").strip():
                blockers.append(f"Record {rid}: source evidence anchor missing")

    ready = not errors and not blockers and len(rows) == 559
    status = "INVALID" if errors else ("STRUCTURALLY_READY" if ready else "PROVISIONAL")
    result = {"status": status, "corpus_rows": len(rows), "unique_ids": len(set(ids)),
              "paired_review_rows": reviewer_pairs, "adjudicated_rows": adjudicated,
              "final_prisma_ready": ready, "errors": errors, "blockers": blockers[:40],
              "total_blockers": len(blockers),
              "warning": "Structural readiness does not authenticate votes, sources, search provenance, or PRISMA counts."}
    if require_final and not ready:
        result["status"] = "NOT_FINAL"
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--report", type=Path)
    p.add_argument("--require-final", action="store_true")
    args = p.parse_args()
    with args.ledger.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        result = assess(list(reader), reader.fieldnames or [], args.require_final)
    out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(out + "\n", encoding="utf-8")
    print(out)
    return 2 if result["errors"] else (3 if args.require_final and not result["final_prisma_ready"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
