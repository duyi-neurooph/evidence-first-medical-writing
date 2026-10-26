# Retrieve and apply current reporting guidelines

## When to run

Before substantive manuscript planning, drafting, rewriting, manuscript review (including a single simulated reviewer), independent multi-reviewer review, or a presubmission audit, identify the actual study design and obtain the applicable reporting guidance. The user need not mention EQUATOR. Also activate on requests such as “use EQUATOR,” “check reporting completeness,” “按报告指南写作,” or “根据最新指南审稿.”

For a section or abstract, retrieve the relevant guidance and limit the assessment to that scope. Pure spelling, formatting, or literal translation without a reporting assessment does not require a new search. Reuse an already verified guideline package within the same task; do not redownload it for every paragraph or reviewer.

This is a runtime procedure for an assistant with browsing and, where available, file-download tools. It does not install a downloader or grant network access. Public guideline retrieval is a default part of the writing/review task when those tools are available and the user has not prohibited external access. Honor any external-search restriction in the Manuscript Contract. Record guideline lookup separately from permission for a broader literature search. Never transmit manuscript text, patient details, unpublished results, or private files to a search engine or third-party checker; use generic design and reporting-topic terms.

## 1. Select by actual design and reporting purpose

First run [study-design-confirmation.md](study-design-confirmation.md). Explain the proposed classification to the author and obtain or reuse fact-based confirmation. If decisive facts remain unresolved, ask focused questions and keep guidance selection provisional; do not finalize a compliance assessment from the title, author-preferred label, routine follow-up, or use of historical records alone.

Read supplied journal instructions, templates, and checklists first. Identify whether the document reports completed research, a protocol, an evidence synthesis, a narrative argument, or guideline/consensus development. Record design features that may require extensions: cluster allocation, noninferiority, routinely collected data, diagnostic AI, prediction modelling, scoping review, and similar features.

Use the [EQUATOR reporting-guideline library](https://www.equator-network.org/reporting-guidelines/) and its [selection toolkit](https://www.equator-network.org/toolkits/selecting-the-appropriate-reporting-guideline/) as discovery entry points. Search by study type, relevant clinical area, and report section; prefer English search terms. Follow the selected record to the issuing group's official site or original publication.

These families are search starting points, not a version registry or exhaustive list:

| Actual manuscript | Search starting point |
|---|---|
| Randomized trial results | CONSORT and applicable design/intervention/abstract extensions |
| Cohort, case-control, cross-sectional study | STROBE; relevant extensions such as RECORD for routinely collected health data |
| Diagnostic accuracy | STARD and relevant extensions, including AI when applicable |
| Prediction-model development, validation, or updating | Current TRIPOD family, including TRIPOD+AI where its scope applies; do not assume regression models are excluded |
| Randomized trial protocol | SPIRIT and relevant extensions; do not apply a completed-results checklist as the protocol standard |
| Systematic review/meta-analysis or scoping review | PRISMA and relevant review-type extensions; search PRISMA-ScR for scoping reviews |
| Systematic-review protocol | PRISMA-P and any applicable protocol guidance |
| Case report, qualitative study, economic evaluation, quality improvement, animal study | CARE, SRQR/COREQ, CHEERS, SQUIRE, or ARRIVE, respectively; verify exact scope |
| Clinical guideline or consensus development | Search RIGHT/AGREE reporting guidance or ACCORD according to the actual development methods; distinguish reporting guidance from appraisal instruments |
| Narrative review, Critical Review, Perspective, Expert Opinion, policy article | Search for genre-specific guidance and journal requirements; do not impose PRISMA solely because the article is called a review |

Select a main guideline plus only relevant extensions after the design gate. A generic table cannot replace author clarification or the live search. Candidate-guideline exploration can inform the discussion, but unresolved classifications remain explicit and cannot support a final checklist pass. If no applicable guideline is found after a targeted search, record the search scope and `No applicable guideline identified`; do not invent an EQUATOR checklist or a compliance score. Use the journal's genre rules and the skill's evidence/argument checks.

## 2. Retrieve, read, and verify the version

1. Open the EQUATOR record, then the issuing organization or primary publication. Confirm scope, publication/version date, corrections, replacements, and relevant extensions. Search-result snippets, a familiar acronym, a year in a URL, and a website's “last updated” date are not sufficient evidence of the current guideline version.
2. Obtain and read the actual checklist and reporting statement. Read the explanation/elaboration or expanded checklist where needed to interpret items; obtain relevant flow diagrams, abstract checklists, and extensions. If a short checklist is ambiguous and its explanation cannot be read, mark that interpretation unverified. Do not reconstruct item wording or numbering from memory.
3. Download official files into the current task's private workspace when file tools support it. Use a task-scoped `guidelines/` directory and versioned filenames; do not overwrite supplied files. Confirm that a download is the intended readable PDF, DOCX, or HTML, not an error/login page, and that item tables and footnotes were actually extracted or visually inspected. An HTTP success or saved filename alone does not prove the document was read.
4. When only browsing is available, reading the complete official HTML or tool-readable document is acceptable. Record `Read online; no local download` and preserve the source link. Never claim a file was downloaded when it was only opened, or a full checklist read when only its landing page was accessible.
5. Compare the main standard, extensions, journal template, and supplied checklist. A journal may still request an older checklist. Preserve its submission requirement, explain differences from the current official guidance, and cross-reference verified item numbers rather than silently swapping editions. Older extensions can remain applicable to a newer main standard; record compatibility and numbering differences instead of automatically discarding them.

Call a version `Current official version verified on YYYY-MM-DD` only when the live sources support that statement. Otherwise use `Version currency unverified` and explain what was accessible. No publication year or external file URL in this skill is permanently authoritative.

## 3. Record a Guideline Manifest

Record one entry per selected main guideline, extension, or journal-required checklist:

| Field | Record |
|---|---|
| Guideline ID | stable local identifier, e.g. G1, G2 |
| Identity and purpose | exact title, version/year, main/extension/journal role, applicable design and selection reason |
| Provenance | EQUATOR record URL; official issuing/publication URL; actual checklist URL |
| Retrieval | date checked; downloaded file path and SHA-256 when feasible, or online-only URL; document format |
| Read coverage | checklist, statement, explanation/elaboration, extensions, flow diagram: read / partially read / unavailable / not applicable |
| Currency | verified current / unverified / superseded but journal-required; evidence and any conflict |
| Application scope | manuscript version, sections available, journal constraints, permitted external access |

Use `Unavailable` for missing metadata, not an invented value. Briefly tell the user which guidelines/versions will be used, why, when checked, and any access or version limitation before drafting or reviewing. Link the sources in the output. Keep downloaded third-party documents in task materials; do not bundle them in the public skill or imply their license is this repository's license.

## 4. Apply a Reporting Guideline Matrix

Use exact item identifiers from the retrieved version and paraphrase requirements briefly. Keep the evidence for each judgment traceable:

| Guideline/version and item | Requirement summary | Manuscript location and evidence | Status | Specific improvement or author query | Owner / issue ID |
|---|---|---|---|---|---|

Allowed status values:

- `Reported`: adequately addressed in the supplied material, with a location.
- `Partially reported`: some required information is present; identify the missing part.
- `Not reported`: absent from the complete relevant material examined.
- `Not applicable`: a reason based on actual design or article type is recorded.
- `Cannot assess`: source, section, data, or interpretation is unavailable or unresolved.
- `Planned`: an outline or draft slot awaits real author information; not a compliance pass.

For a full-manuscript audit, cover every applicable item in the selected checklists and show justified exclusions. For a section or abstract, declare the assessed subset and mark out-of-scope material `Cannot assess` when included in the matrix; do not label an unseen Methods section deficient. Check supplied completed checklists against the manuscript rather than trusting their page references. Use stable section/paragraph/table locations when page or line numbers are unavailable.

For writing, use items to build the outline, section information slots, table/figure plan, and author queries before drafting. Fill them only from verified author materials. For review, link each missing or partial item to its location, scientific or reporting consequence, and smallest concrete improvement. Separate editorial fixes from author confirmation or reanalysis. After revision, update the matrix against the new manuscript and retain the original issue IDs.

Reporting completeness is not study validity, risk of bias, ethical approval, or evidence certainty. Do not create an overall “quality score” from checklist completion or infer misconduct from an omission. An openly reported lack of blinding may satisfy a reporting item while remaining a methodological limitation. Never invent blinding, registration, sample-size calculations, analyses, or results to make a checklist pass. Evaluate methodological concerns separately using the existing credibility and statistical checks.

## 5. Independent reviewers and iteration

Retrieve guidance before freezing Round 1. Put the same unannotated source documents and Guideline Manifest into every reviewer's package, alongside the Manuscript Contract. Assign reporting-completeness responsibility to an appropriate reviewer without replacing other reviewers' remits.

Do not share an editor-filled Reporting Guideline Matrix, suspected omissions, other reviewers' assessments, or prior-round annotated checklists with independent reviewers. They apply the same factual requirements independently; the editor consolidates their findings only after all reports arrive. The editor links accepted reporting issues to the Issue Matrix and Decision Ledger.

Keep the guideline versions frozen across rounds of the same task. Recheck currency for a new task, resubmission, changed study type/journal, or a reported update. If a newly discovered correction changes the review materially, record the reason, version the guidance package, and apply it consistently in the next round; do not silently change the criteria mid-round. Fresh Round 2 reviewers receive the revised manuscript and clean guideline package, not the Round 1 matrix. The editor separately checks closure and non-regression.

Before final delivery, verify that reporting omissions have not reappeared, item numbers still match the selected editions, and author-provided facts have not been replaced by checklist assumptions. Include the Guideline Manifest and relevant Reporting Guideline Matrix with the existing deliverables. A full reporting-completeness pass requires all applicable items assessed and resolved; unavailable guidance or unresolved items must remain visible, even when limited drafting can finish.

## 6. Access failures and stopping

If browsing is forbidden or unavailable, or the official document cannot be retrieved/read, state that limitation before substantive work. Use supplied documents or a previously verified local copy with its original retrieval date and `Version currency unverified`; never describe it as a new live check. Do not bypass access controls or invent a complete checklist.

After a failed official route, try an EQUATOR-linked primary publication or official alternative once when permitted. If access still fails, request the missing checklist only if it is necessary to complete the requested assessment; continue useful provisional work with explicit limits. Do not retry indefinitely or claim `Reporting guideline compliance passed` merely because the manuscript was polished. An unresolved access gap is a final-delivery limitation, not a reason for endless review rounds.

## Official entry points

- [EQUATOR library](https://www.equator-network.org/reporting-guidelines/)
- [Selecting the appropriate guideline](https://www.equator-network.org/toolkits/selecting-the-appropriate-reporting-guideline/)
- [Using reporting guidelines in peer review](https://www.equator-network.org/toolkits/peer-reviewing-research/)

These links are discovery resources. Resolve current source documents at runtime; no external checklist text is embedded here.
