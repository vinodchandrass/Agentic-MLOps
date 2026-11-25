# Agentic MLOps: systematic review reproducibility

Research companion to **Beyond Automation: A Systematic Survey of Adaptive Autonomy, Evidence Quality, and Operational Net Benefit in Agentic MLOps** (target: ACM Computing Surveys).

## Current scientific status (25 November 2026)
- Frozen historical Web of Science working corpus: **559 record identifiers**, not a finalized set of eligible studies.
- Historical tracking: **532 screening decisions, 27 unresolved**. Historical labels are *not* authenticated independent reviewer decisions.
- Four candidate empirical investigations underpin **15 descriptive outcome contrasts**; these are neither 15 independent studies nor a pooled meta-analysis.
- Final PRISMA identification/screening/eligibility/inclusion counts, full search provenance, independent reviewer adjudication, and source-level methodological assessments **are incomplete**.
- Two previously provided 559-row Reviewer A and Reviewer B spreadsheets were inspected in the research library: their **Independent decisions** sheets contained blank decision fields. These are screening templates, *not* 559 independent decisions from either reviewer. Separate completed human assessments are reportedly available, but their original vote artifacts remain to be located/authenticated.
- The recovered backlog contains 415 abstracts; a historical audit reports three supplementary abstracts, giving 418/559. Original supplement entries still require authentication.

## Purpose
This repository presently publishes **validation code, methodological documentation and aggregate audit results**. Do not infer from its existence that PRISMA is complete or the research has been independently verified. No Web of Science export, copyrighted PDFs, reviewer identities, unpublished manuscript, or confidential extraction data have been uploaded.

## Reproduce validation
```bash
python -m unittest discover -s tests -v
python scripts/validate_review.py --ledger path/to/authorized_local_ledger.csv --report validation.json
```
The command verifies schema, row IDs, decision statuses and arithmetic; it **does not fabricate missing votes or transform historical labels into final decisions**. Use `--require-final` for structural completeness checks only; it cannot authenticate reviewer decisions.

## Repository contents
- `docs/METHODOLOGY.md` — original protocol requirements, screening and appraisal boundaries.
- `docs/PRISMA_RECONCILIATION.md` — PRISMA 2020 mapping, open evidence gates, reconciliations.
- `docs/DATA_GOVERNANCE.md` — public release guardrails.
- `schemas/screening_ledger_columns.csv` — template field schema (not data).
- `scripts/validate_review.py` — strict validator.
- `tests/` — tests using **synthetic** records.
- `.github/workflows/` — Python test workflow.

## Pre-release gates
1. Recover original executable WoS search, date, indices, restrictions and deduplication provenance.
2. Authenticate two independent reviewer decisions and adjudication records against unique source records; do not score blanks as exclusions.
3. Confirm record-to-report-to-study crosswalk and source retrieval with exclusion reasons.
4. Complete primary-source extraction, methodological quality appraisal, final PRISMA 2020 checklist and PRISMA-S.
5. Review redistribution rights, confidentiality and blinded-review policies before public dataset or manuscript release.

**Citation/DOI:** not assigned. **Research quality target:** aspirational 9.5+/10, not yet achieved.

## Additional checks
```bash
python scripts/statistical_sensitivity.py
python scripts/check_prisma_flow.py schemas/prisma_flow_template.json
```
The provisional PRISMA template is intentionally rejected because counts are unknown. See `results/` for aggregate audits. Multiple studies may be described in one report; the crosswalk must be verified separately.
