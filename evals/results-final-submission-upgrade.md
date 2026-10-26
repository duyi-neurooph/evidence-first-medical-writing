# Final submission audit validation

Date: 2026-10-26

Base: `7642b9e` (published 0.4.0). Branch: `feature/equator-guideline-retrieval`.

Status: development validation for proposed 0.5.0; not a release announcement.

## Design and integration review

The ten domains are implemented in `references/final-submission-audit.md` and routed through the skill entry point, general audit checklist, submission guidance, and final multi-reviewer delivery. An independent read-only review found no actionable integration gaps. It checked discipline neutrality, factual fidelity, scope boundaries, file preservation, and missing-material statuses.

The source checklist was generalized into methods, not redistributed as a document. No specialty-specific terminology rule, clinical recommendation, private source path, or source original is included. Two potentially unsafe shortcuts were explicitly prevented: changing a minimum–maximum range into IQR without quartiles, and altering contribution roles based on author order. Registration snapshots are distinguished from original registration history.

## Independent forward tests actually run

Fresh read-only contexts received the skill path and synthetic user requests without the expected outcomes, evaluation files, or other reviewers' findings. Both requests prohibited external access and did not authorize manuscript edits.

These runs preceded the later design-confirmation and optional data-audit additions. They record the final-check module's behavior at that stage, not a rerun of the complete final intake. The later additions have separate results in [results-design-and-data-upgrade.md](results-design-and-data-upgrade.md).

### S1 — Cross-file counts, references, order, and summaries: pass

The evaluator located the 118/120 randomized-count conflict and the five-person screening-to-randomization discrepancy, without choosing a corrected value or inventing exclusions. It explicitly avoided summing overlapping analysis sets. It identified the table first-mention problem and the false IQR heading, proposed a truthful range label without changing values, and requested quartiles if an IQR display is needed.

It treated a permitted figure-legend reference as cited, flagged the third entry only as apparently uncited in the supplied material, and did not verify synthetic bibliography placeholders. The response included F1–F10 coverage, kept missing diagrams/registration/contributions and other sources unverified, and did not claim whole-manuscript compliance. No network or manuscript edits were performed.

### S2 — Registry, contributions, and revision closure: pass

The evaluator located the 12/24-week endpoint discrepancy and did not infer original prespecification from a snapshot's last-update date. It requested the identifier, history and relevant protocol versions instead of changing the endpoint. It rejected removal of a contributor's analysis role based on last-author position, distinguished CRediT from authorship eligibility, and left factual roles and approvals for author confirmation.

The response checked comment 1(a) and 1(b) separately, identified insufficient missing-data reporting, and treated a sensitivity-table caption as insufficient evidence of the promised results rather than proof that no analysis occurred. It accepted a reasoned scope-based disagreement on comment 2 within the supplied response, preserved the deleted-background constraint and British English, and did not impose numeric citation ordering on an author-date journal. It returned F1–F10 coverage without networking, automatic editing, new analysis, or extra reviewer rounds.

## Combined static validation (before the later design/data additions)

- Skill frontmatter/structure validation and plugin JSON parsing: passed.
- Local Markdown links: 33 files checked, no missing targets.
- Git whitespace/error check: passed.
- SHA-256 distribution manifest: 43 entries regenerated and verified.
- Targeted terminology scan of the new final-audit reference, fixtures and updated usage documentation found no specialty-specific names or rules.
- Published version metadata remains 0.4.0; proposed 0.5.0 changes are explicitly unreleased.

## Coverage limits

The fixtures are excerpts and synthetic metadata, not complete submission packages. Live registry-history verification, citation-manager field-code handling, document renumbering, file generation, and actual submission were not exercised. The additional cases S3 and S4 in [final-submission-test-cases.md](final-submission-test-cases.md) remain reusable specifications, not claimed behavioral runs. See [results-equator-upgrade.md](results-equator-upgrade.md) for the separate live and offline guideline-retrieval tests.
