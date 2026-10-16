# Procurement risk register: West Berkshire Council

**Revision 2: applies the auditor's decisions.** Built 2026-10-16T00:40:54.

Auditor decision at sign-off applied: R-06 amended (likelihood L2 to L3); all other risks unchanged.

Changed in this revision:

- R-06: likelihood 2 → 3; citations +metric:$.tests.expired_notice_spend.top20[0].dominant_tag, +metric:$.tests.expired_notice_spend.top20[1].dominant_tag, +metric:$.tests.expired_notice_spend.top20[2].dominant_tag, +metric:$.tests.expired_notice_spend.top20[3].dominant_tag, +metric:$.tests.expired_notice_spend.top20[4].dominant_tag, +metric:$.tests.expired_notice_spend.top20[5].dominant_tag, +metric:$.tests.expired_notice_spend.top20[6].dominant_tag, +metric:$.tests.expired_notice_spend.top20[7].dominant_tag (auditor: Amend, "Raise likelihood from L2 to L3 (score 12, Amber), as decided at sign-off on challenge #6: all 8 flagged suppliers carry dominant_tag general_procurement in analytics.json, so the L3 condition is shown. Keep in scope; no other change.")

Inputs: `outputs/risk-ratings.json` sha256 ccc32cac2f2b · `outputs/analytics.json` sha256 2f9ef0af85de · `outputs/history.json` sha256 258043779bfe · `outputs/rules.json` sha256 0cdaf851e5cc

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier.

## Method

- Council 5×5 method from the Risk Management Strategy 2024–2027 as recorded in history.json: likelihood LIK-1…5, impact IMP-n-DIM (Table 1), matrix MX-I1…5 (Figure 1), bands BAND-* (Table 4).
- Score = likelihood × impact, checked against the scores printed in Figure 1. Band and RAG from Table 4; 'matrix label' is the Figure 1 cell name.
- Likelihood follows the rubric in `.claude/skills/risk-assessment/SKILL.md`; each signal is evaluated here from analytics.json. A repeat finding (a cited audit or follow-up with an adverse opinion) adds one point, capped at 5, and is stated on the risk.
- Every figure is filled from analytics.json; [M*] marks a metric listed under the risk's evidence.

**Conflicts inside the council's scoring method** (one value used, the other marked; nothing resolved silently):

- Band names differ between the matrix and Table 4 (Figure 1 'High' = Table 4 'Medium - High'). **Used:** Table 4 band and RAG as the band; the Figure 1 name is shown as 'matrix label'. [DISC-03]
- Corporate Risk Register entry is printed as Table 4 'Extreme' (15 -25) [BAND-EXTREME] and as 'score 9 or above' [ESC-CRR]. **Used:** Table 4 for the band and escalation. **Marked:** risks scoring 9 or above but below 15 carry ‡ (CRR-level under ESC-CRR). [DISC-04, DISC-06]
- Financial impact ranges conflict: £ ranges of adjacent levels share their end points; % of budget ranges overlap (level 3 up to 0.3% vs level 4 from 0.25%). **Used:** the £ ranges; a value on a shared end point takes the higher level. **Not used:** the % ranges (no annual budget figure is in the papers). The £ basis is value exposed to the indicator, not a loss. [DISC-02]
- DISC-01 touches inputs this build reads (MX-I3) and is **not resolved by the builder**: §4.3 text gives the Medium impact level as '(2)'; Table 1 and Figure 1 print Medium against 3. [DISC-01]

## Summary

| ID | Risk | L | I | Score | Matrix label | Band | Scope |
|---|---|---|---|---|---|---|---|
| R-01 | Payments just below the £25,000 competition threshold | 2 | 3 | 6 | Moderate | Moderate | in |
| R-02 | Payments just below the £173,100 Procurement Act threshold for goods and services | 3 | 3 | 9 ‡ | High | Medium - High (Amber) | in |
| R-03 | Same-supplier payment windows that cross competition thresholds while each payment stays below | 4 | 5 | 20 | Extreme | Extreme (Red) | in |
| R-04 | High-value general procurement suppliers with no Contracts Finder notice found | 3 | 5 | 15 | Extreme | Extreme (Red) | in |
| R-05 | Repeated equal payments to the same supplier within 7 days | 3 | 3 | 9 ‡ | High | Medium - High (Amber) | in |
| R-06 | Spend with suppliers whose every matching notice ended before the spend window | 3 | 4 | 12 ‡ | High | Medium - High (Amber) | in |
| R-07 | Annualised spend above the published award value for single-supplier notices | 2 | 5 | 10 ‡ | High | Medium - High (Amber) | in |
| R-08 | Recurring care and education placement payments crossing competition thresholds | 2 | 2 | 4 | Moderate | Moderate | out |
| R-09 | Payments clustered just below the £1,000 quotation threshold | 3 | 2 | 6 | Moderate | Moderate | out |
| R-10 | Waivers, exceptions and award approvals not testable from the spend data | 1 | 3 | 3 | Low | Low (Green) | in |
| R-11 | No published tracker of agreed audit actions to confirm prior procurement findings are closed | 1 | 2 | 2 | Low | Low (Green) | in |

‡ CRR-level under ESC-CRR ('score 9 or above'), not under Table 4. See Method.

## R-01: Payments just below the £25,000 competition threshold

46 payments fall in the band just below the threshold at which invitations to quote and a CDP notice are required [CPR-55] [CPR-56], of which 10 are general procurement [M1]. An indicator to investigate, not evidence of non-compliance.

- **Likelihood 2 – Unlikely.** General procurement payments are present in the band below the threshold [M1], but the band count (46) does not exceed the comparator band just above the threshold (52) [M2], so no clustering beyond the comparator is shown.
  - Signals: ✓ $.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n > 0 → 10 > 0; ✓ $.tests.threshold_clustering.per_threshold[?threshold==25000].band_count < $.tests.threshold_clustering.per_threshold[?threshold==25000].comparator_count → 46 < 52
- **Impact 3 – Medium.** Value exposed to the indicator (not a loss) is the general procurement value in the band, £239,428 [M3], which sits in the council's Medium financial band [IMP-3-FIN].
  - £ basis £239,428 [M3] → council £ band level 3
- **Score 6**: matrix label Moderate; band Moderate.
- **Evidence:**
  - CPR-55 (clause App B row B1): goods or services, Total Value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-56 (clause App B row B2): works, concession or light touch contract, Total Value exclusive of VAT £25,000 or more and less than £500,000
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n` = 10
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==25000].comparator_count` = 52
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.gbp` = 239,427.82
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - CPR-54 (clause App B row A): Total Value exclusive of VAT above £1,000 and less than £25,000
  - AUD-01: Contract Letting – Reasonable Assurance (End of March 2025)
  - M4 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_count` = 46
- **Proposed focus:** For the general procurement payments in the band, check whether quotations were sought as required [CPR-54] and whether related orders for the same requirement together reached the competition threshold [CPR-55].
- **Proposed scope:** in. Low cost to test alongside split purchases (R-03); traces the quotation and competition rules [CPR-54] [CPR-55] [CPR-56]; Contract Letting received Reasonable Assurance [AUD-01].

## R-02: Payments just below the £173,100 Procurement Act threshold for goods and services

The band just below the statutory goods and services threshold holds more payments than the band just above it [M1]. Counts are small; an indicator to investigate [CPR-55]. Split-purchase windows at this threshold are rated under R-03, not here.

- **Likelihood 3 – Likely.** The band below the threshold (3 payments) exceeds the comparator band above it (2) [M2], with 2 general procurement payments in the band [M3]. The counts are small; the split-window evidence at this threshold is relied on under R-03 so that the two risks are not double-counted.
  - Signals: ✓ $.tests.threshold_clustering.per_threshold[?threshold==173100].band_count > $.tests.threshold_clustering.per_threshold[?threshold==173100].comparator_count → 3 > 2; ✓ $.tests.threshold_clustering.per_threshold[?threshold==173100].band_by_tag.general_procurement.n > 0 → 2 > 0
- **Impact 3 – Medium.** Value exposed to the clustering indicator (not a loss) is the general procurement value in the band, £318,886 [M4], in the council's Medium financial band [IMP-3-FIN]; the split windows' value is rated under R-03.
  - £ basis £318,886 [M4] → council £ band level 3
- **Score 9**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==173100].band_count` = 3
  - CPR-55 (clause App B row B1): goods or services, Total Value exclusive of VAT £25,000 or more and less than the Threshold
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==173100].comparator_count` = 2
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==173100].band_by_tag.general_procurement.n` = 2
  - M4 `$.tests.threshold_clustering.per_threshold[?threshold==173100].band_by_tag.general_procurement.gbp` = 318,885.53
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - CPR-01 (clause 3.5): procuring a service contract with estimated value above the Threshold for Goods & Services
  - CPR-11 (clause 6.16): any contract or purchase requirement
- **Proposed focus:** For the general procurement payments in the band, establish the total contract value and whether the procurement route and notice met the statutory tier [CPR-55] [CPR-01] and the anti-splitting rule [CPR-11].
- **Proposed scope:** in. Few transactions to test and the statutory tier carries publication duties [CPR-55]; split windows at the same threshold are covered by R-03.

## R-03: Same-supplier payment windows that cross competition thresholds while each payment stays below

Within a 30-day window, payments to one supplier each below a competition threshold combine to cross it in 39 general procurement windows at the lowest competition threshold [M1]. Recurring invoices under one contract also produce this pattern; an indicator to investigate against the anti-splitting rule [CPR-11].

- **Likelihood 4 – Almost Certain.** General procurement split windows are present at £25,000 (39 windows) [M1] and at £173,100 (6) [M2]; at the latter a second test points the same way, with payments clustered below the threshold beyond the comparator band [M3]. The clustering evidence is shared with R-02.
  - Signals: ✓ $.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows > 0 → 39 > 0; ✓ $.tests.split_purchases.per_threshold[?threshold==173100].headline_general_procurement.windows > 0 → 6 > 0; ✓ $.tests.threshold_clustering.per_threshold[?threshold==173100].band_count > $.tests.threshold_clustering.per_threshold[?threshold==173100].comparator_count → 3 > 2; ✓ $.tests.threshold_clustering.per_threshold[?threshold==173100].band_by_tag.general_procurement.n > 0 → 2 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) is the combined value of the general procurement windows at the lowest competition threshold, £2,221,901 [M4], in the council's Critical financial band [IMP-5-FIN].
  - £ basis £2,221,901 [M4] → council £ band level 5
- **Score 20**: matrix label Extreme; band Extreme (Red).
- **Evidence:**
  - M1 `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows` = 39
  - CPR-11 (clause 6.16): any contract or purchase requirement
  - M2 `$.tests.split_purchases.per_threshold[?threshold==173100].headline_general_procurement.windows` = 6
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==173100].band_count` = 3
  - M4 `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.gbp` = 2,221,901.37
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - CPR-55 (clause App B row B1): goods or services, Total Value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-56 (clause App B row B2): works, concession or light touch contract, Total Value exclusive of VAT £25,000 or more and less than £500,000
  - M5 `$.tests.split_purchases.per_threshold[?threshold==173100].headline_general_procurement.gbp` = 3,143,124.33
  - M6 `$.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.windows` = 2
  - AUD-11: Accounts Payable – Reasonable Assurance (End of December 2025)
- **Proposed focus:** For the top general procurement windows, establish whether the payments relate to one requirement and, if so, whether the aggregated value was procured by the route its tier requires [CPR-11] [CPR-55] [CPR-56]; separate call-offs under an awarded contract from unrelated orders.
- **Proposed scope:** in. Core test of the anti-splitting rule [CPR-11] with the largest value exposed among the threshold tests [M4].

## R-04: High-value general procurement suppliers with no Contracts Finder notice found

42 general procurement suppliers with an annualised estimate above the statutory threshold have no matching notice [M1]. The notices file is not a contract register [M2]: no notice found is an indicator to check, never evidence of off-contract spend.

- **Likelihood 3 – Likely.** General procurement suppliers above the competition threshold with no notice found: 185 [M3], of which 42 exceed the statutory threshold [M1]. Capped at L3 because no contract register is available, only published notices [M2].
  - Signals: ✓ $.tests.off_contract.headline_general_procurement_no_notice_found.suppliers > 0 → 185 > 0; ✓ $.tests.off_contract.statutory_tier.headline_general_procurement_no_notice_found.suppliers > 0 → 42 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) is the annualised estimate for the statutory-tier general procurement suppliers with no notice found, £89,309,551 [M4], in the council's Critical financial band [IMP-5-FIN].
  - £ basis £89,309,551 [M4] → council £ band level 5
- **Score 15**: matrix label Extreme; band Extreme (Red).
- **Evidence:**
  - M1 `$.tests.off_contract.statutory_tier.headline_general_procurement_no_notice_found.suppliers` = 42
  - M2 `$.contracts.register_present` = False
  - M3 `$.tests.off_contract.headline_general_procurement_no_notice_found.suppliers` = 185
  - M4 `$.tests.off_contract.statutory_tier.headline_general_procurement_no_notice_found.annualised_estimate_gbp` = 89,309,550.84
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - CPR-55 (clause App B row B1): goods or services, Total Value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-01 (clause 3.5): procuring a service contract with estimated value above the Threshold for Goods & Services
  - M5 `$.tests.off_contract.headline_general_procurement_no_notice_found.annualised_estimate_gbp` = 97,868,511.80
  - RT-06: Contracts & Partnerships (source of risk prompt)
- **Proposed focus:** Request the council's contract register and the contract, framework call-off or exemption record for each statutory-tier supplier with no notice found [CPR-55] [CPR-01]; record which are explained by older contracts or Find a Tender notices.
- **Proposed scope:** in. Largest value exposed in the register [M4]; resolving it needs the contract register, a fieldwork request.

## R-05: Repeated equal payments to the same supplier within 7 days

Payments of the same amount to the same supplier at different times within 7 days form 35 general procurement groups [M1]. Instalments and recurring fees also produce this pattern; an indicator to investigate.

- **Likelihood 3 – Likely.** General procurement groups at different timestamps (the higher-signal tier) are present: 35 [M1]. Accounts Payable received Reasonable Assurance [AUD-11], which is coverage, not a repeat finding.
  - Signals: ✓ $.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups > 0 → 35 > 0
- **Impact 3 – Medium.** Value exposed (not a loss) is the general procurement value beyond the first payment in each group, £299,374 [M2], in the council's Medium financial band [IMP-3-FIN].
  - £ basis £299,374 [M2] → council £ band level 3
- **Score 9**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups` = 35
  - AUD-11: Accounts Payable – Reasonable Assurance (End of December 2025)
  - M2 `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.gbp_beyond_first` = 299,374.24
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - M3 `$.tests.duplicates.per_tier.same_timestamp.by_tag.general_procurement.groups` = 33
  - RT-07: Finance (source of risk prompt incl. financial control, fraud and corruption)
- **Proposed focus:** For the largest general procurement groups, match each payment to a distinct invoice and goods-received record; confirm any duplicate was identified and recovered [AUD-11].
- **Proposed scope:** in. Cheap, transaction-level test on a defined population [M1]; complements the Accounts Payable audit [AUD-11].

## R-06: Spend with suppliers whose every matching notice ended before the spend window

> **Auditor override (revision 2):** Amend: "Raise likelihood from L2 to L3 (score 12, Amber), as decided at sign-off on challenge #6: all 8 flagged suppliers carry dominant_tag general_procurement in analytics.json, so the L3 condition is shown. Keep in scope; no other change.". Changed: likelihood 2 → 3; citations +metric:$.tests.expired_notice_spend.top20[0].dominant_tag, +metric:$.tests.expired_notice_spend.top20[1].dominant_tag, +metric:$.tests.expired_notice_spend.top20[2].dominant_tag, +metric:$.tests.expired_notice_spend.top20[3].dominant_tag, +metric:$.tests.expired_notice_spend.top20[4].dominant_tag, +metric:$.tests.expired_notice_spend.top20[5].dominant_tag, +metric:$.tests.expired_notice_spend.top20[6].dominant_tag, +metric:$.tests.expired_notice_spend.top20[7].dominant_tag.

8 suppliers were paid in the window although every matching notice had ended before it [M1]. A newer contract or approved extension may exist with no notice; an indicator to check against extension approvals [CPR-62].

- **Likelihood 3 – Likely.** The indicator is present [M1] and every flagged supplier's dominant spend tag is general procurement [M2] [M3] [M4] [M5] [M6] [M7] [M8] [M9], so the indicator sits on the general procurement population. The rating stays at L3, not higher, because the notices file is not a contract register [M10].
  - Signals: ✓ $.tests.expired_notice_spend.suppliers > 0 → 8 > 0
- **Impact 4 – Major.** Value exposed (not a loss) is the annualised estimate of spend with these suppliers, £973,458 [M11], in the council's Major financial band [IMP-4-FIN].
  - £ basis £973,458 [M11] → council £ band level 4
- **Score 12**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.expired_notice_spend.suppliers` = 8
  - CPR-62 (clause App C row D): extension of an existing contract that provides for extension
  - M2 `$.tests.expired_notice_spend.top20[0].dominant_tag` = general_procurement
  - M3 `$.tests.expired_notice_spend.top20[1].dominant_tag` = general_procurement
  - M4 `$.tests.expired_notice_spend.top20[2].dominant_tag` = general_procurement
  - M5 `$.tests.expired_notice_spend.top20[3].dominant_tag` = general_procurement
  - M6 `$.tests.expired_notice_spend.top20[4].dominant_tag` = general_procurement
  - M7 `$.tests.expired_notice_spend.top20[5].dominant_tag` = general_procurement
  - M8 `$.tests.expired_notice_spend.top20[6].dominant_tag` = general_procurement
  - M9 `$.tests.expired_notice_spend.top20[7].dominant_tag` = general_procurement
  - M10 `$.contracts.register_present` = False
  - M11 `$.tests.expired_notice_spend.annualised_estimate_gbp` = 973,457.68
  - IMP-4-FIN: 4 Major – Financial loss to Council: 0.25% - 1% annual WBC budget £500k £2M
  - M12 `$.tests.expired_notice_spend.gbp_in_window` = 243,364.42
- **Proposed focus:** For each supplier, obtain the current contract or the extension and its approval by the S151 Officer [CPR-62].
- **Proposed scope:** in. Small, fully listed population [M1]; only test tracing the extension approval rule [CPR-62].

## R-07: Annualised spend above the published award value for single-supplier notices

12 of 23 suppliers matched to one active notice have an annualised estimate at least 1.25 times the annual award rate [M1]. Award values may be estimates or maxima; an indicator to check against variation approvals [CPR-63] [CPR-64].

- **Likelihood 2 – Unlikely.** The indicator is present [M1], but the analytics give no general procurement breakdown for this test, so the L3 condition cannot be shown.
  - Signals: ✓ $.tests.spend_vs_award.flagged > 0 → 12 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) is the flagged suppliers' annualised estimate, £5,353,417 [M2], in the council's Critical financial band [IMP-5-FIN].
  - £ basis £5,353,417 [M2] → council £ band level 5
- **Score 10**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.spend_vs_award.flagged` = 12
  - CPR-63 (clause App C row E): variation of scope of an existing contract, contract value below the Threshold
  - CPR-64 (clause App C row E): variation of scope of an existing contract, contract value greater than the Threshold
  - M2 `$.tests.spend_vs_award.flagged_annualised_estimate_gbp` = 5,353,417.28
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
- **Proposed focus:** For flagged suppliers, compare actual spend to the contract value and obtain any variation and its approval [CPR-63] [CPR-64].
- **Proposed scope:** in. Small, fully listed population [M1]; only test tracing the variation approval rules [CPR-63] [CPR-64].

## R-08: Recurring care and education placement payments crossing competition thresholds

Placement payments form 126 same-supplier windows crossing the lowest competition threshold [M1]. Placements may be awarded without competition if reasons are recorded [CPR-65]; periodic fees legitimately recur. An indicator to check the exemption records.

- **Likelihood 2 – Unlikely.** Indicators are present only on the placement population [M1] [M2], which may be exempt from competition [CPR-65], so the rating stays at L2. Purchase of residential and nursing care received Reasonable Assurance [AUD-14] (coverage, not a repeat finding).
  - Signals: ✓ $.tests.split_purchases.per_threshold[?threshold==25000].by_tag.care_or_education_placement.windows > 0 → 126 > 0; ✓ $.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.care_or_education_placement.n > 0 → 30 > 0
- **Impact 2 – Minor.** The rule at stake is recording the reasons for the choice of provider on case notes [CPR-65]; a missing record is a compliance gap with low possibility of legal challenge or regulatory interest [IMP-2-CMP].
- **Score 4**: matrix label Moderate; band Moderate.
- **Evidence:**
  - M1 `$.tests.split_purchases.per_threshold[?threshold==25000].by_tag.care_or_education_placement.windows` = 126
  - CPR-65 (clause App C row F): individual social care / SEN placement or package awarded without competition (items a-f)
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.care_or_education_placement.n` = 30
  - AUD-14: Purchase of Residential and Nursing Care Provision – Reasonable Assurance (End of December 2025)
  - IMP-2-CMP: 2 Minor – Compliance (litigation, regulatory, contract): Low possibility of legal challenge. Low possibility regulatory interest
  - M3 `$.tests.split_purchases.per_threshold[?threshold==25000].by_tag.care_or_education_placement.gbp` = 13,571,816.01
  - AUD-12: Personal Budgets (Direct Payments) – Limited Assurance (End of December 2025)
- **Proposed focus:** For a sample of placement suppliers with windows crossing the threshold, confirm the reasons for the choice of provider are recorded on case notes [CPR-65].
- **Proposed scope:** out. Exempt population [CPR-65] recently covered by a Reasonable Assurance audit [AUD-14]; recommended for a later plan unless the auditor wishes to include it.

## R-09: Payments clustered just below the £1,000 quotation threshold

The band just below the single-quote threshold holds more payments than the band just above it [M1], including general procurement payments. An indicator to investigate against the quotation rule [CPR-54].

- **Likelihood 3 – Likely.** The band (323) exceeds the comparator (219) [M2], with 88 general procurement payments in the band [M3]; most of the band is placement spend.
  - Signals: ✓ $.tests.threshold_clustering.per_threshold[?threshold==1000].band_count > $.tests.threshold_clustering.per_threshold[?threshold==1000].comparator_count → 323 > 219; ✓ $.tests.threshold_clustering.per_threshold[?threshold==1000].band_by_tag.general_procurement.n > 0 → 88 > 0
- **Impact 2 – Minor.** Value exposed (not a loss) is the general procurement value in the band, £84,148 [M4], in the council's Minor financial band [IMP-2-FIN].
  - £ basis £84,148 [M4] → council £ band level 2
- **Score 6**: matrix label Moderate; band Moderate.
- **Evidence:**
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==1000].band_count` = 323
  - CPR-54 (clause App B row A): Total Value exclusive of VAT above £1,000 and less than £25,000
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==1000].comparator_count` = 219
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==1000].band_by_tag.general_procurement.n` = 88
  - M4 `$.tests.threshold_clustering.per_threshold[?threshold==1000].band_by_tag.general_procurement.gbp` = 84,148.45
  - IMP-2-FIN: 2 Minor – Financial loss to Council: 0.01% - 0.1% of annual WBC budget £17.5k - £175k
- **Proposed focus:** For a sample of general procurement payments in the band, confirm a quote was obtained [CPR-54].
- **Proposed scope:** out. Low value exposed [M4] and the rule asks only for one quote [CPR-54]; traced here so the rule is covered.

## R-10: Waivers, exceptions and award approvals not testable from the spend data

The rules require named approvals for exceptions to competition and for awards by value tier [CPR-18] [CPR-20] [CPR-50]; the spend data holds no approval or contract-type field, so these controls are tested by walkthrough and sample, not analytics.

- **Likelihood 1 – Rare.** No data indicator: approvals are not in the spend data and the contract-type field needed for the statutory tiers is absent; only the rules [CPR-20] and coverage by the Contract Letting audit (Reasonable Assurance) [AUD-01] are cited.
- **Impact 3 – Medium.** An unapproved exception or award above the statutory threshold carries a reasonable possibility of successful legal challenge [IMP-3-CMP] [CPR-22].
- **Score 3**: matrix label Low; band Low (Green).
- **Evidence:**
  - CPR-18 (clause 7.2): exception or waiver of competition for a contract with value more than £24,999.99
  - CPR-20 (clause 7.3): any waiver of or exception to these Rules
  - CPR-50 (clause App A row 1): Total Contract Value up to relevant Threshold
  - AUD-01: Contract Letting – Reasonable Assurance (End of March 2025)
  - IMP-3-CMP: 3 Medium – Compliance (litigation, regulatory, contract): Reasonable possibility of successful legal challenge. Reasonable possibility of regulatory interest.
  - CPR-22 (clause 7.4.2): exception for a contract above the relevant Threshold and up to £500,000
  - CPR-21 (clause 7.4.1): exception for a contract up to the Threshold
  - CPR-23 (clause 7.4.3): exception for a contract over £500,000
  - CPR-51 (clause App A row 2): Total Contract Value above the relevant threshold and less than £500,000
  - CPR-52 (clause App A row 3): Total Contract Value above £500,000 and less than £2.5million
  - CPR-53 (clause App A row 4): Total Contract Value £2.5million or more
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==500000].band_count` = 0
  - GAP-01: Agreed actions / action tracker (theme, due date, status, overdue)
- **Proposed focus:** Walk through the waiver and exception log and award approvals; test approvals for the high-value suppliers drawn in R-04 and R-03 against the approval tiers [CPR-21] [CPR-22] [CPR-23] [CPR-50] [CPR-51] [CPR-52] [CPR-53].
- **Proposed scope:** in. Approver rules cannot be tested from the data and need control testing [CPR-20]; no clustering or split windows at the upper value tier [M1], so no separate risk there.

## R-11: No published tracker of agreed audit actions to confirm prior procurement findings are closed

The committee papers publish no action tracker, due dates or statuses [GAP-01], so the status of actions from the Contract Letting and Accounts Payable audits cannot be confirmed [AUD-01] [AUD-11].

- **Likelihood 1 – Rare.** Only a gap is cited, with no data indicator [GAP-01].
- **Impact 2 – Minor.** Unconfirmed closure of agreed actions is a governance gap with low possibility of regulatory interest [IMP-2-CMP].
- **Score 2**: matrix label Low; band Low (Green).
- **Evidence:**
  - GAP-01: Agreed actions / action tracker (theme, due date, status, overdue)
  - AUD-01: Contract Letting – Reasonable Assurance (End of March 2025)
  - AUD-11: Accounts Payable – Reasonable Assurance (End of December 2025)
  - IMP-2-CMP: 2 Minor – Compliance (litigation, regulatory, contract): Low possibility of legal challenge. Low possibility regulatory interest
- **Proposed focus:** Request the action tracker for the Contract Letting and Accounts Payable audits and confirm the status of each agreed action [AUD-01] [AUD-11].
- **Proposed scope:** in. A one-line request on the PBC list closes the gap [GAP-01].

## Risks excluded by the builder

None.

## Build notes

- R-06: auditor override departs from the rubric: L3 needs a signal on the general_procurement population

## Auditor decisions

Record a decision for every risk in `outputs/auditor-comments.md` (Approve, Amend or Reject, with a comment for Amend and Reject), then ask for the risk-assessor to be re-run. It re-issues this register as the next revision, applying exactly what you asked and nothing else. The audit program is not built until every risk is decided and applied.

| Risk ID | Decision recorded | Comment |
|---|---|---|
| R-01 | Approve |  |
| R-02 | Amend | Reduce likelihood from L4 to L3 (score 9, Amber). Clustering below £173,100 rests on only 3 payments vs 2 above, which is too thin for L4; keep in scope. Rely on R-03 for the split-window evidence so the two risks are not double-counted. |
| R-03 | Approve |  |
| R-04 | Approve |  |
| R-05 | Approve |  |
| R-06 | Amend | Raise likelihood from L2 to L3 (score 12, Amber), as decided at sign-off on challenge #6: all 8 flagged suppliers carry dominant_tag general_procurement in analytics.json, so the L3 condition is shown. Keep in scope; no other change. |
| R-07 | Approve |  |
| R-08 | Approve |  |
| R-09 | Approve |  |
| R-10 | Approve |  |
| R-11 | Approve |  |
