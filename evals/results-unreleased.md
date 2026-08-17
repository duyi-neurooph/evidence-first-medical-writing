# Unreleased feature validation

Date: 2026-08-17

Branch: `feature/independent-multi-reviewer-workflow`

Target version: `0.4.0`

Status: release-candidate evidence, not a published release baseline

## Static validation

| Check | Result |
|---|---|
| Skill structure (`quick_validate.py`) | Pass |
| Plugin JSON parse | Pass |
| Git whitespace/error check | Pass |
| Local Markdown-link targets | Pass: 27 files checked, 0 missing |
| New reference and evaluation routes | Pass |

## Cold-start workflow evaluation

Fresh, read-only contexts loaded the local skill by path and were not shown the pass criteria.

| Case | Mode | Result |
|---|---|---|
| RCT: nonsignificant primary endpoint, secondary PP signal, mixed publication-status citation cluster | Sequential fallback | Initial partial: scientific handling passed, but one run omitted the fixed capability reminder. The entrance rule was strengthened; fresh retry passed. |
| Diagnostic accuracy: ambiguous `this study`, secondary analysis as independent validation, mixed table hierarchy | Sequential fallback | Pass |
| Critical Perspective: protected conclusion, deleted background, unpublished data, slogan-like prose | Sequential fallback | Pass |
| Systematic review/meta-analysis: five small studies, `I²=88%`, conflicting synthesis advice, missing sources | Sequential fallback | Pass |
| Adversarial bundle: Round 2 restoration of deleted text; invented safety Major issue; no-subagent fallback | Sequential fallback | Pass |

Observed behavior after the reminder fix:

- outputs were labeled as simulated peer review;
- the capability reminder preceded the sequential-fallback disclosure;
- no missing values, analyses, sources, journal rules, or publication metadata were invented;
- primary/secondary endpoint hierarchy and publication status were preserved;
- editors rejected unsupported fixed-effect precision seeking, fabricated safety-table demands, and automatic restoration of deleted text;
- unresolved scientific choices remained author decisions;
- Decision Ledger and Non-Regression rules blocked reintroduction of deleted material;
- reviewers were allowed to report no additional major concern within their remit.

## Parallel isolation probe

Three independent, read-only reviewer contexts received the same frozen systematic-review package and different remits. They did not receive one another's reports or a prewritten defect list.

| Reviewer | Distinct emphasis |
|---|---|
| Clinical-domain reviewer | clinical interpretability, applicability, and the absent PICO/outcome |
| Systematic-review methodologist | search reproducibility, protocol, risk of bias, and synthesis eligibility |
| Meta-analysis statistician | missing effect estimates/uncertainty, model rationale, heterogeneity, and small-study inference |

All three rejected the unsupported efficacy claim without inventing data. Their rationales and severity judgments differed, demonstrating useful role separation rather than mechanical convergence. The editor could preserve the reports, deduplicate overlap, and adjudicate from remit relevance and evidence rather than majority vote.

## Validation limits

- The fixtures contained no full manuscript, journal template, protocol, raw analysis, or verifiable full references.
- Tracked-change document generation and journal-specific formatting were therefore not tested.
- Most article-type tests intentionally exercised the documented sequential fallback; the isolation probe separately tested actual parallel reviewer isolation.
- Package metadata is prepared for `0.4.0`; this file should be renamed or superseded by a versioned baseline only after the release is actually published.
