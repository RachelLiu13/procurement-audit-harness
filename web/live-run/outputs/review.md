# QA review: procurement audit planning pack

Pack version: v3 · Register revision: 1 (built 2026-10-15T11:56:28) · Reviewed: 2026-10-15T12:09:33Z

## Verdict: READY FOR SIGN-OFF

## Check results (as printed by scripts/checks/run_checks.py)

```text
| Check   | Result | Detail
|---------|--------|--------
| quotes  | PASS   | 89 checked
| numbers | PASS   | 68 checked
| trace   | PASS   | 105 checked
| samples | PASS   | 686 checked

VERDICT: READY FOR SIGN-OFF

INFO  quotes: extract-rules verifier: ALL CHECKS PASSED (65 rules, 99 excluded, 0 warning(s))
INFO  quotes: register rule excerpts checked: 24
INFO  numbers: figures checked: 68; source values: 1104
INFO  trace: High risks (score >= 8): R-03 in, R-04 in, R-05 in, R-07 in, R-08 in
INFO  trace: challenges: 8
INFO  samples: sample rows: 686 in 10 file(s); row IDs in audit-program.md: 0
```

## Review history

| Version | quotes | numbers | trace | samples | Sent to |
|---|---|---|---|---|---|
| v1 | PASS | PASS | FAIL | PASS | challenger: QA v1: FAIL trace (challenges #1–#6 open); planner: QA v1: PASS |
| v2 | PASS | PASS | FAIL | PASS | challenger: QA v2: FAIL trace (challenges #7–#8 open); planner: QA v2: PASS |
| v3 | PASS | PASS | PASS | PASS | planner: QA v3: PASS |

## Challenges for the auditor

See `outputs/challenges.md` ("For the auditor"): 2 challenges, #4 and #5.

## Auditor sign-off

- [x] I have read planning-memo.md, risk-control-matrix.md, audit-program.md,
      challenges.md and this review.
- [x] I accept the challenges marked "for the auditor" as decided, or have
      recorded my decision on each below.
- Decision: Sign off
- Name: Team 9
- Role: Internal auditor
- Date: 2026-10-15
- Comments: Approved for this coursework demonstration. For challenge #4, retain the approved scope and defer the £1,000 clustering issue for future consideration given its comparatively low financial exposure. For challenge #5, retain R-08’s current rating because the available evidence does not establish that AUD-12 concerns the same control theme; reassess if further evidence confirms a link.
