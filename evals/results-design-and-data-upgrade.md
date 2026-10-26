# Design confirmation and optional data-audit validation

Date: 2026-10-26

Base: published 0.4.0. Branch: `feature/equator-guideline-retrieval`.

Status: development validation for proposed 0.5.0; not a release announcement.

## Independent forward runs

Fresh contexts read the skill and task-required references but not evaluation criteria, other findings or implementation commentary. All fixtures were synthetic and prohibited internet access. No repository or source-data edits were authorized.

### D1 — Three-turn author design clarification: pass

The first response did not accept an RCT label from two treatment groups, historical records and follow-up alone. It asked three focused questions about allocation, selection and chronology, disclosed unavailable guideline verification, and offered data checks as optional.

After the author described routine-care treatment, baseline-based selection and a research question developed after all outcomes had occurred, the evaluator explained a retrospective comparative observational cohort rather than an RCT. It recorded the factual confirmation, proposed STROBE/possible RECORD as candidates without claiming live verification, and did not invent randomization details. The third author turn confirmed the facts, declined raw data and supplied one Methods sentence. The evaluator reused confirmation, respected refusal and no network, and gave location-specific limited manuscript findings without demanding data or judging unseen sections.

### D2 — Descriptive data reproduction and anomaly triage: pass

The evaluator executed JavaScript arithmetic on all six supplied CSV rows and documented formulas, n, sample-SD denominator, selected variables, filters and integer-display tolerance. It found mean age A=50 rather than 51 and week-12 mean A=12 rather than 13; the corresponding B values and reported SDs reproduced.

It compared all nine cross-group record pairs on four specified variables and located three matching multivariate profiles. It did not infer fabrication, participant duplication or authenticity, noted the synthetic context and plausible but unconfirmed explanations, and did not treat zero observed events as proof of safety. It identified within-person pairing as a concern for the reported unpaired test, distinguished an analysis error from a description error, and did not silently change the test. It also observed zero variability in within-person changes, avoiding an unsupported automatic paired-test substitution. No inferential test, source modification or external transfer was performed. Unseen figures and original-record provenance remained unverified.

### D5 — Correct Table 1, incorrect narrative and figure mapping: pass

The evaluator executed read-only calculations and separately reported that the specified Table 1 counts/means reproduced, while internal logic failed. It located the reversed B-versus-A score direction in R1, the wrong group denominator and inconsistent percentage in R2, and the reversed group-to-mean mapping in the plotting specification F1. It did not infer that the unseen rendered figure was checked.

It correctly allowed nine repeat events in a three-person group, distinguished the two people with events from the group of three, and clarified the ambiguous meaning of “among three participants.” It did not let agreement between the erroneous prose and erroneous figure specification overrule the data/Table 1. No inferential analysis, source edit, causal claim, authenticity certificate or full-manuscript pass was produced.

## Integration review and correction

An independent read-only review checked both new modules, entry-point/Contract/retrieval/final-check hooks and bilingual documentation. It found one real contradiction after the two-layer logic addition: older core checks treated every event numerator as bounded by a participant denominator. Both were corrected to distinguish people with events from repeat-event counts and rates, with matching population/window requirements.

The review also noted that earlier guideline test specifications did not all provide an author-confirmation exchange. The suite now explicitly requires that gate, supplies follow-up facts for key scenarios, and records unspecified scenarios as awaiting clarification rather than claiming selection success.

The independent reviewer rechecked the event-count corrections and directly related F1 logic; no remaining material contradiction was identified.

## Final static validation

- Skill frontmatter/structure and plugin JSON: passed.
- Local Markdown links: 37 files checked, no missing targets.
- Git whitespace/error checks: passed.
- SHA-256 distribution manifest: 47 entries regenerated and verified.
- Targeted scan of new reference modules, fixtures and updated usage documentation: no specialty-specific names or rules.
- Plugin/CITATION version remains the published 0.4.0; CHANGELOG marks proposed 0.5.0 as unreleased. No release, tag or merge is part of this change.

## Limits

D3/D4 are reusable specifications, not separately executed behavioral runs. No real patient dataset, identifiable information, production spreadsheet, live registry, specialist installation or deep forensic analysis was used. These tests do not establish fraud-detection accuracy, clinical validation, privacy compliance or correctness for all statistical models. Earlier guideline and final-submission tests remain stage-specific results; a new complete online two-round manuscript workflow was not rerun after these additions.
