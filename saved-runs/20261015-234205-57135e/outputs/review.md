# QA review: procurement audit planning pack

Pack version: v2 · Register revision: 1 (built 2026-10-16T00:02:33) · Reviewed: 2026-10-16 00:12 UTC

## Verdict: READY FOR SIGN-OFF

**Status after sign-off:** signed off by Team 9 (Internal auditor) on 2026-10-16; see Auditor sign-off below. The verdict above is the QA verdict at review time. The auditor's sign-off decisions were then applied as pack v3 on register revision 2, and all four checks were re-run and pass; see "Revision after sign-off" at the end.

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

## Revision after sign-off (pack v3, register revision 2)

The auditor's decisions recorded in the sign-off comments above were applied to the
pack. No agent was re-run: the inputs were edited as the auditor decided, and the
pack's own builders and QA scripts produced and checked the result. The signed v2
pack is kept unchanged on the server as `outputs-signed/`.

| Sign-off decision | Applied in | Change |
|---|---|---|
| #6: R-06 likelihood L3 (score 12) | `auditor-comments.md` (R-06: Amend), `risk-ratings.json` revision 2, `risk-register.md` revision 2 | R-06 L2 × I4 = 8 → L3 × I4 = 12 (Medium - High (Amber)). Scope and the T-06-1 sample are unchanged. The builder records the rating as an auditor override, with a build note that the rubric's L3 signal is shown by the eight per-supplier tags rather than a single aggregate metric |
| #4: test CPR-09, -12, -28, -47 and -58 at fieldwork | `audit-plan.json` T-10-1, `planning-memo.md` Limitations | T-10-1 gains a step for the five rules on the contracts obtained, and one PBC item. The five rules leave "rules not tested" (now 58 cited, 8 not tested). The memo states the scope limitation applies to the analytics only |
| #7: impact-scale basis confirmed | `planning-memo.md` Limitations | The memo records the auditor's confirmation (no score changes). The register header still lists DISC-01, because the builder marks it from history.json |

QA re-run on pack v3 (`scripts/checks/run_checks.py`, on the server, 2026-10-16):

```text
| Check   | Result | Detail
|---------|--------|--------
| quotes  | PASS   | 91 checked
| numbers | PASS   | 56 checked
| trace   | PASS   | 107 checked
| samples | PASS   | 451 checked

VERDICT: READY FOR SIGN-OFF
```

The 451 sample rows (377 unique transactions) are byte-for-byte the same as in the
signed v2 pack. Details are in `post-sign-off-notes.md`.

### Revision confirmation

- [x] The changes above apply the decisions recorded in my sign-off comments and nothing else.
- Name: Team 9
- Role: Internal auditor
- Date: 2026-10-16
