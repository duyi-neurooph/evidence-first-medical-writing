# Version 0.6.0 validation baseline

Date: 2026-11-05

Target version: `0.6.0`

Status: release baseline. Development reports retain their original dates, baseline versions, unreleased state, and test scope; they are historical records, not current release announcements.

## Release checks

- The reviewed runtime skill and reference files are unchanged by release preparation.
- Skill structure/frontmatter, plugin JSON, citation/agent/template YAML, and Git whitespace checks passed.
- Relative Markdown file targets were checked for existence; external URL availability and Markdown anchors are separate concerns.
- Plugin metadata, citation metadata, changelog, and bilingual current-release links identify version 0.6.0.
- The SHA-256 file manifest covers the full public release tree except itself and was regenerated and verified.
- The full-repository distribution uses the established `evidence-first-medical-writing/` root and includes the skill, references, documentation, evaluation records, license, and required notices. It excludes Git internals, private source material, manuscripts, raw data, downloaded guideline originals, and temporary test outputs.
- The existing five gates, independent reviewer isolation, current-guideline workflow, optional data audit, license, and dated model-availability reminder remain unchanged. No new runtime dependency or automatic installation was added.

## Behavioral evidence

The [development report](results-anti-defensive-upgrade.md) records actual answers for 22 synthetic base scenarios and six paired variants. The first grouped run had 21 passes and one partial result: OD01 preserved scientific meaning but omitted a brief change rationale. A narrow local-rewriting clarification and fresh-context retest resolved that result; the spelling-only control also passed again. A separate two-request continuation checked OD15's decision persistence.

The initial cases were run in three separate agent contexts, with several scenarios per context—not 22 individually isolated contexts. A separate read-only review reported no actionable static findings. Release preparation does not claim a new rerun of these behavioral cases after metadata-only changes.

## Scope limits

This is an additive writing-workflow release, not a new clinical evidence source, AI-authorship detector, statistical sign-off, or fraud-detection certificate. Synthetic tests do not establish performance across all manuscripts, models, or host applications.

Live EQUATOR retrieval, numerical source-data reconciliation, tracked-change generation, and a complete new two-round independent clinical review panel were not rerun for 0.6.0. Earlier evidence remains documented in [results-0.5.0.md](results-0.5.0.md) and its linked stage reports. There is no executable repository CI/test harness; the reported package checks and behavioral runs must not be represented as an automated end-to-end clinical validation suite.
