# Post-sign-off notes: run 20261015-113403-ce6581

Added after the auditor signed off (Team 9, 2026-10-15), in response to a review
of the signed pack. The signed documents are not changed except for the two
status notes described in item 3. These notes clarify how to read the pack;
they do not change a risk, a rating, the scope or a sample.

## 1. Sample size: 686 sample rows, 612 unique transactions

`planning-memo.md` says "Total sampled transactions: 686". That figure is the
number of **sample rows** across the ten `samples/T-*.csv` files. Some
transactions are drawn by more than one test, so the rows cover **612 unique
transactions** (unique `row_id`). Drawing one transaction for several tests is
intended: each test examines it against a different control.

The pack builder (`.claude/skills/audit-program/build_pack.py`) now reports both
figures ("Total sample rows: 686, covering 612 unique transactions") and records
the unique count in `pack-figures.json`, where the QA number check verifies it.
Rebuilding this run's plan with the updated builder gives exactly those figures,
and the numbers, trace and samples checks still pass.

## 2. Six Contracts Finder notices with the buyer name in capitals

`scripts/clean.py` keeps notices whose Organisation Name is exactly
"West Berkshire Council" or "West Berkshire", as CLAUDE.md specifies. Six notices
name the buyer "WEST BERKSHIRE COUNCIL" in capitals and were left out. The
cleaning log records this, and the six are listed in
`analytics-full/notices-dropped-case-variant.csv`.

The exact-match rule was kept because it is the specified rule and the data was
analysed under it. To show whether it matters, the cleaning and analysis
scripts were re-run on the same data with a case-insensitive match that
includes the six notices:

| Measure | Exact match (as run) | Including the six notices |
| --- | --- | --- |
| Council notices kept | 135 | 141 |
| Notices active in the spend window | 61 | 62 |
| High-value general procurement suppliers with no notice found | 186 | 185 |
| Their annualised estimate | £97,905,911.80 | £97,868,511.80 |
| Spend in the window with suppliers whose every notice had ended | £236,349.86 | £243,364.42 |
| Suppliers in the spend-versus-award comparison | 22 | 23 |

One supplier (annualised estimate £37,400) moves from "no notice found" to
"notice found", which is 0.04% of the headline. 13 of the 78 headline metrics
change, each by the small amounts shown above. No risk's likelihood, impact, scope or sample
would change. **Conclusion:** the exclusion does not affect the plan. A future
run can include the six notices by matching the buyer name case-insensitively.

## 3. Wording that predates the sign-off

`review.md` still shows the QA verdict "READY FOR SIGN-OFF", and
`challenges.md` still marks #4 and #5 "for the auditor". Both are records of the
time they were written. To make the outcome clear, two status notes were added:

- `review.md`: under the verdict, "Status after sign-off: signed off by Team 9
  (Internal auditor) on 2026-10-15; see Auditor sign-off below."
- `challenges.md`: a closing section, "Auditor decisions at sign-off", that
  points to the auditor's decisions on #4 and #5 in `review.md` and quotes them.

The harness now adds both notes automatically whenever an auditor signs off.
