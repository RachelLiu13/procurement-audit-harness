# Lead's report · before sign-off

**The audit planning pack (v2) is ready for you to sign off.**

**Risks in scope:** 9 of 11. You approved 8 as written and amended R-02.
- **Extreme (Red):** R-03 (same-supplier payment windows that cross competition thresholds while each payment stays below) and R-04 (high-value suppliers with no Contracts Finder notice found).
- **Medium–High (Amber):** R-02, R-05, R-06 and R-07.
- **Moderate:** R-01.
- **Low (Green):** R-10 and R-11.
- **Out of scope, as you decided:** R-08 and R-09.

**Documents:**
- `outputs/planning-memo.md`
- `outputs/risk-control-matrix.md`
- `outputs/audit-program.md`

The targeted samples total 451 transactions across 10 files in `outputs/samples/`. Every sampled transaction was checked against the spend data. The samples flag risk indicators to look into, not wrongdoing.

**Challenges that need your decision (3 of 7).** The planner accepted and fixed the other four, and the challenger checked the fixes in v2.
- **#4, coverage:** Does your scope limit on rules that depend on contract type apply only to the data analysis, or to fieldwork as well? The pack tests CPR-50, -51, -21, -22 and -66 from the contracts it obtains. It leaves CPR-09, -12, -28, -47 and -58 untested, although a step could be added to T-10-1 to cover them.
- **#6, rating R-06:** Should the risk-assessor re-rate R-06's likelihood (currently 2)? The rating says spend data gives no general procurement breakdown. However, all 8 flagged suppliers are tagged `general_procurement` in `analytics.json`.
- **#7, rating:** You asked for DISC-01 (Medium impact = 3) to be resolved and stated in the register header. Revision 1 of the register still lists it as unresolved. Please confirm the basis for the ratings of R-01, R-02, R-05 and R-10 and have the register re-issued. The planning memo's Limitations section notes this.

**QA verdict: READY FOR SIGN-OFF.** All four checks passed on v2:

| Check | Items checked |
|---|---|
| Quotes | 91 |
| Numbers | 59 |
| Traceability | 107 |
| Samples | 451 |

Version 1 failed only the traceability check, because challenges #1–#7 were still open at that point. Every high risk (score 8 or more: R-02 to R-07) is in scope.

**Next step:** Please complete the sign-off block at the end of `outputs/review.md`. Record your decision on challenges #4, #6 and #7, then choose "Sign off" or "Return to the team". If you want #6 or #7 acted on, the risk-assessor will need to produce a new register revision and the pack will be rebuilt.
