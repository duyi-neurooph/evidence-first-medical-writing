# Offline-first statistical review and journal-policy routing

## When to load

Use for substantive statistical/Methods writing, quantitative Results or table review, a statistical reviewer remit, or a whole clinical-research manuscript audit. Trigger phrases include “JAMA statistical requirements,” “NEJM statistics,” “review the statistical methods,” and “JAMA 统计学要求.” Load this file, then only the relevant journal profile. A nonquantitative Perspective, spelling correction, or literal translation does not need a trial-statistics audit.

This extends the existing design/integrity checks and [journal-guidance.md](journal-guidance.md); it is not a second intake, reporting checklist, or statistical certification. Reuse the Design Confirmation Card and Manuscript Contract. Do not ask again for facts already confirmed.

For P-value editing or a table that reports tests, go directly to [P-value display and table notes](#p-value-display-and-table-notes). A formatting request alone does not authorize new analyses.

## Two separate judgments

1. **Methodological assessment:** use [design-and-integrity.md](design-and-integrity.md), the protocol/SAP, actual analysis outputs, and the local review prompts below. These checks can proceed offline. A well-reported analysis can still be invalid; a missing description is not proof the method was wrong.
2. **Target-journal compliance:** use the actual target's current applicable instructions. The local [JAMA profile](jama-statistical-reporting.md) or [NEJM profile](nejm-statistical-reporting.md) is a dated reading aid, not a permanent policy registry. For a different target, use them only as explicitly optional benchmarks, never as automatic rejection criteria.

Load the local profiles first. Do not require repeated JAMA/NEJM downloads for every statistical edit, paragraph, reviewer, or review round. Verify the affected live policy before claiming current target-journal compliance, on a target/article-type change, or when the user requests the latest rules. This does not remove the existing runtime EQUATOR retrieval step for substantive reporting assessments. Reuse already verified sources within the task. If external access is prohibited or the official source fails, follow the bounded fallback in [reporting-guideline-retrieval.md](reporting-guideline-retrieval.md), use the dated local material provisionally, and state `Current journal compliance not verified`. Do not repeatedly retry a 403, bypass access controls, or call a search snippet full-text verification.

Record selected profiles in the existing Guideline Manifest: profile version, preparation/check date, official URL, original source coverage, supplied-copy provenance when applicable, currency, and role. A profile's preparation date is not the publisher's policy date. Do not attach or redistribute private source copies.

## Verify the software that produced the reported results

During Methods drafting, statistical review and presubmission checks, identify the software and version used for the reported analysis, regardless of who ran it (author, collaborating statistician, external service or another team). Identify the analysis-defining extensions and their versions when applicable: for example, the R package fitting the primary model or the Python library estimating its intervals, not the manuscript editor, plotting tools or every installed dependency. If different tools produced different results, map each to its analysis. Follow the target journal's instructions about placement, manufacturer and required details. Reporting key package versions is this skill's reproducibility default, not necessarily a journal mandate.

Use evidence tied to the original run: a dated session report or package log, an environment lockfile confirmed for that run, an output header, or the analyst's confirmation. A version installed on the writer's computer today, an available update or an analysis plan alone cannot establish which version produced a result. If the evidence is missing or contradictory, retain what is known and send a precise query to the author/analyst for the unresolved item. Do not fill it from memory, infer the package from a test name, or rerun a model to guess its provenance. Ordinary software, external statistical expertise and AI assistance with the writing are **not evidence of AI-assisted statistical analysis**.

For an analysis already done by the author, a statistician, or a service, verify the software from that run and advise keeping its original syntax or GUI records. Do not invent code, rerun an analysis just to fill a gap, or label it AI-assisted because AI edited the manuscript. A script reconstructed later must be labeled as such, never as the original.

## Handoff for an authorized analysis run

This skill does not supply a statistics engine. These rules govern work done with a separate, available tool: the user must explicitly request the analysis, with appropriate data access and permission. Plan the handoff before running it. If the tool did not run, say so; proposed code or an analysis plan is not an executed result. Writing, review, or restyling a figure is not authorization to analyze data. An arithmetic check used only for an audit stays in the audit record.

1. **Choose the method before its implementation.** Match the estimand, design and assumptions to the method. Prefer a mature implementation appropriate to that method (e.g., Python's `statsmodels`, an established R package, or the procedure in the chosen statistical software). Do not hand-code routine tests or models. If custom computation is necessary, explain which requirement the existing implementations do not meet and check it against a known answer, independent implementation or appropriate benchmark. Report the validation result and its limits; if it cannot be validated, do not present it as ready for the manuscript.
2. **Return what the author needs to rerun the reported numbers.** For an authorized run that produces or changes a value in the text, tables or figures, deliver the actual analysis file(s), not just a code excerpt, output screenshot or promise to save them. Identify the versioned input (without redistributing private data), how to run the files in order, the inclusion/exclusion and variable/outcome definitions, missing-data handling, model and key parameters. Capture the software and key package versions from that run; record the seed and relevant settings when randomness is involved. Link outputs to the manuscript values they generate. Prefer the native format: Python `.py` or a notebook runnable top to bottom from a fresh kernel; R `.R`; Stata `.do`; SAS `.sas`; SPSS `.sps`, or equivalent. For GUI-only work, return exported syntax if available, otherwise the project or a replayable record of selections and settings. Distinguish later reconstruction from original execution. If permitted and feasible, rerun from the documented input and compare the reported outputs; distinguish a successful replay from an untested handoff. If file delivery is unavailable, provide the complete runnable contents and instructions and state that no file was saved.
3. **Separate author retention from submission.** Keep whatever determines a reported number, even when it lives in a plotting script: retain the computation of a forest plot's effect estimates and confidence intervals; font changes, page layout and image export alone need not be delivered. If the steps are inseparable, retain the working mixed script. Give the author this material privately; do not automatically append it to a submission or upload it. Prepare a sharing copy when the journal, protocol or funder requires it, subject to permissions. Check code, notebooks (including stored outputs), logs and file paths for identifiers, secrets and machine-specific paths before sharing; use relative paths or documented input parameters. Where permitted, verify that redaction and path changes have not broken the rerun; state what was tested.

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
- **Precision:** preserve underlying outputs. Never infer significance from a rounded `.05` or change an inferential decision by rounding. Do not present an ordinary unadjusted CI as simultaneous coverage.

## P-value display and table notes

First decide which P values are appropriate to report under the design and target policy. A different journal rule takes precedence over this skill's default, in prose, tables and figures alike. Otherwise, report the specific P value where available. Classify using the **unrounded** output, then format; keep three decimal places, including trailing zeros:

| Verified value before rounding | Display |
|---|---|
| Below 0.001 | `P < 0.001` (never `P = 0.000`) |
| 0.001 through 0.999, **both endpoints included** | Equality to three decimals, e.g. `P = 0.001`, `P = 0.040`, `P = 0.999` |
| Above 0.999 but below 1 | `P > 0.999`, even if the value would round to 0.999 or 1.000 |
| Exactly 1, confirmed from the analysis | `P = 1.000` |

Rounding is a display choice, not a new statistical decision. For example, a raw 0.0496 displays as `P = 0.050`; do not use that display to reinterpret the prespecified test or replace its estimate and interval.

A software display of `1.000` does not establish that the underlying value is exactly one, or that it is strictly below one. If only a rounded output or an inequality such as `P < 0.05` is available, preserve what is known; ask for higher-precision output or confirmation when needed. Never invent an equality, extra precision or an analysis. For verified unrounded decimal strings only, the optional [formatter](../scripts/format_p_value.py) applies this default offline: `python3 scripts/format_p_value.py --unrounded 0.99901`. Add `--exact-one` only if the analysis confirms exact equality to one.

Read each statistical table on its own: can the reader identify the **actual test for each reported P value**, without consulting Methods? Use the author's confirmed analysis record. If methods differ, mark each P-value cell with a journal-permitted superscript letter or symbol keyed to a note naming its test (including the variant when it matters). If the journal disallows such markers, use an explicit test label beside each value or another permitted one-to-one mapping. If every P value comes from the same test, one note explicitly covering **all** P values suffices. Keep method markers distinct from significance stars; an unkeyed list of tests is not a mapping.

For a multicategory variable, place its omnibus P value and method marker on the variable row; leave the category rows without that test. Do not imply pairwise comparisons. If the source does not establish which method or contrast produced a value, ask for that mapping; never infer it from the P value or variable type, or run a test just to fill a footnote.

## Findings and independent review

Use the existing Issue Matrix or location-specific diagnosis, adding an explicit category: `Methodological concern`, `Target-journal requirement`, or `Optional benchmark`. Each finding states location, manuscript evidence, source/profile section, consequence for interpretation, smallest action, and whether it needs direct editing, author confirmation, source verification or statistician-led reanalysis. Report unavailable inputs and unverified policies separately. No major concern is a valid outcome.

For independent review, freeze the same selected profile versions and clean verified sources before dispatch. Keep editor judgments and other reviewers' findings out of reviewer packets. Do not change skill or guidance versions mid-round; reconcile any later policy change explicitly through the editor and Decision Ledger. Keep AI disclosure reminder-only under [ai-use-and-disclosure.md](ai-use-and-disclosure.md); no AI-use history is collected.
