# Verify references without editing the manuscript

Use this audit for an explicit reference check, a substantive change to a citation or the claim it supports, or any submission/resubmission check. “投稿前检查” is sufficient: do not wait for a second request. In a whole-manuscript review or final check, audit **every bibliography entry**, including separate supplement lists, not just the cited examples. For an isolated change, check the affected entries and claims. Translation, spelling and language polishing alone do not launch a bibliography audit. A narrow reference-only request does not require a study-design interview or a full manuscript audit.

## 1. Inventory and route by source

Work on a read-only copy. Give each entry a stable ID (prefix supplement IDs); retain its original citation string, key, callouts and manuscript version in the private audit. Extract records from the provided text, tables, legends and bibliography/library. Reconcile extracted counts with the source; an unparseable row is pending, never silently dropped. If no bibliography is supplied, ask for it, complete the portions available and mark F2 incomplete.

| Cited object | Authoritative route and identity evidence |
|---|---|
| English biomedical journal article | Query PubMed and Crossref as applicable. Retrieve the actual record behind an identifier or search candidate. Compare full title, author list or group, journal and publication year; include volume/pages/article number if provided. If a database lacks a field, consult the publisher's version of record for that field. One decisive authority suffices; a second database need not index it. |
| Chinese guideline or consensus | Start with the original journal or the issuing society's publication. Chinese medical databases can locate it; open the original and verify title, authors/group, issuing body, edition/year and any replacement. Distinguish a translation, interpretation or news notice from the guideline itself. |
| Trial registration | Open the exact record at the responsible registry. Check identifier, official title, sponsor and record date/history as relevant. Do not substitute a results paper for the registration. |
| WHO/govt document, medicine label, journal instructions | Use the issuer's official publication/document, regulator's label for the product, formulation and jurisdiction, or actual journal's author instructions. Check version/revision date; for an undated living page record access date and explicitly unknown edition. No DOI or PMID is required. |

Respect external-access restrictions. Search only public bibliographic fields, never manuscript passages, patient data, unpublished titles/results, private author notes or the library itself. With external access prohibited, use readable authorized originals already supplied; otherwise mark pending with the cause. Normal network failure is not a finding of fabrication. Do not bypass access controls.

## 2. Run the bundled article verifier

Prepare a minimal JSON array in the private task workspace. The author need not convert files. Keep only actual fields: omit unknown identifiers; do not invent author names or expand “et al.” from memory. Preserve author order and truncation markers. Use the real source type instead of passing official documents to a journal search:

```json
[{"id":"R1","type":"journal","title":"<published article title>","authors":["<first author>","et al."],"journal":"<journal>","year":2020},
 {"id":"S1","type":"guideline","title":"<official title>","year":2024}]
```

Invoke [the bundled verifier](../scripts/verify_references.py) from the installed skill folder, without a second skill or an upstream pipeline:

```sh
python3 -B scripts/verify_references.py /path/to/private/entries.json
```

Use `--offline` when network calls are not permitted. The script reports to standard output; never direct it into an input or original library. Without Python, perform the same checks by opening the authoritative sources using host tools; do not claim the script ran. Without either capability or local originals, leave the entries pending.

The article verifier is a first pass, **not** a semantic reader or a universal document parser. For non-journal objects, continue from the route in its output: actually open the issuing authority's original, compare the identifiers/metadata, and record the adjudication in the final audit separately from the raw script result. A link, search snippet, HTTP success or a URL supplied by the author is not verification. One original that uniquely confirms an item can resolve it without a DOI/PMID. Do not overwrite the earlier machine evidence.

- Resolve supplied DOI and PMID, not just their syntax. If both are present, reconcile them to the same work; preserve discrepant IDs and do not silently choose one. A DOI for a different paper is a conflict even when its landing page opens. Normalize identifier spelling for duplicate detection, retain all original entry IDs, and never merge a correction, protocol, secondary analysis or follow-up into another work solely because the studies are related.
- With neither identifier, search produces candidates only. Compare the retrieved official titles. Ignore case, spacing and ordinary typographic punctuation only where meaning is preserved. Preserve numbers, signs, doses, positive/negative status, study/report type, follow-up duration and direction. Similarity, rank or a shared author cannot settle identity. Validate all supplied metadata, recognizing legitimate group authors, declared truncation, journal abbreviations and online vs issue years; retain which source supports each discrepancy resolution.
- If an exact title plus available fields distinguish one work, mark **verified**. If a field conflicts or cannot be checked, multiple plausible works remain, lookups are unavailable, or a partial search cannot establish uniqueness, keep **pending** with the competing records, conflicting fields and next action. Do not treat a partial/abbreviated database title as proof of a different paper if a stronger record explicitly binds the IDs and formally resolves the fields. Seek a publisher or original when indices disagree; never average incompatible records.

### Format article titles separately from verifying identity

When drafting a bibliography or checking it before submission, use the **target journal's reference style** for all English journal-article titles, including those in the supplement. If no style is specified, use sentence case consistently: capitalize the first word and proper names; follow the target style for the first word after a colon. Keep meaningful capitalization such as **China**, **Chinese**, named trials, **HIV**, **BRCA1**, and case-sensitive units or scientific notation. Do not apply a blanket lowercase or title-case conversion. These are article-title rules, not instructions to recase journal names, other publication types, identifiers or non-English titles.

Keep the retrieved title as evidence; the manuscript's display title can differ in ordinary capitalization without being a different work. For example, *Health Outcomes in Chinese Adults With HIV* can display as *Health outcomes in Chinese adults with HIV*. In an audit, report inconsistent capitalization as a **style issue**, separately from identity and claim support. The verifier folds case for lookup: if letter case could change the scientific meaning (for example, `mGy` vs `MGy`), inspect the publisher's original rather than clearing the difference as cosmetic. Do not rewrite the author's bibliography or library during an audit; propose the display form, and apply only when authorized.

## 3. Check what the article actually supports

Extend the existing Claim–Citation Map. Open the original for every claim bearing a main conclusion, numerical effect, treatment recommendation, diagnostic criterion or reviewer challenge. Check each distinct clause and its specific citation, including tables and legends. Distinguish the original study from its protocol, secondary analysis or follow-up; prefer original data for numerical results. Compare population, intervention/exposure, comparator, endpoint, time, analysis set, direction, effect size, units and uncertainty where relevant. Cite location (section, page, table/row, figure or recommendation number). A related topic, matching number, vague paraphrase or correct DOI is not evidence of support.

Record **two separate judgments**:

| Output | Minimum traceable fields |
|---|---|
| Identity, one row per entry | Entry ID and original citation; verified / pending; fields compared; official record URL(s) and date/version; candidate/ID conflicts; duplicate links; limitation or next step. |
| Support, one row per priority claim–source pair | Manuscript location and exact sentence/clause; entry ID; source URL, scope read and exact source location; what it actually measured; **supports / partly supports / does not support / insufficient evidence**; mismatch and proposed author action. |

If only the abstract is accessible, say which facts are directly reported there. Never infer an unreported outcome, subgroup, effect size, recommendation or table. Use **insufficient evidence** when unavailable detail could settle the question; use **does not support** when the inspected evidence establishes a material mismatch. A structural outcome is not a clinical benefit. Bibliography-only input can establish identity, not support for absent manuscript claims. Mark non-priority pairs not assessed, rather than inflating the number checked.

Deliver a problem-first list (identifier conflicts, unsupported/overstated claims, duplicate IDs, ambiguity, inaccessible sources), traceable rows and coverage: total listed / assessed / verified / pending, plus priority claim–source pairs read / limited or unavailable. Withhold an F2 pass while material gaps remain. Changing the citation, claim, source version or numbering invalidates its old judgment; recheck the affected rows. Preserve originals and the reference manager library. Propose corrections or replacements for author decision; apply them only on explicit request.
