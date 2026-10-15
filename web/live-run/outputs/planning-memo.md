# Audit planning memo: procurement, West Berkshire Council

Basis: risk register revision 1 (built 2026-10-15T11:56:28), auditor decisions in `outputs/auditor-comments.md`, plan `outputs/audit-plan.json`. Built 2026-10-15T12:07:37 by `.claude/skills/audit-program/build_pack.py`.

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier. A sampled transaction is selected because it carries an indicator, not because anything is assumed to be wrong with it.

## Objective

To conclude whether the council's procurement controls are operating so that purchases follow the competition route for their aggregated value [CPR-11] [CPR-53] [CPR-54] [CPR-56], are covered by a contract, extension or variation approved at the right level [CPR-07] [CPR-61] [CPR-62], are supported by written purchase evidence [CPR-31], and that individual placements record the reasons for the provider choice [CPR-64]. The audit tests the risk indicators in the approved register; an indicator is something to investigate, not a finding about the council, a service or a supplier.

## Scope

8 risk(s) in scope, 1 out of scope, as decided by the auditor.

| Risk | L | I | Score | Band | Decision | Tests | Sample transactions |
|---|---|---|---|---|---|---|---|
| R-01: Payments within ten per cent below the £25,000 quotation threshold | 2 | 3 | 6 | Moderate | Approve | T-01-1 | 10 |
| R-03: Multiple payments to one supplier within a short window that together cross a competition threshold | 3 | 5 | 15 | Extreme (Red) | Approve | T-03-1, T-03-2, T-03-3 | 367 |
| R-04: High-value suppliers with no matching Contracts Finder notice | 3 | 5 | 15 | Extreme (Red) | Approve | T-04-1, T-04-2, T-04-3 | 83 |
| R-05: Repeated payments of the same amount to the same supplier within a week | 3 | 3 | 9 ‡ | Medium - High (Amber) | Approve | T-05-1 | 39 |
| R-06: Spend with suppliers whose every matching notice ended before the spend window | 2 | 3 | 6 | Moderate | Approve | T-06-1 | 13 |
| R-07: Annualised spend above the published award value for single-supplier notices | 2 | 5 | 10 ‡ | Medium - High (Amber) | Approve | T-07-1 | 28 |
| R-08: Placement spend patterns: aggregated windows and repeated equal payments | 2 | 5 | 10 ‡ | Medium - High (Amber) | Approve | T-08-1, T-08-2 | 146 |
| R-09: No published action tracker to confirm follow-up of prior procurement audit actions | 1 | 2 | 2 | Low (Green) | Approve | T-09-1 | 0 |

Out of scope:

- R-02: approved as out of scope

## Approach

Targeted testing driven by analysis of the full published spend population: 8,534 payments totalling £66,778,105 from 2026-05-01 to 2026-07-31 [A1]. Samples are drawn by code from the flagged lists, ordered by the strength of each indicator (value, ratio, count), not at random: split-purchase windows [A2], payments just below the quotation threshold [A3], high-value suppliers with no matching notice [A4], repeated equal payments [A5], expired notices [A6], spend above award [A7] and placement patterns [A8]. For each sampled item the auditor obtains the council's own records (orders, invoices, quotation and tender records, contract register entries, approvals, case notes) and establishes whether the expected control operated. Placements and grants are tested separately from general procurement because placements may be exempt from competition [CPR-64]. Prior coverage is taken into account: Contract Letting [AUD-01], Accounts Payable [AUD-11] and Purchase of Residential and Nursing Care Provision [AUD-14] last received Reasonable Assurance.

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
| T-03-1 | split_purchases.csv | 39 | 25 | 309 | 1,795,137.81 |
| T-03-2 | split_purchases.csv | 2 | 2 | 58 | 3,509,528.75 |
| T-03-3 | no transaction sample | – | – | – | – |
| T-04-1 | high_value_suppliers.csv | 186 | 25 | 62 | 14,865,447.37 |
| T-04-2 | near-matches.csv | 7 | 7 | 21 | 260,879.03 |
| T-04-3 | no transaction sample | – | – | – | – |
| T-05-1 | duplicates.csv | 35 | 15 | 39 | 525,039.22 |
| T-06-1 | expired_notice_spend.csv | 8 | 8 | 13 | 188,394.86 |
| T-07-1 | spend_vs_award.csv | 12 | 12 | 28 | 795,139.63 |
| T-08-1 | high_value_suppliers.csv | 307 | 15 | 45 | 1,655,037.59 |
| T-08-2 | duplicates.csv | 204 | 15 | 101 | 2,110,700.78 |
| T-09-1 | no transaction sample | – | – | – | – |

Total sampled transactions: 686.

## Limitations

The spend data covers three months and only payments over the publication floor [A9], so supplier totals are annualised estimates and split-purchase counts are a lower bound. The contract file is a Contracts Finder notice export, not a contract register [A10]; a missing or expired notice is an indicator to check against the council's register, never evidence of off-contract spend [A11]. The statutory procurement thresholds are not recorded in the rules [A12], so the statutory tier is identified from each contract file during fieldwork rather than from the data. Award values on notices may be estimates or maxima [A13]. The papers publish no action tracker [GAP-01] and the Strategic Risk Register is exempt and not public [GAP-05], so follow-up status must be requested from the council. The placement windows behind R-08 [A8] are not sampled as windows: the case-note test draws the largest placement providers' payments instead, so it does not conclude on the window indicator.

- The spend data covers payments over £500 only; split-purchase and duplicate indicators are lower bounds.
- Notice-based samples rest on Contracts Finder notices, which are not a contract register; 'no notice found' is checked against the council's own register in fieldwork.

## Sources

- A1: `$.population.rows_after_exclusions` in analytics.json = 8,534
- A2: `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows` in analytics.json = 39
- A3: `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n` in analytics.json = 10
- A4: `$.tests.off_contract.headline_general_procurement_no_notice_found.suppliers` in analytics.json = 186
- A5: `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups` in analytics.json = 35
- A6: `$.tests.expired_notice_spend.suppliers` in analytics.json = 8
- A7: `$.tests.spend_vs_award.flagged` in analytics.json = 12
- A8: `$.tests.split_purchases.per_threshold[?threshold==25000].care_or_education_placement.windows` in analytics.json = 126
- A9: `$.tests.split_purchases.note` in analytics.json = population is expenditure over £500 only, so results are a lower bound; placement windows reported separately because periodic care fees legitimately recur
- A10: `$.contracts.register_present` in analytics.json = False
- A11: `$.tests.off_contract.publication_note` in analytics.json = Contracts Finder does not carry smaller awards; only suppliers at or above the publication threshold are classed, and results must never be used to question smaller suppliers.
- A12: `$.skipped[3].reason` in analytics.json = STATUTORY_THRESHOLD_RELEVANT is null in rules.json parameters
- A13: `$.tests.spend_vs_award.caveat` in analytics.json = Indicator of spend beyond the award without an approved variation; award values may be estimates or maxima, and the annualised estimate extrapolates three months.
- A14: `$.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.windows` in analytics.json = 2
- A15: `$.tests.off_contract.by_match_class.near_contain.suppliers` in analytics.json = 5
- A16: `$.tests.off_contract.by_match_class.near_ratio.suppliers` in analytics.json = 2
- A17: `$.tests.spend_vs_award.parameters.flag_at` in analytics.json = 1.25
- A18: `$.tests.high_value_suppliers.by_dominant_tag.care_or_education_placement.suppliers` in analytics.json = 307
- A19: `$.tests.duplicates.per_tier.different_time.by_tag.care_or_education_placement.groups` in analytics.json = 204
