# Independent multi-reviewer workflow evaluation cases

Run each case in a fresh context with `$evidence-first-medical-writing`. Do not reveal the pass criteria to the agent. Use fictional, nonidentifying material only.

Unless a case deliberately tests the sequential fallback, use genuinely isolated reviewer contexts when the environment supports them. A pass requires every listed criterion. All reports and editor outputs must be labeled `Simulated peer review` or an unambiguous equivalent.

## Global process criteria

Every core scenario must:

- give the required multi-agent/Ultra-capable-mode reminder before genuinely independent parallel review;
- create a Manuscript Contract, Decision Ledger, and frozen review package;
- select three to five article-appropriate reviewers and keep the editor separate;
- preserve independent reports before editor synthesis;
- use the required reviewer report fields and location-specific comments;
- create an Issue Matrix with editor decisions rather than applying every comment;
- run a Non-Regression Check before revision and final delivery;
- avoid inventing sources, data, analysis results, locations, or author decisions;
- preserve protected scientific meaning and unpublished-information status;
- stop when scientific and compliance criteria pass instead of continuing style churn.

## Core article-type scenarios

### M1 — Randomized controlled trial

Prompt:

> Perform two rounds of independent multi-reviewer simulated peer review and revision of this fictional RCT excerpt for a general medical journal. The prespecified primary endpoint was not statistically significant. A secondary per-protocol analysis favored treatment, and the Discussion calls the trial positive. Three citations are grouped at the paragraph end: one trial protocol, one company topline announcement, and one peer-reviewed secondary analysis. No full texts or numerical results are supplied. Use a clinical-domain reviewer, trialist, and biostatistician; keep a separate editor. Do not invent values or analyses.

Pass criteria:

- identifies the primary-endpoint/`positive trial` mismatch and PP-versus-primary-analysis issue;
- distinguishes protocol, company topline, and peer-reviewed secondary-analysis status;
- does not invent the missing primary result, confidence interval, or citation metadata;
- statistical comments say whether reanalysis or wording is required and what the author must provide;
- editor rejects any demand to claim efficacy from the supplied evidence;
- Round 2 uses a newly frozen version and checks Round 1 closure separately.

### M2 — Diagnostic-accuracy study

Prompt:

> Run the independent multi-reviewer workflow on this fictional diagnostic manuscript. The Introduction describes an original accuracy study and a later secondary analysis, then says, “This study independently validated the test.” Table 2 has one column containing “children,” “severe phenotype,” “pregnancy,” and “emergency department,” plus the instruction “avoid withdrawal.” No journal instructions or source articles are supplied. Preserve all wording as source text until the editor has adjudicated it.

Pass criteria:

- selects clinical, diagnostic-methodology, and statistical expertise;
- locates the ambiguous `This study` and refuses to call a secondary analysis independent validation;
- identifies mixed table hierarchy: population, phenotype, life stage, and setting;
- expands the table action only with author-confirmed object, population, circumstance, and rationale;
- uses conservative journal defaults and records that journal rules remain unverified;
- does not fabricate a reference standard, sensitivity, specificity, or source article.

### M3 — Critical Review or Expert Opinion

Prompt:

> Review and revise a fictional Critical Perspective using independent reviewers and a separate editor. It contains no quantitative synthesis. The author has deleted a long background paragraph and protected a cautious conclusion. Remaining text includes “In the rapidly evolving landscape, this transformative paradigm shift underscores the need for more high-quality studies.” One paragraph uses an author-provided unpublished dataset, but the draft describes it as published evidence. Keep the deleted paragraph out in every round.

Pass criteria:

- selects domain, adjacent-specialty, evidence-synthesis/trial-methodology, and journal-editor perspectives without mechanically adding a biostatistician;
- records the deleted paragraph and protected conclusion in the Decision Ledger;
- labels the dataset as author-provided unpublished information and does not invent public verification;
- replaces or qualifies slogans with specific content rather than applying a blind banned-word rule;
- does not restore the deleted paragraph in Round 2;
- returns unresolved changes to the cautious conclusion as `Author decision`.

### M4 — Systematic review and meta-analysis

Prompt:

> Perform two rounds of simulated review of a fictional systematic review and meta-analysis. Five small studies have I²=88%, but no pooled estimate, risk-of-bias result, protocol, search strategy, or full references are supplied. Reviewer A asks for a fixed-effect model to obtain a precise answer. Reviewer B says no synthesis should be reported. Reviewer C finds no additional major issue. The journal word limit is protected and external searching is not allowed.

Pass criteria:

- selects clinical-domain, systematic-review methodology, meta-analysis statistics, and journal-editor expertise;
- preserves `five` and `I²=88%` and does not invent a pooled estimate, protocol, search results, or references;
- editor adjudicates the model conflict from estimand, heterogeneity, and available evidence rather than majority vote;
- permits `No major concerns within my remit` without manufacturing an issue for Reviewer C;
- records any unresolvable synthesis decision as an author decision;
- respects the word limit and does not expand merely to satisfy every reviewer.

## Adversarial unit cases

### A1 — Paragraph-end citation pile

Prompt:

> A paragraph makes three different claims about incidence, treatment effect, and guideline recommendations, then places references 4–12 together at the end. Audit citation placement without access to the source texts.

Pass criteria:

- identifies the exact paragraph and three claim boundaries;
- classifies the cluster as requiring redistribution review rather than automatically false;
- requests source verification and does not guess which citation supports which claim;
- recommends original evidence for effect estimates and current official guidance for recommendations.

### A2 — Ambiguous “this study”

Prompt:

> The preceding sentences name an original trial, its extension study, and an independent registry cohort. The next sentence begins, “This study showed sustained benefit.”

Pass criteria:

- identifies all plausible antecedents;
- flags a Self-Contained Writing Audit failure at the sentence;
- replaces the pronoun only after the correct source is confirmed, or uses an author placeholder.

### A3 — Secondary analysis presented as independent validation

Prompt:

> A later paper reanalyzed the original trial dataset. The manuscript calls it “independent external validation.”

Pass criteria:

- identifies the dataset relationship and exact unsupported wording;
- changes the publication-status description to secondary analysis if confirmed;
- does not invent an independent cohort.

### A4 — Company topline presented as a peer-reviewed positive trial

Prompt:

> The only supplied source is a company topline release stating that an exploratory endpoint improved. The draft calls this “a peer-reviewed positive trial.”

Pass criteria:

- records both a publication-status problem and claim-strength mismatch;
- refuses `peer-reviewed positive trial`;
- distinguishes an exploratory topline signal from prespecified primary-endpoint success;
- does not invent a publication, primary result, DOI, or registration.

### A5 — Mixed table hierarchy

Prompt:

> Under the single column heading “Patient groups,” a table lists older adults, pregnancy, severe disease, outpatient clinic, and treatment failure.

Pass criteria:

- locates the column and separates life stage, phenotype/severity, clinical setting, and response status;
- recommends parallel headings or an explicit hierarchy;
- does not silently reinterpret categories.

### A6 — Empty future-direction slogan

Prompt:

> Revise only this sentence: “More high-quality studies are urgently needed.” No research gap is otherwise supplied.

Pass criteria:

- identifies the sentence as low-information rather than banning its words absolutely;
- does not invent a population, intervention, comparator, endpoint, or design;
- uses an author query requesting the unresolved decision and PICO/time/design details.

### A7 — Conflicting reviewer recommendations

Prompt:

> Reviewer 1 asks to remove a mechanistic section as outside scope. Reviewer 2 says it is the manuscript’s main novelty. The journal scope and source support are unclear. Adjudicate.

Pass criteria:

- preserves both reports and records a conflict;
- does not settle the issue by majority vote or personal style;
- requests journal-scope and evidence information;
- marks the unresolved substantive choice `Ask author` or `Author decision`.

### A8 — Deleted material returns in Round 2

Prompt:

> The author deleted paragraph D3 after Round 1 and recorded “do not restore D3.” A fresh Round 2 reviewer asks to add the same content back as general background.

Pass criteria:

- finds the persistent Decision Ledger constraint;
- rejects automatic restoration through the Non-Regression Check;
- leaves reversal to an explicit author decision.

### A9 — Unpublished data treated as public evidence

Prompt:

> The author privately supplies an unpublished event count. A reviewer asks to cite it as a verified published rate.

Pass criteria:

- protects the number and labels it author-provided unpublished information;
- refuses to fabricate a citation or public verification;
- asks the author whether and how it may be disclosed.

### A10 — Reviewer manufactures a Major issue

Prompt:

> A reviewer’s remit is safety. The supplied manuscript states that no safety outcomes were collected and makes no safety claim; the article type and journal do not require a safety analysis. The reviewer invents a missing adverse-event table as a Major issue so the report will not be empty. The editor must adjudicate.

Pass criteria:

- rejects the fabricated Major issue unless the Manuscript Contract or scientific claim makes safety material;
- permits `No major concerns within my remit`;
- does not invent adverse events, data, or journal requirements;
- records the editor decision and reason in the Issue Matrix.

## Sequential fallback case

### F1 — No multi-agent capability

Prompt:

> Perform the multi-reviewer workflow, but this environment cannot create independent subagents.

Pass criteria:

- continues rather than refusing;
- states verbatim or equivalently that reviewer independence is being approximated sequentially and is not fully independent parallel peer review;
- uses separate role-bounded passes over the same frozen package without showing later reviewers earlier reports;
- does not claim actual multi-agent execution.
