# Audit program: procurement, West Berkshire Council

Basis: risk register revision 1 (built 2026-10-15T11:56:28), auditor decisions in `outputs/auditor-comments.md`, plan `outputs/audit-plan.json`. Built 2026-10-15T12:07:37 by `.claude/skills/audit-program/build_pack.py`.

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier. A sampled transaction is selected because it carries an indicator, not because anything is assumed to be wrong with it.

## R-01: Payments within ten per cent below the £25,000 quotation threshold

Score 6 (Moderate); controls: C-01-1 Purchases below the quotation threshold are supported by at least one quote from an appropriate source [CPR-53] and are ordered under the delegated authority of the relevant Service Director or a nominated officer [CPR-49].; C-01-2 Where related orders for one requirement together reach the quotation threshold, invitations to quote are sent via the Procurement Portal to at least three appropriate sources [CPR-54] [CPR-55]; any discretionary exception is recorded in writing with reasons [CPR-19] and fully documented [CPR-24].

### T-01-1 (tests C-01-1, C-01-2)

For each sampled general procurement payment in the band just below the quotation threshold [A3], obtain the order and invoice; establish the order value exclusive of VAT, confirm at least one quote was sought [CPR-53] and that the order was raised under delegated authority [CPR-49]. Trace other orders with the same supplier for the same requirement: where together they reach the quotation threshold, confirm invitations to quote were issued via the Procurement Portal [CPR-54] [CPR-55] or that a written exception with reasons exists [CPR-19] [CPR-24]. Read the result together with the split-purchase windows in R-03.

- **Sample:** `analytics-full/threshold_clustering.csv`; filter: threshold = $.tests.threshold_clustering.per_threshold[?threshold==25000].threshold; tag = general_procurement; sort: Net amount descending; first 10 transactions. Population 10; drawn 10; 10 transactions, £239,427.82. File: `outputs/samples/T-01-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled payment; Quotation records (quotes sought, received and evaluated) for each sampled purchase; Any written exception or waiver, with reasons and approvals, for the sampled purchases

## R-03: Multiple payments to one supplier within a short window that together cross a competition threshold

Score 15 (Extreme (Red)); controls: C-03-1 Requirements are aggregated before the procurement route is chosen and are not split or disaggregated to avoid the Rules [CPR-11]; where a Purchasing Scheme is used, advice confirming entitlement and coverage is obtained first [CPR-27] and any direct award without further competition has prior written approval [CPR-60].; C-03-2 Aggregated requirements at or above the quotation threshold go to invitations to quote via the Procurement Portal [CPR-54] [CPR-55], evaluated against criteria notified in advance [CPR-16] and awarded on best value [CPR-17], with the progress of the procurement documented and kept [CPR-30].; C-03-3 Requirements above the Key Decision value are let by full competitive tender [CPR-56] or the Procurement Legislation route [CPR-57], advertised on the CDP first [CPR-09] with notices approved by the Service Lead for Procurement and Commissioning [CPR-10] and electronic tendering [CPR-12] in a specified format with tenders stored locked until opening [CPR-13], late tenders rejected unless the Monitoring Officer agrees [CPR-14] and opened electronically with an audit record [CPR-15], and awarded as a Key Decision [CPR-04] [CPR-51] or with Executive approval at the highest band [CPR-52].; C-03-4 High-value awards have a written award report [CPR-28] retained for three years [CPR-29], a record of social value consideration for service contracts above the Threshold [CPR-01], a sealed contract where above the Threshold [CPR-46] with the sealing attested and witnessed [CPR-44], and a performance bond in an approved form [CPR-40] or a written risk assessment approved where no bond is required [CPR-41].

### T-03-1 (tests C-03-1, C-03-2)

First, check each sampled supplier against the council's contract register [CPR-07] and record windows covered by a let contract as explained instalments; for those, confirm only that the payments fall within the contract. For windows with no covering contract, sampled from the thirty-day windows of general procurement payments that together cross the quotation threshold [A2], obtain the orders and invoices and establish whether the payments relate to one requirement [CPR-11]. If they do, confirm that invitations to quote were run at the aggregate value [CPR-54] [CPR-55], evaluated against pre-notified criteria [CPR-16] and awarded on best value [CPR-17], with a procurement record kept [CPR-30]; or that a Purchasing Scheme covers them, with the advice [CPR-27] and any direct-award approval [CPR-60].

- **Sample:** `analytics-full/split_purchases.csv`; filter: threshold = $.tests.split_purchases.per_threshold[?threshold==25000].threshold; tag = general_procurement; sort: total_gbp descending; first 25 groups (all payments in each). Population 39; drawn 25; 309 transactions, £1,795,137.81. File: `outputs/samples/T-03-1.csv`.
- **PBC:** The council's contract register with values, start and end dates and suppliers; Purchase orders and invoices for each sampled window; Quotation records (quotes sought, received and evaluated) for each sampled purchase; The contract, framework call-off or Purchasing Scheme advice covering each sampled supplier

### T-03-2 (tests C-03-1, C-03-3)

For each general procurement window whose payments together cross the Key Decision value [A14], identify the contract the payments are made under and trace its award: confirm a full competitive tender [CPR-56] or the Procurement Legislation route where the value is above the statutory threshold [CPR-57], CDP advertising [CPR-09] with an approved notice [CPR-10] and electronic tendering [CPR-12]; from the e-tendering record confirm the tender format and locked storage [CPR-13], the handling of any late tender [CPR-14] and electronic opening with an audit record [CPR-15]; and award as a Key Decision [CPR-04] [CPR-51] or Executive approval where the contract value is in the highest band [CPR-52]. Where no single contract covers the window, establish whether the requirement was split [CPR-11].

- **Sample:** `analytics-full/split_purchases.csv`; filter: threshold = $.tests.split_purchases.per_threshold[?threshold==500000].threshold; tag = general_procurement; sort: total_gbp descending; first 25 groups (all payments in each). Population 2; drawn 2; 58 transactions, £3,509,528.75. File: `outputs/samples/T-03-2.csv`.
- **PBC:** Purchase orders and invoices for each sampled window; Tender and award file for each contract identified (advert, CDP notices, tender evaluation, award decision); Key Decision or Executive decision record for each contract identified; E-tendering system audit record for each contract identified

### T-03-3 (tests C-03-4)

For each contract identified in T-03-2, confirm the written award report exists [CPR-28] and is retained [CPR-29], that social value was considered for a service contract above the Threshold [CPR-01], that the contract was sealed where above the Threshold [CPR-46] with the sealing attested and witnessed on the document [CPR-44], and that a performance bond in an approved form [CPR-40] or an approved written risk assessment [CPR-41] is on the contract file.

- **Sample:** none. Uses the contracts identified from the windows drawn for T-03-2; no further transactions are drawn.
- **PBC:** Award report, sealed contract and performance bond or bond risk assessment for each contract identified

## R-04: High-value suppliers with no matching Contracts Finder notice

Score 15 (Extreme (Red)); controls: C-04-1 The council publishes and maintains a register of contracts in progress and awarded, with value, duration and supplier [CPR-07], each award is notified to the Service Lead for recording on it [CPR-34], contract information is reported to the relevant board monthly [CPR-08], and invitations to tender above the publication value are published [CPR-06].; C-04-2 Every contract is made by an authorised decision-maker [CPR-02] within approved budget [CPR-03], approved at the level for its total value [CPR-49] [CPR-50] [CPR-51] [CPR-52], let by the route for its value [CPR-54] [CPR-55] and put in writing in an approved form [CPR-32].; C-04-3 Exceptions to competition are used only in the listed circumstances [CPR-18], granted in advance by the Monitoring Officer and/or S151 Officer [CPR-20] [CPR-21], with an exception report approved at the level for the value [CPR-22] [CPR-23] [CPR-25], S151 approval recorded [CPR-26], and prior written approval for contracts excluded from competition [CPR-58].

### T-04-1 (tests C-04-1, C-04-2, C-04-3)

For each sampled general procurement supplier with an annualised estimate at or above the quotation threshold and no matching active notice [A4], trace the supplier to the council's contract register [CPR-07]; a notice gap is checked against that register and is not in itself an exception. Obtain the contract and confirm it was awarded by an authorised decision-maker [CPR-02] within budget [CPR-03], approved at the level for its value [CPR-49] [CPR-50] [CPR-51] [CPR-52], let after invitations to quote or tender [CPR-54] [CPR-55] and put in writing [CPR-32]; or obtain the approved exception, its report and S151 approval [CPR-18] [CPR-20] [CPR-21] [CPR-22] [CPR-23] [CPR-25] [CPR-26] [CPR-58]. Confirm the award was notified for the register [CPR-34].

- **Sample:** `analytics-full/high_value_suppliers.csv`; filter: dominant_tag = general_procurement; match_class = none; annualised estimate {">=": "$.tests.off_contract.parameters.threshold"}; sort: annualised estimate descending; first 25 suppliers (largest 3 payments each). Population 186; drawn 25; 62 transactions, £14,865,447.37. File: `outputs/samples/T-04-1.csv`.
- **PBC:** The council's contract register with values, start and end dates and suppliers; The contract and its award approval for each sampled supplier; Any written exception or waiver, with reasons and approvals, for the sampled purchases

### T-04-2 (tests C-04-1)

For each near-match candidate at or above the quotation threshold [A15] [A16], confirm against the council's contract register [CPR-07] whether the candidate notice relates to the paid supplier; where it does not, treat the supplier as in T-04-1 and trace its contract and award route [CPR-54] [CPR-55].

- **Sample:** `analytics-full/near-matches.csv`; filter: annualised_estimate {">=": "$.tests.off_contract.parameters.threshold"}; sort: annualised_estimate descending; first 25 suppliers (largest 3 payments each). Population 7; drawn 7; 21 transactions, £260,879.03. File: `outputs/samples/T-04-2.csv`.
- **PBC:** The council's contract register with values, start and end dates and suppliers; The contract and its award approval for each sampled supplier

### T-04-3 (tests C-04-1)

Obtain the published contract register and confirm it shows contracts in progress and awarded with value, duration and supplier [CPR-07]; obtain the monthly contract reports to the relevant board for the spend window [CPR-08] and confirm that invitations to tender above the publication value are published [CPR-06]. Note whether the register is complete enough to resolve the notice gaps reported in the analysis [A10].

- **Sample:** none. A document test of the register, board reporting and tender publication; it does not depend on individual transactions.
- **PBC:** The council's contract register with values, start and end dates and suppliers; Monthly contract information reports to the relevant board for the spend window; The published list of invitations to tender for the spend window

## R-05: Repeated payments of the same amount to the same supplier within a week

Score 9 (Medium - High (Amber)); controls: C-05-1 Written evidence is held for every purchase and each invoice is matched to it before payment, so that a supply is paid once [CPR-31].; C-05-2 Published expenditure over the publication floor reflects the payments actually made [CPR-05].

### T-05-1 (tests C-05-1, C-05-2)

For each sampled group of equal general procurement payments to one supplier at different times within a week [A5], obtain the invoices and purchase evidence [CPR-31] and confirm each payment relates to a distinct supply, invoice number and period. Trace each payment to the ledger to confirm the published lines are not repeat listings [CPR-05]. Where two payments relate to one supply, confirm a credit note or recovery is recorded.

- **Sample:** `analytics-full/duplicates.csv`; filter: tier = different_time; tag = general_procurement; sort: gbp_beyond_first descending; first 15 groups (all payments in each). Population 35; drawn 15; 39 transactions, £525,039.22. File: `outputs/samples/T-05-1.csv`.
- **PBC:** Invoices and purchase evidence for each sampled payment; Accounts payable ledger extract for each sampled payment, with any credit notes or recoveries

## R-06: Spend with suppliers whose every matching notice ended before the spend window

Score 6 (Moderate); controls: C-06-1 A contract is extended only where it provides for extension and with S151 Officer approval before expiry [CPR-61]; a replacement contract is recorded on the contract register [CPR-34].

### T-06-1 (tests C-06-1)

For each supplier paid in the window although every matching notice had ended before it [A6], trace the supplier to the council's contract register and obtain the current contract, or the extension and its S151 Officer approval [CPR-61]; confirm any replacement contract was notified for the register [CPR-34]. A newer contract may exist with no notice, so a notice gap is checked against the register before any conclusion. Where the sampled spend is a separate small purchase, confirm the quote rule was followed instead [CPR-53].

- **Sample:** `analytics-full/expired_notice_spend.csv`; filter: none; sort: total_gbp descending; first 10 suppliers (largest 3 payments each). Population 8; drawn 8; 13 transactions, £188,394.86. File: `outputs/samples/T-06-1.csv`.
- **PBC:** The council's contract register with values, start and end dates and suppliers; Contract extension approvals (S151 Officer) for each sampled supplier; Purchase orders and invoices for each sampled payment

## R-07: Annualised spend above the published award value for single-supplier notices

Score 10 (Medium - High (Amber)); controls: C-07-1 Variations of scope have prior written approval from the Monitoring Officer and S151 Officer below the Threshold [CPR-62] or relevant board approval following an extension report above it [CPR-63], and the contract register value is kept current [CPR-07].

### T-07-1 (tests C-07-1)

First, confirm from the order or invoice that each sampled payment is made under the matched notice; where it is not, trace the payment's own contract and award route as in T-04-1 [CPR-54] [CPR-55]. Then, for each flagged supplier whose annualised estimate is at least the flag ratio times the annual award value [A7] [A17], obtain the contract and its current value from the council's contract register [CPR-07]; compare actual spend to date with the contract value and, where spend exceeds it, obtain the approved variation [CPR-62] or the board approval and extension report [CPR-63]. Award values may be estimates or maxima, so confirm the contract value before concluding.

- **Sample:** `analytics-full/spend_vs_award.csv`; filter: flag = True; sort: ratio descending; first 15 suppliers (largest 3 payments each). Population 12; drawn 12; 28 transactions, £795,139.63. File: `outputs/samples/T-07-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled payment; The council's contract register with values, start and end dates and suppliers; The contract and any variation approvals or extension reports for each sampled supplier; Spend to date against each sampled contract from the finance system

## R-08: Placement spend patterns: aggregated windows and repeated equal payments

Score 10 (Medium - High (Amber)); controls: C-08-1 For individual social care placements the reasons for the choice of provider are recorded on the individual's case notes [CPR-64]; contracts under the Provider Selection Regime record key decisions and follow its process [CPR-59]; Appendix C exemptions for contracts above the Threshold are approved by the relevant board [CPR-65].; C-08-2 Each placement payment is supported by written evidence of the care purchased and the period it covers, so that repeated equal payments relate to distinct periods of care [CPR-31].

### T-08-1 (tests C-08-1)

The placement windows themselves are not sampled, so this case-note test does not conclude on the window indicator. Placement windows aggregate many individual packages with one provider [A8], so drawing whole windows would pull every package of the largest providers; the test therefore stands in at payment level on the largest placement providers [A18]. Only payments tagged as placements are tested: confirm the tag of each drawn payment first and record any payment that is not a placement as out of this test. For each sampled placement payment, identify the individual placement and confirm the reasons for the choice of provider are on the case notes [CPR-64]; where the service falls under the Provider Selection Regime, confirm key decisions are recorded [CPR-59]; where the provider's annual value exceeds the Threshold under an Appendix C exemption, confirm board approval [CPR-65].

- **Sample:** `analytics-full/high_value_suppliers.csv`; filter: dominant_tag = care_or_education_placement; sort: annualised estimate descending; first 15 suppliers (largest 3 payments each). Population 307; drawn 15; 45 transactions, £1,655,037.59. File: `outputs/samples/T-08-1.csv`.
- **PBC:** Case notes recording the reasons for the choice of provider for each sampled placement; Placement agreement or individual service contract for each sampled placement; Board approval of any Appendix C exemption above the Threshold for the sampled providers

### T-08-2 (tests C-08-2)

For each sampled group of equal placement payments to one provider at different times within a week [A19], obtain the invoices or schedules [CPR-31] and confirm each payment relates to a distinct individual or period of care; where two payments relate to one period, confirm a credit or recovery is recorded. Confirm the placement reasons are on the case notes for one individual in each group [CPR-64].

- **Sample:** `analytics-full/duplicates.csv`; filter: tier = different_time; tag = care_or_education_placement; sort: gbp_beyond_first descending; first 15 groups (all payments in each). Population 204; drawn 15; 101 transactions, £2,110,700.78. File: `outputs/samples/T-08-2.csv`.
- **PBC:** Invoices and purchase evidence for each sampled payment; Accounts payable ledger extract for each sampled payment, with any credit notes or recoveries; Case notes recording the reasons for the choice of provider for each sampled placement

## R-09: No published action tracker to confirm follow-up of prior procurement audit actions

Score 2 (Low (Green)); controls: C-09-1 Actions agreed in prior audits of contract letting and accounts payable, covering the quotation and tender rules [CPR-54] [CPR-56] and purchase evidence [CPR-31], are tracked to implementation and reported [IAP-07].

### T-09-1 (tests C-09-1)

Obtain the internal audit action tracker for Contract Letting [AUD-01] and Accounts Payable [AUD-11]; confirm the status and due dates of agreed actions and, for any open action on the quotation or tender procedure [CPR-54] [CPR-56] or purchase evidence [CPR-31], take its status into account when concluding on R-01, R-03 and R-05.

- **Sample:** none. A document request for the action tracker; no transactions are needed.
- **PBC:** Internal audit action tracker with agreed actions, due dates and status for Contract Letting and Accounts Payable

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

## PBC list

Documents and information to request from the council before fieldwork.

| # | Item | For tests |
|---|---|---|
| 1 | Purchase orders and invoices for each sampled payment | T-01-1, T-06-1, T-07-1 |
| 2 | Quotation records (quotes sought, received and evaluated) for each sampled purchase | T-01-1, T-03-1 |
| 3 | Any written exception or waiver, with reasons and approvals, for the sampled purchases | T-01-1, T-04-1 |
| 4 | The council's contract register with values, start and end dates and suppliers | T-03-1, T-04-1, T-04-2, T-04-3, T-06-1, T-07-1 |
| 5 | Purchase orders and invoices for each sampled window | T-03-1, T-03-2 |
| 6 | The contract, framework call-off or Purchasing Scheme advice covering each sampled supplier | T-03-1 |
| 7 | Tender and award file for each contract identified (advert, CDP notices, tender evaluation, award decision) | T-03-2 |
| 8 | Key Decision or Executive decision record for each contract identified | T-03-2 |
| 9 | E-tendering system audit record for each contract identified | T-03-2 |
| 10 | Award report, sealed contract and performance bond or bond risk assessment for each contract identified | T-03-3 |
| 11 | The contract and its award approval for each sampled supplier | T-04-1, T-04-2 |
| 12 | Monthly contract information reports to the relevant board for the spend window | T-04-3 |
| 13 | The published list of invitations to tender for the spend window | T-04-3 |
| 14 | Invoices and purchase evidence for each sampled payment | T-05-1, T-08-2 |
| 15 | Accounts payable ledger extract for each sampled payment, with any credit notes or recoveries | T-05-1, T-08-2 |
| 16 | Contract extension approvals (S151 Officer) for each sampled supplier | T-06-1 |
| 17 | The contract and any variation approvals or extension reports for each sampled supplier | T-07-1 |
| 18 | Spend to date against each sampled contract from the finance system | T-07-1 |
| 19 | Case notes recording the reasons for the choice of provider for each sampled placement | T-08-1, T-08-2 |
| 20 | Placement agreement or individual service contract for each sampled placement | T-08-1 |
| 21 | Board approval of any Appendix C exemption above the Threshold for the sampled providers | T-08-1 |
| 22 | Internal audit action tracker with agreed actions, due dates and status for Contract Letting and Accounts Payable | T-09-1 |
