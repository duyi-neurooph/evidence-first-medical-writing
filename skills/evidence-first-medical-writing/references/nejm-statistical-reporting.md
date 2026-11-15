# NEJM statistical-reporting profile

Profile: 0.7.1. Prepared: 2026-11-15. Intended official source: [NEJM New Manuscripts — Statistical Reporting Guidelines](https://www.nejm.org/author-center/new-manuscripts). Live verification on 2026-11-15 failed with HTTP 403. This operational summary was checked against an author-supplied, undated copy of sections A (all studies), B (clinical trials), and C (observational studies). **Version currency unverified.** The supplied source and private path are not distributed. Linked external papers and the separate time-to-event document were not part of that copy; do not claim to have read them.

Use with [statistical-policy-router.md](statistical-policy-router.md). The following are provisional target-NEJM checkpoints or optional benchmarks elsewhere, not universal automatic editing commands.

## A. All studies

- **Protocol/SAP:** ask for dated original/final versions, substantive changes and rationale, enough detail to reproduce the analyses, and a concise Methods description of primary/secondary/exploratory procedures and sample-size considerations. Never invent planning documents. Scientific problems in a prespecified analysis still need transparent author/statistician review, not silent preservation or undocumented replacement.
- **Interpretation/display:** distinguish clinical importance from statistical significance. Present effect estimates with uncertainty. Verify test sidedness against the design; noninferiority may need a one-sided framework. Use sensible precision and the target's P-value conventions, with special handling for stopping rules and genome-wide testing. Do not modify analysis decisions by rounding. Ratio estimates in forest plots need appropriate log-scale interval/display treatment, not a change to the underlying effect definition.
- **Multiplicity:** the supplied copy expects a prespecified family-wise error strategy for confirmatory analyses and allows a prespecified false-discovery-rate strategy for suitable exploratory analyses. Label adjusted P values. Its hierarchical-testing display rule stops before the first nonsignificant comparison and omits subsequent P values. Do not hide the corresponding outcomes or effect estimates.
- **Unadjusted secondary/exploratory outcomes:** without prespecified multiplicity control, the copy calls for estimates with 95% CIs instead of P-value claims. State that intervals are not multiplicity-adjusted and cannot substitute for confirmatory testing; limit conclusions accordingly. This is not an instruction to delete every P value in every manuscript. Check safety and other applicable exceptions, target policy, and the actual SAP.
- **Missing data:** quantify missing values for baseline, response and predictor variables across reported analyses. The supplied guidance generally disallows a primary complete-case analysis unless missingness is rare. Require context-supported assumptions, appropriate methods and sensitivity analyses when needed. Imputation, weighting and model-based approaches are possibilities, not automatic remedies; ask the statistician before changing the primary analysis.
- **Time-to-event analyses:** assess proportional-hazards assumptions with supporting diagnostics. The supplied policy asks for alternative summaries if those assumptions are inconsistent with the data. Competing events may require cumulative-incidence and question-matched association measures. Distinguish the estimand and censoring mechanism before recommending a change; do not declare every cause-specific Cox model invalid or calculate a replacement from insufficient summaries.
- **Bayesian work:** check consistency of design and analysis, likelihood, priors, posterior computation/summaries, and prior sensitivity. The copy discourages adding frequentist analyses beside a primary Bayesian analysis; this is a journal preference, not a license to remove a prespecified analysis without explanation.

## B. Clinical trials

- Reconcile the primary analysis with the final protocol/SAP and transparently explain deviations. Do not rewrite post hoc decisions as prespecified.
- Baseline randomized-group tables should not contain hypothesis-test P values; still describe clinically relevant imbalances or allocation concerns.
- Subgroup forest plots remain subject to multiplicity: the copy omits treatment-by-subgroup interaction P values when outside the prespecified adjustment plan. Do not replace an interaction assessment with comparisons of within-group significance.
- Safety outcomes that are not primary endpoints have a stated exception to mandatory multiplicity adjustment; editors may request adverse-event comparisons. Do not apply the secondary-efficacy display rule blindly to safety or suppress a safety signal.
- Post-randomization exclusions used to create a per-protocol set can bias an estimate. Identify the actual estimand, adherence and analysis strategy and request expert review where needed. Do not impose a blanket rule that every per-protocol or noninferiority sensitivity analysis must be erased.
- Present absolute events/rates as well as relative measures. The copy prefers risk ratios in general and asks for justification of odds ratios. Do not relabel an OR as an RR or recalculate without the required information.
- Check participant flow and applicable CONSORT materials. Distinguish sensitivity analyses of assumptions/methods from arbitrary subset analyses.

## C. Observational studies

- Examine selection, measured/unmeasured confounding, adjustment rationale and diagnostics. Where balance is required after weighting/matching, inspect appropriate standardized-difference diagnostics; a baseline P value is not proof of balance.
- The supplied copy requests protocol-equivalent information and an SAP even if written after analysis. Date it honestly and explicitly state its timing relative to preliminary analyses. Report actual primary/secondary aims and decision chronology, not invented preregistration.
- Association-only analyses require association wording. A causal target requires methods designed for causal inference, explicit identification assumptions, justification and diagnostics; a method name alone does not establish a causal effect. Describe residual uncertainty and sensitivity to unmeasured confounding. This conditional allowance differs from JAMA's target-specific wording policy.
- Independent replication can strengthen robustness, but a secondary analysis of the same data is not independent confirmation. Do not demand unavailable replication merely to fill a reviewer report.

## Use and limitations

Report the assessed manuscript locations, exact information gaps and whether a concern needs explanation, author confirmation or reanalysis. An inaccessible official page does not stop an offline methodological review, but it prevents an unqualified claim that these are the latest NEJM requirements. Recheck affected policies before final compliance certification and use the actual target's rules for submission.
