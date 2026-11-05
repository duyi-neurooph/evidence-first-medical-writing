# Over-Defensive Scientific Writing: Detection and Revision

## Purpose and scope

Apply **evidence first, not caution first**: state the observation, interpret it within its evidence boundary, and explain the implication. Avoid chains of disclaimers that add no scientific information. This is not permission to sound more confident, remove uncertainty, or weaken a supported conclusion.

Over-defensive writing repeatedly tells readers what a finding cannot establish, rebuts an interpretation nobody has made, or buries a useful judgment beneath unnecessary qualifications. A negative sentence, hedge, limitation, or cautious author position is not inherently a defect. Accurate, natural writing may need no change.

Use this module with [language-and-logic.md](language-and-logic.md) and [architecture-and-evidence.md](architecture-and-evidence.md) for substantive drafting and revision. In whole-manuscript review, simulated peer review, or final manuscript audit, run a named **Over-Defensive Writing Audit** over the supplied material. It complements the **AI-Like Residue Audit** in [independent-multi-reviewer-workflow.md](independent-multi-reviewer-workflow.md); neither audit is a word blacklist or an AI-authorship detector.

For audit-only requests, return findings and suggested revisions; do not silently modify source files. Apply revisions when requested, retaining original files. Scope and scientific fidelity take priority over a more assertive tone.

**Contents:** protected scientific content; eight detection categories; six-step decision procedure; drafting/local/full-review application; synthetic examples; audit output; decision persistence and non-regression.

## Protected scientific content

Before cutting or reframing, preserve the following wherever readers need them to interpret the claim:

- Actual study design, allocation mechanism, population, comparator, dose, timing, and outcome definitions.
- Negative primary results, effect estimates, uncertainty, and the distinction between nonsignificance and equivalence, safety, or absence of effect.
- Association versus causation; direct versus indirect evidence; surrogate or biomarker change versus patient benefit.
- Intention-to-treat versus per-protocol analyses; primary, secondary, exploratory, post hoc, and prespecified status.
- Secondary analysis of the same dataset versus independent replication; source and publication status, including author-provided unpublished information.
- Material applicability limits, adverse events, participant safety, ethical constraints, regulatory disclosures, and conflicts of interest.
- Author-confirmed scientific positions, terminology, and unresolved uncertainties. If a protected position conflicts with evidence, flag it for author decision rather than silently changing or endorsing it.

Do not change “was associated with better recovery” to “improved recovery” without causal support. Do not change “did not establish efficacy” to “was ineffective.” Compression must neither strengthen nor weaken scientific meaning. A caveat needed to prevent a misleading abstract, table, highlight, or legend cannot be relocated solely to a distant Limitations section.

## Eight detection categories

| Category | Inspect | Decision boundary |
|---|---|---|
| A. Repetitive caveat | Several differently worded negatives qualify the same proposition without adding a new constraint. | Compare meaning, not repeated words. Keep separate limitations when they constrain different inferences. |
| B. Unnecessary rebuttal | A sentence refutes a claim the manuscript, evidence, or plausible reader interpretation does not make. | Delete only when there is no concrete misconception to prevent. Keep correction of an actual exaggerated claim. |
| C. Redundant negative framing | “Not X, but not Y,” double negatives, or balanced exclusions obscure the positive scientific statement. | Reframe only if the new wording preserves both supported and unresolved interpretations; do not invent a false dichotomy. |
| D. Excessive hedging | Stacked “possibly,” “may,” “potentially,” or vague uncertainty markers repeat one uncertainty. | Exploratory, post hoc, secondary, and non-peer-reviewed describe different attributes; do not collapse them as redundant hedges. |
| E. Genre-inappropriate procedural detail | An Expert Opinion, Critical Perspective, narrative review, or Discussion substitutes a procedural inventory for a scientific judgment. | Move necessary detail to its proper location; do not erase reproducibility, protocol, ethics, or reporting requirements. |
| F. Table-column duplication | Result, limitation, and implication columns restate the same negative finding, or a table repeats prose without comparative value. | Result = observation; limitation = constraint on inference; implication = consequence for a decision. Do not invent a limitation to fill a cell. |
| G. Cross-section repetition | The same warning recurs in Abstract, Highlights, Introduction, Discussion, Limitations, Conclusion, Expert Opinion, tables, or supplements. | Assign each occurrence a job. Necessary repetition in independently read units is not a defect. |
| H. Figure-legend disclaimers | Generic “not causal,” “not validated,” or “not a treatment threshold” statements are attached regardless of what the graphic implies. | Keep qualifications needed for schematic arrows, unvalidated cutoffs, safety, clinical decisions, or misleading visual certainty. |

For each candidate, identify the proposition, the specific misconception prevented, and any information lost on deletion. If none is defective, report no substantive over-defensive-writing concern; do not manufacture a problem to complete an audit.

## Six-step decision procedure

1. **Evidence:** Identify the exact scientific proposition, its supporting material, and the interpretation the qualification prevents. Record what is observed, what is inferred, and what remains unknown. Missing evidence is not evidence of redundancy.
2. **Value:** Ask whether removing the wording would misstate design, analysis, effect, uncertainty, applicability, safety, or author position. If yes, keep that boundary, even if its wording can be improved.
3. **Repetition:** Find semantic duplicates within the available scope. Record their locations and functions. Distinguish continuous prose from standalone units. Do not claim to have checked absent sections, figures, sources, or supplements.
4. **Reframe:** Try the smallest edit using an explicit observation, bounded interpretation, or unresolved decision. Choose **Keep**, **Consolidate**, **Reframe**, **Delete**, or **Author decision**. Consolidation must identify both removed and retained locations and preserve the relevant citations.
5. **Author stance:** Compare the original and proposed meanings, not just their length. Reject causal inflation, unwarranted certainty, unwarranted weakening, changed endpoint hierarchy, or lost safety context. Ask the author when an actual scientific choice is required; do not ask merely to remove an empty intensifier.
6. **Genre:** Check section purpose, article type, supplied journal instructions, and applicable reporting requirements. Opinion writing should advance judgment; Methods and protocols still need operational detail. Follow current official guidance through the existing guideline workflow when needed, not personal stylistic preferences.

When only a fragment is available, make a local judgment. If consolidation depends on an unseen passage, state that dependency and retain the necessary qualification provisionally. Use `[Author to provide / 待作者补充: specific content / 具体内容]` for a material missing fact; do not fill it with a plausible limitation, result, or reference.

## Apply at the requested scale

### Substantive drafting

Define each paragraph's scientific job before writing it. Use **Evidence → Interpretation → Implication** as a reasoning sequence, not a mandatory three-sentence template. Attach evidence status and the necessary limit near the claim they qualify. Do not append “cannot establish” to every finding or end every section by reciting the same limitations.

When proposing future work, name the unresolved decision and, where supported or explicitly proposed, the population, intervention/exposure, comparator, timing, endpoint, and design needed to resolve it. Distinguish a suggested research design from facts about an existing study. Do not replace a concrete result with a generic development slogan.

### Local rewriting

Check scientific fidelity, readability, and defensive redundancy within the supplied sentence or paragraph. Prefer minimal changes and explicitly allow **Keep**. When revising a scientific qualification, add a brief change note identifying the retained boundary and why the removed wording was redundant, unless the user requests revised text only. Do not force an audit table on a short rewrite. Do not turn a local request into a full-manuscript audit, or claim cross-section redundancy without seeing those sections. Spelling-only, formatting-only, or literal-translation tasks do not authorize substantive revision or a full audit; flag a material scientific concern separately if necessary.

### Whole-manuscript review and final audit

Inspect Abstract, Highlights, Introduction, Discussion, Limitations, Conclusion, Expert Opinion, main/supplementary tables, and figure legends when supplied; inspect other sections when relevant. Declare coverage and unavailable items. Map repeated propositions across locations rather than merely scanning for `not`, `but`, or `however`.

Prefer one substantive explanation in continuous prose, with brief claim-specific boundaries elsewhere when needed. Abstracts, highlights, tables, legends, and separately distributed supplements must remain interpretable without the main text. Different wording is not automatically new information; identical wording is not automatically unnecessary.

For tables, ask whether each column adds a distinct kind of information and whether the row remains self-contained. If no additional limitation is established, remove an optional duplicate, use a transparent “not assessed from supplied material,” or flag a missing required entry. Do not infer recruitment shortfall, bias, poor power, or imprecision from a nonsignificant result alone. For legends, inspect the actual graphic when available; if it is unavailable, make any proposed disclaimer removal conditional on checking the image.

### Independent review and editorial adjudication

Assign argument force and redundant caveats to a journal editor-style reviewer or an equivalent editorial remit. Assign preserved evidence strength to an evidence/methodology reviewer. These are complementary remits, not instructions to agree or mandatory additional agents. Follow existing frozen-package and reviewer-independence rules; do not give reviewers another reviewer's caveat map or conclusions.

Only the separate editor adjudicates after independent reports arrive. A language reviewer cannot unilaterally remove a methodological or safety boundary. Preserve scientific fidelity when resolving conflict; unresolved changes in scientific position require **Author decision**. Retain original reports and record the rationale in the Issue Matrix and Decision Ledger. Fresh second-round reviewers do not receive earlier reports or the annotated redundancy map; the editor separately checks issue closure and regression.

## Original synthetic examples

These examples illustrate editing decisions, not clinical recommendations or claims about real studies. The stated context is part of each example; do not infer it for a user's manuscript.

### 1. Repeated independent-validation warning — consolidate

**Context:** Two sentences discuss a secondary analysis of the same blood-pressure trial dataset; no independent dataset is reported.

**Before:** “The secondary analysis used the original trial dataset and provides no independent validation. It is not an independent replication because the participants are the same.”

**After:** “The secondary analysis reused the original trial dataset; it therefore provides no independent validation.”

**Decision:** Consolidate. Retain dataset dependence; do not relabel a secondary analysis as replication.

### 2. Population-specific safety — keep the boundary, remove the echo

**Before:** “Pregnant participants were excluded, so these safety findings do not establish safety during pregnancy. Safety in pregnancy cannot be inferred from this study.”

**After:** “Pregnant participants were excluded, so these findings do not establish safety during pregnancy.”

**Decision:** Consolidate the duplicate, not the clinically meaningful applicability limit. A standalone safety table may still need this qualification.

### 3. Composite and component outcomes — reframe precisely

**Context:** A cardiovascular trial reports a lower composite event rate; the mortality estimate remains imprecise.

**Before:** “The composite outcome was lower, but this is not proof of a mortality reduction. It should not be assumed that mortality was reduced.”

**After:** “The composite event rate was lower; the imprecise mortality estimate does not establish a mortality reduction.”

**Decision:** Reframe with the supplied reason. Never infer a component benefit from a composite or invent an imprecise estimate when none is supplied.

### 4. Observational timing — preserve causal meaning

**Before:** “Earlier rehabilitation was associated with better mobility. This association cannot establish causation and does not prove that earlier rehabilitation caused the improvement.”

**After:** “Earlier rehabilitation was associated with better mobility; the observational comparison does not establish a causal effect of treatment timing.”

**Decision:** Consolidate. “Earlier rehabilitation improved mobility” is not an acceptable substitute.

### 5. Biomarker and clinical outcome — preserve the distinction

**Context:** A respiratory study measures an inflammatory marker but not exacerbations.

**Before:** “The marker concentration decreased, but this does not establish fewer exacerbations. A decrease in the marker should not be equated with fewer exacerbations.”

**After:** “The marker concentration decreased; effects on exacerbations were not measured.”

**Decision:** Reframe using a known measurement boundary, not a generic disclaimer. If exacerbations were measured, this revision would be wrong.

### 6. Negative primary endpoint and exploratory signal — keep

**Original:** “The trial did not meet its prespecified primary endpoint. The exploratory symptom-score finding is hypothesis-generating.”

**Decision:** Keep when both statements accurately describe the trial. They serve different purposes; removing either can misrepresent the analysis hierarchy. Do not rewrite as either “the treatment works” or “the treatment has no effect.”

### 7. Actual causal restriction — keep

**Original:** “The association between treatment choice and recovery may reflect residual confounding because treatment was not randomly assigned.”

**Decision:** Keep when the discussion considers changing treatment policy on this evidence. The qualification addresses a real inference risk, not defensive habit.

### 8. Table duplication — use only a documented limitation

**Before:** Result: “No statistically significant group difference in the primary endpoint.” Limitation: “No significant benefit in the primary endpoint.”

**After, if the source explicitly documents attrition:** Retain the result; replace the duplicated limitation with “Outcome data were missing for some participants; the impact depends on the missing-data assumptions.” Preserve any supplied counts and analysis details.

**If no source establishes an additional limitation:** Remove the optional duplicate or mark the required limitation entry as unassessed. Do not invent attrition, under-recruitment, inadequate power, or wide confidence intervals. A nonsignificant result alone proves none of them.

### 9. Expert Opinion — advance the decision, keep the evidence

**Context:** The paragraph has reported an exploratory symptom signal; improvement in daily function remains untested. The following development recommendation is explicitly an author proposal, not an existing protocol.

**Before:** “The exploratory symptom signal cannot establish clinical usefulness. Usefulness has not been demonstrated. Further high-quality studies are required.”

**After:** “The exploratory symptom signal leaves daily function unresolved. The next trial should test whether the candidate improves daily function against usual care before supporting routine use.”

**Decision:** Reframe the recommendation while retaining exploratory status and the unresolved outcome. Confirm the proposed comparator and decision criterion with the author when they are protected or contested; do not invent a dose or trial result.

### 10. Safety and ethics — keep a necessary negative

**Original:** “Urgent rescue care must not be delayed to preserve the scheduled outcome assessment.”

**Decision:** Keep in a protocol, safety procedure, or relevant standalone legend. Removing “must not” because it is negative would reverse the practical safeguard.

### 11. Legend disclaimer — depends on the graphic

**Context A:** A flow diagram only shows database screening and article selection; it contains no treatment pathway or causal arrows.

**Before:** “Study-selection flow diagram. This is not a causal model or treatment algorithm.”

**After:** “Study-selection flow diagram.”

**Context B / keep:** A schematic depicts an unvalidated biomarker cutoff leading to a treatment change. Retain “Illustrative, unvalidated cutoff; not a clinical treatment threshold.” It prevents a plausible and consequential misuse. If the graphic is not supplied, do not claim Context A applies.

## Audit output

For an explicit audit, provide scope first and a compact table; for a short rewrite, use only the relevant fields rather than forcing a full report.

| ID / grade | Location | Original wording | Issue and reason | Scientific risk if removed | Recommended action | Suggested revision / retained location |
|---|---|---|---|---|---|---|
| OD-01 / P2 | Exact section, paragraph, table cell, or legend | Short quotation | Category and specific information deficit | Which boundary could be lost, or why none is lost | Keep / Consolidate / Reframe / Delete / Author decision | Minimal edit; name retained location if consolidating |

Use issue labels such as `Repetitive caveat`, `Unnecessary rebuttal`, `Excessive hedging`, `Redundant negative framing`, `Genre-inappropriate procedural detail`, `Cross-section repetition`, `Table-column duplication`, and `Necessary evidence boundary — keep`. For a figure legend, use the appropriate label and identify the graphic-related interpretation risk. A Keep finding is not automatically a defect or a mandatory correction.

Use the existing P0–P3 hierarchy: P0 for credibility blockers requiring verification, P1 for scientific-logic problems, P2 for structure/self-evidence, and P3 for wording or optional style. In multi-reviewer output, map findings into its existing Critical/Major/Minor/Optional Issue Matrix rather than inventing another severity scale. If editorial effort is helpful, mark high/medium/low as an optional workload/order cue only; it cannot override scientific severity. Identify the author-confirmation owner for unresolved scientific decisions.

## Decision persistence and Non-Regression Check

For iterative work, record each accepted decision in the existing Decision Ledger: stable issue ID, proposition, original locations, removed or revised wording, retained evidence boundary and location, reason, author confirmation if required, and version. Author corrections become persistent constraints unless explicitly revoked. For a local edit, a brief change note is sufficient; do not require a new administrative workflow.

Before the next revision and before final delivery, check:

- [ ] Primary results, effect direction, values, timing, population, endpoint definitions, and evidence status remain unchanged.
- [ ] Negative primary findings remain explicit; nonsignificance has not become no effect, equivalence, or safety.
- [ ] Association has not become causation; exploratory results have not become confirmatory, and a same-dataset secondary analysis has not become independent validation. A prespecified confirmatory secondary outcome retains its status under the applicable hierarchy and multiplicity framework.
- [ ] Safety, ethics, adverse events, applicability limits, and author-approved scientific positions remain visible where needed.
- [ ] Neither stronger nor weaker unsupported conclusions have replaced the original meaning.
- [ ] Deleted repetitions have not reappeared elsewhere; retained necessary boundaries have not disappeared in another pass.
- [ ] Abstracts, highlights, tables, legends, and separately read supplements still stand alone; citations remain attached to their claims.
- [ ] Table columns have distinct jobs without invented explanatory facts; required reporting information remains present.
- [ ] Missing sources or sections are still marked unassessed, not silently upgraded to verified.
- [ ] The result is clearer and scientifically faithful, not merely shorter.

Reopen failed items; do not declare success from fewer negatives, more deletions, or a target compression ratio. Stop when the remaining qualifications are justified and the wording is accurate and natural. Report unresolved author decisions without endless stylistic rewriting.
