# Procurement risk register: West Berkshire Council

**Revision 1: applies the auditor's decisions.** Built 2026-10-15T11:56:28.

Auditor approved all nine risks (R-01 to R-09) as proposed; no amendments, rejections or other instructions.

Changed in this revision:

- nothing; every risk was approved as drafted

Inputs: `outputs/risk-ratings.json` sha256 587c95e03948 · `outputs/analytics.json` sha256 0b3d49cd62bb · `outputs/history.json` sha256 e86dfdda1f41 · `outputs/rules.json` sha256 31d360d118a1

These are **risk indicators to investigate**, not findings of wrongdoing by the council, a service or a supplier.

## Method

- Council 5×5 method from the Risk Management Strategy 2024–2027 as recorded in history.json: likelihood LIK-1…5, impact IMP-n-DIM (Table 1), matrix MX-I1…5 (Figure 1), bands BAND-* (Table 4).
- Score = likelihood × impact, checked against the scores printed in Figure 1. Band and RAG from Table 4; 'matrix label' is the Figure 1 cell name.
- Likelihood follows the rubric in `.claude/skills/risk-assessment/SKILL.md`; each signal is evaluated here from analytics.json. A repeat finding (a cited audit or follow-up with an adverse opinion) adds one point, capped at 5, and is stated on the risk.
- Every figure is filled from analytics.json; [M*] marks a metric listed under the risk's evidence.

**Conflicts inside the council's scoring method** (one value used, the other marked; nothing resolved silently):

- Band names differ between the matrix and Table 4 (Figure 1 'High' = Table 4 'Medium - High'). **Used:** Table 4 band and RAG as the band; the Figure 1 name is shown as 'matrix label'. [DISC-03]
- Corporate Risk Register entry is printed as Table 4 'Extreme' (15 -25) [BAND-EXTREME] and as 'score 9 or above' [ESC-CRR]. **Used:** Table 4 for the band and escalation. **Marked:** risks scoring 9 or above but below 15 carry ‡ (CRR-level under ESC-CRR). [DISC-04]
- Financial impact ranges conflict: £ ranges of adjacent levels share their end points; % of budget ranges overlap (level 3 up to 0.3% vs level 4 from 0.25%). **Used:** the £ ranges; a value on a shared end point takes the higher level. **Not used:** the % ranges (no annual budget figure is in the papers). The £ basis is value exposed to the indicator, not a loss. [DISC-02]
- DISC-01 touches inputs this build reads (MX-I3) and is **not resolved by the builder**: Section 4.3 prints the Medium impact level as 'Medium (2)'; Table 1 and Figure 1 print Medium against 3. [DISC-01]

## Summary

| ID | Risk | L | I | Score | Matrix label | Band | Scope |
|---|---|---|---|---|---|---|---|
| R-01 | Payments within ten per cent below the £25,000 quotation threshold | 2 | 3 | 6 | Moderate | Moderate | in |
| R-02 | Payments just below the £500,000 tender and key-decision threshold | 1 | 4 | 4 | Moderate | Moderate | out |
| R-03 | Multiple payments to one supplier within a short window that together cross a competition threshold | 3 | 5 | 15 | Extreme | Extreme (Red) | in |
| R-04 | High-value suppliers with no matching Contracts Finder notice | 3 | 5 | 15 | Extreme | Extreme (Red) | in |
| R-05 | Repeated payments of the same amount to the same supplier within a week | 3 | 3 | 9 ‡ | High | Medium - High (Amber) | in |
| R-06 | Spend with suppliers whose every matching notice ended before the spend window | 2 | 3 | 6 | Moderate | Moderate | in |
| R-07 | Annualised spend above the published award value for single-supplier notices | 2 | 5 | 10 ‡ | High | Medium - High (Amber) | in |
| R-08 | Placement spend patterns: aggregated windows and repeated equal payments | 2 | 5 | 10 ‡ | High | Medium - High (Amber) | in |
| R-09 | No published action tracker to confirm follow-up of prior procurement audit actions | 1 | 2 | 2 | Low | Low (Green) | in |

‡ CRR-level under ESC-CRR ('score 9 or above'), not under Table 4. See Method.

## R-01: Payments within ten per cent below the £25,000 quotation threshold

46 payments sit just below the £25,000 point at which invitations to quote via the Procurement Portal are required [CPR-54] [CPR-55], of which 10 are general procurement [M1]. This is an indicator to investigate, not a finding.

- **Likelihood 2 – Unlikely.** An indicator is present on general procurement (10 payments in the band [M1]), but across all spend the band below the threshold (46) does not exceed the comparator band just above it (52) [M2], so there is no clustering signal beyond the comparator; rubric L2.
  - Signals: ✓ $.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n > 0 → 10 > 0; ✓ $.tests.threshold_clustering.per_threshold[?threshold==25000].band_count < $.tests.threshold_clustering.per_threshold[?threshold==25000].comparator_count → 46 < 52
- **Impact 3 – Medium.** Value exposed (not a loss) is the general procurement spend in the band, £239,428 [M3], which falls in the council's Medium financial level [IMP-3-FIN].
  - £ basis £239,428 [M3] → council £ band level 3
- **Score 6**: matrix label Moderate; band Moderate.
- **Evidence:**
  - CPR-54 (clause App B row B1): goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-55 (clause App B row B2): works, concession or light touch contract, total value exclusive of VAT £25,000 or more and less than £500,000
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.n` = 10
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==25000].comparator_count` = 52
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_by_tag.general_procurement.gbp` = 239,427.82
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - CPR-53 (clause App B row A): total value exclusive of VAT above £1,000 and less than £25,000
  - CPR-19 (clause 7.2.2): exception or waiver under 7.2 on discretionary grounds (value more than £24,999.99)
  - AUD-01: Contract Letting – Reasonable Assurance (End of March 2025)
  - M4 `$.tests.threshold_clustering.per_threshold[?threshold==25000].band_count` = 46
- **Proposed focus:** For the general procurement payments in the band, check whether one quote was sought [CPR-53] and whether related orders together reached £25,000 without invitations to quote [CPR-54]; test alongside the split-purchase windows (R-03) at the same threshold.
- **Proposed scope:** in. Low-cost to test with R-03 at the same threshold and gives the only data test of [CPR-53] and [CPR-19]; Contract Letting last had Reasonable Assurance [AUD-01].

## R-02: Payments just below the £500,000 tender and key-decision threshold

The full-tender and key-decision requirements apply above £500,000 [CPR-56] [CPR-04]. No payments fall in the band below it [M1] and none below the £2,500,000 Executive-approval point [M2].

- **Likelihood 1 – Rare.** No data indicator: the band below £500,000 holds 0 payments [M1] and the band below £2,500,000 holds 0 [M2]; only the rules are cited [CPR-56]; rubric L1.
- **Impact 4 – Major.** Contracts above £500,000 without a full competitive tender or key decision would carry a high possibility of legal challenge [IMP-4-CMP] [CPR-56] [CPR-04].
- **Score 4**: matrix label Moderate; band Moderate.
- **Evidence:**
  - CPR-56 (clause App B row C): works, concession or light touch contract, total value exclusive of VAT above £500,000 and less than the Threshold (works/concession or light touch threshold as applicable)
  - CPR-04 (clause 4.3): contract award with a value over £500,000
  - M1 `$.tests.threshold_clustering.per_threshold[?threshold==500000].band_count` = 0
  - M2 `$.tests.threshold_clustering.per_threshold[?threshold==2500000].band_count` = 0
  - IMP-4-CMP: 4 Major – Compliance (litigation, regulatory, contract): High possibility of legal challenge. High possibility of regulatory intervention.
  - CPR-11 (clause 6.16): any contract, at any value
  - CPR-50 (clause App A row 2): total contract value above the relevant threshold and less than £500,000
  - CPR-51 (clause App A row 3): total contract value above £500,000 and less than £2.5million
  - CPR-52 (clause App A row 4): total contract value £2.5million or more
  - M3 `$.tests.threshold_clustering.per_threshold[?threshold==500000].baseline_count` = 12
- **Proposed focus:** None from the clustering test; aggregation above £500,000 is covered by the split-purchase windows in R-03 [CPR-11].
- **Proposed scope:** out. No payments in the band [M1]; approver rules at this level ([CPR-50] [CPR-51] [CPR-52]) trace to R-03 and R-04, which test aggregated and supplier-level spend.

## R-03: Multiple payments to one supplier within a short window that together cross a competition threshold

39 general procurement suppliers had payments each under £25,000 that together reached it within 30 days, and 2 did so at £500,000 [M1] [M2]. The rules prohibit artificial disaggregation [CPR-11]; the pattern is an indicator to investigate, as many windows will reflect regular invoicing under one contract.

- **Likelihood 3 – Likely.** Holding signals on the general procurement population at both competition thresholds: 39 windows at £25,000 [M1] and 2 at £500,000 [M2]. Clustering at the same threshold does not beat its comparator (R-01), so no second test supports L4; rubric L3. The population is expenditure over the publication floor only, so counts are a lower bound [M3].
  - Signals: ✓ $.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows > 0 → 39 > 0; ✓ $.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.windows > 0 → 2 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) in the general procurement windows at £25,000 is £2,221,901 [M4], within the council's Critical financial level [IMP-5-FIN].
  - £ basis £2,221,901 [M4] → council £ band level 5
- **Score 15**: matrix label Extreme; band Extreme (Red).
- **Evidence:**
  - M1 `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.windows` = 39
  - M2 `$.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.windows` = 2
  - CPR-11 (clause 6.16): any contract, at any value
  - M3 `$.tests.split_purchases.note` = population is expenditure over £500 only, so results are a lower bound; placement windows reported separately because periodic care fees legitimately recur
  - M4 `$.tests.split_purchases.per_threshold[?threshold==25000].headline_general_procurement.gbp` = 2,221,901.37
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - CPR-54 (clause App B row B1): goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-56 (clause App B row C): works, concession or light touch contract, total value exclusive of VAT above £500,000 and less than the Threshold (works/concession or light touch threshold as applicable)
  - M5 `$.tests.split_purchases.per_threshold[?threshold==500000].headline_general_procurement.gbp` = 3,509,528.75
- **Proposed focus:** For the top general procurement windows, establish whether the payments relate to one requirement and, if so, whether invitations to quote or a tender were run at the aggregate value [CPR-54] [CPR-56] or a contract covers them; record where the payments are instalments under an existing contract [CPR-11].
- **Proposed scope:** in. Strongest general procurement signal with the highest value exposed [M4]; the only data test of the anti-avoidance rule [CPR-11].

## R-04: High-value suppliers with no matching Contracts Finder notice

186 general procurement suppliers with an annualised estimate at or above £25,000 have no matching active notice [M1]. contracts.csv holds published notices, not a contract register, so a missing notice is an indicator to check, never evidence of off-contract spend [M2].

- **Likelihood 3 – Likely.** A holding signal on the general procurement population: 186 suppliers with no notice found [M1]. Capped at L3 because no contract register is available [M2]; only suppliers above the publication threshold are classified, so smaller suppliers are not questioned [M3].
  - Signals: ✓ $.tests.off_contract.headline_general_procurement_no_notice_found.suppliers > 0 → 186 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) is the annualised estimate for these suppliers, £97,905,912 [M4], within the council's Critical financial level [IMP-5-FIN].
  - £ basis £97,905,912 [M4] → council £ band level 5
- **Score 15**: matrix label Extreme; band Extreme (Red).
- **Evidence:**
  - M1 `$.tests.off_contract.headline_general_procurement_no_notice_found.suppliers` = 186
  - M2 `$.contracts.register_present` = False
  - M3 `$.tests.off_contract.publication_note` = Contracts Finder does not carry smaller awards; only suppliers at or above the publication threshold are classed, and results must never be used to question smaller suppliers.
  - M4 `$.tests.off_contract.headline_general_procurement_no_notice_found.annualised_estimate_gbp` = 97,905,911.80
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - CPR-07 (clause 5.2.1): all contracts in progress and awarded
  - CPR-54 (clause App B row B1): goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
  - CPR-55 (clause App B row B2): works, concession or light touch contract, total value exclusive of VAT £25,000 or more and less than £500,000
  - CPR-20 (clause 7.3): any waiver of or exception to these Rules
  - CPR-21 (clause 7.4.1): exception for a contract up to the Threshold
  - RT-05: Contracts and partnerships (procurement contract management)
  - CPR-57 (clause App B row D): goods, services, works, concession or light touch contract, total value exclusive of VAT above the Threshold
  - GAP-08: Assessed procurement/contract risks in any register
- **Proposed focus:** Request the council's contract register [CPR-07] and, for the top suppliers by annualised estimate, the contract, the quotation or tender record [CPR-54] [CPR-55] or the approved exception [CPR-20] [CPR-21].
- **Proposed scope:** in. Largest value exposed [M4] and contracts are a source-of-risk prompt for the council [RT-05]; the statutory-threshold tier could not be tested because the threshold is not in the rules [CPR-57].

## R-05: Repeated payments of the same amount to the same supplier within a week

35 general procurement groups of equal payments to one supplier at different times within 7 days [M1]. These are indicators of possible duplicate payment to investigate; many will be legitimate recurring charges.

- **Likelihood 3 – Likely.** A holding signal on general procurement in the higher-signal tier (different timestamps): 35 groups [M1]; rubric L3. Accounts Payable had Reasonable Assurance [AUD-11], which is coverage, not a repeat finding.
  - Signals: ✓ $.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups > 0 → 35 > 0
- **Impact 3 – Medium.** Value exposed (not a loss) beyond the first payment in each general procurement group is £299,374 [M2], in the council's Medium financial level [IMP-3-FIN].
  - £ basis £299,374 [M2] → council £ band level 3
- **Score 9**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.groups` = 35
  - AUD-11: Accounts Payable – Reasonable Assurance (End of December 2025)
  - M2 `$.tests.duplicates.per_tier.different_time.by_tag.general_procurement.gbp_beyond_first` = 299,374.24
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - CPR-31 (clause 10.1): every purchase
- **Proposed focus:** For the top different-time groups, obtain the invoices and purchase evidence [CPR-31] and confirm each payment relates to a distinct supply; note any credit or recovery.
- **Proposed scope:** in. General procurement signal with value exposed in the Medium band [M2]; quick to test from invoices.

## R-06: Spend with suppliers whose every matching notice ended before the spend window

8 suppliers were paid in the window although every matching notice had ended before it began [M1]. Extensions need S151 Officer approval [CPR-61]; a newer contract or extension may exist with no notice [M2].

- **Likelihood 2 – Unlikely.** The indicator is present, 8 suppliers [M1], but the test has no general procurement breakdown, so L3 is not supported; rubric L2.
  - Signals: ✓ $.tests.expired_notice_spend.suppliers > 0 → 8 > 0
- **Impact 3 – Medium.** Value exposed (not a loss) is the spend in the window with these suppliers, £236,350 [M3], in the council's Medium financial level [IMP-3-FIN].
  - £ basis £236,350 [M3] → council £ band level 3
- **Score 6**: matrix label Moderate; band Moderate.
- **Evidence:**
  - M1 `$.tests.expired_notice_spend.suppliers` = 8
  - CPR-61 (clause App C row D): extension of an existing contract where the contract provides for extension
  - M2 `$.tests.expired_notice_spend.caveat` = Indicator of spend after notice expiry without an approved extension; a newer contract or extension may exist with no notice. **contracts.csv holds published *notices*, not a contract register.** It holds awards published on Contracts Finder in roughly the last five years. A contract awarded earlier (e.g. long-running waste or highways contracts), one advertised only on Find a Tender, a framework call-off recorded under another buyer, or an exempt placement will have no notice here. **"No notice found" is therefore an indicator to check against the council's contract register, never evidence of off-contract spend.** Say so in every output that reports it.
  - M3 `$.tests.expired_notice_spend.gbp_in_window` = 236,349.86
  - IMP-3-FIN: 3 Medium – Financial loss to Council: 0.1% - 0.3% annual WBC budget £175k -500k
  - M4 `$.tests.expired_notice_spend.annualised_estimate_gbp` = 945,399.44
- **Proposed focus:** For each listed supplier, request the current contract or the approved extension [CPR-61].
- **Proposed scope:** in. Small, fully testable list [M1] and the only data test of the extension approval rule [CPR-61].

## R-07: Annualised spend above the published award value for single-supplier notices

12 of 22 suppliers compared have an annualised estimate at least 1.25 times the annual award value [M1]. Variations need prior approval [CPR-62] [CPR-63]; award values may be estimates or maxima [M2].

- **Likelihood 2 – Unlikely.** The indicator is present, 12 flagged suppliers [M1], but the test has no general procurement breakdown, so L3 is not supported; rubric L2.
  - Signals: ✓ $.tests.spend_vs_award.flagged > 0 → 12 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) is the annualised estimate for the flagged suppliers, £5,353,417 [M3], within the council's Critical financial level [IMP-5-FIN].
  - £ basis £5,353,417 [M3] → council £ band level 5
- **Score 10**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.spend_vs_award.flagged` = 12
  - CPR-62 (clause App C row E (below Threshold)): variation of scope of an existing contract (permitted by the contract or legislation), contract value below the Threshold
  - CPR-63 (clause App C row E (above Threshold)): variation of scope of an existing contract, contract value greater than the Threshold
  - M2 `$.tests.spend_vs_award.caveat` = Indicator of spend beyond the award without an approved variation; award values may be estimates or maxima, and the annualised estimate extrapolates three months.
  - M3 `$.tests.spend_vs_award.flagged_annualised_estimate_gbp` = 5,353,417.28
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - M4 `$.tests.spend_vs_award.suppliers_compared` = 22
- **Proposed focus:** For the flagged suppliers, compare actual spend to the contract value and request any approved variation or extension report [CPR-62] [CPR-63].
- **Proposed scope:** in. High value exposed [M3] on a short list, and the only data test of the variation approval rules [CPR-62] [CPR-63].

## R-08: Placement spend patterns: aggregated windows and repeated equal payments

Placement spend shows 126 windows crossing £25,000 [M1] and 204 equal-payment groups [M2]. Individually chosen placements may be exempt from competition, with reasons recorded on the case record [CPR-64].

- **Likelihood 2 – Unlikely.** Indicators are present only outside general procurement, in placements that may be exempt [CPR-64] [M1]; rubric caps placement-only evidence at L2. Purchase of Residential and Nursing Care Provision had Reasonable Assurance [AUD-14], which is coverage, not a repeat finding.
  - Signals: ✓ $.tests.split_purchases.per_threshold[?threshold==25000].care_or_education_placement.windows > 0 → 126 > 0; ✓ $.tests.duplicates.per_tier.different_time.by_tag.care_or_education_placement.groups > 0 → 204 > 0
- **Impact 5 – Critical.** Value exposed (not a loss) in placement windows is £13,571,816 [M3], within the council's Critical financial level [IMP-5-FIN].
  - £ basis £13,571,816 [M3] → council £ band level 5
- **Score 10**: matrix label High; band Medium - High (Amber); ‡ CRR-level under ESC-CRR.
- **Evidence:**
  - M1 `$.tests.split_purchases.per_threshold[?threshold==25000].care_or_education_placement.windows` = 126
  - M2 `$.tests.duplicates.per_tier.different_time.by_tag.care_or_education_placement.groups` = 204
  - CPR-64 (clause App C row F): individual social care placements/packages listed in row F (a)–(f)
  - AUD-14: Purchase of Residential and Nursing Care Provision – Reasonable Assurance (End of December 2025)
  - M3 `$.tests.split_purchases.per_threshold[?threshold==25000].care_or_education_placement.gbp` = 13,571,816.01
  - IMP-5-FIN: 5 Critical – Financial loss to Council: > 1% annual WBC budget >£2m
  - AUD-12: Personal Budgets (Direct Payments) – Limited Assurance (End of December 2025)
- **Proposed focus:** For a sample of the largest placement windows and equal-payment groups, confirm the reasons for the provider choice are on the case record [CPR-64] and that repeated equal payments relate to distinct periods of care.
- **Proposed scope:** in. High value exposed [M3]; a limited case-record test complements recent coverage [AUD-14] rather than repeating it.

## R-09: No published action tracker to confirm follow-up of prior procurement audit actions

The public papers publish no agreed actions, due dates or status [GAP-01], and no assessed procurement risk [GAP-08], so implementation of actions from Contract Letting [AUD-01] cannot be confirmed from the inputs.

- **Likelihood 1 – Rare.** No data indicator; only gaps are cited [GAP-01] [GAP-08]; rubric L1.
- **Impact 2 – Minor.** Unconfirmed follow-up of agreed actions carries a low possibility of regulatory interest [IMP-2-CMP] [GAP-01].
- **Score 2**: matrix label Low; band Low (Green).
- **Evidence:**
  - GAP-01: Agreed actions / action tracker (theme, due date, status)
  - GAP-08: Assessed procurement/contract risks in any register
  - AUD-01: Contract Letting – Reasonable Assurance (End of March 2025)
  - IMP-2-CMP: 2 Minor – Compliance (litigation, regulatory, contract): Low possibility of legal challenge. Low possibility regulatory interest
  - AUD-11: Accounts Payable – Reasonable Assurance (End of December 2025)
- **Proposed focus:** Request the internal audit action tracker for Contract Letting [AUD-01] and Accounts Payable [AUD-11] and confirm the status of agreed actions.
- **Proposed scope:** in. A single document request that closes an evidence gap for planning [GAP-01].

## Risks excluded by the builder

None.

## Auditor decisions

Record a decision for every risk in `outputs/auditor-comments.md` (Approve, Amend or Reject, with a comment for Amend and Reject), then ask for the risk-assessor to be re-run. It re-issues this register as the next revision, applying exactly what you asked and nothing else. The audit program is not built until every risk is decided and applied.

| Risk ID | Decision recorded | Comment |
|---|---|---|
| R-01 | Approve |  |
| R-02 | Approve |  |
| R-03 | Approve |  |
| R-04 | Approve |  |
| R-05 | Approve |  |
| R-06 | Approve |  |
| R-07 | Approve |  |
| R-08 | Approve |  |
| R-09 | Approve |  |
