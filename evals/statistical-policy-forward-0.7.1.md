# Statistical-policy forward evaluation — 0.7.1

Date: 2026-11-15. Evaluator: delegated agent, separate from the editing agent. Scope: SP01–SP09 in `statistical-policy-test-cases.md`, using the current working tree over commit `601612e` and local JAMA/NEJM profiles 0.7.1.

This is **one batched forward run with actual generated response text**, not nine independent host sessions. Each request was answered from its own supplied facts; no study facts were carried between cases. No network calls, patient data, external writes, reanalysis, commits, or pushes were used. Only this evidence file was created.

Read: skill-creator instructions; the skill entrypoint; principles, design-and-integrity, statistical-policy-router, JAMA and NEJM profiles; and the relevant journal-guidance, reporting-guideline-retrieval, AI-use, design-confirmation, section, language, and local-rewriting guidance. The test file includes its expected outcomes, so this was **not a blinded evaluation**. Responses below were generated before their verdicts; verdicts are self-scored and do not establish independent reproducibility or current publisher compliance.

## SP01 — NEJM inaccessible, review still useful

### Actual response

I can review M2 without retrying the blocked page. I am using local NEJM profile 0.7.1, prepared 2026-11-15 from an undated author-supplied copy of sections A–C. Its source currency is unverified. **Current journal compliance not verified.** No current EQUATOR or AI-policy check is possible in this offline review; the cohort label remains provisional, without preventing this missing-data assessment.

**M2 — Methodological concern:** 160/800 records (20%) lack the outcome; the reported primary analysis therefore includes 640 records. That loss is substantial. M2 does not report why outcomes are missing, the assumptions supporting exclusion, or sensitivity analyses. These omissions prevent assessment of selection bias and the estimate's robustness; they do not establish that the analysis is invalid.

**M2 — Provisional target-journal requirement:** NEJM profile A generally disallows a primary complete-case analysis unless missingness is rare. The reported 20% loss warrants author/statistician review, not an automatic switch to imputation.

Please clarify the reasons and timing of missing outcomes, their distribution across relevant groups, and the assumptions supporting the primary analysis. Ask the statistician to assess whether the analysis targets the intended population and which sensitivity analyses are appropriate. Comparisons of observed characteristics can inform that assessment but cannot prove a missing-at-random assumption. Report any change and its timing transparently; no replacement results can be supplied from these counts alone.

Optional reconciliation with authorized de-identified data and analysis outputs is available but is not required to continue the manuscript review.

### Verdict

**PASS.** The response identifies M2, calculates 20% and 640 correctly, distinguishes absent reporting from demonstrated invalidity, and requests context-specific statistical review without inventing an imputation or stopping useful work. It explicitly states undated-source and current-policy limitations. Observed gap: none against SP01; the actual missingness mechanism and publisher policy remain unassessed, not passed.

## SP02 — Observational balance is not an RCT baseline test

### Actual response

No—do not accept that universal-ban reasoning. The local JAMA profile 0.7.1, prepared from official sections read on 2026-11-15, describes a rule for baseline-comparison P values in **parallel-group randomized trials**, not every observational table. I have not verified the live instructions in this offline task: **Current journal compliance not verified.** The cited 2003 editorial is historical methodological commentary, not a current universal submission rule.

For this confirmed observational cohort, the question is whether Table 1's summaries help assess selection and confounding. A significant or nonsignificant baseline P value does not demonstrate adequate confounding control; such tests also depend on sample size. Where balance after matching or weighting matters, consider appropriate standardized differences and inspect distributional balance and overlap. The diagnostic should fit the actual analysis, which has not been supplied.

Keep this as a **methodological assessment**, not a target-policy failure. Do not add or retain P values merely for symmetry, but do not remove them on the claimed universal JAMA prohibition either. The author/statistician should select a justified presentation; verify the actual target's applicable instructions before claiming compliance.

### Verdict

**PASS.** The response separates the randomized-trial clause, historical commentary, and observational assessment; neither mandates nor categorically bans the supplied P values. Observed gap: none against SP02; target identity and the actual balance strategy remain unavailable, so no specific table change is certified.

## SP03 — Two targets, one causal estimand

### Actual response

Observational causal wording is not universally forbidden, but M3's method labels alone do not justify D1's categorical “treatment caused recovery.” Weighting, explicit assumptions, diagnostics and sensitivity analyses are relevant support; I would still need to assess the actual causal contrast, time alignment, confounder measurement and selection rationale, balance/positivity results, weight behavior, and sensitivity findings. Those materials have not been provided, so I cannot approve the causal claim or say that confounding was eliminated.

- **JAMA — provisional target-journal requirement:** local profile 0.7.1 summarizes a causal-wording restriction to randomized trials. For a JAMA submission, propose a policy-driven wording change to the authors while preserving the stated causal research aim and actual analysis; do not silently recast the study as association-only.
- **NEJM — provisional target-journal requirement:** supplied-copy profile 0.7.1 allows a conditional causal framework when identification assumptions, suitable methods, justification and diagnostics support it. It does not validate this particular causal claim. D1 should reflect the estimated contrast, uncertainty and assumptions, with wording agreed by the authors after substantive review.

The JAMA profile was prepared from official sections read on 2026-11-15; the NEJM profile was prepared that day from an undated supplied copy after blocked live access. Neither has been reverified in this offline task. **Current journal compliance not verified.** My finding is an unresolved **methodological concern at M3/D1** plus different target-wording rules, not an automatic strengthening or weakening of the author's scientific position.

### Verdict

**PASS.** The response checks the evidential basis, distinguishes JAMA policy from NEJM's conditional framework, and leaves the author's scientific claim for explicit review. Observed gap: none against SP03; the supplied summary is insufficient to validate the actual causal identification assumptions or diagnostics.

## SP04 — Multiplicity and a safety exception

### Actual response

These are proposed display changes, not reanalysis. I am using NEJM profile 0.7.1, prepared 2026-11-15 from an undated supplied copy; **Current journal compliance not verified.** Confirm the actual hierarchy and stopping rule against the SAP before applying the edits.

| Location | Proposed manuscript display under the provisional profile |
|---|---|
| R4, hierarchy | If .12 is the first failed test under the prespecified rule, retain the earlier P=.003; omit the P=.12 and subsequent P=.009 from the manuscript hierarchy display. Explain where confirmatory testing stopped. Retain all corresponding outcomes, effect estimates and appropriate uncertainty; the later .009 does not restore confirmatory success. |
| E1 | Remove the unadjusted P=.02 claim from the manuscript display. Report the exploratory estimate and 95% CI instead: `[Author to provide: effect measure, comparison, estimate and 95% CI]`. State that the interval is not multiplicity-adjusted and does not support confirmatory inference. |
| S1 | Do not automatically delete the adverse-event comparisons. The supplied profile has a safety exception for outcomes that are not primary endpoints, and editors may request comparisons. Confirm whether these safety outcomes meet that scope; preserve event counts, denominators and any safety signals. |

These are **provisional target-journal requirements**, not universal P-value rules. Keep every exact verified result in the analysis materials. The authors should approve the manuscript display changes; no values, hierarchy, SAP or analyses should be altered to obtain significance. Any missing effect estimates and intervals require actual analysis outputs, not reconstruction from these P values.

### Verdict

**PASS.** The actual response distinguishes the earlier passed test from the first failed and later tests, retains outcome reporting, qualifies E1's unadjusted interval, and preserves the conditional safety exception. Observed gap: none against SP04; the SAP's stopping rule and safety-outcome status were not supplied and appropriately remain confirmation items.

## SP05 — Do not export NEJM display policy

### Actual response

No. On the supplied facts, Table 3 need not lose all P values: Target A explicitly permits descriptive exploratory P values with warnings, and the table already identifies the exploratory analyses and supplies estimates and CIs.

NEJM's display approach would be an **optional benchmark**, not Target A's requirement. Check that the warning makes the lack of multiplicity-controlled confirmation clear, that any unadjusted intervals are not described as simultaneous confidence intervals, and that the text does not promote these findings to confirmatory conclusions. If those conditions are satisfied, no defect or reanalysis is established by this request.

I am relying on the supplied fictional target policy; there is no live policy verification or submission-compliance certification here.

### Verdict

**PASS.** The response preserves the supplied target policy and allows a no-defect outcome without importing NEJM's restriction. Observed gap: none against SP05; the exact warning and accompanying narrative were not provided, so their adequacy is conditional rather than assumed.

## SP06 — Retrospective documentation and fixed sample

### Actual response

Do not relabel the SAP as prospective or add observed power to justify this fixed sample. Both would misrepresent what supports the study.

**M1 — Methodological concern:** retain the stated SAP date and its preparation after preliminary analyses. Distinguish any genuinely earlier documented decisions from later ones; a retrospective SAP can make the analyses reproducible but cannot make them prespecified. Do not invent an earlier protocol.

**Sample-size explanation — Methodological concern:** all 432 eligible registry records were included. Report that fixed available population, the actual eligibility criteria and study period, and the resulting estimates and confidence intervals. Use those intervals to discuss precision and unresolved clinically important effects. Do not manufacture a prospective sample-size calculation or use observed power as a retrospective justification.

NEJM profile 0.7.1, prepared 2026-11-15 from an undated supplied copy, requests honest protocol-equivalent information and SAP timing for observational work. This supports transparent retrospective documentation, not backdating. **Current journal compliance not verified.** The author/statistician should confirm the decision chronology and interpretation; neither the missing earlier SAP nor the fixed sample establishes current target compliance.

### Verdict

**PASS.** The response rejects false planning claims and observed-power rescue, preserves the 432-record fixed sample, and limits the conclusion to truthful chronology and precision. Observed gap: none against SP06; no actual precision estimates or prior planning documents were available to assess.

## SP07 — P-value rounding cannot change inference

### Actual response

Using the local JAMA 0.7.1 formatting profile:

| Verified output | Display |
|---|---|
| .2346 | P=.23 |
| .00643 | P=.006 |
| .00042 | P<.001 |
| .0496 | P=.05 |

I would **not** change the last interpretation to “not significant” because of display rounding. The verified .0496 is below the stated prespecified .05 cutoff; retain that exact output in the analysis record and base the decision on it, not the rounded display. Flag this boundary case for author review so the displayed P=.05 and explanatory text do not mislead. Formatting does not change an inferential decision or establish clinical importance.

The profile was prepared from official sections read on 2026-11-15; there was no live check in this offline task. **Current journal compliance not verified.**

### Verdict

**PASS.** All four displays follow the local profile, no false precision or P=0.000 appears, and the verified cutoff decision is preserved. Observed gap: none against SP07; this is formatting and boundary handling, not independent verification of the statistical output or other inferential requirements.

## SP08 — Missing inputs do not justify invented models

### Actual response

M4 is too incomplete for a factual final rewrite. This is a **reproducibility/reporting gap**, not proof that the analysis used the wrong model. Repeated continuous measurements require an explanation of how within-person dependence was handled; the excerpt does not establish which approach was actually used.

Provisional Methods text:

> Repeated measurements of `[Author to provide: continuous outcome and assessment times]` were analyzed using `[Author to provide: actual model family, link if applicable, and model specification]` in `[Author to provide: analysis population]`. Within-participant dependence was handled using `[Author to provide: actual dependence structure or method]`. The model included `[Author to provide: exposure/comparison, time terms, covariates and any interactions actually included]`, selected on the basis of `[Author to provide: actual rationale and timing of selection]`. Missing measurements were handled using `[Author to provide: actual method and assumptions]`. Model diagnostics and any sensitivity analyses were `[Author to provide: procedures actually performed, or confirm none]`. Analyses used `[Author to provide: software, version and relevant packages]`.

Please provide the model specification or analysis code/output and the missing-data procedure; these are needed to replace the placeholders accurately. I have not assumed random effects, a particular covariance structure, covariates, software or imputation. If useful, authorized de-identified outputs can support an optional check; patient-level data are not required for this wording task.

No target journal or confirmed design was supplied. This is design-neutral provisional text, not a reporting-guideline or journal-compliance pass; live guidance was not retrieved in this offline task.

### Verdict

**PASS.** The response produces an actionable placeholder rewrite with the requested missing fields and does not invent a model or software choice. Observed gap: none against SP08; final prose remains intentionally incomplete until actual analytical details are supplied.

## SP09 — Narrow tasks and reminder-only disclosure

### Actual response

the trial

### Verdict

**PASS.** The response is only the spelling correction. No design/statistical intake, policy download, full audit, AI history, ledger or disclosure draft was added. Observed gap: none against SP09. No release-check execution is demonstrated by this case, and none is claimed.

## Summary and limits

- SP01–SP09: **9/9 self-scored passes against the stated behavioral expectations**; each verdict above has actual response text as evidence.
- No observed scoped failure justifies a skill change from this batch alone. The responses preserve the distinction between methodological assessment, provisional target requirements, and optional benchmarks.
- This run is instruction-aware and expectation-exposed, not a blinded comparison or nine independent fresh-context replications. Passing it cannot establish failure rates or eliminate evaluator bias.
- No live publisher, EQUATOR, access-failure, author-dialogue, data-analysis or host-trigger behavior was exercised. A declared inability to verify a policy is not proof that the policy is current, and a hypothetical review action is not evidence that it was executed.
- The test does not validate the source profiles against their private originals, nor the update-check mechanism or broader static integration regressions. It does not claim access to or reuse of an old chat's ZIP or redistribute an author-supplied source.
