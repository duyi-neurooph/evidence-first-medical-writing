# Final submission audit

## Trigger and scope

Activate for “投稿前最后一遍检查,” “最后核查,” “修回稿最终检查,” “final check before submission,” or an equivalent final manuscript/package check. Also run it at the end of a requested full-manuscript revision or multi-reviewer workflow before delivering a submission-ready package. A standalone final check produces findings and proposed fixes by default; it does not automatically start multiple review rounds, rewrite the whole paper, submit files, or change authorship.

Use the current manuscript version and supplied abstract, tables, figures, legends, supplements, references, journal instructions, and, for a revision, decision letter and response document. Inventory what is actually available. Apply [reporting-guideline-retrieval.md](reporting-guideline-retrieval.md) first, reusing the task's verified package where appropriate. Missing files or prohibited external access limit the conclusion; never treat an unavailable check as passed.

Keep the audit discipline-neutral. Store author-specific terminology and formatting preferences in the task card or Decision Ledger, not as universal specialty rules. Use [audit-checklists.md](audit-checklists.md) for credibility grading and [architecture-and-evidence.md](architecture-and-evidence.md) for claim support; the checks below add the final cross-file reconciliation.

## Ten checks

### F1 — Abstract, text, tables, and supplements agree

Compare repeated study facts in both directions: population and analysis-set counts, groups, outcome definitions and time points, units, denominators, effect directions, estimates, confidence intervals, and P values. Record both conflicting values and their exact locations. Explain genuine differences in population or timing before calling them contradictions. Do not choose the “right” value by majority vote or silently make one section match another; unresolved data conflicts require author/source confirmation.

### F2 — Citation callouts and reference entries reconcile

Build a two-way inventory: every citation must resolve to an entry, and every listed entry must have an allowed citation location. Include main text, tables, legends, and supplements according to the journal's rules for shared or separate reference lists. Flag uncited entries, missing entries, duplicates, and broken citation fields. A source cited only in an allowed legend is not automatically an orphan. This inventory complements, and does not replace, claim-to-citation verification. Do not remove references or renumber a citation-manager library merely because extraction missed field codes.

### F3 — First mentions, labels, and numbering agree

Check first-mention order separately for tables, figures, and each supplementary series; check panel labels and every cross-reference against the actual object. Confirm that each supplied object is cited and that every callout has a corresponding object. Apply citation-order numbering only when the journal uses it; author-date or alphabetic reference systems need their own rules. Do not require a flow diagram to be Figure 1. Any authorized renumbering must update the objects, legends, all callouts, and relevant response-letter locations together.

### F4 — Flow diagrams and counts are coherent

If a flow diagram exists or the applicable guideline requires one, reconcile screening, inclusion, exclusion reasons, allocation, follow-up, and analysis counts against the text and tables. Apply arithmetic only to mutually exclusive branches with the same unit and stage. Distinguish people, visits, specimens, records, reports, and studies; overlapping analysis sets and multiple exclusion reasons must not be summed as disjoint groups. Report the precise broken transition and needed source verification. If only a figure title or unreadable image is available, the diagram check is `Cannot verify`, not passed.

### F5 — Registration and manuscript agree

If registration is reported, use the exact public identifier to retrieve the official registry record and available history when external access is permitted. This specific lookup does not authorize uploading private manuscript text. Record the URL, access date, record/version dates, and read coverage. Compare design, population, interventions/comparators, recruitment/sample targets, primary and secondary outcomes and their timing, analysis plans where recorded, and registration relative to study dates. Distinguish original entries and later amendments; the current registry page alone cannot establish prespecification. Explain documented changes; report unexplained discrepancies without silently rewriting either record or alleging misconduct. If lookup fails or is forbidden, compare supplied snapshots, state the limitation, and leave live/history checks pending. Absence of a registration statement should trigger a requirement check appropriate to the actual study, not a fabricated identifier or a universal misconduct finding.

### F6 — Abbreviations and terminology remain self-contained

Check first use and consistent later use within each relevant reading unit: abstract, main text, each table, and each figure legend may need separate definitions. Follow journal exceptions for standard abbreviations. Respect a task-specific “always spell out” list when supplied. Avoid unnecessary abbreviations for infrequent terms; do not invent a disease-specific restriction or mechanically replace all later full terms when the text needs to stand alone.

### F7 — Statistical descriptions match the actual summaries

Check that Methods descriptions, values, column labels, and footnotes describe the same summaries. Use mean with standard deviation or median with interquartile range when appropriate to the actual analysis and journal conventions. Clearly distinguish standard deviation, standard error, confidence interval, quartile bounds, IQR width, and minimum–maximum range. If clinically relevant extremes are reported, label them explicitly; a range is not universally prohibited. Never relabel minimum–maximum values as IQR, infer quartiles from extrema, or convert summary measures without the necessary data and analysis authorization. Request the required output when a preferred display is unavailable.

### F8 — Eligibility criteria are justified and consistently applied

Compare inclusion and exclusion criteria across Methods, protocol/registration, flow diagram, and actual analysis population. Assess whether definitions, thresholds, timing, feasibility, safety rationale, and applicability fit the research question. Flag unexplained restrictions, excessive breadth, contradictions, and exclusions introduced after observing outcomes. Do not relax or tighten historical criteria, remove participants, or rewrite the original design on the author's behalf. Distinguish a reporting clarification from a proposed future-study improvement or a reanalysis requiring approval.

### F9 — Contributions are truthful and authorship requirements checked

If a contribution statement is missing, flag the journal requirement and ask for a factual account. Compare named contributors and roles with the byline and other supplied statements; flag ambiguity, unsupported roles, or contradictions for confirmation.

When permitted, check current journal rules and [ICMJE authorship recommendations](https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html), recording source and date. Where the ICMJE framework applies, check evidence for all four elements: substantive research contribution, drafting or substantive critical revision, final approval, and accountability. The author group must confirm these; an absent sentence does not prove a person is ineligible. [CRediT roles](https://credit.niso.org/contributor-roles/) describe contributions and do not alone establish authorship eligibility or author order.

Describe work actually done. Do not assign more roles to senior/first authors or fewer roles to later-listed contributors based on perceived importance. Do not fabricate approval, suppress real contributions, change the byline, or resolve an authorship dispute through a wording edit. If external checks are unavailable, state which policy and factual confirmations remain pending.

### F10 — Revision responses close every comment

For a resubmission, map each editor/reviewer comment and its subparts to a direct response, actual manuscript action or reasoned disagreement, accurate revised location, and closure status. Check that claimed edits or analyses exist in the current files, that page/line/table references remain valid, and that corresponding abstract/table/supplement changes are synchronized. Respect the Decision Ledger so accepted corrections and deleted material do not regress. A justified disagreement may close a comment without an edit; “we agree” or “done” alone does not prove closure. Without the decision/response files, mark this check pending rather than assuming every comment was answered.

## Output and closure

Return a compact final-audit report:

1. **Coverage:** manuscript/file versions examined, journal and guideline sources, access limits, and missing materials.
2. **Priority findings:** use the skill's P0–P3 grading (or the existing editor severity system in a multi-reviewer task), with location, conflicting evidence, consequence, smallest fix, and owner.
3. **Final-check matrix:** one row for F1–F10 plus material subitems, with `Pass / Issue found / Cannot verify / Not applicable`, evidence/locations, planned action, and issue ID. Give a reason for `Not applicable`.
4. **Author decisions:** unresolved numbers, missing analysis outputs, registry differences, contribution confirmations, and incomplete reviewer-response actions.

Reuse existing issue IDs and the Reporting Guideline Matrix rather than duplicating a second diagnosis. Pass applies only to the examined material; “no issue detected” is not a certification of data authenticity, study quality, or journal acceptance. Unresolved Critical/P0 or conclusion-changing issues block a submission-ready claim. Deliver useful findings with explicit pending checks when sources are missing. Recheck changed items and affected cross-references after authorized edits, preserve the original files, and stop when the requested coverage is complete without repeated stylistic rewrites.
