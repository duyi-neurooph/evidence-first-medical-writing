# Version 0.5.0 validation baseline

Date: 2026-10-26

Target version: `0.5.0`

Status: release baseline. The linked development reports retain the dates, version state and scope of their original checks; they are not additional release announcements.

## Release checks

- Skill structure/frontmatter, plugin JSON and Git whitespace checks passed.
- Local Markdown-link targets were checked with no missing files.
- Plugin metadata, citation metadata, changelog and bilingual current-release documentation identify version 0.5.0.
- The SHA-256 file manifest was regenerated and verified for the release tree.
- The distribution includes the skill, required references, documentation, evaluation records, license and notices. It does not include private manuscripts, source datasets, the source Word checklist or third-party guideline originals.
- The existing five gates and independent multi-reviewer workflow are retained. No new runtime dependency or automatic software installation was added.

## Behavioral evidence and its scope

| Development stage | Completed checks | Evidence |
|---|---|---|
| Guideline retrieval | Live RCT guideline retrieval/read coverage and offline Critical Perspective handling | [Guideline results](results-equator-upgrade.md) |
| Final submission audit | Cross-file counts/citations/statistical-summary checks and resubmission/registry/contribution boundaries | [Final-check results](results-final-submission-upgrade.md) |
| Design and data integration | Three-turn study-design clarification; actual descriptive calculations and cautious anomaly triage on synthetic data; separate data agreement and manuscript-logic checks | [Design/data results](results-design-and-data-upgrade.md) |

The first two stages preceded the later design-confirmation and optional data-audit additions. Independent integration review identified and corrected the earlier unconditional event-count bound: people with events, repeat events and rates now use their appropriate denominators. Historical 0.4.0 multi-reviewer checks remain documented in [results-0.4.0.md](results-0.4.0.md); they were not all repeated for this release.

## Limits

Reusable test specifications are not all executed runs. A complete online two-round manuscript workflow was not rerun after the final additions. No real patient dataset, live registry-history audit, production document-generation pipeline or specialist forensic validation was performed. These checks do not establish clinical validity, fraud-detection accuracy, privacy compliance or suitability for every statistical model. Missing source access and untested output formats must remain explicit during actual use.
