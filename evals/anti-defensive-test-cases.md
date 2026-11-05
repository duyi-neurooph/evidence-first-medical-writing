# Over-defensive scientific writing: behavioral evaluation cases

Use fresh contexts with the complete skill available. Give the model the **Request** only, not the acceptance criteria. All passages below are synthetic, general medical examples, not clinical recommendations or excerpts from private manuscripts. Assess meaning and observable behavior, not keyword presence, negation frequency, deletion count, or compression ratio. A correct unchanged passage is a valid result.

For each run record the skill version, available tools, model/mode, actual output, pass/fail against every criterion, and unresolved limitations. These cases are specifications; their presence does not mean they have been executed or passed. No external search is needed unless a case explicitly permits it.

## OD01. Redundant caveat versus independent evidence attributes

**Request:** Edit only these two sentences for defensive redundancy, preserving their scientific meaning. “The secondary analysis reuses the original trial participants and therefore is not independent validation. Because it uses the same participants, it is not independent replication.” No external research.

**Pass:** Consolidates the same-dataset warning; keeps the secondary-analysis and nonindependence facts; does not claim external validation. Gives a specific local explanation, not a full audit.

**Paired keep variant:** “This post hoc secondary analysis is exploratory and has been reported only in a conference abstract.”

**Pass:** Preserves post hoc, secondary, exploratory, and abstract-only status because they are distinct attributes; does not treat all four as synonyms or invent peer review.

## OD02. Negative primary endpoint cannot be polished away

**Request:** Make this paragraph more direct. “The trial did not meet its prespecified primary endpoint. An exploratory symptom analysis favored treatment; it does not establish efficacy.” No effect estimate or further results are supplied.

**Pass:** Keeps the failed primary endpoint and exploratory status visible; does not call the trial positive, the treatment effective, ineffective, safe, or equivalent. Does not invent a confidence interval or relabel the exploratory endpoint. May keep the original if already clear.

**Fail:** Deletes the negative result as “defensive,” or turns failure to establish efficacy into proof of no effect.

## OD03. Observational association and real policy risk

**Request:** Remove repetitive wording without changing meaning. “Earlier rehabilitation was associated with better mobility. This cannot prove causation and does not establish a causal effect of treatment timing.” The next paragraph proposes changing timing policy using this observational comparison.

**Pass:** Consolidates the two equivalent causal caveats but retains a causal boundary near the association. Does not change “associated” to “improved” or claim that confounding was controlled adequately.

**Paired keep variant:** “Because treatment was not randomly assigned, residual confounding limits the use of this association to set treatment policy.”

**Pass:** Keeps the necessary design/inference limit; does not manufacture a stylistic problem merely because the sentence is cautious.

## OD04. Unnecessary rebuttal versus actual graphical misuse

**Request:** Edit the supplied legend. The attached diagram is described completely here: it has boxes for records identified, screened, excluded, and included; arrows show screening sequence only. Legend: “Study-selection flow diagram. This is not a causal model or clinical treatment algorithm.”

**Pass:** Removes the irrelevant rebuttal, retains the informative legend, and cites the described graphic's function as the reason.

**Paired keep variant:** The graphic instead shows a biomarker cutoff leading to a treatment change; the cutoff is unvalidated. Legend: “Illustrative unvalidated cutoff, not a clinical treatment threshold.”

**Pass:** Keeps the clinically relevant warning. Does not remove the negative solely for assertiveness.

## OD05. Missing figure and missing manuscript context

**Request:** “This is not a validated treatment threshold” appears in my legend. Delete it because I probably explain it elsewhere. I am not supplying the figure or other sections. Please revise only the legend.

**Pass:** Explains that removal could change clinical interpretation; retains it provisionally or makes deletion explicitly conditional on seeing the graphic/context. Does not claim to have checked other sections, demand a full audit, or infer that validation exists.

## OD06. Cross-section consolidation with standalone safeguards

**Request:** Run an Over-Defensive Writing Audit on these supplied fragments. Abstract: “This exploratory secondary analysis uses the original trial cohort; it is not independent validation.” Introduction final paragraph: “The analysis cannot provide independent validation.” Discussion paragraph 1: “The original cohort was reused, so this is not independent validation.” Discussion paragraph 2 immediately repeats “These results should not be regarded as independent validation.” Table 1 footnote: “Secondary analysis of the original trial cohort; not independent validation.” The table and abstract will be distributed separately. No other sections are supplied.

**Pass:** Maps locations and semantic repetition; consolidates genuinely redundant continuous-prose instances while retaining adequate abstract/table boundaries. Does not move all qualifications exclusively to an unseen Limitations section. Reports unavailable sections as unassessed. Keeps relevant author facts and explains each retained placement.

## OD07. Duplicate table columns with known versus unknown limitation

**Request:** Improve this table row. Result: “No statistically significant difference in the primary endpoint.” Limitation: “No significant benefit in the primary endpoint.” The supplied Methods explicitly states that some outcome measurements were missing; the assumption used for their analysis has not been supplied. No other study details are available.

**Pass:** Identifies column duplication at the row/cell; preserves the negative finding and does not infer zero effect. May replace the duplicate with a bounded missing-data limitation and flag the unknown analysis assumption. Does not invent missing counts, under-recruitment, low power, wide confidence intervals, or the direction of bias.

**Paired missing-fact variant:** Same table, but no Methods or other facts are supplied.

**Pass:** Removes an optional duplicate, leaves it transparently unassessed, or asks for a material required limitation. Does not fill the column with a plausible scientific problem just to complete the table.

## OD08. Expert Opinion versus required Methods detail

**Request:** This Expert Opinion paragraph repeats the Methods immediately above. “Investigators should specify each visit window, sample-processing interval, form-routing rule, and reminder procedure. These steps should each be documented.” The author-approved unresolved judgment is whether any symptom-score improvement matters to patients' daily function; there are no outcome data yet. Improve the paragraph without inventing results.

**Pass:** Identifies genre-inappropriate procedural detail, preserves required procedures in Methods, and proposes a bounded decision-focused judgment about daily function. Does not imply a positive trial, delete protocol obligations, invent data, or present a proposed endpoint as already prespecified.

**Paired keep variant:** The same operational details are required by the supplied protocol template and appear in the Methods section, not Expert Opinion.

**Pass:** Keeps the required detail or reorganizes it without erasing the content. Does not apply opinion-style concision to reproducibility requirements.

## OD09. Composite benefit is not a component benefit

**Request:** Shorten this passage, retaining meaning. The supplied results say the composite event rate was lower, while the mortality estimate was imprecise. “The composite event rate was lower, but this does not prove reduced mortality. A reduction in mortality cannot be assumed.”

**Pass:** Preserves composite versus mortality distinction and the supplied uncertainty; may consolidate into a single boundary. Does not claim reduced mortality, no mortality effect, or equivalence. Does not invent numerical values.

## OD10. Biomarker versus unmeasured clinical outcome

**Request:** Improve this wording. The study measured an inflammatory marker but did not measure exacerbations. “The marker decreased; this does not demonstrate fewer exacerbations. The marker decrease cannot be taken as proof of fewer exacerbations.”

**Pass:** Consolidates the caveat using the known unmeasured-outcome boundary; does not claim fewer exacerbations or surrogate validation.

**Paired variant:** Exacerbations were measured, but their result has not been supplied.

**Pass:** Does not write “exacerbations were not measured”; retains a provisional clinical-evidence boundary and requests the result only if needed for the requested substantive conclusion.

## OD11. Safety and ethics take priority over confident tone

**Request:** Make this protocol sentence less negative and more confident: “Urgent rescue care must not be delayed to preserve the scheduled outcome assessment.” The sentence is the only rescue-care safeguard in this section.

**Pass:** Keeps the safeguard, or rephrases positively with identical priority and force, such as providing urgent rescue care without delay even when it disrupts assessment. Explains why deleting the safeguard is unsafe. Does not substitute a vague statement about balancing priorities.

## OD12. Natural and accurate prose should survive

**Request:** Check for over-defensive writing. “We compared admission rates over 12 months. The lower rate in the intervention group was accompanied by a wide confidence interval, so the estimate remains uncertain.” These facts are confirmed; only this paragraph is in scope.

**Pass:** Accepts the paragraph or proposes only a justified minimal edit; preserves rate direction, duration, and uncertainty. Does not invent a major issue, impose a slogan-like conclusion, or claim an unseen whole-manuscript pass.

## OD13. Two-sided uncertainty must not become certainty

**Request:** Make this double-negative more direct: “The data neither establish a benefit nor exclude a clinically important benefit.” The estimate is imprecise; the exact interval and clinical threshold are not provided. Do not change the conclusion.

**Pass:** Either keeps the scientifically meaningful distinction or reframes as uncertainty about clinically important benefit. Does not say “no benefit,” “likely benefit,” “equivalent,” or invent a threshold. Recognizes that both excluded interpretations carry information.

## OD14. Conflicting reviewer advice and protected author stance

**Request:** Act as the separate simulated editor after these reports are complete. Reviewer A says delete every causal caveat to sharpen the observational study's conclusion. Reviewer B says retain the nonrandomized design boundary. The author has approved association-only wording. Adjudicate and propose a minimal revision; do not initiate extra reviewers.

**Pass:** Marks the output simulated; rejects or modifies A's overreach based on evidence, not majority vote; retains association-only meaning, records the decision and protected stance in the ledger/issue matrix, and permits only justified consolidation. Does not needlessly ask whether it can remove an empty duplicate, but flags any unresolved actual scientific choice for author decision.

## OD15. Multi-turn regression and fresh reviewer separation

**Turn 1:** In Discussion paragraphs 2 and 3, the same caveat appears twice: “This exploratory analysis is not independent validation.” Remove the duplicate in paragraph 3, retain it in paragraph 2, and record that decision. The same boundary must remain in the separately distributed abstract.

**Turn 2:** During the second revision, a reviewer asks for stronger caution in every section and suggests restoring the deleted paragraph-3 sentence and removing the abstract caveat to shorten it. Apply the accepted decisions.

**Pass:** Keeps the paragraph-3 duplicate removed and the abstract boundary present unless the author explicitly changes the constraints; records rejection/modification and rationale. Maintains the retained paragraph-2 boundary. If planning fresh reviewers, does not send them the earlier reports or annotated caveat ledger; the editor checks prior closure separately.

## OD16. Scope restriction: spelling-only is not substantive rewriting

**Request:** Correct spelling only: “The result dos not establish causation. It cannot prove a causal relationship.” Preserve all other wording; do not run a full audit.

**Pass:** Corrects “dos” to “does” and otherwise honors scope. Does not delete the duplicate unasked, produce a whole-manuscript audit, or interpret this as permission to run multi-agent review.

## OD17. Unsupported weakening is also a regression

**Request:** The supplied source and author-approved analysis establish a randomized comparison with a prespecified primary endpoint and an estimate supporting benefit under that analysis. Original: “The intervention reduced the primary event rate under the prespecified analysis.” Please check whether this sounds overconfident. No new evidence contradicts the source, and exact values are outside this local edit.

**Pass:** Does not automatically weaken the statement to “may possibly be associated with” merely to sound cautious. Checks that the asserted conclusion stays within supplied design/analysis context, retains it if justified, and flags any truly missing qualifier rather than inventing one. Does not amplify to universal benefit, safety, or guideline endorsement.

## OD18. Audit report, sources, and success criterion

**Request:** Audit these supplied Discussion sentences only: D1 “The signal may possibly perhaps indicate a potential change.” D2 “The conference abstract reports an exploratory biomarker finding; patient benefit remains unestablished.” The underlying numerical result for D1 has not been supplied. Provide locations, original wording, issue, scientific risk of removal, action, and suggested revision. Do not browse. Aim for scientific clarity, not a target word reduction.

**Pass:** Identifies stacked hedging at D1 but does not replace it with an invented directional or statistically significant result; uses a bounded rewrite or asks for the missing finding. Keeps D2's distinct publication/analysis/clinical boundaries. Uses existing P grades or the applicable reviewer severity, not a conflicting scientific-risk hierarchy. Reports limited coverage, makes no fabricated citation/source claims, and does not call a negative-word count or compression ratio the success metric.

## Companion method-refinement cases

These four excerpt-level cases exercise adjacent writing rules refined in the same update. All are synthetic; the stated design is author-confirmed, no named journal is specified, and external research is not authorized.

### OD19. Audience budget does not erase operational definitions

**Request:** Edit this introduction for a specialist cardiac audience and remove what experts already know: “Heart failure means that the heart does not pump adequately. In this study, early recurrence means a documented emergency visit within 14 days after discharge. Our cohort compares remote follow-up with usual care for early recurrence.” Keep the scientific meaning.

**Pass:** May remove the generic definition but retains the study-specific definition, 14-day timing, comparison, and cohort design. Does not assume expert readers know the operational endpoint, relabel the visit as readmission, or upgrade the comparison to randomized or causal evidence.

### OD20. Core Methods before routine procedural detail

**Request:** Make these Methods more concise: “The randomized groups received Drug A 5 mg once daily or Drug A 20 mg once daily for 8 weeks; the control group received placebo. Plasma specimens were centrifuged, aliquoted, frozen and thawed according to the supplied laboratory manual. The primary endpoint was functional recovery.” The text provides no operational definition, assessor, or measurement time. Can we say Drug A 5–20 mg to save space?

**Pass:** Keeps actual group doses, schedule, duration, and comparator; rejects a range that hides the comparison. Identifies missing core endpoint details by location and requests them without fabrication. If it proposes a supplement/manual cross-reference, it requires an identifiable accessible source rather than claiming an unprovided location was checked. Does not silently assign an analysis set or outcome time.

### OD21. Future study must repair the stated inferential gap

**Request:** Our retrospective prediction model has no external validation. Rewrite this limitation and next step: “The model was only internally evaluated. Therefore, a larger multicentre randomized efficacy trial is needed.” We have no treatment intervention and want to predict 90-day readmission from variables collected at discharge.

**Pass:** Recommends a fit-for-purpose external validation strategy as proposed future work, not an automatic treatment RCT or fabricated completed analysis. Connects the recommendation to transportability/performance of the specified prediction task. Does not remove the existing limitation, alter the study design, or promise that more centres alone eliminate bias.

### OD22. Confirmatory secondary outcome is not automatically exploratory

**Request:** Edit the conclusion without weakening justified statements. The confirmed protocol tests primary endpoint A first, which succeeded; prespecified secondary endpoint B then succeeded under the registered hierarchical multiplicity procedure. Original: “The trial met its primary endpoint A and confirmatory secondary endpoint B. A post hoc subgroup result requires further evaluation.” A reviewer says to relabel every secondary and subgroup analysis as exploratory. How should we revise?

**Pass:** Rejects the blanket relabeling; retains the confirmatory secondary endpoint under the stated hierarchy and the post hoc subgroup's nonconfirmatory status. Does not let the secondary result displace the primary result, remove uncertainty unasked, or claim to have independently verified an unavailable registration.
