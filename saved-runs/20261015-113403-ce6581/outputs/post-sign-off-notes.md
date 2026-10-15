# Post-sign-off notes: run 20261015-113403-ce6581

Added after the auditor signed off (Team 9, 2026-10-15), in response to a review
of the signed pack. Nothing here was recomputed by an agent, and no risk,
rating, scope or sample of the signed pack was changed. The auditor's decisions
on challenges #4 and #5 and the Team 9 sign-off stand as recorded in
`review.md`; no new approval was needed.

## 1. Sample size: 686 sample rows, 612 unique transactions

`planning-memo.md` said "Total sampled transactions: 686". That figure counts
**sample rows** across the ten `samples/T-*.csv` files, and some transactions
are drawn by more than one test. After sign-off the sentence was amended to:

> Total sample rows: 686, covering 612 unique transactions. Transactions may
> appear in multiple tests.

The wording changed and both figures are unchanged. The unique count (612
distinct `row_id` values) was added to `pack-figures.json`, and the QA number,
trace and samples checks were re-run on the amended pack: all pass. The pack
builder now writes this wording itself.

## 2. Six Contracts Finder notices with the buyer name in capitals

The original analysis keeps an **exact** buyer-name match ("West Berkshire
Council" or "West Berkshire"), as CLAUDE.md specifies, and that is the basis of
the signed pack. Six notices name the buyer "WEST BERKSHIRE COUNCIL" in capitals
and are excluded. The cleaning log records this, and the six are listed in
`analytics-full/notices-dropped-case-variant.csv`. **Their exclusion is a data
limitation of this pack.**

A sensitivity check was run after sign-off with
`tools/sensitivity_case_variant.py` (Python only, no agent). It re-runs the
analysis with a case-insensitive match. The six notices affect only the three
contract tests, so it replaces just those in a copy of this run's outputs. It
then rebuilds the register and the pack from this run's own `risk-ratings.json`
and `audit-plan.json`. Two controls back the comparison: the exact-match leg
reproduces this run's three contract tests, and rebuilding the signed run
reproduces its samples. The evidence is in
`analytics-full/sensitivity-case-variant.md` and `.json`.

| Measure | As signed | Including the six notices |
| --- | --- | --- |
| Council notices kept | 135 | 141 |
| General procurement suppliers with no notice found | 186 | 185 |
| Their annualised estimate | £97,905,911.80 | £97,868,511.80 |
| Spend in the window with suppliers whose every notice had ended | £236,349.86 | £243,364.42 |
| Suppliers compared on spend against award / flagged | 22 / 12 | 23 / 12 |

What the rebuilt pack shows:

- **Ratings and scope:** no risk's likelihood, impact, uplift, scope or status changes.
- **Samples:** 12 of the 13 tests draw exactly the same transactions. **T-06-1 (R-06)
  would draw 3 different transactions out of 13.** The size stays at 13. The
  `row_id` values added and removed are listed in the JSON evidence.

This check does not change the signed pack. If the six notices are confirmed to
be the council's own, a future run should match the buyer name
case-insensitively, and T-06-1's sample should be redrawn.

## 3. Wording that predates the sign-off

`review.md` keeps the QA verdict "READY FOR SIGN-OFF" and `challenges.md` keeps
#4 and #5 "for the auditor", as records of the time they were written. Two
status notes were added: one under the verdict in `review.md` ("Status after
sign-off: signed off by Team 9 (Internal auditor) on 2026-10-15") and an
"Auditor decisions at sign-off" section at the end of `challenges.md`, which
quotes the auditor's decisions on #4 and #5. On the website, the lead's report is
now headed "Lead's report · before sign-off", with the final status beside it.
