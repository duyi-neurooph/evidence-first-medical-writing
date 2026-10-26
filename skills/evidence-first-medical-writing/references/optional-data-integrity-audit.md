# Optional Source-Data and Statistical Integrity Audit

## Offer, consent, and scope

During substantive writing or review, briefly offer a bounded reconciliation of authorized, de-identified source data with the manuscript's tables, figures, and statistical methods. Offer once; do not repeatedly solicit data after a refusal. Data sharing and this audit are never prerequisites for writing help. If declined, unavailable, or outside scope, continue the requested writing/review and record `Not performed` with the coverage limitation, without adverse inference.

If accepted, agree on the specific files, variables, outcomes, manuscript locations, computations, and deliverables before inspecting data. A request for an audit authorizes only its stated scope, not unrestricted access or new research analyses. Use the same safeguards across disciplines; do not assume that all records describe patients or that all studies are clinical trials.

Request only what the agreed checks require:

- the minimum authorized de-identified data subset, with stable nonidentifying record keys;
- a data dictionary defining variables, units, codings, missing-value codes, groups, dates/time origins, repeated observations, and relevant derivations;
- the relevant protocol/statistical analysis plan, analysis-set and exclusion definitions, and available analysis code/output;
- the exact manuscript version, table rows/columns, figure panels, legends, and source-data files to reconcile.

Do not request identifiable patient records, linkage keys, unnecessary free text, or full databases by default. Explain that removing names alone may not de-identify combinations of dates, locations, or rare attributes. If identifying information appears, stop inspecting the affected content and request an appropriately minimized/de-identified version; do not repeat it in logs or findings. This audit is not clinical advice, ethics approval, or privacy clearance.

Keep private data in the authorized environment. Do not upload it to websites, external analysis services, repositories, or other destinations, or send it to another reviewer, without specific authorization for that transfer. Public methodology searches must not contain private records or unpublished identifying details. An available tool or connected account is not transfer permission.

## Establish provenance and preserve originals

Record the file/version, supplied scope, author-described provenance, and whether each input is an original observation export, cleaned/derived analysis dataset, aggregate output, or figure-data export. Do not label derived exports as original raw records. Reproducing an analysis export verifies consistency within that export, not its correspondence with original observations or the authenticity of the study.

Use read-only inspection and preserve originals. If computation needs working files, use clearly named, versioned copies within the authorized workspace; record transformations and never silently correct source values. Review supplied code and its data/network effects before execution. Do not run macros or code that would modify originals or transmit data. Do not install tools or dependencies without authorization.

## Bounded, reproducible checks

Prioritize the agreed outcomes and a manageable set of high-impact tables/figures. State coverage rather than claiming an exhaustive audit. When authorized tools and inputs permit a simple check, actually calculate it; otherwise describe the proposed check and mark it `Not performed` or `Cannot assess`. Never imply that visual inspection, a suggested formula, or an unexecuted script is a computed result.

For every computation, retain the input version, exact file/sheet/range or record keys and variable names, selection/filter and grouping rules, formula/code, missing-value handling, software/version where relevant, and output. Specify rounding tolerance and any matching tolerance before interpreting discrepancies; do not tune them to produce a desired finding. Preserve unrounded calculations for comparison.

| Check | Reproducible procedure and interpretation boundary |
|---|---|
| Structure and analysis population | Count rows and unique observational units separately; check keys, group labels, visit structure, eligibility, exclusions, and missingness against the stated analysis set. Reconcile denominators and participant/sample flow without summing overlapping sets or treating repeated observations as independent participants. |
| Basic values and summaries | Check dictionary-supported ranges, units, coding, missing sentinels, dates/time windows, numerators, denominators, percentages, and totals. Recalculate the agreed summaries using the same population, timing, transformations, and definitions; report both manuscript and computed values plus their difference. Out-of-range values require verification, not automatic deletion. |
| Dispersion and precision | Verify the reported mean/SD or median/IQR against the actual calculation, distribution, and scientific purpose; record the SD denominator and quantile convention when relevant. SD/IQR describe observation variability; SE and confidence intervals describe estimation precision and must not be substituted or relabeled as SD/IQR. |
| Tables and figures | Map each checked table cell or figure panel to its underlying data and calculation, including group order, units, timing, error-bar meaning, and rounding. Use the numerical figure-data source, not plotted pixels as if they were raw data. An image alone supports only limited visual checks, not exact numerical reproduction. |
| Repeated records or sequences | Compare prespecified relevant variable combinations and contiguous value sequences within and across groups; record exact matched keys/rows, variables, sequence length, values or safely minimized excerpts, and exact versus tolerance-based matching. State the number of records examined and matching rule, not just an anomaly count. |
| Reported analyses | Reproduce only agreed calculations that the available inputs and methods identify sufficiently. Compare effect estimates, uncertainty intervals, and P values with the stated model, contrast, analysis set, and adjustment. An aggregate table may permit arithmetic checks but not reconstruction of individual-level models. |

## Interpret repeated values without accusations

Repeated multivariate records or long value sequences across supposedly independent groups warrant source verification, particularly when they represent distinct independent observational units. They are anomalies, not proof of fabrication, copying, or misconduct. Distinguish duplicated records from repeated measurements of the same unit and repeated displayed rounded summaries.

Consider explanations supported by the design and provenance: shared controls, paired or longitudinal observations, discrete measurements, structural zeros, rounding, limited instrument precision, deterministic derived variables, formula fill, import/join duplication, or legitimate reuse of a reference series. Ask the author or data custodian to confirm the explanation from source records and processing history; do not declare a benign explanation established merely because it is plausible.

Do not apply Benford's law, digit-frequency tests, P-value patterns, or other generic fraud screens universally. Do not invent chance probabilities or infer intent from an unusual pattern. Any specialized test requires appropriate assumptions, a defensible reference model, and explicit limits; no screening result establishes authenticity or misconduct.

## Assess whether the statistical method fits

Compare the reported method with the confirmed design, outcome scale, estimand, contrast, and protocol/analysis plan. Where relevant assess:

- independence, pairing, repeated measures, clustering, and the unit of allocation versus analysis;
- missing-data definitions/handling, censoring, follow-up/time origin, and analysis-set consistency;
- covariate choice and timing, confounding, model assumptions/diagnostics, multiplicity, and prespecified versus exploratory status;
- effect sizes, reference groups, uncertainty intervals, clinical or scientific importance, and interpretation beyond P values.

State what is supported, what is a reporting omission, and what cannot be assessed without code/data or expert judgment. Do not prescribe a different test solely from sample size or normality-test significance. Do not launch new analyses, remove observations, change thresholds, redefine analysis sets, or relabel endpoints to improve significance. A proposed reanalysis needs a methodological reason, author/statistician confirmation, appropriate authorization, and transparent labeling of deviations or post hoc work.

## Optional Data Audit Ledger

When accepted, deliver a concise ledger or linked file; when declined/unavailable, a short scope note with `Not performed` is sufficient. Use `Not performed` for checks not run and `Cannot assess` when a scoped question lacks the evidence or capability for judgment. Use one row per check or discrepancy:

| Field | Required content |
|---|---|
| Check ID and scope | Stable ID; authorized question; data/manuscript versions; raw-versus-derived provenance and coverage. |
| Evidence location | Exact file, sheet, range/record keys, variables, and corresponding table cell, figure panel, legend, or manuscript passage. Avoid identifying details. |
| Method and observed fact | Executed formula/code and filters, actual output versus reported value, difference/tolerance, or explicit reason no calculation was possible. |
| Interpretation | Separate reproducible discrepancy or methodological risk from hypotheses; record plausible benign explanations and their confirmation status. |
| Limitations and impact | Missing evidence, unresolved assumptions, affected interpretation, and whether source verification or reanalysis could change the conclusion. |
| Owner and next action | Author, data custodian, statistician, or appropriately scoped specialist; exact evidence/action needed. |
| Status | `No discrepancy detected within scope`, `Discrepancy—verification required`, `Methodological concern`, `Explained with evidence`, `Resolved and rechecked`, `Not performed`, or `Cannot assess`. |

Retain original findings and the evidence for resolution; link accepted corrections to manuscript issue IDs and recheck affected abstract, text, tables, figures, supplements, and conclusions. No-discrepancy findings apply only to the checked inputs and rules, never certify authenticity. Preserve unresolved conflicts rather than silently choosing a preferred number. Restrict unsupported affected claims while continuing safe, unaffected writing; refusal to share data is not a credibility failure.

Always keep source-data agreement separate from manuscript logic. After reconciliation, run the two-layer F1 check in [final-submission-audit.md](final-submission-audit.md) on the available prose, tables and figures: copied values can agree with the dataset while denominators, units, time points, group direction or interpretations contradict one another. Report `Source-data reconciliation` and `Within-manuscript logical consistency` separately; a pass in one does not pass the other. Without source data, the second layer still applies and the first remains `Not performed` or `Cannot assess`.

## Escalation without dependency

Escalate material unexplained discrepancies to the author/data custodian for source confirmation, and design/model or consequential reanalysis questions to a qualified statistician or domain methodologist. Explain the precise limitation, required input, and potential effect on interpretation; do not publicly accuse anyone or present an audit as a formal misconduct determination.

For spreadsheet reconstruction, statistical reproduction, or scientific image comparison beyond the current capability, inspect the tools and skills actually available and their documented scope. If a suitable specialized skill is available and authorized, offer or use it within the agreed data boundaries; read its instructions and retain this audit's evidence limits. Never fabricate a skill name, availability, installation command, or download URL. Do not install anything or transfer private data without specific authorization. A specialist tool is optional, not a dependency for writing assistance; if unavailable, provide a concrete human-review handoff and mark the unperformed checks honestly.
