# Audit planning memo: procurement, West Berkshire Council

Basis: risk register revision 2 (built 2026-10-16T00:40:54), auditor decisions in `outputs/auditor-comments.md`, plan `outputs/audit-plan.json`. Built 2026-10-16T00:40:56 by `.claude/skills/audit-program/build_pack.py`.

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier. A sampled transaction is selected because it carries an indicator, not because anything is assumed to be wrong with it.

## Objective

To conclude whether the council's controls over procurement route, aggregation of requirements, contract cover, extensions, variations, exceptions and award approvals operated as the Contract Procedure Rules require, for the approved risk indicators in the register: competition by value tier [CPR-54] [CPR-55] [CPR-56], the anti-splitting rule [CPR-11], extension and variation approvals [CPR-62] [CPR-63] [CPR-64], exceptions [CPR-20] and award approval tiers [CPR-50]. The audit also confirms the status of agreed actions from the Contract Letting and Accounts Payable audits [AUD-01] [AUD-11]. Results are risk indicators to investigate.

## Scope

9 risk(s) in scope, 2 out of scope, as decided by the auditor.

| Risk | L | I | Score | Band | Decision | Tests | Sample transactions |
|---|---|---|---|---|---|---|---|
| R-01: Payments just below the £25,000 competition threshold | 2 | 3 | 6 | Moderate | Approve | T-01-1 | 10 |
| R-02: Payments just below the £173,100 Procurement Act threshold for goods and services | 3 | 3 | 9 ‡ | Medium - High (Amber) | Amend | T-02-1 | 2 |
| R-03: Same-supplier payment windows that cross competition thresholds while each payment stays below | 4 | 5 | 20 | Extreme (Red) | Approve | T-03-1, T-03-2 | 266 |
| R-04: High-value general procurement suppliers with no Contracts Finder notice found | 3 | 5 | 15 | Extreme (Red) | Approve | T-04-1, T-04-2, T-04-3 | 80 |
| R-05: Repeated equal payments to the same supplier within 7 days | 3 | 3 | 9 ‡ | Medium - High (Amber) | Approve | T-05-1 | 39 |
| R-06: Spend with suppliers whose every matching notice ended before the spend window | 3 | 4 | 12 ‡ | Medium - High (Amber) | Amend | T-06-1 | 13 |
| R-07: Annualised spend above the published award value for single-supplier notices | 2 | 5 | 10 ‡ | Medium - High (Amber) | Approve | T-07-1 | 28 |
| R-10: Waivers, exceptions and award approvals not testable from the spend data | 1 | 3 | 3 | Low (Green) | Approve | T-10-1, T-10-2 | 13 |
| R-11: No published tracker of agreed audit actions to confirm prior procurement findings are closed | 1 | 2 | 2 | Low (Green) | Approve | T-11-1 | 0 |

Out of scope:

- R-08: approved as out of scope
- R-09: approved as out of scope

## Approach

Targeted testing over the full population of expenditure the council publishes under the transparency rule [CPR-04] for the spend window starting 2026-05-01 and ending 2026-07-31: 8,534 payments after exclusions, worth £66,778,105 [A1]. Samples are drawn by the builder from the analytics outputs, sorted by the strength of each indicator (value, ratio or count), highest first, not at random: payments just below competition thresholds [A2], same-supplier payment windows crossing a threshold [A3], high-value suppliers with no Contracts Finder notice found [A4], repeated equal payments [A5], spend after notice expiry [A6] and spend above the award rate [A7]. Placement and grant payments are excluded from the samples unless a test is about them, because they may be exempt from competition. Approval, exception and action-tracking controls that leave no trace in the payment data are tested by walkthrough and document request.

## Sampling

Samples are targeted, not random: each test draws the highest-indicator items from the full flagged population in `outputs/analytics-full/`, sized by the risk's register score, and every transaction is checked against `spend-clean.csv`. Files: `outputs/samples/<test>.csv`.

| Register score | Items per test |
|---|---|
| 15+ | 25 |
| 8–14 | 15 |
| 4–7 | 10 |
| 1–3 | 5 |

| Test | Source | Population | Drawn | Transactions | Value £ |
|---|---|---|---|---|---|
| T-01-1 | threshold_clustering.csv | 10 | 10 | 10 | 239,427.82 |
| T-02-1 | threshold_clustering.csv | 2 | 2 | 2 | 318,885.53 |
| T-03-1 | split_purchases.csv | 39 | 25 | 138 | 1,182,808.12 |
| T-03-2 | split_purchases.csv | 8 | 8 | 128 | 5,404,533.12 |
| T-04-1 | high_value_suppliers.csv | 42 | 25 | 62 | 14,865,447.37 |
| T-04-2 | near-matches.csv | 6 | 6 | 18 | 239,360.31 |
| T-04-3 | no transaction sample | – | – | – | – |
| T-05-1 | duplicates.csv | 35 | 15 | 39 | 525,039.22 |
| T-06-1 | expired_notice_spend.csv | 8 | 8 | 13 | 191,349.42 |
| T-07-1 | spend_vs_award.csv | 12 | 12 | 28 | 795,139.63 |
| T-10-1 | high_value_suppliers.csv | 18 | 5 | 13 | 916,841.43 |
| T-10-2 | no transaction sample | – | – | – | – |
| T-11-1 | no transaction sample | – | – | – | – |

Total sample rows: 451, covering 377 unique transactions. Transactions may appear in multiple tests.

## Limitations

The spend data covers only the payments the council publishes under the transparency threshold [CPR-04] for 3 months, so supplier totals are annualised estimates and split and duplicate results are a lower bound [A8]. Rows with a redacted supplier (2,015 rows) are excluded from every supplier-level test [A9]. The notices file holds published Contracts Finder notices, not the council's contract register [A10]: a notice not found is an indicator to check against the council's register, never evidence of off-contract spend, and suppliers below the publication threshold are never questioned on that basis. Scope limitation, recorded at the auditor's instruction: the analytics tests that depend on 'the relevant Threshold' (the full statutory procedure [CPR-58], first advertising on the CDP [CPR-09], electronic tendering above the threshold [CPR-12], the written procurement report [CPR-28] and sealing [CPR-47]) could not be run because the spend data has no contract-type field to choose the threshold [A11]; the goods and services threshold is used only where a rule names it. At the auditor's sign-off decision on the coverage challenge the limitation applies to the analytics only: fieldwork tests these rules in T-10-1 on the contracts obtained, where the contract type is known. Care and education placements and the quotation threshold below competition were approved as out of scope (R-08, R-09), so the placement exemption rule is not tested [CPR-65]. No action tracker is published [GAP-01] and the Strategic Risk Register is exempt and not public [GAP-06]. On the impact-scale conflict [DISC-01], the auditor confirmed at sign-off that the impact table's Medium level is the basis for R-01, R-02, R-05 and R-10, which changes no score. The register header still lists the conflict as unresolved because the builder marks it from history.json, which records it only as a discrepancy.

- The spend data covers payments over £500 only; split-purchase and duplicate indicators are lower bounds.
- Notice-based samples rest on Contracts Finder notices, which are not a contract register; 'no notice found' is checked against the council's own register in fieldwork.

## Sources

- A1: `$.population.rows_after_exclusions` in analytics.json = 8,534
- A2: `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n` in analytics.json = 10
- A3: `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows` in analytics.json = 39
- A4: `$.tests.off_contract.statutory_tier.headline_general_procurement_no_notice_found.suppliers` in analytics.json = 42
- A5: `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups` in analytics.json = 35
- A6: `$.tests.expired_notice_spend.suppliers` in analytics.json = 8
- A7: `$.tests.spend_vs_award.flagged` in analytics.json = 12
- A8: `$.population.annualisation_factor` in analytics.json = 4
- A9: `$.population.excluded.redacted_supplier.rows` in analytics.json = 2,015
- A10: `$.contracts.register_present` in analytics.json = False
- A11: `$.skipped[0].reason` in analytics.json = STATUTORY_THRESHOLD_RELEVANT is null in rules.json parameters: Not a separate figure: it means whichever of the three thresholds fits each contract's type. The spend data has no reliable contract-type field, so tests citing it stay skipped and are listed under 'skipped' with this reason.
- A12: `$.tests.threshold_clustering.per_threshold[?threshold==173100].band_by_tag.general_procurement.n` in analytics.json = 2
- A13: `$.tests.split_purchases.per_threshold[?threshold==173100].headline_general_procurement.windows` in analytics.json = 6
- A14: `$.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.windows` in analytics.json = 2
- A15: `$.tests.off_contract.by_match_class.near_contain.suppliers` in analytics.json = 5
- A16: `$.tests.off_contract.by_match_class.near_ratio.suppliers` in analytics.json = 2
- A17: `$.tests.off_contract.statutory_tier.by_match_class.exact.suppliers` in analytics.json = 19
