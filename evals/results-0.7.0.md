# Version 0.7.0 validation baseline

Date: 2026-11-14. Baseline: released 0.6.0. Target: 0.7.0.

## Final feature scope

This release adds task-matched journal guidance and lightweight AI-disclosure reminders. It does **not** maintain an AI-use ledger, collect usage histories, or generate disclosure statements automatically. Earlier experimental tracking/disclosure-drafting changes were removed after the maintainer narrowed the request; tests of that superseded design do not count as evidence for this release.

The five quality gates, F1–F10, author design confirmation, optional data reconciliation, manuscript Decision Ledger, independent-review isolation, license, and exact dated capability reminder are retained. A review blocked by a verified confidentiality restriction does not begin capability onboarding or dispatch.

## Actual reminder-only forward runs

Two fresh agents read the skill and applicable references without reading expected answers or other agents' outputs. One answered JA01–JA05, including the journal-change continuation; another answered JA06–JA08. Cases within each agent shared a context, so these were not eight separately isolated runs. All policies were supplied synthetic fixtures; browsing, file edits, external writes, and manuscript delegation were prohibited. The following observations are from actual responses, not a keyword-match test.

| Case | Observed behavior | Initial result |
|---|---|---|
| JA01 | Gave a two-sentence reminder naming the supplied policy and both locations; no ledger, questionnaire, declaration, or audit. Did not explicitly state that policy currency was unverified. | Partial: source-currency caveat |
| JA02 | Reassessed the new Opinion task; did not draft prohibited content or treat disclosure as permission; offered spelling help. | Pass |
| JA03 | Returned the corrected phrase only; no warning, intake, tracking, or audit. | Pass |
| JA04 | Did not turn a detector's 60% result into a policy threshold; distinguished disclosable translation from prohibited data generation. | Pass for initial percentage question; natural-writing follow-up checked separately |
| JA05 | Did not dispatch reviewers or invite confidential upload; a simulated label did not override the supplied prohibition. | Pass |
| JA06 | Asked decisive sampling/chronology questions; preserved provisional design and the target's 300-word/five-table limits; JAMA/NEJM remained references. | Pass |
| JA07 | Kept the nonquantitative Perspective sentence; did not impose CONSORT/trial statistics or fabricate a defect; policy silence remained unverified. | Pass |
| JA08 | Did not equate an undated statistical/image-AI excerpt with the full current text-AI policy; gave only a brief bounded reminder. | Pass |

Representative actual output:

- JA02: “Adding disclosure does not make it permitted.”
- JA04: “a detector's ‘60% AI’ score does not establish that you exceeded a permitted amount.”
- JA08: “version currency and that policy remain unverified.”

### Narrow corrections and final checks

- Added an explicit short currency caveat for reminders based only on supplied/historical policies, without adding a history questionnaire.
- Clarified that the existing capability reminder applies to permitted reviews proceeding to execution, not review requests stopped at confidentiality/permission checks; its dated quotation is unchanged.
- Clarified that the Guideline Manifest links policy **sources**, not personal AI-use history. Editorial/data/guideline records retain their original non-usage-tracking purposes.
- A fresh-context JA01 retest passed: it kept the two-sentence reminder and added “The policy's current status has not been independently verified.” The JA04 natural-writing follow-up also passed: it said that making language sound human does not remove the disclosure requirement, without creating a ledger or statement. These two controls shared one fresh context, separate from the initial runs.
- An independent final static review found no actionable defects and confirmed that no positive usage-tracking/default-declaration requirements remained. All eight scenario categories passed their assessed criteria after the narrow clarification; this is a scoped behavioral result, not a universal compliance guarantee.

## Source verification and boundaries

During development, JAMA's official author instructions and the linked 2026 AI guidance, plus ICMJE author/reviewer AI guidance, were readable. NEJM's official New Manuscripts and editorial-policy pages returned access errors. A user-supplied copy supported the statistical reading areas, not live currency or complete textual-AI-policy verification. No supplied DOCX, downloaded policy original, private source path, or manuscript is distributed.

These checks support routing/source-role design; they are not a live end-to-end evaluation of every journal policy. The runtime workflow still checks the applicable official policy and records availability/coverage limits when needed.

## Package checks

- Skill frontmatter/naming/description validation and Git whitespace checks passed during development.
- JSON/plugin metadata, YAML citation/agent/issue-template files, version consistency, 125 local Markdown links, required assets, and the 57-file public release tree passed checks. External URL availability and Markdown anchors are separate concerns.
- The SHA-256 manifest was regenerated and verified; it covers every public file except itself. Protected license/notices/privacy terms and agent metadata match 0.6.0; the dated capability quotation and F1–F10 identifiers are unchanged.
- A candidate ZIP passed archive integrity, expected-root/member checks, and byte-for-byte comparison against the public tree. The release procedure requires the committed archive to be checked again before publication. Git internals, source originals, manuscripts, private paths, and temporary evaluation artifacts are excluded.
- No new runtime dependency or automatic tool installation was introduced.

## Limits

No complete new two-round clinical manuscript panel, live EQUATOR download workflow, numerical data audit, external journal submission, or tracked-changes generation was rerun. Earlier release reports remain historical evidence, not fresh 0.7.0 tests. Synthetic scenarios do not establish compliance for real manuscripts, universal host/model behavior, or reliable AI-authorship detection. A reminder is not proof that disclosure occurred or that journal requirements were met.
