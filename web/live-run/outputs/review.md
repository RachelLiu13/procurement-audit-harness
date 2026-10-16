# QA review: procurement audit planning pack

Pack version: v2 · Register revision: 1 (built 2026-10-16T00:02:33) · Reviewed: 2026-10-16 00:12 UTC

## Verdict: READY FOR SIGN-OFF

**Status after sign-off:** signed off by Team 9 (Internal auditor) on 2026-10-16; see Auditor sign-off below. The verdict above is the QA verdict at review time.

Final pack updated to implement the auditor's sign-off decisions. QA checks rerun and passed; samples unchanged.

## Check results (as printed by scripts/checks/run_checks.py)

```text
| Check   | Result | Detail
|---------|--------|--------
| quotes  | PASS   | 91 checked
| numbers | PASS   | 59 checked
| trace   | PASS   | 107 checked
| samples | PASS   | 451 checked

VERDICT: READY FOR SIGN-OFF

INFO  quotes: extract-rules verifier: ALL CHECKS PASSED (66 rules, 98 excluded, 3 warning(s))
INFO  quotes: register rule excerpts checked: 25
INFO  numbers: figures checked: 59; source values: 1041
INFO  trace: High risks (score >= 8): R-02 in, R-03 in, R-04 in, R-05 in, R-06 in, R-07 in
INFO  trace: challenges: 7
INFO  samples: sample rows: 451 in 10 file(s); row IDs in audit-program.md: 0
```

## Review history

| Version | quotes | numbers | trace | samples | Sent to |
|---|---|---|---|---|---|
| v1 | PASS | PASS | FAIL (challenges #1–#7 not closed, status 'open') | PASS | challenger: QA v1: FAIL trace; planner: QA v1: PASS |
| v2 | PASS | PASS | PASS | PASS | planner: QA v2: PASS |
| v2 (final, after PLANNER DONE v2 and CHALLENGER DONE) | PASS | PASS | PASS | PASS | lead, planner, challenger: QA DONE v2: READY FOR SIGN-OFF |

## Challenges for the auditor

See `outputs/challenges.md` ("For the auditor"): 3 challenges: #4, #6, #7.

## Auditor sign-off

- [x] I have read planning-memo.md, risk-control-matrix.md, audit-program.md,
      challenges.md and this review.
- [x] I accept the challenges marked "for the auditor" as decided, or have
      recorded my decision on each below.
- Decision: Sign off
- Name: Team 9
- Role: Internal auditor
- Date: 2026-10-16
- Comments: Approved for this coursework demonstration. #4: the contract-type scope limitation applies to the analytics only; at fieldwork, extend T-10-1 to test CPR-09, -12, -28, -47 and -58 on the contracts already requested. #6: accepted. All 8 flagged suppliers are tagged general_procurement, so R-06 likelihood should be L3 (score 12, Amber); scope and sample are unchanged because R-06 is already in scope and T-06-1 takes all 8 suppliers, so the re-rating is recorded here and carried into the next register revision. #7: Table 1 (Medium = 3) is confirmed as the basis for R-01, R-02, R-05 and R-10; no score changes. The 'not resolved' flag in the register header is a builder limitation and is noted in the memo's Limitations.
