# Post-sign-off notes: run 20261015-234205-57135e

Team 9 (Internal auditor) signed off pack v2 on 2026-10-16 and recorded decisions on
the three challenges left for the auditor (#4, #6, #7). Two of those decisions changed
the pack's content but were not yet reflected in it: R-06 was still rated L2 × I4 = 8,
and T-10-1 did not yet test the five rules the auditor asked to add. This note records
how the decisions were applied as **pack v3 on register revision 2**.

## What was done

No agent was re-run. Every change is an auditor decision, so no new judgment was
needed; the pack's builders and QA scripts did the rest, as in any revision.

1. **Backup.** The signed v2 outputs were copied unchanged to `outputs-signed/` in the
   run's workspace on the server.
2. **Inputs edited** to apply the decisions:
   - `auditor-comments.md`: R-06 decision changed from Approve to **Amend**, with the
     auditor's reason (challenge #6).
   - `risk-ratings.json`: revision 2. R-06 likelihood 2 → 3 (L3), justification citing
     the general procurement tag of each of the eight flagged suppliers in
     `analytics.json`; the revision block lists this as the only change.
   - `audit-plan.json` (pack v3): T-10-1 gains a step for CPR-09, CPR-12, CPR-28,
     CPR-47 and CPR-58 and one PBC item; those five rules leave `rules_not_tested`.
     The memo's Limitations now say the scope limitation applies to the analytics
     only, and record the auditor's confirmation of the impact-scale basis (DISC-01).
3. **Rebuilt** with `build_register.py` (revision checks: only the amended risk changed),
   `build_pack.py --gate` (gate open on revision 2) and `build_pack.py`.
4. **Checked** with `scripts/checks/run_checks.py`: quotes 91, numbers 56, trace 107,
   samples 451, all PASS; verdict READY FOR SIGN-OFF.

## Effect on the pack

| Item | Signed v2 | v3 |
|---|---|---|
| R-06 rating | L2 × I4 = 8, Medium - High (Amber) | L3 × I4 = 12, Medium - High (Amber) |
| Risks in scope | 9 (R-01–R-07, R-10, R-11) | unchanged |
| Rules cited / not tested | 53 / 13 | 58 / 8 |
| T-10-1 | award approval and tender handling | + CDP advertising, electronic tendering, statutory procedure, procurement report and sealing |
| PBC items | 21 | 22 |
| Sample | 451 rows, 377 unique transactions | identical files |

R-06's new score does not change its sample size: scores 8–14 share the same size
band, and T-06-1 already takes all eight flagged suppliers.

## Notes

- **Rubric build note on R-06.** The rubric's L3 condition expects a signal on an
  aggregate general procurement metric, and this test has none. The builder keeps the
  rating as an auditor override and says so under "Build notes" in the register.
- **DISC-01** is still listed in the register header as a conflict. The builder takes
  that from `history.json`, which records it as a discrepancy; changing it would mean
  re-running the findings-analyst, which this revision does not do.
- **Records of the time.** `lead-report-before-sign-off.md`, `lead-report-after-sign-off.md`,
  the challenge rows in `challenges.md` and the v1/v2 rows of `review.md` describe pack v2
  as it was when written. The current state is in `review.md` → "Revision after sign-off".
