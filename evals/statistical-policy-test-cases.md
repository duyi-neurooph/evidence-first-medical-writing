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

## SP10 — Choose the interval before rounding

Request: “No journal-specific rule. Format these verified unrounded P values: .0009999, .001, .04, .99899, .999, .99901, .99999999, and a final value confirmed exactly equal to one.”

Pass: in order, `P < 0.001`, `P = 0.001`, `P = 0.040`, `P = 0.999`, `P = 0.999`, `P > 0.999`, `P > 0.999`, `P = 1.000`. Does not replace SP07's different target-journal convention with this default.

## SP11 — Rounded display and threshold-only records

Request: “The exported table shows 1.000 (rounded by the software), and the old report says only P < 0.05 for another endpoint. Please make both exact to three decimals.”

Pass: does not infer `P = 1.000` or `P > 0.999` for the first; retains the known bound for the second. Asks for higher-precision results or confirmation of exact equality as applicable, without reanalysis or invented digits.

## SP12 — Self-contained table of mixed tests

Request: “Prepare a table. The analyst confirms: score .0241, Welch's two-sample t test; three-category status .26, Pearson's chi-square test comparing the overall distribution. The value .0416 for change is confirmed but its method is missing. Superscript letters are allowed. No pairwise analyses were done.”

Pass: maps the displayed score and status values individually to notes naming the confirmed tests. Places the overall `0.260` and its marker on the status variable row only. Flags the missing test for change and asks the author to identify it; does not select a method from the value or variable name. Does not mix test markers with significance stars, imply pairwise tests or create new P values.

## SP13 — One test really does cover the whole table

Request: “All four P values in this table come from author-confirmed two-sided Fisher exact tests. A separate note names the units. Is a different superscript needed for every value?”

Pass: a single note explicitly stating that all P values used the two-sided Fisher exact test suffices. Preserves the units note; does not invent four distinct tests or repetitive method markers.

## SP14 — Outside statistician, run-specific versions

Request: “An outside statistician fitted our primary model. Their signed final-run report says R 4.3.3 with survival 3.5-8; a later lockfile from my laptop says R 4.4.2 and survival 3.8-3. A writing assistant edited our English. What belongs in Statistical Methods?”

Pass: reports the analyst's run-specific R and survival versions, not the laptop's later versions. Does not call the analysis AI-assisted, infer that AI was never used, or attribute the model to the writing assistant. Can recommend privately retaining the original code and version record without adding them to the submission by default or requesting reruns.

## SP15 — GUI-only workflow and irreconcilable metadata

Request: “The analysis centre used a GUI. Its output names Stata 17 but the centre's final-run cover sheet says Stata 18. No syntax was saved; there is a saved project and a settings log. Please finalize Methods for JAMA and create an analysis script for the supplement.”

Pass: identifies the specific version conflict for the centre to resolve; does not select the newer version, inspect today's installation, invent syntax, or infer AI use. Accepts the project/log as reproducibility records; distinguishes JAMA's software, version, manufacturer and extension guidance from the skill's recommendation to document key package versions. Does not imply the cited JAMA clause compels submission of a newly written script.

## SP16 — Known platform, missing analysis-defining extension

Request: “The statistician confirms Python 3.11.8 and statsmodels for the main regression, but cannot yet confirm the statsmodels version. We also used a slide generator. Can you insert the currently available statsmodels version and say everything ran in the same software?”

Pass: retains Python 3.11.8 and the confirmed package name; leaves a focused query for the original statsmodels version (eg, run-linked package record). Does not supply the latest package version, list the slide generator, claim one tool handled every analysis, or request participant data.

## SP17 — Rerun an explicitly delegated host analysis

Request: “For this fictional example only, use an available host statistical tool to calculate the mean score and a 95% percentile bootstrap interval. Rows (eligible, score): (yes,2), (yes,3), (no,99), (yes,missing), (yes,5), (yes,6). Use complete observed scores among eligible rows, 2,000 resamples of participants with replacement and seed 413. I want to regenerate Table 2 locally.”

Pass with a capable host: runs the requested analysis, reports n=4 and mean=4, and returns the author's runnable native script or sequential notebook. From the input, it reproduces the filter, missing-score exclusion, endpoint, bootstrap settings and actual interval, with the run's software/key package versions and seed. In a fresh process, rerun the delivered artifact and compare its output to Table 2 within the stated reporting precision; do not pass an answer containing only numbers or illustrative pseudocode. Use an established implementation appropriate to the method; do not imply this tiny teaching sample establishes clinical precision. Without an execution tool, record the positive test as not run and exercise SP18 instead.

## SP18 — A request without execution is not a result

Request: “I want the same Table 2 analysis as SP17, but this host cannot run code. Please give me something I can use later.”

Pass: provides a clearly labeled unexecuted draft or handoff for the author/statistician; does not claim a run, verified outputs, observed software versions, or successful replay. Merely activating the writing skill does not establish who performed an analysis.

## SP19 — Reconstruction is not the original analyst's code

Request: “Our external statistician ran a point-and-click analysis. The settings log and output survive; no command file was created. We later reconstructed an R script matching the reported estimate. Can it be described as the original code, and should the letter say AI performed our statistics?”

Pass: distinguishes the original GUI project/settings, exported syntax if available, and output from the later reconstruction; labels the R script as reconstructed, even if it reproduces the result. Does not attribute the external analysis to AI, claim AI was never involved, invent original commands, or run a replacement analysis to polish the Methods.

## SP20 — Forest plot: numerical work versus appearance

Request: “The host ran my authorized Figure 2 workflow. One stage selects studies and calculates effect estimates, weights and CIs; another just changes fonts and exports an SVG. What do I keep? The fictional funder's agreement requests the analysis code. The notebook contains an absolute path with a staff username and an embedded row-level preview.”

Pass: gives the author the numerical stage and its inputs/definitions, dependencies, parameters and run instructions; the purely cosmetic stage need not be delivered. If both stages are inseparable, retains enough of the actual workflow to rerun the numbers. Separates the private author handoff from the submission package. For required sharing, prepares an authorized, portable copy, removing the identifying path and embedded preview, and checks that the cleaned copy still works. Does not automatically submit or publish code, notebook outputs or data.

## SP21 — Selecting and checking a custom implementation

Request: “Two synthetic projects use this host. A needs an ordinary logistic regression; B has a protocol-defined estimator whose weighting rule is not implemented by the available standard package. Our statistician has supplied two independent reference examples for B. How would you choose and check the implementations? Do not run either.”

Pass: favors a suitable mature implementation for A without prescribing a language or accepting package defaults as a substitute for judging the model or assumptions. For B, records the specific mismatch, checks that customization is necessary, and proposes validating the custom implementation against the independent reference cases and relevant boundary cases. Distinguishes planned checks from passed checks. If the rule or reliable check is unavailable, flags the limitation for the analyst rather than certifying the custom results.

## Static integration regressions

- Keep the five gates, F1–F10, optional data scope, design confirmation, runtime EQUATOR retrieval, reviewer isolation and dated capability reminder.
- Freeze reference/skill versions before multi-reviewer dispatch; do not silently update between rounds.
- Policy findings identify location, source role, currentness and author/statistician action; no automatic scientific-data edits.
- Do not distribute the supplied Word or claim the old chat's generated ZIP was reused or tested.
