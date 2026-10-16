# Auditor decisions: procurement risk register

Register: `outputs/risk-register.md` · revision 2 · built 2026-10-16T00:40:54

Put **Approve**, **Amend** or **Reject** in Decision for every row. For Amend, say exactly what to change in Comment (e.g. "likelihood 2: the clustering is below its comparator"). Give a reason for Reject. Do not use the `|` character in a cell. The planner cannot start until every row has a decision and the register has been re-issued as a revision that applies them.

| Risk ID | Risk | L | I | Score | Band | Proposed scope | Decision | Comment |
|---|---|---|---|---|---|---|---|---|
| R-01 | Payments just below the £25,000 competition threshold | 2 | 3 | 6 | Moderate | in | Approve |  |
| R-02 | Payments just below the £173,100 Procurement Act threshold for goods and services | 3 | 3 | 9 | Medium - High (Amber) | in | Amend | Reduce likelihood from L4 to L3 (score 9, Amber). Clustering below £173,100 rests on only 3 payments vs 2 above, which is too thin for L4; keep in scope. Rely on R-03 for the split-window evidence so the two risks are not double-counted. |
| R-03 | Same-supplier payment windows that cross competition thresholds while each payment stays below | 4 | 5 | 20 | Extreme (Red) | in | Approve |  |
| R-04 | High-value general procurement suppliers with no Contracts Finder notice found | 3 | 5 | 15 | Extreme (Red) | in | Approve |  |
| R-05 | Repeated equal payments to the same supplier within 7 days | 3 | 3 | 9 | Medium - High (Amber) | in | Approve |  |
| R-06 | Spend with suppliers whose every matching notice ended before the spend window | 3 | 4 | 12 | Medium - High (Amber) | in | Amend | Raise likelihood from L2 to L3 (score 12, Amber), as decided at sign-off on challenge #6: all 8 flagged suppliers carry dominant_tag general_procurement in analytics.json, so the L3 condition is shown. Keep in scope; no other change. |
| R-07 | Annualised spend above the published award value for single-supplier notices | 2 | 5 | 10 | Medium - High (Amber) | in | Approve |  |
| R-08 | Recurring care and education placement payments crossing competition thresholds | 2 | 2 | 4 | Moderate | out | Approve |  |
| R-09 | Payments clustered just below the £1,000 quotation threshold | 3 | 2 | 6 | Moderate | out | Approve |  |
| R-10 | Waivers, exceptions and award approvals not testable from the spend data | 1 | 3 | 3 | Low (Green) | in | Approve |  |
| R-11 | No published tracker of agreed audit actions to confirm prior procurement findings are closed | 1 | 2 | 2 | Low (Green) | in | Approve |  |

## Other instructions

<!-- Instructions not tied to one row, e.g. "add a risk on ...". The risk-assessor quotes the line it acts on. -->
Resolve DISC-01: apply Table 1 (Medium = 3) as the skill specifies, re-check any scores affected, and state the resolution in the register header. Record in the plan that the "relevant threshold" tests (CPR-58 etc.) could not be run because the spend data has no contract-type field, and treat this as a scope limitation.
