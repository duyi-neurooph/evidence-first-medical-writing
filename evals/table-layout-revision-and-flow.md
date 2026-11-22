# Table layout, ordinary Word revision and participant flow

These are offline, fictional regression cases, not reports of completed runs. Give a fresh reader the relevant input and request, **not** the acceptance checks. Score scientific content separately from appearance. Use a disposable directory for Word fixtures and output; visual and annotation checks require actual files, not a description of the edits.

## T1 — Read a compact table without the paper

**Input and request.** Reformat a two-group rehabilitation table; the author permits presentation edits only. Each current group heading repeats every summary convention. The only group identifiers needed are Home (20 people) and Clinic (24 people). Here are the approved rows, in Home / Clinic order:

| Characteristic | Home | Clinic | Supplied meaning |
| --- | --- | --- | --- |
| Walk distance | 312 (48) | 326 (52) | metres, mean (SD), at week 6 |
| CRP | 4 (2–6) | 5 (3–7) | mg/L, median (IQR), at baseline |
| Used a walking aid | 6 (30%) | 6 (25%) | counts and percentages of each group at baseline |
| Completed diary | 9/18 (50%) | 14/20 (70%) | percentages of those issued a diary at week 6 |

The target journal allows table notes; it does not prescribe the wording or footnote symbols. No clinical interpretation requested.

**Pass.** Group headers identify groups and sizes without carrying a paragraph of row definitions. From the table alone, a reader can correctly identify time, units, and summary convention for each row and the special diary denominator. Use concise headings, row labels, or clearly scoped notes as appropriate; one blanket “all values are mean (SD)” note fails. Every supplied quantity and relationship survives. **Control:** repeat with just the walk distance measurement at baseline and week 6 in both groups, all in metres and all mean (SD); one shared unit/convention is sufficient. Do not force a shared unit in the mixed table or repeat the same qualification in every cell of the homogeneous table.

**Crowded header control.** A separate column reads “Percentage of scheduled visits for which attendance was documented as a percentage of scheduled visits”; its note repeats the entire heading and adds that only weekday visits were eligible. After shortening, the reader still knows what was documented, what the denominator counts and which visits qualify. Do not recast this as the percentage of patients who attended. Do not repeat the heading verbatim in the note.

## T2 — Siblings, wrapped labels and footnote anchors

**Input and request.** Supply the T1 table data and set a narrow first column so that the long category below wraps. Add “Discharge destination” with the categories Home, Residence with overnight rehabilitation support, and Other (Home group: 12, 5, 3; Clinic group: 13, 7, 4). The author confirms one exact omnibus test for the factor, P = 0.731. The CRP row has P = 0.214 by rank-sum test; its measurements in both groups use a prespecified baseline sampling window of 48 hours. A separate baseline SpO₂ row shows 97 (1) and 96 (2), in %, mean (SD). The supplied abbreviation note reads: SD, standard deviation; SpO₂, peripheral oxygen saturation; CRP, C-reactive protein; IQR, interquartile range. Stars are already reserved for significance. Improve layout, method mapping and the abbreviation note. Do not recompute results.

**Pass.** In the rendered table all three children, including the first and last, start at the same inset relative to the parent. The second line of the long child aligns with its own text, not the parent margin. Other top-level rows remain at the parent level. The test note for each result is keyed by a true superscript on its **P value**; the factor has only its overall P on the parent row. A separate superscript on the **CRP label** scopes the sampling-window note to that variable across groups; it is neither a test nor a qualification on one group value. Each marker resolves unambiguously to its own note without reusing significance stars. The abbreviation list reads CRP, IQR, SD, SpO₂ (alphabetical by abbreviation; sorting the expansions would reverse the last two), with the supplied definitions. No new tests or pairwise P values. A Markdown preview cannot establish Word superscripting or paragraph indents: inspect the DOCX formatting and rendered wrap before scoring those items.

**Value-specific control.** The author adds “Clinic SpO₂ is based on 22 available readings; Home has all 20” and requests a footnote for the exceptional denominator. The marker belongs on the Clinic summary 96 (2), not the SpO₂ label, the Home value, or a P value. Do not change either group's overall header count.

**Note-order control.** With no contrary template, check that any shared summary convention is visibly distinct from keyed notes (one per line) and the separate abbreviation list. If the evaluator supplies a mandatory journal template ordering abbreviations first, preserve that order without breaking the marker mappings.

## W1 — A subsequent, ordinary Word revision

**Fixture for the evaluator.** Make a small editable DOCX from fictional material. Use the accepted T2 layout with its group header, parent and child paragraphs, mapped superscripts and abbreviation note. Set a nondefault width that wraps the long child, plus a functional rule under the group headers. Save this accepted baseline independently. In a working copy, include: (1) a tracked change to retain “Clinic” in place of “Center”; (2) a comment on the header, “Keep this rule and these widths”; (3) an inline author direction next to the table, “[Author: keep all category indents as shown.]”. Retain a copy of this annotated input. Add the sentence “The visit occured in June.” Do not include any other intentional content differences between the approved and annotated views.

**Input and request.** Supply the annotated file: “I have approved the layout you see in my edits and notes. Fix the spelling in the sentence. Give me a clean manuscript and a marked copy that retains my review trail.” No new formatting brief or scientific review.

**Pass.** Compare both outputs with the author's approved view, not with the pre-change text or an older stock style:

- The clean file reads “Clinic” and “occurred”; no change markup, comment text, inline directive, or process receipt remains in the deliverable. The marked copy retains the original tracked decision, comment with its anchor, and inline direction, and makes the requested correction identifiable; these are not two copies of the clean file.
- Table values, labels, notes, markers, methods, and all other scientific content are unchanged. Both render the approved header rule, widths, sibling/wrap alignment, and superscripts. Inspect the Word annotation structures as well as visible pages; a paragraph-text comparison alone cannot verify either trail or appearance. The supplied file remains intact.
- In chat, give a short, specific receipt for the correction and the formatting retained or actually checked. If reliable annotation inspection or rendering is unavailable, identify the unverified part rather than saying it passed. No receipt inside either manuscript.

**Negative control.** Instead ask for a review only and provide only pasted table text, with no accessible Word source. Report what the text supports; do not return an allegedly revised file or claim to have seen tracked changes, comment anchors, styles, or actual wraps.

**Second-round control.** Include a second, unapproved draft saved more recently. Its Table 1 changes a number and resets indents; both tables share a paragraph style. On the approved file the user now asks only for a shorter Table 2 header. Use the explicitly chosen baseline, not the latest timestamp. Verify the single header change against it; Table 1's numbers, styling and notes, and Table 2's other content, must not change. A global style change that alters the approved Table 1 fails even if every cell still contains the same text.

## F1 — An irrelevant fact is not a caption footnote

**Input and request.** Prepare the public labels and legend for a community hearing cohort flowchart. Of 80 adults assessed, 8 failed the prespecified age criterion; 72 enrolled. Of the 72, 6 did not return for the hearing test; 66 completed it and entered the primary analysis. A clinic log also records that 21 of the 72 received a large-print appointment reminder; reminder format had no bearing on eligibility, follow-up, group assignment or analysis. All counts are confirmed people. No special journal legend requirement.

**Pass.** A reader can follow 80 → 72 → 66 and identify both losses and the primary analysis set. The reminder detail appears nowhere in the public figure, title, caption or legend; moving it out of a node and into a footnote does not pass.

**Meaning-changing control.** Instead the lab log lists 78 completed **tests** from the same 66 people: 54 had one test and 12 had two; the analysis uses the first test per person. The requested figure must now explain how 78 tests relate to the analysis of 66 people. Make the counting units and repeated tests clear in the nodes or a short necessary note; do not call 12 people excluded or silently drop the unit change to shorten the figure. The appointment-reminder detail is still irrelevant.

## Release observations (1.0.7)

- A separate synthetic two-round DOCX smoke test used a table with three wrapped category labels, actual superscripts and keyed notes. It edited only a header in a second table in round two. In bundled LibreOffice at 150 dpi, all seven label lines shared the same child indent. The protected first table and its notes were identical in the two renders (zero changed pixels in that region); the clean outputs had no remaining Word comments. This tests one rendering path, not the desktop Word application or every case above.
- A separate text-only, offline reader trial correctly used the author-designated baseline instead of the newer draft, kept the unrelated table and figure decisions, distinguished variable and value markers, and did not claim to have edited or visually verified an unavailable Word document.
