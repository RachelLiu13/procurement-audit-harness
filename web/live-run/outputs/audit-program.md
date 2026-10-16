# Audit program: procurement, West Berkshire Council

Basis: risk register revision 1 (built 2026-10-16T00:02:33), auditor decisions in `outputs/auditor-comments.md`, plan `outputs/audit-plan.json`. Built 2026-10-16T00:10:24 by `.claude/skills/audit-program/build_pack.py`.

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier. A sampled transaction is selected because it carries an indicator, not because anything is assumed to be wrong with it.

## R-01: Payments just below the £25,000 competition threshold

Score 6 (Moderate); controls: C-01-1 Purchases are routed by total value: at least one quote below the competition threshold [CPR-54], and invitations to quote via the Procurement Portal to at least three sources from the competition threshold upward for goods and services [CPR-55] and for works, concession or light touch contracts [CPR-56], with invitations to tender published [CPR-05].; C-01-2 Quotes are evaluated against criteria notified in advance [CPR-16], awarded on best value rather than lowest price alone [CPR-17], and every purchase and procurement step is evidenced in writing and retained [CPR-31] [CPR-30].; C-01-3 Related orders for the same requirement are aggregated before the route is chosen, so no requirement is split to stay below a threshold [CPR-11].

### T-01-1 (tests C-01-1, C-01-2, C-01-3)

For each sampled general procurement payment in the band just below £25,000 [A2], trace the payment to its purchase order and establish the total value of the requirement, including other orders for the same requirement [CPR-11]. Confirm the route matched that value: at least one quote below the threshold [CPR-54], or portal invitations to at least three sources at or above it [CPR-55] [CPR-56] with the invitation published [CPR-05]. Confirm the quotes were evaluated against notified criteria [CPR-16] and the award made on best value [CPR-17], and that the purchase and procurement file are evidenced and retained [CPR-31] [CPR-30].

- **Sample:** `analytics-full/threshold_clustering.csv`; filter: threshold = $.tests.threshold_clustering.per_threshold[?threshold==25000].threshold; tag = general_procurement; sort: Net amount descending; first 10 transactions. Population 10; drawn 10; 10 transactions, £239,427.82. File: `outputs/samples/T-01-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled payment; Quotation or invitation-to-quote records, evaluation and award decision for each sampled purchase; Other orders raised with the same supplier for the same requirement

## R-02: Payments just below the £173,100 Procurement Act threshold for goods and services

Score 9 (Medium - High (Amber)); controls: C-02-1 Goods and services requirements are valued in total before the route is chosen; below the goods and services threshold the portal quotation route applies [CPR-55], and requirements are not split to stay below the threshold [CPR-11].; C-02-2 For service contracts above the goods and services threshold, consideration of social value is recorded [CPR-01], and any notice published on the CDP is approved and issued by the Service Lead for Procurement and Commissioning or delegate [CPR-10].

### T-02-1 (tests C-02-1, C-02-2)

For each general procurement payment in the band just below £173,100 [A12], obtain the contract or order and establish its total value and whether other orders form part of the same requirement [CPR-11]. Where the total is below the threshold, confirm the portal quotation route was followed [CPR-55]; where it is above, confirm social value consideration was recorded [CPR-01] and that any CDP notice was approved by the Service Lead [CPR-10]. Split windows at this threshold are tested under R-03, as the auditor directed.

- **Sample:** `analytics-full/threshold_clustering.csv`; filter: threshold = $.tests.threshold_clustering.per_threshold[?threshold==173100].threshold; tag = general_procurement; sort: Net amount descending; first 15 transactions. Population 2; drawn 2; 2 transactions, £318,885.53. File: `outputs/samples/T-02-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled payment; The contract or order, its total value and the procurement route record for each sampled purchase; CDP notices and their approval for each sampled contract; Other orders raised with the same supplier for the same requirement

## R-03: Same-supplier payment windows that cross competition thresholds while each payment stays below

Score 20 (Extreme (Red)); controls: C-03-1 Requirements are aggregated across orders to one supplier and are not split or disaggregated to avoid a threshold [CPR-11].; C-03-2 The aggregated value determines the route: portal quotations for goods and services [CPR-55] and for works, concession or light touch contracts [CPR-56], and a full competitive tender for works above the upper tier [CPR-57].; C-03-3 Call-offs under a framework or other Purchasing Scheme are supported by recorded advice on entitlement and coverage [CPR-27], and direct awards under a scheme without further competition have prior written Monitoring Officer approval [CPR-61].; C-03-4 Awards are approved at the tier their aggregated value requires [CPR-51] [CPR-52] and procurement progress is documented and retained [CPR-30].

### T-03-1 (tests C-03-1, C-03-2, C-03-3, C-03-4)

For each sampled general procurement window crossing £25,000 [A3], obtain the orders and invoices behind every payment and establish whether they relate to one requirement [CPR-11]. Where they are call-offs under an awarded contract or framework, trace them to the contract and confirm the scheme advice was recorded [CPR-27] and any direct award approved [CPR-61]. Where they are separate orders for one requirement, confirm the aggregated value was procured by the route its tier requires [CPR-55] [CPR-56] and that the procurement file is documented [CPR-30]. Recurring invoices under one contract are an expected cause of this indicator. Windows are drawn with the fewest payments first, then by highest total, so windows that only just cross the threshold with a few payments, the closest match to a split, come before long runs of recurring invoices.

- **Sample:** `analytics-full/split_purchases.csv`; filter: threshold = $.tests.split_purchases.per_threshold[?threshold==25000].threshold; tag = general_procurement; sort: n_payments ascending, total_gbp descending; first 25 groups (all payments in each). Population 39; drawn 25; 138 transactions, £1,182,808.12. File: `outputs/samples/T-03-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled window; The contract, framework call-off or Purchasing Scheme advice record for each sampled supplier; Quotation, tender and award approval records for each sampled supplier

### T-03-2 (tests C-03-1, C-03-2, C-03-3, C-03-4)

For each general procurement window crossing £173,100 [A13] or £500,000 [A14], establish whether the payments relate to one requirement [CPR-11] and, if so, confirm the contract was let by the route for its aggregated value, including a full tender for works above the upper tier [CPR-57], and approved at the award tier for that value [CPR-51] [CPR-52].  Where the payments are call-offs under an awarded contract or framework, trace them to it and confirm the scheme advice [CPR-27] and any direct-award approval [CPR-61]. A supplier may appear in both tests; record the result once and cross-refer.

- **Sample:** `analytics-full/split_purchases.csv`; filter: threshold ["$.tests.split_purchases.per_threshold[?threshold==173100].threshold", "$.tests.split_purchases.per_threshold[?threshold==500000].threshold"]; tag = general_procurement; sort: total_gbp descending; first 25 groups (all payments in each). Population 8; drawn 8; 128 transactions, £5,404,533.12. File: `outputs/samples/T-03-2.csv`.
- **PBC:** Purchase orders and invoices for each sampled window; The contract, framework call-off or Purchasing Scheme advice record for each sampled supplier; Quotation, tender and award approval records for each sampled supplier

## R-04: High-value general procurement suppliers with no Contracts Finder notice found

Score 15 (Extreme (Red)); controls: C-04-1 Every contract is put in writing in a form approved by the Monitoring Officer [CPR-32], notified for the Council Contract Register [CPR-34], and the register of contracts is published [CPR-06].; C-04-2 Contracts are let by the competitive route for their value [CPR-55] [CPR-56], covered by budget provision [CPR-02], awarded only to suppliers checked for suitability and financial standing [CPR-08], with social value considered for service contracts above the goods and services threshold [CPR-01].; C-04-3 Contracts carry the standard clauses [CPR-35], with amended forms approved [CPR-36], the minimum clauses [CPR-37], a Data Protection Impact Assessment [CPR-38] and specifications [CPR-39]; indemnities are relaxed only with written authority [CPR-40], bonds use the approved form [CPR-41] or the risk assessment is approved where none is taken [CPR-42], and insurance levels are set and verified [CPR-43].

### T-04-1 (tests C-04-1, C-04-2)

For each sampled general procurement supplier with an annualised estimate at or above £173,100 and no Contracts Finder notice found [A4], check the supplier against the council's contract register first: a notice gap is an indicator to check, not evidence of off-contract spend. Obtain the written contract, framework call-off or exemption record covering the sampled payments [CPR-32] and confirm it is on the register [CPR-34] [CPR-06], was let by the route for its value [CPR-55] [CPR-56], had budget provision [CPR-02] and a supplier suitability check [CPR-08], and, for services, recorded social value consideration [CPR-01]. Record which suppliers are explained by older contracts, Find a Tender notices or other buyers' frameworks.

- **Sample:** `analytics-full/high_value_suppliers.csv`; filter: dominant_tag = general_procurement; match_class = none; annualised estimate {">=": "$.tests.high_value_suppliers.statutory_tier.parameters.threshold"}; sort: annualised estimate descending; first 25 suppliers (largest 3 payments each). Population 42; drawn 25; 62 transactions, £14,865,447.37. File: `outputs/samples/T-04-1.csv`.
- **PBC:** The council's contract register with values and end dates; The contract, framework call-off or exemption record for each sampled supplier; Purchase orders and invoices for each sampled payment

### T-04-2 (tests C-04-1)

For each general procurement supplier at or above £25,000 whose name only nearly matches a notice [A15] [A16], confirm against the council's contract register whether the notice is the supplier's contract (same legal entity, Companies House number) [CPR-34]; where it is not, obtain the written contract covering the sampled payments [CPR-32]. The file holds all near matches at or above the threshold, so the drawn population can be smaller than the metrics.

- **Sample:** `analytics-full/near-matches.csv`; filter: dominant_tag = general_procurement; annualised_estimate {">=": "$.tests.off_contract.parameters.threshold"}; sort: annualised_estimate descending; first 25 suppliers (largest 3 payments each). Population 6; drawn 6; 18 transactions, £239,360.31. File: `outputs/samples/T-04-2.csv`.
- **PBC:** The council's contract register with values and end dates; The contract, framework call-off or exemption record for each sampled supplier

### T-04-3 (tests C-04-3)

For each written contract obtained under T-04-1 and T-04-2, confirm it contains the standard clauses [CPR-35] and any amended form was approved [CPR-36], the minimum clauses [CPR-37], a Data Protection Impact Assessment [CPR-38] and the specification [CPR-39]; confirm any relaxed indemnity was authorised [CPR-40], any bond used the approved form [CPR-41] or, where none was taken on a contract within the bond rule, the risk assessment was approved [CPR-42], and insurance levels were set and verified [CPR-43].

- **Sample:** none. Performed on the contracts obtained for T-04-1 and T-04-2; no further transactions are drawn.
- **PBC:** The contract, framework call-off or exemption record for each sampled supplier; Data Protection Impact Assessment, bond or bond risk assessment, and insurance evidence for each contract obtained

## R-05: Repeated equal payments to the same supplier within 7 days

Score 9 (Medium - High (Amber)); controls: C-05-1 Each payment is supported by a distinct invoice and written evidence of the purchase and its receipt, so a repeated invoice is identified before payment, and any duplicate paid is identified and recovered [CPR-31].

### T-05-1 (tests C-05-1)

For each sampled general procurement group of equal payments to one supplier at different times within seven days [A5], match every payment to a distinct invoice, purchase order and goods-received record [CPR-31]. Where two payments relate to the same invoice, confirm the duplicate was identified and recovered, and record the recovery date. Instalments and recurring fees are expected causes of this indicator [AUD-11].

- **Sample:** `analytics-full/duplicates.csv`; filter: tier = different_time; tag = general_procurement; sort: gbp_beyond_first descending; first 15 groups (all payments in each). Population 35; drawn 15; 39 transactions, £525,039.22. File: `outputs/samples/T-05-1.csv`.
- **PBC:** Purchase orders and invoices for each sampled payment; Goods-received records for each sampled payment; Duplicate payment reports and recovery records for the spend window

## R-06: Spend with suppliers whose every matching notice ended before the spend window

Score 8 (Medium - High (Amber)); controls: C-06-1 Extensions of existing contracts are approved by the S151 Officer before the original term ends [CPR-62], and awards and extensions are notified for the Council Contract Register with current end dates [CPR-34].

### T-06-1 (tests C-06-1)

For each supplier paid in the spend window whose every matching notice had ended before it [A6], check the council's contract register and obtain the current contract, or the extension and its S151 Officer approval [CPR-62]; confirm the register shows the current end date [CPR-34]. Where a newer contract exists with no notice, record its route and date; where a payment is a one-off purchase below the competition threshold, record that instead of seeking an extension.

- **Sample:** `analytics-full/expired_notice_spend.csv`; filter: none; sort: total_gbp descending; first 15 suppliers (largest 3 payments each). Population 8; drawn 8; 13 transactions, £191,349.42. File: `outputs/samples/T-06-1.csv`.
- **PBC:** The council's contract register with values and end dates; Contract extensions and their S151 Officer approval for each sampled supplier; Purchase orders and invoices for each sampled payment

## R-07: Annualised spend above the published award value for single-supplier notices

Score 10 (Medium - High (Amber)); controls: C-07-1 Variations of scope have prior written Monitoring Officer and S151 Officer approval below the threshold [CPR-63], or relevant-board approval on their recommendation above it [CPR-64].; C-07-2 Contract information, including spend against contract value, is reported to the relevant board monthly so that spend beyond the award is seen [CPR-07].

### T-07-1 (tests C-07-1, C-07-2)

For each supplier whose annualised estimate is at least 1.25 times the annual award rate of its single active notice [A7], obtain the contract and its current value and compare it with actual spend to date; obtain any variation and confirm its approval at the right level [CPR-63] [CPR-64], and confirm the contract appears in the monthly contract report to the board [CPR-07]. Award values may be estimates or maxima and the annualised estimate extrapolates a short window; record where either explains the ratio.

- **Sample:** `analytics-full/spend_vs_award.csv`; filter: flag = True; sort: ratio descending; first 15 suppliers (largest 3 payments each). Population 12; drawn 12; 28 transactions, £795,139.63. File: `outputs/samples/T-07-1.csv`.
- **PBC:** The contract and any variations with their approvals for each sampled supplier; Spend to date against contract value for each sampled supplier; Monthly contract reports to the relevant board for the spend window

## R-10: Waivers, exceptions and award approvals not testable from the spend data

Score 3 (Low (Green)); controls: C-10-1 Awards are approved at the tier their total value requires: Service Director up to the threshold [CPR-50], with reports and board approval above it [CPR-51], as a Key Decision [CPR-52] [CPR-03], and by the Executive at the top tier [CPR-53].; C-10-2 Tenders are handled securely on the portal [CPR-13], late tenders rejected unless the Monitoring Officer agrees [CPR-14], opened with an audit record [CPR-15], evaluated against notified criteria [CPR-16] and awarded on best value [CPR-17], with CDP notices approved by the Service Lead [CPR-10] and the supplier checked for suitability [CPR-08].; C-10-3 Exceptions and waivers are granted only on permitted grounds [CPR-18] with written reasons for discretionary exceptions [CPR-19], by the Monitoring Officer or S151 Officer in advance [CPR-20] at the approval tier for their value [CPR-21] [CPR-22] [CPR-23], fully documented [CPR-24], with an exception report [CPR-25] and a recorded statement of exceptional circumstances [CPR-26].; C-10-4 Appendix C exemptions are approved as required: excluded contracts by the Monitoring Officer [CPR-59], Provider Selection Regime contracts with key decisions recorded [CPR-60], and board approval for exempted contracts above the threshold [CPR-66].

### T-10-1 (tests C-10-1, C-10-2)

For each sampled general procurement supplier above £173,100 with an exact notice match [A17] (that metric counts every spend type; the sample takes general procurement only, so its population is smaller), obtain the award decision and confirm it was approved at the tier for the total contract value [CPR-50] [CPR-51] [CPR-52] [CPR-53], as a Key Decision where required [CPR-03]. Where the award was tendered, inspect the portal record for secure handling and opening [CPR-13] [CPR-15] and any late tender [CPR-14], and confirm evaluation against notified criteria [CPR-16], best value award [CPR-17], CDP notice approval [CPR-10] and the suitability check [CPR-08]. Suppliers with no notice found are covered under R-04.

- **Sample:** `analytics-full/high_value_suppliers.csv`; filter: dominant_tag = general_procurement; match_class = exact; annualised estimate {">=": "$.tests.high_value_suppliers.statutory_tier.parameters.threshold"}; sort: annualised estimate descending; first 5 suppliers (largest 3 payments each). Population 18; drawn 5; 13 transactions, £916,841.43. File: `outputs/samples/T-10-1.csv`.
- **PBC:** Award reports and approval records for each sampled contract; Procurement Portal tender opening and audit records for each sampled contract

### T-10-2 (tests C-10-3, C-10-4)

Walk through the exception, waiver and Appendix C exemption process and obtain the register for the spend window. For the exceptions and exemptions recorded, confirm the grounds [CPR-18] and written reasons [CPR-19], advance approval [CPR-20] at the tier for the value [CPR-21] [CPR-22] [CPR-23], documentation [CPR-24], the exception report [CPR-25] and the statement of exceptional circumstances [CPR-26]; for exemptions, Monitoring Officer approval of excluded contracts [CPR-59], the Provider Selection Regime record [CPR-60] and board approval above the threshold [CPR-66]. Cross-refer any exception that covers a supplier sampled under R-03 or R-04.

- **Sample:** none. The spend data holds no exception, waiver or approval field, so items are selected from the council's exception and exemption register at fieldwork.
- **PBC:** The register of exceptions, waivers and Appendix C exemptions for the spend window, with approvals and exception reports

## R-11: No published tracker of agreed audit actions to confirm prior procurement findings are closed

Score 2 (Low (Green)); controls: C-11-1 Agreed actions from the Contract Letting and Accounts Payable audits are tracked to closure with owners and due dates, so the controls over competitive quotation [CPR-55] and written evidence of purchases [CPR-31] operate as agreed.

### T-11-1 (tests C-11-1)

Obtain the action tracker for the Contract Letting [AUD-01] and Accounts Payable [AUD-11] audits, which the committee papers do not publish [GAP-01]. Confirm the status, owner and due date of each agreed action and, for actions reported closed that concern quotation [CPR-55] or purchase evidence [CPR-31], confirm the evidence of closure.

- **Sample:** none. A document request on the action tracker; no transactions are needed.
- **PBC:** The internal audit action tracker for the Contract Letting and Accounts Payable audits, with status, owners, due dates and closure evidence

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

## PBC list

Documents and information to request from the council before fieldwork.

| # | Item | For tests |
|---|---|---|
| 1 | Purchase orders and invoices for each sampled payment | T-01-1, T-02-1, T-04-1, T-05-1, T-06-1 |
| 2 | Quotation or invitation-to-quote records, evaluation and award decision for each sampled purchase | T-01-1 |
| 3 | Other orders raised with the same supplier for the same requirement | T-01-1, T-02-1 |
| 4 | The contract or order, its total value and the procurement route record for each sampled purchase | T-02-1 |
| 5 | CDP notices and their approval for each sampled contract | T-02-1 |
| 6 | Purchase orders and invoices for each sampled window | T-03-1, T-03-2 |
| 7 | The contract, framework call-off or Purchasing Scheme advice record for each sampled supplier | T-03-1, T-03-2 |
| 8 | Quotation, tender and award approval records for each sampled supplier | T-03-1, T-03-2 |
| 9 | The council's contract register with values and end dates | T-04-1, T-04-2, T-06-1 |
| 10 | The contract, framework call-off or exemption record for each sampled supplier | T-04-1, T-04-2, T-04-3 |
| 11 | Data Protection Impact Assessment, bond or bond risk assessment, and insurance evidence for each contract obtained | T-04-3 |
| 12 | Goods-received records for each sampled payment | T-05-1 |
| 13 | Duplicate payment reports and recovery records for the spend window | T-05-1 |
| 14 | Contract extensions and their S151 Officer approval for each sampled supplier | T-06-1 |
| 15 | The contract and any variations with their approvals for each sampled supplier | T-07-1 |
| 16 | Spend to date against contract value for each sampled supplier | T-07-1 |
| 17 | Monthly contract reports to the relevant board for the spend window | T-07-1 |
| 18 | Award reports and approval records for each sampled contract | T-10-1 |
| 19 | Procurement Portal tender opening and audit records for each sampled contract | T-10-1 |
| 20 | The register of exceptions, waivers and Appendix C exemptions for the spend window, with approvals and exception reports | T-10-2 |
| 21 | The internal audit action tracker for the Contract Letting and Accounts Payable audits, with status, owners, due dates and closure evidence | T-11-1 |
