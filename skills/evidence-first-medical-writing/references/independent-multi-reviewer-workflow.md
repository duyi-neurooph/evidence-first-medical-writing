# Independent Multi-Reviewer Peer Review and Iterative Revision

## Scope and activation

Use this workflow for simulated peer review of general clinical research and medical review manuscripts, including:

- randomized trials and trial protocols;
- cohort, case-control, and cross-sectional studies;
- diagnostic-accuracy and prediction-model studies;
- systematic reviews and meta-analyses;
- narrative reviews, critical reviews, critical perspectives, and expert opinions;
- clinical guidelines, consensus statements, and policy-oriented medical articles;
- reviewer-response revision and whole-manuscript checks before resubmission.

Activate it when the user asks for independent reviewers, mutually isolated specialty reviews, an editor to reconcile reports, two or more review-and-revision rounds, or a combined manuscript/statistical/citation/table/journal audit. Typical triggers include:

- “模拟几个独立审稿人审稿并修改”;
- “不同专业审稿人互不影响”;
- “模拟编辑和审稿人进行两轮修改”;
- “先审稿，再改稿，再复审”;
- “perform independent multi-reviewer peer review”;
- “run two rounds of peer review and revision”;
- “review this manuscript as a clinician, methodologist and statistician”;
- “check references, self-contained writing and AI-like language.”

Every report, decision letter, and consolidated output must be labeled `Simulated peer review` or an unambiguous equivalent. Never imply that the reports came from a real journal, editor, or external peer reviewer.

## Defaults and capability disclosure

Unless the user overrides them, use:

- two rounds;
- three to four independent reviewers selected for the article type;
- one separate editor who is not counted as a reviewer;
- journal-specific compliance review;
- a distinct claim-to-citation audit;
- a clean revision plus an Issue Matrix.

The user may override reviewer roles, number of rounds, strictness, external-search permission, tracked-changes requirements, protected sections, and output formats. Do not begin with a long questionnaire. Ask only when missing information would materially alter scientific meaning or produce a clearly incorrect journal format.

### Versioned availability reminder — checked 2026-08-17

Before any capability or fallback explanation for a request that requires genuinely independent parallel reviewers, reproduce this sentence verbatim:

> For genuinely independent parallel reviewer assessments, use a multi-agent or Ultra-capable mode when available. In the current ChatGPT Work interface, GPT-5.6 Sol with Ultra is recommended when available on the user’s account.

Keep the workflow’s routing capability-based (`multi-agent or Ultra-capable mode`). Treat the specific product and model wording above as a versioned availability note, not a permanent dependency.

The reminder remains required when the current environment cannot create independent subagents; give it first, then disclose the sequential fallback.

If independent subagents are unavailable, continue sequentially and state:

> Reviewer independence is being approximated sequentially with isolated review passes; this is not fully independent parallel peer review.

Do not refuse the task merely because multi-agent or Ultra capability is unavailable.

## 1. Establish the Manuscript Contract

Before review, build an internal Manuscript Contract from the supplied files and instructions. Record:

| Field | Required content |
|---|---|
| Target | journal, article type, target audience |
| Language | manuscript language; British or American English |
| Limits | word limit; mandatory sections |
| Journal rules | abstract, highlights, tables, figures, supplements, and reference requirements |
| Reporting standard | applicable current guideline, such as CONSORT, STROBE, STARD, PRISMA, TRIPOD, or SPIRIT |
| Version | manuscript version and date or other stable identifier |
| Source package | manuscript files, tables, supplements, journal guidelines, template, protocol, registration, and other supplied sources |
| External research | allowed or not allowed; permitted scope |
| Protected decisions | author positions, terminology, data, and structure that must be retained |
| Immutable facts | facts, numbers, endpoint definitions, unpublished information, and other material that must not be altered |
| Rejected content | material the user has deleted, rejected, or instructed the workflow not to restore |
| Deliverables | requested file types, tracked changes, annotations, and naming convention |

If journal guidance or a template is supplied, read it before applying general experience. For requirements that may have changed, consult current official sources only when external research is permitted, and record the date checked.

Use conservative defaults for noncritical omissions and disclose them in the output. Ask the user only when an omission would change the scientific interpretation, the protected content, or a material journal requirement. Never infer unpublished facts.

## 2. Freeze the review package

Create a stable, versioned copy of the material to be reviewed. Never overwrite the original manuscript.

Each reviewer receives the same frozen package:

- frozen manuscript and associated tables, figures, and supplements;
- journal guidelines and required reporting standard;
- relevant source package permitted by the Manuscript Contract;
- the Manuscript Contract;
- one reviewer-specific remit.

The remit may define the reviewer’s expertise and priority checks. It must not contain a prewritten list of manuscript defects or conclusions designed to make reviewers agree.

In multi-agent mode:

1. Use one separate subagent per reviewer.
2. Do not show any reviewer another reviewer’s report, the editor’s synthesis, or another agent’s draft or summary.
3. Do not use a shared leading review outline. Common output fields are allowed, but substantive checks must follow each reviewer’s remit.
4. Permit disagreement and the finding `No major concerns within my remit`.
5. Keep the editor separate until all original reports are complete.

In sequential fallback, run each reviewer as a clean, role-bounded pass over the same frozen package. Do not carry previous reports or editor conclusions into the next reviewer pass. Disclose that independence is approximate. If the available interface cannot isolate contexts at all, state that limitation rather than claiming independent review.

For Round 2, freeze the revised manuscript as a new version and use fresh reviewer subagents or fresh isolated passes. These reviewers normally do not see Round 1 reports. The editor separately checks Round 1 closure against the response matrix.

## 3. Select reviewers by article type

Select three to five reviewers. Do not assign the same panel mechanically to every manuscript.

| Article type | Default reviewer mix |
|---|---|
| Randomized trial | clinical-domain specialist; clinical trialist or intervention specialist; biostatistician; optional safety, implementation, or patient-centred reviewer |
| Observational study | clinical-domain specialist; epidemiologist; biostatistician; optional external-validity or implementation reviewer |
| Diagnostic study | clinical-domain specialist; diagnostic-methodology specialist; biostatistician; optional intended-use or implementation reviewer |
| Prediction study | clinical-domain specialist; prediction-model methodologist; biostatistician; optional implementation reviewer |
| Systematic review/meta-analysis | clinical-domain specialist; systematic-review methodologist; meta-analysis statistician; journal editor-style reviewer |
| Narrative/critical/expert review | disease-domain specialist; relevant adjacent-specialty reviewer; evidence-synthesis or trial-methodology reviewer; journal editor-style reviewer; add a biostatistician only for substantial quantitative comparison, trial interpretation, or meta-analysis |
| Research protocol | clinical trialist; biostatistician; operational-feasibility or recruitment specialist; ethics/safety reviewer |
| Guideline, consensus, or policy article | clinical-domain specialist; guideline/evidence-synthesis methodologist; implementation or policy reviewer; journal editor-style reviewer; add statistics or equity expertise when central |

Add a paediatric, pregnancy, geriatric, patient-reported-outcome, implementation, accessibility, or health-equity perspective only when age, reproductive stage, comorbidity, treatment risk, outcome validity, access, or implementation changes the scientific question. Do not add special-population reviewers merely for demographic completeness.

The editor adjudicates; the editor is never an extra reviewer.

## 4. Reviewer report contract

Each reviewer independently outputs:

1. `Overall assessment`;
2. `Recommendation`: `accept as is`, `minor revision`, `major revision`, or `not suitable in current form`;
3. `Major comments`;
4. `Minor comments`;
5. `Journal-compliance concerns`;
6. `Uncertainties requiring author confirmation`.

Each substantive comment should contain:

```text
Severity:
Exact location:
Quotation or uniquely identifiable text:
Problem:
Why it matters:
Possible consequence for interpretation, reproducibility, or acceptance:
Evidence or methodological basis:
Actionable recommendation:
Resolution owner: Direct edit / Author decision / Reanalysis or source verification
```

Do not accept vague comments such as “The manuscript should be improved,” “More references are needed,” “The discussion should be strengthened,” “More studies are required,” or “The authors should clarify this” unless the reviewer supplies a location, reason, and concrete action.

Reviewers must not manufacture a Major issue to fill their role. `No major concerns within my remit` is a valid, useful conclusion.

### Statistical reviewer remit

Use clinical language and check only what is relevant:

- design-question alignment and the estimand or practical effect being estimated;
- sample size, power, and recruitment shortfall;
- randomization, allocation, baseline imbalance, and analysis sets;
- primary, secondary, and exploratory endpoint hierarchy;
- repeated measures, missing data, censoring, multiplicity, and interim analysis;
- model assumptions, effect estimates, confidence intervals, and overreliance on P values;
- subgroup interactions rather than comparison of within-group significance;
- post hoc and sensitivity analyses and causal language;
- diagnostic sensitivity, specificity, predictive values, and reference standard;
- prediction-model overfitting, calibration, and internal versus external validation;
- meta-analysis heterogeneity, small-study effects, and risk of bias.

For every statistical comment, state whether it may change the conclusion, whether wording alone can resolve it, whether reanalysis is needed, and what the author must provide. Do not redesign the entire study merely to display statistical expertise.

## 5. Editor adjudication

Only after all independent reports are complete may the editor synthesize them. The editor must:

1. preserve the original reports;
2. remove duplicates without erasing differences in rationale;
3. identify conflicts explicitly;
4. decide from evidence, remit relevance, journal scope, and scientific impact rather than majority vote;
5. accept, modify, reject, or return each issue to the author;
6. reject personal style preferences, unnecessary expansion, genre-inappropriate requests, unsupported stronger claims, suggestions that exceed available material, and irrelevant additions made only for apparent completeness;
7. mark unresolved substantive conflicts `Author decision` instead of silently choosing for the author.

### Issue Matrix

Create one row per adjudicated issue:

| Field | Allowed content |
|---|---|
| Issue ID | stable identifier retained across rounds |
| Reviewer | reviewer role or report identifier |
| Severity | Critical / Major / Minor / Optional |
| Location | exact manuscript location |
| Issue | specific defect or concern |
| Editor decision | Accept / Modify / Reject / Ask author |
| Planned action | direct edit, author query, reanalysis, source check, or no action |
| Evidence source | manuscript, protocol, journal rule, reporting guideline, or verified citation |
| Status | Open / In progress / Resolved / Author decision / Rejected |

Severity definitions:

- `Critical`: data integrity, ethics, false or erroneous citation, core design/statistical error, unsupported central claim, material misstatement of population/intervention/primary outcome/result, or fundamental mismatch with journal scope/article type.
- `Major`: may change the main interpretation, conclusion, reproducibility, or editorial decision.
- `Minor`: does not change the scientific conclusion but affects clarity, compliance, or readability.
- `Optional`: reasonable but unnecessary preference or extension.

## 6. Decision Ledger and Non-Regression Check

Create a Decision Ledger when the workflow starts and update it after every editor decision and user correction.

| Ledger section | Record |
|---|---|
| Accepted structure | section order, argument architecture, and elements the user accepted |
| Rejected or deleted content | passages and ideas that must not be restored automatically |
| Protected science | wording, claims, endpoint labels, data, and author positions requiring approval to change |
| Confidential evidence | author-provided unpublished information and its allowed use |
| Language conventions | terminology, abbreviations, British/American English, and naming preferences |
| Citation decisions | source-status labels, numbering method, and accepted citation placement |
| Known failure patterns | recurring ambiguity, citation clustering, hierarchy, tone, or table problems |
| Open uncertainty | unresolved facts and required author decisions |
| Round constraints | every new restriction accepted after each review round |

User corrections become persistent constraints unless the user explicitly revokes them.

Before every revision and before final delivery, run the Non-Regression Check:

- [ ] No deleted or rejected content has returned.
- [ ] Citations have not accumulated at a paragraph end when they support different claims.
- [ ] `this`, `these`, `they`, `it`, `the study`, and `the trial` have one unambiguous referent.
- [ ] Original trial, secondary analysis, extension, independent validation, registry update, conference abstract, company-reported topline, preprint, and unpublished data remain correctly distinguished.
- [ ] No exploratory endpoint has become a primary endpoint.
- [ ] No registry, topline, abstract, preprint, or unpublished result is presented as peer-reviewed full-publication evidence.
- [ ] Empty slogans, template conclusions, and rejected wording have not returned.
- [ ] Table rows and columns remain parallel and independently understandable.
- [ ] Citation callouts, numbering, and the reference list remain synchronized.
- [ ] No protected number, definition, scientific meaning, authorship, funding, conflict disclosure, or unpublished information has changed without approval.

Any failed check reopens or creates an Issue Matrix item. Do not silently waive it.

## 7. Independent audit workstreams

Run the following audits as named workstreams. Citation integrity is not a by-product of language polishing.

### Self-Contained Writing Audit

Check the abstract, main text, figure legends, tables, and supplements for:

- explicit subjects, objects, comparison directions, populations, interventions/exposures, comparators, time windows, and outcomes;
- ambiguous `this`, `these`, `they`, `it`, `the study`, `the trial`, `the programme`, `the former`, and `the latter`;
- explicit distinction among an original trial, analysis of the same dataset, extension, independent replication, registry update, company disclosure, and other publication states;
- expansion of uncommon abbreviations at first use and consistent terminology thereafter;
- headings, subheadings, paragraphs, and list items at parallel logical levels;
- one identifiable main job per paragraph.

For tables, verify that every row can be understood without the main text; column entries share a logical level; population, phenotype, life stage, and clinical setting are not mixed as peers without an explicit hierarchy; verbs identify their objects and conditions; and footnotes define abbreviations, units, time points, outcomes, analysis sets, and comparison directions. Replace telegram phrases such as `avoid withdrawal`, `do not require exclusion`, or `consider escalation` with an explicit object, population, circumstance, and clinical reason.

### AI-Like Residue Audit

Flag formulaic language only when it adds little information or exceeds the evidence. Review phrases such as `It is important to note that`, `This highlights`, `This underscores`, `In the rapidly evolving landscape`, `a paradigm shift`, `robust and comprehensive`, `transformative potential`, `more high-quality studies are urgently needed`, and `not merely X, but Y`, as well as repeated three-part slogans, excessive dashes, low-information symmetry, repeated use of `critical`, `important`, `promising`, or `novel`, and agentless future declarations.

Do not maintain an absolute banned-word list. Ask whether the wording identifies a concrete subject, action, result, time, mechanism, or evidentiary boundary; whether its strength matches the evidence; and whether deletion loses real information.

Future recommendations should state who should act, for which population or setting, what should be done, when, why, and which outcome would show success. Replace generic `more research is needed` with the unresolved decision and the needed population, intervention/exposure, comparator, timing, endpoint, and design. Do not create a false dichotomy merely to sound decisive.

### Claim–Citation Audit

Build a Claim–Citation Map with one row per key factual or normative claim:

| Claim ID | Exact claim and location | Required source type | Current citation | Publication status | Support judgment | Action |
|---|---|---|---|---|---|---|

Apply these rules:

1. Place citations near the sentence or clause they directly support.
2. Do not require one citation per sentence when one source clearly supports a short, continuous argument; make the support span explicit.
3. Use citation clusters only when all sources support the same bounded claim. Trigger manual redistribution review for large clusters without declaring them automatically wrong.
4. Prefer original studies for trial design, primary outcomes, and results; use reviews, guidelines, and consensus documents for context, synthesis, and practice recommendations.
5. Label peer-reviewed full publications, secondary analyses, protocols, trial registries, conference abstracts, company press releases/topline disclosures, preprints, and author-provided unpublished data distinctly.
6. Do not convert exploratory results into primary-endpoint success, per-protocol signals into intention-to-treat findings, secondary analyses into independent confirmation, biological signals into clinical benefit, or nonsignificant trends into positive trials.
7. Use `positive trial` only when the prespecified primary endpoint and analysis framework support that description. Otherwise name the exact signal and its status.
8. Verify existence and, when accessible, authors, title, journal, year, volume, pages, DOI/PMID/registration, population, intervention, comparator, endpoint, and claim fit.
9. Check citation numbering, reference-list correspondence, journal style, and journal restrictions on citations in titles or abstracts.
10. If full text or metadata cannot be verified, mark it; never guess. Report conflicts among a registry, publication, protocol, and company disclosure, and prefer the more authoritative evidence for the claim at issue.

The final Citation Audit must classify each relevant item as `Verified`, `Partially verified`, `Unsupported`, `Misplaced citation`, `Citation cluster requiring redistribution`, `Metadata problem`, `Publication-status problem`, or `Claim-strength mismatch`.

## 8. Revise only after adjudication

Do not edit the manuscript while independent reports are still being produced or before the editor has adjudicated them.

During revision:

- preserve the author’s voice instead of imposing uniform AI journalese;
- do not alter sample size, design, dose, endpoint, result, confidence interval, adverse event, authorship, funding, conflicts of interest, or unpublished information;
- do not replace accurate language with stronger but unsupported wording;
- do not expand the manuscript without a clear issue and evidentiary purpose;
- verify new factual content before insertion;
- label user-provided unpublished information internally as `Author-provided unpublished information` or an equivalent confidential status;
- reduce claim strength or record an evidence gap when support is insufficient;
- make every accepted edit traceable to an Issue Matrix item or an explicit author instruction.

Create a point-by-point response matrix linking issue ID, editor decision, action, revised location, evidence, effect on interpretation, status, and author confirmation if required.

## 9. Rounds and stopping rules

### Round 1

1. Freeze manuscript version 1 and the source package.
2. Obtain independent reports.
3. Adjudicate reports and create the Issue Matrix.
4. Revise only accepted or modified issues.
5. Update the Decision Ledger and Non-Regression Checklist.
6. Produce the response matrix.

### Round 2

1. Freeze the revised manuscript as version 2.
2. Use fresh independent reviewers who normally do not see Round 1 reports.
3. Have the editor separately audit Round 1 issue closure against the response matrix.
4. Identify residual issues, new issues, and revision-induced regressions.
5. Adjudicate and revise again.
6. Complete final citation, statistical, self-contained-writing, table/figure, AI-residue, and journal-compliance audits.

Start Round 3 only if a Critical issue remains; a Major issue may change the main interpretation; reference or data integrity is unresolved; journal compliance still fails; or the user explicitly requests another round.

Stop when there are no unresolved Critical or Major issues; central claims are appropriately supported or qualified; journal and reference checks pass; the Non-Regression Check passes; and further changes would be unbounded style optimization rather than correction.

## 10. Deliverables and file safety

Provide only the deliverables relevant to the user’s request:

1. revised clean manuscript;
2. tracked-changes or annotated version when supported;
3. simulated editor decision letter;
4. independent reviewer reports;
5. consolidated Issue Matrix;
6. point-by-point response matrix;
7. Citation Audit;
8. Decision Ledger;
9. Non-Regression Checklist;
10. final journal-compliance checklist;
11. remaining author decisions;
12. a version manifest with filenames.

Never overwrite source files. Use explicit versioned names, for example:

```text
study_original_v1.docx
study_revised_clean_r1_v2.docx
study_tracked_r1_v2.docx
study_revised_clean_r2_v3.docx
study_tables_r2_v3.docx
study_supplement_r2_v3.docx
study_simulated_reviewer_reports_r1.md
study_simulated_editor_issue_matrix_r1.xlsx
study_citation_audit_r2.xlsx
study_final_audit_r2.md
```

When tracked changes are unavailable, provide an annotated change log linked to stable section or paragraph identifiers. Mark every unresolved item `[Author to provide / 待作者补充: specific content / 具体内容]`.
