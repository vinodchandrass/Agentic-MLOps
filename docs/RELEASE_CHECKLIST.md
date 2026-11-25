# Release checklist

## Software-only snapshot
- Run `python -m unittest discover -s tests -v` and `python -m compileall -q scripts tests`.
- Run `python scripts/statistical_sensitivity.py`.
- Confirm citation authorship and rights-holder-approved software license before licensing or tagging a release.
- Cite the exact commit until a versioned release exists.

## Scientific archive (not yet complete)
- Authenticate original search history and independent reviewer decisions.
- Reconcile record/report/study mappings and final PRISMA counts.
- Verify primary-source extraction and claim-specific appraisal.
- Confirm redistribution permissions and anonymization before depositing any data.
- Archive the approved version and obtain a DOI only after release authorization.

A successful software test suite does not certify scientific completeness. Unknown counts must remain null. No license or DOI is asserted by this checklist.
