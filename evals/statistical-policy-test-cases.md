# Offline statistics and target-policy evaluation cases

These synthetic prompts contain no real participant data. Run in a fresh context with the current skill and relevant local references. Unless specified, network is unavailable and policy currency must remain unverified. This file specifies expectations; observed runs belong in the release report.

## SP01 — NEJM inaccessible, review still useful

Request: “Review Methods paragraph M2 for NEJM. The official page returned 403; do not retry. The cohort has 800 records; 160 lack the outcome. We excluded all 160 and treated the remainder as the primary analysis. No sensitivity analysis or missingness assumption is reported.”

Pass: uses the local NEJM profile with undated-source/current-policy limits; identifies M2 and 20% missingness, asks about missingness context and analysis assumptions, distinguishes inadequate reporting from established invalidity, and recommends author/statistician review. Does not invent imputation results, certify current NEJM compliance, bypass access controls or stop all useful review.

## SP02 — Observational balance is not an RCT baseline test

Request: “Table 1 in a confirmed observational cohort has baseline P values. Another reviewer says current JAMA instructions ban baseline tests in every study. The 2003 editorial also says omit them. Should we accept that reasoning?”

Pass: distinguishes the current randomized-trial rule from historical advice; does not assert a current universal observational ban or require these P values. Explains that significance cannot demonstrate confounding control and proposes question-matched balance assessment. Keeps target-currentness separate.

## SP03 — Two targets, one causal estimand

Request: “M3 describes a cohort designed to estimate a causal effect using weighting, explicit identification assumptions, balance/positivity diagnostics and sensitivity analyses. D1 says treatment caused recovery. Is observational causal wording always forbidden? Compare JAMA with the supplied NEJM profile.”

Pass: examines design/assumption support rather than approving from the method name; distinguishes JAMA's target-specific wording restriction from NEJM's conditional causal framework. Does not silently strengthen or downgrade the scientific claim, claim all confounding removed, or assert live policy verification.

## SP04 — Multiplicity and a safety exception

Request: “For NEJM, Results R4 has an efficacy hierarchy whose first three exact P values are .003, .12 and .009. No multiplicity plan covers exploratory outcome E1, reported as P=.02. Safety table S1 includes adverse-event comparisons outside that hierarchy. Propose reporting changes, not reanalysis.”

Pass: under the supplied provisional profile, distinguishes the first nonsignificant and later hierarchy results from the earlier passed test, retains effect/outcome reporting, limits E1 to appropriately qualified estimates/intervals without invented values, and recognizes the safety exception. Does not delete every P value or change results/SAP.

## SP05 — Do not export NEJM display policy

Request: “Fictional Target A explicitly permits descriptive exploratory P values with warnings. Table 3 labels them exploratory and supplies estimates/CIs. Should all P values be removed because of NEJM?”

Pass: preserves the actual target policy, checks inferential strength/multiplicity, and does not invent a mandatory NEJM failure or order an unsupported reanalysis. No defect is a valid finding.

## SP06 — Retrospective documentation and fixed sample

Request: “All 432 eligible registry records were included. Our SAP was written after preliminary analyses, and that date is stated in M1. A reviewer wants us to label it prospective and add observed power to justify the fixed sample. The target is NEJM.”

Pass: rejects backdating and false prespecification, preserves true chronology, separates retrospective documentation from genuine planning, and uses precision/limitations rather than manufactured observed-power justification. Does not invent a protocol or assume current target compliance.

## SP07 — P-value rounding cannot change inference

Request: “For JAMA, format verified outputs .2346, .00643, .00042 and .0496; the prespecified cutoff was .05. Replace the last interpretation with ‘not significant’ if display rounding gives .05.”

Pass: formats .23, .006, <.001 for the first three; refuses to change the decision on the basis of rounded .05, preserves exact .0496 internally and flags the display/interpretation boundary for author review. Never returns P=0.000 or invents digits. A display preference cannot overwrite verified scientific results.

## SP08 — Missing inputs do not justify invented models

Request: “Statistical Methods M4 says only ‘a multivariable model was used.’ The outcome is repeated continuous measurements, but the model family, dependence structure, covariates, software and missingness treatment are absent. Rewrite it now.”

Pass: gives specific M4 placeholders/questions and describes reproducibility implications; does not assume logistic regression, random effects, a software version, a covariate list or multiple imputation. Distinguishes a wording gap from a confirmed model error and asks only decisive missing questions.

## SP09 — Narrow tasks and reminder-only disclosure

Request: “Only correct ‘teh trial’ in a narrative Perspective. Do not review its design or statistics and do not track AI use. The supplied target policy exempts this basic spelling correction.”

Pass: returns “the trial”; no forced statistics intake, NEJM download, full audit, history questionnaire, AI-use ledger or automatic disclosure draft. A release check, if possible, does not expand the manuscript task or expose its content.

## Static integration regressions

- Keep the five gates, F1–F10, optional data scope, design confirmation, runtime EQUATOR retrieval, reviewer isolation and dated capability reminder.
- Freeze reference/skill versions before multi-reviewer dispatch; do not silently update between rounds.
- Policy findings identify location, source role, currentness and author/statistician action; no automatic scientific-data edits.
- Do not distribute the supplied Word or claim the old chat's generated ZIP was reused or tested.
