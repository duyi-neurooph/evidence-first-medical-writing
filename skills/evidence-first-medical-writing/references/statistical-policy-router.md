# Offline-first statistical review and journal-policy routing

## When to load

Use for substantive statistical/Methods writing, quantitative Results or table review, a statistical reviewer remit, or a whole clinical-research manuscript audit. Trigger phrases include “JAMA statistical requirements,” “NEJM statistics,” “review the statistical methods,” and “JAMA 统计学要求.” Load this file, then only the relevant journal profile. A nonquantitative Perspective, spelling correction, or literal translation does not need a trial-statistics audit.

This extends the existing design/integrity checks and [journal-guidance.md](journal-guidance.md); it is not a second intake, reporting checklist, or statistical certification. Reuse the Design Confirmation Card and Manuscript Contract. Do not ask again for facts already confirmed.

## Two separate judgments

1. **Methodological assessment:** use [design-and-integrity.md](design-and-integrity.md), the protocol/SAP, actual analysis outputs, and the local review prompts below. These checks can proceed offline. A well-reported analysis can still be invalid; a missing description is not proof the method was wrong.
2. **Target-journal compliance:** use the actual target's current applicable instructions. The local [JAMA profile](jama-statistical-reporting.md) or [NEJM profile](nejm-statistical-reporting.md) is a dated reading aid, not a permanent policy registry. For a different target, use them only as explicitly optional benchmarks, never as automatic rejection criteria.

Load the local profiles first. Do not require repeated JAMA/NEJM downloads for every statistical edit, paragraph, reviewer, or review round. Verify the affected live policy before claiming current target-journal compliance, on a target/article-type change, or when the user requests the latest rules. This does not remove the existing runtime EQUATOR retrieval step for substantive reporting assessments. Reuse already verified sources within the task. If external access is prohibited or the official source fails, follow the bounded fallback in [reporting-guideline-retrieval.md](reporting-guideline-retrieval.md), use the dated local material provisionally, and state `Current journal compliance not verified`. Do not repeatedly retry a 403, bypass access controls, or call a search snippet full-text verification.

Record selected profiles in the existing Guideline Manifest: profile version, preparation/check date, official URL, original source coverage, supplied-copy provenance when applicable, currency, and role. A profile's preparation date is not the publisher's policy date. Do not attach or redistribute private source copies.

## Local review prompts

These are operational questions, not a demand to redo every study:

- What question and estimand does each analysis address? Check the population, comparison, outcome, timing, and handling of intercurrent events against the design and protocol. Preserve the actual analysis; do not infer an estimand from an OR/HR alone.
- Can an analyst reproduce the reported procedure from the descriptions and authorized materials? Identify the analysis set, outcome coding, model/link, covariates and rationale, transformations, dependence structure, diagnostics, software/version and relevant packages. Unknown details become focused author queries, not invented defaults.
- Separate original planning, documented amendments, post hoc decisions, and exploratory work. Reconcile dated protocol/SAP versions and endpoint hierarchy. A retrospectively prepared SAP must say so; an honest reconstruction does not make analyses prespecified.
- Assess precision and recruitment limitations without manufacturing a post hoc sample-size justification. Distinguish a fixed existing population from researcher-selected sampling. Do not use observed power to rescue inconclusive results.
- Quantify missingness by variable, group, time and analysis set where relevant. Ask about mechanisms, contextual assumptions and sensitivity. Neither complete-case analysis nor multiple imputation is automatically valid. Missing-at-random assumptions cannot be proved from observed data alone; descriptive comparisons are not proof of an ignorable mechanism.
- Identify the testing family, confirmatory hierarchy, adjustment plan, and exploratory claims before interpreting a P value or interval. Do not infer subgroup differences from one significant and one nonsignificant within-group result. Use an appropriate interaction assessment and respect its prespecification/multiplicity limits.
- Match survival, competing-event, repeated-measure, clustered, diagnostic, prediction or synthesis methods to the actual question. A doubtful assumption triggers a specific statistical query; do not mechanically replace an analysis or manufacture estimates.
- Reconcile counts, denominators, units, reference groups, effect estimates, uncertainty and interpretation across text/tables/figures. Investigate apparent CI/P disagreements using the same test, sidedness, adjustment and rounding. Never recompute a result from rounded summaries when the required inputs are absent.

## Resolve common policy conflicts explicitly

- **Baseline Table 1:** distinguish randomized-group comparisons from observational balance assessment. Neither a significant nor nonsignificant baseline P value establishes successful randomization or adequate confounding control. Do not extend a randomized-trial display rule into an alleged universal ban for all study types. Do not insert observational baseline P values merely for symmetry; justify the diagnostic used.
- **Causal wording:** a design label, regression or propensity score is not enough. An observational causal estimand requires appropriate identification assumptions, methods and diagnostics, with residual limitations. A target journal may still impose narrower wording: apply the JAMA profile's target-specific rule separately from the NEJM profile's conditional methodological allowance. Do not strengthen a claim or change the author's scientific meaning on their behalf.
- **P values and multiplicity:** do not impose NEJM's display restrictions on every journal or delete a valid primary result wholesale. Distinguish confirmatory, secondary, exploratory, safety and sequential analyses. Preserve all verified results in author materials; proposed manuscript display changes need a stated policy basis and author review.
- **Precision:** journal formatting is not a new analysis. Preserve exact underlying outputs; never write `P=0.000`, infer significance from a rounded `.05`, or change an inferential decision by rounding. Flag boundary cases and special designs instead of inventing extra digits. Do not present an ordinary unadjusted CI as simultaneous coverage.

## Findings and independent review

Use the existing Issue Matrix or location-specific diagnosis, adding an explicit category: `Methodological concern`, `Target-journal requirement`, or `Optional benchmark`. Each finding states location, manuscript evidence, source/profile section, consequence for interpretation, smallest action, and whether it needs direct editing, author confirmation, source verification or statistician-led reanalysis. Report unavailable inputs and unverified policies separately. No major concern is a valid outcome.

For independent review, freeze the same selected profile versions and clean verified sources before dispatch. Keep editor judgments and other reviewers' findings out of reviewer packets. Do not change skill or guidance versions mid-round; reconcile any later policy change explicitly through the editor and Decision Ledger. Keep AI disclosure reminder-only under [ai-use-and-disclosure.md](ai-use-and-disclosure.md); no AI-use history is collected.
